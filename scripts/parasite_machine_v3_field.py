
"""
parasite_machine_v3_field.py

Upgrade: vertices are now internal Parasite machines (field-like).
Each node contains its own Parasite dynamics.

This implements:
- field–simplex coupling
- recursive parasitic structure
- internal dynamics at vertices
"""

from dataclasses import dataclass, field
from typing import List, Dict
import random
import math
import json

# --- Inner node now has its own micro-dynamics ---
@dataclass
class InternalField:
    """
    A vertex is now a local dynamical field.

    It has:
    - internal intensity
    - internal fluctuations
    - its own parasite-like updates
    """
    label: str
    intensity: float = 0.5
    memory: float = 0.0

    def step(self, external_influence: float):
        """
        Internal dynamics influenced by external relations.
        """
        noise = random.gauss(0, 0.05)
        self.intensity = max(0, min(1.5, 0.7*self.intensity + 0.3*external_influence + noise))
        self.memory = 0.8*self.memory + 0.2*(1 if self.intensity > 0.6 else 0)

    def snapshot(self):
        return {
            "label": self.label,
            "intensity": round(self.intensity, 4),
            "memory": round(self.memory, 4)
        }


@dataclass
class Relation:
    source: str
    target: str
    intensity: float
    asymmetry: float

    def snapshot(self):
        return {
            "source": self.source,
            "target": self.target,
            "intensity": round(self.intensity, 4),
            "asymmetry": round(self.asymmetry, 4)
        }


@dataclass
class FieldParasiteMachine:
    """
    Full system where each node is itself dynamic.
    """
    A: InternalField
    B: InternalField
    C: InternalField
    relation: Relation
    history: List[Dict] = field(default_factory=list)

    def update_relation(self):
        raw = self.A.intensity - self.B.intensity
        self.relation.intensity = 1/(1+math.exp(-raw))
        self.relation.asymmetry = max(-1, min(1, raw))

    def parasite_effect(self):
        """
        C perturbs relation AND internal fields.
        """
        influence = self.C.intensity
        self.relation.intensity += 0.1 * influence
        self.relation.intensity = max(0, min(1, self.relation.intensity))

    def step(self):
        self.update_relation()
        self.parasite_effect()

        # propagate relation into internal fields
        self.A.step(self.relation.intensity)
        self.B.step(self.relation.intensity)
        self.C.step(self.relation.intensity)

        self.history.append({
            "A": self.A.snapshot(),
            "B": self.B.snapshot(),
            "C": self.C.snapshot(),
            "relation": self.relation.snapshot()
        })

    def run(self, steps=30):
        for _ in range(steps):
            self.step()

    def export(self, path="/mnt/data/parasite_machine_v3_history.json"):
        with open(path, "w") as f:
            json.dump(self.history, f, indent=2)


def main():
    A = InternalField("A", 0.8)
    B = InternalField("B", 0.3)
    C = InternalField("C", 0.5)

    relation = Relation("A", "B", 0.6, 0.5)

    machine = FieldParasiteMachine(A, B, C, relation)
    machine.run(40)
    machine.export()

    print("Done")
    print("/mnt/data/parasite_machine_v3_history.json")


if __name__ == "__main__":
    main()
