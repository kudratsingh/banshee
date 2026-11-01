"""Typed interfaces for the modules the work orders implement.

``Protocol`` classes fix the shape, units, frames and failure behaviour of each component so that
work orders implement against a stable contract and tests can use fakes. Nothing here is a working
flight component. Every implementation must:

- state units and frames of every vector in its docstring (``ironclad.contracts.v1`` action_spec
  is the source);
- never bypass the command gate: only ``CommandGate`` forwards setpoints, after
  ``freshness.assess``;
- treat learned proposals as optional inputs that can be rejected (``LearnedProposalAdapter``).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable


@dataclass(frozen=True)
class StateEstimate:
    """Position (m) and velocity (m/s) in the declared local frame, attitude as a quaternion
    (x, y, z, w), yaw rate (rad/s), estimator validity, capture time in the monotonic clock (ns)."""

    position_m: tuple[float, float, float]
    velocity_mps: tuple[float, float, float]
    attitude_xyzw: tuple[float, float, float, float]
    yaw_rate_radps: float
    valid: bool
    t_ns: int
    frame_id: str


@dataclass(frozen=True)
class VelocitySetpoint:
    """Bounded velocity (m/s) and yaw-rate (rad/s) command: frame, decision time, expiry (ns)."""

    vx: float
    vy: float
    vz: float
    yaw_rate: float
    frame_id: str
    decision_t_ns: int
    valid_until_t_ns: int


@dataclass(frozen=True)
class SkillRequest:
    """A mission-executive request to a skill: name, parameters in SI units, deadline (ns)."""

    skill: str
    params: dict[str, Any] = field(default_factory=dict)
    deadline_t_ns: int | None = None


@runtime_checkable
class Estimator(Protocol):
    """Source of the current state estimate (PX4 EKF2 + VIO through the bridge)."""

    def latest(self) -> StateEstimate: ...


@runtime_checkable
class CommandGate(Protocol):
    """The only component allowed to forward setpoints to the flight controller.

    Implementations must call ``freshness.assess`` and enforce action_spec limits and clearance
    before forwarding; expired setpoints are never sent; every decision is logged with reasons."""

    def submit(self, setpoint: VelocitySetpoint) -> bool:
        """Return True if forwarded, False if held back (reasons go to the structured log)."""


@runtime_checkable
class Skill(Protocol):
    """A conventional skill (go-to, hold, inspect viewpoint, search, return) emitting setpoints."""

    def step(self, estimate: StateEstimate, now_ns: int) -> VelocitySetpoint | None:
        """Return the next setpoint, or None when the skill commands nothing this tick."""

    def done(self) -> bool: ...


@runtime_checkable
class MissionExecutive(Protocol):
    """Explicit state machine: goals to skill requests; independent success detection; recovery."""

    def next_request(self, estimate: StateEstimate, now_ns: int) -> SkillRequest | None: ...

    def on_skill_result(
        self, request: SkillRequest, success: bool, evidence: dict[str, Any]
    ) -> None: ...


@runtime_checkable
class OutcomeJudge(Protocol):
    """Independent mission/waypoint outcome from logged state alone; independent of planning."""

    def judge(self, run_dir: str) -> tuple[bool, dict[str, Any]]: ...


@runtime_checkable
class LearnedProposalAdapter(Protocol):
    """Consumes an exported model manifest from the world-model project (contract boundary) and
    offers predictions or proposals. Shadow mode logs only. The gate may reject every proposal; the
    drone runs without this component. ``command_authority`` in the manifest must be False or the
    adapter refuses to load it."""

    def load_manifest(self, manifest_path: str) -> None: ...

    def propose(self, estimate: StateEstimate, candidate: VelocitySetpoint) -> dict[str, Any]:
        """Return predicted consequences and uncertainty for a candidate setpoint, or abstain."""
