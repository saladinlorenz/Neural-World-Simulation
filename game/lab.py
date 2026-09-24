"""LabRecorder — mesures, événements et exports CSV/JSONL du laboratoire."""
from __future__ import annotations
from collections import Counter, deque
from pathlib import Path
import csv
import json

EVENT_TYPES = (
    "storage_deposit", "storage_withdraw",
    "site_created", "site_block_placed", "site_completed",
    "message_sent", "message_received",
    "imitation_recorded",
    "tool_crafted", "tool_broken",
    "crop_planted", "crop_harvested",
    "route_used",
    "monster_killed",
    "birth", "death",
    "institution",
)


class LabRecorder:
    def __init__(self, root="data/lab", max_events=50_000):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.events = deque(maxlen=max_events)
        self.daily = []
        self._event_counts = Counter()

    def event(self, tick, kind, **payload):
        self.events.append({"tick": int(tick), "kind": kind, **payload})
        self._event_counts[kind] += 1

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
            "monsters": len(sim.monsters),
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
            "event_counts": dict(self._event_counts),
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


class ExperimentRunner:
    """Lance des expériences causales A/B : même seed, feature toggled."""

    def __init__(self, lab_root="data/lab"):
        self.lab_root = Path(lab_root)
        self.lab_root.mkdir(parents=True, exist_ok=True)

    def run_ab(self, build_fn, seeds, feature_name, toggle_fn,
               ticks=3000, n_agents=10):
        """Lance A (feature on) et B (feature off) sur chaque seed.

        build_fn(seed, n_agents, **overrides) -> (world, sim)
        toggle_fn(sim) -> None  (désactive la feature pour la variante B)
        """
        results_a, results_b = [], []
        for seed in seeds:
            w_a, sim_a = build_fn(seed=seed, n_agents=n_agents)
            for _ in range(ticks):
                sim_a.tick()
            results_a.append(self._collect(sim_a))

            w_b, sim_b = build_fn(seed=seed, n_agents=n_agents)
            toggle_fn(sim_b)
            for _ in range(ticks):
                sim_b.tick()
            results_b.append(self._collect(sim_b))

        report = self._compare(feature_name, results_a, results_b)
        self._save_report(feature_name, report)
        return report

    def _collect(self, sim):
        alive = [a for a in sim.agents if a.alive]
        return {
            "population": len(alive),
            "deaths": sim.stats.get("deaths", 0),
            "births": sim.stats.get("births", 0),
            "builds": sim.stats.get("builds", 0),
            "mean_age": sum(a.age_years for a in alive) / max(1, len(alive)),
            "mean_health": sum(a.health for a in alive) / max(1, len(alive)),
            "storages": len(sim.w.storages),
            "sites": len(sim.w.sites),
        }

    def _compare(self, feature_name, results_a, results_b):
        n = len(results_a)
        keys = [k for k in results_a[0] if isinstance(results_a[0][k], (int, float))]
        summary = {"feature": feature_name, "seeds": n, "variants": {}}
        for variant, data in [("A_on", results_a), ("B_off", results_b)]:
            avg = {}
            for k in keys:
                vals = [d[k] for d in data]
                avg[k] = sum(vals) / max(1, len(vals))
            summary["variants"][variant] = avg
        return summary

    def _save_report(self, feature_name, report):
        path = self.lab_root / f"experiment_{feature_name}.json"
        with path.open("w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
