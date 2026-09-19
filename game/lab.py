"""LabRecorder — mesures, événements et exports CSV/JSONL du laboratoire."""
from __future__ import annotations
from collections import Counter, deque
from pathlib import Path
import csv
import json


class LabRecorder:
    def __init__(self, root="data/lab", max_events=50_000):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.events = deque(maxlen=max_events)
        self.daily = []

    def event(self, tick, kind, **payload):
        self.events.append({"tick": int(tick), "kind": kind, **payload})

    def snapshot(self, sim):
        alive = [a for a in sim.agents if a.alive]
        action_counts = Counter(
            (a.goal or {}).get("act", -1) for a in alive
        )
        row = {
            "tick": sim.w.tick,
            "year": sim.clock.year,
            "season": sim.clock.season,
            "day": sim.clock.day,
            "population": len(alive),
            "sheep": len(sim.sheep),
            "births": sim.stats.get("births", 0),
            "deaths": sim.stats.get("deaths", 0),
            "mean_age": sum(a.age_years for a in alive) / max(1, len(alive)),
            "mean_health": sum(a.health for a in alive) / max(1, len(alive)),
            "mean_energy": sum(a.energy for a in alive) / max(1, len(alive)),
            "mean_hunger": sum(a.hunger for a in alive) / max(1, len(alive)),
            "builds": sim.stats.get("builds", 0),
            "harvests": sim.stats.get("harvests", 0),
            "attacks": sim.stats.get("attacks", 0),
            "drinks": sim.stats.get("drinks", 0),
            "academy_score": sim.academy.champion_score,
            "actions": dict(action_counts),
        }
        self.daily.append(row)
        return row

    def export(self, tag="run"):
        json_path = self.root / f"{tag}_events.jsonl"
        with json_path.open("w", encoding="utf-8") as f:
            for event in self.events:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")
        csv_path = self.root / f"{tag}_daily.csv"
        if self.daily:
            keys = [k for k in self.daily[0] if k != "actions"]
            with csv_path.open("w", newline="", encoding="utf-8") as f:
                out = csv.DictWriter(f, fieldnames=keys)
                out.writeheader()
                for row in self.daily:
                    out.writerow({k: row.get(k) for k in keys})
        return json_path, csv_path
