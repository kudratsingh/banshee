"""The X650 proxy's derived values and its edits to PX4's x500 files."""

from __future__ import annotations

import math

import pytest

from banshee.sitl.x650_proxy import (
    MAX_ROTOR_RAD_S,
    PROXIES,
    X500_MASS_KG,
    X500_MOTOR_K,
    X500_ROTOR_DRAG,
    _decel_rate,
    airframe,
    base_sdf,
    model_sdf,
    wind_world,
)

NOMINAL = PROXIES[0]
LOW_DRAG = PROXIES[2]


def test_mass_and_thrust_margin_are_the_stated_ones() -> None:
    assert NOMINAL.mass_kg == 5.0
    assert 2.3 < NOMINAL.thrust_to_weight < 2.5
    assert NOMINAL.motor_k * MAX_ROTOR_RAD_S**2 == pytest.approx(3.0 * 9.81)


def test_drag_gives_the_x500_deceleration_per_unit_speed() -> None:
    x500 = _decel_rate(X500_MASS_KG, X500_MOTOR_K, X500_ROTOR_DRAG)
    assert _decel_rate(NOMINAL.mass_kg, NOMINAL.motor_k, NOMINAL.rotor_drag) == pytest.approx(x500)
    assert LOW_DRAG.rotor_drag == pytest.approx(NOMINAL.rotor_drag / 2)


def test_base_model_edit_changes_only_the_body() -> None:
    source = (
        "<model name='x500_base'><mass>2.0</mass><ixx>1</ixx><iyy>1</iyy><izz>1</izz>"
        "<pose>0.174 -0.174 0</pose><mass>0.016</mass><ixx>7</ixx></model>"
    )
    out = base_sdf(source, NOMINAL)
    assert "<model name='x650_proxy_base'>" in out
    assert "<mass>5</mass>" in out and "<mass>0.016</mass>" in out
    assert "<ixx>7</ixx>" in out
    assert "<pose>0.23 -0.23 0</pose>" in out
    assert f"<izz>{NOMINAL.inertia[1]:.8g}</izz>" in out


def test_model_edit_points_at_its_own_base() -> None:
    source = (
        "<model name='x500'><uri>model://x500_base</uri><timeConstantUp>1</timeConstantUp>"
        "<timeConstantDown>1</timeConstantDown><maxRotVelocity>1000</maxRotVelocity>"
        "<motorConstant>1</motorConstant><rotorDragCoefficient>1</rotorDragCoefficient></model>"
    )
    out = model_sdf(source, NOMINAL)
    assert "model://x650_proxy_base" in out
    assert "<maxRotVelocity>700</maxRotVelocity>" in out


def test_airframe_edit_sets_geometry_and_motor_range() -> None:
    source = (
        "# @name Gazebo x500\nPX4_SIM_MODEL=${PX4_SIM_MODEL:=x500}\n"
        "param set-default CA_ROTOR1_PX -0.13\nparam set-default CA_ROTOR1_PY -0.20\n"
        "param set-default CA_ROTOR1_KM  0.05\n"
        "param set-default SIM_GZ_EC_MIN1 150\nparam set-default SIM_GZ_EC_MAX1 1000\n"
    )
    out = airframe(source, NOMINAL)
    assert "CA_ROTOR1_PX -0.23" in out and "CA_ROTOR1_PY -0.23" in out
    assert "CA_ROTOR1_KM  0.05" in out
    assert "SIM_GZ_EC_MAX1 700" in out and "SIM_GZ_EC_MIN1 105" in out
    assert "PX4_SIM_MODEL:=x650_proxy" in out


def test_wind_world_keeps_the_direction_and_sets_the_speed() -> None:
    source = "<world name='windy'><linear_velocity>5 2 0</linear_velocity></world>"
    out = wind_world(source, "windy_4", 4.0)
    assert "<world name='windy_4'>" in out
    found = out.split("<linear_velocity>")[1].split("</")[0].split()
    east, north = float(found[0]), float(found[1])
    assert math.hypot(east, north) == pytest.approx(4.0)
    assert north / east == pytest.approx(2 / 5)
    with pytest.raises(ValueError):
        wind_world("<world name='other'/>", "windy_4", 4.0)
