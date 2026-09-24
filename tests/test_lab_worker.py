"""Lot G — ExperimentWorker : signaux finished/failed sans event loop Qt."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ["QT_QPA_PLATFORM"] = "offscreen"


_APP = None


def _app():
    global _APP
    from PyQt6.QtWidgets import QApplication
    _APP = QApplication.instance()
    if _APP is None:
        _APP = QApplication(sys.argv)
    return _APP


class _FakeRunner:
    def __init__(self, report=None, error=None):
        self.report = report or {"variants": {}}
        self.error = error
        self.calls = 0

    def run_ab(self, build_fn, seeds, feature_name, toggle_fn,
               ticks, n_agents):
        self.calls += 1
        if self.error is not None:
            raise self.error
        return self.report


def _worker(runner):
    from ui_qt.studio.experiment_worker import ExperimentWorker
    return ExperimentWorker(
        runner,
        build_fn=lambda seed, n_agents: None,
        seeds=[1],
        feature_name="culture",
        toggle_fn=lambda sim: None,
        ticks=1,
        agents=1,
    )


def test_worker_emits_finished_without_event_loop():
    _app()
    report = {"feature": "culture", "variants": {"A_on": {"pop": 3}}}
    worker = _worker(_FakeRunner(report=report))

    got = []
    worker.finished.connect(lambda rep: got.append(rep))
    errors = []
    worker.failed.connect(errors.append)

    worker.run()  # synchrone : connection directe, pas de QThread
    assert got == [report]
    assert errors == []


def test_worker_emits_failed_on_exception():
    _app()
    worker = _worker(_FakeRunner(error=RuntimeError("boom")))

    got = []
    worker.finished.connect(lambda rep: got.append(rep))
    errors = []
    worker.failed.connect(errors.append)

    worker.run()
    assert got == []
    assert len(errors) == 1
    assert errors[0].startswith("RuntimeError:")
    assert "boom" in errors[0]


if __name__ == "__main__":
    test_worker_emits_finished_without_event_loop()
    test_worker_emits_failed_on_exception()
    print("ALL TESTS PASSED")
