"""
parasite_machine_v2_updated.py

Narrative implementation of the refined Parasite machine, updated so that
the tetralemma is no longer a static label but a dynamical, self-referential
state space.

What is new in this version
===========================
Earlier, the machine computed a tetralemmatic state at each step:
    affirmed / negated / both / neither

But that still treated the tetralemma as a descriptive output.

In this updated version:
- the tetralemma has memory,
- it transitions from one state to another,
- the transition depends on:
    * the current forward relation,
    * the implied reverse relation,
    * the mode of C,
    * the current representational mode,
    * the previous tetralemmatic state.

So the tetralemma now functions as part of the machine itself.

Philosophical consequence
=========================
We do not choose one tetralemmatic corner as globally true.
Instead, the system traverses the tetralemma.
Logic becomes dynamics.

The machine therefore now integrates:
- asymmetric relation
- implied counter-relation
- representational curvature
- tetralemmatic self-reference
- parasitic intervention
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Literal
import json
import math
import random


Mode = Literal["identity", "resemblance", "analogy", "contrariety"]
TetraState = Literal["affirmed", "negated", "both", "neither"]
CMode = Literal["noise", "metastability"]


@dataclass
class Position:
    """
    A Position is not a substance.
    It is a placeholder within a relational machine.

    It carries:
    - label
    - intensity
    - memory

    Intensity lets us think in terms of gradients rather than essences.
    Memory lets us model persistence rather than instantaneous snapshots.
    """
    label: str
    intensity: float = 0.0
    memory: float = 0.0

    def snapshot(self) -> Dict[str, float]:
        """Return a JSON-friendly view of this position."""
        return {
            "label": self.label,
            "intensity": round(self.intensity, 4),
            "memory": round(self.memory, 4),
        }


@dataclass
class AsymmetricRelation:
    """
    Primitive one-way intensive relation.

    A relation stores:
    - source
    - target
    - intensity
    - asymmetry
    - representational mode
    - current tetralemmatic state

    The crucial point is that asymmetry is not an accident of a graph.
    It is part of the relation's internal structure.
    """
    source: str
    target: str
    intensity: float
    asymmetry: float
    mode: Mode = "identity"
    tetra_state: TetraState = "affirmed"

    def snapshot(self) -> Dict[str, object]:
        """Return a JSON-friendly view of the relation."""
        return {
            "source": self.source,
            "target": self.target,
            "intensity": round(self.intensity, 4),
            "asymmetry": round(self.asymmetry, 4),
            "mode": self.mode,
            "tetra_state": self.tetra_state,
        }


@dataclass
class ParasiteMachineV2Updated:
    """
    Updated Parasite machine with dynamical tetralemma.

    Structural form
    ---------------
    P = (A, B, C, R, Phi, m, tau, d)

    where:
    - A, B, C are positions
    - R is the primitive asymmetric relation A -> B
    - Phi is the mode-dependent implication operator
    - m is representational mode
    - tau is the tetralemmatic state
    - d is parasitic distance

    New feature
    -----------
    tau is not merely calculated from the relations.
    tau itself evolves through an explicit transition rule.

    This means:
    the machine does not merely inhabit a logical regime;
    it moves through logical regimes.
    """
    A: Position
    B: Position
    C: Position
    relation_AB: AsymmetricRelation
    distance: float = 1.0
    metastability_threshold: float = 0.65
    memory_threshold: float = 0.55
    noise_scale: float = 0.20
    history: List[Dict[str, object]] = field(default_factory=list)

    def coupling(self) -> float:
        """
        Convert parasitic distance into coupling strength.

        Large distance means weak intervention.
        Small distance means strong intervention.
        """
        eps = 1e-6
        return 1.0 / (self.distance + eps)

    def mode_of_C(self) -> CMode:
        """
        Decide whether C acts as noise or metastability.

        C becomes metastable when both its intensity and its memory
        pass threshold.
        """
        if (
            self.C.intensity >= self.metastability_threshold
            and self.C.memory >= self.memory_threshold
        ):
            return "metastability"
        return "noise"

    def baseline_relation_update(self) -> None:
        """
        Update primitive relation A -> B from current positions.

        This remains a local operationalization:
        - stronger A and weaker B strengthen directed intensity
        - imbalance between A and B defines asymmetry
        """
        raw = self.A.intensity - 0.5 * self.B.intensity
        intensity = 1.0 / (1.0 + math.exp(-raw))
        asymmetry = max(-1.0, min(1.0, self.A.intensity - self.B.intensity))

        self.relation_AB.source = self.A.label
        self.relation_AB.target = self.B.label
        self.relation_AB.intensity = intensity
        self.relation_AB.asymmetry = asymmetry

    def parasite_transform_relation(self) -> None:
        """
        Let the third term C act on the primitive relation.

        If C is noise:
            perturb intensity and asymmetry stochastically

        If C is metastability:
            reinforce or redirect the relation more coherently
        """
        mode_C = self.mode_of_C()
        k = self.coupling()

        if mode_C == "noise":
            delta_i = random.gauss(0.0, self.noise_scale) * k
            delta_a = random.gauss(0.0, self.noise_scale * 0.75) * k
        else:
            delta_i = 0.20 * self.C.intensity * k
            delta_a = 0.12 * (self.C.intensity - 0.5) * k

        self.relation_AB.intensity = max(0.0, min(1.0, self.relation_AB.intensity + delta_i))
        self.relation_AB.asymmetry = max(-1.0, min(1.0, self.relation_AB.asymmetry + delta_a))

    def implied_counter_relation(self) -> AsymmetricRelation:
        """
        Derive the implied reverse relation B -> A according to mode.

        identity:
            strong reciprocal implication

        resemblance:
            weaker return

        analogy:
            transformed return

        contrariety:
            return that intensifies divergence
        """
        r = self.relation_AB
        mode = r.mode

        if mode == "identity":
            intensity = min(1.0, 0.95 * r.intensity + 0.03)
            asymmetry = max(-1.0, min(1.0, -0.90 * r.asymmetry))
        elif mode == "resemblance":
            intensity = min(1.0, 0.65 * r.intensity)
            asymmetry = max(-1.0, min(1.0, -0.55 * r.asymmetry))
        elif mode == "analogy":
            intensity = min(1.0, 0.55 * r.intensity + 0.15 * abs(r.asymmetry))
            asymmetry = max(-1.0, min(1.0, -0.35 * r.asymmetry + 0.20))
        else:
            intensity = min(1.0, 0.80 * r.intensity + 0.10)
            asymmetry = max(-1.0, min(1.0, 0.90 * r.asymmetry))

        return AsymmetricRelation(
            source=self.B.label,
            target=self.A.label,
            intensity=intensity,
            asymmetry=asymmetry,
            mode=mode,
            tetra_state=self.relation_AB.tetra_state,
        )

    def candidate_tetralemma_state(self, reverse_relation: AsymmetricRelation) -> TetraState:
        """
        Compute the immediate candidate tetralemma state from the current
        forward and reverse relations.

        This is still the local relational diagnosis.

        But in this updated version, it does not become the next state directly.
        Instead it feeds into a transition rule together with the previous state.
        """
        fwd = self.relation_AB.intensity
        rev = reverse_relation.intensity

        strong_fwd = fwd >= 0.60
        strong_rev = rev >= 0.60

        if strong_fwd and not strong_rev:
            return "affirmed"
        if not strong_fwd and strong_rev:
            return "negated"
        if strong_fwd and strong_rev:
            return "both"
        return "neither"

    def update_tetralemma_state(self, candidate: TetraState, reverse_relation: AsymmetricRelation) -> TetraState:
        """
        Update the tetralemma dynamically.

        This is the key new operator.

        Inputs:
        - previous tetralemmatic state
        - candidate state from current relations
        - mode of C
        - representational mode
        - relation intensities

        Design principle
        ----------------
        The tetralemma is no longer a label assigned from scratch.
        It has inertia, susceptibility, and regime-specific transitions.

        Narrative intuition
        -------------------
        - identity tends to stabilize closure and can favor "both"
        - resemblance tends to drift and can favor "neither" or "affirmed"
        - analogy tends to mediate and can preserve mixed ambiguity
        - contrariety tends to intensify divergence and can favor "negated" or "both"
        """
        previous = self.relation_AB.tetra_state
        mode = self.relation_AB.mode
        c_mode = self.mode_of_C()
        fwd = self.relation_AB.intensity
        rev = reverse_relation.intensity

        # First, if the candidate agrees with the current state,
        # keep it. This models local persistence of logical regime.
        if candidate == previous:
            return previous

        # Second, make regime-specific adjustments.
        # These are not arbitrary truth choices; they model differential
        # tendencies of the system.
        if mode == "identity":
            # Identity favors closure.
            # If both directions are moderately active, collapse upward toward "both".
            if fwd >= 0.45 and rev >= 0.45:
                return "both"
            # If the system weakens significantly, it can drop to neither.
            if fwd < 0.35 and rev < 0.35:
                return "neither"

        elif mode == "resemblance":
            # Resemblance tends to partial one-sided implication.
            # It resists full closure and tends to drift.
            if candidate == "both":
                return "affirmed"
            if previous == "both" and candidate == "neither":
                return "affirmed"

        elif mode == "analogy":
            # Analogy keeps transformation open.
            # It tends to preserve ambiguity when in doubt.
            if candidate in ("affirmed", "negated") and previous == "both":
                return "both"
            if candidate == "neither" and (fwd > 0.40 or rev > 0.40):
                return "both"

        else:  # contrariety
            # Contrariety intensifies divergence.
            # Strong reverse pressure can flip the regime harder.
            if candidate == "affirmed" and rev >= 0.55:
                return "both"
            if candidate == "neither" and abs(self.relation_AB.asymmetry) > 0.45:
                return "negated"

        # Third, let C's regime matter.
        if c_mode == "metastability":
            # Metastable C tends to stabilize complex states rather than collapse them.
            if candidate == "neither" and previous in ("both", "affirmed", "negated"):
                return previous
            if candidate in ("affirmed", "negated") and previous == "both":
                return "both"
        else:
            # Noise tends to destabilize closure and produce drift.
            if previous == "both" and candidate == "affirmed":
                return "neither"
            if previous == "both" and candidate == "negated":
                return "neither"

        # If no stronger transition rule applies, accept the candidate.
        return candidate

    def conic_regime(self) -> str:
        """
        Return the conic interpretation of current representational mode.
        """
        mode = self.relation_AB.mode
        mapping = {
            "identity": "ellipse",
            "resemblance": "parabola",
            "analogy": "mixed",
            "contrariety": "hyperbola",
        }
        return mapping[mode]

    def update_positions(self, reverse_relation: AsymmetricRelation) -> None:
        """
        Update the intensities and memories of positions.

        A relation and its implied reverse feed back into the positions
        that sustain them.
        """
        fwd = self.relation_AB.intensity
        rev = reverse_relation.intensity
        mode_C = self.mode_of_C()
        k = self.coupling()

        new_B = 0.70 * self.B.intensity + 0.50 * fwd
        new_A = 0.76 * self.A.intensity + 0.18 * rev + 0.06 * (1.0 - fwd)

        if mode_C == "noise":
            new_C = 0.52 * self.C.intensity + abs(random.gauss(0.0, self.noise_scale)) * k
        else:
            new_C = 0.80 * self.C.intensity + 0.14 * fwd + 0.08 * rev

        self.A.intensity = max(0.0, min(1.5, new_A))
        self.B.intensity = max(0.0, min(1.5, new_B))
        self.C.intensity = max(0.0, min(1.5, new_C))

        self.A.memory = 0.82 * self.A.memory + 0.18 * (1.0 if self.A.intensity > 0.6 else 0.0)
        self.B.memory = 0.82 * self.B.memory + 0.18 * (1.0 if self.B.intensity > 0.6 else 0.0)
        self.C.memory = 0.82 * self.C.memory + 0.18 * (1.0 if self.C.intensity > 0.6 else 0.0)

    def maybe_permute_roles(self, probability: float = 0.14) -> bool:
        """
        Randomly permute A, B, C.

        This keeps the machine from locking positions into essences.
        """
        if random.random() > probability:
            return False

        mapping = {"A": self.A, "B": self.B, "C": self.C}
        choices = [
            ("B", "C", "A"),
            ("C", "A", "B"),
            ("B", "A", "C"),
            ("C", "B", "A"),
        ]
        perm = random.choice(choices)
        self.A, self.B, self.C = mapping[perm[0]], mapping[perm[1]], mapping[perm[2]]
        return True

    def maybe_shift_distance(self, probability: float = 0.18) -> bool:
        """
        Randomly shift parasitic distance.
        """
        if random.random() > probability:
            return False

        factor = random.choice([0.5, 0.75, 1.25, 2.0])
        self.distance = max(0.01, min(10.0, self.distance * factor))
        return True

    def maybe_shift_mode(self, probability: float = 0.16) -> bool:
        """
        Randomly change representational mode.
        """
        if random.random() > probability:
            return False

        modes = ["identity", "resemblance", "analogy", "contrariety"]
        current = self.relation_AB.mode
        others = [m for m in modes if m != current]
        self.relation_AB.mode = random.choice(others)
        return True

    def step(self) -> None:
        """
        Execute one full step of the updated Parasite machine.

        Sequence:
        1. update primitive relation
        2. let C act on the relation
        3. derive implied reverse relation
        4. compute candidate tetralemmatic state
        5. update tetralemmatic state dynamically
        6. update positions
        7. maybe permute roles
        8. maybe shift distance
        9. maybe shift mode
        """
        self.baseline_relation_update()
        self.parasite_transform_relation()
        reverse_relation = self.implied_counter_relation()

        candidate = self.candidate_tetralemma_state(reverse_relation)
        new_tau = self.update_tetralemma_state(candidate, reverse_relation)

        self.relation_AB.tetra_state = new_tau
        reverse_relation.tetra_state = new_tau

        self.update_positions(reverse_relation)

        permuted = self.maybe_permute_roles()
        shifted_distance = self.maybe_shift_distance()
        shifted_mode = self.maybe_shift_mode()

        self.history.append({
            "A": self.A.snapshot(),
            "B": self.B.snapshot(),
            "C": self.C.snapshot(),
            "relation_AB": self.relation_AB.snapshot(),
            "implied_relation_BA": reverse_relation.snapshot(),
            "mode_of_C": self.mode_of_C(),
            "candidate_tetra_state": candidate,
            "updated_tetra_state": new_tau,
            "distance": round(self.distance, 4),
            "coupling": round(self.coupling(), 4),
            "conic_regime": self.conic_regime(),
            "role_permuted": permuted,
            "distance_shifted": shifted_distance,
            "mode_shifted": shifted_mode,
        })

    def run(self, steps: int = 50) -> None:
        """Run the machine for several steps."""
        for _ in range(steps):
            self.step()

    def summary(self) -> Dict[str, object]:
        """Return a compact final summary."""
        return {
            "final_A": self.A.snapshot(),
            "final_B": self.B.snapshot(),
            "final_C": self.C.snapshot(),
            "final_relation_AB": self.relation_AB.snapshot(),
            "final_distance": round(self.distance, 4),
            "final_mode_of_C": self.mode_of_C(),
            "final_conic_regime": self.conic_regime(),
            "steps": len(self.history),
        }


def build_example_machine(seed: int = 19) -> ParasiteMachineV2Updated:
    """
    Construct a concrete machine with a nontrivial initial condition.

    We start in identity mode but with only moderate relation strength,
    so the system has room to drift, intensify, destabilize, or bifurcate.
    """
    random.seed(seed)

    A = Position(label="A", intensity=0.80, memory=0.26)
    B = Position(label="B", intensity=0.28, memory=0.08)
    C = Position(label="C", intensity=0.46, memory=0.18)

    relation = AsymmetricRelation(
        source="A",
        target="B",
        intensity=0.68,
        asymmetry=0.52,
        mode="identity",
        tetra_state="neither",
    )

    return ParasiteMachineV2Updated(
        A=A,
        B=B,
        C=C,
        relation_AB=relation,
        distance=1.0,
        metastability_threshold=0.65,
        memory_threshold=0.55,
        noise_scale=0.18,
    )


def print_narrative_trace(machine: ParasiteMachineV2Updated, max_rows: int = 18) -> None:
    """
    Print a readable trace.

    The trace now includes:
    - candidate tetralemma state
    - updated tetralemma state

    This makes visible the difference between:
    local relational diagnosis
    and
    self-referential logical transition.
    """
    print("=" * 100)
    print("PARASITE MACHINE V2 UPDATED - DYNAMICAL TETRALEMMA TRACE")
    print("=" * 100)

    for i, row in enumerate(machine.history[:max_rows]):
        print(f"\nStep {i + 1}")
        print(f"  A: {row['A']}")
        print(f"  B: {row['B']}")
        print(f"  C: {row['C']}")
        print(f"  relation_AB: {row['relation_AB']}")
        print(f"  implied_relation_BA: {row['implied_relation_BA']}")
        print(f"  mode_of_C: {row['mode_of_C']}")
        print(f"  candidate_tetra_state: {row['candidate_tetra_state']}")
        print(f"  updated_tetra_state: {row['updated_tetra_state']}")
        print(f"  distance={row['distance']}  coupling={row['coupling']}")
        print(f"  conic_regime={row['conic_regime']}")
        print(
            f"  role_permuted={row['role_permuted']}  "
            f"distance_shifted={row['distance_shifted']}  "
            f"mode_shifted={row['mode_shifted']}"
        )

    print("\nFinal summary:")
    print(json.dumps(machine.summary(), indent=2))


def export_history_json(machine: ParasiteMachineV2Updated, path: str = "/mnt/data/parasite_machine_v2_updated_history.json") -> None:
    """
    Export full machine history to JSON.
    """
    payload = {
        "summary": machine.summary(),
        "history": machine.history,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def main() -> None:
    """
    Run the updated Parasite machine and export its trace.
    """
    machine = build_example_machine(seed=19)
    machine.run(steps=50)
    print_narrative_trace(machine, max_rows=18)
    export_history_json(machine)


if __name__ == "__main__":
    main()
