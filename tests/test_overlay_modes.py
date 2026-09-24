"""Lot C — overlay : ids anglais, OVERLAY_HELP complet, migration save FR→EN."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


EXPECTED_MODES = [
    "normal", "resources", "danger", "memory", "relations",
    "needs", "anima", "culture", "institutions", "territories",
]


def test_modes_english_ids():
    from ui_qt.studio.world_overlay import MODES, _MODE_LABELS

    assert MODES == EXPECTED_MODES
    for mode in MODES:
        label = _MODE_LABELS[mode]
        assert label and label[0].isupper(), (mode, label)
    assert _MODE_LABELS["resources"] == "Resources"
    assert _MODE_LABELS["memory"] == "Memory"
    assert _MODE_LABELS["needs"] == "Needs"
    assert _MODE_LABELS["territories"] == "Territories"


def test_overlay_help_complete():
    from ui_qt.studio.world_overlay import (
        MODES, OVERLAY_HELP, CONTEXT_MODES, WorldOverlay,
    )

    assert set(OVERLAY_HELP) == set(MODES)
    for mode, text in OVERLAY_HELP.items():
        assert text.strip(), f"aide vide pour {mode}"

    ov = WorldOverlay()
    for mode in MODES:
        assert ov.mode_help(mode) == OVERLAY_HELP[mode]
    assert ov.mode_help("inconnu") == ""

    assert CONTEXT_MODES == {"memory", "danger", "relations", "needs", "anima"}
    assert CONTEXT_MODES <= set(MODES)
    assert "resources" not in CONTEXT_MODES


def test_overlay_and_journal_migrations():
    from game.ui_state import UIState

    s = UIState()
    s.apply_dict({"active_overlay": "memoire", "journal_filter": "vie"})
    assert s.active_overlay == "memory"
    assert s.journal_filter == "life"

    s.apply_dict({"active_overlay": "ressources", "journal_filter": "tous"})
    assert s.active_overlay == "resources"
    assert s.journal_filter == "all"

    s.apply_dict({"active_overlay": "institutions", "journal_filter": "culture"})
    assert s.active_overlay == "institutions"
    assert s.journal_filter == "culture"


if __name__ == "__main__":
    test_modes_english_ids()
    test_overlay_help_complete()
    test_overlay_and_journal_migrations()
    print("ALL TESTS PASSED")
