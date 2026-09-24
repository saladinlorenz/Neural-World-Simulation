"""Lot B — export journal CSV : colonnes fixes, ids EN, couleurs hex registre."""
import csv
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _make_sim():
    from game.assets_manager import AssetManager
    from game.assets_api import _set_asset_manager
    from game.engine import build_world

    am = AssetManager(headless=True).discover()
    am.ensure_procedural_blocks()
    _set_asset_manager(am)
    _, sim = build_world(am, seed=42, procedural=True, n_agents=3)
    return sim


def test_registry_eleven_english_ids():
    from game.ui_registry import JOURNAL_CATEGORIES, ALL_CATEGORIES

    assert len(JOURNAL_CATEGORIES) == 11, list(JOURNAL_CATEGORIES)
    assert ALL_CATEGORIES == "all"
    expected = {"world", "life", "family", "social", "combat", "danger",
                "weather", "economy", "building", "culture", "death"}
    assert set(JOURNAL_CATEGORIES) == expected
    for meta in JOURNAL_CATEGORIES.values():
        assert meta["label"] and meta["label"][0].isupper()
        assert meta["color"].startswith("#") and len(meta["color"]) == 7


def test_export_journal_csv_hex_and_ids():
    from game.ui_registry import export_journal_csv, JOURNAL_CATEGORIES

    sim = _make_sim()
    sim.log("Entree vie.", (67, 160, 92), "life")
    from game.ui_snapshots import journal_snapshot
    snap = journal_snapshot(sim, category="life")
    assert snap, "journal vide apres log(cat=life)"

    path = os.path.join(tempfile.gettempdir(), "test_journal_export.csv")
    try:
        export_journal_csv(snap, path)
        with open(path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        assert rows, "CSV vide"
        assert list(rows[0].keys()) == ["tick", "category", "text", "count", "color"]
        for row in rows:
            assert row["category"] == "life"
            assert row["color"] == JOURNAL_CATEGORIES["life"]["color"]
            assert row["color"].startswith("#")
    finally:
        try:
            os.remove(path)
        except OSError:
            pass


def test_export_unknown_category_empty_color():
    from game.ui_registry import export_journal_csv

    path = os.path.join(tempfile.gettempdir(), "test_journal_unknown.csv")
    try:
        export_journal_csv([{"tick": 1, "category": "zzz_inconnu",
                             "text": "x", "count": 1}], path)
        with open(path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        assert rows[0]["color"] == ""
    finally:
        try:
            os.remove(path)
        except OSError:
            pass


if __name__ == "__main__":
    test_registry_eleven_english_ids()
    test_export_journal_csv_hex_and_ids()
    test_export_unknown_category_empty_color()
    print("ALL TESTS PASSED")
