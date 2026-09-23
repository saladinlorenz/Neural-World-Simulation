"""ExperimentWorker — exécute une expérience A/B hors du thread UI (F.3)."""
from PyQt6.QtCore import QObject, pyqtSignal


class ExperimentWorker(QObject):
    """Worker déplaçable dans un QThread : ne touche jamais aux widgets."""

    finished = pyqtSignal(dict)
    failed = pyqtSignal(str)

    def __init__(self, runner, build_fn, seeds, feature_name, toggle_fn,
                 ticks, agents):
        super().__init__()
        self.runner = runner
        self.build_fn = build_fn
        self.seeds = seeds
        self.feature_name = feature_name
        self.toggle_fn = toggle_fn
        self.ticks = ticks
        self.agents = agents

    def run(self):
        try:
            report = self.runner.run_ab(
                self.build_fn,
                self.seeds,
                self.feature_name,
                self.toggle_fn,
                ticks=self.ticks,
                n_agents=self.agents,
            )
            self.finished.emit(report)
        except Exception as exc:
            self.failed.emit(f"{type(exc).__name__}: {exc}")
