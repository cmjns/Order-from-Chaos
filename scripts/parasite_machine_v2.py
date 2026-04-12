"""
parasite_machine_v2.py

Narrative implementation of a refined Parasite machine.

This version extends the earlier model in five major ways:

1. Relations are explicitly one-way and asymmetric.
   We do not model a neutral edge. We model an intensive, directed relation.

2. A one-way relation may imply its own counter-relation.
   The reverse relation is not assumed automatically; it is derived
   according to a representational mode.

3. Representational modes are built into the machine.
   We include four modes:
       - identity
       - resemblance
       - analogy
       - contrariety

   These correspond to distinct "curvatures" of implication.

4. The tetralemma is built into the machine as a phase-space of relational determination.
   A relation may be:
       - affirmed
       - negated
       - both
       - neither

5. The Parasite (the third term C) acts not only on a relation A -> B,
   but on:
       - its intensity
       - its asymmetry
       - its implied counter-relation
       - its tetralemmatic state
       - its representational mode

Ontological discipline
======================
This model presupposes:
- no conserved quantities
- no underlying substances
- no fixed identities of roles

It assumes only:
- positions
- asymmetric relations
- implication rules
- transformation
- thresholds
- regime shifts
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
    It is a placeholder in a relational machine.

    It carries:
    - a label
    - an intensity
    - a memory score

    Why intensity?
    --------------
    Because the machine is built around gradients and thresholds,
    not essences.

    Why memory?
    ----------
    Because persistence matters.
    A metastable configuration is not merely strong;
    it endures long enough to count.
    """
    label: str
    intensity: float = 0.0
    memory: float = 0.0

    def snapshot(self) -> Dict[str, float]:
        """Return a JSON-friendly view of the position."""
        return {
            "label": self.label,
            "intensity": round(self.intensity, 4),
            "memory": round(self.memory, 4),
        }


@dataclass
class AsymmetricRelation:
    """
    The primitive relation of the refined Parasite machine.

    A relation is explicitly one-way:
        source -> target

    and carries:
    - intensity: how strong the directed relation is
    - asymmetry: how directional / biased it is
    - mode: the representational regime governing implied return
    - tetra_state: the tetralemmatic phase of the relation

    Conceptual point:
    -----------------
    We do NOT start with symmetry and then break it.
    We start with asymmetry as primitive.

    The counter-relation may be implied,
    but that implication depends on representational mode.
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
class ParasiteMachineV2:
    """
    Refined Parasite machine.

    Structural form:
    ----------------
    P = (A, B, C, R, Phi, m, tau, d)

    where:
    - A, B, C are positions
    - R is the primitive asymmetric relation A -> B
    - Phi is the mode-dependent implication of a counter-relation
    - m is the representational mode
    - tau is the tetralemmatic state
    - d is the parasitic distance

    Distance and coupling
    ---------------------
    C acts on the relation A -> B at a variable distance d.
    We operationalize this with:
        coupling = 1 / (d + epsilon)

    So:
    - large distance  -> weak parasitic influence
    - small distance  -> strong parasitic influence

    Noise and metastability
    -----------------------
    C itself can be in one of two regimes:
    - noise
    - metastability

    This matters because C acts differently on the relation depending on regime.
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
        """
        eps = 1e-6
        return 1.0 / (self.distance + eps)

    def mode_of_C(self) -> CMode:
        """
        Decide whether C acts as noise or metastability.
        """
        if (
            self.C.intensity >= self.metastability_threshold
            and self.C.memory >= self.memory_threshold
        ):
            return "metastability"
        return "noise"

    def baseline_relation_update(self) -> None:
        """
        Update the primitive relation A -> B from current positions.

        intensity:
            stronger A and weaker B support stronger directed force

        asymmetry:
            directional imbalance between source and target
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
        Let C act on the primitive relation A -> B.

        C as noise:
            random perturbation of relation intensity and asymmetry

        C as metastability:
            structured stabilization / redirection
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
        Derive the counter-relation B -> A according to representational mode.

        identity:
            strong reciprocal implication; elliptic closure

        resemblance:
            weaker return; parabolic implication

        analogy:
            transformed return; mediated structural resemblance

        contrariety:
            return intensifies divergence; hyperbolic separation
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
            tetra_state="affirmed",
        )

    def determine_tetralemma_state(self, reverse_relation: AsymmetricRelation) -> TetraState:
        """
        Determine tetralemmatic state of the relation.

        affirmed:
            A -> B strong, B -> A weak

        negated:
            A -> B weak, B -> A strong

        both:
            both relations strong

        neither:
            neither relation stabilizes
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

    def conic_regime(self) -> str:
        """
        Return the conic interpretation of the current representational mode.
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
        Update positions from forward and implied reverse relations.
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
        Randomly permute roles A, B, C.
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
        Randomly change parasitic distance.
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
        Execute one full step of the refined Parasite machine.
        """
        self.baseline_relation_update()
        self.parasite_transform_relation()
        reverse_relation = self.implied_counter_relation()

        tetra = self.determine_tetralemma_state(reverse_relation)
        self.relation_AB.tetra_state = tetra
        reverse_relation.tetra_state = tetra

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


def build_example_machine(seed: int = 17) -> ParasiteMachineV2:
    """
    Construct a concrete refined Parasite machine.
    """
    random.seed(seed)

    A = Position(label="A", intensity=0.78, memory=0.28)
    B = Position(label="B", intensity=0.24, memory=0.08)
    C = Position(label="C", intensity=0.44, memory=0.16)

    relation = AsymmetricRelation(
        source="A",
        target="B",
        intensity=0.70,
        asymmetry=0.54,
        mode="identity",
        tetra_state="affirmed",
    )

    return ParasiteMachineV2(
        A=A,
        B=B,
        C=C,
        relation_AB=relation,
        distance=1.0,
        metastability_threshold=0.65,
        memory_threshold=0.55,
        noise_scale=0.18,
    )


def print_narrative_trace(machine: ParasiteMachineV2, max_rows: int = 16) -> None:
    """
    Print a readable narrative trace.
    """
    print("=" * 96)
    print("REFINED PARASITE MACHINE V2 - NARRATIVE TRACE")
    print("=" * 96)

    for i, row in enumerate(machine.history[:max_rows]):
        print(f"\\nStep {i + 1}")
        print(f"  A: {row['A']}")
        print(f"  B: {row['B']}")
        print(f"  C: {row['C']}")
        print(f"  relation_AB: {row['relation_AB']}")
        print(f"  implied_relation_BA: {row['implied_relation_BA']}")
        print(f"  mode_of_C: {row['mode_of_C']}")
        print(f"  distance={row['distance']}  coupling={row['coupling']}")
        print(f"  conic_regime={row['conic_regime']}")
        print(
            f"  role_permuted={row['role_permuted']}  "
            f"distance_shifted={row['distance_shifted']}  "
            f"mode_shifted={row['mode_shifted']}"
        )

    print("\\nFinal summary:")
    print(json.dumps(machine.summary(), indent=2))


def export_history_json(machine: ParasiteMachineV2, path: str = "/mnt/data/parasite_machine_v2_history.json") -> None:
    """
    Export the full machine history to JSON.
    """
    payload = {
        "summary": machine.summary(),
        "history": machine.history,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def main() -> None:
    """
    Demonstration entry point.
    """
    machine = build_example_machine(seed=17)
    machine.run(steps=50)
    print_narrative_trace(machine, max_rows=18)
    export_history_json(machine)


if __name__ == "__main__":
    main()
