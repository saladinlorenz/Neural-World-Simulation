"""PerfMetrics — instrumentation légère pour mesurer les sections critiques.

Utilisation :
    from game.perfmetrics import PerfMetrics

    perf = PerfMetrics(window=120)
    with perf.measure("simulation"):
        sim.step()

    print(perf.snapshot())
"""
from __future__ import annotations

from contextlib import contextmanager
from time import perf_counter
from typing import Dict, List


class PerfMetrics:
    """Métriques de performance à fenêtre glissante."""

    def __init__(self, window: int = 120):
        self.window = max(10, int(window))
        self.values: Dict[str, List[float]] = {}
        self.counts: Dict[str, int] = {}
        self._starts: Dict[str, float] = {}

    @contextmanager
    def measure(self, name: str):
        started = perf_counter()
        try:
            yield
        finally:
            self.add(name, (perf_counter() - started) * 1000.0)

    def add(self, name: str, milliseconds: float) -> None:
        rows = self.values.setdefault(name, [])
        rows.append(float(milliseconds))
        if len(rows) > self.window:
            del rows[:-self.window]

    def increment(self, name: str, amount: int = 1) -> None:
        self.counts[name] = self.counts.get(name, 0) + int(amount)

    def average(self, name: str) -> float:
        rows = self.values.get(name, ())
        return sum(rows) / len(rows) if rows else 0.0

    def snapshot(self) -> dict[str, float | int]:
        result = {
            f"{name}_ms": self.average(name)
            for name in self.values
        }
        result.update(self.counts)
        return result

    def reset_counts(self) -> None:
        self.counts.clear()

    def reset(self) -> None:
        """Clear all timings and counts (for per-tick reset)."""
        self.values.clear()
        self.counts.clear()
        self._starts.clear()

    def summary(self) -> dict[str, dict[str, float | int]]:
        """Return per-section stats: avg_ms, max_ms, count, plus total_ms (sum of averages)."""
        result: dict[str, dict[str, float | int]] = {}
        total_ms = 0.0
        for name, rows in self.values.items():
            if rows:
                avg_ms = sum(rows) / len(rows)
                max_ms = max(rows)
                count = len(rows)
                result[name] = {"avg_ms": avg_ms, "max_ms": max_ms, "count": count}
                total_ms += avg_ms
        result["_total"] = {"avg_ms": total_ms, "max_ms": 0.0, "count": 0}
        return result


# Instance globale pour le moteur (créée dans Sim.__init__)
_global_perf: "PerfMetrics | None" = None


def get_global_perf() -> "PerfMetrics":
    global _global_perf
    if _global_perf is None:
        _global_perf = PerfMetrics()
    return _global_perf


def set_global_perf(perf: "PerfMetrics") -> None:
    global _global_perf
    _global_perf = perf