"""
parasite_machine.py

Narrative implementation of the "Parasite" machine.

Core idea
=========
A Parasite consists of:

1. A one-way relation between positions A -> B
2. A third position C that relates to the relation A -> B
3. C can operate as:
   a) noise
   b) metastability (an emergent entity)
4. Roles can suddenly exchange:
   C can become A, A can become B, B can become C

We model this without assuming substances or conserved quantities.
We only assume:
- positions
- directed relations
- coupling / distance
- transformation rules

Philosophical translation
=========================
- A and B are not "things" in themselves; they are positions in a relation.
- C is not just a third thing; it is a relation-to-the-relation.
- Noise and entity are two regimes of the same position C.
- The system can reassign roles, so no position has an intrinsic identity.

This file is intentionally written as narrative code:
- long docblocks explain conceptual purpose
- inline comments tie implementation back to the logic
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Literal
import math
import random
import json


Mode = Literal["noise", "metastability"]


@dataclass
class Position:
    """
    A Position is a placeholder in a relational machine.

    Important:
    ----------
    We do not treat A, B, C as substances. A Position holds only:
    - a label
    - an intensity
    - a local memory score

    Why intensity?
    --------------
    Because we want to think in gradients and thresholds rather than fixed essences.

    Why memory?
    ----------
    Because metastability is not pure instantaneous value.
    A metastable entity is something that persists long enough to count.
    """
    label: str
    intensity: float = 0.0
    memory: float = 0.0

    def snapshot(self) -> Dict[str, float]:
        """Return a serializable view of the position."""
        return {
            "label": self.label,
            "intensity": round(self.intensity, 4),
            "memory": round(self.memory, 4),
        }


@dataclass
class Parasite:
    """
    The Parasite machine.

    Structure
    ---------
    - A -> B is the primary directed relation
    - C is the third position that acts on that relation
    - distance controls the strength of C's action on A -> B

    Interpretation of distance
    --------------------------
    The user defined a variable distance for C relative to the relation A -> B.
    We model it this way:

    - large distance  -> weak coupling (C approaches zero effect)
    - small distance  -> strong coupling
    - extremely small -> C can dominate the relation

    This matches the intuition:
    C may be negligible, modulatory, or overwhelming.

    Noise vs metastability
    ----------------------
    C is not intrinsically one or the other.
    Its regime is determined dynamically from:
    - local intensity
    - persistence (memory)
    - threshold

    Role exchange
    -------------
    The machine permits sudden role permutation:
    (A, B, C) -> (B, C, A) or other permutations

    This is crucial:
    no position has an ontological privilege.
    """
    A: Position
    B: Position
    C: Position
    distance: float = 1.0
    metastability_threshold: float = 0.65
    memory_threshold: float = 0.55
    noise_scale: float = 0.25
    history: List[Dict[str, object]] = field(default_factory=list)

    def coupling(self) -> float:
        """
        Convert distance into coupling strength.

        We avoid a singularity at zero by adding a tiny epsilon.
        The chosen form is simple and interpretable:

            coupling = 1 / (distance + epsilon)

        So:
        - as distance grows, coupling weakens toward 0
        - as distance shrinks, coupling grows

        This does not claim metaphysical truth.
        It is just a clean operationalization of the idea.
        """
        eps = 1e-6
        return 1.0 / (self.distance + eps)

    def mode_of_C(self) -> Mode:
        """
        Determine whether C currently acts as noise or metastability.

        We say C counts as metastability when:
        - its intensity is high enough
        - its memory is high enough

        In other words:
        a metastable entity is stabilized intensity.

        Everything else is treated as noise.
        """
        if (
            self.C.intensity >= self.metastability_threshold
            and self.C.memory >= self.memory_threshold
        ):
            return "metastability"
        return "noise"

    def relation_strength(self) -> float:
        """
        Compute the baseline strength of A -> B.

        This is a minimal directed relation:
        - stronger A increases directional force
        - stronger B can dampen reception if it is already saturated

        The formula is deliberately simple:
            sigmoid(A - 0.5 * B)

        This gives us a bounded relation strength in [0, 1].
        """
        x = self.A.intensity - 0.5 * self.B.intensity
        return 1.0 / (1.0 + math.exp(-x))

    def apply_C_to_relation(self) -> float:
        """
        Apply the third term C to the relation A -> B.

        The result is a transformed relation value.

        Two regimes:
        ------------
        1. noise:
           C perturbs the relation with random variation scaled by coupling
        2. metastability:
           C stabilizes / redirects the relation with structured influence

        Why this distinction?
        --------------------
        Because the same third position can either:
        - disrupt a relation
        - become an entity that reorganizes it
        """
        base = self.relation_strength()
        k = self.coupling()
        mode = self.mode_of_C()

        if mode == "noise":
            # In the noise regime, C is primarily perturbative.
            perturbation = random.gauss(0.0, self.noise_scale) * k
            transformed = base + perturbation
        else:
            # In the metastable regime, C acts like a stabilized operator:
            # it does not merely perturb; it reshapes the relation.
            transformed = base + (0.35 * self.C.intensity * k)

        # Clamp to a readable range for interpretability.
        return max(0.0, min(1.0, transformed))

    def update_positions(self) -> None:
        """
        Advance the machine by one step.

        Narrative of the update:
        ------------------------
        1. Compute transformed relation A -> B under influence of C
        2. Update B as the primary recipient of the transformed relation
        3. Update A as a partially altered source
        4. Update C according to whether it is stabilizing or destabilizing
        5. Update memory for all positions

        Important:
        ----------
        We do not conserve anything here.
        Intensities can grow, shrink, dissipate, or amplify.
        """
        transformed_relation = self.apply_C_to_relation()
        mode = self.mode_of_C()
        k = self.coupling()

        # B receives the relation.
        new_B = 0.72 * self.B.intensity + 0.55 * transformed_relation

        # A is altered by having served as the directional source.
        new_A = 0.83 * self.A.intensity + 0.12 * (1.0 - transformed_relation)

        # C updates differently depending on its regime.
        if mode == "noise":
            # Noise is unstable and fluctuating.
            new_C = 0.50 * self.C.intensity + abs(random.gauss(0.0, self.noise_scale)) * k
        else:
            # Metastability is self-reinforcing, but not permanent.
            new_C = 0.78 * self.C.intensity + 0.18 * transformed_relation

        # Clamp to a readable range.
        self.A.intensity = max(0.0, min(1.5, new_A))
        self.B.intensity = max(0.0, min(1.5, new_B))
        self.C.intensity = max(0.0, min(1.5, new_C))

        # Memory accumulates when a position remains intense.
        self.A.memory = 0.82 * self.A.memory + 0.18 * (1.0 if self.A.intensity > 0.6 else 0.0)
        self.B.memory = 0.82 * self.B.memory + 0.18 * (1.0 if self.B.intensity > 0.6 else 0.0)
        self.C.memory = 0.82 * self.C.memory + 0.18 * (1.0 if self.C.intensity > 0.6 else 0.0)

        self.history.append({
            "A": self.A.snapshot(),
            "B": self.B.snapshot(),
            "C": self.C.snapshot(),
            "distance": round(self.distance, 4),
            "coupling": round(k, 4),
            "mode_of_C": mode,
            "relation_strength": round(self.relation_strength(), 4),
            "transformed_relation": round(transformed_relation, 4),
        })

    def permute_roles(self, permutation: Tuple[str, str, str]) -> None:
        """
        Permute the roles of A, B, C.

        Example:
            ("B", "C", "A")
        means:
            new A = old B
            new B = old C
            new C = old A

        This implements the claim that roles can exchange suddenly.
        """
        mapping = {"A": self.A, "B": self.B, "C": self.C}
        self.A, self.B, self.C = (
            mapping[permutation[0]],
            mapping[permutation[1]],
            mapping[permutation[2]],
        )

    def maybe_permute(self, probability: float = 0.15) -> bool:
        """
        Randomly trigger a role exchange.
        """
        if random.random() > probability:
            return False

        choices = [
            ("B", "C", "A"),
            ("C", "A", "B"),
            ("B", "A", "C"),
            ("C", "B", "A"),
        ]
        chosen = random.choice(choices)
        self.permute_roles(chosen)
        return True

    def maybe_shift_distance(self, probability: float = 0.20) -> bool:
        """
        Randomly shift the distance of C relative to A -> B.

        Small distance means strong intervention.
        Large distance means near-irrelevance.
        """
        if random.random() > probability:
            return False

        factor = random.choice([0.5, 0.75, 1.25, 2.0])
        self.distance = max(0.01, min(10.0, self.distance * factor))
        return True

    def run(self, steps: int = 40, permute_probability: float = 0.15, distance_probability: float = 0.20) -> None:
        """
        Run the parasite machine for several steps.

        At each step:
        - update intensities
        - maybe permute roles
        - maybe shift distance
        """
        for _ in range(steps):
            self.update_positions()
            permuted = self.maybe_permute(permute_probability)
            shifted = self.maybe_shift_distance(distance_probability)
            self.history[-1]["role_permuted"] = permuted
            self.history[-1]["distance_shifted"] = shifted

    def summary(self) -> Dict[str, object]:
        """
        Return a compact summary of the machine's final state.
        """
        return {
            "final_A": self.A.snapshot(),
            "final_B": self.B.snapshot(),
            "final_C": self.C.snapshot(),
            "final_distance": round(self.distance, 4),
            "final_mode_of_C": self.mode_of_C(),
            "steps": len(self.history),
        }


def build_example_machine(seed: int = 7) -> Parasite:
    """
    Build a concrete parasite machine.

    We initialize:
    - A as moderately intense
    - B as weakly intense
    - C as ambiguous: not yet clearly noise or entity
    """
    random.seed(seed)

    A = Position(label="A", intensity=0.75, memory=0.30)
    B = Position(label="B", intensity=0.25, memory=0.10)
    C = Position(label="C", intensity=0.40, memory=0.15)

    return Parasite(
        A=A,
        B=B,
        C=C,
        distance=1.0,
        metastability_threshold=0.65,
        memory_threshold=0.55,
        noise_scale=0.20,
    )


def print_narrative_history(machine: Parasite, max_rows: int = 12) -> None:
    """
    Print selected steps as readable narrative output.
    """
    print("=" * 88)
    print("PARASITE MACHINE NARRATIVE TRACE")
    print("=" * 88)

    rows = machine.history[:max_rows]
    for i, row in enumerate(rows):
        print(f"\nStep {i+1}")
        print(f"  A: {row['A']}")
        print(f"  B: {row['B']}")
        print(f"  C: {row['C']}")
        print(f"  distance={row['distance']}  coupling={row['coupling']}")
        print(f"  mode_of_C={row['mode_of_C']}")
        print(f"  relation_strength={row['relation_strength']}")
        print(f"  transformed_relation={row['transformed_relation']}")
        print(f"  role_permuted={row['role_permuted']}  distance_shifted={row['distance_shifted']}")

    print("\nFinal summary:")
    print(json.dumps(machine.summary(), indent=2))


def export_history_json(machine: Parasite, path: str = "parasite_machine_history.json") -> None:
    """
    Export machine history to JSON.
    """
    payload = {
        "summary": machine.summary(),
        "history": machine.history,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def main() -> None:
    """
    Main demonstration.

    This gives a minimal runnable example of the Parasite as machine.
    """
    machine = build_example_machine(seed=7)
    machine.run(steps=40, permute_probability=0.18, distance_probability=0.22)
    print_narrative_history(machine, max_rows=14)
    export_history_json(machine, path="/mnt/data/parasite_machine_history.json")


if __name__ == "__main__":
    main()
