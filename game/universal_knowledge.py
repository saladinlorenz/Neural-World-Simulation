"""UniversalKnowledge — savoir partagé factuel et vérifiable.

Ne crée jamais d'objectifs imposés : rend simplement des cibles disponibles
dans la mémoire utilisable. Le cerveau individuel conserve la décision.
"""
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass, asdict
from typing import Dict, Tuple
import numpy as np

FACT_TTL = 12_000
MIN_CONFIRMATIONS = 2


@dataclass
class PlaceFact:
    category: str
    tx: int
    ty: int
    confidence: float
    confirmations: int
    last_verified: int
    source: str


class UniversalKnowledge:
    def __init__(self, omniscient=False):
        self.omniscient = bool(omniscient)
        self.static_affordances: Dict[int, dict] = {}
        self.places: Dict[str, Dict[Tuple[int, int], PlaceFact]] = defaultdict(dict)
        self.revision = 0

    def bootstrap_assets(self, am):
        self.static_affordances = {
            int(a.id): {
                "role": a.role,
                "edible": float(a.edible),
                "harvest": dict(a.harvest or {}),
                "tool": bool(a.tool),
                "shelter": bool(a.shelter),
                "solid": bool(a.solid),
                "affordances": tuple(a.afford),
            }
            for a in am.assets
        }
        self.revision += 1

    def verify_place(self, category, tx, ty, tick, source="world", confidence=1.0):
        key = (int(tx), int(ty))
        old = self.places[category].get(key)
        if old is None:
            self.places[category][key] = PlaceFact(
                category, key[0], key[1], float(confidence), 1, int(tick), source
            )
        else:
            old.confirmations += 1
            old.confidence = min(1.0, max(old.confidence, float(confidence)))
            old.last_verified = int(tick)
            if source == "world" or old.confirmations >= MIN_CONFIRMATIONS:
                old.source = "world" if source == "world" else "consensus"
        self.revision += 1

    def invalidate(self, category, tx, ty):
        if self.places.get(category, {}).pop((int(tx), int(ty)), None) is not None:
            self.revision += 1

    def nearest(self, category, tx, ty, maxdist=10_000, tick=None):
        best = None
        bestd = float("inf")
        for fact in self.places.get(category, {}).values():
            if tick is not None and tick - fact.last_verified > FACT_TTL:
                continue
            d = max(abs(fact.tx - tx), abs(fact.ty - ty))
            if d <= maxdist and d < bestd:
                best, bestd = fact, d
        return best

    def sync_from_world(self, world, am, tick):
        if not self.omniscient:
            return
        present = defaultdict(set)

        water_ys, water_xs = np.nonzero(world.water > 0)
        for tx, ty in zip(water_xs, water_ys):
            present["water"].add((int(tx), int(ty)))

        content_mask = world.content >= 0
        content_ys, content_xs = np.nonzero(content_mask)
        aids = world.content[content_ys, content_xs]
        for i, aid in enumerate(aids):
            if aid < 0 or aid >= len(am.assets):
                continue
            a = am.assets[aid]
            tx, ty = int(content_xs[i]), int(content_ys[i])
            if a.edible > 0:
                present["food"].add((tx, ty))
            if a.harvest:
                mat = a.harvest.get("material")
                cat = {"bois": "wood", "pierre": "stone", "or": "stone"}.get(mat)
                if cat:
                    present[cat].add((tx, ty))
            if a.shelter:
                present["shelter"].add((tx, ty))

        for category, positions in present.items():
            for tx, ty in positions:
                self.verify_place(category, tx, ty, tick, source="world", confidence=1.0)
        for category, facts in list(self.places.items()):
            if category not in present:
                continue
            for pos in list(facts):
                if pos not in present[category]:
                    self.invalidate(category, *pos)

    def to_dict(self):
        return {
            "omniscient": self.omniscient,
            "revision": self.revision,
            "static_affordances": self.static_affordances,
            "places": {
                cat: {f"{x},{y}": asdict(f) for (x, y), f in facts.items()}
                for cat, facts in self.places.items()
            },
        }

    @classmethod
    def from_dict(cls, data):
        out = cls(data.get("omniscient", False))
        out.revision = int(data.get("revision", 0))
        out.static_affordances = dict(data.get("static_affordances", {}))
        for cat, facts in data.get("places", {}).items():
            for _, raw in facts.items():
                fact = PlaceFact(**raw)
                out.places[cat][(fact.tx, fact.ty)] = fact
        return out
