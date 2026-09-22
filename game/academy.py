"""Academy — registre de cerveaux validés (champions).

Pas de partage de poids en écriture directe : un nouveau modèle est accepté
uniquement après évaluation mesurée. Les enfants continuent d'hériter des
parents par Brain.breed().
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
import json
import time

import numpy as np

from .brain import N_IN


@dataclass
class ModelManifest:
    version: int
    created_at: float
    brain_size: int
    action_count: int
    input_count: int
    score: float
    label: str


class Academy:
    def __init__(self):
        self.champion_params = None
        self.champion_size = None
        self.champion_score = float("-inf")
        self.champion_label = "aucun"

    def score_agent(self, a, tick):
        survival = min(1.0, a.age_years / 20.0)
        wellbeing = 0.30 * a.health + 0.25 * a.energy + 0.25 * (1.0 - a.hunger)
        social = 0.10 * max(0.0, min(1.0, a.rep / 5.0 + 0.5))
        skills = 0.10 * float(np.mean(a.skills))
        return float(survival + wellbeing + social + skills)

    def consider(self, a, tick):
        score = self.score_agent(a, tick)
        if score <= self.champion_score:
            return False
        self.champion_params = a.brain.p.copy()
        self.champion_size = int(a.brain.n)
        self.champion_score = score
        self.champion_label = f"{a.name}-g{a.gen}-t{tick}"
        return True

    def make_seed_params(self, nhid, rng, mutation_sigma=0.015):
        if self.champion_params is None or self.champion_size != nhid:
            return None
        p = self.champion_params.copy()
        if mutation_sigma > 0:
            p += rng.normal(0.0, mutation_sigma, size=p.shape)
        return p

    def export_model(self, path, universal_knowledge, label=None):
        if self.champion_params is None:
            raise RuntimeError("Aucun champion valide a exporter")
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        label = label or self.champion_label
        manifest = ModelManifest(
            version=1,
            created_at=time.time(),
            brain_size=int(self.champion_size),
            input_count=N_IN,
            action_count=15,
            score=float(self.champion_score),
            label=label,
        )
        np.savez_compressed(path.with_suffix(".npz"), params=self.champion_params)
        path.with_suffix(".json").write_text(json.dumps({
            "manifest": asdict(manifest),
            "universal_knowledge": universal_knowledge.to_dict(),
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        return path.with_suffix(".npz"), path.with_suffix(".json")

    def import_model(self, path):
        path = Path(path)
        data = np.load(path.with_suffix(".npz"))
        info = json.loads(path.with_suffix(".json").read_text(encoding="utf-8"))
        m = info["manifest"]
        if m["input_count"] != N_IN or m["action_count"] != 15:
            raise ValueError("Modele incompatible avec le vecteur/action actuel")
        self.champion_params = np.asarray(data["params"], dtype=np.float64)
        self.champion_size = int(m["brain_size"])
        self.champion_score = float(m["score"])
        self.champion_label = str(m["label"])
        return info.get("universal_knowledge")
