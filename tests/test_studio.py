"""Tests pour le module Studio (couche neutre)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestStudioText(unittest.TestCase):
    def test_level_labels(self):
        from game.studio_text import level_label
        self.assertEqual(level_label(0.0), "Tres faible")
        self.assertEqual(level_label(0.3), "Faible")
        self.assertEqual(level_label(0.5), "Moyen")
        self.assertEqual(level_label(0.7), "Eleve")
        self.assertEqual(level_label(1.0), "Tres eleve")

    def test_level_label_clamped(self):
        from game.studio_text import level_label
        self.assertEqual(level_label(-0.5), "Tres faible")
        self.assertEqual(level_label(1.5), "Tres eleve")

    def test_level_colors_are_hex(self):
        from game.studio_text import level_color
        for v in [0.0, 0.3, 0.5, 0.7, 1.0]:
            c = level_color(v)
            self.assertTrue(c.startswith("#"), f"{v} -> {c}")
            self.assertEqual(len(c), 7)

    def test_describe_agent(self):
        from game.studio_text import describe_agent
        snap = {"name": "Aro", "identity": {"builder": 0.8, "explorer": 0.2}}
        result = describe_agent(snap)
        self.assertIn("Aro", result)
        self.assertIn("constructeur", result)

    def test_describe_agent_no_identity(self):
        from game.studio_text import describe_agent
        snap = {"name": "X", "identity": {}}
        result = describe_agent(snap)
        self.assertIn("pas encore", result)

    def test_event_sentence_known(self):
        from game.studio_text import event_sentence
        result = event_sentence({"kind": "monster_attack", "actor_name": "Aro"})
        self.assertIn("Aro", result)
        self.assertIn("attaque", result)

    def test_event_sentence_unknown(self):
        from game.studio_text import event_sentence
        result = event_sentence({"kind": "unknown_event"})
        self.assertIn("evenement", result.lower())

    def test_society_summary(self):
        from game.studio_text import society_summary
        snap = {"population": 12, "families": 3, "storages": 2, "completed_buildings": 5}
        result = society_summary(snap)
        self.assertIn("12", result)
        self.assertIn("3", result)


class TestStudioParameters(unittest.TestCase):
    def test_param_store_defaults(self):
        from game.studio_parameters import ParameterStore
        store = ParameterStore()
        self.assertIsNotNone(store.get("simulation.speed"))
        self.assertIsNotNone(store.get("anima.trauma"))

    def test_param_set_valid(self):
        from game.studio_parameters import ParameterStore
        store = ParameterStore()
        store.set("simulation.speed", 4)
        self.assertEqual(store.get("simulation.speed"), 4)

    def test_param_set_invalid_raises(self):
        from game.studio_parameters import ParameterStore
        store = ParameterStore()
        with self.assertRaises(ValueError):
            store.set("simulation.speed", 99)

    def test_param_reset(self):
        from game.studio_parameters import ParameterStore
        store = ParameterStore()
        store.set("simulation.speed", 4)
        store.reset("simulation.speed")
        self.assertEqual(store.get("simulation.speed"), 1)

    def test_param_reset_all(self):
        from game.studio_parameters import ParameterStore
        store = ParameterStore()
        store.set("simulation.speed", 4)
        store.set("anima.trauma", "fort")
        store.reset()
        self.assertEqual(store.get("simulation.speed"), 1)
        self.assertEqual(store.get("anima.trauma"), "normal")

    def test_param_by_group(self):
        from game.studio_parameters import ParameterStore
        store = ParameterStore()
        groups = store.by_group()
        self.assertIn("Population", groups)
        self.assertIn("Anima", groups)

    def test_param_validate_choice(self):
        from game.studio_parameters import ParameterStore
        store = ParameterStore()
        with self.assertRaises(ValueError):
            store.set("anima.trauma", "invalid_value")

    def test_runtime_config(self):
        from game.studio_parameters import ParameterStore
        store = ParameterStore()
        store.set("anima.trauma", "fort")
        rt = store.get_runtime()
        self.assertTrue(rt.trauma_enabled)
        self.assertEqual(rt.trauma_scale, 2.0)

    def test_param_to_dict(self):
        from game.studio_parameters import ParameterStore
        store = ParameterStore()
        d = store.to_dict()
        self.assertIn("simulation.speed", d)
        self.assertIn("anima.trauma", d)


class TestStudioScenarios(unittest.TestCase):
    def test_list_scenarios(self):
        from game.studio_scenarios import list_scenarios
        scenarios = list_scenarios()
        self.assertGreater(len(scenarios), 0)
        names = [s[0] for s in scenarios]
        self.assertIn("calme", names)
        self.assertIn("danger", names)

    def test_apply_scenario(self):
        from game.studio_scenarios import apply_scenario
        from game.studio_parameters import ParameterStore
        store = ParameterStore()
        apply_scenario(store, "calme")
        self.assertEqual(store.get("world.food"), "élevé")

    def test_scenario_summary(self):
        from game.studio_scenarios import scenario_summary
        s = scenario_summary("calme")
        self.assertIn("recommandée", s)

    def test_invalid_scenario_raises(self):
        from game.studio_scenarios import apply_scenario
        from game.studio_parameters import ParameterStore
        store = ParameterStore()
        with self.assertRaises(ValueError):
            apply_scenario(store, "nonexistent")


class TestStudioTimeline(unittest.TestCase):
    def test_normalize_event(self):
        from game.studio_timeline import normalize_event
        raw = {"tick": 150, "kind": "birth", "actor_name": "Aro", "title": "Naissance"}
        event = normalize_event(raw)
        self.assertEqual(event["tick"], 150)
        self.assertEqual(event["category"], "Famille")
        self.assertIn("Aro", event["actor_name"])

    def test_format_event(self):
        from game.studio_timeline import format_event
        event = {"tick": 150, "category": "Danger", "kind": "attack", "actor_name": "X"}
        result = format_event(event)
        self.assertIn("Jour", result)
        self.assertIn("Danger", result)

    def test_filter_events(self):
        from game.studio_timeline import filter_events, normalize_event
        events = [
            normalize_event({"tick": 100, "kind": "birth"}),
            normalize_event({"tick": 200, "kind": "attack"}),
            normalize_event({"tick": 300, "kind": "birth"}),
        ]
        births = filter_events(events, category="Famille")
        self.assertEqual(len(births), 2)

    def test_build_timeline(self):
        from game.studio_timeline import build_timeline
        raw = [{"tick": 200, "kind": "attack"}, {"tick": 100, "kind": "birth"}]
        tl = build_timeline(raw)
        self.assertEqual(tl[0]["tick"], 100)
        self.assertEqual(tl[1]["tick"], 200)

    def test_categories_exist(self):
        from game.studio_timeline import CATEGORIES
        self.assertIn("Tous", CATEGORIES)
        self.assertIn("Danger", CATEGORIES)
        self.assertIn("Famille", CATEGORIES)


class TestStudioReports(unittest.TestCase):
    def test_build_report(self):
        from game.studio_reports import build_report
        result = {
            "scenario": "Test", "seed": 42, "duration": 1000,
            "population_start": 20, "population_end": 18,
            "births": 3, "deaths": 5, "builds": 2,
        }
        report = build_report(result)
        self.assertIn("20", report)
        self.assertIn("18", report)
        self.assertIn("3", report)

    def test_build_short_summary(self):
        from game.studio_reports import build_short_summary
        result = {"population_start": 20, "population_end": 18, "deaths": 2, "builds": 1}
        summary = build_short_summary(result)
        self.assertIn("20", summary)
        self.assertIn("18", summary)

    def test_interpret_trust(self):
        from game.studio_reports import interpret_metric
        self.assertIn("augmenté", interpret_metric("trust", 0.5, 0.7))
        self.assertIn("diminué", interpret_metric("trust", 0.7, 0.5))
        self.assertIn("stable", interpret_metric("trust", 0.5, 0.52))

    def test_report_no_invention(self):
        from game.studio_reports import build_report
        result = {"population_start": 10, "population_end": 10}
        report = build_report(result)
        self.assertNotIn("attaque", report.lower())
        self.assertNotIn("traumatisme", report.lower())


class TestStudioCompare(unittest.TestCase):
    def test_compare_results(self):
        from game.studio_compare import compare_results
        a = {"population_end": 20, "deaths": 2, "mean_health": 0.8}
        b = {"population_end": 15, "deaths": 5, "mean_health": 0.5}
        rows = compare_results(a, b)
        self.assertEqual(len(rows), 9)

    def test_compare_summary(self):
        from game.studio_compare import compare_summary
        a = {"scenario": "A", "population_end": 20, "deaths": 2, "mean_health": 0.8}
        b = {"scenario": "B", "population_end": 15, "deaths": 5, "mean_health": 0.5}
        summary = compare_summary(a, b)
        self.assertIn("A", summary)
        self.assertIn("B", summary)


class TestStudioExport(unittest.TestCase):
    def test_export_json(self):
        import tempfile, os, json
        from game.studio_export import export_json
        path = os.path.join(tempfile.gettempdir(), "test_export.json")
        data = {"test": True, "value": 42}
        export_json(data, path)
        with open(path) as f:
            loaded = json.load(f)
        self.assertTrue(loaded["test"])
        self.assertEqual(loaded["value"], 42)
        os.unlink(path)

    def test_export_csv(self):
        import tempfile, os
        from game.studio_export import export_csv
        path = os.path.join(tempfile.gettempdir(), "test_export.csv")
        export_csv({"pop": 10, "deaths": 2}, path)
        with open(path) as f:
            content = f.read()
        self.assertIn("pop", content)
        os.unlink(path)

    def test_export_txt(self):
        import tempfile, os
        from game.studio_export import export_txt
        path = os.path.join(tempfile.gettempdir(), "test_export.txt")
        export_txt("Hello World", path)
        with open(path) as f:
            content = f.read()
        self.assertEqual(content, "Hello World")
        os.unlink(path)

    def test_export_markdown(self):
        from game.studio_export import export_markdown
        md = export_markdown("Test report", metrics={"pop": 10})
        self.assertIn("# Rapport", md)
        self.assertIn("pop", md)


class TestStudioSnapshots(unittest.TestCase):
    def test_level_label_readable(self):
        from game.studio_text import level_label
        self.assertEqual(level_label(0.5), "Moyen")


if __name__ == "__main__":
    unittest.main()
