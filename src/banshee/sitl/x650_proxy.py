"""A simulated stand-in for the Holybro X650, made from PX4's x500 model. Runs inside the VM.

This is a proxy, not an X650 model: the mass, size and thrust are set from published figures, and
the rest is scaled. It exists to measure how the envelope's braking, overrun and drift terms move
with mass. Its results are simulation results on this proxy, and no substitute for flight logs.

Published: 650 mm wheelbase, 2,000 g kit, takeoff limit 6,300 g at 70% throttle (Holybro); up to
3.3 kg per motor with a larger prop (T-Motor). The owner states about 4-5 kg at takeoff.

Estimated here: 3.0 kg per motor with the 15-inch prop; inertia scaled as m * L^2; drag scaled so
that the deceleration per unit speed from rotor drag matches the x500's; motor time constants.
"""

from __future__ import annotations

import argparse
import math
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

G = 9.81
X500_MASS_KG = 2.0
X500_ARM_M = 0.174
X500_IXX = 0.02166666666666667
X500_IZZ = 0.04000000000000001
X500_MOTOR_K = 8.54858e-06
X500_ROTOR_DRAG = 8.06428e-05
ROTORS_MASS_KG = 4 * 0.016076923076923075
X650_ARM_M = 0.23
THRUST_PER_MOTOR_N = 3.0 * G
MAX_ROTOR_RAD_S = 700.0
TIME_CONSTANT_UP_S = 0.10
TIME_CONSTANT_DOWN_S = 0.15


@dataclass(frozen=True)
class Proxy:
    name: str
    autostart: int
    mass_kg: float
    drag_factor: float = 1.0

    @property
    def motor_k(self) -> float:
        return THRUST_PER_MOTOR_N / MAX_ROTOR_RAD_S**2

    @property
    def inertia(self) -> tuple[float, float]:
        scale = (self.mass_kg / X500_MASS_KG) * (X650_ARM_M / X500_ARM_M) ** 2
        return X500_IXX * scale, X500_IZZ * scale

    @property
    def rotor_drag(self) -> float:
        """Rotor drag that gives the x500's deceleration per unit speed, times ``drag_factor``."""
        rate = _decel_rate(X500_MASS_KG, X500_MOTOR_K, X500_ROTOR_DRAG)
        hover = _hover_rotor_rad_s(self.mass_kg, self.motor_k)
        total = self.mass_kg + ROTORS_MASS_KG
        return self.drag_factor * rate * total / (4 * hover)

    @property
    def thrust_to_weight(self) -> float:
        return 4 * THRUST_PER_MOTOR_N / ((self.mass_kg + ROTORS_MASS_KG) * G)


def _hover_rotor_rad_s(mass_kg: float, motor_k: float) -> float:
    return math.sqrt((mass_kg + ROTORS_MASS_KG) * G / (4 * motor_k))


def _decel_rate(mass_kg: float, motor_k: float, rotor_drag: float) -> float:
    return 4 * rotor_drag * _hover_rotor_rad_s(mass_kg, motor_k) / (mass_kg + ROTORS_MASS_KG)


PROXIES = (
    Proxy("x650_proxy", 4901, 5.0),
    Proxy("x650_proxy_4kg", 4902, 4.0),
    Proxy("x650_proxy_lowdrag", 4903, 5.0, drag_factor=0.5),
)


def _set_tag(text: str, tag: str, value: float, *, count: int = 0) -> str:
    out, found = re.subn(rf"<{tag}>[^<]*</{tag}>", f"<{tag}>{value:.8g}</{tag}>", text, count=count)
    if not found:
        raise ValueError(f"no <{tag}> in the source model")
    return out


def base_sdf(source: str, proxy: Proxy) -> str:
    """The x500_base model with this proxy's name, mass, inertia and arm length."""
    ixx, izz = proxy.inertia
    text = source.replace("<model name='x500_base'>", f"<model name='{proxy.name}_base'>")
    # Arm length first: the new inertia values can contain the old arm length's digits.
    text = text.replace(str(X500_ARM_M), str(X650_ARM_M))
    text = _set_tag(text, "mass", proxy.mass_kg, count=1)
    text = _set_tag(text, "ixx", ixx, count=1)
    text = _set_tag(text, "iyy", ixx, count=1)
    return _set_tag(text, "izz", izz, count=1)


def model_sdf(source: str, proxy: Proxy) -> str:
    """The x500 model with this proxy's motors."""
    text = source.replace("<model name='x500'>", f"<model name='{proxy.name}'>")
    text = text.replace("model://x500_base", f"model://{proxy.name}_base")
    text = _set_tag(text, "timeConstantUp", TIME_CONSTANT_UP_S)
    text = _set_tag(text, "timeConstantDown", TIME_CONSTANT_DOWN_S)
    text = _set_tag(text, "maxRotVelocity", MAX_ROTOR_RAD_S)
    text = _set_tag(text, "motorConstant", proxy.motor_k)
    return _set_tag(text, "rotorDragCoefficient", proxy.rotor_drag)


def airframe(source: str, proxy: Proxy) -> str:
    """The gz_x500 airframe with this proxy's geometry and motor range."""
    text = source.replace("Gazebo x500", f"Gazebo {proxy.name}, a proxy for the Holybro X650")
    text = text.replace("PX4_SIM_MODEL:=x500", f"PX4_SIM_MODEL:={proxy.name}")
    text = re.sub(
        r"(CA_ROTOR\d_P[XY]\s+-?)0\.\d+",
        lambda found: f"{found.group(1)}{X650_ARM_M}",
        text,
    )
    text = re.sub(
        r"(SIM_GZ_EC_MAX\d\s+)\d+", lambda found: f"{found.group(1)}{MAX_ROTOR_RAD_S:.0f}", text
    )
    return re.sub(
        r"(SIM_GZ_EC_MIN\d\s+)\d+",
        lambda found: f"{found.group(1)}{0.15 * MAX_ROTOR_RAD_S:.0f}",
        text,
    )


def install(px4: Path) -> None:
    """Add the proxies to the VM's PX4 tree as untracked files. PX4's commit is unchanged."""
    models = px4 / "Tools/simulation/gz/models"
    airframes = px4 / "build/px4_sitl_default/etc/init.d-posix/airframes"
    for proxy in PROXIES:
        for suffix, source, make in (
            ("_base", "x500_base", base_sdf),
            ("", "x500", model_sdf),
        ):
            target = models / f"{proxy.name}{suffix}"
            target.mkdir(exist_ok=True)
            shutil.copy(models / source / "model.config", target / "model.config")
            config = target / "model.config"
            config.write_text(
                config.read_text(encoding="utf-8").replace(source, f"{proxy.name}{suffix}"),
                encoding="utf-8",
            )
            sdf = (models / source / "model.sdf").read_text(encoding="utf-8")
            (target / "model.sdf").write_text(make(sdf, proxy), encoding="utf-8")
        frame = (airframes / "4001_gz_x500").read_text(encoding="utf-8")
        (airframes / f"{proxy.autostart}_gz_{proxy.name}").write_text(
            airframe(frame, proxy), encoding="utf-8"
        )
        print(
            f"{proxy.name}: {proxy.mass_kg} kg, thrust/weight {proxy.thrust_to_weight:.2f}, "
            f"k {proxy.motor_k:.4g}, drag {proxy.rotor_drag:.4g}, inertia {proxy.inertia}"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--px4", type=Path, required=True)
    install(parser.parse_args(argv).px4)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
