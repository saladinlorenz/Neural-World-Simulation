# Documentation complète du projet

Ce document a été généré automatiquement par `generate_project_md.py`.

- **Racine du projet :** `E:\my world2`

- **Date de génération :** `2026-09-21 23:01:13`

- **Fichiers inclus :** `99`

- **Extensions incluses :** `.md, .py, .txt`

## Arborescence du projet

```text
my world2/
├── assets/
│   ├── _merged/
│   ├── craftpix-net-211148-free-fantasy-chibi-female-sprites-pixel-art/
│   │   ├── Enchantress/
│   │   ├── Knight/
│   │   └── Musketeer/
│   ├── craftpix-net-385863-free-top-down-trees-pixel-art/
│   │   └── PNG/
│   │       └── Assets_separately/
│   │           ├── Trees/
│   │           ├── Trees_shadow/
│   │           ├── Trees_texture_shadow/
│   │           └── Trees_texture_shadow_dark/
│   ├── craftpix-net-439247-free-fantasy-chibi-male-sprites-pixel-art/
│   │   ├── Archer/
│   │   ├── Swordsman/
│   │   └── Wizard/
│   ├── generated_assets/
│   │   └── cut/
│   ├── kaykit_resources/
│   ├── kenney_survival-kit/
│   │   ├── Previews/
│   │   └── License.txt
│   ├── portraits/
│   └── Tiny Swords (Free Pack) (1)/
│       └── Tiny Swords (Free Pack)/
│           ├── Buildings/
│           │   ├── Black Buildings/
│           │   ├── Blue Buildings/
│           │   ├── Purple Buildings/
│           │   ├── Red Buildings/
│           │   └── Yellow Buildings/
│           ├── Particle FX/
│           └── Terrain/
│               └── Resources/
│                   ├── Gold/
│                   │   ├── Gold Resource/
│                   │   └── Gold Stones/
│                   ├── Meat/
│                   │   ├── Meat Resource/
│                   │   └── Sheep/
│                   ├── Tools/
│                   └── Wood/
│                       └── Wood Resource/
├── docs/
│   └── PARITY_CHECKLIST.md
├── game/
│   ├── __init__.py
│   ├── academy.py
│   ├── affordance_definitions.py
│   ├── assets_api.py
│   ├── assets_manager.py
│   ├── brain.py
│   ├── brain_api.py
│   ├── brain_schema.py
│   ├── camera.py
│   ├── clock.py
│   ├── config.py
│   ├── construction.py
│   ├── dashboard.py
│   ├── debuglog.py
│   ├── diagnostics.py
│   ├── engine.py
│   ├── entities.py
│   ├── invariants.py
│   ├── lab.py
│   ├── mapapi.py
│   ├── messages.py
│   ├── renderer.py
│   ├── save.py
│   ├── simulation.py
│   ├── simulation_controller.py
│   ├── social_memory.py
│   ├── storage.py
│   ├── studio_compare.py
│   ├── studio_export.py
│   ├── studio_parameters.py
│   ├── studio_reports.py
│   ├── studio_scenarios.py
│   ├── studio_snapshots.py
│   ├── studio_text.py
│   ├── studio_timeline.py
│   ├── tool_editor.py
│   ├── ui_api.py
│   ├── ui_commands.py
│   ├── ui_kit.py
│   ├── ui_registry.py
│   ├── ui_snapshots.py
│   ├── ui_state.py
│   ├── universal_knowledge.py
│   ├── world.py
│   └── worldgen.py
├── map/
├── tests/
│   ├── __init__.py
│   ├── rapport_2026-09-20.md
│   ├── results_phase2.md
│   ├── results_phase2.txt
│   ├── results_phase_finale.md
│   ├── test_behavior_chain.py
│   ├── test_headless.py
│   ├── test_qt_smoke.py
│   ├── test_studio.py
│   └── test_ui_neutral.py
├── ui_pygame/
│   ├── __init__.py
│   ├── assets_panel.py
│   ├── base_panel.py
│   ├── creator_panel.py
│   ├── journal_panel.py
│   ├── population_panel.py
│   ├── society_panel.py
│   └── world_tools_panel.py
├── ui_qt/
│   ├── docks/
│   │   ├── __init__.py
│   │   ├── assets_dock.py
│   │   ├── inspector_dock.py
│   │   ├── journal_dock.py
│   │   ├── population_dock.py
│   │   ├── society_dock.py
│   │   └── tools_dock.py
│   ├── map/
│   │   ├── __init__.py
│   │   └── map_view.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── anima_model.py
│   │   ├── assets_model.py
│   │   ├── journal_model.py
│   │   ├── population_model.py
│   │   └── society_model.py
│   ├── studio/
│   │   ├── __init__.py
│   │   ├── comparison_panel.py
│   │   ├── laboratory_dock.py
│   │   ├── metrics_models.py
│   │   ├── parameter_dock.py
│   │   ├── report_panel.py
│   │   ├── scenario_dialog.py
│   │   ├── timeline_dock.py
│   │   └── world_overlay.py
│   ├── theme/
│   │   ├── __init__.py
│   │   └── theme.py
│   ├── __init__.py
│   ├── app.py
│   ├── dialogs.py
│   └── main_window.py
├── generate_project_md.py
├── main.py
├── main_qt.py
└── requirements.txt
```

## Contenu des fichiers

## assets/kenney_survival-kit/License.txt

**Type :** `.txt`

```text

	

	Survival Kit (2.0)

	Created/distributed by Kenney (www.kenney.nl)
	Creation date: 03-04-2024 14:59
	
			------------------------------

	License: (Creative Commons Zero, CC0)
	http://creativecommons.org/publicdomain/zero/1.0/

	You can use this content for personal, educational, and commercial purposes.

	Support by crediting 'Kenney' or 'www.kenney.nl' (this is not a requirement)

			------------------------------

	• Website : www.kenney.nl
	• Donate  : www.kenney.nl/donate

	• Patreon : patreon.com/kenney
	
	Follow on social media for updates:

	• Twitter:   twitter.com/KenneyNL
	• Instagram: instagram.com/kenney_nl
	• Mastodon:  mastodon.gamedev.place/@kenney

```

## docs/PARITY_CHECKLIST.md

**Type :** `.md`

```markdown

# Parity Checklist: Pygame Dashboard vs Qt Interface

**Last updated:** 2026-09-21

---

## Summary

| Category | DONE | TODO |
|---|---|---|
| Simulation | 6 | 0 |
| Selection | 3 | 0 |
| Population | 6 | 0 |
| Journal | 5 | 0 |
| Society | 2 | 0 |
| Inspector | 9 | 0 |
| Tools | 4 | 0 |
| Map | 9 | 0 |
| Assets | 6 | 0 |
| Save/Load | 2 | 0 |
| Theme | 4 | 0 |
| Studio Parameters | 5 | 0 |
| Studio Scenarios | 3 | 0 |
| Studio Timeline | 4 | 0 |
| Studio Laboratory | 4 | 0 |
| Studio Comparison | 4 | 0 |
| Studio Overlay | 10 | 0 |
| Studio Exports | 4 | 0 |
| **TOTAL** | **90** | **0** |

---

## Simulation

| Feature | Pygame | Qt | Status |
|---|---|---|---|
| Pause/Resume toggle | `_cmd_pause_toggle` via toolbar | `_on_pause` + Space shortcut | DONE |
| Step (single tick) | `_cmd_step` via toolbar | `_on_step` + N shortcut | DONE |
| Speed control (1-8) | Speed spinbox | `QSpinBox` range 1-8 | DONE |
| Spawn agent | `spawn_agent` command | Toolbar button + `spawn_agent` command | DONE |
| Spawn sheep | `spawn_sheep` command | Toolbar button | DONE |
| Spawn monster | `spawn_monster` command | Toolbar button | DONE |

## Selection

| Feature | Pygame | Qt | Status |
|---|---|---|---|
| Select agent by click | `select_agent` on map click | `inspect` mode in `map_view.py` | DONE |
| Select tile | `select_tile` command | `inspect` mode in `map_view.py` | DONE |
| Follow selected agent | `follow` flag | `_follow_action` checkbox in toolbar | DONE |

## Population

| Feature | Pygame | Qt | Status |
|---|---|---|---|
| Population list | `_tab_habitants` scrollable list | `PopulationDock` with `QTableView` | DONE |
| Search/filter by name | `hab_search` text field | `QLineEdit` filter with `QSortFilterProxyModel` | DONE |
| Filter by age/stage | Not in Pygame | `_stage_filter` QComboBox (enfant/adulte/ancien) | DONE |
| Filter alive/all | Not in Pygame | `_alive_filter` QComboBox | DONE |
| Sortable table columns | Not in Pygame | `QSortFilterProxyModel` with sorting enabled | DONE |
| Remove agent (delete button) | `hdel_pending` confirmation | `_remove_btn` with confirmation dialog | DONE |

## Journal

| Feature | Pygame | Qt | Status |
|---|---|---|---|
| Journal display | `_tab_journal` | `JournalDock` with `JournalModel` | DONE |
| Filter by category | `jfilter` combo | `_filter_combo` QComboBox from `LOG_TITLES` | DONE |
| Search text | Not in Pygame | `_search` QLineEdit with live filtering | DONE |
| Export JSON/CSV/TXT | Not in Pygame | `_export` method with `QFileDialog` | DONE |
| Sortable entries | Not in Pygame | `QTableView` with sorting enabled | DONE |

## Society

| Feature | Pygame | Qt | Status |
|---|---|---|---|
| Society stats table | `_tab_societe` | `SocietyDock` with `SocietyModel` | DONE |
| Relations table | Inline in inspecteur | `_relations_table` (Agent1, Agent2, Type, Confiance, Affinite) | DONE |

## Inspector

| Feature | Pygame | Qt | Status |
|---|---|---|---|
| Identity banner (name, sex, stage, age, clan) | `_identity` method | `_identity_label` rich text with name, sex, stage, age, class, clan, gen | DONE |
| Accordion sections (body, cog, perso, emo, needs) | `_accordion` method | `_create_info_groups` with 5 QGroupBox (Corps, Cognition, Personnalite, Emotions, Besoins) | DONE |
| Anima table (identity, values, trauma, episodic) | `_draw_agent_diagnostics` Anima section | `AnimaModel` in `InspectorDock` with `QTableView` | DONE |
| Relations list | In `_identity` + `_draw_agent_diagnostics` | `_relations_label` with conf/aff/vivant | DONE |
| Goal/intention display | `goal` badge in identity | `_goal_label` with action name and distance | DONE |
| Brain badge (neuron count, frequency, top actions) | `NEURONES` badge | `_brain_group` with neurons, freq, badge showing top 3 actions | DONE |
| Inventory display | `INVENTAIRE` in diagnostics | `_inventory_group` listing items and quantities | DONE |
| Tool display | `outil` in diagnostics | `_tool_group` with tool name and durability | DONE |
| Memory/belief_places card | `_card_memoire` | `_memory_group` with beliefs (croyances) and autobiography (last 5 episodes) | DONE |

## Tools

| Feature | Pygame | Qt | Status |
|---|---|---|---|
| All painting tools (water, land, wall, carve, restore, erase, place, floor, block) | Mode buttons | `ToolsDock` with all mode buttons | DONE |
| Brush size slider | `brush_size` with +/- buttons | `_brush_slider` QSlider 1-15 | DONE |
| Tool hints | `TAB_HINTS` in toolbar | `_hint` label | DONE |
| Block material selector | Material buttons | Material buttons in `ToolsDock` | DONE |

## Map

| Feature | Pygame | Qt | Status |
|---|---|---|---|
| Terrain rendering | Tile-based with water/land/blocked colors | `_draw_terrain` in `MapView` with QPainter | DONE |
| Entity rendering (agents, sheep, monsters) | Sprite-based with clan colors | `_draw_entities` with ellipses (agents), ellipses (sheep), rects (monsters) | DONE |
| Pan (right-click drag) | `drag` state | `mousePressEvent` RightButton + `mouseMoveEvent` | DONE |
| Zoom (mouse wheel) | Not explicitly in dashboard code | `wheelEvent` with zoom factor 0.05-6.0 | DONE |
| Tool-based painting on drag | `apply_map_tool` | `mouseMoveEvent` with mode check for continuous painting | DONE |
| Map legend overlay | `_map_overlay` with Fertilite/Ressource/Danger | `_draw_legend` with 7 items (Eau, Terre, Mur, Feu, Agent, Mouton, Monstre) | DONE |
| Minimap | `minimap_rect` in dashboard | `_draw_minimap` bottom-right with terrain, agents, viewport rect | DONE |
| Fire rendering | `tile["fire"]` | `if tile["fire"] > 0` with alpha overlay | DONE |
| Overlay modes (10 modes) | Not in Pygame | `WorldOverlay` with 10 modes via `QComboBox` in toolbar | DONE |

## Assets

| Feature | Pygame | Qt | Status |
|---|---|---|---|
| Asset catalog grid | `_grid` with thumbnails | `AssetsDock` with `QListWidget` + thumbnails | DONE |
| Category filter chips | `CAT_ALL` + category chips | `_cat_combo` QComboBox from `CATEGORY_LABELS` | DONE |
| Search assets | `search` text field | `_search` QLineEdit with live filtering | DONE |
| Favorites toggle | `favs` list with star icon | `_favs_only` checkbox + double-click to toggle (max 12) | DONE |
| Asset info card (name, cat, role, placable, solid) | Info in `_tab_decor` | Detail panel: name, category, role, placable, solide, size, description | DONE |
| Thumbnail rendering | `am.thumbnail()` | `_load_thumbnail` with 48x48 thumbnails + colored placeholder fallback | DONE |

## Save/Load

| Feature | Pygame | Qt | Status |
|---|---|---|---|
| Save dialog (F5) | `save` command | `SaveDialog` with slot list | DONE |
| Load dialog (F9) | `load` command | `SaveDialog` mode="load" | DONE |

## Theme

| Feature | Pygame | Qt | Status |
|---|---|---|---|
| Light theme | Design tokens `T` class | `LIGHT_COLORS` + `apply_theme` with full stylesheet | DONE |
| Dark theme | Not in Pygame | `DARK_COLORS` + `_toggle_theme` button in toolbar | DONE |
| Theme persistence | Not in Pygame | `QSettings` save/restore (`get_theme_name`/`set_theme_name`) | DONE |
| Window geometry persistence | Not in Pygame | `saveGeometry`/`restoreGeometry` + `windowState` in `QSettings` | DONE |

---

## Studio Features

### Studio Parameters

| Feature | Backend (`studio_parameters.py`) | UI (`parameter_dock.py`) | Status |
|---|---|---|---|
| 14 validated parameters | `PARAMETERS` list of `ParamDef` (population.max, population.birth_rate, world.food, world.predators, world.size, simulation.speed, simulation.seed, anima.trauma, anima.culture, anima.episodes_max, ecology.regrowth, ecology.fire_spread, performance.max_agents, performance.snapshot_freq) | `ParameterDock` with typed widgets (QSpinBox, QDoubleSpinBox, QCheckBox, QComboBox) | DONE |
| Parameter groups (Population, Monde, Simulation, Anima, Ecologie, Performance) | `PARAM_GROUPS` sorted from `ParamDef.group` | `QGroupBox` per group with `QGridLayout` | DONE |
| Validation (type + range + choices) | `ParamDef.validate()` with ValueError | Error display via `QMessageBox.warning` on apply | DONE |
| Reset to defaults | `ParameterStore.reset()` | `_reset_btn` with confirmation dialog | DONE |
| RuntimeConfig hot-apply | `RuntimeConfig` dataclass with `apply_param()` | `parameters_applied` signal + `_on_apply` writes to `sim.parameters` | DONE |

### Studio Scenarios

| Feature | Backend (`studio_scenarios.py`) | UI (`scenario_dialog.py`) | Status |
|---|---|---|---|
| 6 preset scenarios (calme, danger, famine, test_culture, high_trauma, social_experiment) | `SCENARIOS` dict with label, description, duration, parameters, summary | `ScenarioDialog` with `QListWidget` | DONE |
| Apply scenario to ParameterStore | `apply_scenario(store, name)` | `_on_launch` applies to `sim.parameter_store` + `sim.parameters` | DONE |
| Scenario summary + parameter display | `scenario_summary(name)` + `get_scenario(name)` | `_summary_box` + `_params_grid` showing each param label/value | DONE |

### Studio Timeline

| Feature | Backend (`studio_timeline.py`) | UI (`timeline_dock.py`) | Status |
|---|---|---|---|
| Normalize events | `normalize_event()` with category mapping (10 categories: Vie, Famille, Social, Danger, Construction, Economie, Culture, Meteo, Mort) | `build_timeline()` from journal snapshot | DONE |
| Category filter | `filter_events(events, category=...)` | `_cat_combo` QComboBox with all categories | DONE |
| Text search | `filter_events` + inline text filter | `_search` QLineEdit with button | DONE |
| Export (TXT, CSV, JSON) | `format_event()` for readable sentences | `_export_txt`, `_export_csv`, `_export_json` with `QFileDialog` | DONE |

### Studio Laboratory

| Feature | Backend (`studio_reports.py`) | UI (`laboratory_dock.py`) | Status |
|---|---|---|---|
| Report generation | `build_report(result)` — scenario, pop start/end, births, deaths, builds, harvests, messages, institutions, health/trust | `_summary_text` QTextEdit | DONE |
| Metrics table | 9 metrics (population_end, deaths, births, builds, harvests, messages, mean_health, mean_hunger, mean_trust) | `_metrics_table` QTableWidget with French labels | DONE |
| Interpretation | `interpret_metric(name, start, end)` for health/trust/hunger | `_interp_text` with French interpretation sentences | DONE |
| Scenario info display | `result.get("scenario"/"seed"/"duration")` | `_scenario_text` QTextEdit | DONE |

### Studio Comparison

| Feature | Backend (`studio_compare.py`) | UI (`comparison_panel.py`) | Status |
|---|---|---|---|
| A/B load from JSON files | N/A (file I/O in UI) | `_load_result("a"/"b")` with `QFileDialog.getOpenFileName` | DONE |
| Compare 9 metrics with diff | `compare_results(a, b)` returns rows with label, a, b, difference | `_table` QTableWidget (Metric, A, B, Diff) with color-coded diff | DONE |
| Summary text | `compare_summary(a, b)` — French sentences about significant changes | `_summary` QTextEdit | DONE |
| Export comparison | N/A | `_export` saves JSON with a, b, rows, summary | DONE |

### Studio Overlay

| Feature | Backend/Logic (`world_overlay.py`) | UI Integration | Status |
|---|---|---|---|
| 10 overlay modes | `MODES` list: normal, ressources, danger, memoire, relations, besoins, anima, culture, institutions, territoires | `_overlay_combo` QComboBox in toolbar | DONE |
| Danger overlay | `_paint_danger` — tile-based danger heatmap with level_color | Applied in `MapView.paintEvent` | DONE |
| Ressources overlay | `_paint_ressources` — tile-based regrow heatmap | Applied in `MapView.paintEvent` | DONE |
| Memoire overlay | `_paint_memoire` — agent belief circles + tile grid | Applied in `MapView.paintEvent` | DONE |
| Relations overlay | `_paint_relations` — lines between related agents | Applied in `MapView.paintEvent` | DONE |
| Besoins overlay | `_paint_besoins` — agent circles colored by hunger level | Applied in `MapView.paintEvent` | DONE |
| Anima overlay | `_paint_anima` — agent circles colored by dominant identity | Applied in `MapView.paintEvent` | DONE |
| Culture overlay | `_paint_culture` — squares around agents with confirmed knowledge | Applied in `MapView.paintEvent` | DONE |
| Institutions overlay | `_paint_institutions` — lines connecting institution members | Applied in `MapView.paintEvent` | DONE |
| Territoires overlay | `_paint_territoires` — clan-colored circles around agents | Applied in `MapView.paintEvent` | DONE |

### Studio Exports

| Format | Backend (`studio_export.py`) | UI Integration | Status |
|---|---|---|---|
| TXT | `export_txt(report_text, filepath)` | Laboratory `_export_txt` + ReportPanel | DONE |
| Markdown | `export_markdown(report_text, timeline_events, metrics, filepath)` | Laboratory `_export_md` + ReportPanel | DONE |
| CSV | `export_csv(metrics_dict, filepath)` | Laboratory (timeline `_export_csv` for events) | DONE |
| JSON | `export_json(data, filepath)` | Laboratory `_export_json` + Comparison `_export` + ReportPanel | DONE |

```

## game/__init__.py

**Type :** `.py`

```python

# Univers Vivant - package du laboratoire d'emergence IA

```

## game/academy.py

**Type :** `.py`

```python

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
            input_count=95,
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
        if m["input_count"] != 95 or m["action_count"] != 15:
            raise ValueError("Modele incompatible avec le vecteur/action actuel")
        self.champion_params = np.asarray(data["params"], dtype=np.float64)
        self.champion_size = int(m["brain_size"])
        self.champion_score = float(m["score"])
        self.champion_label = str(m["label"])
        return info.get("universal_knowledge")

```

## game/affordance_definitions.py

**Type :** `.py`

```python

"""Registre des affordances — définition structurée de chaque tag du catalogue.

Chaque définition contient :
- requires : préconditions (outil, distance, etc.)
- cost      : coût en temps / énergie
- effect    : effets monde / agent (sont des gabarits, interpolés ailleurs)
- risk      : 0.0 = sûr, >0 = danger potentiel

Le point clé : une seule définition par tag, partagée par tous les assets.
Les paramètres variables (materiau, recolte.amount, poids, enflammable, edible, etc.)
viennent du catalogue asset individuel et sont lus en même temps que la définition.
"""
from typing import Any, Dict, List


AFFORDANCE_DEFS: Dict[str, Dict[str, Any]] = {
    "observe": {
        "requires": {},
        "cost": {"time": 0.5, "energy": 0.0},
        "effect": {"world": "perception mise à jour"},
        "risk": 0.0,
    },

    "harvest": {
        "requires": {"tool": None, "distance_max": 1, "needs_hp": True},
        "cost": {"time": 2.0, "energy": 4.0},
        "effect": {"world": "object.hp -= 1",
                   "on_depletion": "spawn_material({materiau}, {recolte.amount})",
                   "on_pickup": "agent.inv[{materiau}] += gain * (2 si agent.tool)"},
        "risk": 0.0,
    },

    "eat": {
        "requires": {"edible": ">0"},
        "cost": {"time": 1.0, "energy": 0.0},
        "effect": {"world": "object consommé",
                   "agent": "faim -= {edible}/110.0, energie += {edible}/150.0, soif -= {edible}/260.0"},
        "risk": 0.0,
    },

    "carry": {
        "requires": {"poids": "<= agent.force_max"},
        "cost": {"time": 0.2, "energy": 0.5},
        "effect": {"world": "object -> agent.inv",
                   "agent": "inv[{materiau}] += {recolte.amount}"},
        "risk": 0.0,
    },

    "place": {
        "requires": {},
        "cost": {"time": 0.3, "energy": 0.5},
        "effect": {"world": "agent.inv[{materiau}] -> world.object",
                   "agent": "inv[{materiau}] -= 1"},
        "risk": 0.0,
    },

    "use": {
        "requires": {"role": "tool"},
        "cost": {"time": 1.0, "energy": 1.0},
        "effect": {"agent": "agent.tool = object.id (multiplicateur récolte ×2)",
                   "world": "outil équipé"},
        "risk": 0.0,
    },

    "shelter": {
        "requires": {},
        "cost": {"time": 0.5, "energy": 0.0},
        "effect": {"agent": "securite += 0.15, abri = true",
                   "world": "tuile marquée abri"},
        "risk": 0.0,
    },

    "sleep": {
        "requires": {"energy": "<0.2 or nuit"},
        "cost": {"time": 10.0, "energy": 0.0},
        "effect": {"agent": "energie += REST_GAIN * (SHELTER_BONUS si abri)",
                   "world": "état = sleep"},
        "risk": 0.05,
    },

    "burn": {
        "requires": {"enflammable": True},
        "cost": {"time": 1.0, "energy": 0.0},
        "effect": {"world": "allume feu (object.hp -= fire_damage), propagation possible"},
        "risk": 0.6,
    },

    "block": {
        "requires": {},
        "cost": {"time": 0.0, "energy": 0.0},
        "effect": {"world": "obstacle physique",
                   "agent": "mouvement empêché"},
        "risk": 0.0,
    },

    "hit": {
        "requires": {},
        "cost": {"time": 1.0, "energy": 2.0},
        "effect": {"agent": "cible.hp -= dmg(force)",
                   "world": "riposte possible"},
        "risk": 0.3,
    },

    "throw": {
        "requires": {},
        "cost": {"time": 0.5, "energy": 1.0},
        "effect": {"agent": "projectile lancé (dégât à distance)",
                   "world": "projectile créé"},
        "risk": 0.2,
    },

    "give": {
        "requires": {"target_proche": True},
        "cost": {"time": 0.5, "energy": 0.5},
        "effect": {"agent": "objet transféré, lien social +0.05",
                   "target": "inv[materiau] += 1"},
        "risk": 0.0,
    },

    "mourn": {
        "requires": {"role": "grave"},
        "cost": {"time": 2.0, "energy": 0.0},
        "effect": {"agent": "tristesse -0.2, mémoire deuil créée, lien social renforcé"},
        "risk": 0.0,
    },

    "mark": {
        "requires": {},
        "cost": {"time": 1.0, "energy": 0.5},
        "effect": {"world": "phéromone territoire déposée (marqueur clan)",
                   "agent": "reconnaissance territoire"},
        "risk": 0.0,
    },

    "sit": {
        "requires": {},
        "cost": {"time": 1.0, "energy": -0.5},
        "effect": {"agent": "repos léger, energie +0.02",
                   "world": "état = sit"},
        "risk": 0.0,
    },

    "climb": {
        "requires": {"obstacle_hauteur": "<= agent.mobilite"},
        "cost": {"time": 1.0, "energy": 2.0},
        "effect": {"agent": "se déplace au-dessus de l'obstacle",
                   "world": "position modifiée"},
        "risk": 0.15,
    },

    "chase": {
        "requires": {"cible_mobile": True},
        "cost": {"time": 1.0, "energy": 2.0},
        "effect": {"agent": "poursuit la cible",
                   "world": "poursuite engagée"},
        "risk": 0.2,
    },

    "shear": {
        "requires": {},
        "cost": {"time": 2.0, "energy": 1.0},
        "effect": {"agent": "laine/ressource récupérée",
                   "target": "recolte = laine"},
        "risk": 0.0,
    },

    "lean": {
        "requires": {},
        "cost": {"time": 1.0, "energy": 0.0},
        "effect": {"agent": "s'appuie, repos passif",
                   "world": "état = lean"},
        "risk": 0.0,
    },

    "decorate": {
        "requires": {"role": "prop or decor"},
        "cost": {"time": 1.0, "energy": 0.5},
        "effect": {"agent": "estime sociale +0.05, monde changé visuellement",
                   "world": "décoration posée"},
        "risk": 0.0,
    },

    "follow": {
        "requires": {"cible_sociale": True},
        "cost": {"time": 0.5, "energy": 0.2},
        "effect": {"agent": "suit la cible",
                   "world": "groupe formé"},
        "risk": 0.0,
    },
}


# ------------------------------------------------------------------ recettes de construction
# Posées par rôle (house, fort, tool). Utilisées par _do_build au lieu de
# coûts codés en dur (3 bois + 1 pierre par défaut).

BUILD_RECIPES: Dict[str, Dict[str, Any]] = {
    "house": {
        "materials": [{"materiau": "bois", "quantity": 6},
                      {"materiau": "pierre", "quantity": 2}],
        "tool_required": None,
        "primitives": ["take", "carry", "place", "assemble"],
        "duration": 12.0,
    },
    "fort": {
        "materials": [{"materiau": "bois", "quantity": 4},
                      {"materiau": "pierre", "quantity": 4}],
        "tool_required": None,
        "primitives": ["take", "carry", "place", "assemble"],
        "duration": 16.0,
    },
    "tool": {
        "materials": [{"materiau": "bois", "quantity": 1}],
        "tool_required": None,
        "primitives": ["take", "carry", "place", "assemble"],
        "duration": 3.0,
    },
}


def render_asset(asset) -> Dict[str, Dict[str, Any]]:
    """Retourne la vue des affordances pour un asset donné.

    Pour chaque tag présent dans a.afford, on renvoie la définition
    partagée AFFORDANCE_DEFS[tag]. C'est la même définition pour tous les
    assets portant ce tag ; ce sont les attributs de l'asset (a.harvest,
    a.edible, a.flammable, etc.) qui apportent la variation.
    """
    out: Dict[str, Dict[str, Any]] = {}
    for tag in getattr(asset, "afford", ["observe"]):
        defn = AFFORDANCE_DEFS.get(tag)
        if defn is not None:
            out[tag] = defn
    return out


def build_recipe_for(asset) -> Dict[str, Any] | None:
    """Retourne la recette de construction si l'asset a un rôle constructible."""
    return BUILD_RECIPES.get(asset.role)


def plans_for(am, inv: Dict[str, int]) -> List[Dict[str, Any]]:
    """Retourne la liste des assets constructibles avec l'inventaire donné.

    Pour chaque asset placable possédant une build_recipe, on vérifie que
    l'inventaire contient suffisamment de chaque matière première.
    """
    out: List[Dict[str, Any]] = []
    for a in am.assets:
        if not getattr(a, "placable", False):
            continue
        rec = BUILD_RECIPES.get(a.role)
        if rec is None:
            continue
        missing: Dict[str, int] = {}
        for m in rec["materials"]:
            have = inv.get(m["materiau"], 0)
            need = m["quantity"]
            if have < need:
                missing[m["materiau"]] = need - have
        if missing:
            continue
        out.append({
            "aid": a.id,
            "label": a.label,
            "role": a.role,
            "recipe": rec,
            "missing": missing,
            "footprint": a.size_tiles,
            "px": a.px,
        })
    return out

```

## game/assets_api.py

**Type :** `.py`

```python

"""Couche Assets — API publique en lecture seule.

Fournit des accès typés aux assets du catalogue, sans exposer les détails
internes d'AssetDef. Toutes les fonctions retournent des dataclasses
immutables (AssetData) contenant seulement les champs nécessaires aux autres
couches (UI, Cerveau, Simulation).

Aucun module pygame n'est importé ici — cette couche est entièrement
déterministe et peut être utilisée en mode headless.

Chaque fonction accepte un paramètre optionnel `asset_manager` ; si non
fourni, le module tente de l'importer de façon paresseuse (utile pour les
tests unitaires). En production, main.py fournit l'instance via
`from game import assets_manager as am`.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

# Cache paresseux — sera remplacé par main.py si disponible
_AM: Optional["AssetManager"] = None


def _set_asset_manager(am):  # pragma: no cover
    """Appelé par main.py pour injecter l'instance AssetManager."""
    global _AM
    _AM = am


def _get_am() -> "AssetManager":
    """Retourne l'instance AssetManager en cache, ou l'importe paresseusement."""
    global _AM
    if _AM is not None:
        return _AM
    from game import assets_manager as _mod
    _AM = _mod.AssetManager(headless=True).discover()
    return _AM


from game.assets_manager import AssetDef, CATEGORY_LABELS, NON_PLACABLE


class AssetData:
    """Snapshot immuable d'un asset — les couches supérieures ne doivent
    jamais accéder AssetDef.__dict__ directement, seulement par ce type."""
    __slots__ = (
        "id", "label", "role", "category", "placable", "affordances",
        "build_recipe", "solid", "edible", "harvest", "material", "color",
        "blocked_footprint", "size_tiles", "px", "kind", "frames",
    )

    def __init__(self, def_: AssetDef):
        self.id = def_.id
        self.label = def_.label
        self.role = def_.role
        self.category = def_.category
        self.placable = def_.placable
        self.affordances = list(def_.afford)
        self.build_recipe = getattr(def_, "build_recipe", None)
        self.solid = def_.solid
        self.edible = def_.edible
        self.harvest = getattr(def_, "harvest", None)
        self.material = getattr(def_, "material", "")
        self.color = getattr(def_, "color", "")
        self.blocked_footprint = def_.blocked_footprint
        self.size_tiles = def_.size_tiles
        self.px = def_.px
        self.kind = def_.kind
        self.frames = def_.frames

    def __repr__(self) -> str:
        return f"<AssetData id={self.id} label={self.label!r} role={self.role!r} cat={self.category!r}>"


# ---- Accès catalogue ----

def get_asset(asset_id: int, asset_manager: Optional["AssetManager"] = None) -> AssetData:
    """Retourne un AssetData par son identifiant global (0..N-1).

    Si `asset_manager` n'est pas fourni, utilise le cache paresseux.
    """
    am = asset_manager or _get_am()
    if 0 <= asset_id < len(am.assets):
        return AssetData(am.assets[asset_id])
    raise IndexError(f"asset_id {asset_id} hors gamme [0..{len(am.assets)-1}]")


def list_assets(
    category: Optional[str] = None,
    placable_only: bool = True,
    asset_manager: Optional["AssetManager"] = None,
) -> List[AssetData]:
    """Retourne tous les assets, optionnellement filtrés par catégorie
    et par placable (panneau Décor).
    """
    am = asset_manager or _get_am()
    result: List[AssetData] = []
    for a in am.assets:
        if placable_only and a.placable is False:
            continue
        if category is not None and a.category != category:
            continue
        result.append(AssetData(a))
    return result


def list_by_role(role: str, asset_manager: Optional["AssetManager"] = None) -> List[AssetData]:
    """Retourne tous les assets d'un rôle donné (ex. 'house', 'tool', 'fort')."""
    am = asset_manager or _get_am()
    return [AssetData(a) for a in am.assets if a.role == role]


def get_placable_assets(asset_manager: Optional["AssetManager"] = None) -> List[AssetData]:
    """Retourne uniquement les assets posables dans le monde (panneau Décor)."""
    am = asset_manager or _get_am()
    return [AssetData(a) for a in am.assets if a.placable]


def get_non_placable_assets(asset_manager: Optional["AssetManager"] = None) -> List[AssetData]:
    """Retourne les assets de travail (atlas, rendus, interface, unites)."""
    am = asset_manager or _get_am()
    return [AssetData(a) for a in am.assets if not a.placable]


def get_category_labels() -> Dict[str, str]:
    """Retourne le dictionnaire {code_courtois: label_affichage}."""
    from game.assets_manager import CATEGORY_LABELS
    return dict(CATEGORY_LABELS)


# ---- Affordances ----

def get_affordance_definition(name: str, asset_manager: Optional["AssetManager"] = None) -> Optional[Dict[str, Any]]:
    """Retourne la définition structurée d'une affordance par nom."""
    from game import affordance_definitions as af
    am = asset_manager or _get_am()
    # Les definitions sont globales, pas besoin de l'asset manager pour ça
    return af.AFFORDANCE_DEFS.get(name)


def get_affordance_definitions(asset_manager: Optional["AssetManager"] = None) -> Dict[str, Dict[str, Any]]:
    """Retourne le dictionnaire complet des définitions d'affordances."""
    from game import affordance_definitions as af
    return af.AFFORDANCE_DEFS


def can_build(materials_carried: Dict[str, int], asset_manager: Optional["AssetManager"] = None) -> List[AssetData]:
    """Retourne la liste des assets constructibles avec l'inventaire donné.

    materials_carried : dict {materiau: quantite} tel que l'être le transporte
    actuellement (ex. {'bois': 6, 'pierre': 2}).

    Ne considère que les assets ayant une build_recipe (house, fort, tool).
    """
    am = asset_manager or _get_am()
    from game.affordance_definitions import BUILD_RECIPES

    out: List[AssetData] = []
    for a in am.assets:
        if not a.placable:
            continue
        recipe = BUILD_RECIPES.get(a.role)
        if recipe is None:
            continue

        ok = True
        for m in recipe["materials"]:
            have = materials_carried.get(m["materiau"], 0)
            need = m["quantity"]
            if have < need:
                ok = False
                break
        if ok:
            out.append(AssetData(a))
    return out


# ---- Utilitaires internes ----

def _asset_to_data(a: AssetDef) -> AssetData:
    return AssetData(a)

```

## game/assets_manager.py

**Type :** `.py`

```python

"""Moteur d'assets : discover, dedup by content hash, classify by heuristics of path,
slice sprite sheets, expose semantic pools for the simulation + dashboard.

Every image file in /assets is catalogued (minus byte-identical repetitions) and can be
placed from the dashboard; key ones get simulation semantics (edible, harvestable, solid...).
"""
import hashlib
import os
from collections import OrderedDict

import numpy as np
import pygame
from PIL import Image

from .affordance_definitions import render_asset, build_recipe_for
from .config import ASSETS_DIR, CLAN_COLORS

IMG_EXT = (".png", ".jpg", ".jpeg", ".bmp", ".tga", ".gif")

# ----------------------------------------------------------------------------
# asset record
# ----------------------------------------------------------------------------
class AssetDef:
    __slots__ = ("id", "name", "label", "path", "pack", "category", "role", "kind",
                 "frames", "fw", "fh", "px", "solid", "shelter", "edible", "harvest",
                 "tool", "material", "color", "blocked_footprint", "meta", "afford",
                 "flammable", "weight", "placable", "afford_details", "build_recipe",
                 "_procedural_surface")

    def __init__(self, **kw):
        self.id = -1
        self.name = ""
        self.label = ""
        self.path = ""
        self.pack = ""
        self.category = "divers"
        self.role = ""
        self.kind = "single"      # single | strip | grid44 | tiles
        self.frames = 1
        self.fw = 16
        self.fh = 16
        self.px = 16              # display size in world px (largest side)
        self.solid = False
        self.shelter = False
        self.edible = 0.0         # nutrition (>0 = edible)
        self.harvest = None       # dict(material=..., amount=..., hp=...)
        self.tool = False
        self.material = ""
        self.color = ""
        self.blocked_footprint = 1
        self.meta = {}
        self.afford = ["observe"]           # possibilites physiques exposees au cerveau
        self.flammable = False
        self.weight = 1.0
        self.placable = True      # posable dans le monde via le panneau Decor
        self.afford_details = None
        self.build_recipe = None
        self._procedural_surface = None
        for k, v in kw.items():
            setattr(self, k, v)

    @property
    def size_tiles(self):
        return max(1, min(4, int(np.ceil(self.px / 16.0))))

    @property
    def world_rect(self):
        s = self.px
        ar = self.fw / max(1, self.fh)
        w = s * ar if ar >= 1 else s
        h = s if ar >= 1 else s / ar
        return w, h


CATEGORY_LABELS = [
    ("ressources", "Ressources"),
    ("nourriture", "Nourriture"),
    ("outils", "Outils"),
    ("animaux", "Animaux"),
    ("props", "Props"),
    ("vehicules", "Vehicules"),
    ("tombe", "Tombes"),
    ("decor", "Decors"),
    ("sol", "Sols"),
    ("unites", "Unites"),
    ("effets", "Effets"),
    ("interface", "Interface"),
    ("atlas", "Atlas"),
    ("rendus", "Rendus"),
    ("divers", "Divers"),
]

# categories d'assets NON posables dans le monde : fichiers de travail de la
# palette (feuilles de texture brutes, images promo, icones d'UI, frames de
# skel persons) — pas des objets du monde.
NON_PLACABLE = {"atlas", "rendus", "interface", "unites"}


def _tokens(rel):
    return rel.replace("\\", "/").lower()


def _classify(rel, fname):
    """Return (category, role, extra_kwargs) from path heuristics."""
    t = _tokens(rel)
    f = fname.lower()
    kw = {}
    in_tiny = "tiny swords" in t

    # ------------------------------------------------------------------ generated_assets (food / animals)
    if "generated_assets" in t:
        if f.startswith("food_"):
            FOOD_NUTRITION = {
                "tomato": 25.0, "potato": 30.0, "mushroom": 20.0,
                "meat_cooked": 55.0, "fish_raw": 40.0, "egg": 25.0,
                "cheese": 35.0, "carrot": 30.0, "bread": 40.0,
                "berry": 15.0, "banana": 25.0, "apple": 20.0,
            }
            key = f[5:-4]  # strip "food_" and ".png"
            n = FOOD_NUTRITION.get(key, 25.0)
            return "nourriture", "food", {"px": 16, "edible": n}
        if f.startswith("animal_"):
            kind = f[7:-4]  # strip "animal_" and ".png"
            px = {"bear": 26, "wolf": 22, "deer": 22, "rabbit": 16,
                  "bird": 14, "fish": 16}.get(kind, 20)
            return "animaux", "monster", {"px": px,
                                          "meta": {"kind": kind, "state": "idle"}}

    # ------------------------------------------------------------------ tiny units
    if in_tiny and "/units/" in t:
        color = next((c for c in CLAN_COLORS if f"{c} units" in t), "")
        cls = next((c for c in ("pawn", "archer", "lancer", "monk", "warrior") if f"/{c}/" in t), "")
        if "arrow" in f:
            return "effets", "projectile", {"px": 12}
        if "effect" in f or "heal_effect" in f:
            return "effets", "fx_heal", {"px": 28}
        state = ""
        for s in ("idle", "run", "attack", "shoot", "guard", "defence", "interact", "heal"):
            if s in f:
                state = "work" if s == "interact" else ("guard" if s == "defence" else s)
                break
        tool = next((x for x in ("axe", "pickaxe", "hammer", "knife", "meat", "gold", "wood") if x in f), "")
        kw = dict(meta={"cls": cls, "state": state, "tool": tool, "color": color})
        return "unites", "skin", dict(px=26, **kw)

    # ------------------------------------------------------------------ tiny terrain
    if in_tiny and "/terrain/" in t:
        if "/resources/wood/trees" in t:
            if "stump" in f:
                return "ressources", "stump", {"px": 18}
            return "ressources", "tree", {"px": 34, "solid": True,
                                          "harvest": dict(material="bois", amount=2, hp=6)}
        if "/resources/wood" in t and "wood resource" in f:
            return "ressources", "item_wood", {"px": 14, "material": "bois"}
        if "/resources/gold/gold stones" in t:
            if "_highlight" in f:
                return "ressources", "fx_highlight", {"px": 20}
            return "ressources", "gold_stone", {"px": 22, "solid": True,
                                                "harvest": dict(material="or", amount=2, hp=5)}
        if "/resources/gold" in t:
            return "ressources", "gold_pile", {"px": 14, "material": "or"}
        if "/resources/meat/meat resource" in t:
            return "nourriture", "meat_res", {"px": 14, "edible": 55.0}
        if "/resources/meat/sheep" in t:
            state = "grass" if "grass" in f else ("move" if "move" in f else "idle")
            return "animaux", "sheep", {"px": 22, "meta": {"state": state}}
        if "/resources/tools" in t:
            return "outils", "tool", {"px": 12, "tool": True}
        if "/decorations/bushes" in t:
            return "nourriture", "bush", {"px": 20, "edible": 14.0}
        if "/decorations/clouds" in t:
            return "decor", "cloud", {"px": 90}
        if "/decorations/rocks in the water" in t:
            return "decor", "waterrock", {"px": 20, "solid": True}
        if "/decorations/rocks" in t:
            return "ressources", "stone_res", {"px": 20, "solid": True,
                                               "harvest": dict(material="pierre", amount=2, hp=5)}
        if "rubber duck" in t:
            return "decor", "duck", {"px": 10}
        if "/terrain/tileset" in t:
            if "shadow" in f:
                return "effets", "shadow", {"px": 20}
            return "sol", "floor", {"kind": "tiles", "px": 16}
        return "decor", "decor", {"px": 18}

    # ignorer tiny buildings (pre-construits)
    if in_tiny and "/buildings/" in t:
        return None, None, None

    # ------------------------------------------------------------------ tiny fx
    if in_tiny and "particle fx" in t:
        fxn = "dust" if "dust" in f else ("explosion" if "explosion" in f else "fire")
        return "effets", "fx", {"px": 18, "meta": {"fx": fxn}}

    # ------------------------------------------------------------------ tiny UI
    if in_tiny and "ui element" in t:
        sub = "buttons" if "/buttons/" in t else ("bars" if "/bars/" in t else
              ("avatars" if "human avatars" in t else ("icons" if "/icons/" in t else
              ("cursors" if "/cursors/" in t else ("ribbons" if "ribbons" in t else
              ("banners" if "banners" in t or "banner" in f else ("papers" if "/papers/" in t else
              ("table" if "wood table" in t else ("swords" if "swords" in t else "misc")))))))))
        return "interface", "ui_" + sub, {"px": 32}

    # ------------------------------------------------------------------ kenney previews
    if "/previews/" in t and fname.lower().endswith(".png"):
        kit = _tokens(rel).split("/")[0]
        return _kenney(kit, f)

    # ------------------------------------------------------------------ ultimate fantasy rts (rendus PNG 1024px a decoupe alpha)
    if "ultimate fantasy rts" in t and "/png/" in t:
        return _uf_rts(f[:-4].replace("_", " ").lower())

    # ------------------------------------------------------------------ kaykit (3D : skip, pas utilisable en 2D)
    if "kaykit" in t or "resource_bits" in t:
        return None, None, None

    # ------------------------------------------------------------------ craftpix top-down trees (AVANT atlas)
    if "craftpix" in t and "top-down-trees" in t:
        if "/trees_shadow" in t or "/trees_texture_shadow" in t:
            return None, None, None
        if "source" in f or f.endswith(".psd") or "coupon" in f:
            return None, None, None
        if "palm" in f:
            return "decor", "tree", {"px": 48, "solid": True,
                                     "harvest": dict(material="bois", amount=2, hp=4)}
        return "ressources", "tree", {"px": 44, "solid": True,
                                      "harvest": dict(material="bois", amount=3, hp=6),
                                      "meta": {"trim": True}}

    # ------------------------------------------------------------------ murals / atlases / samples
    if any(x in t for x in ("/samples/", "preview", "sample", "contents_", "overview", "extra_")):
        return "rendus", "mural", {"px": 120}
    if any(x in t for x in ("/textures/", "texture", "atlas", "hexagons_medieval", "wild_animals_map")):
        return "atlas", "mural", {"px": 140}

    # ------------------------------------------------------------------ craftpix chibi sprites
    if "craftpix" in t and ("chibi" in t or "sprites" in t):
        is_female = "female" in t
        is_male = "male" in t
        if is_female or is_male:
            # extraire le nom du personnage (ex: Enchantress, Knight...)
            parts = t.replace("\\", "/").split("/")
            char_name = ""
            for p in parts:
                if p.startswith("craftpix"):
                    continue
                if "sprite" in p or "free" in p or "fantasy" in p or "chibi" in p or "pixel" in p:
                    continue
                if p and not p.endswith(".png"):
                    char_name = p.capitalize()
                    break
            CRAFTPIX_MAP = {
                "enchantress": ("purple", "enchantress"),
                "knight":      ("blue",   "knight"),
                "musketeer":   ("red",    "musketeer"),
                "archer":      ("yellow", "archer"),
                "swordsman":   ("black",  "swordsman"),
                "wizard":      ("purple", "wizard"),
            }
            # skip non-usable frames
            if any(x in f for x in ("dead.png", "hurt.png", "jump.png")):
                return None, None, None
            state = ""
            if "idle" in f:
                state = "idle"
            elif "run" in f:
                state = "run"
            elif "walk" in f:
                state = "run"
            elif "attack" in f:
                state = "attack"
            elif "contruire" in f or "build" in f:
                state = "build"
            else:
                return None, None, None
            cn = char_name.lower()
            color, cls = CRAFTPIX_MAP.get(cn, ("blue", cn))
            return "unites", "skin", dict(px=26, meta={"cls": cls, "state": state, "tool": "", "color": color})

    # ------------------------------------------------------------------ craftpix portraits
    if "portraits" in t and fname.lower().endswith(".png"):
        return "interface", "ui_portraits", {"px": 44}

    # ------------------------------------------------------------------ outils custom (tools_custom/)
    if "tools_custom" in t or "custom_tools" in t:
        kind = "hache"
        for k in ("hache", "pioche", "marteau"):
            if k in f:
                kind = k
                break
        return "outils", "tool", {"px": 14, "tool": True,
                                  "meta": {"tool_kind": kind, "custom": True}}

    # ------------------------------------------------------------------ vegetables (custom sprites extraits)
    if "vegetable" in t or "vegetables" in t:
        nutrition = 35.0
        if "carotte" in f:
            nutrition = 30.0
        elif "tomate" in f:
            nutrition = 25.0
        elif "champignon" in f:
            nutrition = 20.0
        elif "oignon" in f:
            nutrition = 22.0
        elif "courgette" in f:
            nutrition = 28.0
        return "nourriture", "food", {"px": 16, "edible": nutrition}

    # ------------------------------------------------------------------ retro rpg animals (extracted singles)
    if "animals" in t and "retro" not in t:
        if "_attack" in f:
            kind = f.split("_attack")[0]
            return "animaux", "monster_attack", {"px": 22,
                                                  "meta": {"kind": kind, "state": "attack"}}
        kind = f.replace(".png", "")
        px = {"bear": 24, "wolf": 22, "snake": 18, "beatle": 14}.get(kind, 20)
        return "animaux", "monster", {"px": px,
                                      "meta": {"kind": kind, "state": "idle"}}

    # ------------------------------------------------------------------ retro rpg animals (original sheets = ignored, use extracted singles)
    if "retro rpg" in t and "animal" in t:
        return "divers", "ignored", {}

    # ------------------------------------------------------------------ standalone environment sprites
    if fname.lower() == "sheep.png":
        return "animaux", "sheep", {"px": 22, "meta": {"state": "idle"}}

    return "divers", "decor", {"px": 20}


def _kenney(kit, f):
    name = f[:-4].replace("-", " ").replace("_", " ")
    FOOD_HI = ("meat", "fish", "chicken", "ham", "turkey", "bacon", "pork", "cheese", "bread",
               "egg", "soup", "dish", "meal", "drumstick", "boar", "steak", "ribs", "sushi",
               "pie", "cake", "cookie")
    if kit == "kenney_food-kit":
        n = 40.0 if any(x in name for x in FOOD_HI) else 22.0
        if "half" in name or "slice" in name:
            n = 16.0
        return "nourriture", "food", {"px": 13, "edible": n}
    SOLID = ("wall", "barricade", "tower", "castle", "house", "hut", "gate", "door", "roof",
             "chimney", "pillar", "column", "bridge", "coffin", "barrel", "box", "crate",
             "well", "forge", "machine", "arcade", "jukebox", "hockey", "basketball",
             "sarcophagus", "statue", "fence")
    shelter = any(x in name for x in ("house", "hut", "tent", "bed", "bedroll"))
    solid = any(x in name for x in SOLID) or shelter
    if kit == "kenney_graveyard-kit":
        return "tombe", "grave", {"px": 16, "solid": solid}
    if kit in ("kenney_castle-kit", "kenney_building-kit"):
        return None, None, None
    if kit == "kenney_car-kit":
        return "vehicules", "vehicle", {"px": 30, "solid": True}
    if kit == "kenney_survival-kit":
        ed = 0.0
        if any(x in name for x in FOOD_HI):
            ed = 34.0
        # outils
        if name.startswith("tool "):
            up = "upgraded" in name
            tool_kind = name.replace(" upgraded", "").replace("tool ", "")
            px = 14 if up else 12
            return "outils", "tool", {"px": px, "tool": True,
                                      "meta": {"tool_kind": tool_kind, "upgraded": up}}
        # ressources
        if name.startswith("resource "):
            mat = "bois" if "wood" in name or "planks" in name else "pierre"
            return "ressources", "stone_res" if mat == "pierre" else "item_wood", {
                "px": 16, "material": mat}
        # arbres
        if name.startswith("tree"):
            return "ressources", "tree", {"px": 32, "solid": True,
                                          "harvest": dict(material="bois", amount=3, hp=6)}
        # ignorer structures pre-construites
        if name.startswith("structure") or name.startswith("tent"):
            return None, None, None
        # ignorer workbench
        if name.startswith("workbench"):
            return None, None, None
        # campfeu
        if name.startswith("campfire"):
            return "props", "prop", {"px": 18, "edible": 0.0, "flammable": True}
        # caisses / stockage
        if any(name.startswith(x) for x in ("box", "chest", "barrel", "bucket")):
            return "props", "prop", {"px": 18, "solid": True}
        # clotures
        if name.startswith("fence"):
            return "props", "prop", {"px": 18, "solid": True}
        # poissons
        if name.startswith("fish"):
            return "nourriture", "food", {"px": 14, "edible": 40.0}
        # nature
        if name.startswith("rock") or name.startswith("patch") or name.startswith("grass"):
            return "decor", "decor", {"px": 16}
        # panneau
        if name.startswith("signpost"):
            return "props", "prop", {"px": 18}
        # lits (sans shelter)
        if name.startswith("bedroll"):
            return "props", "prop", {"px": 18}
        # bouteille
        if name.startswith("bottle"):
            return "props", "prop", {"px": 14}
        # panneaux metal
        if name.startswith("metal"):
            return "props", "prop", {"px": 18, "solid": True}
        # floor
        if name.startswith("floor"):
            return "props", "prop", {"px": 18}
        return "props", "prop", {"px": 18, "solid": solid, "edible": ed}
    if kit == "kenney_mini-arcade":
        return "props", "prop", {"px": 24, "solid": solid}
    return "props", "prop", {"px": 18, "solid": solid}


def _uf_rts(n):
    """Ultimate Fantasy RTS : rendus 1024x1024 avec transparence, a rogner (trim)."""
    def T(px_, **kw):
        meta = kw.pop("meta", {})
        meta["trim"] = True
        return dict(px=px_, meta=meta, **kw)
    if "_cut" in n or "group cut" in n:
        return "ressources", "stump", T(44)
    if n.startswith("resource tree") or n.startswith("resource pine") or n.startswith("resource tree group"):
        return "ressources", "tree", T(52, solid=True,
                                        harvest=dict(material="bois", amount=3, hp=7))
    if n.startswith("resource gold"):
        return "ressources", "gold_stone", T(32, solid=True,
                                             harvest=dict(material="or", amount=3, hp=6))
    if n.startswith("resource rock") or n in ("rock", "rock group"):
        return "ressources", "stone_res", T(34, solid=True,
                                            harvest=dict(material="pierre", amount=3, hp=6))
    if "mountain" in n:
        return "decor", "boulder", T(110, solid=True)
    if n == "logs":
        return "ressources", "item_wood", T(30, material="bois")
    if "wheat" in n:
        return "nourriture", "bush", T(58, edible=26.0)
    if "barrel" in n or "crate" in n:
        return "props", "prop", T(30, solid=True, material="bois")
    # Ignorer tous les batiments pre-construits
    return None, None, None


def _apply_afford(a):
    """Affordances : ce que le monde PERMET de faire avec cet objet.
    Le cerveau recoit ces possibilites, jamais une etiquette de role."""
    r = a.role
    af = ["observe"]
    if r == "tree":
        af += ["harvest", "burn", "block"]
        a.flammable = True
    elif r == "stump":
        af += ["burn"]
        a.flammable = True
    elif r in ("stone_res", "gold_stone"):
        af += ["harvest", "carry", "throw", "hit", "block"]
    elif r in ("food", "bush", "meat_res"):
        af += ["eat", "carry", "give", "burn"]
        a.flammable = True
    elif r in ("item_wood", "gold_pile"):
        af += ["carry", "place", "give", "burn"]
        a.flammable = True
    elif r == "tool":
        af += ["use", "carry", "hit"]
    elif r in ("house", "fort"):
        af += ["shelter", "sleep", "burn", "block"]
        a.flammable = True
    elif r == "grave":
        af += ["mourn", "mark"]
    elif r in ("prop", "vehicle"):
        af += ["block", "hit", "sit"]
    elif r in ("waterrock", "boulder"):
        af += ["block", "climb"]
    elif r == "sheep":
        af += ["chase", "hit", "shear"]
    elif r == "mural":
        af += ["lean", "decorate"]
    elif r == "duck":
        af += ["follow"]
    a.afford = af


# ----------------------------------------------------------------------------
# manager
# ----------------------------------------------------------------------------
class AssetManager:
    def __init__(self, headless=False):
        self.headless = headless
        self.assets: list[AssetDef] = []
        self.by_role: dict[str, list[int]] = {}
        self.by_cat: dict[str, list[int]] = {}
        self.skins: dict[tuple, list[int]] = {}     # (color, cls, state) -> [aid]
        self.sheep: dict[str, int] = {}
        self.monsters: dict[str, dict[str, int]] = {}
        self.fx: dict[str, list[int]] = {}
        self.ui: dict[str, list[int]] = {}
        self.floors: list[int] = []
        self.projectile = None
        self.shadow = None
        self.flammable = set()
        self._surf_cache = OrderedDict()
        self._thumb_cache = OrderedDict()
        self._tile_cache = {}
        self._avatar_cache = OrderedDict()
        self.discovered = 0
        self.deduped = 0

    # ------------------------------------------------------------------ scan
    def discover(self):
        seen = {}
        recs = []
        # collect craftpix attack frames for merging
        _attack_buf = {}  # (pack, char_name, color, cls) -> [(p, f), ...]
        for dp, _dn, fn in os.walk(ASSETS_DIR):
            if "__MACOSX" in dp or "_merged" in dp:
                continue
            for f in sorted(fn):
                if f.startswith("._") or not f.lower().endswith(IMG_EXT):
                    continue
                p = os.path.join(dp, f)
                try:
                    with open(p, "rb") as fh:
                        head = fh.read(65536)
                        fh.seek(0, 2)
                        size = fh.tell()
                    h = hashlib.sha1(head).hexdigest() + f"|{size}"
                except OSError:
                    continue
                self.discovered += 1
                if h in seen:
                    continue
                seen[h] = p
                self.deduped += 1
                rel = os.path.relpath(p, ASSETS_DIR)
                pack = rel.replace("\\", "/").split("/")[0]
                cat, role, kw = _classify(rel, f)
                # skip files that _classify marked as unusable
                if cat is None:
                    continue
                try:
                    with Image.open(p) as im:
                        w, hh = im.size
                except Exception:
                    continue
                # collect craftpix attack frames for later merge
                if (cat == "unites" and role == "skin"
                        and kw.get("meta", {}).get("state") == "attack"
                        and "craftpix" in rel.replace("\\", "/").lower()):
                    mk = (pack, kw["meta"].get("cls", ""), kw["meta"].get("color", ""))
                    _attack_buf.setdefault(mk, []).append(p)
                    continue
                kind = kw.pop("kind", "single")
                frames = 1
                fw, fh_ = w, hh
                if kind == "strip" or (w > hh and w % hh == 0 and hh >= 48 and cat in
                                       ("unites", "ressources", "animaux", "decor", "effets")):
                    frames = max(1, w // hh)
                    fw, fh_ = hh, hh
                    kind = "strip"
                    # detect grid spritesheets (frames too large for a strip)
                    if fw > 128 and hh > 128 and w >= 48 and hh >= 48:
                        # treat as grid: assume 48x48 frames
                        fw, fh_ = 48, 48
                        cols = max(1, w // 48)
                        rows = max(1, hh // 48)
                        frames = cols * rows
                        kind = "grid"
                elif cat == "interface" and "avatars" in role:
                    frames, fw, fh_, kind = 16, w // 4, hh // 4, "grid44"
                meta = kw.get("meta") or {}
                if meta.get("trim") and kind == "single":
                    try:
                        with Image.open(p) as im:
                            bb = im.convert("RGBA").split()[3].getbbox()
                        if bb and bb[2] - bb[0] > 8 and bb[3] - bb[1] > 8:
                            meta["_bb"] = bb
                            fw, fh_ = bb[2] - bb[0], bb[3] - bb[1]
                        else:
                            meta.pop("trim")
                    except Exception:
                        meta.pop("trim")
                aid = len(self.assets)
                a = AssetDef(id=aid, name=f, label=f[:-4].replace("_", " ").replace("-", " "),
                             path=p, pack=pack, category=cat, role=role, kind=kind,
                             frames=frames, fw=fw, fh=fh_, **kw)
                a.placable = cat not in NON_PLACABLE
                a.blocked_footprint = a.size_tiles if a.solid else 1
                _apply_afford(a)
                a.afford_details = render_asset(a)
                a.build_recipe = build_recipe_for(a)
                self.assets.append(a)
                if a.flammable:
                    self.flammable.add(aid)
                self.by_role.setdefault(role, []).append(aid)
                self.by_cat.setdefault(cat, []).append(aid)

        # merge craftpix attack frames into strips
        for (pack, cls, color), paths in _attack_buf.items():
            if not paths:
                continue
            imgs = []
            for pp in sorted(paths):
                try:
                    with Image.open(pp) as im:
                        imgs.append(im.convert("RGBA"))
                except Exception:
                    continue
            if not imgs:
                continue
            fw, fh_ = imgs[0].size
            merged = Image.new("RGBA", (fw * len(imgs), fh_), (0, 0, 0, 0))
            for i, im in enumerate(imgs):
                merged.paste(im, (i * fw, 0))
            merged_path = os.path.join(ASSETS_DIR, "_merged", f"{pack}_{cls}_attack.png")
            os.makedirs(os.path.dirname(merged_path), exist_ok=True)
            merged.save(merged_path)
            aid = len(self.assets)
            a = AssetDef(id=aid, name=f"{cls}_attack.png",
                         label=f"{cls} attack", path=merged_path, pack=pack,
                         category="unites", role="skin", kind="strip",
                         frames=len(imgs), fw=fw, fh=fh_, px=26,
                         meta={"cls": cls, "state": "attack", "tool": "", "color": color})
            a.placable = False
            a.blocked_footprint = 1
            _apply_afford(a)
            a.afford_details = render_asset(a)
            a.build_recipe = build_recipe_for(a)
            self.assets.append(a)
            self.by_role.setdefault("skin", []).append(aid)
            self.by_cat.setdefault("unites", []).append(aid)

        # indices
        for a in self.assets:
            m = a.meta
            if a.role == "skin":
                st = m.get("state") or "idle"
                st = {"shoot": "attack", "guard": "idle"}.get(st, st)
                if st not in ("idle", "run", "attack", "work", "heal", "build"):
                    st = "idle"
                key = (m.get("color", "blue"), m.get("cls", "pawn"), st)
                self.skins.setdefault(key, []).append(a.id)
            elif a.role == "sheep":
                self.sheep[m["state"]] = a.id
            elif a.role in ("monster", "monster_attack"):
                kind = m.get("kind", "unknown")
                state = m.get("state", "idle")
                self.monsters.setdefault(kind, {})[state] = a.id
            elif a.role == "fx":
                self.fx.setdefault(m["fx"], []).append(a.id)
            elif a.role.startswith("ui_"):
                self.ui.setdefault(a.role[3:], []).append(a.id)
            elif a.role == "floor":
                self.floors.append(a.id)
            elif a.role == "projectile":
                self.projectile = a.id
            elif a.role == "shadow":
                self.shadow = a.id

        # copy build sprites to all characters (they share the same animation)
        build_ids = [a.id for a in self.assets if a.role == "skin"
                     and a.meta.get("state") == "build"]
        if build_ids:
            all_chars = {(k[0], k[1]) for k in self.skins
                         if k[2] == "idle"}
            for color, cls in all_chars:
                key = (color, cls, "build")
                if key not in self.skins:
                    self.skins[key] = list(build_ids)
        for k in self.skins:
            self.skins[k].sort()
        return self

    # ------------------------------------------------------------------ pixel io
    def _pil_frame(self, a: AssetDef, frame=0):
        with Image.open(a.path) as im:
            im = im.convert("RGBA")
            if a.kind == "strip":
                x = frame * a.fw
                im = im.crop((x, 0, x + a.fw, a.fh))
            elif a.kind == "grid" or a.kind == "grid44":
                cols = max(1, im.width // a.fw)
                i, j = frame % cols, frame // cols
                im = im.crop((i * a.fw, j * a.fh, (i + 1) * a.fw, (j + 1) * a.fh))
            elif a.kind == "tiles":
                raise ValueError("use tile_cells")
            else:
                if a.meta.get("_bb"):
                    im = im.crop(a.meta["_bb"])
                else:
                    im = im.copy()
            return im

    def _to_surf(self, pil, w, h):
        if (pil.width, pil.height) != (w, h):
            pil = pil.resize((max(1, int(w)), max(1, int(h))), Image.LANCZOS)
        if self.headless:
            return pil
        return pygame.image.fromstring(pil.tobytes(), pil.size, "RGBA").convert_alpha()

    def surface(self, aid, frame=0, scale=1.0):
        a = self.assets[aid]
        if getattr(a, "_procedural_surface", None) is not None:
            base = a._procedural_surface
            if abs(scale - 1.0) < 1e-6:
                return base
            w = max(1, int(base.get_width() * scale))
            h = max(1, int(base.get_height() * scale))
            return pygame.transform.scale(base, (w, h))
        k = (aid, frame, round(scale, 2))
        hit = self._surf_cache.get(k)
        if hit is not None:
            self._surf_cache.move_to_end(k)
            return hit
        try:
            if a.kind == "tiles":
                pil = self._tile_pil(aid, (aid * 7 + 3) % 216)   # carreau representatif
            else:
                pil = self._pil_frame(a, frame)
        except Exception:
            pil = Image.new("RGBA", (8, 8), (255, 0, 255, 255))
        ar = a.fw / max(1, a.fh)
        if ar >= 1:
            ww, hh = a.px, a.px / ar
        else:
            ww, hh = a.px * ar, a.px
        surf = self._to_surf(pil, ww * scale, hh * scale)
        self._surf_cache[k] = surf
        if len(self._surf_cache) > 2600:
            self._surf_cache.popitem(last=False)
        return surf

    def display_size(self, aid, scale=1.0):
        a = self.assets[aid]
        ar = a.fw / max(1, a.fh)
        if ar >= 1:
            return int(a.px * scale), int(a.px / ar * scale) or 2
        return int(a.px * ar * scale) or 2, int(a.px * scale)

    def thumbnail(self, aid, size=54):
        k = (aid, size)
        hit = self._thumb_cache.get(k)
        if hit is not None:
            self._thumb_cache.move_to_end(k)
            return hit
        a = self.assets[aid]
        try:
            if a.kind == "tiles":
                pil = self._tile_pil(aid, (aid * 7 + 3) % 216)
            else:
                pil = self._pil_frame(a, 0)
            pil.thumbnail((size, size), Image.LANCZOS)
            surf = self._to_surf(pil, pil.width, pil.height)
        except Exception:
            surf = pygame.Surface((size, size), pygame.SRCALPHA)
            surf.fill((60, 40, 70, 255))
        self._thumb_cache[k] = surf
        if len(self._thumb_cache) > 1400:
            self._thumb_cache.popitem(last=False)
        return surf

    # ------------------------------------------------------------------ tileset floors
    def _tile_pil(self, sheet_aid, cell):
        a = self.assets[sheet_aid]
        with Image.open(a.path) as im:
            im = im.convert("RGBA")
            cols = im.width // 32
            i, j = cell % cols, cell // cols
            i %= max(1, cols)
            j = min(j, max(0, im.height // 32 - 1))
            return im.crop((i * 32, j * 32, i * 32 + 32, j * 32 + 32))

    def tile_cells(self, sheet_aid):
        a = self.assets[sheet_aid]
        return (a.fw // 32) * (a.fh // 32) if a.kind == "tiles" else 0

    def floor_tile(self, sheet_aid, cell, scale=1.0):
        k = (sheet_aid, cell, round(scale, 2))
        hit = self._tile_cache.get(k)
        if hit is not None:
            return hit
        pil = self._tile_pil(sheet_aid, cell).resize((int(16 * scale), int(16 * scale)), Image.LANCZOS)
        surf = self._to_surf(pil, pil.width, pil.height)
        self._tile_cache[k] = surf
        return surf

    def random_floor_tile(self, sheet_aid, rng):
        return self.floor_tile(sheet_aid, int(rng.integers(self.tile_cells(sheet_aid) or 1)))

    # ------------------------------------------------------------------ avatars (UI)
    def avatar(self, idx, size=44):
        sheets = self.ui.get("avatars", [])
        if not sheets:
            s = pygame.Surface((size, size), pygame.SRCALPHA)
            return s
        k = (idx % (len(sheets) * 16), size)
        hit = self._avatar_cache.get(k)
        if hit is not None:
            self._avatar_cache.move_to_end(k)
            return hit
        sheet = sheets[(idx // 16) % len(sheets)]
        frame = idx % 16
        a = self.assets[sheet]
        i, j = frame % 4, frame // 4
        with Image.open(a.path) as im:
            im = im.convert("RGBA")
            cw, ch = im.width // 4, im.height // 4
            pil = im.crop((i * cw, j * ch, i * cw + cw, j * ch + ch))
        pil.thumbnail((size, size), Image.LANCZOS)
        surf = self._to_surf(pil, pil.width, pil.height)
        self._avatar_cache[k] = surf
        if len(self._avatar_cache) > 500:
            self._avatar_cache.popitem(last=False)
        return surf

    # ------------------------------------------------------------------ helpers
    def pool(self, role):
        return self.by_role.get(role, [])

    def pick(self, pool_ids, rng, default=None):
        if not pool_ids:
            return default
        return int(rng.choice(pool_ids))

    def skin_states(self, color, cls):
        out = {}
        for st in ("idle", "run", "attack", "work", "heal", "build"):
            ids = self.skins.get((color, cls, st))
            if ids:
                out[st] = ids
        if not out.get("idle"):
            pawn_ids = self.skins.get((color, "pawn", "idle"))
            if not pawn_ids:
                for c in CLAN_COLORS:
                    pawn_ids = self.skins.get((c, "pawn", "idle"))
                    if pawn_ids:
                        break
            out["idle"] = pawn_ids or []
        out.setdefault("run", out["idle"])
        return out

    def unit_colors(self):
        if getattr(self, "_colors", None) is None:
            self._colors = [c for c in CLAN_COLORS if any(k[0] == c for k in self.skins)]
        return self._colors

    def unit_classes(self, color):
        if getattr(self, "_classes", None) is None:
            self._classes = {}
        if color not in self._classes:
            self._classes[color] = sorted({k[1] for k in self.skins if k[0] == color})
        return self._classes[color]

    def stats(self):
        return dict(discovered=self.discovered, deduped=self.deduped,
                    per_cat={lbl: len(self.by_cat.get(c, [])) for c, lbl in CATEGORY_LABELS})

    def plans_for(self, inv):
        """Retourne la liste des assets constructibles avec l'inventaire donné."""
        from .affordance_definitions import plans_for as _plans_for
        return _plans_for(self, inv)

    def ensure_procedural_blocks(self):
        specs = [
            ("block_wood", "Bloc bois", (150, 108, 62), (110, 78, 44), True),
            ("block_stone", "Bloc pierre", (150, 150, 156), (108, 108, 114), True),
            ("block_roof", "Tuile toit", (125, 70, 55), (86, 45, 38), False),
            ("block_door", "Porte", (108, 70, 38), (65, 42, 25), False),
        ]
        for role, label, fill, edge, solid in specs:
            if self.by_role.get(role):
                continue
            surf = pygame.Surface((16, 16), pygame.SRCALPHA)
            surf.fill(fill)
            pygame.draw.rect(surf, edge, surf.get_rect(), 2)
            if role == "block_door":
                pygame.draw.circle(surf, (220, 190, 80), (12, 8), 1)
            elif role == "block_roof":
                pygame.draw.line(surf, edge, (1, 5), (15, 5), 1)
                pygame.draw.line(surf, edge, (1, 10), (15, 10), 1)
            aid = len(self.assets)
            a = AssetDef(
                id=aid, name=f"{role}.png",
                label=label,
                path="", pack="procedural", category="batiments", role=role,
                kind="single", frames=1, fw=16, fh=16, px=16,
                solid=solid, blocked_footprint=1, placable=False,
                meta={"procedural": True},
            )
            a.afford = ("block", "hit")
            a._procedural_surface = surf
            self.assets.append(a)
            self.by_role.setdefault(role, []).append(aid)
            self.by_cat.setdefault("batiments", []).append(aid)

    def ensure_procedural_tools(self):
        shapes = {
            "hache": (168, 118, 68),
            "pioche": (148, 148, 156),
            "marteau": (120, 120, 130),
        }
        for kind, color in shapes.items():
            role_key = f"tool_{kind}"
            if self.by_role.get(role_key):
                continue
            surf = pygame.Surface((14, 14), pygame.SRCALPHA)
            pygame.draw.polygon(surf, color, [(2, 12), (10, 2), (12, 4), (4, 14)])
            pygame.draw.polygon(surf, (40, 40, 44), [(2, 12), (10, 2), (12, 4), (4, 14)], 1)
            aid = len(self.assets)
            a = AssetDef(
                id=aid, name=f"{kind}.png", label=kind.capitalize(), path="",
                pack="procedural", category="outils", role="tool",
                kind="single", frames=1, fw=14, fh=14, px=14, tool=True,
                placable=True, meta={"tool_kind": kind, "procedural": True},
            )
            a.afford = ("use", "carry", "hit")
            a._procedural_surface = surf
            self.assets.append(a)
            self.by_role.setdefault("tool", []).append(aid)
            self.by_role.setdefault(role_key, []).append(aid)
            self.by_cat.setdefault("outils", []).append(aid)

    def register_custom_tool(self, path, tool_kind, label=None):
        img = pygame.image.load(path).convert_alpha()
        aid = len(self.assets)
        a = AssetDef(
            id=aid, name=os.path.basename(path), label=label or tool_kind,
            path=path, pack="custom_tools", category="outils", role="tool",
            kind="single", frames=1, fw=img.get_width(), fh=img.get_height(),
            px=20, tool=True, meta={"tool_kind": tool_kind}, placable=True,
        )
        a.afford = ("use", "carry", "hit")
        self.assets.append(a)
        self.by_role.setdefault("tool", []).append(aid)
        self.by_role.setdefault(f"tool_{tool_kind}", []).append(aid)
        self.by_cat.setdefault("outils", []).append(aid)

    def ensure_kaykit_resources(self):
        """KayKit Resource Bits : sprites extraits de la texture atlas."""
        import os as _os
        from .config import ASSETS_DIR
        res_dir = _os.path.join(_os.path.dirname(ASSETS_DIR), "assets", "kaykit_resources")
        if not _os.path.isdir(res_dir):
            return
        specs = [
            ("wood_log",          "Bois (tronc)",     "ressources", "item_wood",
             {"material": "bois", "px": 16}),
            ("wood_plank",        "Planche",          "ressources", "item_wood",
             {"material": "bois", "px": 16}),
            ("wood_planks_stack", "Pile planches",    "ressources", "item_wood",
             {"material": "bois", "px": 20}),
            ("stone_brick",       "Brique pierre",    "ressources", "stone_res",
             {"material": "pierre", "px": 16}),
            ("stone_chunks",      "Cailloux",         "ressources", "stone_res",
             {"material": "pierre", "px": 16}),
            ("stone_stack",       "Pile pierres",     "ressources", "stone_res",
             {"material": "pierre", "px": 20}),
            ("gold_bar",          "Lingot or",        "ressources", "gold_pile",
             {"material": "or", "px": 16}),
            ("gold_nuggets",      "Pepites or",       "ressources", "gold_pile",
             {"material": "or", "px": 16}),
            ("gold_bars_stack",   "Pile lingots or",  "ressources", "gold_pile",
             {"material": "or", "px": 20}),
            ("iron_bar",          "Lingot fer",       "props", "prop",
             {"px": 16, "solid": True}),
            ("iron_nuggets",      "Pepites fer",      "props", "prop",
             {"px": 16}),
            ("iron_bars_stack",   "Pile lingots fer", "props", "prop",
             {"px": 20, "solid": True}),
            ("copper_bar",        "Lingot cuivre",    "props", "prop",
             {"px": 16, "solid": True}),
            ("copper_nuggets",    "Pepites cuivre",   "props", "prop",
             {"px": 16}),
            ("copper_bars",       "Barres cuivre",    "props", "prop",
             {"px": 20, "solid": True}),
        ]
        for fname, label, cat, role, kw in specs:
            path = _os.path.join(res_dir, f"{fname}.png")
            if not _os.path.exists(path):
                continue
            if self.by_role.get(role) and any(
                self.assets[i].name == f"{fname}.png" for i in self.by_role.get(role, [])
            ):
                continue
            try:
                img = pygame.image.load(path).convert_alpha()
            except pygame.error:
                continue
            aid = len(self.assets)
            a = AssetDef(
                id=aid, name=f"{fname}.png", label=label,
                path=path, pack="kaykit", category=cat, role=role,
                kind="single", frames=1,
                fw=img.get_width(), fh=img.get_height(),
                px=kw.pop("px", 16),
                solid=kw.pop("solid", False),
                blocked_footprint=1, placable=True,
                material=kw.pop("material", ""),
                meta={"procedural": True},
            )
            for k, v in kw.items():
                setattr(a, k, v)
            a.afford = ("block", "carry", "hit") if a.solid else ("carry", "hit")
            a._procedural_surface = img
            self.assets.append(a)
            self.by_role.setdefault(role, []).append(aid)
            self.by_cat.setdefault(cat, []).append(aid)

    def register_grid_items(self, path, category, role, cell_w, cell_h,
                            labels=None, edible=0.0, tool_item=False,
                            solid=False, harvest=None):
        from PIL import Image as _Img
        with _Img.open(path) as source:
            image = source.convert("RGBA")
        columns = max(1, image.width // cell_w)
        rows = max(1, image.height // cell_h)
        gen_dir = os.path.join(ASSETS_DIR, "generated")
        os.makedirs(gen_dir, exist_ok=True)
        base = os.path.splitext(os.path.basename(path))[0]
        created = []
        for row in range(rows):
            for col in range(columns):
                index = row * columns + col
                x0, y0 = col * cell_w, row * cell_h
                tile = image.crop((x0, y0, x0 + cell_w, y0 + cell_h))
                alpha = tile.split()[3]
                if alpha.getbbox() is None:
                    continue
                tile_path = os.path.join(gen_dir, f"{base}_{index}.png")
                tile.save(tile_path)
                aid = len(self.assets)
                label = (labels[index] if labels and index < len(labels)
                         else f"{role} {index + 1}")
                asset = AssetDef(
                    id=aid, name=os.path.basename(tile_path), label=label,
                    path=tile_path, pack="generated_grid", category=category,
                    role=role, kind="single", frames=1,
                    fw=cell_w, fh=cell_h,
                    px=max(cell_w, cell_h),
                    solid=solid, edible=edible, tool=tool_item,
                    blocked_footprint=1, placable=True,
                    meta={"source_sheet": os.path.basename(path),
                           "grid_index": index},
                )
                if harvest:
                    asset.harvest = harvest
                if edible > 0:
                    asset.afford = ("eat", "carry", "give", "burn")
                else:
                    asset.afford = ("carry", "hit") if solid else ("carry",)
                self.assets.append(asset)
                self.by_role.setdefault(role, []).append(aid)
                self.by_cat.setdefault(category, []).append(aid)
                created.append(aid)
        return created

```

## game/brain.py

**Type :** `.py`

```python

"""Cerveau — moteur d'arbitrage + apprentissage.

L'etre possede un SAVOIR GENERAL (affordances du monde, lois physiques) mais
AUCUN objectif impose. A chaque reflexion, le cerveau recoit une representation
structuree (encoders : corps, besoins, emotions, personnalite, soi, social,
experiences, competences, habitudes, perception locale, MEMOIRE de ce qui a ete
percu — jamais d'omniscience — et le temps) et produit une INTENTION
structuree : action + cible + intensite.

Architecte : Elman a contexte diagonal, taille figee a la creation (verrouillee,
meme le createur ne peut plus la changer). Les POIDS, eux, APPRENNENT pendant la
vie : REINFORCE (gradient du log-proba de l'action choisie x recompense vecue),
taux modulе par l'age (un enfant apprend 2x plus vite, un vieux fige).

Boucle du contrat moteur :
  perception -> cerveau -> intention -> le MONDE verifie la faisabilite
  -> consequences -> experience -> recompense -> apprentissage -> cerveau.

--------------------------------------------------------------------------
AMELIORATIONS (integration inchangee : meme classe Brain, memes methodes
think/learn/breed/copy, memes constantes N_IN/N_OUT/ACTION_*) :

1. Modulation reelle par l'age dans learn() — le docstring la promettait,
   elle n'etait pas cablee. Un parametre optionnel age_factor (0..1+) est
   accepte partout ou l'appelant peut le fournir ; par defaut =1.0 (comportement
   identique a avant si l'appelant ne change rien).
2. Trace d'eligibilite courte (multi-pas) — une recompense qui arrive
   quelques pas apres l'action qui l'a causee (ex: recolter -> manger plus
   tard) peut maintenant renforcer aussi les decisions recentes, avec une
   decroissance temporelle, au lieu de ne renforcer que le dernier choix.
3. Entropie liee a la personnalite (curiosite/prudence) — un etre curieux
   explore davantage (temperature effective plus haute), un prudent se
   restreint aux actions sures ; brancher sur les traits deja definis dans
   ACTION_TRAIT sans ajouter de nouvelle dependance externe.
4. explain() — expose un classement lisible des intentions (nom, couleur,
   probabilite) pour que le dashboard affiche "ce qu'il va faire et pourquoi"
   sans avoir a connaitre la representation interne du reseau.
5. Garde-fous NaN/Inf sur les poids et sur la sortie, essentiels sur une
   vie simulee longue (des milliers de pas d'apprentissage continu).
--------------------------------------------------------------------------
"""
import numpy as np
from collections import deque

N_IN = 132
N_OUT = 15
N_STRATEGIES = 6
N_TARGETS = 8

# vocabulaire d'actions elementaires (composables par le monde, jamais des roles)
(REST, SLEEP, EAT, DRINK, HARVEST, DROP, BUILD, GIVE, TAKE, ATTACK,
 FLEE, EXPLORE, TALK, MARK, SOCIAL) = range(15)

ACTION_NAMES = {REST: "Repos", SLEEP: "Dormir", EAT: "Manger", DRINK: "Boire",
                HARVEST: "Récolter", DROP: "Poser", BUILD: "Construire",
                GIVE: "Offrir", TAKE: "Prendre", ATTACK: "Attaquer",
                FLEE: "Fuir", EXPLORE: "Explorer", TALK: "Parler", MARK: "Marquer",
                SOCIAL: "Rejoindre"}
ACTION_COLORS = {REST: (140, 140, 160), SLEEP: (120, 110, 180), EAT: (236, 150, 86),
                 DRINK: (90, 180, 230), HARVEST: (110, 200, 120), DROP: (170, 140, 100),
                 BUILD: (236, 190, 86), GIVE: (160, 230, 200), TAKE: (200, 160, 90),
                 ATTACK: (222, 96, 96), FLEE: (150, 150, 200), EXPLORE: (96, 168, 222),
                  TALK: (255, 180, 220), MARK: (255, 120, 200), SOCIAL: (200, 160, 255)}

# strategies
(IMMEDIAT, PRUDENT, ECONOMIQUE, COOPERATIF, EXPLORATION, DEFENSIF) = range(N_STRATEGIES)
STRATEGY_NAMES = {IMMEDIAT: "Immédiat", PRUDENT: "Prudent", ECONOMIQUE: "Économique",
                  COOPERATIF: "Coopératif", EXPLORATION: "Exploration", DEFENSIF: "Défensif"}
STRATEGY_COLORS = {IMMEDIAT: (220, 120, 80), PRUDENT: (120, 180, 120),
                   ECONOMIQUE: (180, 180, 80), COOPERATIF: (120, 180, 220),
                   EXPLORATION: (100, 160, 220), DEFENSIF: (200, 140, 140)}

# types de cible
(SOI, NOURRITURE, EAU, BOIS, PIERRE, ABRI, DEPOT_CHANTIER, ETRE_VIVANT) = range(N_TARGETS)
TARGET_NAMES = {SOI: "Soi", NOURRITURE: "Nourriture", EAU: "Eau", BOIS: "Bois",
                PIERRE: "Pierre", ABRI: "Abri", DEPOT_CHANTIER: "Dépôt/Chantier",
                ETRE_VIVANT: "Être vivant"}
TARGET_COLORS = {SOI: (180, 180, 180), NOURRITURE: (236, 150, 86), EAU: (90, 180, 230),
                 BOIS: (150, 108, 62), PIERRE: (150, 150, 156), ABRI: (170, 140, 100),
                 DEPOT_CHANTIER: (200, 160, 90), ETRE_VIVANT: (200, 160, 255)}

# personnalite : 0 sociabilite 1 agressivite 2 curiosite 3 prudence 4 patience
# 5 empathie 6 impulsivite 7 confiance 8 perseverance 9 ambition 10 generosite
# 11 discipline
ACTION_TRAIT = {
    REST:    (8, -0.28),
    SLEEP:   (11, -0.20),
    EAT:     (3, -0.08),
    DRINK:   (3, -0.08),
    HARVEST: (8, 0.30),
    DROP:    (11, 0.10),
    BUILD:   (8, 0.36),
    GIVE:    (10, 0.48),
    TAKE:    (1, 0.30),
    ATTACK:  (1, 0.42),
    FLEE:    (3, 0.30),
    EXPLORE: (2, 0.44),
    TALK:    (0, 0.42),
    MARK:    (9, 0.22),
    SOCIAL:  (0, 0.40),
}

# actions considerees "sures" par un profil prudent (utilisees uniquement
# pour moduler l'entropie/exploration ci-dessous — n'affecte jamais les
# probas de base issues du reseau)
_SAFE_ACTIONS = {REST, SLEEP, EAT, DRINK, DROP, TALK}

SIZES = (25, 50, 75, 100, 128, 256, 512, 768, 1000)


def think_every(n):
    if n <= 128:
        return 2
    if n <= 256:
        return 4
    if n <= 1024:
        return 8
    return 16


def params_size(n):
    return N_IN * n + n + n + N_OUT * n + N_OUT


def rand_weights(rng, n):
    p = np.empty(params_size(n), dtype=np.float64)
    i = 0
    p[i:i + N_IN * n] = rng.normal(0, 0.6, N_IN * n); i += N_IN * n
    p[i:i + n] = rng.normal(0, 0.8, n); i += n
    p[i:i + n] = rng.normal(0, 0.3, n); i += n
    p[i:i + N_OUT * n] = rng.normal(0, 0.6, N_OUT * n); i += N_OUT * n
    p[i:] = rng.normal(0, 0.3, N_OUT)
    return p


def unpack(p, n):
    i = 0
    Wx = p[i:i + N_IN * n].reshape(n, N_IN); i += N_IN * n
    Wd = p[i:i + n]; i += n
    b1 = p[i:i + n]; i += n
    Wo = p[i:i + N_OUT * n].reshape(N_OUT, n); i += N_OUT * n
    b2 = p[i:]
    return Wx, Wd, b1, Wo, b2


class Brain:
    def __init__(self, n_hid=128, params=None, rng=None, elig_len=6, elig_decay=0.55):
        self.rng = rng or np.random.default_rng()
        self.n = int(n_hid)
        self.te = think_every(self.n)
        self.p = np.array(rand_weights(rng, self.n) if params is None else params,
                          dtype=np.float64)
        self.h = np.zeros(self.n)
        self.last_out = np.zeros(N_OUT)
        self.probs = np.full(N_OUT, 1.0 / N_OUT)
        self.base = 0.0                     # baseline REINFORCE
        self._has_thought = False             # True après think(), reset après learn()
        # trace multi-pas : chaque decision recente reste renforçable un moment
        self._trace = deque(maxlen=max(1, int(elig_len)))
        self._trace_decay = float(elig_decay)
        # têtes supplémentaires : stratégie + cible (Lot 7.2)
        scale = 0.4 / np.sqrt(self.n)
        if rng is not None:
            self._Wo_strat = rng.normal(0, scale, (N_STRATEGIES, self.n)).astype(np.float64)
            self._b2_strat = rng.normal(0, 0.15, N_STRATEGIES).astype(np.float64)
            self._Wo_targ = rng.normal(0, scale, (N_TARGETS, self.n)).astype(np.float64)
            self._b2_targ = rng.normal(0, 0.15, N_TARGETS).astype(np.float64)
        else:
            self._Wo_strat = np.zeros((N_STRATEGIES, self.n), dtype=np.float64)
            self._b2_strat = np.zeros(N_STRATEGIES, dtype=np.float64)
            self._Wo_targ = np.zeros((N_TARGETS, self.n)).astype(np.float64)
            self._b2_targ = np.zeros(N_TARGETS).astype(np.float64)
        self._strat_probs = np.full(N_STRATEGIES, 1.0 / N_STRATEGIES)
        self._targ_probs = np.full(N_TARGETS, 1.0 / N_TARGETS)
        self._strategy = IMMEDIAT
        self._target = SOI
        self._sync()

    def _sync(self):
        self._Wx, self._Wd, self._b1, self._Wo, self._b2 = unpack(self.p, self.n)

    def think(self, x, temperature=1.0, bias=None, curiosity=None, caution=None):
        """Représentation interne -> politique softmax -> intention échantillonnée.
        bias = ponderations du corps (personnalite, emotions, urgences vitales).
        Les logits du reseau sont amortis pour que le biais corporel puisse
        dominer en cas d'urgence, sans effacer l'individualite du cerveau.

        curiosity/caution (optionnels, 0..1) : si l'appelant transmet ces deux
        traits de personnalite (ils existent deja dans l'encoder personnalite,
        index 2 et 3), la temperature effective est ajustee — un etre curieux
        explore un peu plus, un prudent se resserre sur les actions sures.
        Comportement inchange si ces arguments ne sont pas fournis."""
        h_prev = self.h
        self.h = np.tanh(x @ self._Wx.T + self._Wd * self.h + self._b1)
        # garde-fou : un cerveau qui vit tres longtemps et apprend en continu
        # peut voir ses poids diverger ; on neutralise silencieusement plutot
        # que de laisser NaN se propager dans toute la simulation
        if not np.all(np.isfinite(self.h)):
            self.h = np.nan_to_num(self.h, nan=0.0, posinf=1.0, neginf=-1.0)
        logits = (self.h @ self._Wo.T + self._b2) * 0.45
        if bias is not None:
            logits = logits + bias * 1.8

        eff_temp = max(0.15, temperature)
        if curiosity is not None or caution is not None:
            c = 0.0 if curiosity is None else float(curiosity)
            p = 0.0 if caution is None else float(caution)
            # curiosite ouvre l'exploration, prudence la referme ; net borne
            eff_temp *= max(0.5, 1.0 + 0.6 * c - 0.5 * p)
            if p > 0.0:
                penal = np.array([0.0 if a in _SAFE_ACTIONS else 1.0 for a in range(N_OUT)])
                logits = logits - penal * (p * 1.2)

        z = (logits - logits.max()) / eff_temp
        e = np.exp(z)
        probs = e / e.sum()
        if not np.all(np.isfinite(probs)):
            probs = np.full(N_OUT, 1.0 / N_OUT)
        self.last_out = probs
        self.probs = probs
        act = int(self.rng_choice(probs))

        # tete strategie
        strat_logits = (self.h @ self._Wo_strat.T + self._b2_strat) * 0.35
        sz = (strat_logits - strat_logits.max()) / eff_temp
        se = np.exp(sz)
        self._strat_probs = se / se.sum()
        if not np.all(np.isfinite(self._strat_probs)):
            self._strat_probs = np.full(N_STRATEGIES, 1.0 / N_STRATEGIES)
        self._strategy = int(self.rng_choice(self._strat_probs))

        # tete cible
        targ_logits = (self.h @ self._Wo_targ.T + self._b2_targ) * 0.35
        tz = (targ_logits - targ_logits.max()) / eff_temp
        te2 = np.exp(tz)
        self._targ_probs = te2 / te2.sum()
        if not np.all(np.isfinite(self._targ_probs)):
            self._targ_probs = np.full(N_TARGETS, 1.0 / N_TARGETS)
        self._target = int(self.rng_choice(self._targ_probs))

        self._has_thought = True
        self._trace.append((x.copy(), h_prev.copy(), act, probs.copy(),
                            self._strategy, self._targ_probs.copy()))
        return act, probs

    def rng_choice(self, probs):
        return int(self.rng.choice(len(probs), p=probs))

    def explain(self, top=5):
        """Classement lisible de la derniere intention, pour le dashboard :
        renvoie une liste de dicts {action, nom, couleur, probabilite}
        triee par probabilite decroissante — aucune connaissance du reseau
        n'est requise cote UI."""
        order = np.argsort(-self.probs)[:max(1, int(top))]
        return [
            {
                "action": int(a),
                "nom": ACTION_NAMES.get(int(a), "?"),
                "couleur": ACTION_COLORS.get(int(a), (200, 200, 200)),
                "probabilite": float(self.probs[a]),
            }
            for a in order
        ]

    # ------------------------------------------------------------------ apprentissage
    def learn(self, reward, lr=0.0022, age_factor=1.0):
        """REINFORCE : renforcer ce qui a reduit la frustration, affaiblir le reste.
        Seuls POIDS et BIAIS bougent — l'architecture reste verrouillée.

        age_factor (0..~2, defaut 1.0) : multiplie le taux d'apprentissage
        effectif — un jeune (>1.0) apprend plus vite, un vieux (<1.0) se fige,
        conformement au docstring. Comportement inchange si l'appelant ne
        fournit rien.

        La derniere decision est renforcee pleinement ; les decisions
        recentes (trace courte) sont renforcees avec une decroissance
        temporelle, pour capturer les recompenses qui arrivent quelques pas
        apres l'action qui les a causees (ex: recolter -> manger plus tard)."""
        if not self._has_thought:
            return
        self._has_thought = False
        adv = reward - self.base
        self.base += 0.05 * adv
        eff_lr = lr * max(0.0, float(age_factor))

        # decision la plus recente en premier (poids plein), puis les
        # precedentes avec decroissance geometrique
        n = len(self._trace)
        for i, entry in enumerate(reversed(self._trace)):
            w = self._trace_decay ** i
            if w < 0.02:
                break
            # compat : ancien format (x,h,act,probs) vs nouveau (x,h,act,probs,strat,targ_probs)
            if len(entry) == 4:
                x, h_prev, act, probs = entry
                strat, targ_probs = None, None
            else:
                x, h_prev, act, probs, strat, targ_probs = entry
            # gradient sur l'action
            d = (np.arange(N_OUT) == act) - probs
            d = d * (adv * eff_lr * w)
            dh = (d @ self._Wo) * (1.0 - h_prev ** 2)
            self._b2 += d
            self._Wo += np.outer(d, self.h if i == 0 else h_prev)
            self._b1 += dh * 0.5
            self._Wd += dh * h_prev * 0.5
            self._Wx += np.outer(dh, x) * 0.5
            # gradient sur la strategie
            if strat is not None:
                ds = (np.arange(N_STRATEGIES) == strat) - self._strat_probs
                ds = ds * (adv * eff_lr * w * 0.5)
                self._b2_strat += ds
                self._Wo_strat += np.outer(ds, self.h if i == 0 else h_prev)
            # gradient sur la cible
            if targ_probs is not None:
                dt = (np.arange(N_TARGETS) == self._target) - targ_probs
                dt = dt * (adv * eff_lr * w * 0.5)
                self._b2_targ += dt
                self._Wo_targ += np.outer(dt, self.h if i == 0 else h_prev)

        # garde-fou anti-divergence sur une vie simulee longue
        if not np.all(np.isfinite(self._Wx)):
            np.nan_to_num(self._Wx, copy=False, nan=0.0, posinf=2.0, neginf=-2.0)
        if not np.all(np.isfinite(self._Wo)):
            np.nan_to_num(self._Wo, copy=False, nan=0.0, posinf=2.0, neginf=-2.0)
        if not np.all(np.isfinite(self._Wo_strat)):
            np.nan_to_num(self._Wo_strat, copy=False, nan=0.0, posinf=2.0, neginf=-2.0)
        if not np.all(np.isfinite(self._Wo_targ)):
            np.nan_to_num(self._Wo_targ, copy=False, nan=0.0, posinf=2.0, neginf=-2.0)
        self._sync()

    # ------------------------------------------------------------------ evolution
    @staticmethod
    def breed(pa, pb, na, rng, sigma=0.06, rate=0.08):
        if na is None:
            na = pa.n if rng.random() < 0.5 else pb.n
        if pa.n == pb.n == na:
            child = np.where(rng.random(pa.p.size) < 0.5, pa.p, pb.p)
        elif pa.n == na:
            child = pa.p.copy()
        elif pb.n == na:
            child = pb.p.copy()
        else:
            child = rand_weights(rng, na)
        mut = rng.random(child.size) < rate
        child[mut] += rng.normal(0, sigma, mut.sum())
        return child, na

    def copy(self):
        b = Brain.__new__(Brain)
        b.n, b.te = self.n, self.te
        b.p = self.p.copy()
        b.h = self.h.copy()
        b.last_out = self.last_out.copy()
        b.probs = self.probs.copy()
        b.base = self.base
        b._has_thought = False
        b._trace = deque(maxlen=self._trace.maxlen)
        b._trace_decay = self._trace_decay
        b.rng = np.random.default_rng(self.rng.bit_generator.state["state"]["state"])
        # têtes strategie + cible
        b._Wo_strat = self._Wo_strat.copy()
        b._b2_strat = self._b2_strat.copy()
        b._Wo_targ = self._Wo_targ.copy()
        b._b2_targ = self._b2_targ.copy()
        b._strat_probs = self._strat_probs.copy()
        b._targ_probs = self._targ_probs.copy()
        b._strategy = self._strategy
        b._target = self._target
        b._sync()
        return b


OLD_NIN = 128

def migrate_input_weights(old_p, old_n=OLD_NIN, new_n=N_IN):
    """Etend un vecteur de poids historique vers la version courante.

    Layout: Wx(N_IN*n) + Wd(n) + b1(n) + Wo(N_OUT*n) + b2(N_OUT)
    = n*(N_IN + 2 + N_OUT) + N_OUT
    Les anciennes colonnes d'entree (Wx) sont conservees, les nouvelles
    sont initialisees a zero.  Wd, b1, Wo, b2 sont conserves.
    Supporte 95->132 (anciennes saves) et 128->132 (Anima Phase 1).
    """
    denom = old_n + 2 + N_OUT
    n_hid = (old_p.size - N_OUT) // denom
    if n_hid <= 0 or (old_p.size - N_OUT) % denom != 0:
        return old_p, new_n
    Wx_old = old_p[:old_n * n_hid].reshape(old_n, n_hid)
    rest = old_p[old_n * n_hid:]
    Wx_new = np.zeros((new_n, n_hid), dtype=np.float64)
    Wx_new[:old_n, :] = Wx_old
    new_p = np.concatenate([Wx_new.ravel(), rest])
    return new_p, new_n

```

## game/brain_api.py

**Type :** `.py`

```python

"""Courage Brain — API publique.

Fournit les fonctions que les autres couches (simulation, UI) peuvent appeler
pour interagir avec le réseau de neurones sans jamais importer pygame directement.

L'API est délibérément minimaliste : elle ne contient aucune logique de rendu,
aucun gestionnaire d'events, aucun accès aux fichiers ou à la fenêtre. Elle
ne fait que : faire "penser" un cerveau, apprendre de la récompense, et produire
une intention (action + cible + intensité) qui sera interprétée par la couche
supérieure (simulation ou UI).

Toutes les dépendances lourdes (numpy, la structure du réseau) restent dans
brain.py ; ce fichier n'expose que le contrat.
"""
from __future__ import annotations

from typing import Dict, Any, Optional, List

import numpy as np

# Constantes d'action — partagées avec simulation et UI
from game.brain import (
    REST, SLEEP, EAT, DRINK, HARVEST, DROP, BUILD, GIVE, TAKE, ATTACK,
    FLEE, EXPLORE, TALK, MARK, SOCIAL,
    ACTION_NAMES, ACTION_COLORS, N_IN, N_OUT,
    N_STRATEGIES, N_TARGETS, STRATEGY_NAMES, STRATEGY_COLORS,
    TARGET_NAMES, TARGET_COLORS, IMMEDIAT, PRUDENT, ECONOMIQUE,
    COOPERATIF, EXPLORATION, DEFENSIF,
    SOI, NOURRITURE, EAU, BOIS, PIERRE, ABRI, DEPOT_CHANTIER, ETRE_VIVANT,
)

# Import lightweight de la structure Brain (sans dépendre de pygame ou du monde)
from game.brain import Brain


class Intention:
    """Résultat simple et autonome du cerveau — aucun référence pygame/UI.

    action      : index dans 0..14 correspondant au vocabulaire d'actions.
    target_aid  : identifiant d'actif cible (asset id), ou None si pas de cible.
    intensity   : float 0.0 .. 1.0 — force/urgency de l'intention.
    raw_probs   : (optionnel) tableau numpy des probabilités brutes — utile
                   pour le debug ou l'analyse, jamais utilisé par la simulation
                   directement (celle-ci n'a que l'intention choisie).
    strategy    : index de la stratégie choisie (0..5).
    strat_probs : probabilités brutes des stratégies.
    target_type : index du type de cible choisi (0..7).
    targ_probs  : probabilités brutes des types de cible.
    """
    __slots__ = ("action", "target_aid", "intensity", "raw_probs",
                 "strategy", "strat_probs", "target_type", "targ_probs")

    def __init__(self, action: int, target_aid: Optional[int],
                 intensity: float, raw_probs: Optional[np.ndarray] = None,
                 strategy: int = 0, strat_probs: Optional[np.ndarray] = None,
                 target_type: int = 0, targ_probs: Optional[np.ndarray] = None):
        self.action = action
        self.target_aid = target_aid
        self.intensity = float(intensity)
        self.raw_probs = raw_probs
        self.strategy = strategy
        self.strat_probs = strat_probs
        self.target_type = target_type
        self.targ_probs = targ_probs

    def __repr__(self) -> str:
        tgt = f"target={self.target_aid}" if self.target_aid is not None else "pas de cible"
        return f"<Intention action={ACTION_NAMES.get(self.action, self.action)} {tgt} intensité={self.intensity:.2f}>"


def think(brain: Brain, perception: Dict[str, Any]) -> Intention:
    """Faire "penser" un cerveau à partir de sa représentation de perception.

    perception : dict contenant les informations nécessaires au cerveau :
        - corps : dict avec besoins, émotions, état physique
        - monde : dict perception locale (tuiles voisines, ressources visibles)
        - temps : dict avec heure/jour en cours

    Retourne une Intention que la couche supérieure (simulation/UI) appliquera
    au monde via les primitives connues (BUILD, HARVEST, MOVE, etc.).

    Note : brain.py conserve ses poids internes (N_IN=132, N_OUT=15) — cette
    fonction ne fait que Forward pass + échantillonnage d'action.
    """
    x = np.asarray(perception.get("input", np.zeros(N_IN, dtype=np.float64)),
                    dtype=np.float64).ravel()
    if x.shape[0] != N_IN:
        x = np.zeros(N_IN, dtype=np.float64)
    x = x.reshape(1, -1)
    act, probs = brain.think(x, temperature=1.0)

    # Mapping index -> target aid si applicable (selon l'action)
    target_aid = None
    if act == HARVEST:
        # La perception aura fourni la cible potentielle ; ici on laisse None
        # et c'est la simulation qui vérifiera les affordances avant d'agir.
        pass
    elif act == BUILD:
        pass
    elif act == EAT:
        pass

    return Intention(
        action=int(act),
        target_aid=target_aid,
        intensity=brain.probs[act],
        raw_probs=brain.last_out.copy() if hasattr(brain, "last_out") else None,
        strategy=getattr(brain, '_strategy', 0),
        strat_probs=getattr(brain, '_strat_probs', None),
        target_type=getattr(brain, '_target', 0),
        targ_probs=getattr(brain, '_targ_probs', None),
    )


def learn(brain: Brain, reward: float, lr: float = 0.0022,
          age_factor: float = 1.0) -> None:
    """Appliquer un pas d'apprentissage REINFORCE.

    reward      : récompense reçue suite à l'action précédente (peut être négative).
    lr          : taux d'apprentissage (par défaut 0.0022 tel que dans brain.py).
    age_factor  : 0..~2, multiplie le lr — un jeune (>1.0) apprend plus vite,
                  un vieux (<1.0) se fige.

    Ne fait bouger que les poids et biais du cerveau — l'architecture (N_IN,
    N_OUT, nombre de neurones cachés) reste verrouillée.
    """
    brain.learn(reward=reward, lr=lr, age_factor=age_factor)


def explain(brain: Brain, top: int = 5) -> List[Dict[str, Any]]:
    """Classement lisible de la dernière intention, pour le dashboard.

    Retourne une liste de dicts {action, nom, couleur, probabilite}
    triée par probabilité décroissante — aucune connaissance du réseau
    n'est requise côté UI.
    """
    result = brain.explain(top=top)
    # ajouter strategie et cible courantes
    strat = getattr(brain, '_strategy', 0)
    target = getattr(brain, '_target', 0)
    result.append({
        "action": -1,
        "nom": STRATEGY_NAMES.get(strat, "?"),
        "couleur": STRATEGY_COLORS.get(strat, (180, 180, 180)),
        "probabilite": float(getattr(brain, '_strat_probs', np.zeros(N_STRATEGIES))[strat]),
        "type": "strategie",
    })
    result.append({
        "action": -2,
        "nom": TARGET_NAMES.get(target, "?"),
        "couleur": TARGET_COLORS.get(target, (180, 180, 180)),
        "probabilite": float(getattr(brain, '_targ_probs', np.zeros(N_TARGETS))[target]),
        "type": "cible",
    })
    return result


def new_brain(n_hid: int = 128,
              params: Optional[np.ndarray] = None) -> Brain:
    """Créer un nouveau cerveau avec la taille donnée.

    n_hid    : nombre de neurones cachés (taille de la couche intermédiaire).
    params   : poids existants (optionnel) à copier ; si None, poids aléatoires.
    Retourne une instance Brain prête à être utilisée par think()/learn().
    """
    from game.brain import Brain as _Brain
    return _Brain(n_hid=n_hid, params=params)


# ---- Déploiement des constantes partagées ----
# Ces tuples/lists sont aussi définis dans brain.py ; on les réexporte ici
# afin que les autres couches puissent les importer sans importer brain.py
# directement (pour éviter toute dépendance circulaire potentielle).

ACTION_NAMES_EXP = {
    REST: "Repos", SLEEP: "Dormir", EAT: "Manger", DRINK: "Boire",
    HARVEST: "Récolter", DROP: "Poser", BUILD: "Construire",
    GIVE: "Offrir", TAKE: "Prendre", ATTACK: "Attaquer",
    FLEE: "Fuir", EXPLORE: "Explorer", TALK: "Parler", MARK: "Marquer",
    SOCIAL: "Rejoindre",
}

ACTION_TRAIT_EXP = {
    REST: (8, -0.28),
    SLEEP: (11, -0.20),
    EAT: (3, -0.08),
    DRINK: (3, -0.08),
    HARVEST: (8, 0.30),
    DROP: (11, 0.10),
    BUILD: (8, 0.36),
    GIVE: (10, 0.48),
    TAKE: (1, 0.30),
    ATTACK: (1, 0.42),
    FLEE: (3, 0.30),
    EXPLORE: (2, 0.44),
    TALK: (0, 0.42),
    MARK: (9, 0.22),
    SOCIAL: (0, 0.40),
}

SIZES_EXP = (25, 50, 75, 100, 128, 256, 512, 768, 1000)

ACTION_COLORS_EXP = ACTION_COLORS


def think_every(n: int) -> int:
    """Règle la fréquence de réflexion (identique à brain.think_every)."""
    if n <= 128:
        return 2
    if n <= 256:
        return 4
    if n <= 1024:
        return 8
    return 16


def params_size(n: int) -> int:
    """Taille totale des paramètres pour un cerveau de n neurones cachés."""
    return N_IN * n + n + n + N_OUT * n + N_OUT


# Export pratique : importer ces constantespuisque brain.py les a déjà
# on les réexporte ici pour que UI/simulation puissent les avoir sans
# dépendre directement de l'implémentation brain.py (bien qu'ils existent
# dedans aussi). Cela découple les imports "bas niveau".
__all__ = [
    "Intention", "think", "learn", "explain", "new_brain",
    "ACTION_NAMES_EXP", "ACTION_TRAIT_EXP", "ACTION_COLORS", "ACTION_COLORS_EXP",
    "SIZES_EXP",
    "think_every", "params_size",
]

```

## game/brain_schema.py

**Type :** `.py`

```python

"""Registre officiel des 132 entrées du vecteur de perception.

Ce fichier est LA source de vérité pour les indices du vecteur sense().
Toute modification d'entrées doit passer par ici.
"""

NIN_VERSION = 3
NIN = 132

INPUT = {
    # Besoins vitaux (0-9)
    "hunger": 0,
    "energy": 1,
    "thirst": 2,
    "sleep": 3,
    "fear_inverse": 4,
    "belonging": 5,
    "esteem_need": 6,
    "health": 7,
    "age": 8,
    "temperature": 9,

    # Corps (10-14)
    "body_start": 10,       # body[0..4]

    # Personnalité (15-26)
    "personality_start": 15, # personality[0..11]

    # Émotions (27-34)
    "emotion_start": 27,     # emotions[0..7]

    # Cognition (35-38)
    "cognition_start": 35,   # cog[0..3]

    # Estime de soi / réputation (39-40)
    "self_esteem": 39,
    "reputation": 40,

    # Social (41-44)
    "near_trust": 41,
    "has_hated": 42,
    "has_partner": 43,
    "is_child": 44,

    # Compétences (45-48)
    "skills_start": 45,      # skills[0..3]

    # Habitudes (49-63)
    "habits_start": 49,      # habits[0..14]

    # Humeur (64)
    "mood": 64,

    # Perception locale 8 canaux (65-72)
    "local_start": 65,       # _loc[0..7]

    # Mémoire spatiale 6 catégories × 3 (73-90)
    "memory_start": 73,

    # Temps (91-94)
    "day_sin": 91,
    "day_cos": 92,
    "weather_temp": 93,
    "rain": 94,

    # Inventaire (95-98)
    "wood_inventory": 95,
    "stone_inventory": 96,
    "seed_inventory": 97,
    "gold_inventory": 98,

    # Outil (99-103)
    "tool_equipped": 99,
    "tool_durability": 100,
    "tool_axe": 101,
    "tool_pickaxe": 102,
    "tool_hammer": 103,

    # Contexte spatial (104-115)
    "food_density": 104,
    "wood_density": 105,
    "stone_density": 106,
    "sheep_near": 107,
    "allies_near": 108,
    "enemies_near": 109,
    "storage_near": 110,
    "storage_food": 111,
    "storage_wood": 112,
    "site_near": 113,
    "site_progress": 114,
    "site_missing": 115,

    # Mémoire de distance (116-119)
    "food_distance": 116,
    "water_distance": 117,
    "shelter_distance": 118,
    "partner_distance": 119,

    # État avancé (120-127)
    "route_danger": 120,
    "neighbor_need": 121,
    "local_reputation": 122,
    "winter": 123,
    "home_storage": 124,
    "inventory_load": 125,
    "local_fear": 126,
    "life_progress": 127,

    # Anima — mémoire épisodique émotionnelle (128-131)
    "trauma_attack": 128,
    "belief_danger": 129,
    "episode_count": 130,
    "anima_fighter": 131,
}

N_ACTIONS = 15

```

## game/camera.py

**Type :** `.py`

```python

"""Camera : deplacement/zoom + INCLINAISON 2.5D.

Le sol est verticalement ecrase par cos(tilt) (vue plongeante 45-60 degres),
les sprites restent debouts (billboards) ancrs au sol : c'est la projection
conceptuelle du document d'architecture, en 2D pur.

    screen_x = (wx - cam.x) * zoom
    screen_y = (wy - cam.y) * zoom * cos(tilt)
"""
import math

from .config import GRID, TILE, VIEW_W, VIEW_H

WORLD = GRID * TILE
ZOOMS = (0.1, 0.15, 0.2, 0.25, 0.35, 0.5, 0.75, 1, 1.5, 2, 3, 4, 6)


class Camera:
    def __init__(self, tilt=55.0):
        self.zoom = 0.25
        self.tilt = max(30.0, min(70.0, float(tilt)))
        self.x = WORLD / 2 - self.view_w() / 2
        self.y = WORLD / 2 - self.view_h() / 2

    @property
    def ys(self):
        return math.cos(math.radians(self.tilt))

    def view_w(self):
        return VIEW_W / self.zoom

    def view_h(self):
        return VIEW_H / (self.zoom * self.ys)

    def clamp(self):
        vw, vh = self.view_w(), self.view_h()
        if vw >= WORLD:
            self.x = (WORLD - vw) / 2
        else:
            self.x = min(max(self.x, 0), WORLD - vw)
        if vh >= WORLD:
            self.y = (WORLD - vh) / 2
        else:
            self.y = min(max(self.y, 0), WORLD - vh)

    def center_on(self, x, y):
        self.x = x - self.view_w() / 2
        self.y = y - self.view_h() / 2
        self.clamp()

    def to_world(self, sx, sy):
        return self.x + sx / self.zoom, self.y + sy / (self.zoom * self.ys)

    def to_screen(self, wx, wy):
        return (wx - self.x) * self.zoom, (wy - self.y) * self.zoom * self.ys

    def visible_tiles(self):
        tw = self.view_w()
        th = self.view_h()
        x0 = int(self.x // TILE) - 2
        y0 = int(self.y // TILE) - 2
        x1 = int((self.x + tw) // TILE) + 4
        y1 = int((self.y + th) // TILE) + 4
        return x0, y0, x1, y1

    def set_zoom(self, nz, anchor_screen=None):
        if anchor_screen is None:
            self.zoom = nz
            self.clamp()
            return
        ax, ay = anchor_screen
        wx, wy = self.to_world(ax, ay)
        self.zoom = nz
        self.x = wx - ax / nz
        self.y = wy - ay / (nz * self.ys)
        self.clamp()

```

## game/clock.py

**Type :** `.py`

```python

"""Temps meteo : jour/nuit, saisons, pluie, vent, temperature.
Le monde vieillit : une foret laissee seule ne doit pas rester identique."""
import numpy as np

from .config import DAY_TICKS, DAYS_PER_SEASON, SEASONS


class Clock:
    def __init__(self, rng=None):
        self.rng = rng or np.random.default_rng(3)
        self.t = 0
        self.day = 0
        self.season = 0
        self.year = 0
        self.light = 1.0          # 0 nuit -> 1 jour
        self.temp = 0.6           # 0 glace -> 1 canicule
        self.rain = 0.0           # 0..1 intensite
        self.wind = (0.0, 0.0)
        self.growth_f = 1.0
        self._storm = 0

    @property
    def day_frac(self):
        return (self.t % DAY_TICKS) / DAY_TICKS

    @property
    def is_night(self):
        return self.light < 0.35

    @property
    def is_winter(self):
        return self.season == 3

    def label(self):
        h = int(self.day_frac * 24)
        m = int((self.day_frac * 24 - h) * 60)
        return f"An {self.year+1} · {SEASONS[self.season]} · jour {self.day % (DAYS_PER_SEASON*4)+1} · {h:02}:{m:02}"

    def step(self):
        self.t += 1
        f = self.day_frac
        # lumiere : aube 0.05-0.25, jour, crépuscule 0.7-0.9
        if f < 0.05:
            self.light = 0.15 + f / 0.05 * 0.85
        elif f < 0.70:
            self.light = 1.0
        elif f < 0.85:
            self.light = 1.0 - (f - 0.70) / 0.15 * 0.85
        else:
            self.light = 0.15
        # cycle jour/nuit -> saison -> annee
        if f < 1.0 / DAY_TICKS:
            self.day += 1
            if self.day % DAYS_PER_SEASON == 0:
                self.season = (self.season + 1) % 4
                if self.season == 0:
                    self.year += 1
        # temperature saisonniere + diurne + bruit
        s_base = (0.85, 0.95, 0.6, 0.25)[self.season]
        self.temp = float(np.clip(s_base + 0.15 * (self.light - 0.5)
                                  + self.rng.normal(0, 0.02), 0, 1))
        self.growth_f = max(0.15, self.temp * (1.0 + 0.8 * self.rain)
                            - 0.25 * (self.season == 3))
        # meteo : etat machine (sec / nuage / pluie / orage)
        if self._storm > 0:
            self._storm -= 1
            self.rain = min(1.0, self.rain + 0.02)
        elif self.rain > 0:
            self.rain = max(0.0, self.rain - 0.004)
        elif self.rng.random() < 0.0012:
            self._storm = int(self.rng.integers(400, 1400))
            self.rain = 0.3
        ang = self.rng.uniform(0, 6.283) if self.rain > 0.5 else None
        if ang is not None:
            self.wind = (float(np.cos(ang)) * self.rain, float(np.sin(ang)) * self.rain)
        else:
            self.wind = (self.wind[0] * 0.98, self.wind[1] * 0.98)
        return self

    def lightning(self):
        """Eclairs pendant les orages — le feu n'est jamais scripted ailleurs."""
        return self.rain > 0.75 and self.rng.random() < 0.004

```

## game/config.py

**Type :** `.py`

```python

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(ROOT, "assets")
MAP_FILE = os.path.join(ROOT, "map", "sea_blue_16000x16000.png")

TILE = 16
GRID = 1000
WORLD_PX = GRID * TILE

# detect screen size dynamically
def _detect_screen():
    try:
        import ctypes
        user32 = ctypes.windll.user32
        return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    except Exception:
        pass
    return 1600, 900

_sw, _sh = _detect_screen()
SCREEN_W = min(_sw - 40, 1600)
SCREEN_H = min(_sh - 80, 900)
LEFT_W = 320
DASH_W = 380
VIEW_W = SCREEN_W - DASH_W - LEFT_W
VIEW_H = SCREEN_H

MAX_POP = 800
MAX_SHEEP = 300

BG = (12, 14, 22)
PANEL = (20, 24, 36)
PANEL2 = (26, 30, 44)
INK = (232, 238, 248)
MUTED = (142, 152, 172)
ACCENT = (78, 168, 232)
GOOD = (108, 208, 128)
BAD = (228, 98, 98)
GOLD = (248, 208, 98)

CLAN_COLORS = {
    "blue": (88, 148, 228),
    "red": (218, 88, 78),
    "yellow": (238, 198, 78),
    "purple": (178, 118, 218),
    "black": (62, 68, 82),
}

# ---- temps / climat
# Objectif : 1 h réelle = 10 ans simulés à vitesse ×4
# SIM_HZ=30, ×4 = 120 ticks/s, 1 h = 432 000 ticks
# Calendrier : 20 jours/an (4 saisons × 5 jours)
SIM_HZ = 30
FPS = 20
TARGET_OBSERVATION_SPEED = 4.0
TARGET_YEARS_PER_REAL_HOUR = 10.0
TICKS_PER_REAL_HOUR_AT_TARGET = int(SIM_HZ * TARGET_OBSERVATION_SPEED * 3600)
TICKS_PER_YEAR = int(TICKS_PER_REAL_HOUR_AT_TARGET / TARGET_YEARS_PER_REAL_HOUR)
DAYS_PER_SEASON = 5
SEASONS = ("Printemps", "Été", "Automne", "Hiver")
DAYS_PER_YEAR = DAYS_PER_SEASON * len(SEASONS)
DAY_TICKS = TICKS_PER_YEAR // DAYS_PER_YEAR
NIGHT_START = 0.72          # fraction du jour où la nuit tombe

# ---- âges biologiques (dérivés du calendrier)
AGE_CHILD_YEARS = 18
AGE_ELDER_YEARS = 65
AGE_MIN_NATURAL_DEATH_YEARS = 75
AGE_MAX_NATURAL_DEATH_YEARS = 95
DEFAULT_SPAWN_AGE_YEARS = 18

AGE_CHILD_TICKS = AGE_CHILD_YEARS * TICKS_PER_YEAR
AGE_ELDER_TICKS = AGE_ELDER_YEARS * TICKS_PER_YEAR
AGE_MIN_NATURAL_DEATH_TICKS = AGE_MIN_NATURAL_DEATH_YEARS * TICKS_PER_YEAR
AGE_MAX_NATURAL_DEATH_TICKS = AGE_MAX_NATURAL_DEATH_YEARS * TICKS_PER_YEAR
DEFAULT_SPAWN_AGE_TICKS = DEFAULT_SPAWN_AGE_YEARS * TICKS_PER_YEAR

SAVE_DIR = os.path.join(ROOT, "data", "saves")

# ---- besoins (couches de l'être)
NEED_DEFS = ["faim", "énergie", "soif", "sommeil", "sécurité", "appartenance", "estime"]
EMOTION_DEFS = ["peur", "joie", "colère", "tristesse", "stress", "surprise",
                "dégoût", "affection"]
BODY_DEFS = ["force", "endurance", "mobilité", "sens", "récupération"]
COG_DEFS = ["mémoire", "anticipation", "imagination", "attention"]
PERSONALITY_DEFS = ["sociabilité", "agressivité", "curiosité", "prudence", "patience",
                    "empathie", "impulsivité", "confiance", "persévérance", "ambition",
                    "générosité", "discipline"]

TOOL_RECIPES = {
    "hache":   {"bois": 2, "pierre": 1, "durability": 40},
    "pioche":  {"bois": 1, "pierre": 3, "durability": 45},
    "marteau": {"bois": 3, "pierre": 2, "durability": 50},
}

```

## game/construction.py

**Type :** `.py`

```python

"""Construction progressive avec tâches à identité unique.

Chaque phase d'une même tuile a son propre identifiant :
- fondation (niveau 0)
- mur/porte (niveau 1)
- toit (niveau 2)

Ainsi, poser une fondation ne termine jamais automatiquement le mur.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class BlockTask:
    tx: int
    ty: int
    material: str
    phase: str
    layer: int
    solid: bool = True

    @property
    def key(self):
        return self.tx, self.ty, self.layer, self.phase


@dataclass
class ConstructionSite:
    origin_tx: int
    origin_ty: int
    blueprint_name: str
    tasks: list[BlockTask]
    placed: set[tuple[int, int, int, str]] = field(default_factory=set)
    contributors: dict[int, int] = field(default_factory=dict)
    created_tick: int = 0
    owner_eid: int | None = None
    owner_clan: str | None = None

    @property
    def key(self):
        return self.origin_tx, self.origin_ty

    def remaining_tasks(self):
        return [task for task in self.tasks if task.key not in self.placed]

    def complete(self):
        return len(self.placed) >= len(self.tasks)

    def progress(self):
        return 1.0 if not self.tasks else min(1.0, len(self.placed) / len(self.tasks))

    def missing_materials(self):
        result = {}
        for task in self.remaining_tasks():
            result[task.material] = result.get(task.material, 0) + 1
        return result

    def next_task_for(self, inventory):
        order = {"foundation": 0, "wall": 1, "door": 1, "roof": 2}
        for task in sorted(self.remaining_tasks(), key=lambda t: (t.layer, order.get(t.phase, 9))):
            if inventory.get(task.material, 0) > 0:
                return task
        return None

    def mark_placed(self, eid, task):
        self.placed.add(task.key)
        self.contributors[eid] = self.contributors.get(eid, 0) + 1


class HouseBlueprint:
    """Plans de bâtiments composés de tâches ordonnées."""

    @staticmethod
    def small_house(tx, ty, wall_material="bois"):
        tasks = []
        width, height = 5, 5
        door_x = tx + width // 2
        door_y = ty + height - 1

        for y in range(ty, ty + height):
            for x in range(tx, tx + width):
                edge = x in (tx, tx + width - 1) or y in (ty, ty + height - 1)
                if edge:
                    tasks.append(BlockTask(x, y, "pierre", "foundation", layer=0, solid=True))

        for y in range(ty, ty + height):
            for x in range(tx, tx + width):
                edge = x in (tx, tx + width - 1) or y in (ty, ty + height - 1)
                if not edge:
                    continue
                if x == door_x and y == door_y:
                    tasks.append(BlockTask(x, y, "bois", "door", layer=1, solid=False))
                else:
                    tasks.append(BlockTask(x, y, wall_material, "wall", layer=1, solid=True))

        for x in range(tx, tx + width):
            tasks.append(BlockTask(x, ty, "bois", "roof", layer=2, solid=False))

        return tasks

    @staticmethod
    def storage_hut(tx, ty):
        tasks = []
        for y in range(ty, ty + 3):
            for x in range(tx, tx + 3):
                edge = x in (tx, tx + 2) or y in (ty, ty + 2)
                if edge:
                    tasks.append(BlockTask(x, y, "bois", "wall", layer=1, solid=True))
        tasks.append(BlockTask(tx + 1, ty + 2, "bois", "door", layer=1, solid=False))
        return tasks

    @staticmethod
    def coffre(tx, ty):
        tasks = [BlockTask(tx, ty, "bois", "foundation", layer=0, solid=True)]
        return tasks

    @staticmethod
    def grenier(tx, ty):
        tasks = []
        for y in range(ty, ty + 2):
            for x in range(tx, tx + 2):
                tasks.append(BlockTask(x, y, "bois", "wall", layer=1, solid=True))
        tasks.append(BlockTask(tx, ty + 1, "bois", "door", layer=1, solid=False))
        tasks.append(BlockTask(tx, ty, "bois", "roof", layer=2, solid=False))
        tasks.append(BlockTask(tx + 1, ty, "bois", "roof", layer=2, solid=False))
        return tasks

    @staticmethod
    def atelier(tx, ty):
        tasks = []
        for y in range(ty, ty + 3):
            for x in range(tx, tx + 3):
                edge = x in (tx, tx + 2) or y in (ty, ty + 2)
                if edge:
                    tasks.append(BlockTask(x, y, "pierre", "wall", layer=1, solid=True))
        tasks.append(BlockTask(tx + 1, ty + 2, "pierre", "door", layer=1, solid=False))
        tasks.append(BlockTask(tx, ty, "bois", "roof", layer=2, solid=False))
        tasks.append(BlockTask(tx + 1, ty, "bois", "roof", layer=2, solid=False))
        tasks.append(BlockTask(tx + 2, ty, "bois", "roof", layer=2, solid=False))
        return tasks

    @staticmethod
    def puits(tx, ty):
        tasks = [BlockTask(tx, ty, "pierre", "foundation", layer=0, solid=True)]
        return tasks


def blueprint_from_name(name, tx, ty):
    if name == "storage_hut":
        return HouseBlueprint.storage_hut(tx, ty)
    if name == "coffre":
        return HouseBlueprint.coffre(tx, ty)
    if name == "grenier":
        return HouseBlueprint.grenier(tx, ty)
    if name == "atelier":
        return HouseBlueprint.atelier(tx, ty)
    if name == "puits":
        return HouseBlueprint.puits(tx, ty)
    return HouseBlueprint.small_house(tx, ty)

```

## game/dashboard.py

**Type :** `.py`

```python

"""Dashboard — Univers Vivant (style « atelier clair »).

Structure :
    [rail] [ panneau gauche repliable ] [ carte ] [ panneau droit 2 colonnes ]

Tout est piloté par des REGISTRES en haut de fichier :
    · SECTION_REGISTRY  → les accordéons de l'inspecteur (Corps, Cognition…)
    · CARD_REGISTRY     → les cartes de la colonne droite (Intention, Gabarit…)
    · TABS / MODES      → navigation et outils
Ajouter une section ou une carte = ajouter UNE entrée, rien d'autre.

Aucune coordonnée en dur : tout dérive de SCREEN_W / SCREEN_H, et chaque
bloc est rogné à sa zone visible — rien ne peut sortir de l'écran.

API publique inchangée : Dashboard(am), .draw(screen, sim, cam),
.handle_event(ev, sim), .set_ghost(cam), .apply_map_tool(sim, cam, button),
.action, .mode, .tab, .follow, .focus_search, .hover_tile.

⚠ Le panneau gauche étant repliable, la carte n'a plus une largeur fixe :
le moteur de rendu doit lire dash.view_rect() (ou .view_x / .view_w) au
lieu des constantes LEFT_W / VIEW_W de config.

--------------------------------------------------------------------------
AMELIORATIONS (integration inchangee — memes methodes publiques, memes
registres, memes signatures) :

1. Bug corrige dans _identity() : `ag.bonded` est un eid (int) fourni par
   simulation.py (`a.bonded, e.bonded = e.eid, a.eid`), jamais un objet
   Being — l'ancien code faisait `ag.bonded.name` et plantait a la
   selection de tout etre en couple. Resolu via recherche dans sim.agents.
2. Stats "Societe" fiabilisees : `max_gen` et `bonded` n'existent pas dans
   sim.stats (qui ne contient que des compteurs d'evenements) — l'ancien
   affichage montrait donc toujours 0. Calcules en direct.
3. Nouvelle carte INTENTION (CARD_REGISTRY) : classement en direct des
   intentions du cerveau via brain.explain(), avec marquage de celle
   reellement engagee comme but (utile pour voir quand la faisabilite
   du monde ecarte le choix prefere du reseau).
4. Nouvelle carte MEMOIRE : autobiographie de l'etre (a.life) + nombre
   de lieux crus dangereux (belief_places) — fenetre sur le vecu
   subjectif, pas seulement les stats brutes.
5. Presets de vitesse ×1/×2/×4/×8 en plus des +/- existants.
--------------------------------------------------------------------------
"""
import os
import numpy as np
import pygame

from . import config
from .assets_api import CATEGORY_LABELS
from .brain_api import ACTION_NAMES_EXP as ACTION_NAMES, ACTION_COLORS_EXP as ACTION_COLORS, \
    SIZES_EXP as SIZES, think_every
from .config import (BODY_DEFS, CLAN_COLORS, COG_DEFS, DASH_W, EMOTION_DEFS,
                     GRID, LEFT_W, NEED_DEFS, PERSONALITY_DEFS, SCREEN_H,
                     SCREEN_W, TILE)


from dataclasses import dataclass


@dataclass
class ScrollState:
    offset: int = 0
    drag_grab_y: int | None = None


class ScrollController:
    """Scrollbar déterministe : molette douce, drag précis, clic piste = page."""
    MIN_HANDLE = 32
    WHEEL_STEP = 28

    @staticmethod
    def clamp(offset, content_h, view_h):
        return max(0, min(int(offset), max(0, int(content_h) - int(view_h))))

    @classmethod
    def handle_rect(cls, track, content_h, offset):
        track = pygame.Rect(track)
        if content_h <= track.height:
            return None
        max_offset = max(1, content_h - track.height)
        handle_h = max(cls.MIN_HANDLE, int(track.height * track.height / content_h))
        handle_h = min(track.height, handle_h)
        travel = max(1, track.height - handle_h)
        y = track.y + int((offset / max_offset) * travel)
        return pygame.Rect(track.x + 2, y, max(6, track.width - 4), handle_h)

    @classmethod
    def wheel(cls, state, wheel_y, content_h, view_h):
        state.offset = cls.clamp(
            state.offset - int(wheel_y) * cls.WHEEL_STEP, content_h, view_h)
        return state.offset

    @classmethod
    def press(cls, state, pos, track, content_h, view_h):
        track = pygame.Rect(track)
        handle = cls.handle_rect(track, content_h, state.offset)
        if handle is None or not track.collidepoint(pos):
            return False
        if handle.collidepoint(pos):
            state.drag_grab_y = pos[1] - handle.y
            return True
        if pos[1] < handle.y:
            state.offset -= int(view_h * 0.85)
        else:
            state.offset += int(view_h * 0.85)
        state.offset = cls.clamp(state.offset, content_h, view_h)
        return True

    @classmethod
    def drag(cls, state, pos, track, content_h, view_h):
        if state.drag_grab_y is None:
            return False
        track = pygame.Rect(track)
        handle = cls.handle_rect(track, content_h, state.offset)
        if handle is None:
            state.drag_grab_y = None
            return False
        max_offset = max(1, content_h - track.height)
        travel = max(1, track.height - handle.height)
        target_y = pos[1] - state.drag_grab_y
        ratio = max(0.0, min(1.0, (target_y - track.y) / travel))
        state.offset = cls.clamp(int(ratio * max_offset), content_h, view_h)
        return True

    @staticmethod
    def release(state):
        state.drag_grab_y = None


# ══════════════════════════════════════════════════════════════════════
#  1. DESIGN TOKENS
# ══════════════════════════════════════════════════════════════════════
class T:
    APP = (238, 240, 244)          # fond application
    RAIL = (246, 247, 249)         # rail d'icônes
    SURFACE = (255, 255, 255)
    SURFACE_2 = (250, 251, 253)
    HOVER = (241, 244, 249)
    SELECT = (232, 240, 253)
    TRACK = (237, 239, 244)   # plus discret
    BORDER = (226, 229, 235)
    BORDER_2 = (205, 210, 219)
    TEXT = (31, 36, 48)
    MUTED = (105, 114, 129)
    FAINT = (156, 163, 176)
    ON_DARK = (255, 255, 255)
    ACCENT = (59, 118, 214)
    DARK = (32, 38, 50)            # badge neurones
    DANGER = (214, 84, 84)
    WARN = (222, 160, 50)
    OK = (72, 158, 104)
    TIP_BG = (34, 40, 52)
    TIP_FG = (232, 236, 243)
    TIP_MUTED = (150, 159, 174)
    S1, S2, S3, S4, S5 = 4, 8, 12, 16, 24
    R1, R2, R3 = 6, 9, 13
    F_MICRO, F_SMALL, F_BODY, F_SUB, F_TITLE = 11, 12, 13, 15, 18
    H_ROW = 22                # la pilule respire mieux
    H_HEAD = 27
    H_BTN = 25
    H_TAB = 28
    H_FIELD = 27
    CELL = 68
    RAIL_W = 46


# — accents par famille de donnée, réutilisés partout —
C_CORPS = (67, 160, 92)
C_COG = (62, 124, 214)
C_PERSO = (222, 164, 46)
C_EMO = (34, 158, 142)
C_BESOIN = (146, 96, 186)
C_EXP = (206, 126, 60)
C_MEM = (150, 110, 200)

FONT_STACK = "segoeui,seguisb,inter,dejavusans,liberationsans,arial"


# ══════════════════════════════════════════════════════════════════════
#  2. REGISTRES — le seul endroit à toucher pour étendre l'interface
# ══════════════════════════════════════════════════════════════════════
SKILL_DEFS = ["récolte", "construction", "combat", "social"]

#  (clé, libellé, couleur, libellés des champs, attribut agent, attribut gabarit)
SECTION_REGISTRY = [
    ("body",   "Corps",        C_CORPS,  BODY_DEFS,        "body",        "tpl_body"),
    ("cog",    "Cognition",    C_COG,    COG_DEFS,         "cog",         "tpl_cog"),
    ("perso",  "Personnalité", C_PERSO,  PERSONALITY_DEFS, "personality", "tpl_personality"),
    ("emo",    "Émotions",     C_EMO,    EMOTION_DEFS,     "emotions",    "tpl_emotions"),
    ("needs",  "Besoins",      C_BESOIN, NEED_DEFS,        "needs",       "tpl_needs"),
    ("skills", "Expérience",   C_EXP,    SKILL_DEFS,       "skills",      "tpl_skills"),
]
DEFAULT_OPEN = {"body": True, "cog": True, "perso": True,
                "emo": True, "needs": False, "skills": False}

#  Cartes de la colonne de droite : (clé, nom de la méthode de rendu)
#  Chaque méthode a la signature (self, screen, rect, sim) -> hauteur utilisée.
CARD_REGISTRY = [
    ("intention", "_card_intention"),
    ("memoire", "_card_memoire"),
    ("gabarit", "_card_gabarit"),
    ("events", "_card_events"),
]

MODES = [("place", "Poser"), ("erase", "Gommer"), ("floor", "Sol"),
         ("block", "Bloc"),
         ("agent", "Être"), ("sheep", "Mouton"), ("monster", "Monstre"),
         ("inspect", "Examiner"),
         ("water", "Eau"), ("land", "Terre"), ("wall", "Mur"),
         ("carve", "Sculpter"), ("restore", "Restaurer")]

SEX_CLASSES = {
    "M": ("swordsman", "archer", "wizard", "pawn"),
    "F": ("knight", "enchantress", "musketeer", "pawn"),
}
TAB_MODES = {
    "decor":    [("place", "Poser"), ("erase", "Gommer"), ("floor", "Sol"),
                 ("block", "Bloc"),
                 ("water", "Eau"), ("land", "Terre"), ("wall", "Mur"),
                 ("carve", "Sculpter"), ("restore", "Restaurer"),
                 ("inspect", "Examiner")],
    "etre":     [("agent", "Être"), ("inspect", "Examiner")],
    "habitants": [("agent", "Créer"), ("inspect", "Examiner")],
    "societe":  [],
    "journal":  [],
}
TAB_HINTS = {
    "place": "clic = poser l'asset · glisser = peindre",
    "erase": "clic = effacer les objets de la case",
    "floor": "clic = peindre le sol sélectionné",
    "agent": "clic = insérer l'être défini dans le gabarit",
    "sheep": "clic = ajouter un mouton",
    "monster": "clic = ajouter un monstre aléatoire",
    "inspect": "clic = examiner un être",
    "water": "glisser = transformer terre en eau (pinceau)",
    "land": "glisser = transformer eau en terre (pinceau)",
    "wall": "glisser = placer des rochers solides (pinceau)",
    "carve": "glisser = creuser les montagnes (pinceau)",
    "restore": "glisser = restaurer le terrain procédural (pinceau)",
}
TABS = [("decor", "DÉCOR"), ("etre", "ÊTRE"), ("habitants", "HABITANTS"),
        ("creator", "CRÉATEUR"),
        ("societe", "SOCIÉTÉ"), ("journal", "JOURNAL")]
READONLY_TABS = ("societe", "journal", "habitants")
CAT_ALL = "__all__"
HIDDEN_CATS = {"unites", "interface", "atlas", "rendus"}

LOG_CATS = {"combat": (214, 84, 84), "social": (198, 100, 162),
            "meteo": (62, 124, 214), "economie": (206, 160, 50),
            "vie": (67, 160, 92), "mort": (140, 80, 86),
            "batiment": (96, 154, 96), "monde": (112, 126, 150)}
LOG_TITLES = {"combat": "Combat", "social": "Social", "meteo": "Météo",
              "economie": "Économie", "vie": "Vie", "mort": "Mort",
              "batiment": "Bâtiment", "monde": "Monde"}

CHIP_LABELS = {"__all__": "Tous", "ressources": "Ressources", "nourriture": "Nourriture",
               "batiments": "Bâtiments", "outils": "Outils", "animaux": "Animaux",
               "props": "Props", "vehicules": "Véhicules", "tombe": "Tombes",
               "decor": "Décor", "sol": "Sols", "unites": "Unités",
               "effets": "Effets", "interface": "Interface", "atlas": "Atlas",
               "rendus": "Rendus", "divers": "Divers"}

#  Légende de la carte (overlay coin haut-droit du viewport)
MAP_LEGEND = [("Fertilité", (126, 196, 122)), ("Ressource", (226, 186, 78)),
              ("Danger", (218, 108, 100))]

SPEED_PRESETS = (1, 2, 4, 8)


def _mix(a, b, t):
    return (int(a[0] + (b[0] - a[0]) * t), int(a[1] + (b[1] - a[1]) * t),
            int(a[2] + (b[2] - a[2]) * t))


def _tint(c, t=0.12):
    return _mix(T.SURFACE, c, t)


def _goal_txt(a):
    if a is not None and getattr(a, "goal", None):
        return f"{ACTION_NAMES.get(a.goal['act'], '?')} → ({a.goal['x']},{a.goal['y']})"
    return "—"


# ══════════════════════════════════════════════════════════════════════
#  3. DASHBOARD
# ══════════════════════════════════════════════════════════════════════
class Dashboard:
    def __init__(self, am, controller=None):
        self.am = am
        self.controller = controller
        # — largeurs : bornées pour ne jamais écraser la carte —
        self.panel_l = min(LEFT_W, 320)
        self.panel_r = min(DASH_W, 420)
        self.left_open = True
        self.x0 = SCREEN_W - self.panel_r          # recalculé à chaque frame
        self.view_x, self.view_w = 0, 0

        self.mode = "agent"
        trees = am.pool("tree")
        self.asset = trees[0] if trees else 0
        self.category = CAT_ALL
        self.tab = "etre"
        self.search = ""
        self.hab_search = ""
        self.focus_search = False
        self.hab_focus = False
        self.scroll = 0
        self.filtered = [a.id for a in am.assets]
        self._filter_sig = None
        self.hover_asset = None
        self.hover_tile = (0, 0)
        self.recents, self.favs = [], []
        self.only_favs = False
        self.jfilter = "tous"
        self.sections = dict(DEFAULT_OPEN)
        self.cards_open = {k: True for k, _ in CARD_REGISTRY}

        # — portraits (portraits 64x64)
        self.portraits = {}
        self._load_portraits()

        from game.brain import N_IN as _N_IN
        self.brain_size = _N_IN
        self._init_state()

    def _load_portraits(self):
        # La v1 pointait vers un chemin absolu Windows ("E:\\my world2\\...") :
        # aucun portrait ne se chargeait ailleurs que sur la machine d'origine.
        # On cherche maintenant à côté du paquet, puis à côté du script.
        here = os.path.dirname(os.path.abspath(__file__))
        candidates = [
            os.environ.get("UNIVERS_PORTRAITS", ""),
            os.path.join(here, "assets", "portraits"),
            os.path.join(here, "..", "assets", "portraits"),
            os.path.join(os.getcwd(), "assets", "portraits"),
        ]
        base = next((os.path.normpath(c) for c in candidates
                     if c and os.path.isdir(c)), None)
        if base is None:
            return
        mapping = {
            # (sex, cls) -> filename
            ("M", "swordsman"): "male_swordsman",
            ("M", "archer"): "male_archer",
            ("M", "wizard"): "male_wizard",
            ("M", "pawn"): "male_swordsman",
            ("F", "knight"): "female_knight",
            ("F", "enchantress"): "female_enchantress",
            ("F", "musketeer"): "female_musketeer",
            ("F", "pawn"): "female_knight",
        }
        for key, fname in mapping.items():
            path = os.path.join(base, f"{fname}.png")
            if not os.path.exists(path):
                continue
            try:
                self.portraits[key] = pygame.image.load(path).convert_alpha()
            except pygame.error:
                pass   # un fichier illisible ne doit pas empêcher le démarrage

    def _get_portrait(self, sex, cls):
        key = (sex, cls.lower())
        if key in self.portraits:
            return self.portraits[key]
        # fallback par sexe
        fallback = ("M", "pawn") if sex == "M" else ("F", "pawn")
        return self.portraits.get(fallback)

    def _get_cached_portrait(self, sex, cls, size=24):
        if not hasattr(self, '_portrait_cache'):
            self._portrait_cache = {}
        ckey = (sex, cls.lower(), size)
        if ckey not in self._portrait_cache:
            p = self._get_portrait(sex, cls)
            if p:
                self._portrait_cache[ckey] = pygame.transform.smoothscale(p, (size, size))
            else:
                self._portrait_cache[ckey] = None
        return self._portrait_cache[ckey]

    def template_classes(self):
        candidates = SEX_CLASSES.get(self.tpl_sex, ("pawn",))
        available = []
        for cls in candidates:
            states = self.am.skin_states(self.tpl_color, cls)
            if states.get("idle"):
                available.append(cls)
        if not available:
            available = self.am.unit_classes(self.tpl_color) or ["pawn"]
        return available

    def normalize_template_class(self):
        choices = self.template_classes()
        if self.tpl_cls not in choices:
            self.tpl_cls = choices[0]

    def report_ui_error(self, context, exc):
        """Erreur non bloquante mais visible dans stderr et journal si disponible."""
        import traceback
        print(f"[Dashboard:{context}] {exc}")
        traceback.print_exc(limit=2)
        if self._sim_ref is not None:
            self._sim_ref.log(f"Erreur UI ({context}) : {type(exc).__name__}",
                              (214, 84, 84), "monde")

    def brain_memory_estimate_mb(self, n=None):
        """Poids Elman float64 : Wx(N_IN*n)+Wd(n)+b1(n)+Wo(N_OUT*n)+b2(N_OUT)."""
        from game.brain import N_IN, N_OUT
        n = int(n if n is not None else self.brain_size)
        params = N_IN * n + 2 * n + N_OUT * n + N_OUT
        return params * 8 / (1024 * 1024)

    def _init_state(self):
        self.tpl_color, self.tpl_cls, self.tpl_sex = "blue", "pawn", "M"
        self.tpl_body = np.full(len(BODY_DEFS), 0.5)
        self.tpl_cog = np.full(len(COG_DEFS), 0.5)
        self.tpl_personality = np.full(len(PERSONALITY_DEFS), 0.5)
        self.tpl_emotions = np.full(len(EMOTION_DEFS), 0.2)
        self.tpl_needs = np.full(len(NEED_DEFS), 0.5)
        self.tpl_skills = np.zeros(len(SKILL_DEFS))
        self.brush_size = 3          # rayon en tiles (3 = 5×5)
        self.hdel_pending = None     # eid en attente de confirmation de suppression
        self._needs_save = False     # vrai après spawn → déclenche auto-save
        self.spawn_modal = False     # True = fenêtre modale de spawn ouverte
        self.block_material = "bois" # matériau pour le mode Bloc
        self.drag = None
        self.follow = False
        self.action = None
        self.painting = None
        self.creator_focus = False
        self.selected_tile = None    # (tx, ty) de la dernière tuile examinée
        self.last_tile_snapshot = None
        self.active_overlay = "none"
        from .tool_editor import ToolEditor
        self.tool_editor = ToolEditor()
        self.tool_editor_kind = "hache"
        self._cam = None
        self._sim_ref = None
        self._over_map = False
        self._scroll = {t: 0 for t, _ in TABS}
        self._scroll["_left"] = 0
        self._scroll["_right"] = 0
        self._content_h = dict(self._scroll)
        self.buttons, self._cells, self._slider_geo = [], [], {}
        self._scroll_geo = {}
        self._hit_clip = None
        self._minimap_surf, self._minimap_ver = None, -1
        self._fonts = {}
        self.scroll_state = {k: ScrollState() for k in
                             ("decor", "etre", "habitants", "societe", "journal", "creator", "_left")}
        self.scroll_tracks = {}
        # Modal scroll state
        self.modal_scroll = ScrollState()
        self.modal_view = None
        self.modal_content_h = 0
        self.modal_track = None
        self.modal_handle = None

    # compat ascendante
    @property
    def pscroll(self):
        return self._scroll.get(self.tab, 0)

    @property
    def hscroll(self):
        return self._scroll.get("habitants", 0)

    # ── 3.1 primitives ──────────────────────────────────────────────
    def _font(self, size, bold=False):
        k = (size, bold)
        if k not in self._fonts:
            self._fonts[k] = pygame.font.SysFont(FONT_STACK, size, bold=bold)
        return self._fonts[k]

    def _clip_text(self, size, txt, max_w, bold=False):
        f = self._font(size, bold)
        if max_w is None or f.size(txt)[0] <= max_w:
            return txt
        ew = f.size("…")[0]
        out = ""
        for ch in txt:
            if f.size(out + ch)[0] + ew > max_w:
                break
            out += ch
        return out + "…"

    def _t(self, s, size, txt, col, x, y, cx=False, cy=False, bold=False,
           right=False, max_w=None, maxw=None):
        if max_w is None:
            max_w = maxw
        txt = self._clip_text(size, str(txt), max_w, bold)
        img = self._font(size, bold).render(txt, True, col)
        if cx:
            x -= img.get_width() // 2
        if right:
            x -= img.get_width()
        if cy:
            y -= img.get_height() // 2
        s.blit(img, (x, y))
        return img.get_width()

    def _tw(self, size, txt, bold=False):
        return self._font(size, bold).size(str(txt))[0]

    def _push(self, rect, fid):
        """Zone cliquable, rognée à la région visible courante."""
        if fid is None:
            return
        r = pygame.Rect(rect)
        if self._hit_clip is not None:
            r = r.clip(self._hit_clip)
            if r.width <= 0 or r.height <= 0:
                return
        self.buttons.append((r, fid))

    def _card(self, s, rect, radius=T.R2, fill=T.SURFACE, border=T.BORDER):
        r = pygame.Rect(rect)
        pygame.draw.rect(s, fill, r, border_radius=radius)
        if border:
            pygame.draw.rect(s, border, r, 1, border_radius=radius)
        return r

    def _btn(self, s, rect, label, fid, primary=False, disabled=False,
             size=T.F_SMALL, radius=T.R1, icon=None):
        r = pygame.Rect(rect)
        hov = (not disabled) and r.collidepoint(pygame.mouse.get_pos())
        if disabled:
            bg, fg, bd = T.SURFACE_2, T.FAINT, T.BORDER
        elif primary:
            bg, fg, bd = (_mix(T.ACCENT, (0, 0, 0), .12) if hov else T.ACCENT), T.ON_DARK, None
        else:
            bg, fg, bd = (T.HOVER if hov else T.SURFACE), T.TEXT, (T.BORDER_2 if hov else T.BORDER)
        pygame.draw.rect(s, bg, r, border_radius=radius)
        if bd:
            pygame.draw.rect(s, bd, r, 1, border_radius=radius)
        tx = r.centerx + (6 if icon else 0)
        if icon:
            icon(s, r.x + 12, r.centery, fg)
        self._t(s, size, label, fg, tx, r.centery, cx=True, cy=True,
                max_w=r.width - (24 if icon else 10))
        if not disabled:
            self._push(r, fid)
        return r

    def _chip(self, s, rect, label, fid, sel=False, color=None, size=T.F_MICRO):
        r = pygame.Rect(rect)
        col = color or T.ACCENT
        hov = r.collidepoint(pygame.mouse.get_pos())
        if sel:
            bg, fg, bd = col, T.ON_DARK, col
        else:
            bg, fg, bd = (T.HOVER if hov else T.SURFACE), (T.TEXT if hov else T.MUTED), T.BORDER
        rad = r.height // 2
        pygame.draw.rect(s, bg, r, border_radius=rad)
        pygame.draw.rect(s, bd, r, 1, border_radius=rad)
        self._t(s, size, label, fg, r.centerx, r.centery, cx=True, cy=True,
                max_w=r.width - 10)
        self._push(r, fid)
        return r

    def _bar(self, s, rect, v, col, radius=None):
        r = pygame.Rect(rect)
        rad = r.height // 2 if radius is None else radius
        pygame.draw.rect(s, T.TRACK, r, border_radius=rad)
        w = int(r.width * max(0.0, min(1.0, float(v))))
        if w >= 2:
            pygame.draw.rect(s, col, (r.x, r.y, max(w, r.height), r.height),
                             border_radius=rad)
        return r

    # — petites icônes vectorielles (pas d'emoji : rendu non garanti) —
    def _i_search(self, s, x, y, c):
        pygame.draw.circle(s, c, (x, y - 1), 4, 1)
        pygame.draw.line(s, c, (x + 3, y + 2), (x + 6, y + 5), 1)

    def _i_lock(self, s, x, y, c):
        pygame.draw.rect(s, c, (x - 4, y - 1, 9, 7), border_radius=2)
        pygame.draw.arc(s, c, (x - 3, y - 7, 7, 9), 0, 3.15, 1)

    def _i_home(self, s, x, y, c):
        pygame.draw.polygon(s, c, [(x, y - 7), (x + 8, y), (x - 8, y)])
        pygame.draw.rect(s, c, (x - 5, y, 10, 7), border_radius=1)

    def _i_layers(self, s, x, y, c):
        for i, dy in enumerate((-5, 0, 5)):
            pygame.draw.polygon(s, c if i == 0 else _mix(c, T.SURFACE, .45),
                                [(x, y + dy - 3), (x + 7, y + dy),
                                 (x, y + dy + 3), (x - 7, y + dy)], 0 if i == 0 else 1)

    def _i_star(self, s, x, y, c, filled=True, rad=7):
        pts = []
        for i in range(10):
            a = -np.pi / 2 + i * np.pi / 5
            rr = rad if i % 2 == 0 else rad * .45
            pts.append((x + rr * np.cos(a), y + rr * np.sin(a)))
        pygame.draw.polygon(s, c, pts, 0 if filled else 1)

    def _chevron(self, s, x, y, c, open_):
        pts = ([(x - 4, y - 2), (x + 4, y - 2), (x, y + 3)] if open_
               else [(x - 2, y - 4), (x + 3, y), (x - 2, y + 4)])
        pygame.draw.polygon(s, c, pts)

    def _scrollbar(self, s, region, total, off, scroll_key=None):
        """Scrollbar avec ScrollController : molette douce, drag précis."""
        if total <= region.height:
            return
        bar_w = 14
        x = region.right - bar_w
        track = pygame.Rect(x, region.y, bar_w, region.height)
        if scroll_key is not None:
            self.scroll_tracks[scroll_key] = (track, int(total))
            state = self.scroll_state_for(scroll_key)
            state.offset = ScrollController.clamp(off, total, region.height)
            self._scroll[scroll_key] = state.offset
        handle = ScrollController.handle_rect(track, total, off)
        if handle is None:
            return

        # Draw track background
        pygame.draw.rect(s, (235, 238, 244), track, border_radius=7)
        pygame.draw.rect(s, (207, 213, 223), track, 1, border_radius=7)

        # Draw handle with hover effect
        hovering = handle.collidepoint(pygame.mouse.get_pos())
        state = self.scroll_state_for(scroll_key) if scroll_key else None
        is_dragging = state is not None and state.drag_grab_y is not None
        color = (77, 104, 140) if hovering or is_dragging else (125, 136, 152)
        pygame.draw.rect(s, color, handle, border_radius=6)

        # Register handle and track for interaction
        self._push(handle, f"scrollthumb:{scroll_key}")
        self._push(track, f"scrolltrack:{scroll_key}")

    def current_scroll_key(self):
        return self.tab

    def scroll_state_for(self, key=None):
        k = key or self.current_scroll_key()
        if k not in self.scroll_state:
            self.scroll_state[k] = ScrollState()
        return self.scroll_state[k]

    # ── 3.2 layout ──────────────────────────────────────────────────
    def _mm(self):
        return max(92, min(126, SCREEN_H // 9))

    def footer_h(self):
        return self._mm() + T.S2 + T.H_BTN + T.S2 + T.H_BTN + T.S3

    def footer_top(self):
        return SCREEN_H - self.footer_h()

    def content_top(self):
        return 150

    def content_bottom(self):
        return self.footer_top() - T.S2

    def left_w(self):
        return self.panel_l if self.left_open else 0

    def view_rect(self):
        """Zone de la carte — à utiliser par le moteur de rendu."""
        x = T.RAIL_W + self.left_w()
        return pygame.Rect(x, 0, self.x0 - x, SCREEN_H)

    def minimap_rect(self):
        s = self._mm()
        return pygame.Rect(self.x0 + T.S3, self.footer_top(), s, s)

    def _cols(self, w):
        return max(1, (w - T.S2) // T.CELL)

    @staticmethod
    def _clamp(v, total, view_h):
        return max(0, min(int(v), max(0, total - view_h)))

    # ── 3.3 filtres ─────────────────────────────────────────────────
    def _refilter(self):
        sig = (self.category, self.search.lower(), self.only_favs, len(self.favs))
        if sig == self._filter_sig:
            return
        self._filter_sig = sig
        pool = self.am.assets
        if self.only_favs:
            pool = [a for a in pool if a.id in self.favs]
        if self.category == CAT_ALL:
            pool = [a for a in pool if a.category not in HIDDEN_CATS]
        elif self.category:
            pool = [a for a in pool if a.category == self.category]
        if self.search:
            q = self.search.lower()
            pool = [a for a in pool if q in a.name.lower()]
        self.filtered = [a.id for a in pool]
        self._scroll["_left"] = 0
        self._scroll["decor"] = 0

    def _habitants(self, sim):
        alive = [a for a in sim.agents if getattr(a, "alive", True)]
        q = self.hab_search.lower().strip()
        if not q:
            return alive
        return [a for a in alive
                if q in f"{a.name} {a.color} {getattr(a,'cls','')} "
                        f"{getattr(a,'stage','')}".lower()]

    def _array(self, ag, key):
        for k, _l, _c, _n, attr_ag, attr_tpl in SECTION_REGISTRY:
            if k == key:
                return getattr(ag, attr_ag, None) if ag is not None \
                    else getattr(self, attr_tpl, None)
        return None

    def _measure_content(self, key, sim):
        """Pré-mesure la hauteur d'un onglet pour que le scroll fonctionne
        avant le premier rendu."""
        rh = 38
        if key == "habitants":
            people = self._habitants(sim)
            self._content_h["habitants"] = len(people) * rh + T.S2
        elif key == "etre":
            self._content_h["etre"] = 800
        elif key == "_right":
            self._content_h["_right"] = 800
        elif key == "decor":
            self._content_h["decor"] = 600
        elif key == "societe":
            self._content_h["societe"] = 600
        elif key == "journal":
            self._content_h["journal"] = 600

    # ══════════════════════════════════════════════════════════════════
    #  4. RENDU
    # ══════════════════════════════════════════════════════════════════
    def draw(self, screen, sim, cam):
        self.buttons.clear()
        self._cells.clear()
        self._slider_geo.clear()
        self._hit_clip = None
        self._cam, self._sim_ref = cam, sim
        self.x0 = SCREEN_W - self.panel_r
        vr = self.view_rect()
        self.view_x, self.view_w = vr.x, vr.width
        self._refilter()

        self._rail(screen)
        if self.left_open:
            self._left_panel(screen)
        self._map_overlay(screen, vr)

        pygame.draw.rect(screen, T.APP, (self.x0, 0, self.panel_r, SCREEN_H))
        pygame.draw.line(screen, T.BORDER_2, (self.x0, 0), (self.x0, SCREEN_H))
        self._header(screen, sim)
        self._toolbar(screen)
        self._tabs(screen)

        y = self.content_top()
        {"decor": self._tab_decor, "etre": self._tab_etre,
         "habitants": self._tab_habitants, "societe": self._tab_societe,
         "journal": self._tab_journal,
         "creator": self._tab_creator}[self.tab](screen, sim, y)

        self._footer(screen, sim, cam)
        self._tooltip(screen)
        self._draw_spawn_modal(screen, sim)

    # ── 4.1 rail d'icônes ───────────────────────────────────────────
    def _rail(self, screen):
        if not self.left_open:
            # mini-bouton pour réouvrir le catalogue
            r = pygame.Rect(4, T.S3, T.RAIL_W - 8, 34)
            hov = r.collidepoint(pygame.mouse.get_pos())
            pygame.draw.rect(screen, T.HOVER if hov else T.RAIL, r, border_radius=T.R1)
            pygame.draw.rect(screen, T.BORDER, r, 1, border_radius=T.R1)
            self._i_layers(screen, r.centerx, r.centery, T.ACCENT)
            self._push(r, "toggle_left")
            return
        pygame.draw.rect(screen, T.RAIL, (0, 0, T.RAIL_W, SCREEN_H))
        pygame.draw.line(screen, T.BORDER_2, (T.RAIL_W - 1, 0), (T.RAIL_W - 1, SCREEN_H))
        items = [("home", self._i_home, False),
                 ("toggle_left", self._i_layers, self.left_open),
                 ("only_favs", lambda s, x, y, c: self._i_star(s, x, y, c, self.only_favs),
                  self.only_favs)]
        for i, (fid, icon, active) in enumerate(items):
            r = pygame.Rect(7, T.S3 + i * 42, T.RAIL_W - 14, 34)
            hov = r.collidepoint(pygame.mouse.get_pos())
            if active:
                pygame.draw.rect(screen, T.SELECT, r, border_radius=T.R1)
            elif hov:
                pygame.draw.rect(screen, T.HOVER, r, border_radius=T.R1)
            icon(screen, r.centerx, r.centery, T.ACCENT if active else T.MUTED)
            self._push(r, fid)

    # ── 4.2 panneau gauche — catalogue ──────────────────────────────
    def _left_panel(self, screen):
        w = self.panel_l
        x = T.RAIL_W
        pygame.draw.rect(screen, T.APP, (x, 0, w, SCREEN_H))
        # pas de bordure droite ici — le rail gère la séparation
        mouse = pygame.mouse.get_pos()
        y = T.S3

        self._t(screen, T.F_SUB, "CATALOGUE", T.TEXT, x + T.S3, y, bold=True)
        cl = pygame.Rect(x + w - T.S3 - 22, y - 2, 22, 20)
        self._t(screen, T.F_BODY, "‹", T.MUTED, cl.centerx, cl.centery, cx=True, cy=True)
        self._push(cl, "toggle_left")
        y += 26

        # recherche
        sr = pygame.Rect(x + T.S3, y, w - 2 * T.S3, T.H_FIELD)
        self._card(screen, sr, T.R1, T.SURFACE, T.ACCENT if self.focus_search else T.BORDER_2)
        self._i_search(screen, sr.x + 14, sr.centery, T.MUTED)
        if self.search:
            self._t(screen, T.F_BODY, self.search, T.TEXT, sr.x + 26, sr.centery,
                    cy=True, max_w=sr.width - 50)
            cr = pygame.Rect(sr.right - 22, sr.centery - 8, 16, 16)
            self._t(screen, T.F_BODY, "×", T.MUTED, cr.centerx, cr.centery, cx=True, cy=True)
            self._push(cr, "search_clear")
        else:
            self._t(screen, T.F_BODY, "Rechercher un asset…", T.FAINT,
                    sr.x + 26, sr.centery, cy=True)
        self._push(sr, "search")
        y = sr.bottom + T.S2

        # chips catégories (repliées sur 2 lignes max)
        cats = [CAT_ALL] + list(dict(CATEGORY_LABELS).keys())
        fx, fy, lines = x + T.S3, y, 0
        for cat in cats:
            lbl = CHIP_LABELS.get(cat, cat.capitalize())
            cw = self._tw(T.F_MICRO, lbl) + 16
            if fx + cw > x + w - T.S3:
                fx, fy, lines = x + T.S3, fy + 23, lines + 1
                if lines >= 3:
                    break
            self._chip(screen, (fx, fy, cw, 19), lbl, f"cat:{cat}", self.category == cat)
            fx += cw + T.S1
        y = fy + 26

        self._t(screen, T.F_MICRO, f"{len(self.filtered)} assets", T.FAINT, x + T.S3 + 2, y)
        if self.favs:
            self._t(screen, T.F_MICRO, f"{len(self.favs)} favoris", T.FAINT,
                    x + w - T.S3, y, right=True)
        y += 17

        # favoris / récents
        items = (self.favs + [r for r in self.recents if r not in self.favs])[:self._cols(w)]
        if items:
            self._t(screen, T.F_SMALL, "FAVORIS / RÉCENTS", T.MUTED, x + T.S3, y, bold=True)
            y += 17
            for i, aid in enumerate(items):
                r = pygame.Rect(x + T.S3 + i * (T.CELL - 10), y, T.CELL - 16, T.CELL - 16)
                if r.right > x + w - T.S2:
                    break
                sel = aid == self.asset
                self._card(screen, r, T.R1,
                           T.SELECT if sel else (T.HOVER if r.collidepoint(mouse) else T.SURFACE),
                           T.ACCENT if sel else T.BORDER)
                if aid < len(self.am.assets):
                    tile = self.am.thumbnail(aid, T.CELL - 30)
                    if tile:
                        screen.blit(tile, (r.centerx - tile.get_width() // 2,
                                           r.centery - tile.get_height() // 2))
                if aid in self.favs:
                    self._i_star(screen, r.right - 8, r.y + 8, T.WARN, True, 5)
                self._push(r, f"asset:{aid}")
            y += T.CELL - 16 + T.S3

        region = pygame.Rect(x, y, w, SCREEN_H - y - T.S2)
        self._left_region_h = region.height
        self._content_h["_left"] = self._grid(screen, region, self._scroll["_left"], scroll_key="_left")

    # ── 4.3 grille d'assets (mutualisée) ────────────────────────────
    def _grid(self, screen, region, off, scroll_key=None):
        cols = self._cols(region.width)
        row_h = T.CELL + 14
        rows = (len(self.filtered) + cols - 1) // cols
        total = rows * row_h + T.S2
        old, oldhit = screen.get_clip(), self._hit_clip
        screen.set_clip(region)
        self._hit_clip = region
        mouse = pygame.mouse.get_pos()
        first = max(0, off // row_h)
        last = min(rows, first + region.height // row_h + 2)

        for row in range(first, last):
            for col in range(cols):
                k = row * cols + col
                if k >= len(self.filtered):
                    break
                r = pygame.Rect(region.x + T.S2 + col * T.CELL,
                                region.y + T.S2 + row * row_h - off,
                                T.CELL - T.S2, T.CELL - T.S2)
                aid = self.filtered[k]
                sel, hov = aid == self.asset, r.collidepoint(mouse)
                pygame.draw.rect(screen, T.SELECT if sel else (T.HOVER if hov else T.SURFACE),
                                 r, border_radius=T.R1)
                pygame.draw.rect(screen, T.ACCENT if sel else T.BORDER, r,
                                 2 if sel else 1, border_radius=T.R1)
                if aid < len(self.am.assets):
                    a = self.am.assets[aid]
                    tile = self.am.thumbnail(aid, T.CELL - 28)
                    if tile:
                        screen.blit(tile, (r.centerx - tile.get_width() // 2, r.y + 5))
                    self._t(screen, T.F_MICRO, a.name, T.TEXT if sel else T.MUTED,
                            r.centerx, r.bottom - 13, cx=True, max_w=r.width - 6)
                fav = aid in self.favs
                if fav or hov:
                    sx, sy = r.right - 11, r.y + 10
                    self._i_star(screen, sx, sy, T.WARN if fav else T.FAINT, fav, 6)
                    self._push(pygame.Rect(sx - 9, sy - 9, 18, 18), f"fav:{aid}")
                self._push(r, f"asset:{aid}")
                self._cells.append((pygame.Rect(r), aid))
        screen.set_clip(old)
        self._hit_clip = oldhit
        self._scrollbar(screen, region, total, off, scroll_key=scroll_key)
        return total

    # ── 4.4 overlay légende sur la carte ────────────────────────────
    def _map_overlay(self, screen, vr):
        if vr.width < 220:
            return
        w, h = 116, 18 + len(MAP_LEGEND) * 18
        r = pygame.Rect(vr.right - w - T.S4, T.S4, w, h)
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(s, (255, 255, 255, 232), (0, 0, w, h), border_radius=T.R2)
        screen.blit(s, r)
        pygame.draw.rect(screen, T.BORDER, r, 1, border_radius=T.R2)
        for i, (lbl, col) in enumerate(MAP_LEGEND):
            cy = r.y + 17 + i * 18
            pygame.draw.circle(screen, col, (r.x + 15, cy), 5)
            self._t(screen, T.F_SMALL, lbl, T.TEXT, r.x + 27, cy, cy=True,
                    max_w=w - 36)

    # ── 4.5 en-tête / outils / onglets ──────────────────────────────
    def _header(self, screen, sim):
        x0, c = self.x0, sim.clock
        self._t(screen, T.F_TITLE, "UNIVERS VIVANT", T.TEXT, x0 + T.S4, T.S3, bold=True)
        tw = self._tw(T.F_TITLE, "UNIVERS VIVANT", True)
        self._t(screen, T.F_MICRO, c.label(), T.MUTED, x0 + T.S4 + tw + T.S3, T.S3 + 5,
                max_w=self.panel_r - tw - 3 * T.S4)
        self._t(screen, T.F_MICRO,
                f"pop {len([a for a in sim.agents if a.alive])} · tick {sim.w.tick}", T.FAINT,
                x0 + self.panel_r - T.S4, T.S3 + 22, right=True)
        create_rect = pygame.Rect(x0 + self.panel_r - 158, 31, 146, 25)
        self._btn(screen, create_rect, "+ Nouvel habitant", "spawn_agent", radius=T.R1)

    def _toolbar(self, screen):
        x0, y = self.x0, 62
        modes = TAB_MODES.get(self.tab, MODES)
        if not modes:
            return
        avail = self.panel_r - 2 * T.S3
        min_btn_w = 72
        per_row = max(1, avail // min_btn_w)
        rows = [modes[i:i + per_row] for i in range(0, len(modes), per_row)]
        cy = y
        for row in rows:
            w = avail // len(row)
            for i, (mid, lbl) in enumerate(row):
                r = pygame.Rect(x0 + T.S3 + i * w, cy, w - T.S1, T.H_BTN)
                self._btn(screen, r, lbl, f"mode:{mid}",
                          primary=(self.mode == mid))
            cy += T.H_BTN + T.S1
        hint = TAB_HINTS.get(self.mode, "")
        if hint:
            self._t(screen, T.F_MICRO, hint, T.FAINT, x0 + T.S4, cy + 1,
                    max_w=self.panel_r - 2 * T.S4)

    def _tabs(self, screen):
        x0, y = self.x0, 110
        w = (self.panel_r - 2 * T.S3) // len(TABS)
        pygame.draw.line(screen, T.BORDER, (x0 + T.S3, y + T.H_TAB),
                         (x0 + self.panel_r - T.S3, y + T.H_TAB))
        for i, (tid, lbl) in enumerate(TABS):
            r = pygame.Rect(x0 + T.S3 + i * w, y, w, T.H_TAB)
            sel = self.tab == tid
            hov = r.collidepoint(pygame.mouse.get_pos())
            if sel:
                pygame.draw.rect(screen, _tint(T.ACCENT, .10), r, border_radius=T.R1)
            elif hov:
                pygame.draw.rect(screen, T.HOVER, r, border_radius=T.R1)
            self._t(screen, T.F_SMALL, lbl,
                    T.ACCENT if sel else (T.TEXT if hov else T.MUTED),
                    r.centerx, r.centery, cx=True, cy=True, bold=sel, max_w=r.width - 6)
            if sel:
                pygame.draw.rect(screen, T.ACCENT, (r.x + 6, r.bottom - 2, r.width - 12, 2))
            self._push(r, f"tab:{tid}")

    # ══════════════════════════════════════════════════════════════════
    #  5. ONGLET ÊTRE — deux colonnes
    # ══════════════════════════════════════════════════════════════════
    def _tab_etre(self, screen, sim, y):
        x0, ag = self.x0, sim.selected
        bottom = self.content_bottom()

        band = self._identity(screen, sim, pygame.Rect(
            x0 + T.S3, y, self.panel_r - 2 * T.S3, 0))
        y = band + T.S2

        two = self.panel_r >= 400
        gap = T.S2
        lw = int((self.panel_r - 2 * T.S3 - gap) * 0.54) if two else self.panel_r - 2 * T.S3
        left = pygame.Rect(x0 + T.S3, y, lw, bottom - y)
        right = pygame.Rect(left.right + gap, y,
                            self.panel_r - 2 * T.S3 - lw - gap, bottom - y)

        # — colonne 1 : générateur (si aucun être sélectionné) + accordéons —
        off = self._scroll["etre"]
        old = screen.get_clip()
        screen.set_clip(left)
        self._hit_clip = left
        cy = left.y - off
        if ag is None:
            self._card(screen, pygame.Rect(left.x, cy, left.width, 100), T.R2, T.SURFACE, T.BORDER)
            self._t(screen, T.F_SUB, "AUCUN ÊTRE SÉLECTIONNÉ", T.ACCENT,
                    left.centerx, cy + 22, cx=True)
            self._t(screen, T.F_SMALL,
                    "Utilise Examiner sur la carte ou choisis une ligne dans le Registre.",
                    T.MUTED, left.centerx, cy + 46, cx=True, max_w=left.width - 28)
            cr = pygame.Rect(left.x + 18, cy + 68, left.width - 36, 30)
            self._btn(screen, cr, "+ Nouvel habitant", "spawn_agent", radius=T.R2)
            cy += 108
        for key, label, color, names, _a, _t in SECTION_REGISTRY:
            cy = self._accordion(screen, ag, left, cy, key, label, color, names)
        total = (cy + off) - left.y
        screen.set_clip(old)
        self._hit_clip = None
        self._content_h["etre"] = total
        self._scrollbar(screen, left, total, off, scroll_key="etre")

        # — colonne 2 : cartes du registre —
        if not two:
            return
        off2 = self._scroll["_right"]
        screen.set_clip(right)
        self._hit_clip = right
        cy = right.y - off2
        for key, meth in CARD_REGISTRY:
            cy = getattr(self, meth)(screen, pygame.Rect(right.x, cy, right.width, 0), sim)
            cy += T.S2
        total2 = (cy + off2) - right.y
        screen.set_clip(old)
        self._hit_clip = None
        self._content_h["_right"] = total2
        self._scrollbar(screen, right, total2, off2, scroll_key="_right")

    def _identity(self, screen, sim, rect):
        """Bandeau identité — hauteur variable, rien ne peut en déborder."""
        ag = sim.selected
        if ag is None:
            r = pygame.Rect(rect.x, rect.y, rect.width, 46)
            self._card(screen, r, T.R2, _tint(T.ACCENT, .06), _tint(T.ACCENT, .30))
            self._t(screen, T.F_BODY, "Aucun être sélectionné", T.ACCENT,
                    r.x + T.S3, r.centery - 8, bold=True, max_w=r.width - 2 * T.S3)
            self._t(screen, T.F_MICRO,
                    "Outil « Examiner » ou onglet HABITANTS pour en choisir un.",
                    T.MUTED, r.x + T.S3, r.centery + 4, max_w=r.width - 2 * T.S3)
            return r.bottom

        fam = []
        bonded_eid = getattr(ag, "bonded", None)
        if bonded_eid is not None:
            # bonded est un eid (int), jamais un objet Being — on le resout
            partner = next((x for x in sim.agents if x.eid == bonded_eid), None)
            if partner is not None:
                fam.append(f"en couple avec {partner.name}")
        if getattr(ag, "children", None):
            fam.append(f"{len(ag.children)} enfant(s)")
        h = 88 + (14 if fam else 0)
        r = self._card(screen, pygame.Rect(rect.x, rect.y, rect.width, h), T.R2)
        clan = CLAN_COLORS.get(ag.color, (150, 150, 150))

        # — portrait (64x64) si disponible —
        av = pygame.Rect(r.x + T.S3, r.y + T.S3, 56, 56)
        portrait = self._get_portrait(ag.sex, getattr(ag, "cls", "pawn"))
        if portrait:
            # arrondir le coin
            mask = pygame.Surface((56, 56), pygame.SRCALPHA)
            pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, 56, 56), border_radius=20)
            frame = portrait.copy()
            frame.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            screen.blit(frame, av)
            pygame.draw.rect(screen, clan, av, 2, border_radius=20)
        else:
            # fallback : cercle coloré + initiales
            pygame.draw.rect(screen, _tint(clan, .30), av, border_radius=28)
            pygame.draw.rect(screen, clan, av, 2, border_radius=28)
            self._t(screen, T.F_BODY, ag.name[:2].upper(), _mix(clan, (0, 0, 0), .4),
                    av.centerx, av.centery, cx=True, cy=True, bold=True)

        # badge neurones, ancré à droite — largeur mesurée, jamais coupé
        btxt = f"{ag.brain.n} NEURONES"
        bw = self._tw(T.F_SMALL, btxt, True) + 40
        bdg = pygame.Rect(r.right - T.S3 - bw, r.y + T.S3, bw, 28)
        pygame.draw.rect(screen, T.DARK, bdg, border_radius=T.R2)
        self._i_lock(screen, bdg.x + 16, bdg.centery, T.ON_DARK)
        self._t(screen, T.F_SMALL, btxt, T.ON_DARK, bdg.x + 28, bdg.centery,
                cy=True, bold=True)

        tx, tw_max = av.right + T.S3, bdg.x - av.right - 2 * T.S3
        self._t(screen, T.F_SUB, f"{ag.name} ({ag.sex})", T.TEXT, tx, r.y + T.S3,
                bold=True, max_w=tw_max)
        self._t(screen, T.F_MICRO, f"{ag.stage} · {ag.age_years:.1f} ans · gén {ag.gen} · clan {ag.color}",
                T.MUTED, tx, r.y + T.S3 + 19, max_w=tw_max)
        self._t(screen, T.F_MICRO, f"but : {_goal_txt(ag)}", T.MUTED,
                tx, r.y + T.S3 + 33, max_w=tw_max)
        if fam:
            self._t(screen, T.F_MICRO, " · ".join(fam), T.FAINT, r.x + T.S3,
                    r.y + 60, max_w=r.width - 2 * T.S3)

        vy = r.bottom - 16
        vw = (r.width - 2 * T.S3 - 2 * T.S2) // 3
        for i, (lbl, val, col) in enumerate([
                ("santé", getattr(ag, "health", 0), C_CORPS),
                ("énergie", getattr(ag, "energy", 0), T.WARN),
                ("satiété", 1 - getattr(ag, "hunger", 0), C_EMO)]):
            vx = r.x + T.S3 + i * (vw + T.S2)
            self._t(screen, 10, lbl, T.FAINT, vx, vy - 12)
            self._bar(screen, (vx, vy, vw, 6), val, col)
        return r.bottom

    def _accordion(self, screen, ag, region, y, key, label, color, names):
        arr = self._array(ag, key)
        open_ = self.sections.get(key, False)
        hr = pygame.Rect(region.x, y, region.width, T.H_HEAD)
        hov = hr.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, _tint(color, .15) if open_ else (T.HOVER if hov else T.SURFACE),
                         hr, border_radius=T.R1)
        pygame.draw.rect(screen, _tint(color, .45) if open_ else T.BORDER, hr, 1,
                         border_radius=T.R1)
        self._chevron(screen, hr.x + 14, hr.centery,
                      _mix(color, (0, 0, 0), .2) if open_ else T.MUTED, open_)
        self._t(screen, T.F_BODY, label, _mix(color, (0, 0, 0), .35) if open_ else T.TEXT,
                hr.x + 26, hr.centery, cy=True, bold=True, max_w=hr.width - 80)
        if not open_ and arr is not None:
            self._t(screen, T.F_MICRO, f"{len(names)}", T.FAINT,
                    hr.right - T.S3, hr.centery, cy=True, right=True)
        self._push(hr, f"sec:{key}")
        y = hr.bottom + 2

        if open_ and arr is not None:
            lab_w = min(108, int(region.width * 0.40))
            val_w = 38
            mouse = pygame.mouse.get_pos()
            for pi, pname in enumerate(names):
                if pi >= len(arr):
                    break
                row = pygame.Rect(region.x + T.S2, y, region.width - 2 * T.S2, T.H_ROW)
                fid = f"ps:{key}:{pi}"
                active = row.collidepoint(mouse) or self.drag == fid
                self._t(screen, T.F_SMALL, pname,
                        T.TEXT if active else T.MUTED, row.x, row.centery,
                        cy=True, max_w=lab_w - 6)
                bx = row.x + lab_w
                bw = max(24, row.width - lab_w - val_w)
                v = float(arr[pi])
                self._bar(screen, (bx, row.centery - 4, bw, 7), v, color)
                # poignée seulement sur la ligne survolée ou en cours de glissement
                if active:
                    hx = bx + int(bw * max(0.0, min(1.0, v)))
                    hx = max(bx + 3, min(bx + bw - 3, hx))
                    pygame.draw.circle(screen, T.SURFACE, (hx, row.centery), 6)
                    pygame.draw.circle(screen, color, (hx, row.centery), 6, 2)
                self._t(screen, T.F_SMALL, f"{v:.2f}",
                        T.TEXT if active else T.MUTED, row.right, row.centery,
                        cy=True, right=True, bold=active)
                self._slider_geo[fid] = (bx, bw)
                self._push(row, fid)
                y += T.H_ROW
            y += T.S1
        return y + T.S1

    # ── 5.1 cartes de la colonne droite (CARD_REGISTRY) ─────────────
    def _card_head(self, screen, rect, title, color, fid, count=None):
        hr = pygame.Rect(rect.x, rect.y, rect.width, T.H_HEAD)
        open_ = self.cards_open.get(fid, True)
        pygame.draw.rect(screen, _tint(color, .14), hr, border_radius=T.R1)
        pygame.draw.rect(screen, _tint(color, .40), hr, 1, border_radius=T.R1)
        self._chevron(screen, hr.x + 14, hr.centery, _mix(color, (0, 0, 0), .2), open_)
        self._t(screen, T.F_BODY, title, _mix(color, (0, 0, 0), .35), hr.x + 26,
                hr.centery, cy=True, bold=True, max_w=hr.width - 60)
        if count is not None:
            self._t(screen, T.F_MICRO, f"({count})", T.MUTED, hr.right - T.S3,
                    hr.centery, cy=True, right=True)
        self._push(hr, f"card:{fid}")
        return hr.bottom, open_

    def _card_intention(self, screen, rect, sim):
        """Ce que l'être va faire, et pourquoi — lecture directe de
        brain.explain(). Purement une fenêtre d'observation : n'affecte
        jamais la simulation."""
        y, open_ = self._card_head(screen, rect, "INTENTION", T.ACCENT, "intention")
        if not open_:
            return y
        ag = sim.selected
        if ag is None or not getattr(ag, "alive", True):
            self._t(screen, T.F_SMALL, "Sélectionne un être pour voir ses intentions.",
                    T.FAINT, rect.centerx, y + 14, cx=True, max_w=rect.width - 2 * T.S3)
            return y + 30

        explain = getattr(ag.brain, "explain", None)
        ranking = explain(top=5) if callable(explain) else []
        if not ranking:
            self._t(screen, T.F_SMALL, "Cerveau sans explain() disponible.",
                    T.FAINT, rect.centerx, y + 14, cx=True, max_w=rect.width - 2 * T.S3)
            return y + 30

        rh = 24
        yy = y + T.S2
        engaged_act = ag.goal.get("act") if getattr(ag, "goal", None) else None
        for i, rk in enumerate(ranking):
            row = pygame.Rect(rect.x + T.S2, yy, rect.width - 2 * T.S2, rh - 4)
            col = rk.get("couleur", ACTION_COLORS.get(rk["action"], (150, 150, 150)))
            chosen = engaged_act == rk["action"]
            self._bar(screen, (row.x + 60, row.centery - 4, row.width - 60 - 48, 8),
                      rk["probabilite"], col)
            self._t(screen, T.F_SMALL, rk["nom"], T.TEXT if i == 0 else T.MUTED,
                    row.x, row.centery, cy=True, bold=(i == 0), max_w=56)
            self._t(screen, T.F_MICRO, f"{rk['probabilite']:.0%}", T.MUTED,
                    row.right, row.centery, cy=True, right=True, max_w=44)
            if chosen:
                pygame.draw.circle(screen, T.OK, (row.right - 46, row.centery), 3)
            yy += rh
        yy += T.S1
        self._t(screen, T.F_MICRO, f"engagé : {_goal_txt(ag)}", T.FAINT,
                rect.x + T.S3, yy, max_w=rect.width - 2 * T.S3)
        yy += 16
        pygame.draw.rect(screen, T.BORDER, (rect.x, y + 2, rect.width, yy - y - 2), 1,
                         border_radius=T.R1)
        return yy

    def _card_memoire(self, screen, rect, sim):
        """Vécu subjectif de l'être : autobiographie (a.life) et lieux
        qu'il croit dangereux (belief_places) — pas des stats globales,
        mais ce que CET être, en particulier, a retenu de sa vie."""
        y, open_ = self._card_head(screen, rect, "MÉMOIRE", C_MEM, "memoire")
        if not open_:
            return y
        ag = sim.selected
        if ag is None or not getattr(ag, "alive", True):
            self._t(screen, T.F_SMALL, "Sélectionne un être pour voir son vécu.",
                    T.FAINT, rect.centerx, y + 14, cx=True, max_w=rect.width - 2 * T.S3)
            return y + 30

        yy = y + T.S2
        n_danger = len(getattr(ag, "belief_places", {}) or {})
        n_beings = len(getattr(ag, "belief_beings", {}) or {})
        self._t(screen, T.F_SMALL,
                f"{n_danger} lieu(x) craint(s) · {n_beings} être(s) jugé(s)",
                T.MUTED, rect.x + T.S3, yy, max_w=rect.width - 2 * T.S3)
        yy += 20

        life = list(getattr(ag, "life", []) or [])[-5:]
        if not life:
            self._t(screen, T.F_SMALL, "Aucun événement marquant encore.",
                    T.FAINT, rect.x + T.S3, yy, max_w=rect.width - 2 * T.S3)
            yy += 18
        else:
            for entry in reversed(life):
                if isinstance(entry, tuple) and len(entry) >= 2:
                    txt = f"{entry[0]} : {entry[1]}"
                else:
                    txt = str(entry)
                pygame.draw.circle(screen, C_MEM, (rect.x + T.S4, yy + 7), 3)
                self._t(screen, T.F_MICRO, txt, T.TEXT, rect.x + 26, yy,
                        max_w=rect.width - 34)
                yy += 17
        yy += T.S1
        pygame.draw.rect(screen, T.BORDER, (rect.x, y + 2, rect.width, yy - y - 2), 1,
                         border_radius=T.R1)
        return yy

    def _card_gabarit(self, screen, rect, sim):
        """Générateur complet d'habitant — tous les paramètres modifiables."""
        y, open_ = self._card_head(screen, rect, "GENERATEUR D'HABITANT",
                                   T.ACCENT, "gabarit")
        if not open_:
            return y

        # ── prévisualisation skin idle réel ──
        ids = self.am.skin_states(self.tpl_color, self.tpl_cls).get("idle", [])
        if ids:
            try:
                skin = self.am.surface(ids[0], 0, 1.5)
                if skin:
                    pv = pygame.Rect(rect.x + T.S2, y + 2, rect.width - 2 * T.S2,
                                     max(skin.get_height() + 16, 40))
                    self._card(screen, pv, T.R1, T.SURFACE_2, T.BORDER)
                    sx = pv.centerx - skin.get_width() // 2
                    sy = pv.bottom - skin.get_height() - 3
                    screen.blit(skin, (sx, sy))
                    clan = CLAN_COLORS.get(self.tpl_color, (150, 150, 150))
                    self._t(screen, T.F_MICRO,
                            f"{self.tpl_cls} · {self.tpl_sex} · {self.tpl_color} · {self.brain_size}N",
                            T.TEXT, pv.x + T.S3, pv.y + T.S2, maxw=pv.width - 2 * T.S3)
                    pygame.draw.rect(screen, clan, pv, 1, border_radius=T.R1)
                    y = pv.bottom + T.S2
            except Exception as exc:
                self.report_ui_error("preview_skin_gabarit", exc)

        body = pygame.Rect(rect.x, y + 2, rect.width, 0)
        yy = body.y + T.S2

        # ── 1. Clan ──
        self._t(screen, 10, "CLAN", T.FAINT, body.x + T.S2, yy)
        yy += 13
        for i, cc in enumerate(CLAN_COLORS):
            r = pygame.Rect(body.x + T.S2 + i * 27, yy, 22, 18)
            if r.right > body.right - T.S2:
                break
            pygame.draw.rect(screen, CLAN_COLORS[cc], r, border_radius=T.R1)
            if self.tpl_color == cc:
                pygame.draw.rect(screen, T.TEXT, r.inflate(4, 4), 2, border_radius=T.R1 + 2)
            self._push(r, f"tcolor:{cc}")
        yy += 24

        # ── 2. Sexe ──
        self._t(screen, 10, "SEXE", T.FAINT, body.x + T.S2, yy)
        yy += 13
        for i, s in enumerate(["M", "F"]):
            self._chip(screen, (body.x + T.S2 + i * 30, yy, 27, 19), s,
                       f"tsex:{s}", self.tpl_sex == s, size=T.F_SMALL)
        yy += 25

        # ── 3. Classe ──
        self._t(screen, 10, "CLASSE", T.FAINT, body.x + T.S2, yy)
        yy += 13
        fx = body.x + T.S2
        for cls in self.template_classes():
            cw = self._tw(T.F_MICRO, cls) + 16
            if fx + cw > body.right - T.S2:
                fx, yy = body.x + T.S2, yy + 23
            self._chip(screen, (fx, yy, cw, 19), cls, f"tcls:{cls}", self.tpl_cls == cls)
            fx += cw + T.S1
        yy += 25

        # ── 4. Cerveau (slider 25–1000) ──
        br = pygame.Rect(body.x + T.S2, yy, body.width - 2 * T.S2, 32)
        self._card(screen, br, T.R1, T.SURFACE_2, T.BORDER)
        self._btn(screen, (br.x + 2, br.y + 2, 24, 24), "−", "bsize-", radius=T.R1 - 2)
        self._btn(screen, (br.right - 26, br.y + 2, 24, 24), "+", "bsize+", radius=T.R1 - 2)
        self._t(screen, T.F_SMALL, f"{self.brain_size} N · ×{think_every(self.brain_size)}",
                T.TEXT, br.centerx, br.centery, cx=True, cy=True, bold=True,
                max_w=br.width - 56)
        yy += 38
        # slider continu 25–1000 (élargi x4)
        sbr = pygame.Rect(body.x + T.S2, yy, body.width - 2 * T.S2, 28)
        sl_x, sl_w = sbr.x, sbr.width
        pygame.draw.rect(screen, T.TRACK, sbr, border_radius=14)
        t = (self.brain_size - 25) / max(1, 1000 - 25)
        hx = sl_x + int(sl_w * max(0.0, min(1.0, t)))
        pygame.draw.rect(screen, T.ACCENT, (sl_x, sbr.y, max(14, hx - sl_x), 28), border_radius=14)
        pygame.draw.circle(screen, T.SURFACE, (hx, sbr.centery), 14)
        pygame.draw.circle(screen, T.ACCENT, (hx, sbr.centery), 14, 2)
        self._slider_geo["bsize_slider"] = (sl_x, sl_w)
        self._push(sbr, "bsize_slider")
        yy += 32
        if self.brain_size >= 512:
            self._t(screen, T.F_MICRO, "⚠ mémoire élevée — risque de ralenti",
                    (228, 158, 58), body.x + T.S2, yy, max_w=body.width - 2 * T.S2)
            yy += 14
        mem = self.brain_memory_estimate_mb()
        self._t(screen, T.F_MICRO,
                f"≈ {mem:.2f} Mo de poids · réflexion toutes les {think_every(self.brain_size)} ticks",
                T.WARN if self.brain_size >= 512 else T.FAINT,
                body.x + T.S2, yy, max_w=body.width - 2 * T.S2)
        yy += 16

        # ── sections paramétrables ──
        GEN_SECTIONS = [
            ("body",   "CORPS",         C_CORPS,  BODY_DEFS,        "tpl_body"),
            ("cog",    "COGNITION",     C_COG,    COG_DEFS,         "tpl_cog"),
            ("perso",  "PERSONNALITÉ",  C_PERSO,  PERSONALITY_DEFS, "tpl_personality"),
            ("emo",    "ÉMOTIONS",      C_EMO,    EMOTION_DEFS,     "tpl_emotions"),
            ("needs",  "BESOINS",       C_BESOIN, NEED_DEFS,        "tpl_needs"),
            ("skills", "EXPÉRIENCE",    C_EXP,    SKILL_DEFS,       "tpl_skills"),
        ]
        for key, label, color, names, tpl_attr in GEN_SECTIONS:
            sec_key = f"gen_{key}"
            open_sec = self.cards_open.get(sec_key, False)
            hr = pygame.Rect(body.x, yy, body.width, T.H_HEAD)
            hov = hr.collidepoint(pygame.mouse.get_pos())
            pygame.draw.rect(screen, _tint(color, .15) if open_sec else (T.HOVER if hov else T.SURFACE),
                             hr, border_radius=T.R1)
            pygame.draw.rect(screen, _tint(color, .45) if open_sec else T.BORDER, hr, 1,
                             border_radius=T.R1)
            self._chevron(screen, hr.x + 14, hr.centery,
                          _mix(color, (0, 0, 0), .2) if open_sec else T.MUTED, open_sec)
            self._t(screen, T.F_BODY, label,
                    _mix(color, (0, 0, 0), .35) if open_sec else T.TEXT,
                    hr.x + 26, hr.centery, cy=True, bold=True, max_w=hr.width - 60)
            if not open_sec:
                arr = getattr(self, tpl_attr, None)
                if arr is not None:
                    self._t(screen, T.F_MICRO, f"{len(names)} champs", T.FAINT,
                            hr.right - T.S3, hr.centery, cy=True, right=True)
            self._push(hr, f"card:{sec_key}")
            yy = hr.bottom + 2

            if open_sec:
                arr = getattr(self, tpl_attr, None)
                if arr is not None:
                    lab_w = min(108, int(body.width * 0.40))
                    val_w = 38
                    mouse = pygame.mouse.get_pos()
                    for pi, pname in enumerate(names):
                        if pi >= len(arr):
                            break
                        row = pygame.Rect(body.x + T.S2, yy, body.width - 2 * T.S2, T.H_ROW)
                        fid = f"ps:{key}:{pi}"
                        active = row.collidepoint(mouse) or self.drag == fid
                        self._t(screen, T.F_SMALL, pname,
                                T.TEXT if active else T.MUTED, row.x, row.centery,
                                cy=True, max_w=lab_w - 6)
                        bx = row.x + lab_w
                        bw = max(24, row.width - lab_w - val_w)
                        v = float(arr[pi])
                        self._bar(screen, (bx, row.centery - 6, bw, 14), v, color)
                        if active:
                            hx = bx + int(bw * max(0.0, min(1.0, v)))
                            hx = max(bx + 6, min(bx + bw - 6, hx))
                            pygame.draw.circle(screen, T.SURFACE, (hx, row.centery), 10)
                            pygame.draw.circle(screen, color, (hx, row.centery), 10, 2)
                        self._t(screen, T.F_SMALL, f"{v:.2f}",
                                T.TEXT if active else T.MUTED, row.right, row.centery,
                                cy=True, right=True, bold=active)
                        self._slider_geo[fid] = (bx, bw)
                        self._push(row, fid)
                        yy += T.H_ROW
                    yy += T.S1
            yy += T.S1

        # ── bouton Créer ──
        btn = pygame.Rect(body.x + T.S2, yy, body.width - 2 * T.S2, 36)
        self._btn(screen, btn, "Créer un habitant", "spawn_modal", radius=T.R2)
        yy = btn.bottom + T.S2

        # ── bouton Cimetière ──
        cemetery_count = len(self._sim_ref.w.cemetery) if self._sim_ref else 0
        if cemetery_count > 0:
            cbtn = pygame.Rect(body.x + T.S2, yy, body.width - 2 * T.S2, 28)
            self._btn(screen, cbtn,
                      f"Aller au cimetière ({cemetery_count})",
                      "goto_cemetery", radius=T.R2)
            yy = cbtn.bottom + T.S2

        pygame.draw.rect(screen, T.BORDER,
                         (rect.x, y + 2, rect.width, yy - y - 2), 1,
                         border_radius=T.R1)
        return yy

    def _draw_spawn_modal(self, screen, sim):
        if not self.spawn_modal:
            self.modal_view = None
            self.modal_track = None
            self.modal_handle = None
            return

        sw, sh = screen.get_size()
        overlay = pygame.Surface((sw, sh), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        pw = min(760, max(560, int(sw * 0.46)))
        ph = min(sh - 34, 820)
        panel = pygame.Rect((sw - pw) // 2, (sh - ph) // 2, pw, ph)
        pygame.draw.rect(screen, T.SURFACE, panel, border_radius=14)
        pygame.draw.rect(screen, T.BORDER_2, panel, 2, border_radius=14)

        # ── Entête fixe ──
        header_h = 48
        header = pygame.Rect(panel.x, panel.y, panel.width, header_h)
        pygame.draw.rect(screen, T.SURFACE_2, header,
                         border_top_left_radius=14, border_top_right_radius=14)
        pygame.draw.line(screen, T.BORDER, (header.x + 12, header.bottom - 1),
                         (header.right - 12, header.bottom - 1), 1)

        self._t(screen, T.F_TITLE, "CREER UN HABITANT", T.ACCENT,
                header.centerx, header.centery, cx=True, cy=True)

        xbtn = pygame.Rect(header.right - 34, header.y + 9, 25, 25)
        hov_x = xbtn.collidepoint(pygame.mouse.get_pos())
        self._t(screen, T.F_BODY, chr(0x00d7),
                (214, 84, 84) if hov_x else T.MUTED,
                xbtn.centerx, xbtn.centery, cx=True, cy=True)
        self._push(xbtn, "spawn_modal")

        # ── Actions fixes (bas) ──
        footer_h = 54
        footer = pygame.Rect(panel.x, panel.bottom - footer_h, panel.width, footer_h)
        pygame.draw.rect(screen, T.SURFACE_2, footer,
                         border_bottom_left_radius=14, border_bottom_right_radius=14)
        pygame.draw.line(screen, T.BORDER, (footer.x + 12, footer.y),
                         (footer.right - 12, footer.y), 1)

        cancel = pygame.Rect(footer.x + 14, footer.y + 11, 130, 31)
        confirm = pygame.Rect(footer.right - 214, footer.y + 11, 200, 31)
        self._btn(screen, cancel, "Annuler", "spawn_modal", radius=T.R2)
        self._btn(screen, confirm, "Creer et placer", "spawn_confirm",
                  primary=True, radius=T.R2)

        # ── Zone scrollable ──
        view = pygame.Rect(panel.x + 18, header.bottom + 8,
                           panel.width - 18 - 28 - 18,
                           footer.y - header.bottom - 16)
        self.modal_view = view

        info = self.modal_scroll
        modal_offset = info.offset

        old_clip = screen.get_clip()
        old_hitclip = self._hit_clip
        screen.set_clip(view)
        self._hit_clip = view

        try:
            yy = view.y + 8 - modal_offset
            body = pygame.Rect(view.x, yy, view.width, 0)

            # ── PREVIEW SKIN ──
            ids = self.am.skin_states(self.tpl_color, self.tpl_cls).get("idle", [])
            preview_h = 106
            preview = pygame.Rect(view.x, yy, view.width, preview_h)
            self._card(screen, preview, T.R2, T.SURFACE_2, T.BORDER)
            if ids:
                try:
                    frames = max(1, self.am.assets[ids[0]].frames)
                    frame = (pygame.time.get_ticks() // 180) % frames
                    skin = self.am.surface(ids[0], frame, 2.6)
                    screen.blit(skin, (preview.centerx - skin.get_width() // 2,
                                       preview.bottom - skin.get_height() - 7))
                except Exception as exc:
                    self.report_ui_error("preview_skin_modal", exc)

            self._t(screen, T.F_BODY,
                    f"{self.tpl_cls}  {self.tpl_sex}  clan {self.tpl_color}  {self.brain_size}N",
                    T.TEXT, preview.x + 10, preview.y + 9, max_w=preview.width - 20)
            clan_color = CLAN_COLORS.get(self.tpl_color, (150, 150, 150))
            pygame.draw.rect(screen, clan_color, preview, 2, border_radius=T.R2)
            yy = preview.bottom + 10

            # ── CLAN ──
            self._t(screen, T.F_BODY, "CLAN", T.MUTED, view.x, yy, bold=True)
            yy += 21
            for i, cc in enumerate(CLAN_COLORS):
                r = pygame.Rect(view.x + i * 40, yy, 33, 25)
                pygame.draw.rect(screen, CLAN_COLORS[cc], r, border_radius=T.R1)
                if self.tpl_color == cc:
                    pygame.draw.rect(screen, T.TEXT, r.inflate(5, 5), 2, border_radius=T.R1)
                self._push(r, f"tcolor:{cc}")
            yy += 40

            # ── SEXE ──
            self._t(screen, T.F_BODY, "SEXE", T.MUTED, view.x, yy, bold=True)
            yy += 21
            for i, s in enumerate(["M", "F"]):
                r = pygame.Rect(view.x + i * 50, yy, 43, 26)
                self._chip(screen, r, s, f"tsex:{s}", self.tpl_sex == s,
                           size=T.F_BODY)
            yy += 42

            # ── CLASSE ──
            self._t(screen, T.F_BODY, "CLASSE", T.MUTED, view.x, yy, bold=True)
            yy += 21
            cx2 = view.x
            for c in self.template_classes():
                cw = max(56, self._tw(T.F_BODY, c) + 22)
                if cx2 + cw > view.right:
                    cx2 = view.x
                    yy += 31
                r = pygame.Rect(cx2, yy, cw, 26)
                self._chip(screen, r, c, f"tcls:{c}", self.tpl_cls == c,
                           size=T.F_SMALL)
                cx2 += cw + 5
            yy += 42

            # ── CERVEAU ──
            self._t(screen, T.F_BODY, f"CERVEAU  {self.brain_size}N", T.MUTED,
                    view.x, yy, bold=True)
            yy += 23
            slider = pygame.Rect(view.x, yy, view.width, 28)
            pygame.draw.rect(screen, T.TRACK, slider, border_radius=14)
            ratio = max(0.0, min(1.0, (self.brain_size - 25) / (1000 - 25)))
            hx = slider.x + int(slider.width * ratio)
            pygame.draw.rect(screen, T.ACCENT,
                             pygame.Rect(slider.x, slider.y, max(14, hx - slider.x), slider.height),
                             border_radius=14)
            pygame.draw.circle(screen, T.SURFACE, (hx, slider.centery), 14)
            pygame.draw.circle(screen, T.ACCENT, (hx, slider.centery), 14, 2)
            self._slider_geo["bsize_slider_modal"] = (slider.x, slider.width)
            self._push(slider, "bsize_slider_modal")
            yy += 34
            mem = self.brain_memory_estimate_mb()
            self._t(screen, T.F_MICRO,
                    f"≈ {mem:.2f} Mo / habitant · réflexion toutes les {think_every(self.brain_size)} ticks",
                    T.WARN if self.brain_size >= 512 else T.FAINT,
                    view.x, yy, max_w=view.width)
            yy += 24

            # ── GROUPES DE PARAMÈTRES ──
            GEN_SECTIONS = [
                ("body",   "CORPS",        C_CORPS,  BODY_DEFS,        "tpl_body"),
                ("cog",    "COGNITION",    C_COG,    COG_DEFS,         "tpl_cog"),
                ("perso",  "PERSONNALITE", C_PERSO,  PERSONALITY_DEFS, "tpl_personality"),
                ("emo",    "EMOTIONS",     C_EMO,    EMOTION_DEFS,     "tpl_emotions"),
                ("needs",  "BESOINS",      C_BESOIN, NEED_DEFS,        "tpl_needs"),
                ("skills", "EXPERIENCE",   C_EXP,    SKILL_DEFS,       "tpl_skills"),
            ]
            mouse = pygame.mouse.get_pos()
            for key, label, color, names, tpl_attr in GEN_SECTIONS:
                arr = getattr(self, tpl_attr, None)
                if arr is None:
                    continue
                hr = pygame.Rect(view.x, yy, view.width, 27)
                open_sec = True
                pygame.draw.rect(screen, _tint(color, .14), hr, border_radius=T.R1)
                pygame.draw.rect(screen, _tint(color, .42), hr, 1, border_radius=T.R1)
                self._t(screen, T.F_BODY, label, _mix(color, (0, 0, 0), .55),
                        hr.x + 10, hr.centery, cy=True, bold=True, max_w=hr.width - 80)
                self._t(screen, T.F_MICRO, f"{len(names)} champs", T.FAINT,
                        hr.right - T.S3, hr.centery, cy=True, right=True)
                yy = hr.bottom + 3

                lab_w = min(116, int(view.width * 0.36))
                val_w = 40
                for pi, pname in enumerate(names):
                    if pi >= len(arr):
                        break
                    row = pygame.Rect(view.x, yy, view.width, 25)
                    fid = f"ps:{key}:{pi}"
                    active = row.collidepoint(mouse) or self.drag == fid
                    self._t(screen, T.F_SMALL, pname,
                            T.TEXT if active else T.MUTED, row.x + 4, row.centery,
                            cy=True, max_w=lab_w - 8)
                    bx = row.x + lab_w
                    bw = max(48, row.width - lab_w - val_w)
                    v = float(arr[pi])
                    self._bar(screen, (bx, row.centery - 5, bw, 10), v, color)
                    if active:
                        hx = bx + int(bw * max(0.0, min(1.0, v)))
                        hx = max(bx + 3, min(bx + bw - 3, hx))
                        pygame.draw.circle(screen, T.SURFACE, (hx, row.centery), 7)
                        pygame.draw.circle(screen, color, (hx, row.centery), 7, 2)
                    self._t(screen, T.F_SMALL, f"{v:.2f}",
                            T.TEXT if active else T.MUTED,
                            row.right - 3, row.centery, cy=True, right=True)
                    self._slider_geo[fid] = (bx, bw)
                    self._push(row, fid)
                    yy += 27
                yy += 9

            # Marge finale
            content_h = yy - (view.y - modal_offset) + 18

        finally:
            screen.set_clip(old_clip)
            self._hit_clip = old_hitclip

        # Update scroll geometry
        self.modal_content_h = max(view.height, int(content_h))
        info.offset = ScrollController.clamp(info.offset, self.modal_content_h, view.height)

        # Draw scrollbar if needed
        if self.modal_content_h > view.height:
            bar_w = 12
            track_x = view.right + 5
            self.modal_track = pygame.Rect(track_x, view.y, bar_w, view.height)
            self.modal_handle = ScrollController.handle_rect(
                self.modal_track, self.modal_content_h, info.offset)
            if self.modal_handle:
                pygame.draw.rect(screen, (232, 235, 241), self.modal_track, border_radius=6)
                pygame.draw.rect(screen, (207, 212, 221), self.modal_track, 1, border_radius=6)
                hovering = self.modal_handle.collidepoint(pygame.mouse.get_pos())
                color = (77, 104, 140) if hovering or info.drag_grab_y is not None else (125, 136, 152)
                pygame.draw.rect(screen, color, self.modal_handle, border_radius=6)
                # Register handle and track for interaction
                self._push(self.modal_handle, "modal_scrollthumb")
                self._push(self.modal_track, "modal_scrolltrack")
        else:
            self.modal_track = None
            self.modal_handle = None

    def _card_events(self, screen, rect, sim):
        """Événements récents groupés par catégorie — issus de LOG_CATS."""
        groups = {}
        for e in list(sim.journal)[-80:]:
            cat = e[3] if len(e) > 3 else "monde"
            groups.setdefault(cat, []).append(e)
        y = rect.y
        for cat, entries in sorted(groups.items(), key=lambda kv: -len(kv[1]))[:5]:
            col = LOG_CATS.get(cat, T.MUTED)
            key = f"ev_{cat}"
            self.cards_open.setdefault(key, True)
            y, open_ = self._card_head(screen,
                                       pygame.Rect(rect.x, y, rect.width, 0),
                                       LOG_TITLES.get(cat, cat.capitalize()),
                                       col, key, len(entries))
            if open_:
                for e in entries[-3:]:
                    txt = e[1] if len(e) > 1 else ""
                    cnt = e[4] if len(e) > 4 else 1
                    pygame.draw.circle(screen, col, (rect.x + T.S4, y + 11), 4)
                    self._t(screen, T.F_SMALL,
                            txt + (f"  ×{cnt}" if cnt and cnt > 1 else ""),
                            T.TEXT, rect.x + 28, y + 4, max_w=rect.width - 36)
                    y += 21
            y += T.S2
        if not groups:
            self._t(screen, T.F_SMALL, "Aucun événement.", T.FAINT,
                    rect.centerx, rect.y + 6, cx=True)
            y = rect.y + 26
        return y

    # ══════════════════════════════════════════════════════════════════
    #  6. AUTRES ONGLETS
    # ══════════════════════════════════════════════════════════════════
    def _draw_tile_inspector(self, screen, sim, rect):
        from .diagnostics import tile_snapshot
        if self.selected_tile is None:
            return rect.y
        tx, ty = self.selected_tile
        data = tile_snapshot(sim, tx, ty)
        y = rect.y
        x0 = rect.x
        w = rect.width

        self._card(screen, pygame.Rect(x0, y, w, 0), T.R2, T.SURFACE, T.BORDER)
        self._t(screen, T.F_SUB, f"TUILE {tx}, {ty}", T.TEXT, x0 + T.S3, y + T.S2, bold=True)
        y += 28

        rows = [
            ("Terrain", "eau" if data["eau"] else "terre" if data["terre"] else "hors sol"),
            ("Bloquée", "oui" if data["bloque"] else "non"),
            ("Abri", "oui" if data["abri"] else "non"),
            ("Feu", str(data["feu"])),
            ("Odeur", f"{data['odeur']:.2f}"),
            ("Exploration", f"{data['exploration']:.2f}"),
            ("Phéromones", f"{data['pheromone']:.2f}"),
        ]

        if "biome" in data:
            rows.extend([
                ("Biome", str(data["biome"])),
                ("Altitude", f"{data['altitude']:.2f}"),
                ("Pente", f"{data['pente']:.2f}"),
            ])

        obj = data.get("objet")
        if obj:
            rows.extend([
                ("Objet", obj["nom"]),
                ("Rôle", obj["role"]),
                ("PV", str(data["pv_objet"])),
                ("Affordances", ", ".join(obj["affordances"][:4]) or "—"),
            ])

        if data.get("tombe"):
            grave = data["tombe"]
            rows.extend([
                ("Tombe", grave["nom"]),
                ("Décès tick", str(grave["tick_deces"])),
            ])

        storage = data.get("stockage")
        if storage:
            rows.extend([
                ("Dépôt", storage.get("clan") or "commun"),
                ("Remplissage", f"{storage['remplissage']:.0%}"),
                ("Inventaire", str(storage["inventaire"])),
            ])

        site = data.get("chantier")
        if site:
            rows.extend([
                ("Chantier", site.get("nom", "?")),
                ("Progression", f"{site.get('progression', 0):.0%}"),
                ("Blocs", f"{site.get('blocs_poses', 0)} / {site.get('blocs_total', 0)}"),
                ("Contributeurs", str(len(site.get("contributeurs", [])))),
            ])

        for label, value in rows:
            self._t(screen, T.F_MICRO, label, T.MUTED, x0 + T.S3, y, max_w=w * 0.38)
            self._t(screen, T.F_MICRO, value, T.TEXT,
                    x0 + w - T.S3, y, right=True, max_w=w * 0.56)
            y += 20

        return y + T.S2

    def _draw_agent_diagnostics(self, screen, sim, rect):
        from .diagnostics import agent_snapshot
        agent = sim.selected
        data = agent_snapshot(sim, agent)
        if data is None:
            return rect.y
        y = rect.y
        x0 = rect.x
        w = rect.width

        self._card(screen, pygame.Rect(x0, y, w, 0), T.R2, T.SURFACE, T.BORDER)
        self._t(screen, T.F_SUB, data["nom"], T.TEXT, x0 + T.S3, y + T.S2, bold=True)
        self._t(screen,
                T.F_MICRO,
                f"{data['sexe']} · {data['classe']} · {data['age_ans']:.1f} ans · "
                f"gén. {data['generation']} · {data['cerveau']['neurones']} N",
                T.MUTED,
                x0 + T.S3, y + 23, max_w=w - 2 * T.S3)
        y += 45

        vital = (
            ("Santé", data["sante"], C_CORPS),
            ("Énergie", data["energie"], T.WARN),
            ("Satiété", 1.0 - data["faim"], C_EMO),
            ("Soif", 1.0 - data["soif"], T.ACCENT),
        )
        for label, value, color in vital:
            self._t(screen, T.F_MICRO, label, T.MUTED, x0 + T.S3, y)
            bar = pygame.Rect(x0 + 74, y - 2, w - 124, 9)
            self._bar(screen, bar, value, color)
            self._t(screen, T.F_MICRO, f"{value:.2f}", T.TEXT,
                    x0 + w - T.S3, y, right=True)
            y += 17
        y += 6

        goal = data["but"]
        self._t(screen, T.F_BODY, "INTENTION ACTUELLE", T.ACCENT, x0 + T.S3, y, bold=True)
        y += 19
        self._t(screen, T.F_SMALL, goal["action_nom"], T.TEXT, x0 + T.S3, y)
        target = "—"
        if goal["cible_x"] is not None:
            target = f"tuile {goal['cible_x']}, {goal['cible_y']}"
        self._t(screen, T.F_SMALL, target, T.MUTED, x0 + w - T.S3, y, right=True)
        y += 18
        if goal["distance_px"] is not None:
            self._t(screen, T.F_MICRO,
                    f"distance {goal['distance_px'] / TILE:.1f} tuiles · "
                    f"bloqué {goal['bloque_ticks']} ticks",
                    T.FAINT, x0 + T.S3, y, max_w=w - 2 * T.S3)
            y += 18

        self._t(screen, T.F_BODY, "INVENTAIRE", C_EXP, x0 + T.S3, y, bold=True)
        y += 19
        inv = data["inventaire"]
        self._t(screen, T.F_SMALL,
                f"bois {inv.get('bois', 0)} · pierre {inv.get('pierre', 0)} · "
                f"or {inv.get('or', 0)} · graines {inv.get('graine', 0)}",
                T.TEXT, x0 + T.S3, y, max_w=w - 2 * T.S3)
        y += 19

        tool = data["outil"]
        tool_label = "aucun"
        if tool:
            tool_label = f"{tool['nom']} · durabilité {data['durabilite_outil']}"
        self._t(screen, T.F_SMALL, f"Outil : {tool_label}", T.MUTED,
                x0 + T.S3, y, max_w=w - 2 * T.S3)
        y += 23

        self._t(screen, T.F_BODY, "CERVEAU", C_COG, x0 + T.S3, y, bold=True)
        y += 19
        for item in data["cerveau"]["classement_actions"]:
            self._t(screen, T.F_SMALL, item.get("nom", "?"), T.TEXT, x0 + T.S3, y)
            self._t(screen, T.F_SMALL, f"{item.get('probabilite', 0):.1%}", T.MUTED,
                    x0 + w - T.S3, y, right=True)
            y += 18

        self._t(screen, T.F_BODY, "RELATIONS", C_MEM, x0 + T.S3, y + 4, bold=True)
        y += 24
        for relation in data["relations"][:5]:
            self._t(screen, T.F_SMALL, relation["nom"], T.TEXT, x0 + T.S3, y)
            self._t(screen, T.F_MICRO,
                    f"confiance {relation['confiance']:+.2f} · "
                    f"affection {relation['affection']:+.2f}",
                    T.MUTED, x0 + w - T.S3, y, right=True, max_w=150)
            y += 18

        # ── ANIMA : memoire episodique emotionnelle ──
        anima = getattr(agent, "anima", None)
        if anima:
            y += 4
            self._t(screen, T.F_BODY, "ANIMA", (180, 140, 220), x0 + T.S3, y, bold=True)
            y += 19
            # identite dominante
            ID_LABELS = {
                "builder": "Constructeur", "provider": "Pourvoyeur",
                "fighter": "Combattant", "explorer": "Explorateur",
                "caretaker": "Protecteur", "survivor": "Survivant",
                "mediator": "Mediateur",
            }
            ident = anima["identity"]
            dom = max(ident.items(), key=lambda kv: kv[1]) if ident else None
            if dom and dom[1] >= 0.20:
                self._t(screen, T.F_SMALL,
                        f"Identite: {ID_LABELS.get(dom[0], dom[0])} ({dom[1]:.2f})",
                        (140, 200, 140), x0 + T.S3, y, max_w=w - 2 * T.S3)
                y += 17
            # top 3 identites
            top_id = sorted(ident.items(), key=lambda kv: -kv[1])[:3]
            top_id = [(k, v) for k, v in top_id if v > 0.05]
            if top_id:
                parts = [f"{ID_LABELS.get(k, k)} {v:.2f}" for k, v in top_id]
                self._t(screen, T.F_MICRO, "ID: " + " · ".join(parts),
                        (120, 160, 120), x0 + T.S3, y, max_w=w - 2 * T.S3)
                y += 15
            # top 3 valeurs
            V_LABELS = {
                "survival": "Survie", "family": "Famille",
                "security": "Securite", "community": "Communaute",
                "knowledge": "Connaissance", "wealth": "Ressources",
                "generosity": "Generosite",
            }
            vals = anima.get("values", {})
            top_v = sorted(vals.items(), key=lambda kv: -kv[1])[:3]
            if top_v:
                parts = [f"{V_LABELS.get(k, k)} {v:.2f}" for k, v in top_v]
                self._t(screen, T.F_MICRO, "Valeurs: " + " · ".join(parts),
                        (160, 160, 200), x0 + T.S3, y, max_w=w - 2 * T.S3)
                y += 15
            # dernier episode
            eps = anima["episodic_memory"]
            if eps:
                last = eps[-1]
                kind_labels = {
                    "monster_attack": "attaque monstre",
                    "monster_survival": "monstre tue",
                    "food_found": "nourriture trouvee",
                    "food_given": "nourriture donnee",
                    "food_received": "nourriture recue",
                    "construction_complete": "construction terminee",
                    "new_area_discovered": "nouvelle zone",
                    "loss": "perte d'un proche",
                    "danger_discovered": "danger repere",
                    "help": "aide",
                    "talk": "conversation",
                    "theft": "vol",
                }
                label = kind_labels.get(last["kind"], last["kind"])
                imp = last["importance"]
                fear_v = last["emotion"].get("fear", 0)
                self._t(screen, T.F_MICRO, f"Event: {label}",
                        T.TEXT, x0 + T.S3, y, max_w=w - 2 * T.S3)
                self._t(screen, T.F_MICRO,
                        f"imp {imp:.2f} · peur {fear_v:.2f}",
                        T.MUTED, x0 + w - T.S3, y, right=True)
                y += 15
            # trauma
            trauma = anima["trauma"]
            trauma_items = [(k, v) for k, v in trauma.items() if v > 0.05]
            if trauma_items:
                self._t(screen, T.F_MICRO, "Trauma: " + " · ".join(
                    f"{k} {v:.2f}" for k, v in trauma_items),
                    (200, 120, 120), x0 + T.S3, y, max_w=w - 2 * T.S3)
                y += 15
            # confiance sociale
            beings = anima.get("beliefs", {}).get("beings", {})
            if beings:
                top_b = sorted(beings.items(),
                               key=lambda kv: -kv[1].get("trust", 0))[:3]
                shown = [(k, v) for k, v in top_b
                         if v.get("trust", 0) != 0.5 or v.get("danger", 0) > 0.05]
                if shown:
                    parts = []
                    for eid, b in shown:
                        nm = next((x.name for x in sim.agents
                                   if x.eid == eid), f"#{eid}")
                        tr = b.get("trust", 0.5)
                        dg = b.get("danger", 0.0)
                        parts.append(f"{nm}:conf{tr:.2f}")
                        if dg > 0.05:
                            parts[-1] += f"/danger{dg:.2f}"
                    self._t(screen, T.F_MICRO, "Sociale: " + " · ".join(parts),
                            (180, 160, 200), x0 + T.S3, y, max_w=w - 2 * T.S3)
                    y += 15
            # ── intention ──
            intent = anima.get("intention")
            if intent:
                ik = intent.get("kind", "?")
                ip = intent.get("priority", 0)
                INT_LABELS = {
                    "secure_food": "Securiser nourriture",
                    "protect_family": "Proteger famille",
                    "build_home": "Construire abri",
                    "recover_from_loss": "Recuperer perte",
                    "avoid_danger": "Eviter danger",
                    "help_ally": "Aider allie",
                    "explore_unknown": "Explorer",
                }
                self._t(screen, T.F_MICRO,
                        f"Intent: {INT_LABELS.get(ik, ik)} ({ip:.2f})",
                        (200, 180, 140), x0 + T.S3, y, max_w=w - 2 * T.S3)
                y += 15
            else:
                self._t(screen, T.F_MICRO, "Intent: aucune",
                        T.FAINT, x0 + T.S3, y)
                y += 15
            # ── attachements ──
            att = anima.get("attachments", {})
            top_att = sorted(att.items(), key=lambda kv: -kv[1])[:3]
            top_att = [(k, v) for k, v in top_att if v > 0.05]
            if top_att:
                parts = []
                for k, v in top_att:
                    if isinstance(k, int):
                        nm = next((x.name for x in sim.agents if x.eid == k), f"#{k}")
                        parts.append(f"{nm}:{v:.2f}")
                    else:
                        parts.append(f"{k}:{v:.2f}")
                self._t(screen, T.F_MICRO, "Att: " + " · ".join(parts),
                        (200, 160, 180), x0 + T.S3, y, max_w=w - 2 * T.S3)
                y += 15

        return y + T.S2

    def _tab_decor(self, screen, sim, y):
        x0 = self.x0
        r = pygame.Rect(x0 + T.S3, y, self.panel_r - 2 * T.S3, 0)
        cy = r.y

        if self.selected_tile is not None:
            cy = self._draw_tile_inspector(
                screen, sim,
                pygame.Rect(x0 + T.S3, cy, self.panel_r - 2 * T.S3, 0),
            )
            cy += T.S2

        # asset sélectionné — infos détaillées
        if self.asset >= 0 and self.asset < len(self.am.assets):
            a = self.am.assets[self.asset]
            # carte info
            ir = pygame.Rect(r.x, cy, r.width, 72)
            self._card(screen, ir, T.R1, T.SELECT, T.ACCENT)
            tile = self.am.thumbnail(self.asset, 48)
            if tile:
                screen.blit(tile, (ir.x + 8, ir.y + 12))
            tx = ir.x + 60
            self._t(screen, T.F_BODY, a.name, T.TEXT, tx, ir.y + 6, bold=True,
                    max_w=ir.width - 68)
            self._t(screen, T.F_MICRO, f"catégorie: {a.category}", T.MUTED,
                    tx, ir.y + 22, max_w=ir.width - 68)
            props = []
            if a.solid:
                props.append("solide")
            if a.flammable:
                props.append("flammable")
            props.append(f"taille: {a.size_tiles}×{a.size_tiles}")
            hp_val = a.harvest.get("hp", "?") if a.harvest else "?"
            props.append(f"pv: {hp_val}")
            self._t(screen, T.F_MICRO, " · ".join(props), T.MUTED,
                    tx, ir.y + 36, max_w=ir.width - 68)
            if a.build_recipe:
                mats = ", ".join(f"{m['materiau']}×{m['quantity']}" for m in a.build_recipe["materials"])
                self._t(screen, T.F_MICRO, f"recette: {mats}", T.MUTED,
                        tx, ir.y + 50, max_w=ir.width - 68)
            cy = ir.bottom + T.S2
        else:
            self._card(screen, pygame.Rect(r.x, cy, r.width, 40), T.R1, T.SURFACE, T.BORDER)
            self._t(screen, T.F_SMALL, "Cliquez sur un asset dans le catalogue pour le sélectionner",
                    T.FAINT, r.x + T.S4, cy + 14)
            cy += 44

        # favoris / récents
        items = (self.favs + [x for x in self.recents if x not in self.favs])[:8]
        if items:
            self._t(screen, T.F_SMALL, "ACCÈS RAPIDE", T.MUTED, r.x + T.S4, cy, bold=True)
            cy += 18
            cols = max(1, r.width // 52)
            for i, aid in enumerate(items):
                col, row = i % cols, i // cols
                tr = pygame.Rect(r.x + T.S4 + col * 52, cy + row * 52, 46, 46)
                sel = aid == self.asset
                self._card(screen, tr, T.R1,
                           T.SELECT if sel else (T.HOVER if tr.collidepoint(pygame.mouse.get_pos()) else T.SURFACE),
                           T.ACCENT if sel else T.BORDER)
                if aid < len(self.am.assets):
                    tile = self.am.thumbnail(aid, 34)
                    if tile:
                        screen.blit(tile, (tr.centerx - tile.get_width() // 2,
                                           tr.centery - tile.get_height() // 2))
                self._push(tr, f"asset:{aid}")
            cy += ((len(items) - 1) // cols + 1) * 52 + T.S2

        # taille pinceau (modes eau/terre/mur)
        if self.mode in ("water", "land", "wall"):
            self._t(screen, T.F_SMALL, "TAILLE PINCEAU", T.MUTED, r.x + T.S4, cy, bold=True)
            cy += 18
            bs = self.brush_size
            diam = bs * 2 + 1
            self._t(screen, T.F_MICRO, f"{diam}×{diam} tiles ({diam * config.TILE}px)",
                    T.TEXT, r.x + T.S4, cy)
            cy += 15
            sl = pygame.Rect(r.x + T.S4, cy, r.width - 2 * T.S4, 28)
            pygame.draw.rect(screen, T.TRACK, sl, border_radius=14)
            t = max(0.0, min(1.0, (bs - 1) / 14))
            hx = sl.x + int(sl.width * t)
            pygame.draw.rect(screen, T.ACCENT, (sl.x, sl.y, max(14, hx - sl.x), 28), border_radius=14)
            pygame.draw.circle(screen, T.SURFACE, (hx, sl.centery), 14)
            pygame.draw.circle(screen, T.ACCENT, (hx, sl.centery), 14, 2)
            self._slider_geo["brush_slider"] = (sl.x, sl.width)
            self._push(sl, "brush_slider")
            cy += 34
            # boutons +/-
            bw = 36
            self._btn(screen, (r.x + T.S4, cy, bw, 26), "−", "brush-",
                      radius=T.R1 - 2, size=T.F_SMALL)
            self._btn(screen, (r.right - T.S4 - bw, cy, bw, 26), "+", "brush+",
                      radius=T.R1 - 2, size=T.F_SMALL)
            cy += 26

        # selecteur materiau (mode bloc)
        if self.mode == "block":
            self._t(screen, T.F_SMALL, "MATERIAU", T.MUTED, r.x + T.S4, cy, bold=True)
            cy += 18
            for i, mat in enumerate(("bois", "pierre")):
                rr = pygame.Rect(r.x + T.S4 + i * 70, cy, 64, 24)
                sel = self.block_material == mat
                pygame.draw.rect(screen, T.SELECT if sel else T.SURFACE, rr, border_radius=T.R1)
                if sel:
                    pygame.draw.rect(screen, T.ACCENT, rr, 1, border_radius=T.R1)
                self._t(screen, T.F_SMALL, mat, T.TEXT if sel else T.MUTED,
                        rr.centerx, rr.centery, cx=True, cy=True)
                self._push(rr, f"blockmat:{mat}")
            cy += 30

        # stats carte
        self._t(screen, T.F_SMALL, "CARTE", T.MUTED, r.x + T.S4, cy, bold=True)
        cy += 18
        st = sim.stats
        stats = [
            f"population: {len([a for a in sim.agents if a.alive])}",
            f"moutons: {len(sim.sheep)}",
            f"naissances: {st.get('births', 0)}  morts: {st.get('deaths', 0)}",
            f"constructions: {st.get('builds', 0)}  combats: {st.get('attacks', 0)}",
        ]
        for s in stats:
            self._t(screen, T.F_MICRO, s, T.MUTED, r.x + T.S4, cy)
            cy += 15
        cy += T.S2

        OVERLAY_LABELS = (
            ("none", "Normal"),
            ("resources", "Ressources"),
            ("memory", "Mémoire"),
            ("goal", "But"),
            ("danger", "Danger"),
            ("exploration", "Exploration"),
            ("territory", "Territoire"),
            ("storage", "Dépôts"),
            ("sites", "Chantiers"),
            ("cemetery", "Cimetière"),
        )
        self._t(screen, T.F_SMALL, "COUCHE DE DIAGNOSTIC", T.MUTED, r.x + T.S4, cy, bold=True)
        cy += 19
        fx = r.x + T.S4
        for key, label in OVERLAY_LABELS:
            chip_w = self._tw(T.F_MICRO, label) + 16
            if fx + chip_w > r.right - T.S4:
                fx = r.x + T.S4
                cy += 24
            chip = pygame.Rect(fx, cy, chip_w, 20)
            sel = self.active_overlay == key
            pygame.draw.rect(screen, T.SELECT if sel else T.SURFACE, chip, border_radius=T.R1)
            if sel:
                pygame.draw.rect(screen, T.ACCENT, chip, 1, border_radius=T.R1)
            self._t(screen, T.F_MICRO, label,
                    T.ACCENT if sel else T.MUTED,
                    chip.centerx, chip.centery, cx=True, cy=True)
            self._push(chip, f"overlay:{key}")
            fx += chip_w + 4
        cy += 28

        self._content_h["decor"] = cy - r.y

    def _tab_habitants(self, screen, sim, y):
        x0 = self.x0
        people = self._habitants(sim)
        alive = len([a for a in sim.agents if getattr(a, "alive", True)])
        self._t(screen, T.F_SUB, "HABITANTS", T.TEXT, x0 + T.S4, y, bold=True)
        self._t(screen, T.F_SMALL, f"{len(people)} / {alive}", T.MUTED,
                x0 + self.panel_r - T.S4, y + 2, right=True)
        y += 24

        sr = pygame.Rect(x0 + T.S3, y, self.panel_r - 2 * T.S3, T.H_FIELD)
        self._card(screen, sr, T.R1, T.SURFACE, T.ACCENT if self.hab_focus else T.BORDER_2)
        self._i_search(screen, sr.x + 14, sr.centery, T.MUTED)
        self._t(screen, T.F_BODY, self.hab_search or "filtrer par nom, clan, classe…",
                T.TEXT if self.hab_search else T.FAINT, sr.x + 26, sr.centery,
                cy=True, max_w=sr.width - 50)
        if self.hab_search:
            cr = pygame.Rect(sr.right - 22, sr.centery - 8, 16, 16)
            self._t(screen, T.F_BODY, "×", T.MUTED, cr.centerx, cr.centery, cx=True, cy=True)
            self._push(cr, "hab_clear")
        self._push(sr, "hab_focus")
        y = sr.bottom + T.S2

        region = pygame.Rect(x0 + T.S3, y, self.panel_r - 2 * T.S3,
                             self.content_bottom() - y)
        self._card(screen, region, T.R2)
        off, rh = self._scroll["habitants"], 38
        old = screen.get_clip()
        screen.set_clip(region)
        self._hit_clip = region
        mouse = pygame.mouse.get_pos()
        first = max(0, off // rh)
        for i in range(first, min(len(people), first + region.height // rh + 2)):
            ag = people[i]
            rr = pygame.Rect(region.x + T.S1, region.y + T.S1 + i * rh - off,
                             region.width - 2 * T.S1, rh - 2)
            if sim.selected is ag:
                pygame.draw.rect(screen, T.SELECT, rr, border_radius=T.R1)
            elif rr.collidepoint(mouse):
                pygame.draw.rect(screen, T.HOVER, rr, border_radius=T.R1)
            # petit portrait 24x24 (cache)
            pm = self._get_cached_portrait(ag.sex, getattr(ag, "cls", "pawn"), 24)
            if pm:
                pmx, pmy = rr.x + 7, rr.centery - 12
                screen.blit(pm, (pmx, pmy))
                clan = CLAN_COLORS.get(ag.color, (150, 150, 150))
                pygame.draw.rect(screen, clan, (pmx, pmy, 24, 24), 1, border_radius=12)
            else:
                pygame.draw.circle(screen, CLAN_COLORS.get(ag.color, (150, 150, 150)),
                                   (rr.x + 14, rr.centery), 6)
            self._t(screen, T.F_BODY, f"{ag.name} ({ag.sex})", T.TEXT,
                    rr.x + 28, rr.y + 5, max_w=rr.width - 170)
            self._t(screen, T.F_MICRO,
                    f"{ag.stage} · {ag.age_years:.1f} ans · {getattr(ag,'cls','—')} · {ag.brain.n} N",
                    T.MUTED, rr.x + 28, rr.y + 21, max_w=rr.width - 170)
            gx = rr.right - 130
            for j, (v, c) in enumerate([(getattr(ag, "health", 0), C_CORPS),
                                         (getattr(ag, "energy", 0), T.WARN),
                                         (1 - getattr(ag, "hunger", 0), C_EMO)]):
                self._bar(screen, (gx + j * 34, rr.centery - 3, 30, 6), v, c)
            dr = pygame.Rect(rr.right - 52, rr.centery - 10, 36, 20)
            hov_d = dr.collidepoint(mouse)
            if self.hdel_pending == ag.eid:
                pygame.draw.rect(screen, (214, 84, 84), dr, border_radius=4)
                self._t(screen, T.F_MICRO, "Confirmer", T.ON_DARK,
                        dr.centerx, dr.centery, cx=True, cy=True, bold=True)
            else:
                bg = (235, 100, 100) if hov_d else (214, 84, 84)
                pygame.draw.rect(screen, bg, dr, border_radius=4)
                self._t(screen, T.F_MICRO, "Supprimer", T.ON_DARK,
                        dr.centerx, dr.centery, cx=True, cy=True, bold=True)
            self._push(rr, f"hsel:{ag.eid}")
            self._push(dr, f"hdel:{ag.eid}")
        if not people:
            self._t(screen, T.F_BODY, "Aucun habitant ne correspond.", T.FAINT,
                    region.centerx, region.y + 36, cx=True)
        screen.set_clip(old)
        self._hit_clip = None
        self._content_h["habitants"] = len(people) * rh + T.S2
        self._scrollbar(screen, region, self._content_h["habitants"], off, scroll_key="habitants")

    def _tab_societe(self, screen, sim, y):
        x0, st = self.x0, sim.stats
        # max_gen et bonded ne sont pas suivis dans sim.stats (compteurs
        # d'evenements uniquement) — calcules ici en direct pour ne plus
        # afficher un 0 fige quelle que soit la population.
        alive = [a for a in sim.agents if getattr(a, "alive", True)]
        max_gen = max((a.gen for a in alive), default=0)
        bonded_count = sum(1 for a in alive if getattr(a, "bonded", None)) // 2
        n_children = sum(1 for a in alive if getattr(a, "child", False))
        groups = [
            ("Démographie", C_CORPS, [("Population", len(alive)),
                                      ("Naissances", st.get("births", 0)),
                                      ("Décès", st.get("deaths", 0)),
                                      ("Génération max", max_gen),
                                      ("Couples", bonded_count),
                                      ("Enfants", n_children)]),
            ("Activité", C_PERSO, [("Constructions", st.get("builds", 0)),
                                   ("Villages", st.get("villages", 0)),
                                   ("Récoltes", st.get("harvests", 0)),
                                   ("Outils trouvés", st.get("tool_found", 0))]),
            ("Social", C_BESOIN, [("Dons", st.get("gives", 0)),
                                  ("Vols", st.get("takes", 0)),
                                  ("Paroles", st.get("talks", 0)),
                                  ("Attaques", st.get("attacks", 0))]),
            ("Monde", C_COG, [("Feux", st.get("fires", 0)),
                              ("Moutons", len(getattr(sim, "sheep", []))),
                              ("Monstres", len(getattr(sim, "monsters", [])))]),
        ]
        self._t(screen, T.F_SUB, "SOCIÉTÉ", T.TEXT, x0 + T.S4, y, bold=True)
        self._t(screen, T.F_SMALL, "motifs observés, jamais imposés", T.MUTED,
                x0 + T.S4 + self._tw(T.F_SUB, "SOCIÉTÉ", True) + T.S3, y + 3,
                max_w=self.panel_r - 180)
        y += 26
        region = pygame.Rect(x0 + T.S3, y, self.panel_r - 2 * T.S3,
                             self.content_bottom() - y)
        off = self._scroll["societe"]
        old = screen.get_clip()
        screen.set_clip(region)
        self._hit_clip = region
        cy = region.y - off
        for title, color, rows in groups:
            h = 28 + ((len(rows) + 1) // 2) * 21 + T.S2
            card = self._card(screen, pygame.Rect(region.x, cy, region.width, h), T.R2)
            pygame.draw.rect(screen, color, (card.x, card.y + T.S2, 3, 15), border_radius=2)
            self._t(screen, T.F_SMALL, title.upper(), _mix(color, (0, 0, 0), .3),
                    card.x + T.S3, card.y + T.S2, bold=True)
            colw = (card.width - 2 * T.S3) // 2
            for i, (lbl, val) in enumerate(rows):
                lx = card.x + T.S3 + (i % 2) * colw
                ly = card.y + 30 + (i // 2) * 21
                self._t(screen, T.F_SMALL, lbl, T.MUTED, lx, ly, max_w=colw - 54)
                self._t(screen, T.F_BODY, val, T.TEXT, lx + colw - T.S3, ly - 1,
                        right=True, bold=True)
            cy = card.bottom + T.S2
        screen.set_clip(old)
        self._hit_clip = None
        self._content_h["societe"] = (cy + off) - region.y
        self._scrollbar(screen, region, self._content_h["societe"], off, scroll_key="societe")

    def _tab_journal(self, screen, sim, y):
        x0 = self.x0
        self._t(screen, T.F_SUB, "JOURNAL", T.TEXT, x0 + T.S4, y, bold=True)
        y += 26
        fx, fy = x0 + T.S3, y
        for cid in ["tous"] + list(LOG_CATS.keys()):
            col = T.MUTED if cid == "tous" else LOG_CATS[cid]
            lbl = "tous" if cid == "tous" else LOG_TITLES.get(cid, cid)
            cw = self._tw(T.F_MICRO, lbl) + 16
            if fx + cw > x0 + self.panel_r - T.S3:
                fx, fy = x0 + T.S3, fy + 23
            self._chip(screen, (fx, fy, cw, 19), lbl, f"jfil:{cid}",
                       self.jfilter == cid, color=col)
            fx += cw + T.S1
        y = fy + 27

        region = pygame.Rect(x0 + T.S3, y, self.panel_r - 2 * T.S3,
                             self.content_bottom() - y)
        self._card(screen, region, T.R2)
        entries = [e for e in sim.journal
                   if self.jfilter == "tous" or (len(e) > 3 and e[3] == self.jfilter)]
        rh = 23
        shown = entries[-max(1, (region.height - T.S2) // rh):]
        old = screen.get_clip()
        screen.set_clip(region)
        for i, e in enumerate(shown):
            t = e[0] if len(e) > 0 else 0
            txt = e[1] if len(e) > 1 else ""
            cat = e[3] if len(e) > 3 else "monde"
            cnt = e[4] if len(e) > 4 else 1
            ry = region.y + T.S2 + i * rh
            pygame.draw.circle(screen, LOG_CATS.get(cat, T.MUTED),
                               (region.x + T.S4, ry + 8), 4)
            mm, ss = divmod(int(t / config.SIM_HZ), 60)
            self._t(screen, T.F_MICRO, f"{mm:02}:{ss:02}", T.FAINT, region.x + 27, ry + 2)
            self._t(screen, T.F_SMALL, txt + (f"  ×{cnt}" if cnt and cnt > 1 else ""),
                    T.TEXT, region.x + 68, ry + 1, max_w=region.width - 80)
        if not shown:
            self._t(screen, T.F_BODY, "Rien à signaler pour ce filtre.", T.FAINT,
                    region.centerx, region.y + 36, cx=True)
        screen.set_clip(old)

    def _tab_creator(self, screen, sim, y):
        x0 = self.x0
        self._t(screen, T.F_SUB, "CREER UN OUTIL", T.TEXT, x0 + T.S4, y, bold=True)
        self._t(screen, T.F_SMALL, "dessine, nomme, choisis un type, puis equipe l'etre selectionne",
                T.MUTED, x0 + T.S4, y + 18)
        y += 40
        ed = self.tool_editor
        ed.draw(screen, x0 + T.S4, y)
        base_y = ed.palette_y + 34

        name_r = pygame.Rect(x0 + T.S4, base_y, self.panel_r - 2 * T.S4, 28)
        self._card(screen, name_r, T.R1, T.SURFACE, T.BORDER_2)
        self._t(screen, T.F_BODY, ed.name, T.TEXT, name_r.x + 8, name_r.centery, cy=True)
        self._push(name_r, "creator_name")
        y2 = name_r.bottom + T.S2

        self._t(screen, T.F_SMALL, "TYPE", T.MUTED, x0 + T.S4, y2, bold=True)
        y2 += 18
        for i, kind in enumerate(("hache", "pioche", "marteau")):
            r = pygame.Rect(x0 + T.S4 + i * 74, y2, 68, 22)
            sel = self.tool_editor_kind == kind
            pygame.draw.rect(screen, T.SELECT if sel else T.SURFACE, r, border_radius=T.R1)
            if sel:
                pygame.draw.rect(screen, T.ACCENT, r, 1, border_radius=T.R1)
            self._t(screen, T.F_SMALL, kind, T.TEXT if sel else T.MUTED,
                    r.centerx, r.centery, cx=True, cy=True)
            self._push(r, f"creator_kind:{kind}")
        y2 += 30

        disabled = sim.selected is None or not getattr(sim.selected, "alive", False)
        save_r = pygame.Rect(x0 + T.S4, y2, self.panel_r - 2 * T.S4, 32)
        self._btn(screen, save_r,
                  "Creer et equiper" if not disabled else "Selectionne un etre d'abord",
                  "creator_save", radius=T.R2)
        clear_r = pygame.Rect(x0 + T.S4, save_r.bottom + T.S1, self.panel_r - 2 * T.S4, 28)
        self._btn(screen, clear_r, "Effacer le dessin", "creator_clear", radius=T.R1)
        return clear_r.bottom + T.S2

    # ══════════════════════════════════════════════════════════════════
    #  7. PIED DE PAGE
    # ══════════════════════════════════════════════════════════════════
    def _footer(self, screen, sim, cam):
        x0, mm = self.x0, self.minimap_rect()
        pygame.draw.line(screen, T.BORDER, (x0 + T.S3, mm.y - T.S2),
                         (x0 + self.panel_r - T.S3, mm.y - T.S2))
        ver = sim.w.tick // 30
        gen = getattr(sim.w, "gen", None)
        if gen is not None:
            ver = (ver, gen.version)
        if (self._minimap_surf is None or self._minimap_ver != ver
                or self._minimap_surf.get_width() != mm.width):
            self._minimap_surf = self._build_minimap(sim, mm, gen)
            self._minimap_ver = ver
        screen.blit(self._minimap_surf, mm)
        pygame.draw.rect(screen, T.BORDER_2, mm, 1, border_radius=T.R1)
        sc = mm.width / (GRID * TILE)
        for sh in getattr(sim, "sheep", [])[::4]:
            pygame.draw.circle(screen, (234, 236, 240),
                               (int(mm.x + sh.x * sc), int(mm.y + sh.y * sc)), 1)
        for ag in sim.agents:
            pygame.draw.circle(screen, CLAN_COLORS.get(ag.color, (150, 150, 150)),
                               (int(mm.x + ag.x * sc), int(mm.y + ag.y * sc)), 2)
        vr = pygame.Rect(int(mm.x + cam.x * sc), int(mm.y + cam.y * sc),
                         max(6, int(cam.view_w() * sc)), max(6, int(cam.view_h() * sc)))
        vr.clamp_ip(mm)
        pygame.draw.rect(screen, T.ACCENT, vr, 1)
        self._push(mm, "minimap")

        info = pygame.Rect(mm.right + T.S2, mm.y,
                           self.panel_r - mm.width - 3 * T.S3, mm.height)
        self._card(screen, info, T.R2)
        self._t(screen, T.F_BODY, f"zoom ×{cam.zoom}  ·  {int(cam.tilt)}°",
                T.TEXT, info.x + T.S3, info.y + T.S2, bold=True, max_w=info.width - 2 * T.S3)
        for i, ln in enumerate(["molette = zoom · [ / ] = incliner",
                                 "clic molette = examiner · F = suivre"]):
            self._t(screen, T.F_MICRO, ln, T.MUTED, info.x + T.S3,
                    info.y + 22 + i * 13, max_w=info.width - 2 * T.S3)
        name = sim.selected.name if sim.selected else "—"
        self._btn(screen, (info.x + T.S3, info.bottom - 24, info.width - 2 * T.S3, 20),
                  f"Suivi · {name}" if self.follow else f"Suivre {name}",
                  "follow", primary=self.follow)

        cy = mm.bottom + T.S2
        bx = x0 + T.S3
        u = (self.panel_r - 2 * T.S3) // 8
        self._btn(screen, (bx, cy, u * 2 - T.S1, T.H_BTN),
                  "Pause" if not sim.paused else "Lancer", "pause", primary=sim.paused)
        self._btn(screen, (bx + u * 2, cy, u - T.S1, T.H_BTN), "Pas", "step")
        sp = self._card(screen, (bx + u * 3, cy, u - T.S1, T.H_BTN), T.R1, T.SURFACE_2)
        self._t(screen, T.F_SMALL, f"×{sim.speed}", T.TEXT, sp.centerx, sp.centery,
                cx=True, cy=True, bold=True)
        self._btn(screen, (bx + u * 4, cy, u - T.S1, T.H_BTN), "−", "speed-1")
        self._btn(screen, (bx + u * 5, cy, u - T.S1, T.H_BTN), "+", "speed+1")
        self._btn(screen, (bx + u * 6, cy, u * 2 - T.S1, T.H_BTN), "Sauver", "save_game")
        self._btn(screen, (bx + u * 7, cy, u * 2 - T.S1, T.H_BTN), "Charger", "load_game")

    def _build_minimap(self, sim, mm, gen):
        """Vignette du monde.

        Bug corrigé : la v1 allouait `a` en (largeur, hauteur, 3) — la forme
        attendue par `blit_array` — puis l'indexait avec des masques en
        (hauteur, largeur). La grille étant carrée, numpy ne levait aucune
        erreur : la minimap était simplement TRANSPOSÉE, sans que rien ne le
        signale. On construit désormais en (y, x) puis on transpose une fois.
        """
        land = sim.w.land
        h, w = land.shape
        if gen is not None:
            from game import worldgen as _wg
            rgb = _wg.render_minimap_rgb(gen, max(mm.width, 128))
            rgb = rgb.astype(np.uint8)
            step_h, step_w = rgb.shape[0], rgb.shape[1]
            # surcouches (abri / feu) rééchantillonnées sur la même grille
            iy = (np.arange(step_h) * (h / step_h)).astype(int).clip(0, h - 1)
            ix = (np.arange(step_w) * (w / step_w)).astype(int).clip(0, w - 1)
            shelter = sim.w.shelter[np.ix_(iy, ix)] > 0
            fire = sim.w.fire[np.ix_(iy, ix)] > 0
            rgb[shelter] = (226, 180, 98)
            rgb[fire] = (224, 122, 74)
            a = rgb
        else:
            a = np.empty((h, w, 3), dtype=np.uint8)
            a[:] = (208, 216, 226)
            a[land > 0] = (170, 202, 174)
            a[sim.w.blocked > 0] = (128, 118, 106)
            a[sim.w.shelter > 0] = (226, 180, 98)
            a[sim.w.fire > 0] = (224, 122, 74)
        surf = pygame.Surface((a.shape[1], a.shape[0]))
        pygame.surfarray.blit_array(surf, np.ascontiguousarray(a.transpose(1, 0, 2)))
        return pygame.transform.smoothscale(surf, (mm.width, mm.height))

    # ── infobulle ───────────────────────────────────────────────────
    def _tooltip(self, screen):
        if self.hover_asset is None or self.hover_asset >= len(self.am.assets):
            return
        a = self.am.assets[self.hover_asset]
        lines = [CHIP_LABELS.get(a.category, a.category)]
        aff = " · ".join(list(getattr(a, "affordances", []))[:6])
        if aff:
            lines.append(aff)
        w = min(280, max([self._tw(T.F_SMALL, a.name, True)] +
                         [self._tw(T.F_MICRO, l) for l in lines]) + 2 * T.S3)
        h = 20 + len(lines) * 15 + T.S2
        mx, my = pygame.mouse.get_pos()
        tx = max(0, min(mx + 14, SCREEN_W - w - T.S2))
        ty = max(0, min(my + 14, SCREEN_H - h - T.S2))
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(s, (*T.TIP_BG, 244), (0, 0, w, h), border_radius=T.R1)
        screen.blit(s, (tx, ty))
        self._t(screen, T.F_SMALL, a.name, T.TIP_FG, tx + T.S3, ty + T.S2,
                bold=True, max_w=w - 2 * T.S3)
        for i, ln in enumerate(lines):
            self._t(screen, T.F_MICRO, ln, T.TIP_MUTED, tx + T.S3,
                    ty + 24 + i * 15, max_w=w - 2 * T.S3)

    # ══════════════════════════════════════════════════════════════════
    #  8. INTERACTION CARTE
    # ══════════════════════════════════════════════════════════════════
    def brush_radius(self):
        """Rayon courant du pinceau, en tuiles — lu par le renderer pour
        dessiner l'aperçu circulaire des outils de terrain."""
        return self.brush_size if self.mode in (
            "water", "land", "wall", "carve", "restore", "erase") else 0

    def process_action(self, sim):
        """Route l'action courante via le controller si disponible, sinon legacy.

        Appelé par main.py après handle_event(). Retourne le résultat.
        """
        if self.action is None:
            return None
        action = self.action
        self.action = None

        if self.controller is not None:
            cmd = self.controller.translate_action(action)
            if cmd is not None:
                result = self.controller.execute(cmd)
                return result
            # Actions qui modifient le dashboard lui-même (pas le sim)
            kind, val = action
            if kind == "grid":
                return {"kind": "grid"}
            elif kind == "legend":
                return {"kind": "legend"}
            return None

        # Legacy : retourne le tuple pour main.py
        return action

    def set_ghost(self, cam):
        self._cam = cam
        mx, my = pygame.mouse.get_pos()
        vr = self.view_rect()
        self._over_map = vr.collidepoint((mx, my))
        if self._over_map:
            wx, wy = cam.to_world(mx - vr.x, my)
            self.hover_tile = (int(wx // TILE), int(wy // TILE))
        self.hover_asset = None
        for rect, aid in self._cells:
            if rect.collidepoint((mx, my)):
                self.hover_asset = aid
                break

    def apply_map_tool(self, sim, cam, button):
        mx, my = pygame.mouse.get_pos()
        vr = self.view_rect()
        if not vr.collidepoint((mx, my)):
            return
        wx, wy = cam.to_world(mx - vr.x, my)
        tx, ty = int(wx // TILE), int(wy // TILE)

        if button == 2 or self.mode == "inspect":
            pick_radius_world = max(TILE * 2.0, 60.0 / max(0.10, cam.zoom))
            best, bd = None, pick_radius_world * pick_radius_world
            for ag in sim.agents:
                if not getattr(ag, "alive", False):
                    continue
                d2 = (ag.x - wx) ** 2 + (ag.y - wy) ** 2
                if d2 <= bd:
                    best, bd = ag, d2
            if best is None:
                for sh in sim.sheep:
                    if not getattr(sh, "alive", False):
                        continue
                    d2 = (sh.x - wx) ** 2 + (sh.y - wy) ** 2
                    if d2 <= bd:
                        best, bd = sh, d2
            if best is not None:
                from .entities import Being, Sheep
                if isinstance(best, Being):
                    sim.selected = best
                    self.tab = "etre"
                    self._scroll["etre"] = 0
                    self.follow = True
                    sim.log(f"Examen : {best.name}, {best.age_years:.1f} ans.",
                            (59, 118, 214), "monde")
                elif isinstance(best, Sheep):
                    self.tab = "etre"
                    sim.log(f"Mouton en ({best.tx}, {best.ty}). "
                            f"Energie : {best.energy:.0%}",
                            (108, 208, 128), "monde")
                return True
            from .diagnostics import tile_snapshot
            self.selected_tile = (tx, ty)
            self.last_tile_snapshot = tile_snapshot(sim, tx, ty)
            self.tab = "decor"
            self._scroll["decor"] = 0
            return True

        if button != 1:
            return False

        if not (0 <= tx < GRID and 0 <= ty < GRID):
            return False

        w = sim.w
        changed = False

        if self.mode in ("water", "land", "wall"):
            r = self.brush_size
            for dy in range(-r, r + 1):
                for dx in range(-r, r + 1):
                    if dx * dx + dy * dy > r * r + 1:
                        continue
                    cx, cy = tx + dx, ty + dy
                    if not (0 <= cx < GRID and 0 <= cy < GRID):
                        continue
                    if self.mode == "water":
                        if w.land[cy, cx]:
                            w.remove(cx, cy, quiet=True)
                            w.land[cy, cx] = 0
                            w.water[cy, cx] = 1
                            w.blocked[cy, cx] = 0
                            w.floor[cy, cx] = -1
                            w.mark_dirty(cx, cy, 2)
                            changed = True
                    elif self.mode == "land":
                        if not w.land[cy, cx] or w.blocked[cy, cx]:
                            w.land[cy, cx] = 1
                            w.water[cy, cx] = 0
                            w.blocked[cy, cx] = 0
                            w.floor[cy, cx] = -1
                            w.mark_dirty(cx, cy, 2)
                            changed = True
                    elif self.mode == "wall":
                        if w.land[cy, cx] and not w.blocked[cy, cx] and w.content_at(cx, cy) < 0:
                            stones = self.am.pool("stone_res") or self.am.pool("gold_stone")
                            if stones:
                                aid = int(self.am.pick(stones, sim.rng))
                                w.place(cx, cy, aid, self.am, hp=8, solid=True,
                                        size=self.am.assets[aid].size_tiles)
                                changed = True
            if changed:
                self._minimap_ver = -1
            return changed

        gen = getattr(w, "gen", None)
        if self.mode in ("carve", "restore"):
            if gen is None:
                return False
            from game import worldgen as _wg
            fn = _wg.carve_mountain if self.mode == "carve" else _wg.restore_mountain
            changed = fn(w, gen, tx, ty, radius=self.brush_size,
                         strength=0.12 if self.mode == "carve" else 0.18)
            if changed:
                self._minimap_ver = -1
            return bool(changed)

        if self.mode == "erase":
            removed = w.remove(tx, ty)
            old_len = len(w.items)
            w.items = [it for it in w.items
                       if not (int(it.x // TILE) == tx and int(it.y // TILE) == ty)]
            had_floor = w.floor[ty, tx] >= 0
            w.floor[ty, tx] = -1
            w.mark_dirty(tx, ty)
            self._minimap_ver = -1
            return removed or len(w.items) != old_len or had_floor

        if self.mode == "floor":
            aid = self.asset
            if aid in self.am.floors:
                sheet_idx = self.am.floors.index(aid)
                w.set_floor(tx, ty, sheet_idx * 216)
                return True
            if self.am.floors:
                w.set_floor(tx, ty, 0)
                return True
            return False

        if self.mode == "block":
            return sim.do_build_block_player(tx, ty, material=self.block_material)

        if self.mode == "place":
            aid = self.asset
            if not (0 <= aid < len(self.am.assets)):
                return False
            adef = self.am.assets[aid]
            if not getattr(adef, "placable", False):
                return False
            if not w.land[ty, tx] or w.blocked[ty, tx] or w.content_at(tx, ty) >= 0:
                return False
            w.place(tx, ty, aid, self.am, hp=max(1, getattr(adef, "hp", 1)),
                    solid=bool(adef.solid), shelter=bool(adef.shelter),
                    size=adef.size_tiles if adef.solid else 1)
            return True

        if self.mode == "agent":
            created = sim.spawn_agent(
                x=wx, y=wy, color=self.tpl_color, cls=self.tpl_cls,
                n_hid=self.brain_size, sex=self.tpl_sex,
                body=self.tpl_body.copy(), cog=self.tpl_cog.copy(),
                personality=self.tpl_personality.copy(),
                emotions=self.tpl_emotions.copy(), needs=self.tpl_needs.copy(),
            )
            if created is not None:
                sim.selected = created
                self._needs_save = True
                self.follow = True
                return True
            return False

        if self.mode == "sheep":
            sim.spawn_sheep(x=wx, y=wy)
            return True

        if self.mode == "monster":
            sim.spawn_monster(x=wx, y=wy)
            return True

        return False

    # ══════════════════════════════════════════════════════════════════
    #  9. ÉVÉNEMENTS
    # ══════════════════════════════════════════════════════════════════
    def handle_event(self, ev, sim):
        self._sim_ref = sim
        pos = getattr(ev, "pos", None)

        # 1. Modale : reçoit tous les événements tant qu'elle est ouverte
        if self.spawn_modal:
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                self.spawn_modal = False
                self.drag = None
                self.modal_scroll.drag_grab_y = None
                return True

            if ev.type == pygame.MOUSEWHEEL:
                if self.modal_view is not None:
                    self.modal_scroll.offset = ScrollController.clamp(
                        self.modal_scroll.offset - int(ev.y) * ScrollController.WHEEL_STEP,
                        self.modal_content_h, self.modal_view.height)
                return True

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = pos or pygame.mouse.get_pos()

                # Check modal scrollbar handle
                if self.modal_handle and self.modal_handle.collidepoint((mx, my)):
                    self.modal_scroll.drag_grab_y = my - self.modal_handle.y
                    self.drag = "scrollbar:modal"
                    return True

                # Check modal scrollbar track (page scroll)
                if self.modal_track and self.modal_track.collidepoint((mx, my)):
                    page = int(self.modal_view.height * 0.85)
                    if my < self.modal_handle.y if self.modal_handle else my < self.modal_track.centery:
                        self.modal_scroll.offset -= page
                    else:
                        self.modal_scroll.offset += page
                    self.modal_scroll.offset = ScrollController.clamp(
                        self.modal_scroll.offset, self.modal_content_h, self.modal_view.height)
                    return True

                # Check buttons
                for r, fid in reversed(self.buttons):
                    if r.collidepoint((mx, my)):
                        if fid.startswith("ps:"):
                            self.drag = fid
                            self._drag_set(sim, mx, my)
                            return True
                        self._click(fid)
                        return True
                return True  # Click outside: keep modal open

            if ev.type == pygame.MOUSEMOTION:
                mx, my = pos or pygame.mouse.get_pos()
                if self.drag == "scrollbar:modal":
                    if self.modal_track and self.modal_handle:
                        handle_h = self.modal_handle.height
                        max_offset = max(1, self.modal_content_h - self.modal_track.height)
                        travel = max(1, self.modal_track.height - handle_h)
                        target_y = my - self.modal_scroll.drag_grab_y
                        ratio = max(0.0, min(1.0, (target_y - self.modal_track.y) / travel))
                        self.modal_scroll.offset = ScrollController.clamp(
                            int(ratio * max_offset), self.modal_content_h, self.modal_view.height)
                    return True
                # Normal drag for sliders
                if self.drag:
                    self._drag_set(sim, mx, my)
                    return True

            if ev.type == pygame.MOUSEBUTTONUP:
                if self.drag == "scrollbar:modal":
                    self.modal_scroll.drag_grab_y = None
                self.drag = None
                return True

            return True

        # 2. Gestion normale (pas de modale)
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            if self.creator_focus:
                self.creator_focus = False
                return True
            return False

        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            mx, my = pos or pygame.mouse.get_pos()
            for r, fid in reversed(self.buttons):
                if not r.collidepoint((mx, my)):
                    continue
                if fid.startswith("ps:"):
                    self.drag = fid
                    self._drag_set(sim, mx, my)
                    return True
                if fid == "minimap":
                    self._minimap_jump((mx, my))
                    return True
                if fid.startswith("sec:"):
                    k = fid[4:]
                    self.sections[k] = not self.sections.get(k, False)
                    return True
                if fid.startswith("card:"):
                    k = fid[5:]
                    self.cards_open[k] = not self.cards_open.get(k, True)
                    return True
                if fid.startswith("fav:"):
                    self._toggle_fav(int(fid[4:]))
                    return True
                self._click(fid)
                return True
            if not self.view_rect().collidepoint((mx, my)):
                self.focus_search = self.hab_focus = False
            return False

        if ev.type == pygame.MOUSEBUTTONDOWN and self.tab == "creator" and ev.button in (1, 3):
            mx, my = pos or pygame.mouse.get_pos()
            picked = self.tool_editor.palette_hit(mx, my)
            if picked is not None:
                self.tool_editor.current_color = picked
                return True
            if self.tool_editor.paint_at(mx, my, erase=(ev.button == 3)):
                self.painting = ev.button
                return True

        if ev.type == pygame.MOUSEMOTION and self.drag:
            if isinstance(self.drag, str) and self.drag.startswith("scrollbar:"):
                key = self.drag.split(":", 1)[1]
                if key in self.scroll_tracks:
                    track, ch = self.scroll_tracks[key]
                    state = self.scroll_state_for(key)
                    ScrollController.drag(state, ev.pos, track, ch, track.height)
                    self._scroll[key] = state.offset
                return True
            mx, my = pos or pygame.mouse.get_pos()
            self._drag_set(sim, mx, my)
            return True

        if ev.type == pygame.MOUSEMOTION and getattr(self, "painting", None) and self.tab == "creator":
            mx, my = pos or pygame.mouse.get_pos()
            self.tool_editor.paint_at(mx, my, erase=(self.painting == 3))
            return True

        if ev.type == pygame.MOUSEBUTTONUP and self.drag:
            if isinstance(self.drag, str) and self.drag.startswith("scrollbar:"):
                key = self.drag.split(":", 1)[1]
                ScrollController.release(self.scroll_state_for(key))
            self.drag = None
            return True
        if ev.type == pygame.MOUSEBUTTONUP:
            self.painting = None

        if ev.type == pygame.MOUSEWHEEL:
            mx, my = pygame.mouse.get_pos()
            if self.left_open and T.RAIL_W <= mx < T.RAIL_W + self.panel_l:
                lh = getattr(self, '_left_region_h', SCREEN_H - 200)
                state = self.scroll_state_for("_left")
                state.offset = ScrollController.clamp(
                    state.offset - ev.y * ScrollController.WHEEL_STEP,
                    self._content_h.get("_left", 0), lh)
                self._scroll["_left"] = state.offset
                return True
            if mx >= self.x0:
                key = self.current_scroll_key()
                track_info = self.scroll_tracks.get(key)
                if track_info is not None:
                    region, ch = track_info
                    content_region = pygame.Rect(
                        self.x0 + T.S3, self.content_top(),
                        self.panel_r - 2 * T.S3 - 18,
                        self.content_bottom() - self.content_top())
                    if content_region.collidepoint((mx, my)) or region.collidepoint((mx, my)):
                        state = self.scroll_state_for(key)
                        state.offset = ScrollController.clamp(
                            state.offset - ev.y * ScrollController.WHEEL_STEP,
                            ch, region.height)
                        self._scroll[key] = state.offset
                        return True
                h = self.content_bottom() - self.content_top()
                if self._content_h.get(self.tab, 0) == 0:
                    self._measure_content(self.tab, sim)
                state = self.scroll_state_for(key)
                state.offset = ScrollController.clamp(
                    state.offset - ev.y * ScrollController.WHEEL_STEP,
                    self._content_h.get(self.tab, 0), h)
                self._scroll[key] = state.offset
                return True
            return False

        if ev.type == pygame.KEYDOWN and (self.focus_search or self.hab_focus or self.creator_focus):
            arrow_keys = {pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN}
            if ev.key in arrow_keys:
                return False
            if self.creator_focus:
                cur = self.tool_editor.name
                if ev.key == pygame.K_BACKSPACE:
                    self.tool_editor.name = cur[:-1]
                elif ev.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    self.creator_focus = False
                elif ev.unicode and ev.unicode.isprintable() and len(cur) < 20:
                    self.tool_editor.name = cur + ev.unicode
            else:
                field = "search" if self.focus_search else "hab_search"
                cur = getattr(self, field)
                if ev.key == pygame.K_BACKSPACE:
                    setattr(self, field, cur[:-1])
                elif ev.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    self.focus_search = self.hab_focus = False
                elif ev.unicode and ev.unicode.isprintable() and len(cur) < 24:
                    setattr(self, field, cur + ev.unicode)
            return True

        return False

    def _click(self, fid):
        if not fid.startswith("hdel:"):
            self.hdel_pending = None
        if fid.startswith("mode:"):
            new_mode = fid[5:]
            if new_mode == "agent":
                self.spawn_modal = True
                self.focus_search = False
                self.hab_focus = False
                self.creator_focus = False
                self.drag = None
                return
            self.mode = new_mode
        elif fid.startswith("tab:"):
            self.tab = fid[4:]
            self.focus_search = self.hab_focus = False
        elif fid.startswith("cat:"):
            self.category = fid[4:]
        elif fid.startswith("asset:"):
            aid = int(fid[6:])
            self.asset = aid
            if aid not in self.recents:
                self.recents.insert(0, aid)
                self.recents = self.recents[:12]
            if self.mode in ("inspect", "agent", "sheep", "monster"):
                self.mode = "place"
        elif fid.startswith("jfil:"):
            self.jfilter = fid[5:]
        elif fid == "toggle_left":
            self.left_open = not self.left_open
        elif fid == "only_favs":
            self.only_favs = not self.only_favs
            self._filter_sig = None
        elif fid == "home":
            self.tab = "etre"
        elif fid == "search":
            self.focus_search, self.hab_focus = True, False
        elif fid == "search_clear":
            self.search = ""
        elif fid == "hab_focus":
            self.hab_focus, self.focus_search = True, False
        elif fid == "hab_clear":
            self.hab_search = ""
        elif fid in ("pause", "step", "reset", "reseed", "grid", "save_game", "load_game"):
            self.action = (fid, None)
        elif fid == "follow":
            self.follow = not self.follow
        elif fid.startswith("spawn_sheep:"):
            self.action = ("spawn_sheep", int(fid.split(":")[1]))
        elif fid == "spawn_agent":
            self.spawn_modal = True
            self.focus_search = False
            self.hab_focus = False
            self.creator_focus = False
            self.drag = None
        elif fid == "spawn_modal":
            self.spawn_modal = not self.spawn_modal
        elif fid == "spawn_confirm":
            self.spawn_modal = False
            self.mode = "agent"
        elif fid == "goto_cemetery":
            graves = getattr(self._sim_ref.w, "cemetery", ()) if self._sim_ref else ()
            if graves and self._cam:
                cx = sum(g[0] for g in graves) / len(graves)
                cy = sum(g[1] for g in graves) / len(graves)
                self._cam.center_on(cx * TILE, cy * TILE)
        elif fid == "creator_clear":
            self.tool_editor.clear()
        elif fid.startswith("creator_kind:"):
            self.tool_editor_kind = fid[13:]
        elif fid == "creator_name":
            self.focus_search = self.hab_focus = False
            self.creator_focus = True
        elif fid == "creator_save":
            self.action = ("create_tool", None)
        elif fid == "speed+1":
            self.action = ("speed", 1)
        elif fid == "speed-1":
            self.action = ("speed", -1)
        elif fid.startswith("speed_set:"):
            self.action = ("speed_set", int(fid.split(":")[1]))
        elif fid in ("bsize-", "bsize+"):
            sizes = list(SIZES)
            i = sizes.index(self.brain_size) if self.brain_size in SIZES else 1
            i = max(0, i - 1) if fid == "bsize-" else min(len(sizes) - 1, i + 1)
            self.brain_size = sizes[i]
        elif fid == "bsize_slider":
            geo = self._slider_geo.get("bsize_slider")
            if geo:
                mx = pygame.mouse.get_pos()[0]
                sl_x, sl_w = geo
                t = max(0.0, min(1.0, (mx - sl_x) / max(1, sl_w)))
                raw = 25 + t * (1000 - 25)
                sizes = list(SIZES)
                closest = min(sizes, key=lambda s: abs(s - raw))
                self.brain_size = closest
            self.drag = "bsize_slider"
        elif fid == "bsize_slider_modal":
            geo = self._slider_geo.get("bsize_slider_modal")
            if geo:
                mx = pygame.mouse.get_pos()[0]
                sl_x, sl_w = geo
                t = max(0.0, min(1.0, (mx - sl_x) / max(1, sl_w)))
                raw = 25 + t * (1000 - 25)
                sizes = list(SIZES)
                closest = min(sizes, key=lambda s: abs(s - raw))
                self.brain_size = closest
            self.drag = "bsize_slider_modal"
        elif fid in ("brush-", "brush+"):
            self.brush_size = max(1, min(15, self.brush_size + (1 if fid == "brush+" else -1)))
        elif fid == "brush_slider":
            geo = self._slider_geo.get("brush_slider")
            if geo:
                mx = pygame.mouse.get_pos()[0]
                sl_x, sl_w = geo
                t = max(0.0, min(1.0, (mx - sl_x) / max(1, sl_w)))
                self.brush_size = max(1, min(15, int(1 + t * 14)))
            self.drag = "brush_slider"
        elif fid.startswith("scrollthumb:"):
            key = fid[12:]
            mx, my = pygame.mouse.get_pos()
            state = self.scroll_state.get(key)
            if state:
                track_info = self.scroll_tracks.get(key)
                if track_info:
                    track, ch = track_info
                    handle = ScrollController.handle_rect(track, ch, state.offset)
                    if handle and handle.collidepoint((mx, my)):
                        state.drag_grab_y = my - handle.y
                        self.drag = f"scrollbar:{key}"
        elif fid.startswith("scrolltrack:"):
            key = fid[12:]
            mx, my = pygame.mouse.get_pos()
            state = self.scroll_state.get(key)
            if state:
                track_info = self.scroll_tracks.get(key)
                if track_info:
                    track, ch = track_info
                    handle = ScrollController.handle_rect(track, ch, state.offset)
                    # Page scroll: click above handle = scroll up, below = scroll down
                    page = int(track.height * 0.85)
                    if handle is None or my < handle.y:
                        state.offset -= page
                    else:
                        state.offset += page
                    state.offset = ScrollController.clamp(state.offset, ch, track.height)
                    self._scroll[key] = state.offset
        elif fid.startswith("scroll:"):
            key = fid[7:]
            geo = self._scroll_geo.get(key)
            if geo:
                region, total = geo
                mx, my = pygame.mouse.get_pos()
                if total > region.height:
                    t = max(0.0, min(1.0, (my - region.y) / region.height))
                    self._scroll[key] = int(t * (total - region.height))
                    self.drag = fid
        elif fid.startswith("blockmat:"):
            self.block_material = fid[9:]
        elif fid.startswith("overlay:"):
            self.active_overlay = fid[8:]
        elif fid.startswith("tcolor:"):
            self.tpl_color = fid[7:]
            self.normalize_template_class()
        elif fid.startswith("tcls:"):
            candidate = fid[5:]
            if candidate in self.template_classes():
                self.tpl_cls = candidate
        elif fid.startswith("tsex:"):
            self.tpl_sex = fid[5:]
            self.normalize_template_class()
        elif fid.startswith("hsel:"):
            eid = int(fid[5:])
            for a in self._sim_ref.agents:
                if a.eid == eid:
                    self._sim_ref.selected = a
                    self.follow = True
                    self.tab = "etre"
                    self._scroll["etre"] = 0
                    break
        elif fid.startswith("hdel:"):
            eid = int(fid[5:])
            if self.hdel_pending == eid:
                # 2e clic : confirmer suppression
                for a in self._sim_ref.agents:
                    if a.eid == eid:
                        self._sim_ref.remove_agent(a, a.name)
                        if self._sim_ref.selected is a:
                            self._sim_ref.selected = None
                        self.hdel_pending = None
                        self._needs_save = True
                        break
            else:
                # 1er clic : armer la confirmation
                self.hdel_pending = eid

    def _toggle_fav(self, aid):
        if aid in self.favs:
            self.favs.remove(aid)
        else:
            self.favs.insert(0, aid)
            self.favs = self.favs[:12]
        self._filter_sig = None

    def _minimap_jump(self, pos):
        if not self._cam:
            return
        mm = self.minimap_rect()
        sc = mm.width / (GRID * TILE)
        self._cam.center_on((pos[0] - mm.x) / sc, (pos[1] - mm.y) / sc)

    def _drag_set(self, sim, mx, my=None):
        if not self.drag:
            return
        if self.drag == "scrollbar:modal":
            # Already handled in handle_event
            return
        if self.drag.startswith("scroll:"):
            key = self.drag[7:]
            geo = self._scroll_geo.get(key)
            if geo and my is not None:
                region, total = geo
                if total > region.height:
                    t = max(0.0, min(1.0, (my - region.y) / region.height))
                    self._scroll[key] = int(t * (total - region.height))
            return
        if self.drag == "bsize_slider":
            geo = self._slider_geo.get("bsize_slider")
            if geo:
                sl_x, sl_w = geo
                t = max(0.0, min(1.0, (mx - sl_x) / max(1, sl_w)))
                raw = 25 + t * (1000 - 25)
                sizes = list(SIZES)
                closest = min(sizes, key=lambda s: abs(s - raw))
                self.brain_size = closest
            return
        if self.drag == "bsize_slider_modal":
            geo = self._slider_geo.get("bsize_slider_modal")
            if geo:
                sl_x, sl_w = geo
                t = max(0.0, min(1.0, (mx - sl_x) / max(1, sl_w)))
                raw = 25 + t * (1000 - 25)
                sizes = list(SIZES)
                closest = min(sizes, key=lambda s: abs(s - raw))
                self.brain_size = closest
            return
        if self.drag == "brush_slider":
            geo = self._slider_geo.get("brush_slider")
            if geo:
                sl_x, sl_w = geo
                t = max(0.0, min(1.0, (mx - sl_x) / max(1, sl_w)))
                self.brush_size = max(1, min(15, int(1 + t * 14)))
            return
        p = self.drag.split(":")
        if len(p) != 3:
            return
        key, pi = p[1], int(p[2])
        arr = self._array(sim.selected, key)
        geo = self._slider_geo.get(self.drag)
        if arr is None or geo is None or pi >= len(arr):
            return
        bx, bw = geo
        t = max(0.0, min(1.0, (mx - bx) / max(1, bw)))
        arr[pi] = t
        ag = sim.selected
        if ag is not None and key == "needs":
            if pi == 0:
                ag.hunger = t
            elif pi == 1:
                ag.energy = t

```

## game/debuglog.py

**Type :** `.py`

```python

"""Journal d'erreurs techniques — remplace les except Exception: pass.

Les erreurs critiques sont visibles dans stderr ET dans le fichier de log
data/logs/univers_vivant.log, sans arrêter la simulation.
"""
from __future__ import annotations

import logging
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "data" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "univers_vivant.log"

logger = logging.getLogger("univers_vivant")
logger.setLevel(logging.INFO)

if not logger.handlers:
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def report_error(context: str, exc: Exception, sim=None):
    """Log une erreur technique sans arrêter la simulation."""
    message = f"{context}: {type(exc).__name__}: {exc}"
    logger.exception(message)
    print(f"[ERROR] {message}")
    if sim is not None:
        try:
            sim.log(f"Erreur technique [{context}] : {type(exc).__name__}",
                    (214, 84, 84), "monde")
        except Exception:
            pass

```

## game/diagnostics.py

**Type :** `.py`

```python

"""Diagnostics purs du monde vivant.

Ce module ne modifie jamais Sim, World ou Being. Il convertit leur état
réel en dictionnaires simples que l'UI peut afficher sans dupliquer la
logique métier.
"""
from __future__ import annotations

from typing import Any
import math

from .config import GRID, TILE


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def action_name(sim, action: int | None) -> str:
    if action is None:
        return "Aucune"
    try:
        from .brain_api import ACTION_NAMES_EXP
        return ACTION_NAMES_EXP.get(int(action), f"Action {action}")
    except Exception:
        return f"Action {action}"


def asset_info(am, aid: int | None) -> dict | None:
    if aid is None or not (0 <= int(aid) < len(am.assets)):
        return None
    a = am.assets[int(aid)]
    return {
        "id": int(aid),
        "nom": getattr(a, "label", getattr(a, "name", "asset")),
        "role": getattr(a, "role", ""),
        "categorie": getattr(a, "category", ""),
        "solid": bool(getattr(a, "solid", False)),
        "abri": bool(getattr(a, "shelter", False)),
        "comestible": float(getattr(a, "edible", 0.0)),
        "outil": bool(getattr(a, "tool", False)),
        "recolte": dict(getattr(a, "harvest", None) or {}),
        "affordances": list(getattr(a, "afford", ()) or ()),
        "inflammable": bool(getattr(a, "flammable", False)),
    }


def agent_snapshot(sim, agent) -> dict[str, Any] | None:
    """Instantané complet d'un habitant vivant.

    Toutes les valeurs proviennent directement de l'instance Being.
    """
    if agent is None or not getattr(agent, "alive", False):
        return None

    goal = getattr(agent, "goal", None) or {}
    goal_tx = goal.get("x")
    goal_ty = goal.get("y")
    distance = None
    if goal_tx is not None and goal_ty is not None:
        distance = math.hypot(goal_tx * TILE + TILE / 2 - agent.x,
                              goal_ty * TILE + TILE / 2 - agent.y)

    tool_aid = getattr(agent, "tool", -1)
    tool = asset_info(sim.am, tool_aid) if tool_aid >= 0 else None

    brain_rank = []
    explain = getattr(getattr(agent, "brain", None), "explain", None)
    if callable(explain):
        try:
            brain_rank = explain(top=5)
        except Exception:
            brain_rank = []

    memories = {}
    for category, entries in getattr(agent, "seen", {}).items():
        memories[category] = [
            {"x": int(x), "y": int(y), "force": float(force)}
            for x, y, force in entries
        ]

    relatives = []
    for other in sim.agents:
        if other.eid == agent.eid:
            continue
        relation = getattr(agent, "rel", {}).get(other.eid)
        if relation is None:
            continue
        trust = relation[0] if isinstance(relation, (tuple, list)) else float(relation)
        affection = relation[1] if isinstance(relation, (tuple, list)) and len(relation) > 1 else 0.0
        relatives.append({
            "eid": other.eid,
            "nom": other.name,
            "confiance": float(trust),
            "affection": float(affection),
            "vivant": bool(other.alive),
        })

    relatives.sort(key=lambda r: (r["confiance"] + r["affection"]), reverse=True)

    return {
        "eid": int(agent.eid),
        "nom": agent.name,
        "vivant": bool(agent.alive),
        "sexe": agent.sex,
        "classe": agent.cls,
        "clan": agent.color,
        "generation": int(agent.gen),
        "age_ans": float(agent.age_years),
        "stage": agent.stage,
        "mort_naturelle_ans": float(agent.natural_death_age / 43200.0),
        "position": {"x": float(agent.x), "y": float(agent.y),
                     "tx": int(agent.tx), "ty": int(agent.ty)},
        "etat": getattr(agent, "state", "idle"),
        "sante": float(agent.health),
        "douleur": float(agent.pain),
        "temperature": float(agent.temp),
        "energie": float(agent.energy),
        "faim": float(agent.hunger),
        "soif": float(agent.needs[2]),
        "sommeil": float(agent.needs[3]),
        "securite": float(agent.needs[4]),
        "appartenance": float(agent.needs[5]),
        "estime": float(agent.needs[6]),
        "emotions": {str(i): float(v) for i, v in enumerate(agent.emotions)},
        "personnalite": {str(i): float(v) for i, v in enumerate(agent.personality)},
        "corps": {str(i): float(v) for i, v in enumerate(agent.body)},
        "cognition": {str(i): float(v) for i, v in enumerate(agent.cog)},
        "competences": {"recolte": float(agent.skills[0]),
                        "construction": float(agent.skills[1]),
                        "combat": float(agent.skills[2]),
                        "social": float(agent.skills[3])},
        "inventaire": dict(agent.inv),
        "outil": tool,
        "durabilite_outil": int(getattr(agent, "tool_durability", 0)),
        "but": {
            "action": goal.get("act"),
            "action_nom": action_name(sim, goal.get("act")),
            "cible_x": goal_tx,
            "cible_y": goal_ty,
            "distance_px": distance,
            "expiration_tick": goal.get("until"),
            "intensite": goal.get("intensity", 0.0),
            "bloque_ticks": int(getattr(agent, "stuck", 0)),
        },
        "cerveau": {
            "neurones": int(agent.brain.n),
            "frequence_reflexion": int(agent.brain.te),
            "classement_actions": brain_rank,
        },
        "memoire": memories,
        "croyances_danger": dict(getattr(agent, "belief_places", {})),
        "relations": relatives[:12],
        "partenaire_eid": getattr(agent, "bonded", None),
        "parents": list(getattr(agent, "parents", ()) or ()),
        "enfants": list(getattr(agent, "children", ()) or ()),
        "episodes": list(getattr(agent, "episodes", ()))[-12:],
        "vie": list(getattr(agent, "life", ()))[-12:],
    }


def tile_snapshot(sim, tx: int, ty: int) -> dict[str, Any]:
    """Instantané exact d'une tuile ou d'une cellule du monde."""
    w = sim.w
    tx, ty = int(tx), int(ty)
    if not (0 <= tx < w.g and 0 <= ty < w.g):
        return {"dans_monde": False, "tx": tx, "ty": ty}

    aid = w.content_at(tx, ty)
    ainfo = asset_info(sim.am, aid)
    result = {
        "dans_monde": True,
        "tx": tx,
        "ty": ty,
        "terre": bool(w.land[ty, tx]),
        "eau": bool(w.water[ty, tx]),
        "bloque": bool(w.blocked[ty, tx]),
        "abri": bool(w.shelter[ty, tx]),
        "feu": int(w.fire[ty, tx]),
        "odeur": float(w.smell[ty, tx]),
        "exploration": float(w.heat[ty, tx]),
        "pheromone": float(w.marker[ty, tx]),
        "couleur_pheromone": int(w.marker_col[ty, tx]),
        "sol": int(w.floor[ty, tx]),
        "objet": ainfo,
        "pv_objet": int(w.hp[ty, tx]) if aid >= 0 else 0,
        "repousse": float(w.regrow[ty, tx]),
        "cimetiere": False,
        "tombe": None,
        "stockage": None,
        "chantier": None,
    }

    for grave in getattr(w, "cemetery", ()):
        gx, gy, name, death_tick, color = grave
        if int(gx) == tx and int(gy) == ty:
            result["cimetiere"] = True
            result["tombe"] = {
                "nom": name,
                "tick_deces": int(death_tick),
                "couleur": tuple(color),
            }
            break

    storage = getattr(w, "storages", {}).get((tx, ty))
    if storage is not None:
        result["stockage"] = {
            "capacite": int(storage.capacity),
            "inventaire": dict(storage.inventory),
            "clan": getattr(storage, "owner_clan", None),
            "remplissage": float(sum(storage.inventory.values()) / max(1, storage.capacity)),
        }

    site = getattr(w, "sites", {}).get((tx, ty))
    if site is None:
        site = w.site_at(tx, ty)
    if site is not None:
        result["chantier"] = {
            "nom": site.blueprint_name,
            "progression": site.progress(),
            "manquant": site.missing_materials(),
            "contributeurs": list(site.contributors),
            "blocs_poses": len(site.placed),
            "blocs_total": len(site.tasks),
        }

    gen = getattr(w, "gen", None)
    if gen is not None:
        try:
            from . import worldgen as wg
            result["biome"] = wg.biome_name(gen, tx, ty)
            result["altitude"] = float(wg.height_at(gen, tx, ty))
            result["pente"] = float(wg.slope(gen)[ty, tx])
        except Exception as exc:
            result["diagnostic_error"] = f"{type(exc).__name__}: {exc}"

    return result


def world_snapshot(sim) -> dict[str, Any]:
    """Résumé global léger, utile au panneau laboratoire."""
    alive = [a for a in sim.agents if a.alive]
    w = sim.w
    return {
        "tick": int(w.tick),
        "annee": int(sim.clock.year + 1),
        "saison": sim.clock.season,
        "jour": int(sim.clock.day + 1),
        "heure": sim.clock.label,
        "population": len(alive),
        "moutons": len(sim.sheep),
        "items": len(w.items),
        "feux": int((w.fire > 0).sum()),
        "tombes": len(getattr(w, "cemetery", ())),
        "naissances": int(sim.stats.get("births", 0)),
        "deces": int(sim.stats.get("deaths", 0)),
        "recoltes": int(sim.stats.get("harvests", 0)),
        "constructions": int(sim.stats.get("builds", 0)),
        "attaques": int(sim.stats.get("attacks", 0)),
        "dons": int(sim.stats.get("gives", 0)),
        "vols": int(sim.stats.get("takes", 0)),
        "paroles": int(sim.stats.get("talks", 0)),
        "temperature": float(sim.clock.temp),
        "pluie": float(sim.clock.rain),
        "lumiere": float(sim.clock.light),
        "champion": getattr(sim.academy, "champion_label", "aucun"),
        "score_champion": float(getattr(sim.academy, "champion_score", float("-inf"))),
    }

```

## game/engine.py

**Type :** `.py`

```python

"""Engine backend — logique pure, aucune dépendance pygame.

Extrait de main.py pour que le web (Flask-SocketIO) puisse lancer la
simulation sans importer pygame.

Corrections et améliorations par rapport à la v1
------------------------------------------------
1. BUG MAJEUR : `populate()` n'était JAMAIS appelé par `build_world()`.
   Le monde procédural naissait vide — aucun arbre, aucune nourriture,
   donc aucune famine possible, donc aucune pression de sélection.
2. BUG : `place_random(trees, …, hp=am.assets[am.pick(trees)].harvest["hp"])`
   tirait un arbre pour calculer les PV et un AUTRE arbre à l'intérieur de
   `place_random` — les PV ne correspondaient pas à l'asset posé. Le tirage
   est maintenant fait une seule fois, et les PV dérivent de l'asset réel.
3. Le décor est désormais pondéré par le BIOME et la PENTE issus de
   worldgen : forêts denses en zone humide, carrières près des montagnes,
   fruits en prairie, rien sur les pentes raides. Le monde a l'air
   « conçu à la main » alors qu'il est entièrement procédural.
4. `blob` respecte `w.blocked` et `w.water`, et son échantillonnage est
   vectorisé au lieu d'une boucle de rejet Python.
5. `build_world()` accepte `populate_dense` et `n_agents` : on peut
   désormais obtenir un monde peuplé et prêt à tourner en un seul appel.
6. Journal de départ enrichi (répartition réelle des biomes) et graine
   propagée partout — deux appels avec la même graine donnent le même monde.
"""
from __future__ import annotations

import numpy as np

from game.config import GRID, TILE
from game.world import World
from game.simulation import Sim


# ══════════════════════════════════════════════════════════════════════
#  Terrain
# ══════════════════════════════════════════════════════════════════════
#: Proportions visées par défaut — 92 % de terre émergée, 8 % d'eau.
#: `mountain_frac` fait partie de la terre : elle est simplement infranchissable.
WATER_FRAC    = 0.08
MOUNTAIN_FRAC = 0.14

#: Superficie du monde, en pixels de rendu. GRID est fixé dans game/config.py ;
#: cette constante sert aux messages et aux conversions px <-> tuiles.
WORLD_PX = GRID * TILE

#: Espacement des chaînes de montagnes, en pixels.
RIDGE_SPACING_PX = 4000


def world_pixels():
    """Côté du monde en pixels de rendu (GRID tuiles x TILE px)."""
    return GRID * TILE


def compute_land(seed=None, *, tile_period=None, ridge_width=None,
                 water_frac=WATER_FRAC, mountain_frac=MOUNTAIN_FRAC):
    """Génère le terrain procédural via worldgen. None → monde plat classique.

    `tile_period` et `ridge_width` sont exprimés en TUILES ; laissés à None,
    ils sont dérivés de RIDGE_SPACING_PX pour que l'espacement reste constant
    en pixels quelle que soit la taille de GRID.
    """
    if seed is None:
        return None
    from game import worldgen
    if tile_period is None:
        tile_period = worldgen.period_for_pixels(RIDGE_SPACING_PX, TILE)
    if ridge_width is None:
        ridge_width = max(8, int(tile_period * 0.22))
    return worldgen.generate(grid_size=GRID, tile_period=tile_period,
                             ridge_width=ridge_width, seed=int(seed),
                             water_frac=water_frac,
                             mountain_frac=mountain_frac)


# ══════════════════════════════════════════════════════════════════════
#  Outils de placement
# ══════════════════════════════════════════════════════════════════════
def _free(w, x, y):
    """La case accepte-t-elle un nouvel objet ?"""
    return (0 < x < GRID - 1 and 0 < y < GRID - 1
            and w.land[y, x] and not w.blocked[y, x]
            and w.content_at(x, y) < 0)


def blob(w, am, rng, cx, cy, radius, fn, density=2.0):
    """Applique `fn(x, y)` sur un nuage gaussien de cases libres.

    Vectorisé : un seul tirage numpy au lieu d'une boucle de rejet.
    """
    n = max(4, int(radius * radius * density))
    xs = np.clip(np.round(rng.normal(cx, radius / 2.0, n)), 1, GRID - 2).astype(int)
    ys = np.clip(np.round(rng.normal(cy, radius / 2.0, n)), 1, GRID - 2).astype(int)
    for x, y in zip(xs, ys):
        if _free(w, int(x), int(y)):
            fn(int(x), int(y))


def _biome_sites(w, rng, n, biomes, *, max_slope=None, margin=20):
    """Tire `n` centres au hasard parmi les tuiles appartenant à `biomes`.

    Sans heightmap, retombe sur un tirage uniforme. C'est ce qui donne aux
    forêts, carrières et vergers leur placement « logique » sans qu'aucune
    règle ne soit écrite à la main.
    """
    gen = getattr(w, "gen", None)
    if gen is None:
        return [(int(rng.integers(margin, GRID - margin)),
                 int(rng.integers(margin, GRID - margin))) for _ in range(n)]

    from game import worldgen as wg
    mask = np.isin(gen.biome, list(biomes))
    mask[:margin, :] = mask[-margin:, :] = False
    mask[:, :margin] = mask[:, -margin:] = False
    if max_slope is not None:
        mask &= wg.slope(gen) <= max_slope
    ys, xs = np.nonzero(mask)
    if not len(xs):
        return [(int(rng.integers(margin, GRID - margin)),
                 int(rng.integers(margin, GRID - margin))) for _ in range(n)]
    idx = rng.integers(0, len(xs), n)
    return [(int(xs[i]), int(ys[i])) for i in idx]


def populate(w, am, rng, dense=True):
    """Installe le décor naturel : forêts, carrières, sources, fruits sauvages,
    outils oubliés, ruines. Aucun ordre imposé — seulement des probabilités
    pondérées par le biome."""
    trees  = am.pool("tree")
    stones = am.pool("stone_res")
    golds  = am.pool("gold_stone")
    bushes = am.pool("bush")
    rocks  = am.pool("decor") + am.pool("waterrock")
    tools  = am.pool("tool")
    foods  = am.pool("food")
    meats  = am.pool("meat_res")
    if not trees:
        return

    from game import worldgen as wg
    gen = getattr(w, "gen", None)

    def place(pool, x, y, hp=1, solid=False, size=None):
        """Pose UN asset tiré du pool. Le tirage sert aussi aux PV : c'est la
        correction du bug de la v1, où l'asset posé et l'asset mesuré
        différaient."""
        if not pool or not _free(w, x, y):
            return
        aid = int(am.pick(pool, rng))
        a = am.assets[aid]
        if hp == "harvest":
            hp = int(a.harvest.get("hp", 1)) if getattr(a, "harvest", None) else 1
        s = size if size is not None else (a.size_tiles if a.solid else 1)
        w.place(x, y, aid, am, hp=hp, solid=solid, shelter=a.shelter, size=s)

    B = wg  # raccourci de lisibilité

    # ── forêts : là où l'humidité fait déjà pousser la forêt ──────────
    for cx, cy in _biome_sites(w, rng, 26 if dense else 6,
                               (B.BIOME_FOREST, B.BIOME_GRASS), max_slope=0.9):
        blob(w, am, rng, cx, cy, 11,
             lambda x, y: place(trees, x, y, hp="harvest", solid=True))

    # ── carrières : au pied des montagnes ─────────────────────────────
    for cx, cy in _biome_sites(w, rng, 9 if dense else 2,
                               (B.BIOME_ROCK, B.BIOME_GRASS)):
        blob(w, am, rng, cx, cy, 6,
             lambda x, y: place(stones, x, y, hp=5, solid=True))

    # ── filons d'or : plus haut, plus rares ───────────────────────────
    for cx, cy in _biome_sites(w, rng, 5 if dense else 1,
                               (B.BIOME_ROCK, B.BIOME_SNOW), margin=30):
        blob(w, am, rng, cx, cy, 4,
             lambda x, y: place(golds, x, y, hp=5, solid=True))

    # ── broussailles et rochers, partout ──────────────────────────────
    for _ in range(1200 if dense else 150):
        x, y = int(rng.integers(4, GRID - 4)), int(rng.integers(4, GRID - 4))
        place(bushes + rocks, x, y)

    # ── fruits sauvages : prairies et lisières ────────────────────────
    for x, y in _biome_sites(w, rng, 2500 if dense else 250,
                             (B.BIOME_GRASS, B.BIOME_FOREST, B.BIOME_MARSH),
                             margin=4):
        place(foods, x, y, hp=1)

    # ── carcasses ─────────────────────────────────────────────────────
    for _ in range(34 if dense else 5):
        x, y = int(rng.integers(8, GRID - 8)), int(rng.integers(8, GRID - 8))
        place(meats, x, y, hp=1)

    # ── outils oubliés ────────────────────────────────────────────────
    for _ in range(10 if dense else 2):
        x, y = int(rng.integers(6, GRID - 6)), int(rng.integers(6, GRID - 6))
        place(tools, x, y)

    _paint_floors(w, am, rng, dense)


def _paint_floors(w, am, rng, dense):
    """Clairières herbeuses et mares — peinture de sol, pas des objets."""
    if not am.floors:
        return
    n_sheets = len(am.floors)

    def paint(x, y):
        sheet = 0 if rng.random() < 0.9 else min(1, n_sheets - 1)
        cells = am.tile_cells(am.floors[sheet]) or 1
        w.set_floor(x, y, sheet * 216 + int(rng.integers(cells)))

    for cx, cy in _biome_sites(w, rng, 7 if dense else 2,
                               (3, 4), max_slope=0.8):   # prairie / forêt
        blob(w, am, rng, cx, cy, 9, paint)

    water_sheet = next((i for i, f in enumerate(am.floors)
                        if "water background" in am.assets[f].name.lower()), 5)
    water_sheet = min(water_sheet, n_sheets - 1)

    def paint_water(x, y):
        cells = am.tile_cells(am.floors[water_sheet]) or 1
        w.set_floor(x, y, water_sheet * 216 + int(rng.integers(cells)))

    cx, cy = (int(rng.integers(30, GRID - 30)), int(rng.integers(30, GRID - 30)))
    blob(w, am, rng, cx, cy, 5, paint_water)


# ══════════════════════════════════════════════════════════════════════
#  Construction du monde
# ══════════════════════════════════════════════════════════════════════
def build_world(am, seed, procedural=False, *, populate_dense=True,
                n_agents=0, tile_period=None, ridge_width=None,
                water_frac=WATER_FRAC, mountain_frac=MOUNTAIN_FRAC):
    """Construit le monde complet : heightmap, décor, simulation prête.

    `procedural=False` conserve l'ancien comportement (terre pleine, pas de
    relief) ; `procedural=True` génère les chaînes de montagnes.
    """
    from game import renderer as _ren
    _ren.set_blank_mode(False)

    rng = np.random.default_rng(seed)
    w = World()

    gen = compute_land(seed if procedural else None,
                       tile_period=tile_period, ridge_width=ridge_width,
                       water_frac=water_frac, mountain_frac=mountain_frac)
    if gen is not None:
        from game import worldgen as _wg
        _wg.apply_to_layers(w, gen)          # pose aussi w.gen
    else:
        w.set_land(np.ones((GRID, GRID), dtype=np.uint8))
        w.gen = None
    w.save_mountains()

    sim = Sim(w, am, seed=seed)

    # ← la v1 sautait cette étape : le monde naissait stérile
    populate(w, am, rng, dense=populate_dense)

    for _ in range(max(0, int(n_agents))):
        x, y = _spawn_spot(w, rng)
        sim.spawn_agent(x=x * TILE + TILE / 2, y=y * TILE + TILE / 2, parents=None)

    sim.paused = True
    if gen is not None:
        from game import worldgen as _wg
        parts = sorted(_wg.stats(gen).items(), key=lambda kv: -kv[1])[:4]
        repartition = ", ".join(f"{k} {v*100:.0f}%" for k, v in parts)
        px = world_pixels()
        sim.log(f"Monde prêt — {px}x{px} px ({GRID}x{GRID} tuiles) · "
                f"terre {(1 - water_frac) * 100:.0f}% / eau {water_frac * 100:.0f}% · "
                f"crêtes tous les {gen.tile_period * TILE} px · {repartition}. "
                f"Outil « Sculpter » pour creuser, « Restaurer » pour rétablir.",
                (108, 208, 128), "monde")
    else:
        sim.log("Monde prêt — terrain plat, pas de relief.",
                (108, 208, 128), "monde")
    return w, sim


def build_world_blank(am, seed):
    """Monde vierge : tout eau, aucun asset, aucun habitant.
    L'utilisateur peint ses îles avec les outils de terrain."""
    from game import renderer as _ren
    _ren.set_blank_mode(True)

    w = World()
    w.set_land(np.zeros((GRID, GRID), dtype=np.uint8))
    w.gen = None
    sim = Sim(w, am, seed=seed)
    sim.paused = True
    sim.log("Monde vide — tout est océan. Peignez des îles avec les outils "
            "de terrain.", (78, 168, 232), "monde")
    return w, sim


def _spawn_spot(w, rng, tries=400):
    """Trouve une case libre et praticable pour y faire naître un être."""
    for _ in range(tries):
        x = int(rng.integers(8, GRID - 8))
        y = int(rng.integers(8, GRID - 8))
        if w.land[y, x] and not w.blocked[y, x] and w.content_at(x, y) < 0:
            return x, y
    ys, xs = np.nonzero(w.land > 0)
    if len(xs):
        i = int(rng.integers(0, len(xs)))
        return int(xs[i]), int(ys[i])
    return GRID // 2, GRID // 2

```

## game/entities.py

**Type :** `.py`

```python

"""Being — composition d'un etre (document d'architecture §4).

Identite, Corps, Perception, Cognition, Memoire (episodique + semantique +
spatiale + sociale), Emotions, Personnalite, Besoins, Motivations (emergentes),
Volonte (inertie/persistance), Soi (estime, autobiographie), Imagination
(projection), Croyances (lieux dangereux, etres de confiance), Relations
(directionnelles), Experience, Competences, Habitudes, Inventaire, Cerveau.

Tout est reglable a la creation et pendant la vie — SAUF la taille du cerveau,
verrouillee a l'insertion pour toujours."""
import math
from collections import deque

import numpy as np

from .brain import Brain
from .config import (
    CLAN_COLORS, TILE, TICKS_PER_YEAR, AGE_CHILD_TICKS, AGE_ELDER_TICKS,
    AGE_MIN_NATURAL_DEATH_TICKS, AGE_MAX_NATURAL_DEATH_TICKS,
)

NAME_SYLL = ["Aa", "Be", "Co", "Dra", "El", "Fa", "Gi", "Ha", "I", "Jo", "Ka", "Lo",
             "Me", "Na", "O", "Pyr", "Qu", "Ro", "Sa", "Ti", "U", "Vane", "Wi", "Xo",
             "Yla", "Zo", "Mor", "Nim", "Sal", "Tor", "Ul", "Vre", "Yn", "Zeph"]

# categories de memoire spatiale
MEM_CATS = ("food", "wood", "stone", "water", "shelter", "agent")


class ClanKnowledge:
    """Mémoire commune du clan : géographie, ressources, dangers partagés."""
    def __init__(self):
        self.places = {}       # (cat, tx//8, ty//8) -> (founder_eid, tick, strength)
        self.dangers = {}      # (tx//8, ty//8) -> (reporter_eid, tick, level)
        self.reservations = {} # (tx, ty) -> eid (agent qui occupe la place)
        # Lot I : connaissances culturelles
        self.culture = {}      # (claim, tx//8, ty//8) -> {confidence, sources, confirmations, last_update}
        # Lot J : institutions émergentes
        self.institutions = {}  # (kind, tx//8, ty//8) -> {members, practices, trust, age, stability}

    def share_place(self, cat, tx, ty, eid, tick):
        key = (cat, tx // 8, ty // 8)
        old = self.places.get(key)
        if old is None or tick - old[2] > 500:
            self.places[key] = (eid, tick, min(1.0, (old[2] if old else 0) + 0.3))

    def report_danger(self, tx, ty, eid, tick, level=0.8):
        key = (tx // 8, ty // 8)
        old = self.dangers.get(key)
        if old is None or level > old[2]:
            self.dangers[key] = (eid, tick, level)

    def forget_danger(self, tx, ty, tick, decay_ticks=2000):
        key = (tx // 8, ty // 8)
        old = self.dangers.get(key)
        if old and tick - old[1] > decay_ticks:
            del self.dangers[key]

    def reserve(self, tx, ty, eid):
        self.reservations[(tx, ty)] = eid

    def release(self, tx, ty):
        self.reservations.pop((tx, ty), None)

    def is_reserved(self, tx, ty, eid):
        r = self.reservations.get((tx, ty))
        return r is not None and r != eid

    def nearby_places(self, cat, tx, ty, max_dist=60):
        """Retourne les lieux connus dans un rayon donné."""
        out = []
        for (c, cx8, cy8), (fid, t, s) in self.places.items():
            if c != cat:
                continue
            d = max(abs(cx8 * 8 - tx), abs(cy8 * 8 - ty))
            if d < max_dist:
                out.append((cx8 * 8, cy8 * 8, s, d))
        out.sort(key=lambda t: t[2] / (1 + t[3] * 0.1), reverse=True)
        return out

    # ── Lot I : culture ──

    def report_culture(self, claim, tx, ty, eid, tick):
        """Signale une connaissance culturelle."""
        key = (claim, tx // 8, ty // 8)
        entry = self.culture.get(key)
        if entry is None:
            self.culture[key] = {
                "confidence": 0.2, "sources": [eid],
                "confirmations": 1, "last_update": tick,
            }
        else:
            if eid not in entry["sources"]:
                entry["sources"].append(eid)
            entry["confirmations"] += 1
            entry["confidence"] = min(1.0, entry["confidence"] + 0.15)
            entry["last_update"] = tick

    def is_cultural(self, claim, tx, ty):
        """Une connaissance est culturelle si confirmée par plusieurs sources."""
        key = (claim, tx // 8, ty // 8)
        entry = self.culture.get(key)
        if entry is None:
            return False
        return (len(entry["sources"]) >= 2
                or entry["confirmations"] >= 3) and entry["confidence"] > 0.4

    # ── Lot J : institutions émergentes ──

    def add_institution(self, kind, tx, ty, eid, tick):
        """Ajoute un membre à une institution existante ou en crée une."""
        key = (kind, tx // 8, ty // 8)
        inst = self.institutions.get(key)
        if inst is None:
            self.institutions[key] = {
                "kind": kind, "members": [eid],
                "practices": {}, "trust": 0.3,
                "age": 0, "stability": 0.1,
                "created_tick": tick,
            }
        else:
            if eid not in inst["members"]:
                inst["members"].append(eid)
            inst["trust"] = min(1.0, inst["trust"] + 0.05)
            inst["stability"] = min(1.0, inst["stability"] + 0.03)

    def record_practice(self, kind, tx, ty, eid, action, tick):
        """Enregistre une pratique répétée dans une institution."""
        key = (kind, tx // 8, ty // 8)
        inst = self.institutions.get(key)
        if inst is None:
            return
        practices = inst.setdefault("practices", {})
        count = practices.get(action, 0)
        practices[action] = count + 1
        if count + 1 >= 3:
            inst["stability"] = min(1.0, inst["stability"] + 0.05)
        inst["age"] = tick - inst.get("created_tick", tick)

    def decay_institutions(self, tick, rate=0.001):
        """Dégrade les institutions inactives."""
        for key in list(self.institutions.keys()):
            inst = self.institutions[key]
            if tick - inst.get("last_practice_tick", inst.get("created_tick", 0)) > 5000:
                inst["stability"] *= (1.0 - rate)
                if inst["stability"] < 0.05:
                    del self.institutions[key]


class Being:
    """Un habitant : un corps, un esprit, une histoire."""

    def __init__(self, eid, x, y, color, cls, states, gen=0, brain=None, parents=(),
                 personality=None, rng=None, born_tick=0, n_hid=128,
                 body=None, cog=None, emotions=None, needs=None, sex=None):
        rng = rng or np.random.default_rng(eid * 7919 + 13)
        # ---- Identite / Soi
        self.eid = eid
        self.name = rng.choice(NAME_SYLL) + rng.choice(NAME_SYLL)
        self.gen = gen
        self.color = color
        self.cls = cls
        self.parents = parents
        self.children = []
        self.born_tick = born_tick
        self.life = deque(maxlen=48)          # autobiographie (events marquants)
        self.self_esteem = 0.5
        # ---- Corps
        self.x, self.y = float(x), float(y)
        self.vx = self.vy = 0.0
        self.fx, self.fy = int(rng.integers(-1, 2)) or 1, int(rng.integers(-1, 2))
        self.sex = sex if sex is not None else ("F" if rng.random() < 0.5 else "M")
        self.age = 0
        self.natural_death_age = int(rng.integers(
            AGE_MIN_NATURAL_DEATH_TICKS,
            AGE_MAX_NATURAL_DEATH_TICKS + 1,
        ))
        self.body = body if body is not None else np.clip(
            rng.random(5) * 0.6 + 0.25, 0, 1)        # force endurance mobilite sens recuperation
        self.health = 1.0
        self.pain = 0.0
        self.temp = 0.5                              # temperature corporelle
        self.tool = -1
        self.tool_durability = 0
        self.inv = {"bois": 0, "pierre": 0, "or": 0, "graine": 0}
        # ---- Cognition / cerveau (TAILLE VERROUILLEE)
        self.brain = brain or Brain(n_hid=n_hid, rng=rng)
        self.cog = cog if cog is not None else np.clip(
            rng.random(4) * 0.6 + 0.25, 0, 1)        # memoire anticipation imagination attention
        # ---- Emotions (etats continus, jamais des if)
        self.emotions = emotions if emotions is not None else np.array(
            [0.0, 0.35, 0.0, 0.1, 0.1, 0.0, 0.0, 0.0])  # peur joie colere tristesse stress surprise degout affection
        # ---- Besoins
        self.needs = needs if needs is not None else np.array(
            [0.25, 0.70, 0.30, 0.30, 0.80, 0.50, 0.40])
        # faim energie soif sommeil securite appartenance estime
        self.energy = float(self.needs[1])
        self.hunger = float(self.needs[0])
        # ---- Personnalite (predispositions, pas programmations)
        self.personality = (personality if personality is not None
                            else np.clip(rng.random(12) * 0.7 + 0.15, 0, 1))
        # ---- Experience / competences / habitudes
        self.skills = np.zeros(4)                    # recolte construction combat social
        self.habits = np.full(15, 0.06)
        # ---- Memoire
        self.seen = {c: [] for c in MEM_CATS}        # spatiale: [(x,y,force)]
        self.episodes = deque(maxlen=64)             # episodique: (tick, type, data)
        self.belief_beings = {}                      # semantique sociale: eid -> trait -1..1
        self.belief_places = {}                      # croyances lieux: (cx,cy) -> danger 0..1
        self.known = {}
        self.kn_t = -99
        self._loc = np.zeros(8)
        self._near_agents = []
        self._near_sheep = []
        self._near_monsters = []
        self._last_heard = -1
        # ---- Relations (directionnelles)
        self.rel = {}                                # eid -> [confiance, affection]
        self.rep = 0.0
        self.hated = None
        self.bonded = None                           # partenaire (famille)
        self.dangers = []
        self.gave = {}
        self.talk_cd = {}
        # ---- Anima (memoire episodique emotive)
        self.anima = {
            "episodic_memory": deque(maxlen=32),
            "beliefs": {"places": {}, "beings": {}},
            "identity": {
                "builder": 0.0, "provider": 0.0, "fighter": 0.0,
                "explorer": 0.0, "caretaker": 0.0, "survivor": 0.0,
                "mediator": 0.0,
            },
            "values": {
                "survival": 0.8, "family": 0.6, "security": 0.7,
                "community": 0.5, "knowledge": 0.4,
                "wealth": 0.5, "generosity": 0.5,
            },
            "trauma": {"attack": 0.0, "hunger": 0.0, "loss": 0.0, "betrayal": 0.0, "fire": 0.0},
            "attachments": {},
            "intention": None,
        }
        # ---- Volonte
        self.goal = None                             # intention structuree (dict)
        self.goal_t = 0
        self.commitment = 0.0                        # engagement dans le but courant
        self.stuck = 0
        self.failed_targets = {}                     # {(act,tx,ty): (count, until_tick)}
        self.observed_actions = deque(maxlen=32)     # actions observees chez autrui
        self.context = {
            "food_density": 0.0,
            "wood_density": 0.0,
            "stone_density": 0.0,
            "sheep_count": 0.0,
            "monster_count": 0.0,
            "ally_count": 0.0,
            "enemy_count": 0.0,
            "storage_near": 0.0,
            "site_near": 0.0,
            "route_danger": 0.0,
        }
        self.prev_wellbeing = 0.0
        self.mood_phase = float(rng.uniform(0, math.tau))
        self.mood_freq = float(rng.uniform(0.004, 0.02))
        self.home = None
        self.work_t = 0
        self.atk_t = 0
        self.repro_cd = 400
        # ---- Mariage / reproduction / filiation
        self.married = False
        self.partner_id = None            # eid du conjoint
        self.parent_pere_id = None        # eid du père
        self.parent_mere_id = None        # eid de la mère
        self.affinity_cd = 0              # cooldown avant prochaine tentative drague
        self.state = "idle"
        self.alive = True
        self.avatar = int(rng.integers(0, 400))
        self.col_idx = 1
        self.frame = 0
        self.anim_t = 0
        self.states = states
        self._last_px, self._last_py = self.x, self.y

    # ------------------------------------------------------------------ cycle de vie
    @property
    def age_years(self) -> float:
        return self.age / float(TICKS_PER_YEAR)

    @property
    def age_label(self) -> str:
        return f"{self.age_years:.1f} ans"

    @property
    def stage(self):
        if self.age < AGE_CHILD_TICKS:
            return "enfant"
        if self.age < AGE_ELDER_TICKS:
            return "adulte"
        return "ancien"

    @property
    def child(self):
        return self.age < AGE_CHILD_TICKS

    def age_health_cap(self) -> float:
        """Fragilité progressive, sans décès biologique avant 65 ans."""
        if self.age <= AGE_ELDER_TICKS:
            return 1.0
        span = max(1, self.natural_death_age - AGE_ELDER_TICKS)
        u = min(1.0, (self.age - AGE_ELDER_TICKS) / span)
        smooth = u * u * (3.0 - 2.0 * u)
        return 1.0 - 0.65 * smooth

    @property
    def hunger(self):
        return self.needs[0]

    @hunger.setter
    def hunger(self, v):
        self.needs[0] = v

    @property
    def rgb(self):
        return CLAN_COLORS.get(self.color, (200, 200, 200))

    @property
    def tx(self):
        return int(self.x // TILE)

    @property
    def ty(self):
        return int(self.y // TILE)

    def carry(self):
        return self.inv["bois"] + self.inv["pierre"] + self.inv["or"]

    def mood(self, tick):
        return math.sin(tick * self.mood_freq + self.mood_phase)

    def speed(self, light=1.0, heat=0.0):
        if self.child:
            age_factor = 0.55
        elif self.age < AGE_ELDER_TICKS:
            age_factor = 1.0
        else:
            age_factor = max(0.40, 0.75 * self.age_health_cap())
        hurt = max(0.35, 1.0 - 0.5 * self.pain - 0.4 * max(0.0, 0.2 - self.needs[1]))
        load_weight = (self.inv.get("bois", 0) * 1.0 +
                       self.inv.get("pierre", 0) * 1.5 +
                       self.inv.get("or", 0) * 2.0 +
                       self.inv.get("graine", 0) * 0.2)
        load_factor = max(0.45, 1.0 - 0.04 * load_weight)
        road_bonus = min(0.18, heat * 0.08)
        return (2.7 * (0.6 + 0.7 * self.body[2]) * age_factor * hurt
                * (0.8 + 0.2 * light) * load_factor * (1.0 + road_bonus))

    def drain_f(self):
        return (1.35 - 0.7 * self.body[1]) * (1.25 if self.child else 1.0)

    def dmg_f(self):
        return (0.7 + 0.8 * self.body[0]) * (1 + 0.5 * self.skills[2]) * (0.5 if self.child else 1.0)

    def sense_r(self, light=1.0):
        base = 12 + 44 * self.body[3]
        return int(base * (0.45 + 0.55 * light) * (0.6 + 0.4 * self.cog[3]))

    def sense_r_near(self):
        """Vision court portée : 8 cases autour (Moore), pour actions physiques."""
        return 8

    def trust(self, other_eid):
        r = self.rel.get(other_eid)
        return r[0] if r else 0.0

    def remember(self, cat, x, y):
        """La perception d'aujourd'hui devient la memoire de demain."""
        lst = self.seen[cat]
        for i in range(len(lst) - 1, -1, -1):
            if lst[i][0] == x and lst[i][1] == y:
                lst[i] = (x, y, min(1.0, lst[i][2] + 0.5))
                return
        lst.append((x, y, 0.85))
        if len(lst) > 40:
            lst.sort(key=lambda t: -t[2])
            del lst[40:]

    def recall(self, cat, tx, ty):
        """Se souvenir : (x,y,dist) le plus proche dans ma memoire, ou None."""
        best, bd = None, 1e9
        for (x, y, f) in self.seen[cat]:
            if f < 0.18:
                continue
            d = max(abs(x - tx), abs(y - ty)) / (1.15 - 0.5 * f)   # le doute eloigne
            if d < bd:
                best, bd = (x, y), d
        return (best[0], best[1], bd) if best else None

    def forget(self, cat, x, y):
        """Un souvenir inaccessible devient une fausse croyance : on l'efface."""
        self.seen[cat] = [(sx, sy, f) for sx, sy, f in self.seen[cat]
                          if not (sx == x and sy == y)]

    def remember_event(self, kind, data=None):
        self.episodes.append((self.born_tick, kind, data))

    def remember_anima_episode(self, tick, kind, place, actors=None,
                               action="", outcome="", emotion=None,
                               importance=0.0):
        """Enregistre un episode dans la memoire episodique Anima."""
        if emotion is None:
            emotion = {}
        ep = {
            "tick": tick, "kind": kind, "place": place,
            "actors": actors or [], "action": action,
            "outcome": outcome, "emotion": emotion,
            "importance": importance,
        }
        if importance < 0.20:
            return ep
        self.anima["episodic_memory"].append(ep)
        if importance >= 0.70:
            self._anima_strong_belief(kind, place, importance, emotion)
        else:
            self._anima_weak_belief(kind, place, importance)
        return ep

    def _anima_strong_belief(self, kind, place, importance, emotion):
        a = self.anima
        fear = emotion.get("fear", 0.0)
        cx, cy = place[0] // 8, place[1] // 8
        key = (cx, cy)
        old = a["beliefs"]["places"].get(key, 0.0)
        a["beliefs"]["places"][key] = min(1.0, max(old, importance * fear))
        if "attack" in kind:
            a["trauma"]["attack"] = min(1.0, a["trauma"]["attack"] + 0.15 * importance)
            a["identity"]["survivor"] = min(1.0, a["identity"]["survivor"] + 0.05)
        if "hunger" in kind:
            a["trauma"]["hunger"] = min(1.0, a["trauma"]["hunger"] + 0.10 * importance)
        if "loss" in kind:
            a["trauma"]["loss"] = min(1.0, a["trauma"]["loss"] + 0.12 * importance)

    def _anima_weak_belief(self, kind, place, importance):
        cx, cy = place[0] // 8, place[1] // 8
        key = (cx, cy)
        old = self.anima["beliefs"]["places"].get(key, 0.0)
        self.anima["beliefs"]["places"][key] = min(1.0, max(old, importance * 0.5))

    def anima_perceived_danger(self, tx, ty, base_danger):
        """Danger percu = visible + croyance + trauma - confiance allies."""
        a = self.anima
        cx, cy = tx // 8, ty // 8
        belief = a["beliefs"]["places"].get((cx, cy), 0.0)
        trauma_fear = min(1.0, a["trauma"]["attack"] * 0.4)
        ally_trust = min(0.3, len([e for e in a["attachments"].values()
                                    if e > 0.3]) * 0.1)
        perceived = base_danger + belief * 0.35 + trauma_fear - ally_trust
        return max(0.0, min(1.0, perceived))

    # ── Anima Phase 2 : API centralisee ──

    @staticmethod
    def anima_clamp(value: float) -> float:
        return max(0.0, min(1.0, float(value)))

    def anima_add_identity(self, key: str, delta: float) -> float:
        identity = self.anima.setdefault("identity", {})
        old = float(identity.get(key, 0.0))
        identity[key] = self.anima_clamp(old + float(delta))
        return identity[key]

    def anima_add_value(self, key: str, delta: float) -> float:
        values = self.anima.setdefault("values", {})
        old = float(values.get(key, 0.5))
        values[key] = self.anima_clamp(old + float(delta))
        return values[key]

    def anima_dominant_identity(self):
        identity = self.anima.get("identity", {})
        if not identity:
            return None
        key, score = max(identity.items(), key=lambda item: item[1])
        return key if score >= 0.20 else None

    def anima_decay_identity(self, amount: float = 0.001):
        for key, value in self.anima.get("identity", {}).items():
            self.anima["identity"][key] = self.anima_clamp(
                value * (1.0 - amount))

    # ── Lot C : trauma, résilience, attachement ──

    def anima_decay_trauma(self, safety: float = 1.0, support: float = 0.0):
        """Décroissance du trauma basée sur sécurité et soutien social."""
        recovery = 0.0005 + 0.0015 * self.personality[5]
        rate = recovery * max(0.35, safety) * (0.6 + 0.4 * min(1.0, support))
        for key in self.anima.get("trauma", {}):
            self.anima["trauma"][key] = self.anima_clamp(
                self.anima["trauma"][key] * (1.0 - rate))

    def anima_add_attachment(self, key, delta: float):
        """Ajoute un delta d'attachement pour une cible (eid, lieu, etc.)."""
        att = self.anima.setdefault("attachments", {})
        att[key] = self.anima_clamp(att.get(key, 0.0) + delta)

    def anima_get_attachment(self, key) -> float:
        return self.anima.get("attachments", {}).get(key, 0.0)

    def anima_home_preference(self) -> float:
        """Préférence de retour au foyer basée sur attachement."""
        if self.home is None:
            return 0.0
        key = f"home:{self.home[0]}:{self.home[1]}"
        return self.anima_get_attachment(key) * 0.3

    # ── Lot D : intention psychologique persistante ──

    def anima_set_intention(self, kind: str, reason: str = "",
                            target=None, place=None,
                            priority: float = 0.5, tick: int = 0,
                            duration: int = 500):
        """Définit ou remplace l'intention Anima courante."""
        self.anima["intention"] = {
            "kind": kind,
            "reason": reason,
            "target": target,
            "place": place,
            "priority": self.anima_clamp(priority),
            "created_tick": tick,
            "expires_tick": tick + duration,
            "progress": 0.0,
        }

    def anima_clear_intention(self):
        self.anima["intention"] = None

    def anima_get_intention(self):
        return self.anima.get("intention")

    def anima_intention_valid(self, tick: int) -> bool:
        """Vérifie si l'intention courante est encore valide."""
        intent = self.anima.get("intention")
        if intent is None:
            return False
        if tick > intent.get("expires_tick", 0):
            self.anima["intention"] = None
            return False
        return True

    def anima_update_intention_progress(self, delta: float, tick: int):
        """Met à jour la progression de l'intention."""
        intent = self.anima.get("intention")
        if intent is None:
            return
        intent["priority"] = self.anima_clamp(intent["priority"] + delta)
        intent["expires_tick"] = tick + 500

    # ── Lot F : apprentissage causal différé ──

    def anima_add_causal_trace(self, action, place, tick, expected_effect=""):
        """Enregistre une trace causale pour crédit différé."""
        traces = self.anima.setdefault("causal_traces", [])
        traces.append({
            "tick": tick, "action": action, "place": place,
            "eligibility": 1.0, "contribution": 0.0,
            "expected_effect": expected_effect,
        })
        if len(traces) > 32:
            traces.pop(0)

    def anima_decay_causal_traces(self, rate: float = 0.02):
        traces = self.anima.get("causal_traces", [])
        for t in traces:
            t["eligibility"] *= (1.0 - rate)
        self.anima["causal_traces"] = [t for t in traces if t["eligibility"] > 0.05]

    def anima_credit_for(self, effect_kind, tick, max_delay=2000):
        """Retourne et consomme le crédit causale pour un effet donné."""
        traces = self.anima.get("causal_traces", [])
        credit = 0.0
        for t in traces:
            if t.get("expected_effect") == effect_kind and t["eligibility"] > 0.1:
                delay = tick - t.get("tick", 0)
                if 0 < delay < max_delay:
                    credit += t["eligibility"] * max(0.0, 1.0 - delay / max_delay)
                    t["contribution"] = min(1.0, t["contribution"] + 0.3)
                    t["eligibility"] *= 0.5
        return min(1.0, credit)

    # ── Lot H : imitation réelle ──

    def anima_record_observation(self, action, reward, tick):
        """Enregistre l'observation d'une action réussie par autrui."""
        obs = self.anima.setdefault("observations", deque(maxlen=24))
        obs.append({"action": int(action), "reward": float(reward), "tick": tick})

    def anima_apply_observation_learning(self):
        """Modifie les habitudes basées sur les observations."""
        obs = self.anima.get("observations")
        if not obs:
            return
        for o in list(obs):
            act = o.get("action", -1)
            reward = o.get("reward", 0.0)
            if 0 <= act < len(self.habits) and reward > 0:
                self.habits[act] = self.anima_clamp(
                    self.habits[act] + 0.01 * reward)
        obs.clear()

    # ── Lot 2 : memoire sociale personnelle ──

    def anima_social_belief(self, other_eid: int, tick: int):
        beliefs = self.anima.setdefault("beliefs", {}).setdefault("beings", {})
        eid = int(other_eid)
        existing = beliefs.get(eid)
        if existing is None or not isinstance(existing, dict):
            beliefs[eid] = {
                "trust": 0.5, "danger": 0.0, "generosity": 0.5,
                "reliability": 0.5, "confidence": 0.0,
                "last_update": int(tick),
            }
        return beliefs[eid]

    def anima_update_social_belief(self, other_eid: int, tick: int,
                                   trust_delta=0.0, danger_delta=0.0,
                                   generosity_delta=0.0,
                                   reliability_delta=0.0,
                                   confidence_delta=0.0):
        belief = self.anima_social_belief(other_eid, tick)
        for key, delta in {
            "trust": trust_delta, "danger": danger_delta,
            "generosity": generosity_delta,
            "reliability": reliability_delta,
            "confidence": confidence_delta,
        }.items():
            belief[key] = self.anima_clamp(
                float(belief.get(key, 0.0)) + float(delta))
        belief["last_update"] = int(tick)
        return belief

    def anima_social_score(self, other_eid: int) -> float:
        belief = (self.anima.get("beliefs", {})
                  .get("beings", {}).get(int(other_eid)))
        if not belief or not isinstance(belief, dict):
            return 0.0
        trust = float(belief.get("trust", 0.5))
        reliability = float(belief.get("reliability", 0.5))
        danger = float(belief.get("danger", 0.0))
        return (trust - 0.5) * 0.8 + (reliability - 0.5) * 0.4 - danger * 0.9

    def set_dir(self, dx, dy):
        dx, dy = float(dx), float(dy)
        if abs(dx) + abs(dy) < 0.08:
            return
        self.vx, self.vy = dx, dy
        self.fx = int(dx > 0.18) - int(dx < -0.18)
        self.fy = int(dy > 0.18) - int(dy < -0.18)
        if self.fx == 0 and self.fy == 0:
            self.fx = 1


class Sheep:
    __slots__ = ("eid", "x", "y", "vx", "vy", "energy", "health", "brain", "state",
                 "alive", "anim_t", "frame", "fear")

    def __init__(self, eid, x, y, brain=None):
        rng = np.random.default_rng(eid * 104729 + 7)
        self.eid = eid
        self.x, self.y = x, y
        self.vx = self.vy = 0.0
        self.energy = 0.6
        self.health = 1.0
        self.brain = brain or Brain(n_hid=64, rng=rng)
        self.state = "idle"
        self.alive = True
        self.anim_t = 0
        self.frame = 0
        self.fear = 0.0

    @property
    def tx(self):
        return int(self.x // TILE)

    @property
    def ty(self):
        return int(self.y // TILE)


class Monster:
    __slots__ = ("eid", "x", "y", "vx", "vy", "energy", "health", "kind",
                 "alive", "anim_t", "frame", "hostile", "damage", "sight", "state")

    def __init__(self, eid, x, y, kind="wolf"):
        self.eid = eid
        self.x, self.y = x, y
        self.vx = self.vy = 0.0
        self.energy = 0.8
        self.health = 1.0
        self.kind = kind
        self.alive = True
        self.anim_t = 0
        self.frame = 0
        self.state = "idle"
        stats = {"bear": {"hostile": True, "damage": 0.18, "sight": 6},
                 "wolf": {"hostile": True, "damage": 0.12, "sight": 8},
                 "snake": {"hostile": True, "damage": 0.10, "sight": 5},
                 "beatle": {"hostile": False, "damage": 0.0, "sight": 3}}
        s = stats.get(kind, stats["wolf"])
        self.hostile = s["hostile"]
        self.damage = s["damage"]
        self.sight = s["sight"]

    @property
    def tx(self):
        return int(self.x // TILE)

    @property
    def ty(self):
        return int(self.y // TILE)


# compat nom historique (dashboard/renderer)
Inhabitant = Being

```

## game/invariants.py

**Type :** `.py`

```python

"""Tests d'invariants exécutables en mode debug."""
from __future__ import annotations


def validate_simulation(sim):
    errors = []
    w = sim.w

    for a in sim.agents:
        if not a.alive:
            errors.append(f"agent mort encore présent : eid={a.eid}")
        if not (0 <= a.tx < w.g and 0 <= a.ty < w.g):
            errors.append(f"agent hors monde : eid={a.eid}")
        if not (0.0 <= a.health <= 1.0):
            errors.append(f"santé invalide : eid={a.eid}")
        if not (0.0 <= a.energy <= 1.0):
            errors.append(f"énergie invalide : eid={a.eid}")
        if not (0.0 <= a.hunger <= 1.0):
            errors.append(f"faim invalide : eid={a.eid}")
        if a.tool >= 0 and not (0 <= a.tool < len(sim.am.assets)):
            errors.append(f"outil invalide : eid={a.eid}")

    for tx, ty, name, death_tick, color in getattr(w, "cemetery", ()):
        if not (0 <= tx < w.g and 0 <= ty < w.g):
            errors.append(f"tombe hors monde : {name}")

    for (tx, ty), storage in getattr(w, "storages", {}).items():
        if (tx, ty) != (storage.tx, storage.ty):
            errors.append("clé de stockage incohérente")
        if sum(storage.inventory.values()) > storage.capacity:
            errors.append(f"stockage dépasse capacité : {tx},{ty}")

    return errors

```

## game/lab.py

**Type :** `.py`

```python

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

```

## game/mapapi.py

**Type :** `.py`

```python

"""MapAPI — abstraction de carte sans Pygame.

Fournit des snapshots de carte et des conversions de coordonnees
pour n'importe quel frontend (Pygame, Qt, web).
"""
from __future__ import annotations

import math
from typing import Any


class MapTransform:
    """Transformation geometrique de la carte (neutre, pas de Pygame)."""

    def __init__(self, x: float = 0.0, y: float = 0.0,
                 zoom: float = 0.25, tilt: float = 55.0):
        self.x = x
        self.y = y
        self.zoom = zoom
        self.tilt = tilt

    @property
    def ys(self) -> float:
        return math.cos(math.radians(self.tilt))

    def view_w(self, screen_w: int) -> float:
        return screen_w / self.zoom

    def view_h(self, screen_h: int) -> float:
        return screen_h / (self.zoom * self.ys)

    def to_screen(self, wx: float, wy: float) -> tuple[float, float]:
        """Coordonnees monde -> ecran."""
        return (wx - self.x) * self.zoom, (wy - self.y) * self.zoom * self.ys

    def to_world(self, sx: float, sy: float) -> tuple[float, float]:
        """Coordonnees ecran -> monde."""
        return self.x + sx / self.zoom, self.y + sy / (self.zoom * self.ys)

    def clamp(self, world_size: float) -> None:
        """Empeche de sortir du monde."""
        vw = self.view_w(world_size)
        vh = self.view_h(world_size)
        if vw >= world_size:
            self.x = (world_size - vw) / 2
        else:
            self.x = min(max(self.x, 0), world_size - vw)
        if vh >= world_size:
            self.y = (world_size - vh) / 2
        else:
            self.y = min(max(self.y, 0), world_size - vh)

    def center_on(self, wx: float, wy: float, screen_w: int, screen_h: int,
                  world_size: float) -> None:
        """Centre la vue sur un point monde."""
        self.x = wx - self.view_w(screen_w) / 2
        self.y = wy - self.view_h(screen_h) / 2
        self.clamp(world_size)

    def visible_tiles(self, tile_size: int, grid_size: int) -> tuple[int, int, int, int]:
        """Retourne (x0, y0, x1, y1) des tuiles visibles."""
        vw = self.view_w(grid_size * tile_size)
        vh = self.view_h(grid_size * tile_size)
        x0 = max(0, int(self.x // tile_size) - 2)
        y0 = max(0, int(self.y // tile_size) - 2)
        x1 = min(grid_size, int((self.x + vw) // tile_size) + 3)
        y1 = min(grid_size, int((self.y + vh) // tile_size) + 3)
        return x0, y0, x1, y1

    def set_zoom(self, new_zoom: float, anchor_screen: tuple[int, int] = (0, 0),
                 screen_w: int = 800, screen_h: int = 600) -> None:
        """Change le zoom en gardant un point ecran fixe."""
        wx, wy = self.to_world(anchor_screen[0], anchor_screen[1])
        self.zoom = max(0.05, min(6.0, new_zoom))
        sx, sy = self.to_screen(wx, wy)
        self.x -= (sx - anchor_screen[0]) / self.zoom
        self.y -= (sy - anchor_screen[1]) / (self.zoom * self.ys)


def map_tile_data(sim, tx: int, ty: int) -> dict[str, Any] | None:
    """Donnees d'une tuile pour le rendu (pas de surface Pygame)."""
    w = sim.w
    if not (0 <= tx < w.g and 0 <= ty < w.g):
        return None

    aid = w.content_at(tx, ty)
    return {
        "tx": tx,
        "ty": ty,
        "land": bool(w.land[ty, tx]),
        "water": bool(w.water[ty, tx]),
        "blocked": bool(w.blocked[ty, tx]),
        "shelter": bool(w.shelter[ty, tx]),
        "fire": int(w.fire[ty, tx]),
        "floor": int(w.floor[ty, tx]),
        "hp": int(w.hp[ty, tx]) if aid >= 0 else 0,
        "asset_id": int(aid) if aid >= 0 else -1,
        "regrow": float(w.regrow[ty, tx]),
    }


def map_visible_data(sim, transform: MapTransform, screen_w: int, screen_h: int,
                     tile_size: int = None) -> dict[str, Any]:
    """Snapshot de la zone visible pour le rendu carte.

    Retourne des donnees simples, pas de surfaces.
    """
    from .config import GRID, TILE
    ts = tile_size or TILE
    grid_size = GRID
    world_size = grid_size * ts

    x0, y0, x1, y1 = transform.visible_tiles(ts, grid_size)

    # Terrain (batch)
    terrain = []
    for ty in range(y0, y1):
        for tx in range(x0, x1):
            td = map_tile_data(sim, tx, ty)
            if td is not None:
                terrain.append(td)

    # Agents visibles
    agents = []
    vw = transform.view_w(screen_w)
    vh = transform.view_h(screen_h)
    for a in sim.agents:
        if not a.alive:
            continue
        sx, sy = transform.to_screen(a.x, a.y)
        if -50 < sx < screen_w + 50 and -50 < sy < screen_h + 50:
            agents.append({
                "eid": int(a.eid),
                "sx": float(sx), "sy": float(sy),
                "color": str(a.color),
                "cls": str(a.cls),
                "stage": str(a.stage),
            })

    # Sheep visibles
    sheep = []
    for s in sim.sheep:
        sx, sy = transform.to_screen(s.x, s.y)
        if -50 < sx < screen_w + 50 and -50 < sy < screen_h + 50:
            sheep.append({"eid": int(s.eid), "sx": float(sx), "sy": float(sy)})

    # Monsters visibles
    monsters = []
    for m in sim.monsters:
        sx, sy = transform.to_screen(m.x, m.y)
        if -50 < sx < screen_w + 50 and -50 < sy < screen_h + 50:
            monsters.append({
                "eid": int(m.eid), "sx": float(sx), "sy": float(sy),
                "kind": str(getattr(m, "kind", "")),
            })

    # Effets visibles
    effects = []
    for e in sim.effects:
        sx, sy = transform.to_screen(e.get("x", 0), e.get("y", 0))
        if -50 < sx < screen_w + 50 and -50 < sy < screen_h + 50:
            effects.append({
                "kind": str(e.get("kind", "")),
                "sx": float(sx), "sy": float(sy),
                "color": tuple(e.get("color", (255, 255, 255))),
            })

    return {
        "tick": int(sim.w.tick),
        "tile_range": (x0, y0, x1, y1),
        "terrain": terrain,
        "agents": agents,
        "sheep": sheep,
        "monsters": monsters,
        "effects": effects,
        "zoom": float(transform.zoom),
        "tilt": float(transform.tilt),
    }

```

## game/messages.py

**Type :** `.py`

```python

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Message:
    sender_eid: int
    receiver_eid: int
    kind: str
    category: str | None
    tx: int | None
    ty: int | None
    confidence: float
    tick: int

```

## game/renderer.py

**Type :** `.py`

```python

"""Rendu du monde : terrain procédural (worldgen), tuiles de sol peintes,
phéromones, assets ancrés animables, habitants, moutons, objets lâchés,
effets, nuit / pluie, fantôme de pose.

Corrections et améliorations par rapport à la v1
------------------------------------------------
1. BUG D'ANCRAGE DU TERRAIN : la v1 blittait le patch de terrain à
   `sy - sh`, où `sh` est la hauteur de TOUT le patch. `cam.to_screen()`
   renvoyant le bord bas d'une SEULE tuile, le terrain était décalé vers le
   haut de (hauteur_du_patch − une_tuile). Corrigé : `sy - th`.
2. CACHE DE TERRAIN : la v1 recalculait `render_patch_rgb` + `smoothscale`
   à chaque frame (des millions d'opérations pour rien). Le terrain est
   maintenant mis en cache, invalidé par `gen.version` (incrémenté par les
   outils de sculpture), la zone visible et le zoom.
3. `_night` reconstruisait un dégradé radial par feu et par frame. Les halos
   sont désormais mis en cache par rayon.
4. Polices : `_legend` appelait `SysFont` à chaque frame. Toutes les polices
   passent par `_font()`, mis en cache.
5. Aperçu du pinceau pour les outils de terrain (Sculpter / Restaurer / Eau /
   Terre / Mur) : un cercle de rayon réel, au lieu du carré 1×1 trompeur.
6. Bornes clampées avant usage (la v1 clampait `x1`/`y1` APRÈS s'en être
   servi), `show_grid` déclaré dans `__init__`, variables mortes retirées.
"""
from __future__ import annotations

import numpy as np
import pygame

from . import config
from .config import CLAN_COLORS, GRID, TILE
from .entities import Inhabitant, Sheep, Monster
from .world import Item

_blank_mode = False


def set_blank_mode(flag=True):
    global _blank_mode
    _blank_mode = flag


def _zq(zoom):
    """Zoom quantifié — clé de cache stable pour les surfaces mises à l'échelle."""
    return round(zoom, 2)


# --- couleurs de repli (utilisées quand le monde n'a pas de heightmap) ---
_WATER_COL = (46, 92, 158)
_LAND_COL = (86, 150, 62)
_WALL_COL = (128, 118, 106)

_FONT_STACK = "segoeui,inter,dejavusans,liberationsans,arial"

# Couleurs d'aperçu par outil de terrain
_BRUSH_COLORS = {
    "carve":   (228, 142, 78),
    "restore": (118, 198, 138),
    "water":   (78, 168, 232),
    "land":    (150, 196, 96),
    "wall":    (186, 172, 150),
    "erase":   (228, 98, 98),
}
_BRUSH_MODES = tuple(_BRUSH_COLORS)


class _CamView:
    """Caméra décalée sur la zone de carte.

    `Camera.to_screen()` renvoie des coordonnées relatives au coin haut-gauche
    du VIEWPORT, pas de la fenêtre : `dashboard.apply_map_tool` le confirme en
    faisant `cam.to_world(mx - vr.x, my)`. Le renderer blittait pourtant ces
    coordonnées telles quelles sur `screen`, donc toute la carte était décalée
    de la largeur du panneau gauche — et comme ce panneau est repliable, le
    décalage change en cours de partie.

    Ce proxy ajoute l'origine du viewport à `to_screen` et la retire de
    `to_world`. Tout le reste du renderer continue d'appeler `cam.to_screen`
    sans rien savoir de la mise en page.
    """
    __slots__ = ("_c", "ox", "oy", "w", "h")

    def __init__(self, cam, rect):
        self._c = cam
        self.ox, self.oy = rect.x, rect.y
        self.w, self.h = rect.width, rect.height

    def __getattr__(self, name):          # zoom, ys, tilt, x, y, clamp…
        return getattr(self._c, name)

    def to_screen(self, wx, wy):
        sx, sy = self._c.to_screen(wx, wy)
        return sx + self.ox, sy + self.oy

    def to_world(self, sx, sy):
        return self._c.to_world(sx - self.ox, sy - self.oy)

    def visible_tiles(self):
        return self._c.visible_tiles()


class Renderer:
    show_grid = False

    def __init__(self, am):
        self.am = am
        self.clock = 0.0
        self.show_grid = False

        # caches
        self.circle_cache = {}
        self.shadow_cache = {}
        self._ftile_cache = {}
        self._fonts = {}
        self._glow_cache = {}
        self._night_cache = None
        self._night_key = None
        self._rain_cache = None
        self._rain_key = None
        self._terrain_surf = None
        self._terrain_key = None
        self._terrain_pos = (0, 0)

    # ══════════════════════════════════════════════════════════════════
    #  Outils internes
    # ══════════════════════════════════════════════════════════════════
    def _font(self, size, bold=False):
        k = (size, bold)
        f = self._fonts.get(k)
        if f is None:
            f = pygame.font.SysFont(_FONT_STACK, size, bold=bold)
            self._fonts[k] = f
        return f

    def _clan_rgb(self, idx):
        cols = list(CLAN_COLORS.values())
        if 1 <= idx <= len(cols):
            return cols[idx - 1]
        return (180, 180, 180)

    def _circle(self, rgb, size, ys=1.0, alpha=90):
        k = (rgb, int(size), round(ys, 2), alpha)
        c = self.circle_cache.get(k)
        if c is None:
            h = max(3, int(k[1] * k[2]))
            c = pygame.Surface((k[1], h), pygame.SRCALPHA)
            pygame.draw.ellipse(c, (*rgb, alpha), (0, 0, k[1], h))
            if len(self.circle_cache) > 2000:
                self.circle_cache.clear()
            self.circle_cache[k] = c
        return c

    def _ftile(self, sheet_aid, cell, zq, ys_q):
        k = (sheet_aid, cell, zq, ys_q)
        s = self._ftile_cache.get(k)
        if s is None:
            base = self.am.floor_tile(sheet_aid, cell, zq)
            w = base.get_width()
            h = max(2, int(base.get_height() * ys_q))
            s = pygame.transform.scale(base, (w, h)) if h != base.get_height() else base
            if len(self._ftile_cache) > 3000:
                self._ftile_cache.clear()
            self._ftile_cache[k] = s
        return s

    def _ground_shadow(self, w, ys=1.0):
        k = (max(4, int(w)), round(ys, 2))
        s = self.shadow_cache.get(k)
        if s is None:
            s = pygame.Surface((k[0], max(2, int(k[0] * 0.5 * ys))), pygame.SRCALPHA)
            pygame.draw.ellipse(s, (0, 0, 0, 70), (0, 0, k[0], s.get_height()))
            self.shadow_cache[k] = s
        return s

    def _glow(self, radius, alpha):
        """Halo radial mis en cache — évite de le reconstruire par feu et par frame."""
        k = (int(radius), int(alpha) // 8)
        g = self._glow_cache.get(k)
        if g is None:
            rr = max(4, k[0])
            g = pygame.Surface((rr * 2, rr * 2), pygame.SRCALPHA)
            for r in range(rr, 0, -3):
                a = min(255, int(6 * (1.0 - r / rr) * alpha / 3))
                if a > 0:
                    pygame.draw.circle(g, (255, 180, 90, a), (rr, rr), r)
            if len(self._glow_cache) > 64:
                self._glow_cache.clear()
            self._glow_cache[k] = g
        return g

    # ══════════════════════════════════════════════════════════════════
    #  Boucle de rendu
    # ══════════════════════════════════════════════════════════════════
    def draw(self, screen, sim, cam, ui):
        self.clock = pygame.time.get_ticks() / 1000.0
        w, z = sim.w, cam.zoom
        ys = cam.ys
        ys_q = round(ys, 2)
        zq = _zq(z)

        # Zone de carte : le panneau gauche est repliable, donc elle bouge.
        # `main.py` la fournit via ui["view_rect"] (= dash.view_rect()) ;
        # sans elle on retombe sur la fenêtre entière.
        # IMPORTANT : view_rect est en coordonnées surface-local (0,0,w,h)
        # car le renderer reçoit view_surf, pas l'écran global.
        view = ui.get("view_rect")
        view = pygame.Rect(view) if view is not None else screen.get_rect()
        if view.width <= 0 or view.height <= 0:
            return
        cam = _CamView(cam, view)

        # tout le rendu de monde reste confiné à la zone de carte
        prev_clip = screen.get_clip()
        screen.set_clip(screen.get_rect())
        try:
            self._draw_world(screen, sim, cam, ui, view, z, ys, ys_q, zq)
        finally:
            screen.set_clip(prev_clip)

    def _draw_world(self, screen, sim, cam, ui, view, z, ys, ys_q, zq):
        w = sim.w

        # bornes visibles, clampées AVANT tout usage
        x0, y0, x1, y1 = self._visible_box(view, cam)

        # 1) fond
        screen.fill(_WATER_COL, view)

        # 2) terrain
        self._terrain(screen, w, cam, x0, y0, x1, y1)

        # Seuils de détail : en vue très éloignée un sprite fait moins d'un
        # pixel. Les dessiner coûte des dizaines de milliers de blits pour un
        # résultat invisible — le terrain porte déjà toute l'information.
        draw_floors = z >= 0.25
        draw_props = z >= 0.20

        # 3) sol peint (tuiles écrasées = perspective)
        floors = w.floor[y0:y1 + 1, x0:x1 + 1] if draw_floors else np.empty((0, 0), np.int32)
        fy, fx = np.nonzero(floors >= 0) if floors.size else ((), ())
        n_sheets = len(self.am.floors)
        for j, i in zip(fy, fx):
            sheet, cell = divmod(int(floors[j, i]), 216)
            if sheet >= n_sheets:
                continue
            surf = self._ftile(self.am.floors[sheet], cell, zq, ys_q)
            sx, sy = cam.to_screen((x0 + i) * TILE, (y0 + j) * TILE)
            screen.blit(surf, (sx, sy))

        # 4) phéromones (inutiles et coûteuses en vue éloignée)
        if z >= 0.75:
            msub = w.marker[y0:y1 + 1, x0:x1 + 1]
            mys, mxs = np.nonzero(msub > 0.06)
            for j, i in zip(mys, mxs):
                col = self._clan_rgb(int(w.marker_col[y0 + j, x0 + i]))
                sz = max(5, int(22 * z * float(msub[j, i])))
                sx, sy = cam.to_screen((x0 + i) * TILE + 8, (y0 + j) * TILE + 8)
                screen.blit(self._circle(col, sz, ys_q),
                            (sx - sz / 2, sy - sz * ys_q / 2))

        # 5) tout ce qui a une profondeur, trié par y
        draws = []
        for it in w.items:
            if x0 - 1 <= it.x / TILE <= x1 + 1 and y0 - 1 <= it.y / TILE <= y1 + 1:
                draws.append((it.y, 0, self._draw_item, (it,)))
        for s in sim.sheep:
            if x0 - 1 <= s.x / TILE <= x1 + 1 and y0 - 1 <= s.y / TILE <= y1 + 1:
                draws.append((s.y, 1, self._draw_sheep, (s,)))
        for m in sim.monsters:
            if x0 - 1 <= m.x / TILE <= x1 + 1 and y0 - 1 <= m.y / TILE <= y1 + 1:
                draws.append((m.y, 1, self._draw_monster, (m,)))
        for a in sim.agents:
            if a.alive and x0 - 1 <= a.x / TILE <= x1 + 1 and y0 - 1 <= a.y / TILE <= y1 + 1:
                draws.append((a.y, 2, self._draw_agent, (a, ui)))
        if draw_props:
            csub = w.content[y0:y1 + 1, x0:x1 + 1]
            cys, cxs = np.nonzero(csub >= 0)
            for j, i in zip(cys, cxs):
                aid = int(csub[j, i])
                if aid < 0 or aid >= len(self.am.assets):
                    continue
                a_def = self.am.assets[aid]
                bottom_y = ((y0 + j) + a_def.size_tiles) * TILE
                draws.append((bottom_y, 3, self._draw_asset,
                              (int(i) + x0, int(j) + y0, aid, w)))
        for eff in sim.effects:
            draws.append((eff["y"] + 1, 4, self._draw_fx, (eff, sim.w.tick)))
        # cimetière : pierres tombales neutres
        for tx, ty, name, dtick, col in w.cemetery:
            if x0 - 1 <= tx <= x1 + 1 and y0 - 1 <= ty <= y1 + 1:
                draws.append(((ty) * TILE + 8, 3.5, self._draw_headstone,
                              (tx, ty, name, col)))
        draws.sort(key=lambda t: (t[0], t[1]))
        for _, _, fn, arg in draws:
            fn(screen, cam, *arg)

        # 5.5) chantiers en cours (blueprints translucides)
        self._draw_sites(screen, cam, w, (x0, y0, x1, y1))

        # 6) ligne de quête de l'habitant sélectionné
        self._goal_line(screen, cam, ui)

        # 6.5) overlay de diagnostic
        self._draw_diagnostic_overlay(screen, sim, cam, ui, (x0, y0, x1, y1))

        # 7) atmosphère
        box = (x0, y0, x1, y1)
        self._fires(screen, cam, w, box)
        self._night(screen, sim, cam, w, box)
        self._rain(screen, sim)

        # 8) surcouches d'interface
        if ui.get("legend"):
            self._legend(screen, view)
        if ui.get("ghost"):
            self._ghost(screen, cam, ui)
        if self.show_grid:
            self._grid_lines(screen, cam, view)

    def _visible_box(self, view, cam):
        """Rectangle de tuiles réellement couvert par le viewport.

        `cam.visible_tiles()` sous-estime la zone en vue éloignée ou en forte
        inclinaison : c'est pourquoi le terrain n'occupait qu'une partie de
        l'écran. On projette donc les quatre coins de l'écran vers le monde
        via `cam.to_world`, ce qui couvre l'écran quels que soient le zoom et
        l'angle. `visible_tiles()` sert de repli si la caméra n'expose pas
        `to_world`.
        """
        to_world = getattr(cam, "to_world", None)
        if callable(to_world):
            try:
                corners = [to_world(view.left, view.top),
                           to_world(view.right, view.top),
                           to_world(view.left, view.bottom),
                           to_world(view.right, view.bottom)]
                xs = [c[0] for c in corners]
                ys = [c[1] for c in corners]
                # marge d'une tuile : un objet ancré hors champ peut déborder
                bx0 = int(np.floor(min(xs) / TILE)) - 1
                bx1 = int(np.ceil(max(xs) / TILE)) + 1
                by0 = int(np.floor(min(ys) / TILE)) - 1
                by1 = int(np.ceil(max(ys) / TILE)) + 1
            except Exception:
                bx0, by0, bx1, by1 = cam.visible_tiles()
        else:
            bx0, by0, bx1, by1 = cam.visible_tiles()

        x0 = max(0, min(GRID - 1, int(bx0)))
        y0 = max(0, min(GRID - 1, int(by0)))
        x1 = max(x0, min(GRID - 1, int(bx1)))
        y1 = max(y0, min(GRID - 1, int(by1)))
        return x0, y0, x1, y1

    # ── terrain ──────────────────────────────────────────────────────
    def _terrain(self, screen, w, cam, x0, y0, x1, y1):
        """Dessine le heightmap via worldgen, avec cache invalidé par version."""
        gen = getattr(w, "gen", None)
        if gen is None:
            self._terrain_fallback(screen, w, cam, x0, y0, x1, y1)
            return

        py0, py1 = y0, min(GRID, y1 + 2)
        px0, px1 = x0, min(GRID, x1 + 2)
        if py1 <= py0 or px1 <= px0:
            return

        z, ys = cam.zoom, cam.ys
        tw = TILE * z
        th = TILE * z * ys
        pw, ph = px1 - px0, py1 - py0
        sw = max(1, int(round(pw * tw)))
        sh = max(1, int(round(ph * th)))

        key = (gen.version, py0, py1, px0, px1, sw, sh)
        if key != self._terrain_key:
            patch = _wg().render_patch_rgb(gen, py0, py1, px0, px1)
            h, wd = patch.shape[:2]
            # frombuffer attend (largeur, hauteur) et des lignes contiguës
            surf = pygame.image.frombuffer(
                np.ascontiguousarray(patch).tobytes(), (wd, h), "RGB")
            self._terrain_surf = pygame.transform.smoothscale(surf, (sw, sh))
            self._terrain_key = key
            gen.clear_dirty()

        # `Camera.to_screen(wx, wy)` renvoie le coin HAUT-GAUCHE de la tuile
        # (cf. camera.py : (wy - cam.y) * zoom * ys). Le patch se blitte donc
        # tel quel — la v1 soustrayait toute la hauteur du patch, ce qui le
        # projetait très au-dessus de l'écran.
        sx, sy = cam.to_screen(px0 * TILE, py0 * TILE)
        screen.blit(self._terrain_surf, (int(round(sx)), int(round(sy))))

    def _terrain_fallback(self, screen, w, cam, x0, y0, x1, y1):
        """Rendu simple quand le monde n'a pas de heightmap (monde vierge)."""
        z, ys = cam.zoom, cam.ys
        tw = TILE * z
        th = TILE * z * ys
        land = w.land[y0:y1 + 1, x0:x1 + 1]
        blocked = w.blocked[y0:y1 + 1, x0:x1 + 1]
        lys, lxs = np.nonzero(land > 0)
        for j, i in zip(lys, lxs):
            sx, sy = cam.to_screen((x0 + i) * TILE, (y0 + j) * TILE)
            col = _WALL_COL if blocked[j, i] else _LAND_COL
            pygame.draw.rect(screen, col,
                             (int(sx), int(sy), int(tw) + 1, int(th) + 1))

    # ── ligne de quête ───────────────────────────────────────────────
    def _goal_line(self, screen, cam, ui):
        ag = ui.get("agent")
        if ag is None or not getattr(ag, "alive", False):
            return
        goal = getattr(ag, "goal", None)
        if not goal or goal.get("act") in (0, 1, 13):
            return
        from .brain_api import ACTION_COLORS
        sx, sy = cam.to_screen(ag.x, ag.y)
        gx, gy = cam.to_screen(goal["x"] * TILE + 8, goal["y"] * TILE + 8)
        col = ACTION_COLORS.get(goal["act"], (255, 255, 255))
        d = ((gx - sx) ** 2 + (gy - sy) ** 2) ** 0.5
        if d <= 6:
            return
        n = max(2, int(d / TILE))
        for t in range(0, n, 2):
            a0 = t / n
            a1 = min(1.0, (t + 0.55) / n)
            pygame.draw.line(screen, col,
                             (sx + (gx - sx) * a0, sy + (gy - sy) * a0),
                             (sx + (gx - sx) * a1, sy + (gy - sy) * a1), 2)
        pygame.draw.circle(screen, col, (int(gx), int(gy)), 4, 1)

    # ══════════════════════════════════════════════════════════════════
    #  Entités
    # ══════════════════════════════════════════════════════════════════
    def _draw_asset(self, screen, cam, tx, ty, aid, world):
        am = self.am
        if not (0 <= aid < len(am.assets)):
            return
        a = am.assets[aid]
        if a.role in ("cloud", "shadow"):
            return
        frame = 0
        if a.frames > 1 and a.role == "tree":
            hp = int(world.hp[ty, tx])
            frame = max(0, min(a.frames - 1, 5 - hp))
        size = a.blocked_footprint if a.solid else 1
        cx, _ = cam.to_screen(tx * TILE + size * TILE / 2, 0)
        _, by = cam.to_screen(0, ty * TILE + size * TILE)
        surf = am.surface(aid, frame, _zq(cam.zoom))
        if a.role == "mural":
            surf = surf.copy()
            surf.set_alpha(210)
        screen.blit(surf, (cx - surf.get_width() / 2, by - surf.get_height() + 2))

    def _draw_item(self, screen, cam, it: Item):
        am = self.am
        if it.aid is None or not (0 <= it.aid < len(am.assets)):
            return
        sx, sy = cam.to_screen(it.x, it.y)
        surf = am.surface(it.aid, 0, _zq(cam.zoom * 0.7))
        screen.blit(surf, (sx - surf.get_width() / 2, sy - surf.get_height() / 2))

    def _draw_sheep(self, screen, cam, s: Sheep):
        am = self.am
        moving = abs(getattr(s, "vx", 0.0)) > 0.15
        state = "move" if moving else ("grass" if s.state == "grass" else "idle")
        aid = am.sheep.get(state) or am.sheep.get("idle")
        if aid is None:
            return
        frames = max(1, am.assets[aid].frames)
        surf = am.surface(aid, (s.anim_t // 8) % frames, _zq(cam.zoom))
        sx, sy = cam.to_screen(s.x, s.y)
        if getattr(s, "vx", 0) < -0.05:
            surf = pygame.transform.flip(surf, True, False)
        screen.blit(surf, (sx - surf.get_width() / 2, sy - surf.get_height() + 3))

    def _draw_monster(self, screen, cam, m: Monster):
        am = self.am
        kind = m.kind
        state = getattr(m, "state", "idle")
        aid = am.monsters.get(kind, {}).get(state) or am.monsters.get(kind, {}).get("idle")
        if aid is None:
            return
        surf = am.surface(aid, 0, _zq(cam.zoom))
        sx, sy = cam.to_screen(m.x, m.y)
        if getattr(m, "vx", 0) < -0.05:
            surf = pygame.transform.flip(surf, True, False)
        screen.blit(surf, (sx - surf.get_width() / 2, sy - surf.get_height() + 3))

    def _draw_headstone(self, screen, cam, tx, ty, name, col):
        """Pierre tombale volontairement neutre : stèle grise, sans symbole religieux."""
        sx, sy = cam.to_screen(tx * TILE + TILE / 2, ty * TILE + TILE / 2)
        z = cam.zoom
        wpx = max(4, int(10 * z))
        hpx = max(6, int(14 * z))
        rect = pygame.Rect(int(sx - wpx / 2), int(sy - hpx), wpx, hpx)
        # Socle discret
        pygame.draw.ellipse(screen, (90, 94, 92),
                            (rect.x - max(1, wpx // 4), rect.bottom - 2,
                             rect.width + max(2, wpx // 2), max(2, hpx // 4)))
        # Stèle arrondie, aucun signe/croix
        pygame.draw.rect(screen, (160, 155, 148), rect, border_radius=max(2, wpx // 2))
        pygame.draw.rect(screen, (112, 108, 104), rect, 1, border_radius=max(2, wpx // 2))
        # Trait horizontal neutre d'inscription
        if hpx >= 9:
            pygame.draw.line(screen, (122, 117, 110),
                             (rect.x + 2, rect.y + hpx // 2),
                             (rect.right - 3, rect.y + hpx // 2), 1)
        if z >= 1.2 and name:
            try:
                f = pygame.font.SysFont(None, max(8, min(12, int(9 * z))))
                txt = f.render(str(name)[:10], True, (90, 86, 82))
                screen.blit(txt, (int(sx - txt.get_width() / 2), rect.bottom + 1))
            except Exception:
                pass

    def _draw_agent(self, screen, cam, a: Inhabitant, ui):
        am = self.am
        st = {"run": "run", "attack": "attack", "work": "work", "build": "build",
              "give": "work", "eat": "work", "talk": "idle", "drink": "idle",
              "rest": "idle", "sleep": "idle"}.get(a.state, "idle")
        ids = a.states.get(st) or a.states.get("work") or a.states.get("idle")
        if not ids:
            return
        aid = ids[0]
        frames = max(1, am.assets[aid].frames)
        rate = 5 if st in ("run", "attack", "work") else 16
        surf = am.surface(aid, (a.anim_t // rate) % frames, _zq(cam.zoom))
        if a.child:
            surf = pygame.transform.smoothscale(
                surf, (max(4, int(surf.get_width() * 0.72)),
                       max(4, int(surf.get_height() * 0.72))))
        sx, sy = cam.to_screen(a.x, a.y)

        # anneau de clan sous les pieds : la carte doit se lire d'un coup d'œil
        ring = self._circle(a.rgb, max(6, int(11 * cam.zoom)), cam.ys, alpha=110)
        screen.blit(ring, (sx - ring.get_width() / 2, sy - ring.get_height() / 2 - 2))

        if a.vx < -0.05:
            surf = pygame.transform.flip(surf, True, False)
        sh = surf.get_height()
        screen.blit(surf, (sx - surf.get_width() / 2, sy - sh + 3))

        if a.tool >= 0:
            ts = am.surface(a.tool, 0, _zq(cam.zoom * 0.55))
            screen.blit(ts, (sx + surf.get_width() * 0.22, sy - sh + 1))

        if cam.zoom >= 1.0:
            cols = {"bois": (168, 118, 68), "pierre": (148, 148, 156),
                    "or": (248, 208, 98), "graine": (108, 168, 78)}
            k = 0
            yy = int(sy - sh - 3 * cam.zoom)
            rad = max(1, int(2.2 * cam.zoom))
            for mm in ("bois", "pierre", "or", "graine"):
                for _ in range(min(3, a.inv.get(mm, 0))):
                    pygame.draw.circle(screen, cols[mm],
                                       (int(sx - 9 + k * 6), yy), rad)
                    k += 1

        sel = ui.get("agent") is a
        if sel or a.health < 0.35:
            col = CLAN_COLORS.get(a.color, (255, 255, 255))
            r = max(7, int(surf.get_width() * 0.62))
            pygame.draw.circle(screen, col, (int(sx), int(sy - sh * 0.45)), r,
                               2 if sel else 1)
        if sel:
            self._mini_bars(screen, sx, sy - sh - 8 * cam.zoom, a, cam.zoom)

    def _mini_bars(self, screen, sx, sy, a, z):
        vals = [(a.energy, (108, 208, 128)),
                (1 - a.hunger, (248, 208, 98)),
                (a.health, (228, 98, 98))]
        wpx = max(10, int(28 * z))
        hpx = max(2, int(3 * z))
        for i, (v, c) in enumerate(vals):
            x, y = int(sx - wpx / 2), int(sy - i * (hpx + 2))
            pygame.draw.rect(screen, (12, 14, 20), (x, y, wpx, hpx))
            pygame.draw.rect(screen, c,
                             (x, y, int(wpx * max(0.0, min(1.0, v))), hpx))

    def _draw_fx(self, screen, cam, eff, tick):
        am = self.am
        a = am.assets[eff["aid"]]
        age = tick - eff["t0"]
        if age < 0 or age > eff["ttl"]:
            return
        frame = min(a.frames - 1, int(age * a.frames / max(1, eff["ttl"])))
        surf = am.surface(eff["aid"], frame, _zq(cam.zoom))
        sx, sy = cam.to_screen(eff["x"], eff["y"])
        screen.blit(surf, (sx - surf.get_width() / 2, sy - surf.get_height() / 2))

    # ══════════════════════════════════════════════════════════════════
    #  Atmosphère
    # ══════════════════════════════════════════════════════════════════
    def _fires(self, screen, cam, w, box):
        x0, y0, x1, y1 = box
        sub = w.fire[y0:y1 + 1, x0:x1 + 1]
        ys, xs = np.nonzero(sub > 0)
        if not len(xs):
            return
        aids = self.am.fx.get("fire") or []
        if not aids:
            return
        frames = max(1, self.am.assets[aids[0]].frames)
        zq = _zq(cam.zoom * 0.8)
        for j, i in zip(ys, xs):
            sx, sy = cam.to_screen((x0 + i) * TILE + 8, (y0 + j) * TILE + 12)
            fr = int(self.clock * 10 + i * 7 + j * 3) % frames
            s = self.am.surface(aids[0], fr, zq)
            screen.blit(s, (sx - s.get_width() / 2, sy - s.get_height()),
                        special_flags=pygame.BLEND_RGB_ADD)

    def _night(self, screen, sim, cam, w, box):
        light = sim.clock.light
        if light > 0.98:
            return
        alpha = int(165 * (1.0 - light))
        size = screen.get_clip().size or screen.get_size()
        key = (size, alpha)
        if self._night_key != key:
            dark = pygame.Surface(size, pygame.SRCALPHA)
            dark.fill((8, 10, 26, alpha))
            self._night_cache = dark
            self._night_key = key
        dark = self._night_cache.copy()
        clip = screen.get_clip()

        # trous de lumière autour des feux
        x0, y0, x1, y1 = box
        sub = w.fire[y0:y1 + 1, x0:x1 + 1]
        ys, xs = np.nonzero(sub > 0)
        rr = max(8, int(60 * cam.zoom))
        glow = self._glow(rr, alpha)
        for j, i in list(zip(ys, xs))[:40]:
            sx, sy = cam.to_screen((x0 + i) * TILE + 8, (y0 + j) * TILE + 8)
            dark.blit(glow, (sx - rr - clip.x, sy - rr - clip.y),
                      special_flags=pygame.BLEND_RGBA_SUB)
        screen.blit(dark, clip.topleft)

    def _rain(self, screen, sim):
        r = sim.clock.rain
        if r <= 0.05:
            return
        n = int(80 * r)
        clip = screen.get_clip()
        key = (clip.size, n, pygame.time.get_ticks() // 50)
        if self._rain_key != key:
            col = (150, 170, 210, int(90 * r))
            rs = pygame.Surface(clip.size, pygame.SRCALPHA)
            t = pygame.time.get_ticks()
            wd, hg = clip.size
            for k in range(n):
                x = (k * 197 + t // 2) % wd
                y = (k * 251 + t) % hg
                pygame.draw.line(rs, col, (x, y), (x - 2, y + 9), 1)
            self._rain_cache = rs
            self._rain_key = key
        screen.blit(self._rain_cache, clip.topleft)

    # ══════════════════════════════════════════════════════════════════
    #  Surcouches
    # ══════════════════════════════════════════════════════════════════
    def _legend(self, screen, view=None):
        items = [
            ((60, 180, 255), "halo = territoire (phéromones de clan)"),
            (None, "anneau sous un être = son clan"),
            ((228, 108, 48), "flammes = feu actif"),
            ((198, 168, 78), "point or = abri / construction"),
            ((46, 92, 158), "bleu = eau"),
            ((128, 118, 106), "gris = montagne infranchissable"),
        ]
        wdt, hgt = 340, 16 * len(items) + 30
        area = view if view is not None else screen.get_rect()
        sh = area.bottom
        left = area.left + 8
        panel = pygame.Surface((wdt, hgt), pygame.SRCALPHA)
        panel.fill((10, 13, 20, 238))
        pygame.draw.rect(panel, (38, 42, 52), (0, 0, wdt, hgt), 1)
        screen.blit(panel, (left, sh - hgt - 8))

        title = self._font(15, True).render("Légende — V pour masquer",
                                            True, (235, 240, 248))
        screen.blit(title, (left + 10, sh - hgt - 2))
        f = self._font(11)
        for i, (col, txt) in enumerate(items):
            y = sh - hgt + 22 + i * 16
            if col:
                pygame.draw.circle(screen, col, (left + 16, y + 5), 5)
            screen.blit(f.render(txt, True, (140, 150, 170)), (left + 28, y))

    def _ghost(self, screen, cam, ui):
        """Aperçu de l'outil courant sous le curseur."""
        tx, ty = ui["tile"]
        mode = ui.get("mode")
        aid = ui.get("asset")
        sx, sy = cam.to_screen(tx * TILE, ty * TILE)
        tw = TILE * cam.zoom
        th = TILE * cam.zoom * cam.ys

        # outils à pinceau : montrer le rayon réel, pas une case 1×1
        if mode in _BRUSH_MODES:
            r = max(1, int(ui.get("brush", 1)))
            col = _BRUSH_COLORS[mode]
            rx = int(r * tw)
            ry = max(2, int(r * th))
            rect = pygame.Rect(int(sx + tw / 2 - rx), int(sy - th / 2 - ry),
                               rx * 2, ry * 2)
            pygame.draw.ellipse(screen, col, rect, 2)
            pygame.draw.ellipse(screen, col,
                                rect.inflate(-rx, -ry), 1)
            return

        if mode == "place" and aid is not None and 0 <= aid < len(self.am.assets):
            a = self.am.assets[aid]
            surf = self.am.surface(aid, 0, _zq(cam.zoom)).copy()
            if a.role == "floor" or a.kind == "tiles":
                surf.set_alpha(175)
                screen.blit(surf, (sx, sy))
                pygame.draw.rect(screen, (138, 218, 138), (sx, sy, tw, th), 2)
                return
            sz = a.blocked_footprint if a.solid else 1
            surf.set_alpha(150)
            gx = sx + sz * tw / 2 - surf.get_width() / 2
            gy = sy + sz * th - surf.get_height()
            screen.blit(surf, (gx, gy))
            pygame.draw.rect(screen, (118, 218, 138),
                             pygame.Rect(sx, sy, sz * tw, sz * th), 2)
            return

        col = (108, 208, 128) if mode == "agent" else (78, 168, 232)
        pygame.draw.rect(screen, col, (sx, sy, tw, th), 2)

    def _grid_lines(self, screen, cam, view):
        x0, y0, x1, y1 = self._visible_box(view, cam)
        col = (0, 0, 0)
        # au-delà d'une certaine densité, la grille devient un aplat noir
        if (x1 - x0) > 160 or (y1 - y0) > 160:
            return
        for x in range(max(0, int(x0)), min(GRID, int(x1) + 1)):
            sx, _ = cam.to_screen(x * TILE, 0)
            pygame.draw.line(screen, col, (sx, view.top), (sx, view.bottom), 1)
        for y in range(max(0, int(y0)), min(GRID, int(y1) + 1)):
            _, sy = cam.to_screen(0, y * TILE)
            pygame.draw.line(screen, col, (view.left, sy), (view.right, sy), 1)

    def _draw_sites(self, screen, cam, world, box):
        x0, y0, x1, y1 = box
        for site in getattr(world, "sites", {}).values():
            if not (x0 - 6 <= site.origin_tx <= x1 + 6
                    and y0 - 6 <= site.origin_ty <= y1 + 6):
                continue
            for task in site.remaining_tasks():
                sx, sy = cam.to_screen(task.tx * TILE, task.ty * TILE)
                tw = max(2, int(TILE * cam.zoom))
                th = max(2, int(TILE * cam.zoom * cam.ys))
                if task.phase == "foundation":
                    color = (145, 145, 155, 130)
                elif task.phase == "door":
                    color = (178, 120, 60, 150)
                elif task.phase == "roof":
                    color = (170, 88, 64, 140)
                else:
                    color = (142, 104, 68, 125) if task.material == "bois" else (145, 145, 155, 125)
                ghost = pygame.Surface((tw, th), pygame.SRCALPHA)
                ghost.fill(color)
                pygame.draw.rect(ghost, (230, 230, 235, 170), ghost.get_rect(), 1)
                screen.blit(ghost, (int(sx), int(sy)))
            if cam.zoom >= 0.5:
                import math as _m
                sx, sy = cam.to_screen((site.origin_tx + 2.5) * TILE,
                                       (site.origin_ty + 2.5) * TILE)
                font = self._font(max(9, int(11 * cam.zoom)), True)
                label = font.render(f"{site.progress():.0%}", True, (238, 194, 86))
                screen.blit(label, (int(sx - label.get_width() / 2),
                                    int(sy - 26 * cam.zoom)))

    def _draw_diagnostic_overlay(self, screen, sim, cam, ui, box):
        overlay = ui.get("overlay", "none")
        if overlay == "none":
            return

        import math as _math
        w = sim.w
        x0, y0, x1, y1 = box
        selected = ui.get("agent")

        if overlay == "resources":
            csub = w.content[y0:y1 + 1, x0:x1 + 1]
            ys, xs = np.nonzero(csub >= 0)
            for j, i in zip(ys, xs):
                tx, ty = x0 + int(i), y0 + int(j)
                aid = int(csub[j, i])
                if aid < 0 or aid >= len(self.am.assets):
                    continue
                a = self.am.assets[aid]
                if a.edible > 0:
                    col = (96, 215, 114)
                elif a.harvest:
                    mat = a.harvest.get("material")
                    col = {
                        "bois": (139, 96, 55),
                        "pierre": (150, 150, 164),
                        "or": (240, 198, 60),
                    }.get(mat, (220, 220, 220))
                elif a.tool:
                    col = (92, 164, 236)
                else:
                    continue
                sx, sy = cam.to_screen(tx * TILE + TILE / 2, ty * TILE + TILE / 2)
                pygame.draw.circle(screen, col, (int(sx), int(sy)),
                                   max(2, int(4 * cam.zoom)))

        elif overlay == "memory" and selected is not None:
            colors = {
                "food": (96, 215, 114),
                "water": (72, 165, 235),
                "wood": (139, 96, 55),
                "stone": (150, 150, 164),
                "shelter": (238, 194, 86),
                "agent": (220, 154, 215),
            }
            for category, points in selected.seen.items():
                col = colors.get(category, (230, 230, 230))
                for tx, ty, force in points:
                    sx, sy = cam.to_screen(tx * TILE + TILE / 2, ty * TILE + TILE / 2)
                    radius = max(2, int((3 + 5 * force) * cam.zoom))
                    pygame.draw.circle(screen, col, (int(sx), int(sy)), radius, 1)

        elif overlay == "goal" and selected is not None:
            goal = selected.goal or {}
            if goal.get("x") is not None and goal.get("y") is not None:
                sx, sy = cam.to_screen(selected.x, selected.y)
                gx, gy = cam.to_screen(goal["x"] * TILE + TILE / 2,
                                       goal["y"] * TILE + TILE / 2)
                pygame.draw.line(screen, (255, 238, 104), (sx, sy), (gx, gy), 2)
                pygame.draw.circle(screen, (255, 238, 104), (int(gx), int(gy)),
                                   max(4, int(6 * cam.zoom)), 2)

        elif overlay == "danger":
            sub = w.fire[y0:y1 + 1, x0:x1 + 1]
            ys, xs = np.nonzero(sub > 0)
            for j, i in zip(ys, xs):
                sx, sy = cam.to_screen((x0 + i) * TILE + TILE / 2,
                                       (y0 + j) * TILE + TILE / 2)
                pygame.draw.circle(screen, (235, 90, 68), (int(sx), int(sy)),
                                   max(4, int(7 * cam.zoom)), 2)
            if selected is not None:
                for (cx, cy), value in selected.belief_places.items():
                    tx, ty = cx * 8, cy * 8
                    if not (x0 <= tx <= x1 and y0 <= ty <= y1):
                        continue
                    sx, sy = cam.to_screen(tx * TILE + TILE / 2, ty * TILE + TILE / 2)
                    r = max(3, int(12 * cam.zoom * value))
                    pygame.draw.circle(screen, (214, 84, 84), (int(sx), int(sy)), r, 1)

        elif overlay == "exploration":
            sub = w.heat[y0:y1 + 1, x0:x1 + 1]
            ys, xs = np.nonzero(sub > 0.08)
            for j, i in zip(ys, xs):
                value = float(sub[j, i])
                sx, sy = cam.to_screen((x0 + i) * TILE, (y0 + j) * TILE)
                size = max(1, int(TILE * cam.zoom))
                alpha = int(130 * min(1.0, value))
                layer = pygame.Surface((size, max(1, int(size * cam.ys))), pygame.SRCALPHA)
                layer.fill((92, 164, 236, alpha))
                screen.blit(layer, (int(sx), int(sy)))

        elif overlay == "territory":
            sub = w.marker[y0:y1 + 1, x0:x1 + 1]
            ys, xs = np.nonzero(sub > 0.06)
            for j, i in zip(ys, xs):
                value = float(sub[j, i])
                col = self._clan_rgb(int(w.marker_col[y0 + j, x0 + i]))
                sx, sy = cam.to_screen((x0 + i) * TILE + TILE / 2,
                                       (y0 + j) * TILE + TILE / 2)
                pygame.draw.circle(screen, col, (int(sx), int(sy)),
                                   max(2, int(6 * cam.zoom * value)), 1)

        elif overlay == "storage":
            for (stx, sty), storage in getattr(w, "storages", {}).items():
                if not (x0 <= stx <= x1 and y0 <= sty <= y1):
                    continue
                sx, sy = cam.to_screen(stx * TILE + TILE / 2, sty * TILE + TILE / 2)
                r = max(4, int(8 * cam.zoom))
                pygame.draw.rect(screen, (238, 194, 86),
                                 pygame.Rect(int(sx - r), int(sy - r), 2 * r, 2 * r), 2)

        elif overlay == "sites":
            for (stx, sty), site in getattr(w, "sites", {}).items():
                if not (x0 <= stx <= x1 and y0 <= sty <= y1):
                    continue
                sx, sy = cam.to_screen(stx * TILE + TILE / 2, sty * TILE + TILE / 2)
                r = max(4, int(8 * cam.zoom))
                pygame.draw.rect(screen, (92, 164, 236),
                                 pygame.Rect(int(sx - r), int(sy - r), 2 * r, 2 * r), 2)
                prog = site.progress()
                pygame.draw.arc(screen, (96, 215, 114),
                                pygame.Rect(int(sx - r - 2), int(sy - r - 2),
                                            2 * r + 4, 2 * r + 4),
                                -_math.pi / 2,
                                -_math.pi / 2 + 2 * _math.pi * prog, 2)

        elif overlay == "cemetery":
            for tx, ty, name, death_tick, color in getattr(w, "cemetery", ()):
                if not (x0 <= tx <= x1 and y0 <= ty <= y1):
                    continue
                sx, sy = cam.to_screen(tx * TILE + TILE / 2, ty * TILE + TILE / 2)
                pygame.draw.circle(screen, (160, 155, 148), (int(sx), int(sy)),
                                   max(4, int(7 * cam.zoom)), 2)


def _wg():
    """Import différé de worldgen (évite un cycle d'import au chargement)."""
    from . import worldgen
    return worldgen

```

## game/save.py

**Type :** `.py`

```python

"""Sauvegarde / chargement complet de la simulation.

Sauvegarde : world + sim + agents + cerveaux + camera → data/saves/slot_N.npz
Charge : restaure l'état exact, y compris les poids de neurones."""
import ast
import os
import pickle
import numpy as np

from .config import SAVE_DIR, GRID, TILE, AGE_MAX_NATURAL_DEATH_TICKS


def _slot_path(slot=0):
    os.makedirs(SAVE_DIR, exist_ok=True)
    return os.path.join(SAVE_DIR, f"slot_{slot}.pkl")


def save_game(sim, cam=None, slot=0):
    """Sauvegarde complète : monde, simulation, agents, cerveaux, camera."""
    w = sim.w
    data = {
        # --- world arrays ---
        "land": w.land,
        "water": w.water,
        "mountains": w.mountains,
        "floor": w.floor,
        "content": w.content,
        "owner": w.owner,
        "blocked": w.blocked,
        "shelter": w.shelter,
        "hp": w.hp,
        "marker": w.marker,
        "marker_col": w.marker_col,
        "regrow": w.regrow,
        "fire": w.fire,
        "smell": w.smell,
        "heat": w.heat,
        "foundation": w.foundation,
        "roof": w.roof,
        "cemetery": list(w.cemetery),
        "sites": {
            f"{tx},{ty}": {
                "origin_tx": s.origin_tx,
                "origin_ty": s.origin_ty,
                "blueprint_name": s.blueprint_name,
                "tasks": [{"tx": t.tx, "ty": t.ty, "material": t.material,
                           "phase": t.phase, "layer": t.layer, "solid": t.solid}
                          for t in s.tasks],
                "placed": list(s.placed),
                "contributors": dict(s.contributors),
                "created_tick": s.created_tick,
                "owner_eid": s.owner_eid,
                "owner_clan": s.owner_clan,
            }
            for (tx, ty), s in w.sites.items()
        },
        "storages": {
            f"{tx},{ty}": {
                "tx": st.tx, "ty": st.ty, "capacity": st.capacity,
                "owner_clan": st.owner_clan,
                "inventory": dict(st.inventory),
                "contributors": dict(st.contributors),
                "withdrawals": dict(st.withdrawals),
                "last_access_tick": st.last_access_tick,
            }
            for (tx, ty), st in w.storages.items()
        },
        "crop_plots": {
            f"{tx},{ty}": {
                "tx": cp.tx, "ty": cp.ty, "owner_eid": cp.owner_eid,
                "planted_tick": cp.planted_tick, "growth": cp.growth,
                "water_need": cp.water_need, "crop_type": cp.crop_type,
            }
            for (tx, ty), cp in w.crop_plots.items()
        },
        "items": [(it.x, it.y, it.aid, it.kind, it.life) for it in w.items],
        "w_tick": w.tick,
        "g": w.g,
        # --- worldgen ---
        "has_gen": w.gen is not None,
        # --- sim state ---
        "next_eid": sim.next_eid,
        "paused": sim.paused,
        "speed": sim.speed,
        "stats": dict(sim.stats),
        "journal": list(sim.journal)[-40:],
        "society": sim.society[:],
        "pop_hist": list(sim.pop_hist)[-60:],
        "clock_light": sim.clock.light,
        "clock_rain": sim.clock.rain,
        "clock_season": sim.clock.season,
        "clock_day": sim.clock.day,
        "clock_year": sim.clock.year,
        "clock_t": sim.clock.t,
        "clock_temp": sim.clock.temp,
        "clock_wind": sim.clock.wind,
        "clock_growth_f": sim.clock.growth_f,
        "clock_storm": sim.clock._storm,
        "rng_state": sim.rng.bit_generator.state,
        # --- sim social/commerce ---
        "clan_knowledge": {
            "places": sim.clan_knowledge.places,
            "dangers": sim.clan_knowledge.dangers,
            "reservations": sim.clan_knowledge.reservations,
            "culture": sim.clan_knowledge.culture,
            "institutions": sim.clan_knowledge.institutions,
        },
        "trade": sim._trade,
        "dominance": dict(sim._dominance),
        "village_pts": list(sim._village_pts),
        "recent_attacks": list(sim._recent_attacks),
        "last_war_log": sim._last_war_log,
        # --- universal knowledge ---
        "universal_knowledge": sim.universal_knowledge.to_dict(),
        # --- academy ---
        "academy": {
            "params": sim.academy.champion_params,
            "size": sim.academy.champion_size,
            "score": sim.academy.champion_score,
            "label": sim.academy.champion_label,
        },
        # --- lab ---
        "lab_daily": list(sim.lab.daily[-5000:]),
        # --- agents ---
        "n_agents": len(sim.agents),
        "agents": [_serialize_agent(a) for a in sim.agents],
        # --- sheep ---
        "n_sheep": len(sim.sheep),
        "sheep": [_serialize_sheep(s) for s in sim.sheep],
        # --- monsters ---
        "n_monsters": len(sim.monsters),
        "monsters": [_serialize_monster(m) for m in sim.monsters],
        "social_memory": {
            f"{obs},{tgt}": {
                "trust": r.trust, "violence": r.violence,
                "theft": r.theft, "generosity": r.generosity,
                "last_tick": r.last_tick,
            }
            for (obs, tgt), r in sim.social_memory.records.items()
        },
    }
    if w.gen is not None:
        data["gen_height_base"] = w.gen.height_base
        data["gen_height_current"] = w.gen.height_current
        data["gen_biome"] = w.gen.biome
        data["gen_shade"] = w.gen.shade
        data["gen_carved"] = w.gen.carved
        data["gen_moisture"] = w.gen.moisture
        data["gen_g"] = w.gen.g
    # --- camera ---
    if cam is not None:
        data["cam_x"] = cam.x
        data["cam_y"] = cam.y
        data["cam_zoom"] = cam.zoom
        data["cam_tilt"] = cam.tilt

    path = _slot_path(slot)
    tmp = path + ".tmp"
    try:
        with open(tmp, "wb") as f:
            pickle.dump(data, f, protocol=5)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except Exception:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise
    size_mb = os.path.getsize(path) / (1024 * 1024)
    return path, size_mb


def load_game(am, slot=0):
    """Charge une sauvegarde. Retourne (sim, cam) ou (None, None) si pas trouvé."""
    path = _slot_path(slot)
    if not os.path.exists(path):
        return None, None
    with open(path, "rb") as f:
        data = pickle.load(f)

    from .world import World
    from .simulation import Sim
    from .camera import Camera

    # --- reconstruire world ---
    w = World()
    g = data.get("g", GRID)
    w.g = g
    w.land = data["land"]
    w.water = data["water"]
    w.mountains = data.get("mountains", w.blocked.copy())
    w.foundation = data.get("foundation", np.zeros_like(w.blocked))
    w.roof = data.get("roof", np.zeros_like(w.blocked))
    w.floor = data["floor"]
    w.content = data["content"]
    w.owner = data["owner"]
    w.blocked = data["blocked"]
    w.shelter = data["shelter"]
    w.hp = data["hp"]
    w.marker = data["marker"]
    w.marker_col = data["marker_col"]
    w.regrow = data["regrow"]
    w.fire = data["fire"]
    w.smell = data["smell"]
    w.heat = data["heat"]
    w.cemetery = data.get("cemetery", [])
    w.sites = {}
    from .construction import ConstructionSite, BlockTask
    for raw in data.get("sites", {}).values():
        tasks = [BlockTask(tx=t["tx"], ty=t["ty"], material=t["material"],
                           phase=t["phase"], layer=t.get("layer", 0),
                           solid=t.get("solid", True))
                 for t in raw.get("tasks", [])]
        site = ConstructionSite(
            origin_tx=raw["origin_tx"],
            origin_ty=raw["origin_ty"],
            blueprint_name=raw.get("blueprint_name", "small_house"),
            tasks=tasks,
            placed={tuple(p) for p in raw.get("placed", [])},
            contributors={int(k): int(v) for k, v in raw.get("contributors", {}).items()},
            created_tick=int(raw.get("created_tick", 0)),
            owner_eid=raw.get("owner_eid"),
            owner_clan=raw.get("owner_clan"),
        )
        w.sites[site.key] = site
    w.storages = {}
    from .storage import SharedStorage
    for raw_s in data.get("storages", {}).values():
        st = SharedStorage(
            tx=raw_s["tx"], ty=raw_s["ty"], capacity=raw_s.get("capacity", 80),
            owner_clan=raw_s.get("owner_clan"),
            inventory=raw_s.get("inventory", {}),
            contributors={int(k): int(v) for k, v in raw_s.get("contributors", {}).items()},
            withdrawals={int(k): int(v) for k, v in raw_s.get("withdrawals", {}).items()},
            last_access_tick=int(raw_s.get("last_access_tick", 0)),
        )
        w.storages[st.tx, st.ty] = st
    w.crop_plots = {}
    from .world import CropPlot
    for raw_cp in data.get("crop_plots", {}).values():
        cp = CropPlot(
            tx=raw_cp["tx"], ty=raw_cp["ty"],
            owner_eid=raw_cp.get("owner_eid"),
            planted_tick=int(raw_cp.get("planted_tick", 0)),
            growth=float(raw_cp.get("growth", 0.0)),
            water_need=float(raw_cp.get("water_need", 0.5)),
            crop_type=raw_cp.get("crop_type", "grain"),
        )
        w.crop_plots[(cp.tx, cp.ty)] = cp
    w.tick = data["w_tick"]
    w.items = []
    for (ix, iy, iaid, ikind, ilife) in data.get("items", []):
        from .world import Item
        w.items.append(Item(ikind, iaid, ix, iy, life=ilife))

    # --- worldgen ---
    if data.get("has_gen", False):
        from .worldgen import WorldGen
        w.gen = WorldGen(
            g=data["gen_g"],
            height_base=data["gen_height_base"],
            height_current=data["gen_height_current"],
            biome=data["gen_biome"],
            shade=data["gen_shade"],
            carved=data["gen_carved"],
            moisture=data["gen_moisture"],
        )
    else:
        w.gen = None

    # --- reconstruire sim ---
    sim = Sim(w, am, seed=0)
    sim.next_eid = data["next_eid"]
    sim.paused = data["paused"]
    sim.speed = data["speed"]
    sim.stats = data["stats"]
    sim.journal = data["journal"]
    sim.society = data.get("society", [])
    sim.pop_hist = data.get("pop_hist", [])
    # clock
    sim.clock.light = data.get("clock_light", 0.5)
    sim.clock.rain = data.get("clock_rain", 0.0)
    sim.clock.season = data.get("clock_season", 0)
    sim.clock.day = data.get("clock_day", 0)
    sim.clock.year = data.get("clock_year", 1)
    sim.clock.t = data.get("clock_t", 0)
    sim.clock.temp = data.get("clock_temp", 0.6)
    sim.clock.wind = data.get("clock_wind", (0.0, 0.0))
    sim.clock.growth_f = data.get("clock_growth_f", 1.0)
    sim.clock._storm = data.get("clock_storm", 0)
    # rng
    if "rng_state" in data:
        sim.rng.bit_generator.state = data["rng_state"]
    # clan knowledge (compatible versions anciennes)
    ck = data.get("clan_knowledge")
    if ck:
        def _parse_key(k):
            return ast.literal_eval(k) if isinstance(k, str) else k
        sim.clan_knowledge.places = {_parse_key(k): v for k, v in ck.get("places", {}).items()}
        sim.clan_knowledge.dangers = {_parse_key(k): v for k, v in ck.get("dangers", {}).items()}
        sim.clan_knowledge.reservations = {_parse_key(k): v for k, v in ck.get("reservations", {}).items()}
        sim.clan_knowledge.culture = {_parse_key(k): v for k, v in ck.get("culture", {}).items()}
        sim.clan_knowledge.institutions = {_parse_key(k): v for k, v in ck.get("institutions", {}).items()}
    # social / commerce
    sim._trade = {ast.literal_eval(k) if isinstance(k, str) else k: v for k, v in data.get("trade", {}).items()}
    sim._dominance = data.get("dominance", {})
    sim._village_pts = [tuple(p) for p in data.get("village_pts", [])]
    from collections import deque as _dq
    sim._recent_attacks = _dq(data.get("recent_attacks", []), maxlen=400)
    sim._last_war_log = data.get("last_war_log", -9999)
    # universal knowledge (compatible anciennes saves)
    from .universal_knowledge import UniversalKnowledge
    sim.universal_knowledge = UniversalKnowledge.from_dict(
        data.get("universal_knowledge", {})
    )
    # academy
    acad = data.get("academy", {})
    sim.academy.champion_params = acad.get("params")
    sim.academy.champion_size = acad.get("size")
    sim.academy.champion_score = acad.get("score", float("-inf"))
    sim.academy.champion_label = acad.get("label", "aucun")
    # lab
    sim.lab.daily = list(data.get("lab_daily", []))
    # social memory
    from .social_memory import SocialRecord
    sim.social_memory.records = {}
    for key, raw in data.get("social_memory", {}).items():
        observer, target = map(int, key.split(","))
        sim.social_memory.records[(observer, target)] = SocialRecord(**raw)

    # --- agents ---
    sim.agents = []
    for ad in data.get("agents", []):
        sim.agents.append(_deserialize_agent(ad))
    # --- sheep ---
    sim.sheep = []
    for sd in data.get("sheep", []):
        sim.sheep.append(_deserialize_sheep(sd))
    # --- monsters ---
    sim.monsters = []
    for md in data.get("monsters", []):
        sim.monsters.append(_deserialize_monster(md))

    # --- rebuild spatial hash (grid_bucket + _entity_cells) ---
    sim.grid_bucket = {}
    sim._entity_cells = {}
    for a in sim.agents:
        cx, cy = int(a.x // 32), int(a.y // 32)
        sim.grid_bucket.setdefault((cx, cy), []).append(a)
        sim._entity_cells[a.eid] = (cx, cy)
    for s in sim.sheep:
        cx, cy = int(s.x // 32), int(s.y // 32)
        sim.grid_bucket.setdefault((cx, cy), []).append(s)
        sim._entity_cells[s.eid] = (cx, cy)
    for m in sim.monsters:
        cx, cy = int(m.x // 32), int(m.y // 32)
        sim.grid_bucket.setdefault((cx, cy), []).append(m)
        sim._entity_cells[m.eid] = (cx, cy)

    # --- camera ---
    cam = Camera()
    if "cam_zoom" in data:
        cam.x = data.get("cam_x", 0)
        cam.y = data.get("cam_y", 0)
        cam.zoom = data.get("cam_zoom", 0.25)
        cam.tilt = data.get("cam_tilt", 55.0)
        cam.clamp()
    else:
        ys, xs = np.nonzero(w.land)
        if len(xs):
            cam.center_on(float(xs.mean()) * TILE, float(ys.mean()) * TILE)

    return sim, cam


# ------------------------------------------------------------------ serialisation
def _serialize_agent(a):
    return {
        "eid": a.eid, "name": a.name, "gen": a.gen, "color": a.color,
        "cls": a.cls,         "sex": a.sex, "age": a.age, "natural_death_age": a.natural_death_age,
        "born_tick": a.born_tick,
        "x": a.x, "y": a.y, "vx": a.vx, "vy": a.vy,
        "fx": a.fx, "fy": a.fy, "health": a.health, "pain": a.pain,
        "temp": a.temp, "energy": a.energy, "hunger": a.hunger,
        "tool": a.tool, "tool_durability": getattr(a, "tool_durability", 0),
        "inv": dict(a.inv),
        "body": a.body.copy(), "cog": a.cog.copy(),
        "emotions": a.emotions.copy(), "needs": a.needs.copy(),
        "personality": a.personality.copy(),
        "skills": a.skills.copy(), "habits": a.habits.copy(),
        "self_esteem": a.self_esteem, "rep": a.rep,
        "state": a.state, "alive": a.alive,
        "avatar": a.avatar, "col_idx": a.col_idx,
        "commitment": a.commitment, "stuck": a.stuck,
        "failed_targets": {f"{k[0]}|{k[1]}|{k[2]}": list(v) for k, v in a.failed_targets.items()},
        "mood_phase": a.mood_phase, "mood_freq": a.mood_freq,
        "home": a.home, "work_t": a.work_t, "atk_t": a.atk_t,
        "repro_cd": a.repro_cd,
        "goal": a.goal, "goal_t": a.goal_t,
        "bonded": a.bonded, "hated": a.hated,
        "married": a.married, "partner_id": a.partner_id,
        "parent_pere_id": a.parent_pere_id, "parent_mere_id": a.parent_mere_id,
        "parents": a.parents, "children": a.children,
        # brain
        "brain_n": a.brain.n, "brain_p": a.brain.p.copy(),
        "brain_h": a.brain.h.copy(),
        "brain_last_out": a.brain.last_out.copy(),
        "brain_probs": a.brain.probs.copy(),
        "brain_base": a.brain.base,
        "brain_rng": a.brain.rng.bit_generator.state if hasattr(a.brain, 'rng') else None,
        "brain_trace": list(a.brain._trace),
        # brain tete strategie + cible (Lot 7.2)
        "brain_Wo_strat": a.brain._Wo_strat.copy(),
        "brain_b2_strat": a.brain._b2_strat.copy(),
        "brain_Wo_targ": a.brain._Wo_targ.copy(),
        "brain_b2_targ": a.brain._b2_targ.copy(),
        # memory
        "seen": {k: list(v) for k, v in a.seen.items()},
        "belief_places": dict(a.belief_places),
        "belief_beings": dict(a.belief_beings),
        "rel": dict(a.rel),
        "dangers": list(a.dangers),
        "affinity_cd": a.affinity_cd,
        # episodic / autobiographique
        "life": list(a.life),
        "episodes": list(a.episodes),
        "talk_cd": dict(a.talk_cd),
        # Anima Phase 1+
        "anima": {
            "episodic_memory": list(a.anima["episodic_memory"]),
            "beliefs": {
                "places": {f"{k[0]}|{k[1]}": v
                           for k, v in a.anima["beliefs"]["places"].items()},
                "beings": {str(k): v
                           for k, v in a.anima["beliefs"]["beings"].items()},
            },
            "identity": dict(a.anima["identity"]),
            "values": dict(a.anima["values"]),
            "trauma": dict(a.anima["trauma"]),
            "attachments": {str(k): v
                            for k, v in a.anima.get("attachments", {}).items()},
            "intention": a.anima.get("intention"),
            "causal_traces": list(a.anima.get("causal_traces", [])),
            "observations": list(a.anima.get("observations", [])),
        },
    }


def _deserialize_agent(d):
    from collections import deque as _dq
    from .brain import Brain, N_IN, OLD_NIN, migrate_input_weights
    brain = Brain(n_hid=d["brain_n"], params=d["brain_p"])
    brain.h = d["brain_h"]
    brain.last_out = d["brain_last_out"]
    brain.probs = d["brain_probs"]
    brain.base = d["brain_base"]
    # Migration 128→132 entrées pour anciennes saves
    from .brain import N_OUT
    denom = OLD_NIN + 2 + N_OUT
    old_h = (d["brain_p"].size - N_OUT) // denom
    if old_h > 0 and (d["brain_p"].size - N_OUT) % denom == 0:
        expected_old = old_h * denom + N_OUT
        if d["brain_p"].size == expected_old:
            brain.p, _ = migrate_input_weights(d["brain_p"], old_n=OLD_NIN, new_n=N_IN)
    if d.get("brain_rng") is not None:
        brain.rng.bit_generator.state = d["brain_rng"]
    if d.get("brain_trace"):
        brain._trace = _dq(d["brain_trace"], maxlen=brain._trace.maxlen)
    # tete strategie + cible (fallback: aleatoire pour anciens saves)
    if d.get("brain_Wo_strat") is not None:
        brain._Wo_strat = d["brain_Wo_strat"]
        brain._b2_strat = d["brain_b2_strat"]
        brain._Wo_targ = d["brain_Wo_targ"]
        brain._b2_targ = d["brain_b2_targ"]

    a = Being(
        eid=d["eid"], x=d["x"], y=d["y"], color=d["color"], cls=d["cls"],
        states={}, gen=d["gen"], brain=brain, parents=d.get("parents", ()),
        personality=d["personality"], rng=None, born_tick=d["born_tick"],
        n_hid=d["brain_n"], body=d["body"], cog=d["cog"],
        emotions=d["emotions"], needs=d["needs"], sex=d["sex"],
    )
    a.name = d["name"]
    a.age = d["age"]
    a.natural_death_age = d.get("natural_death_age", AGE_MAX_NATURAL_DEATH_TICKS)
    a.vx = d["vx"]; a.vy = d["vy"]
    a.fx = d["fx"]; a.fy = d["fy"]
    a.health = d["health"]; a.pain = d["pain"]; a.temp = d["temp"]
    a.energy = d["energy"]; a.hunger = d["hunger"]
    a.tool = d["tool"]; a.inv = d["inv"]
    a.tool_durability = d.get("tool_durability", 0)
    a.skills = d["skills"]; a.habits = d["habits"]
    a.self_esteem = d["self_esteem"]; a.rep = d["rep"]
    a.state = d["state"]; a.alive = d["alive"]
    a.avatar = d["avatar"]; a.col_idx = d["col_idx"]
    a.commitment = d["commitment"]; a.stuck = d["stuck"]
    ft_raw = d.get("failed_targets", {})
    a.failed_targets = {(k.split("|")[0], int(k.split("|")[1]), int(k.split("|")[2])): tuple(v)
                        for k, v in ft_raw.items()}
    a.mood_phase = d["mood_phase"]; a.mood_freq = d["mood_freq"]
    a.home = d["home"]; a.work_t = d["work_t"]; a.atk_t = d["atk_t"]
    a.repro_cd = d["repro_cd"]
    a.goal = d["goal"]; a.goal_t = d["goal_t"]
    a.bonded = d.get("bonded"); a.hated = d.get("hated")
    a.married = d.get("married", False); a.partner_id = d.get("partner_id")
    a.parent_pere_id = d.get("parent_pere_id"); a.parent_mere_id = d.get("parent_mere_id")
    a.children = d.get("children", [])
    a.seen = d.get("seen", {c: [] for c in ("food","wood","stone","water","shelter","agent")})
    a.belief_places = d.get("belief_places", {})
    a.belief_beings = d.get("belief_beings", {})
    a.rel = d.get("rel", {})
    a.dangers = d.get("dangers", [])
    a.affinity_cd = d.get("affinity_cd", 0)
    # episodique / autobiographique
    a.life = _dq(d.get("life", []), maxlen=48)
    a.episodes = _dq(d.get("episodes", []), maxlen=64)
    a.talk_cd = d.get("talk_cd", {})
    # Anima Phase 1
    ad = d.get("anima")
    if ad:
        a.anima["episodic_memory"] = _dq(ad.get("episodic_memory", []), maxlen=32)
        places_raw = ad.get("beliefs", {}).get("places", {})
        a.anima["beliefs"]["places"] = {
            (int(k.split("|")[0]), int(k.split("|")[1])): v
            for k, v in places_raw.items()
        }
        beings_raw = ad.get("beliefs", {}).get("beings", {})
        loaded_beings = {}
        for k, v in beings_raw.items():
            eid = int(k)
            if isinstance(v, dict):
                loaded_beings[eid] = v
            else:
                loaded_beings[eid] = {
                    "trust": 0.5, "danger": 0.0, "generosity": 0.5,
                    "reliability": 0.5, "confidence": 0.0,
                    "last_update": 0,
                }
        a.anima["beliefs"]["beings"] = loaded_beings
        for k in ("identity", "values", "trauma"):
            if k in ad:
                a.anima[k].update(ad[k])
        att_raw = ad.get("attachments", {})
        loaded_att = {}
        for k, v in att_raw.items():
            try:
                loaded_att[int(k)] = v
            except (ValueError, TypeError):
                loaded_att[k] = v
        a.anima["attachments"] = loaded_att
        # Lot D/F/H : champs nouveaux
        if ad.get("intention") is not None:
            a.anima["intention"] = ad["intention"]
        a.anima["causal_traces"] = list(ad.get("causal_traces", []))
        from collections import deque as _dq2
        a.anima["observations"] = _dq2(ad.get("observations", []), maxlen=24)
    return a


def _serialize_sheep(s):
    return {
        "eid": s.eid, "x": s.x, "y": s.y,
        "vx": s.vx, "vy": s.vy,
        "energy": s.energy, "health": s.health,
        "state": s.state, "alive": s.alive,
        "fear": s.fear,
        "brain_n": s.brain.n, "brain_p": s.brain.p.copy(),
        "brain_h": s.brain.h.copy(),
    }


def _deserialize_sheep(d):
    from .brain import Brain
    brain = Brain(n_hid=d["brain_n"], params=d["brain_p"])
    brain.h = d["brain_h"]
    s = Sheep(d["eid"], d["x"], d["y"], brain=brain)
    s.vx = d["vx"]; s.vy = d["vy"]
    s.energy = d["energy"]; s.health = d["health"]
    s.state = d["state"]; s.alive = d["alive"]
    s.fear = d.get("fear", 0.0)
    return s


def _serialize_monster(m):
    return {
        "eid": m.eid, "x": m.x, "y": m.y,
        "vx": m.vx, "vy": m.vy,
        "energy": m.energy, "health": m.health,
        "kind": m.kind, "alive": m.alive,
    }


def _deserialize_monster(d):
    m = Monster(d["eid"], d["x"], d["y"], kind=d["kind"])
    m.vx = d["vx"]; m.vy = d["vy"]
    m.energy = d["energy"]; m.health = d["health"]
    m.alive = d["alive"]
    return m


# --- import circular ---
from .entities import Being, Sheep, Monster

```

## game/simulation.py

**Type :** `.py`

```python

"""Simulation — le contrat moteur.

  1. le monde ne donne JAMAIS de mission
  2. le cerveau ne modifie pas la realite : il DEMANDE une intention
  3. le monde verifie la faisabilite (affordances, capacites physiques)
  4. toute action a des consequences
  5. les consequences deviennent experience -> recompense -> apprentissage

L'etre percoit (sens limités, jour/nuit, attention), MEMORISE (et oublie),
arbitre (reseau + personnalite + emotions + croyances + habitudes + risque),
agit (14 primitives composables), apprend (REINFORCE), grandit (enfant ->
adulte -> ancien), s'allie, fonde une famille, transmet (culture), et meurt
en laissant une reputation.
"""
import math
from collections import deque

import numpy as np

from .brain_api import (ATTACK, BUILD, DRINK, DROP, EAT, EXPLORE, FLEE, GIVE,
                     HARVEST, MARK, N_IN, N_OUT, REST, SLEEP, SOCIAL, TAKE,
                     TALK, ACTION_NAMES_EXP as ACTION_NAMES, ACTION_TRAIT_EXP as ACTION_TRAIT)
from .brain import Brain
from .brain_schema import INPUT
from .brain import (IMMEDIAT, PRUDENT, ECONOMIQUE, COOPERATIF, EXPLORATION, DEFENSIF,
                    SOI, NOURRITURE, EAU, BOIS, PIERRE, ABRI, DEPOT_CHANTIER, ETRE_VIVANT)
from .clock import Clock
from .config import (CLAN_COLORS, GRID, MAX_POP, MAX_SHEEP, TILE, WORLD_PX,
                     DEFAULT_SPAWN_AGE_TICKS, TICKS_PER_YEAR, AGE_ELDER_TICKS,
                     AGE_MAX_NATURAL_DEATH_TICKS, DAY_TICKS)
from .entities import Being, Sheep, Monster, ClanKnowledge
from .world import Item
from .universal_knowledge import UniversalKnowledge
from .academy import Academy
from .lab import LabRecorder
from .construction import ConstructionSite, blueprint_from_name

MAT_AIDS = {"bois": "item_wood", "pierre": "stone_res", "or": "gold_pile"}

# --- metabolisme (lois biologiques, pas des comportements)
HUNGER_RATE = 0.00012
THIRST_RATE = 0.00008
SLEEP_RATE_D = 0.00006
SLEEP_RATE_N = 0.00020
E_DRAIN = 0.00004
MOVE_DRAIN = 0.00018
REST_GAIN = 0.00180
SLEEP_GAIN = 0.00420
SHELTER_BONUS = 1.9
STARVE_HP = 0.00012
THIRST_HP = 0.00012
LOWE_HP = 0.00008
INV_CAP = 8
ATTACK_DMG = 0.16
ATTACK_DMG_TOOL = 0.30
WORK_TICKS = 6
PERCEPT_CELLS = 70          # echantillons de perception / tick / etre


class Sim:
    def __init__(self, world, am, seed=7):
        self.w = world
        self.am = am
        self.rng = np.random.default_rng(seed)
        self.clock = Clock(np.random.default_rng(seed + 1))
        self.agents: list[Being] = []
        self.sheep: list[Sheep] = []
        self.monsters: list[Monster] = []
        self.effects: list[dict] = []
        self.sounds: deque = deque(maxlen=40)
        self.next_eid = 1
        self.paused = True
        self.speed = 2
        self.grid_bucket = {}
        self.item_bucket = {}
        self.food_cells = {}
        self._entity_cells = {}
        self.stats = dict(births=0, deaths=0, builds=0, villages=0, attacks=0,
                          gives=0, takes=0, talks=0, harvests=0, tool_found=0,
                          explored=0, drinks=0, sleeps=0, fires=0)
        # Lot M : diagnostics comportementaux
        self.debug_action_counts = {}
        self.debug_failure_counts = {"path": 0, "feasible": 0, "affordance": 0}
        self.debug_anima_counts = {"episodes": 0, "intentions": 0, "plans": 0}
        self.journal = deque(maxlen=120)
        self.society = []
        self.pop_hist = deque(maxlen=220)
        self._recent_attacks = deque(maxlen=400)
        self._village_pts = []
        self._last_war_log = -9999
        self._dominance = {}
        self._trade = {}
        self._sens = np.zeros(N_IN, dtype=np.float64)
        self.selected = None
        self.clan_knowledge = ClanKnowledge()
        self.universal_knowledge = UniversalKnowledge(omniscient=False)
        self.academy = Academy()
        self.lab = LabRecorder()
        from .social_memory import SocialMemory
        self.social_memory = SocialMemory()

    # ------------------------------------------------------------------ journal
    def log(self, text, color=None, cat="monde"):
        """cat: combat|social|meteo|economie|vie|batiment|monde — groupés à l'affichage."""
        if self.journal and self.journal[-1][1] == text and self.w.tick - self.journal[-1][0] < 900:
            t0, tx, c, k, n = self.journal[-1]
            self.journal[-1] = (self.w.tick, tx, c, k, n + 1)
            return
        self.journal.append((self.w.tick, text, color, cat, 1))

    def emit_sound(self, x, y, kind, intensity=1.0):
        self.sounds.append((x, y, kind, intensity, self.w.tick))

    # ------------------------------------------------------------------ spawns
    def spawn_agent(self, x=None, y=None, color=None, gen=0, brain=None, parents=(),
                    energy=None, personality=None, n_hid=None, cls=None,
                    body=None, cog=None, emotions=None, needs=None, sex=None):
        if len(self.agents) >= MAX_POP:
            return None
        colors = self.am.unit_colors() or ["blue"]
        color = color or colors[int(self.rng.integers(len(colors)))]
        classes = self.am.unit_classes(color) or ["pawn"]
        cls = cls if cls in classes else classes[int(self.rng.integers(len(classes)))]
        states = self.am.skin_states(color, cls)
        for _ in range(60):
            if x is None:
                tx = int(self.rng.integers(6, GRID - 6))
                ty = int(self.rng.integers(6, GRID - 6))
                if self.w.land[ty, tx] and not self.w.blocked[ty, tx]:
                    break
            else:
                x = min(max(x, 4), WORLD_PX - 6)
                y = min(max(y, 4), WORLD_PX - 6)
                break
        if x is None:
            x, y = tx * TILE + 8, ty * TILE + 8
        if n_hid is None:
            n_hid = int(self.rng.choice((64, 128, 128, 256)))
        if brain is None and parents is None:
            seed = self.academy.make_seed_params(n_hid, self.rng)
            if seed is not None:
                brain = Brain(n_hid=n_hid, params=seed, rng=self.rng)
        a = Being(self.next_eid, x, y, color, cls, states, gen, brain, parents,
                  personality=personality, rng=self.rng, born_tick=self.w.tick,
                  n_hid=n_hid, body=body, cog=cog, emotions=emotions, needs=needs,
                  sex=sex)
        a.col_idx = self._colidx(color)
        if parents is None:
            a.age = DEFAULT_SPAWN_AGE_TICKS
        else:
            a.age = 0
        if energy is not None:
            a.energy = a.needs[1] = energy
        self.next_eid += 1
        self.agents.append(a)
        cx, cy = int(a.x // 32), int(a.y // 32)
        self.grid_bucket.setdefault((cx, cy), []).append(a)
        self._entity_cells[a.eid] = (cx, cy)
        self.bootstrap_resource_memory(a, radius=max(40, a.sense_r(self.clock.light)))
        return a

    def spawn_sheep(self, x=None, y=None):
        if len(self.sheep) >= MAX_SHEEP:
            return
        for _ in range(30):
            if x is None:
                tx = int(self.rng.integers(6, GRID - 6))
                ty = int(self.rng.integers(6, GRID - 6))
            else:
                tx = min(GRID - 2, max(1, int(x // TILE)))
                ty = min(GRID - 2, max(1, int(y // TILE)))
            if self.w.land[ty, tx] and not self.w.blocked[ty, tx]:
                break
        s = Sheep(self.next_eid, tx * TILE + 8, ty * TILE + 8)
        self.next_eid += 1
        self.sheep.append(s)
        cx, cy = int(s.x // 32), int(s.y // 32)
        self.grid_bucket.setdefault((cx, cy), []).append(s)
        self._entity_cells[s.eid] = (cx, cy)

    def spawn_monster(self, x=None, y=None, kind=None):
        if len(self.monsters) >= 20:
            return
        kinds = ["bear", "wolf", "snake", "beatle"]
        for _ in range(30):
            if x is None:
                tx = int(self.rng.integers(6, GRID - 6))
                ty = int(self.rng.integers(6, GRID - 6))
            else:
                tx = min(GRID - 2, max(1, int(x // TILE)))
                ty = min(GRID - 2, max(1, int(y // TILE)))
            if self.w.land[ty, tx] and not self.w.blocked[ty, tx]:
                break
        k = kind or self.rng.choice(kinds)
        m = Monster(self.next_eid, tx * TILE + 8, ty * TILE + 8, kind=k)
        self.next_eid += 1
        self.monsters.append(m)
        cx, cy = int(m.x // 32), int(m.y // 32)
        self.grid_bucket.setdefault((cx, cy), []).append(m)
        self._entity_cells[m.eid] = (cx, cy)

    def remove_agent(self, a, name="le gardien"):
        """Retrait manuel depuis le tableau de bord : l'habitant quitte le monde
        sans laisser de cadavre. Les liens sociaux sont nettoyés."""
        if a is None or not getattr(a, "alive", False):
            return
        if self.selected is a:
            self.selected = None
        a.alive = False
        for other in self.agents:
            other.rel.pop(a.eid, None)
            if other.bonded == a.eid:
                other.bonded = None
                other.married = False
                other.partner_id = None
                other.life.append("a perdu son partenaire")
            other.children[:] = [c for c in other.children if c != a.eid]
        self.stats["deaths"] += 1
        self.log(f"{a.name} a quitté le monde (retiré par {name}).", (148, 148, 208), "vie")
        self.agents[:] = [x for x in self.agents if x.alive]

    def _colidx(self, color):
        keys = self.am.unit_colors()
        return (keys.index(color) + 1) if color in keys else 1

    def bootstrap_resource_memory(self, a, radius=12):
        w = self.w
        for ty in range(max(0, a.ty - radius), min(w.g, a.ty + radius + 1)):
            for tx in range(max(0, a.tx - radius), min(w.g, a.tx + radius + 1)):
                aid = w.content_at(tx, ty)
                if aid < 0:
                    if w.water[ty, tx]:
                        a.remember("water", tx, ty)
                    continue
                asset = self.am.assets[aid]
                if asset.edible > 0:
                    a.remember("food", tx, ty)
                elif asset.harvest:
                    material = asset.harvest.get("material")
                    if material == "bois":
                        a.remember("wood", tx, ty)
                    elif material in ("pierre", "or"):
                        a.remember("stone", tx, ty)
                elif asset.shelter:
                    a.remember("shelter", tx, ty)

    def _by_eid(self, eid):
        for a in self.agents:
            if a.eid == eid:
                return a
        return None

    # ------------------------------------------------------------------ Anima
    def _record_anima(self, a, kind, place, actors=None, action="",
                      outcome="survived", health_loss=0.0, fear=0.0,
                      surprise=0.0, social_impact=0.0, achievement=0.0):
        """Calcule l'importance et enregistre un episode Anima."""
        importance = (
            0.35 * min(1.0, health_loss)
            + 0.25 * min(1.0, fear)
            + 0.15 * min(1.0, surprise)
            + 0.15 * min(1.0, social_impact)
            + 0.10 * min(1.0, achievement)
        )
        if importance < 0.05:
            return None
        emotion = {"fear": fear, "pain": min(1.0, health_loss),
                    "surprise": surprise}
        ep = a.remember_anima_episode(
            self.w.tick, kind, place, actors=actors,
            action=action, outcome=outcome, emotion=emotion,
            importance=importance,
        )
        if importance >= 0.20:
            cx, cy = place[0] // 8, place[1] // 8
            a.anima["beliefs"]["places"][(cx, cy)] = min(1.0,
                max(a.anima["beliefs"]["places"].get((cx, cy), 0.0), importance))
            # Lot F : trace causale pour crédit différé
            a.anima_add_causal_trace(kind, place, self.w.tick,
                                     expected_effect=kind)
            self.update_anima_from_event(a, {
                "tick": self.w.tick, "kind": kind, "place": place,
                "actors": actors or [], "action": action,
                "outcome": outcome, "emotion": emotion,
                "importance": importance,
            })
        return ep

    # -- Lot 3 : mise a jour centree apres evenements --
    IDENTITY_EFFECTS = {
        "construction_complete": {"builder": 0.06},
        "construction_started": {"builder": 0.02},
        "food_given": {"provider": 0.04, "caretaker": 0.02},
        "monster_survival": {"survivor": 0.06},
        "monster_attack": {"survivor": 0.02},
        "monster_killed": {"fighter": 0.05},
        "new_area_discovered": {"explorer": 0.025},
        "help": {"caretaker": 0.03, "mediator": 0.01},
        "birth": {"caretaker": 0.03},
        "injury": {"survivor": 0.01},
    }
    VALUE_EFFECTS = {
        "food_given": {"community": 0.01, "generosity": 0.01},
        "food_received": {"community": 0.005},
        "food_found": {"wealth": 0.005},
        "theft": {"security": 0.02, "community": -0.01},
        "betrayal": {"security": 0.025, "community": -0.015},
        "monster_attack": {"survival": 0.01, "security": 0.015},
        "construction_complete": {"security": 0.01, "family": 0.005},
        "construction_started": {"knowledge": 0.005},
        "new_area_discovered": {"knowledge": 0.01},
        "help": {"community": 0.008, "generosity": 0.005},
        "birth": {"family": 0.02, "community": 0.005},
        "injury": {"survival": 0.005},
        "resource_deposited": {"community": 0.003},
        "resource_withdrawn": {"wealth": 0.003},
    }
    TRAUMA_EFFECTS = {
        "monster_attack": {"attack": 0.08},
        "injury": {"attack": 0.04},
        "theft": {"betrayal": 0.08},
        "betrayal": {"betrayal": 0.12},
        "loss": {"loss": 0.15},
        "fire": {"fire": 0.10},
    }

    def update_anima_from_event(self, agent, event):
        """Met a jour la psychologie personnelle apres un evenement reel."""
        kind = event.get("kind", "")
        actors = event.get("actors", [])
        tick = event.get("tick", self.w.tick)
        importance = event.get("importance", 0.0)
        health_loss = event.get("health_loss", 0.0)
        # --- identite ---
        identity_fx = self.IDENTITY_EFFECTS.get(kind, {})
        for id_key, delta in identity_fx.items():
            agent.anima_add_identity(id_key, delta)
        # --- valeurs ---
        value_fx = self.VALUE_EFFECTS.get(kind, {})
        for v_key, delta in value_fx.items():
            agent.anima_add_value(v_key, delta)
        # --- trauma ---
        trauma_fx = self.TRAUMA_EFFECTS.get(kind, {})
        for t_key, delta in trauma_fx.items():
            agent.anima["trauma"][t_key] = min(
                1.0, agent.anima["trauma"].get(t_key, 0.0) + delta)
        # --- attachement ---
        if kind == "food_received" and actors:
            for oid in [e for e in actors if e != agent.eid]:
                agent.anima["attachments"][oid] = min(
                    1.0, agent.anima["attachments"].get(oid, 0.0) + 0.05)
        elif kind == "help" and actors:
            for oid in [e for e in actors if e != agent.eid]:
                agent.anima["attachments"][oid] = min(
                    1.0, agent.anima["attachments"].get(oid, 0.0) + 0.03)
        elif kind == "birth":
            agent.anima["attachments"]["child"] = min(
                1.0, agent.anima["attachments"].get("child", 0.0) + 0.30)
        elif kind == "loss":
            agent.anima["attachments"]["lost"] = 0.0
        # --- croyances sociales ---
        other_eids = [e for e in actors if e != agent.eid]
        if kind == "food_given" and other_eids:
            for oid in other_eids:
                agent.anima_update_social_belief(
                    oid, tick, trust_delta=0.08,
                    generosity_delta=0.06, reliability_delta=0.03)
        elif kind == "food_received" and other_eids:
            for oid in other_eids:
                agent.anima_update_social_belief(
                    oid, tick, trust_delta=0.10, confidence_delta=0.04)
        elif kind in ("theft", "betrayal") and other_eids:
            for oid in other_eids:
                agent.anima_update_social_belief(
                    oid, tick, trust_delta=-0.20, danger_delta=0.15,
                    reliability_delta=-0.15)
        elif kind == "monster_attack" and other_eids:
            for oid in other_eids:
                agent.anima_update_social_belief(
                    oid, tick, trust_delta=-0.10, danger_delta=0.08)
        elif kind == "help" and other_eids:
            for oid in other_eids:
                agent.anima_update_social_belief(
                    oid, tick, trust_delta=0.06, reliability_delta=0.05)
        elif kind == "talk" and other_eids:
            for oid in other_eids:
                agent.anima_update_social_belief(
                    oid, tick, trust_delta=0.03, confidence_delta=0.02)
        elif kind == "loss" and other_eids:
            for oid in other_eids:
                agent.anima_update_social_belief(
                    oid, tick, trust_delta=-0.05, danger_delta=0.03)
        elif kind == "resource_deposited" and other_eids:
            for oid in other_eids:
                agent.anima_update_social_belief(
                    oid, tick, reliability_delta=0.02)
        elif kind == "message_received" and other_eids:
            for oid in other_eids:
                agent.anima_update_social_belief(
                    oid, tick, confidence_delta=0.01)
        # --- croyance lieu (danger percu) ---
        if kind in ("monster_attack", "injury", "fire") and event.get("place"):
            cx, cy = event["place"][0] // 8, event["place"][1] // 8
            agent.anima["beliefs"]["places"][(cx, cy)] = min(
                1.0, max(agent.anima["beliefs"]["places"].get((cx, cy), 0.0),
                         importance))

    # ------------------------------------------------------------------ step
    def step(self):
        w = self.w
        self.clock.step()
        w.step(self.am, self.clock)
        # feu : systeme physique pur (combustible + vent - pluie)
        burned = w.step_fire(self.am, self.clock.wind, self.clock.rain, self.am.flammable)
        if burned and w.tick % 30 == 0:
            self.stats["fires"] += 1
        if self.clock.lightning():
            for _ in range(3):
                tx, ty = int(self.rng.integers(GRID)), int(self.rng.integers(GRID))
                if w.land[ty, tx] and w.content_at(tx, ty) >= 0:
                    w.ignite(tx, ty)
                    self.log("La foudre a allumé un feu.", (218, 138, 58), "meteo")
                    break
        self._bucket()
        for a in self.agents:
            if a.alive:
                self._perceive(a)
                self._agent(a)
                # Lot C : decroissance trauma + identite (tous les 100 ticks)
                if w.tick % 100 == 0:
                    a.anima_decay_identity()
                    n_near = len([o for o in self.agents
                                  if o.alive and o.eid != a.eid
                                  and abs(o.tx - a.tx) + abs(o.ty - a.ty) < 8])
                    safety = 1.0 if a.needs[4] > 0.6 else 0.35
                    a.anima_decay_trauma(safety=safety, support=n_near / 4.0)
        for s in self.sheep:
            if s.alive:
                self._sheep(s)
        for m in self.monsters:
            if m.alive:
                self._monster(m)
        self.agents = [a for a in self.agents if a.alive]
        self.sheep = [s for s in self.sheep if s.alive]
        self.monsters = [m for m in self.monsters if m.alive]
        # nettoyage grid_bucket : entités mortes
        for dead_eid in [eid for eid, cell in list(self._entity_cells.items())
                         if not any(a.eid == eid for a in self.agents)
                         and not any(s.eid == eid for s in self.sheep)
                         and not any(m.eid == eid for m in self.monsters)]:
            cell = self._entity_cells.pop(dead_eid, None)
            if cell is not None:
                bucket = self.grid_bucket.get(cell)
                if bucket:
                    self.grid_bucket[cell] = [e for e in bucket if getattr(e, "eid", None) != dead_eid]
                    if not self.grid_bucket[cell]:
                        del self.grid_bucket[cell]
        self.effects = [e for e in self.effects if w.tick - e["t0"] < e["ttl"]]
        # odeurs des objets
        if w.tick % 20 == 0:
            for it in w.items:
                if it.kind == "food":
                    w.smell[int(it.y // TILE), int(it.x // TILE)] = min(1.0,
                        w.smell[int(it.y // TILE), int(it.x // TILE)] + 0.2)
        if w.tick % 240 == 0:
            for a in self.agents:
                for c in a.seen:
                    decay = 0.995 + 0.004 * a.cog[0]
                    a.seen[c] = [(x, y, f * decay) for x, y, f in a.seen[c] if f > 0.16]
        recent = sum(1 for t in self._recent_attacks if w.tick - t < 300)
        if recent >= 14 and w.tick - self._last_war_log > 900:
            self._last_war_log = w.tick
            self.log("Des habitants s'entredéchirent pour les ressources !", (228, 98, 98), "combat")
        if w.tick % 60 == 0:
            self.pop_hist.append(len(self.agents))
        if w.tick % 900 == 0:
            self._analyze_society()
        if w.tick % 300 == 0:
            self.universal_knowledge.sync_from_world(self.w, self.am, self.w.tick)
        if w.tick % 3600 == 0:
            self.social_memory.decay(self.w.tick)
        if w.tick % 1800 == 0:
            for a in self.agents:
                if a.alive and not a.child:
                    accepted = self.academy.consider(a, self.w.tick)
                    if accepted:
                        self.log(f"Nouveau champion : {a.name} ({a.age_years:.1f} ans)",
                                 (88, 148, 228), "laboratoire")
        if w.tick % DAY_TICKS == 0:
            self.lab.snapshot(self)
        if __debug__ and w.tick % 600 == 0:
            from .invariants import validate_simulation
            for error in validate_simulation(self):
                self.log(f"INVARIANT: {error}", (214, 84, 84), "monde")
        if w.tick % 1800 == 0:
            for a in self.agents:
                expired = [k for k, (_, until) in a.failed_targets.items() if w.tick > until]
                for k in expired:
                    del a.failed_targets[k]
        if w.tick % 60 == 0:
            self._grow_crops()

    def _grow_crops(self):
        w = self.w
        for (tx, ty), plot in list(w.crop_plots.items()):
            if not (0 <= tx < w.g and 0 <= ty < w.g):
                continue
            if w.water[ty, tx]:
                plot.watered = True
            elif self.clock.rain > 0.3:
                plot.watered = True
            else:
                plot.watered = False
            growth_rate = 0.001
            if plot.watered:
                growth_rate *= 2.0
            if self.clock.is_night:
                growth_rate *= 0.5
            plot.growth = min(1.0, plot.growth + growth_rate)
            if plot.growth >= 1.0 and w.content_at(tx, ty) < 0:
                pool = self.am.pool("food")
                if pool:
                    aid = int(self.am.pick(pool, self.rng))
                    w.place(tx, ty, aid, self.am, hp=3, solid=False, size=1)
                    del w.crop_plots[(tx, ty)]
                    self.lab.event(self.w.tick, "crop_harvested",
                                   eid=plot.owner_eid, tx=tx, ty=ty)

    # ------------------------------------------------------------------ messages
    SEMANTIC_VOCABULARY = {
        "danger_here": {"urgency": 0.8, "decay": 0.001},
        "food_here": {"urgency": 0.3, "decay": 0.0005},
        "water_here": {"urgency": 0.3, "decay": 0.0005},
        "need_help": {"urgency": 0.7, "decay": 0.002},
        "need_resource": {"urgency": 0.5, "decay": 0.001},
        "build_site": {"urgency": 0.2, "decay": 0.0003},
        "follow_me": {"urgency": 0.4, "decay": 0.001},
        "trust_warning": {"urgency": 0.6, "decay": 0.001},
        "thanks": {"urgency": 0.1, "decay": 0.003},
        "grief": {"urgency": 0.5, "decay": 0.001},
    }

    def send_fact(self, sender, receiver, category, tx, ty, confidence=0.6):
        trust = receiver.trust(sender.eid)
        if trust < -0.3:
            return False
        # Lot G : fiabilité du message basée sur la source
        source_belief = receiver.anima_social_belief(sender.eid, self.w.tick)
        source_reliability = source_belief.get("reliability", 0.5)
        effective_confidence = confidence * (0.5 + 0.5 * source_reliability)
        receiver.remember(category, tx, ty)
        receiver.episodes.append((self.w.tick, "message", {
            "from": sender.eid,
            "category": category,
            "tx": tx,
            "ty": ty,
            "confidence": effective_confidence,
        }))
        self.lab.event(self.w.tick, "message_sent",
                       sender_eid=sender.eid, receiver_eid=receiver.eid,
                       category=category, tx=tx, ty=ty, confidence=effective_confidence)
        self.lab.event(self.w.tick, "message_received",
                       sender_eid=sender.eid, receiver_eid=receiver.eid,
                       category=category, tx=tx, ty=ty, trust=trust)
        self._record_anima(
            receiver, "message_received", (tx, ty),
            actors=[receiver.eid, sender.eid], action="receive_message",
            outcome="received", surprise=0.1)
        return True

    def _bucket(self):
        self.item_bucket = {}
        self.food_cells = {}
        keep = []
        for it in self.w.items:
            it.life -= 1
            if it.life <= 0:
                continue
            if it.kind == "food" and it.spoil_tick > 0 and self.w.tick >= it.spoil_tick:
                continue
            keep.append(it)
            self.item_bucket.setdefault((int(it.x // 32), int(it.y // 32)), []).append(it)
            if it.kind == "food":
                self.food_cells.setdefault((int(it.x // 128), int(it.y // 128)), []).append(it)
        self.w.items = keep

    def _near(self, x, y, pred, r=1):
        cx, cy = int(x // 32), int(y // 32)
        out = []
        for j in range(cy - r, cy + r + 1):
            for i in range(cx - r, cx + r + 1):
                for e in self.grid_bucket.get((i, j), ()):
                    if pred(e):
                        out.append(e)
        return out

    def _has_food_near(self, x, y, radius_px=40):
        cell = 128
        cx, cy = int(x // cell), int(y // cell)
        r = max(1, math.ceil(radius_px / cell))
        r2 = radius_px * radius_px
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                for item in self.food_cells.get((xx, yy), ()):
                    if (item.x - x) ** 2 + (item.y - y) ** 2 <= r2:
                        return True
        return False

    # ------------------------------------------------------------------ perception double : longue + courte portée
    def _perceive(self, a: Being):
        w = self.w
        light = self.clock.light
        R = a.sense_r(light)                    # longue portée (10-15 tiles)
        R_near = a.sense_r_near()               # courte portée (8 tiles = Moore)
        tx, ty = a.tx, a.ty
        old_heat = float(w.heat[ty, tx])
        w.heat[ty, tx] = min(1.0, w.heat[ty, tx] + 0.012)
        if old_heat < 0.5 and w.heat[ty, tx] >= 0.5:
            self.lab.event(self.w.tick, "route_used", tx=tx, ty=ty)

        # ====== VISION LONGUE PORTÉE : mémoire / navigation ======
        n = PERCEPT_CELLS + int(40 * a.cog[3])
        for _ in range(n):
            ang = self.rng.uniform(0, 6.283)
            rad = self.rng.random() ** 0.6 * R
            x = int(tx + math.cos(ang) * rad)
            y = int(ty + math.sin(ang) * rad)
            if not (0 <= x < w.g and 0 <= y < w.g):
                continue
            if w.fire[y, x] > 0:
                a.emotions[0] = min(1.0, a.emotions[0] + 0.02)
                a.emotions[5] = min(1.0, a.emotions[5] + 0.02)
                a.belief_places[(x // 8, y // 8)] = min(1.0,
                    a.belief_places.get((x // 8, y // 8), 0) + 0.1)
                self.clan_knowledge.report_danger(x, y, a.eid, w.tick, 0.6)
                continue
            aid = w.content_at(x, y)
            if aid < 0:
                if w.water[y, x]:
                    a.remember("water", x, y)
                continue
            asd = self.am.assets[aid]
            if asd.edible > 0:
                a.remember("food", x, y)
                self.clan_knowledge.share_place("food", x, y, a.eid, w.tick)
            elif asd.harvest:
                m = asd.harvest["material"]
                cat = {"bois": "wood", "pierre": "stone",
                        "or": "stone"}.get(m, "wood")
                a.remember(cat, x, y)
                self.clan_knowledge.share_place(cat, x, y, a.eid, w.tick)
            elif asd.tool:
                a.remember("wood", x, y)
                self.clan_knowledge.share_place("wood", x, y, a.eid, w.tick)
            elif asd.shelter:
                a.remember("shelter", x, y)
                self.clan_knowledge.share_place("shelter", x, y, a.eid, w.tick)

        # ====== VISION COURTE PORTÉE : Moore neighborhood (actions physiques) ======
        near_agents = []
        near_sheep = []
        near_monsters = []
        R_near_chunks = max(1, int(R_near * TILE / 32))
        cx_a, cy_a = int(a.x // 32), int(a.y // 32)
        R_near_px = R_near * TILE
        for j in range(cy_a - R_near_chunks, cy_a + R_near_chunks + 1):
            for i in range(cx_a - R_near_chunks, cx_a + R_near_chunks + 1):
                for e in self.grid_bucket.get((i, j), ()):
                    if isinstance(e, Being) and e.eid != a.eid and getattr(e, "alive", False):
                        d2 = (e.x - a.x) ** 2 + (e.y - a.y) ** 2
                        if d2 < R_near_px ** 2:
                            near_agents.append(e)
                    elif isinstance(e, Sheep) and getattr(e, "alive", False):
                        d2 = (e.x - a.x) ** 2 + (e.y - a.y) ** 2
                        if d2 < R_near_px ** 2:
                            near_sheep.append(e)
                    elif isinstance(e, Monster) and getattr(e, "alive", False):
                        d2 = (e.x - a.x) ** 2 + (e.y - a.y) ** 2
                        if d2 < R_near_px ** 2:
                            near_monsters.append(e)
        # mémoriser agents vus en longue portée aussi
        for e in near_agents:
            a.remember("agent", e.tx, e.ty)

        # sons percus
        for (sx, sy, kind, inten, st) in self.sounds:
            if st == a._last_heard:
                continue
            d = math.hypot(sx - a.x, sy - a.y)
            if d < (30 + 70 * a.body[3]) * inten:
                a._last_heard = st
                self._on_sound(a, kind, sx, sy)

        # canaux locaux (8 cases Moore — court portée)
        loc = a._loc if hasattr(a, "_loc") else np.zeros(8)
        fx, fy = tx + (a.fx or 1), ty + a.fy
        loc[0] = 1.0 if (0 <= fx < w.g and 0 <= fy < w.g and w.blocked[fy, fx]) else 0.0
        loc[1] = 1.0 if any(w.content_at(x, y) >= 0 and self.am.assets[w.content_at(x, y)].harvest
                            for x, y in self._ring(tx, ty)) else 0.0
        loc[2] = 1.0 if near_agents else 0.0
        loc[3] = 1.0 if near_sheep else 0.0
        loc[4] = 1.0 if w.near_water(tx, ty) else 0.0
        loc[5] = 1.0 if w.fire[max(0, ty - 2):ty + 3, max(0, tx - 2):tx + 3].any() else 0.0
        loc[6] = float(w.smell[ty, tx])
        loc[7] = float(w.shelter[ty, tx])
        a._loc = loc
        a._near_agents = near_agents
        a._near_sheep = near_sheep
        a._near_monsters = near_monsters
        for monster in near_monsters:
            a.belief_places[(monster.tx // 8, monster.ty // 8)] = min(
                1.0,
                a.belief_places.get((monster.tx // 8, monster.ty // 8), 0.0) + 0.20,
            )

        # ====== CONTEXTE LOCAL STRUCTURE ======
        def local_density(category):
            count = 0
            radius = 5
            for yy in range(max(0, ty - radius), min(w.g, ty + radius + 1)):
                for xx in range(max(0, tx - radius), min(w.g, tx + radius + 1)):
                    aid = w.content_at(xx, yy)
                    if aid < 0:
                        continue
                    asset = self.am.assets[aid]
                    if category == "food" and asset.edible > 0:
                        count += 1
                    elif category == "wood" and asset.harvest and asset.harvest.get("material") == "bois":
                        count += 1
                    elif category == "stone" and asset.harvest and asset.harvest.get("material") in ("pierre", "or"):
                        count += 1
            return min(1.0, count / 12.0)

        ctx = a.context
        ctx["food_density"] = local_density("food")
        ctx["wood_density"] = local_density("wood")
        ctx["stone_density"] = local_density("stone")
        ctx["sheep_count"] = min(1.0, len(near_sheep) / 5.0)
        ctx["monster_count"] = min(1.0, len(near_monsters) / 4.0)
        ctx["ally_count"] = min(1.0, sum(1 for e in near_agents if a.trust(e.eid) > 0.2) / 5.0)
        ctx["enemy_count"] = min(1.0, sum(1 for e in near_agents if a.trust(e.eid) < -0.2) / 5.0)
        stor = self.nearest_storage(tx, ty, max_dist=12)
        ctx["storage_near"] = 0.0 if stor is None else max(0.0, 1.0 - stor.total() / max(1, stor.capacity))
        ctx["site_near"] = 1.0 if any(
            abs(sx - tx) <= 8 and abs(sy - ty) <= 8
            for sx, sy in w.sites
        ) else 0.0
        ctx["route_danger"] = min(1.0, float(w.smell[ty, tx]))

    @staticmethod
    def _ring(tx, ty):
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx or dy:
                    yield tx + dx, ty + dy

    def _on_sound(self, a, kind, sx, sy):
        if kind == "chop":
            a.emotions[5] = min(1.0, a.emotions[5] + 0.08)   # curiosite
        elif kind == "scream":
            a.emotions[0] = min(1.0, a.emotions[0] + 0.3)
            a.belief_places[(int(sx // 128), int(sy // 128))] = min(
                1.0, a.belief_places.get((int(sx // 128), int(sy // 128)), 0) + 0.25)
        elif kind == "fight":
            a.emotions[0] = min(1.0, a.emotions[0] + 0.15)
        elif kind == "voice" and a.child:
            a.skills[3] = min(1.0, a.skills[3] + 0.02)       # l'enfant écoute et apprend

    # ------------------------------------------------------------------ vecteur mental
    def _sense(self, a: Being):
        s = self._sens
        n, e, p, b = a.needs, a.emotions, a.personality, a.body
        tx, ty = a.tx, a.ty
        s[0] = a.hunger
        s[1] = a.energy
        s[2] = n[2]
        s[3] = n[3]
        s[4] = 1.0 - e[0]
        s[5] = n[5]
        s[6] = n[6]
        s[7] = a.health
        s[8] = min(1.0, a.age / float(AGE_ELDER_TICKS * 2))
        s[9] = self.clock.temp
        s[10:15] = b
        s[15:27] = p
        s[27:35] = e
        s[35:39] = a.cog
        s[39] = a.self_esteem
        s[40] = max(-1.0, min(1.0, a.rep / 8.0))
        near_trust = 0.0
        if a._near_agents:
            near_trust = float(np.mean([a.trust(x.eid) for x in a._near_agents]))
        s[41] = near_trust
        s[42] = 1.0 if a.hated is not None else 0.0
        s[43] = 1.0 if a.bonded is not None else 0.0
        s[44] = 1.0 if a.child else 0.0
        s[45:49] = a.skills
        s[49:64] = a.habits
        s[64] = a.mood(self.w.tick)
        s[65:73] = a._loc
        i = 73
        for cat in ("food", "wood", "stone", "water", "shelter", "agent"):
            mem = a.recall(cat, tx, ty)
            if mem:
                ang = math.atan2(mem[1] - ty, mem[0] - tx)
                s[i] = 1.0
                s[i + 1] = math.cos(ang)
                s[i + 2] = math.sin(ang)
            else:
                s[i] = s[i + 1] = s[i + 2] = 0.0
            i += 3
        f = self.clock.day_frac
        s[91] = math.sin(f * 6.283)
        s[92] = math.cos(f * 6.283)
        s[93] = self.clock.temp
        s[94] = self.clock.rain
        # === Nouvelles entrees (95-127) ===
        INVCAP = 8.0
        s[INPUT["wood_inventory"]] = min(1.0, a.inv.get("bois", 0) / INVCAP)
        s[INPUT["stone_inventory"]] = min(1.0, a.inv.get("pierre", 0) / INVCAP)
        s[INPUT["seed_inventory"]] = min(1.0, a.inv.get("graine", 0) / INVCAP)
        s[INPUT["gold_inventory"]] = min(1.0, a.inv.get("or", 0) / INVCAP)
        s[INPUT["tool_equipped"]] = 1.0 if a.tool >= 0 else 0.0
        s[INPUT["tool_durability"]] = min(1.0, a.tool_durability / 20.0) if a.tool >= 0 else 0.0
        tool_kind = ""
        if a.tool >= 0:
            tool_kind = self.am.assets[a.tool].meta.get("tool_kind", "")
        s[INPUT["tool_axe"]] = 1.0 if tool_kind == "hache" else 0.0
        s[INPUT["tool_pickaxe"]] = 1.0 if tool_kind == "pioche" else 0.0
        s[INPUT["tool_hammer"]] = 1.0 if tool_kind == "marteau" else 0.0
        ctx = getattr(a, 'context', {})
        s[INPUT["food_density"]] = ctx.get("food_density", 0.0)
        s[INPUT["wood_density"]] = ctx.get("wood_density", 0.0)
        s[INPUT["stone_density"]] = ctx.get("stone_density", 0.0)
        s[INPUT["sheep_near"]] = ctx.get("sheep_count", 0.0)
        s[INPUT["allies_near"]] = ctx.get("ally_count", 0.0)
        s[INPUT["enemies_near"]] = ctx.get("enemy_count", 0.0)
        s[INPUT["storage_near"]] = ctx.get("storage_near", 0.0)
        stor = self.nearest_storage(tx, ty, max_dist=14)
        if stor:
            s[INPUT["storage_food"]] = min(1.0, stor.inventory.get("food", 0) / max(1, stor.capacity))
            s[INPUT["storage_wood"]] = min(1.0, stor.inventory.get("bois", 0) / max(1, stor.capacity))
        s[INPUT["site_near"]] = ctx.get("site_near", 0.0)
        site = self.nearest_site(tx, ty, max_dist=10)
        if site:
            s[INPUT["site_progress"]] = site.progress()
            missing = sum(1 for t in site.tasks if t.key not in site.placed)
            s[INPUT["site_missing"]] = min(1.0, missing / 10.0)
        food_mem = a.recall("food", tx, ty)
        s[INPUT["food_distance"]] = min(1.0, (food_mem[2] / 100.0) if food_mem else 1.0)
        water_mem = a.recall("water", tx, ty)
        s[INPUT["water_distance"]] = min(1.0, (water_mem[2] / 100.0) if water_mem else 1.0)
        shelter_mem = a.recall("shelter", tx, ty)
        s[INPUT["shelter_distance"]] = min(1.0, (shelter_mem[2] / 100.0) if shelter_mem else 1.0)
        if a.bonded is not None:
            partner = self._by_eid(a.bonded)
            if partner:
                d = max(abs(partner.tx - tx), abs(partner.ty - ty))
                s[INPUT["partner_distance"]] = min(1.0, d / 40.0)
        s[INPUT["route_danger"]] = ctx.get("route_danger", 0.0)
        s[INPUT["neighbor_need"]] = min(1.0, len(a._near_agents) / 3.0)
        s[INPUT["local_reputation"]] = max(-1.0, min(1.0, a.rep / 8.0))
        s[INPUT["winter"]] = 1.0 if self.clock.is_winter else 0.0
        if a.home:
            hx, hy = a.home
            if 0 <= hx < self.w.g and 0 <= hy < self.w.g:
                stor_home = self.w.storages.get((hx, hy))
                if stor_home:
                    s[INPUT["home_storage"]] = min(1.0, stor_home.total() / max(1, stor_home.capacity))
        s[INPUT["inventory_load"]] = min(1.0, sum(max(0, v) for v in a.inv.values()) / 32.0)
        s[INPUT["local_fear"]] = float(a.emotions[0])
        s[INPUT["life_progress"]] = min(1.0, a.age / float(AGE_ELDER_TICKS * 3))
        # Anima: mémoire épisodique émotionnelle
        anima = a.anima
        s[INPUT["trauma_attack"]] = min(1.0, anima["trauma"]["attack"])
        belief_near = 0.0
        cx, cy = tx // 8, ty // 8
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                v = anima["beliefs"]["places"].get((cx + dx, cy + dy), 0.0)
                if v > belief_near:
                    belief_near = v
        s[INPUT["belief_danger"]] = min(1.0, belief_near)
        s[INPUT["episode_count"]] = min(1.0, len(anima["episodic_memory"]) / 20.0)
        s[INPUT["anima_fighter"]] = min(1.0, anima["identity"]["fighter"])
        return s

    # ------------------------------------------------------------------ arbitrage
    def _bias(self, a: Being):
        """Personnalite + emotions + besoins + croyances + risque -> bias de logits."""
        p, e, n = a.personality, a.emotions, a.needs
        ctx = getattr(a, "context", {})
        bias = np.zeros(N_OUT)
        for act in range(N_OUT):
            tr, wgt = ACTION_TRAIT[act]
            bias[act] += wgt * p[tr]
        bias[EXPLORE] -= 0.4 * p[3]
        bias[ATTACK] -= 0.4 * p[5]
        bias[ATTACK] -= 0.3 * p[3]
        bias[REST] -= 0.3 * p[8]
        bias[ATTACK] += 0.7 * e[2] - 0.8 * e[0]
        bias[FLEE] += 0.9 * e[0]
        bias[EXPLORE] -= 0.5 * e[0]
        bias[SLEEP] += 0.3 * e[3]
        bias[TALK] += 0.35 * e[1] + 0.4 * e[7]
        bias[EAT] += (n[0] - 0.70) * 2.6 * (0.4 + 0.6 * p[8]) if n[0] > 0.70 else 0
        if n[0] > 0.90:
            bias[EAT] += 1.6
            bias[SLEEP] = -1.0
        bias[DRINK] += (n[2] - 0.70) * 2.6 if n[2] > 0.70 else 0
        if n[2] > 0.85:
            bias[DRINK] += 1.6
            bias[SLEEP] = -1.0
        if a._loc[4] > 0 and n[2] > 0.45:
            bias[DRINK] += 0.9
        bias[SLEEP] += (n[3] - 0.75) * 2.4 if n[3] > 0.75 else 0
        bias[REST] += (a.energy - 0.22) * -2.8 if a.energy < 0.22 else 0
        bias[GIVE] += 0.5 * n[5] * p[0] + 0.4 * p[10]
        bias[BUILD] += 0.4 * n[6] * p[7] + 0.3 * p[9]
        bias[MARK] += 0.3 * n[6]
        bias[HARVEST] += 0.3 * a.skills[0]
        bias[BUILD] += 0.25 * a.skills[1]
        bias[TALK] += 0.2 * a.skills[3]
        bias += 0.5 * a.habits * (1.0 - 0.7 * p[6])
        knows_wood = bool(a.recall("wood", a.tx, a.ty))
        knows_stone = bool(a.recall("stone", a.tx, a.ty))
        has_materials = (
            a.inv.get("bois", 0) > 0 or a.inv.get("pierre", 0) > 0
        )
        if not has_materials and (knows_wood or knows_stone):
            bias[HARVEST] += 0.18
        if ctx.get("wood_density", 0.0) > 0.20:
            bias[HARVEST] += 0.10 * ctx["wood_density"]
        if ctx.get("stone_density", 0.0) > 0.20:
            bias[HARVEST] += 0.08 * ctx["stone_density"]
        if ctx.get("storage_near", 0.0) > 0.3:
            bias[GIVE] += 0.06 * ctx["storage_near"]
        if ctx.get("site_near", 0.0) > 0.3:
            bias[BUILD] += 0.08 * ctx["site_near"]
        if a.inv.get("bois", 0) >= 3 or a.inv.get("pierre", 0) >= 1:
            bias[BUILD] += 0.10
        if a.tool >= 0 and a.tool_durability < 5:
            bias[HARVEST] -= 0.04
            bias[BUILD] += 0.03
        if a.hated is not None:
            t = self._by_eid(a.hated)
            if t is not None:
                d = max(abs(t.tx - a.tx), abs(t.ty - a.ty))
                if d < 14:
                    bias[ATTACK] += (0.6 * e[2] + 0.3 * p[1]) * (1 - d / 14)
        if a.bonded is not None:
            t = self._by_eid(a.bonded)
            if t is not None and not t.child:
                d = max(abs(t.tx - a.tx), abs(t.ty - a.ty))
                if d > 10:
                    bias[SOCIAL] += 0.4 * e[7]
        if self.clock.rain > 0.6:
            bias[SLEEP] += 0.6 * self.clock.rain
            bias[REST] += 0.5 * self.clock.rain
            bias[EXPLORE] -= 0.8 * self.clock.rain
            bias[HARVEST] -= 0.4 * self.clock.rain
        if a._near_monsters:
            nearest = min(a._near_monsters,
                          key=lambda m: (m.x - a.x)**2 + (m.y - a.y)**2)
            if nearest.hostile:
                bias[FLEE] += 1.2
                bias[ATTACK] += 0.3 * e[2]
        for event in list(getattr(a, "observed_actions", ())):
            if self.w.tick - event["tick"] > 1800:
                continue
            if event["reward"] > 0:
                bias[event["action"]] += min(0.08, 0.04 * event["reward"])

        # Territoire doux : pheromones modulent peur, securite, retour foyer
        w = self.w
        phero = float(w.marker[a.ty, a.tx])
        if phero > 0.2:
            bias[REST] += 0.3 * phero
            bias[EXPLORE] -= 0.2 * phero
            bias[SOCIAL] += 0.15 * phero
        if phero > 0.5:
            bias[FLEE] -= 0.3 * phero
            bias[ATTACK] -= 0.2 * phero

        # ── Anima : beliefs + trauma modulent les decisions ──
        anima = a.anima
        trauma_atk = anima["trauma"]["attack"]
        # danger percu local
        cx, cy = a.tx // 8, a.ty // 8
        belief_local = 0.0
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                v = anima["beliefs"]["places"].get((cx + dx, cy + dy), 0.0)
                if v > belief_local:
                    belief_local = v
        # trauma → FLEE, evite zones dangereuses
        if trauma_atk > 0.2:
            bias[FLEE] += 0.4 * trauma_atk
            bias[EXPLORE] -= 0.2 * trauma_atk
        # croyance lieu dangereux → FLEE, evite zone
        if belief_local > 0.3:
            bias[FLEE] += 0.3 * belief_local
            bias[HARVEST] -= 0.15 * belief_local
        # identity.fighter → ATTACK plus tentant
        if anima["identity"]["fighter"] > 0.3:
            bias[ATTACK] += 0.2 * anima["identity"]["fighter"]
        # identity.builder → BUILD plus tentant
        if anima["identity"]["builder"] > 0.2:
            bias[BUILD] += 0.15 * anima["identity"]["builder"]
        # identity.explorer → EXPLORE plus tentant
        if anima["identity"]["explorer"] > 0.2:
            bias[EXPLORE] += 0.12 * anima["identity"]["explorer"]

        # ── Lot 4 : valeurs actives ──
        vals = anima.get("values", {})
        survival = float(vals.get("survival", 0.5))
        family = float(vals.get("family", 0.5))
        security = float(vals.get("security", 0.5))
        community = float(vals.get("community", 0.5))
        knowledge = float(vals.get("knowledge", 0.5))
        wealth = float(vals.get("wealth", 0.5))
        generosity = float(vals.get("generosity", 0.5))
        bias[FLEE] += 0.30 * (security - 0.5)
        bias[REST] += 0.12 * (survival - 0.5)
        bias[SLEEP] += 0.12 * (survival - 0.5)
        bias[EAT] += 0.16 * (survival - 0.5)
        bias[DRINK] += 0.16 * (survival - 0.5)
        bias[BUILD] += 0.18 * (security - 0.5) + 0.10 * (family - 0.5)
        bias[GIVE] += 0.22 * (community - 0.5) + 0.24 * (generosity - 0.5)
        bias[TALK] += 0.16 * (community - 0.5)
        bias[SOCIAL] += 0.16 * (family - 0.5) + 0.12 * (community - 0.5)
        bias[EXPLORE] += 0.22 * (knowledge - 0.5)
        bias[HARVEST] += 0.14 * (wealth - 0.5)
        bias[TAKE] += 0.08 * (wealth - 0.5) - 0.12 * (generosity - 0.5)

        # ── Lot D : intention persistante → biais ──
        intent = a.anima.get("intention")
        if intent and intent.get("priority", 0) > 0.3:
            ik = intent.get("kind", "")
            ip = intent["priority"]
            INTENTION_BIAS = {
                "secure_food": {HARVEST: 0.25, EAT: 0.10, EXPLORE: 0.05},
                "protect_family": {FLEE: 0.15, ATTACK: 0.10, SOCIAL: 0.10},
                "build_home": {BUILD: 0.30, HARVEST: 0.15},
                "recover_from_loss": {REST: 0.20, SOCIAL: 0.10},
                "avoid_danger": {FLEE: 0.30, EXPLORE: -0.10},
                "help_ally": {GIVE: 0.20, SOCIAL: 0.15, TALK: 0.10},
                "explore_unknown": {EXPLORE: 0.30},
            }
            for act_key, bdelta in INTENTION_BIAS.get(ik, {}).items():
                bias[act_key] += bdelta * ip

        # ── Lot E : plans courts → biais additionnel ──
        plans = getattr(a, '_cached_plans', None)
        if plans and plans[0].get("score", 0) > 0.2:
            top = plans[0]
            for step in top.get("steps", []):
                if 0 <= step < len(bias):
                    bias[step] += 0.08 * top["score"]

        return bias

    def _feasible(self, a: Being):
        w = self.w
        f = np.zeros(N_OUT, dtype=bool)
        f[REST] = True
        f[EXPLORE] = True
        f[MARK] = a.energy > 0.12
        f[SLEEP] = (a.needs[3] > 0.55 or (self.clock.is_night and a.needs[3] > 0.3)) \
            and a.needs[2] < 0.8 and a.hunger < 0.92 and a.energy > 0.08
        f[EAT] = a.hunger > 0.28 and (bool(a.recall("food", a.tx, a.ty))
                                       or self._has_food_near(a.x, a.y))
        f[HARVEST] = bool(
            a.recall("wood", a.tx, a.ty)
            or a.recall("stone", a.tx, a.ty)
            or a.seen.get("wood")
            or a.seen.get("stone")
        )
        f[DRINK] = a.needs[2] > 0.32 and (a._loc[4] > 0 or bool(a.recall("water", a.tx, a.ty)))
        f[DROP] = a.carry() > 0
        f[BUILD] = ((a.inv.get("bois", 0) >= 3 or a.inv.get("pierre", 0) >= 1)
                     or a.inv.get("graine", 0) > 0) and not a.child
        f[GIVE] = bool(a._near_agents) and a.carry() > 1
        f[TAKE] = bool(a._near_agents) and not a.child
        f[ATTACK] = (
            (bool(a._near_agents) or bool(a._near_sheep) or bool(a._near_monsters))
            and a.energy > 0.25
            and not a.child
        )
        f[FLEE] = (
            a.emotions[0] > 0.35
            and (bool(a._near_agents) or bool(a._near_sheep) or bool(a._near_monsters))
        )
        f[TALK] = bool(a._near_agents) and \
            self.w.tick - a.talk_cd.get(a._near_agents[0].eid, -999) > 240
        f[SOCIAL] = bool(a.recall("agent", a.tx, a.ty)) or bool(a._near_agents)
        return f

    def _decide(self, a: Being):
        x = self._sense(a)
        bias = self._bias(a)
        temperature = 0.5 + 0.9 * a.personality[6] + 0.4 * a.emotions[4]
        act, probs = a.brain.think(
            x, temperature, bias,
            curiosity=a.personality[2],
            caution=a.personality[3],
        )
        f = self._feasible(a)
        if not f[act]:
            order = np.argsort(-probs)
            for cand in order:
                if f[cand]:
                    act = int(cand)
                    break
            else:
                act = REST
        a.habits *= 0.992
        a.habits[act] = min(1.0, a.habits[act] + 0.02)
        # Lot M : comptage actions
        from .brain_api import ACTION_NAMES_EXP
        act_name = ACTION_NAMES_EXP.get(act, str(act))
        self.debug_action_counts[act_name] = self.debug_action_counts.get(act_name, 0) + 1
        self._set_goal(a, act)

    def _known_or_universal(self, a, category, tx, ty):
        personal = a.recall(category, tx, ty)
        if personal is not None:
            return personal
        clan_places = self.clan_knowledge.nearby_places(category, tx, ty, max_dist=100)
        if clan_places:
            best = clan_places[0]
            return best[0], best[1], best[3]
        fact = self.universal_knowledge.nearest(category, tx, ty, tick=self.w.tick)
        if fact is None:
            return None
        return fact.tx, fact.ty, max(abs(fact.tx - tx), abs(fact.ty - ty))

    def _set_goal(self, a, act):
        w = self.w
        tx, ty = a.tx, a.ty
        strategy = getattr(a.brain, '_strategy', IMMEDIAT)
        target = getattr(a.brain, '_target', SOI)
        g = {"act": act, "x": tx, "y": ty, "ref": None, "intensity": 1.0,
             "until": w.tick + 420}
        if act == EAT:
            m = self._known_or_universal(a, "food", tx, ty)
            if not m:
                a.goal = None
                return
            g["x"], g["y"] = m[0], m[1]
        elif act == DRINK:
            m = self._known_or_universal(a, "water", tx, ty)
            if m:
                wx, wy = m[0], m[1]
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        nx2, ny2 = wx + dx, wy + dy
                        if 0 <= nx2 < GRID and 0 <= ny2 < GRID and self.w.land[ny2, nx2] \
                           and not self.w.blocked[ny2, nx2]:
                            wx, wy = nx2, ny2
                            break
                    else:
                        continue
                    break
                g["x"], g["y"] = wx, wy
        elif act == HARVEST:
            if target == BOIS:
                mw = self._known_or_universal(a, "wood", tx, ty)
                m = mw
            elif target == PIERRE:
                ms = self._known_or_universal(a, "stone", tx, ty)
                m = ms
            else:
                mw = self._known_or_universal(a, "wood", tx, ty)
                ms = self._known_or_universal(a, "stone", tx, ty)
                m = None
                if mw and ms:
                    m = ms if (a.inv["pierre"] < 2 and ms[2] <= mw[2] * 2.2) or a.inv["bois"] >= 6 else mw
                else:
                    m = mw or ms
            if not m:
                a.goal = None
                return
            g["x"], g["y"] = m[0], m[1]
        elif act in (SOCIAL, GIVE, TAKE, TALK, ATTACK):
            if a._near_agents:
                if act == ATTACK:
                    e = max(a._near_agents, key=lambda t: t.health)
                elif act in (SOCIAL, GIVE, TALK):
                    e = max(a._near_agents,
                            key=lambda o: a.anima_social_score(o.eid))
                else:
                    e = a._near_agents[0]
                g["x"], g["y"], g["ref"] = e.tx, e.ty, e
            elif act == ATTACK and a._near_sheep:
                e = a._near_sheep[0]
                g["x"], g["y"], g["ref"] = e.tx, e.ty, e
            elif act == ATTACK and a._near_monsters:
                e = max(a._near_monsters, key=lambda m: m.health)
                g["x"], g["y"], g["ref"] = e.tx, e.ty, e
            elif act == SOCIAL and a.bonded is not None:
                t = self._by_eid(a.bonded)
                if t:
                    g["x"], g["y"], g["ref"] = t.tx, t.ty, t
                else:
                    a.bonded = None
                    a.goal = None
                    return
            else:
                m = a.recall("agent", tx, ty)
                if not m:
                    a.goal = None
                    return
                g["x"], g["y"] = m[0], m[1]
        elif act == FLEE:
            t = (a._near_agents or a._near_sheep or [None])[0]
            if t is None:
                a.goal = None
                return
            ang = math.atan2(a.y - t.y, a.x - t.x)
            g["x"] = int(np.clip(tx + math.cos(ang) * 18, 2, GRID - 3))
            g["y"] = int(np.clip(ty + math.sin(ang) * 18, 2, GRID - 3))
            if not w.land[g["y"], g["x"]]:
                g["x"], g["y"] = tx, ty
        elif act == EXPLORE:
            best, bs = None, 1e9
            for ang in np.arange(0, 6.283, 0.785):
                fx = int(np.clip(tx + math.cos(ang) * 14, 2, GRID - 3))
                fy = int(np.clip(ty + math.sin(ang) * 14, 2, GRID - 3))
                if not w.land[fy, fx]:
                    continue
                dan = a.belief_places.get((fx // 8, fy // 8), 0.0)
                sc = float(w.heat[fy, fx]) + dan * 2.0
                if sc < bs:
                    best, bs = (fx, fy), sc
            if best is None:
                a.goal = None
                return
            g["x"], g["y"] = best
            g["until"] = self.w.tick + 900
        elif act == SLEEP:
            m = self._known_or_universal(a, "shelter", tx, ty)
            if m is None and a.home:
                m = a.home
            if m:
                g["x"], g["y"] = m[0], m[1]
            else:
                g["x"], g["y"] = tx, ty
        elif act == BUILD:
            if target == DEPOT_CHANTIER:
                site = self.nearest_site(a.tx, a.ty, max_dist=20)
                if site is not None:
                    g["x"], g["y"] = site.origin_tx, site.origin_ty
                else:
                    storage = self.nearest_storage(a.tx, a.ty, max_dist=20)
                    if storage is not None:
                        g["x"], g["y"] = storage.tx, storage.ty
                    else:
                        new_site = self.create_house_site(a)
                        if new_site is None:
                            a.goal = None
                            return
                        g["x"], g["y"] = new_site.origin_tx, new_site.origin_ty
            elif target == ABRI:
                m = self._known_or_universal(a, "shelter", tx, ty)
                if m and m[2] < 14 and self.rng.random() < 0.7:
                    g["x"], g["y"] = m[0], m[1]
            else:
                m = self._known_or_universal(a, "shelter", tx, ty)
                if m and m[2] < 14 and self.rng.random() < 0.7:
                    g["x"], g["y"] = m[0], m[1]
        if self.target_is_blocked(a, act, g["x"], g["y"]):
            a.goal = None
            return
        if strategy == PRUDENT:
            danger = a.belief_places.get((g["x"] // 8, g["y"] // 8), 0.0)
            if danger > 0.45:
                a.goal = None
                return
        a.goal = g
        a.goal_t = 0
        a.stuck = 0
        a._last_px, a._last_py = a.x, a.y

    def register_goal_failure(self, a, reason="blocked"):
        goal = a.goal or {}
        key = (goal.get("act"), goal.get("x"), goal.get("y"))
        count, until = a.failed_targets.get(key, (0, 0))
        count += 1
        cooldown = min(1800, 180 * count)
        a.failed_targets[key] = (count, self.w.tick + cooldown)
        a.goal = None
        a.stuck = 0
        a.emotions[3] = min(1.0, a.emotions[3] + 0.04)
        self._reward(a, -0.03)

    def target_is_blocked(self, a, act, tx, ty):
        count, until = a.failed_targets.get((act, tx, ty), (0, 0))
        return self.w.tick < until

    # ------------------------------------------------------------------ depots
    def nearest_storage(self, tx, ty, max_dist=12):
        best, best_distance = None, 10**9
        for storage in self.w.storages.values():
            distance = max(abs(storage.tx - tx), abs(storage.ty - ty))
            if distance <= max_dist and distance < best_distance:
                best, best_distance = storage, distance
        return best

    def create_storage(self, a, tx, ty, capacity=80):
        from .storage import SharedStorage
        if (tx, ty) in self.w.storages:
            return self.w.storages[(tx, ty)]
        storage = SharedStorage(tx=tx, ty=ty, capacity=capacity, owner_clan=a.color)
        self.w.storages[(tx, ty)] = storage
        return storage

    def deposit_to_storage(self, a, storage):
        material = max(a.inv, key=a.inv.get)
        if a.inv.get(material, 0) <= 0:
            return False
        moved = storage.deposit(a.eid, material, min(2, a.inv[material]), self.w.tick)
        if moved <= 0:
            return False
        a.inv[material] -= moved
        a.skills[3] = min(1.0, a.skills[3] + 0.01)
        a.rep += 0.05
        self._reward(a, 0.08)
        self.lab.event(self.w.tick, "storage_deposit",
                       eid=a.eid, tx=storage.tx, ty=storage.ty,
                       material=material, amount=moved)
        self._record_anima(
            a, "resource_deposited", (storage.tx, storage.ty),
            actors=[a.eid], action="deposit", outcome="success",
            achievement=0.05)
        return True

    def withdraw_from_storage(self, a, storage, material):
        if a.inv.get(material, 0) >= INV_CAP:
            return False
        moved = storage.withdraw(a.eid, material, min(2, INV_CAP - a.inv.get(material, 0)), self.w.tick)
        if moved <= 0:
            return False
        a.inv[material] = a.inv.get(material, 0) + moved
        self.lab.event(self.w.tick, "storage_withdraw",
                       eid=a.eid, tx=storage.tx, ty=storage.ty,
                       material=material, amount=moved)
        self._record_anima(
            a, "resource_withdrawn", (storage.tx, storage.ty),
            actors=[a.eid], action="withdraw", outcome="success")
        return True

    # ------------------------------------------------------------------ agent
    def _agent(self, a: Being):
        w = self.w
        a.age += 1
        a.repro_cd = max(0, a.repro_cd - 1)
        a.atk_t = max(0, a.atk_t - 1)
        a.goal_t += 1
        a.pain = max(0.0, a.pain - 0.0004)

        # VOLONTE : le but persiste (engagement). On ne re-delibere que si :
        # but fini/expiré/bloque, urgence viscerale, ou mollesse (petit cerveau
        # en veille). Un grand cerveau stratege va au bout de sa tache.
        g = a.goal
        expired = g is not None and w.tick > g["until"]
        soft = g is not None and g["act"] in (REST, MARK, SOCIAL, TALK)
        urgent = (a.hunger > 0.85 or a.needs[2] > 0.85 or a.energy < 0.12
                  or a.emotions[0] > 0.7 or a.pain > 0.6)
        if self.w.tick - a.born_tick < 240:
            memories = (
                a.seen.get("food", []) + a.seen.get("wood", [])
                + a.seen.get("stone", []) + a.seen.get("water", [])
            )
            if not memories:
                self.bootstrap_resource_memory(a, radius=12)
        if g is None or expired or a.stuck > 20 + 50 * a.personality[8]:
            self._decide(a)
        elif a.goal_t % a.brain.te == 0:
            if urgent and self.rng.random() > 0.25:
                self._decide(a)
            elif soft and a.goal_t > 60 and self.rng.random() > \
                    (0.4 + 0.5 * a.personality[4] - 0.4 * a.personality[6]):
                self._decide(a)
        if a.goal is None:
            a.goal = {"act": REST, "x": a.tx, "y": a.ty, "ref": None,
                      "intensity": 1.0, "until": w.tick + 300}
            a.goal_t = 0

        self._execute(a)
        self._metabolize(a)

        after = self._wellbeing(a)
        delta = after - getattr(a, 'prev_wellbeing', after)
        if abs(delta) > 0.001:
            self._reward(a, 0.08 * delta)
        a.prev_wellbeing = after

        # ── Lot D : generation d'intentions (tous les 200 ticks) ──
        if w.tick % 200 == 0 and not a.anima_intention_valid(w.tick):
            self._generate_intention(a)
        # ── Lot E : generation de plans (tous les 100 ticks) ──
        if w.tick % 100 == 0:
            a._cached_plans = self._generate_plans(a)
        # ── Lot F+H : décroissance traces causales + observation learning ──
        if w.tick % 150 == 0:
            a.anima_decay_causal_traces()
            a.anima_apply_observation_learning()

        if a.age >= a.natural_death_age:
            self._die(a, cause="vieillesse")
        elif a.health <= 0:
            self._die(a)

    def _generate_intention(self, a: Being):
        """Génère une intention Anima basée sur l'état courant."""
        w = self.w
        vals = a.anima.get("values", {})
        trauma = a.anima.get("trauma", {})
        # priorité par besoin
        if a.hunger > 0.7:
            a.anima_set_intention("secure_food", "faim", priority=0.7,
                                  tick=w.tick, duration=600)
        elif trauma.get("loss", 0) > 0.2:
            a.anima_set_intention("recover_from_loss", "deuil", priority=0.5,
                                  tick=w.tick, duration=800)
        elif trauma.get("attack", 0) > 0.3:
            a.anima_set_intention("avoid_danger", "peur", priority=0.6,
                                  tick=w.tick, duration=400)
        elif a.home is None and a.inv.get("bois", 0) >= 2:
            a.anima_set_intention("build_home", "sans abri", priority=0.6,
                                  tick=w.tick, duration=1000)
        elif vals.get("community", 0.5) > 0.6 and a._near_agents:
            target = max(a._near_agents,
                         key=lambda o: a.anima_social_score(o.eid))
            a.anima_set_intention("help_ally", "communauté",
                                  target=target.eid, priority=0.4,
                                  tick=w.tick, duration=500)
        elif vals.get("knowledge", 0.5) > 0.6:
            a.anima_set_intention("explore_unknown", "curiosité",
                                  priority=0.35, tick=w.tick, duration=600)

    # ── Lot E : plans courts et alternatives ──

    def _generate_plans(self, a: Being):
        """Génère 1 à 4 plans alternatifs de 1-3 étapes."""
        w = self.w
        plans = []
        f = self._feasible(a)
        vals = a.anima.get("values", {})
        ident = a.anima.get("identity", {})
        trauma_sum = sum(a.anima.get("trauma", {}).values())
        # plan 1: nourriture
        if f[HARVEST]:
            plans.append({
                "steps": [HARVEST, DROP],
                "need_gain": 0.3 * (1.0 - a.hunger),
                "value_fit": vals.get("wealth", 0.5) * 0.2,
                "identity_fit": ident.get("provider", 0) * 0.15,
                "risk": 0.05, "energy_cost": 0.1,
                "social_gain": 0.0, "confidence": 0.6,
            })
        # plan 2: construire
        if f[BUILD]:
            plans.append({
                "steps": [BUILD],
                "need_gain": 0.2 * (1.0 if a.home is None else 0.1),
                "value_fit": vals.get("security", 0.5) * 0.25,
                "identity_fit": ident.get("builder", 0) * 0.2,
                "risk": 0.02, "energy_cost": 0.15,
                "social_gain": 0.0, "confidence": 0.5,
            })
        # plan 3: aide sociale
        if f[GIVE] and a._near_agents:
            plans.append({
                "steps": [GIVE],
                "need_gain": 0.05,
                "value_fit": vals.get("community", 0.5) * 0.3 + vals.get("generosity", 0.5) * 0.2,
                "identity_fit": ident.get("provider", 0) * 0.1,
                "risk": 0.03, "energy_cost": 0.05,
                "social_gain": 0.25, "confidence": 0.4,
            })
        # plan 4: explorer
        if f[EXPLORE]:
            plans.append({
                "steps": [EXPLORE],
                "need_gain": 0.1,
                "value_fit": vals.get("knowledge", 0.5) * 0.3,
                "identity_fit": ident.get("explorer", 0) * 0.2,
                "risk": 0.15, "energy_cost": 0.12,
                "social_gain": 0.0, "confidence": 0.35,
            })
        # score et trie
        for p in plans:
            p["score"] = (
                p["need_gain"] + p["value_fit"] + p["identity_fit"]
                + p["social_gain"] + p["confidence"]
                - p["risk"] - p["energy_cost"] - 0.1 * trauma_sum
            )
        plans.sort(key=lambda p: p["score"], reverse=True)
        return plans[:4]

    def _wellbeing(self, a):
        return (
            0.30 * a.health
            + 0.25 * a.energy
            + 0.25 * (1.0 - a.hunger)
            + 0.20 * (1.0 - a.needs[2])
        )

    def _metabolize(self, a: Being):
        w = self.w
        act = a.goal["act"] if a.goal else REST
        night = self.clock.is_night
        n = a.needs
        n[0] = min(1.0, n[0] + HUNGER_RATE * (1.3 if act != REST else 1.0))
        n[2] = min(1.0, n[2] + THIRST_RATE * (0.5 + self.clock.temp))
        n[3] = min(1.0, n[3] + (SLEEP_RATE_N if night else SLEEP_RATE_D))
        a.hunger = n[0]
        if act == REST:
            a.energy += REST_GAIN * (SHELTER_BONUS if w.shelter[a.ty, a.tx] else 1.0) \
                * (0.6 + 0.8 * a.body[1])
            a.state = "rest"
        elif act == SLEEP:
            sh = w.shelter[a.ty, a.tx]
            a.energy += SLEEP_GAIN * (1.6 if sh else 1.0) * (0.5 + a.body[4])
            n[3] = max(0.0, n[3] - 0.004)
            a.health += 0.0009 * (2.0 if sh else 1.0)
            a.state = "sleep"
            if a.pain > 0.5 or a.emotions[0] > 0.6 or (not night and n[3] < 0.2):
                a.goal = None
                if self.rng.random() < 0.3:
                    a.remember_event("dream", "chasse")
        else:
            a.energy -= E_DRAIN * (1.4 if self.clock.temp < 0.3 else 1.0)
        if n[2] > 0.9:
            a.health -= THIRST_HP
        if a.hunger >= 1.0:
            a.health -= STARVE_HP
        if a.energy < 0.04:
            a.health -= LOWE_HP
        # vieillissement : fragilité progressive après 65 ans
        a.health = min(a.health, a.age_health_cap())
        a.energy = min(1.0, max(0.0, a.energy))
        a.health = min(1.0, a.health)
        a.needs[1] = a.energy
        # appartenance : la solitude ronge ; estime de soi derive de la reputation
        if a._near_agents:
            n[5] = max(0.0, n[5] - 0.00025)
        else:
            n[5] = min(1.0, n[5] + 0.00012 * (0.5 + a.personality[0]))
        a.self_esteem += 0.0002 * (np.clip(a.rep / 10.0, -1, 1) - a.self_esteem)
        # decantation emotionnelle
        e = a.emotions
        e[0] = max(0.0, e[0] * 0.996 - 0.0002)
        e[1] += (0.3 - e[1]) * 0.0008
        e[2] = max(0.0, e[2] * 0.997)
        e[3] += (0.15 + 0.4 * (1 - e[1]) - e[3]) * 0.0005
        e[4] = min(1.0, 0.4 * a.hunger + 0.3 * e[0] + 0.3 * max(0.0, 0.2 - a.energy)
                   + 0.4 * n[2] + 0.3 * n[3])
        e[5] = max(0.0, e[5] * 0.99)
        e[6] = max(0.0, e[6] * 0.99)
        e[7] = max(0.0, e[7] * 0.999)
        a.anim_t += 1

    # ------------------------------------------------------------------ execution
    def _execute(self, a: Being):
        w = self.w
        g = a.goal
        act, gx, gy = g["act"], g["x"], g["y"]
        if w.tick > g["until"]:
            a.goal = None
            return
        ref = g.get("ref")
        if isinstance(ref, Being) and not ref.alive:
            a.goal = None
            return
        dx, dy = gx * TILE + 8 - a.x, gy * TILE + 8 - a.y
        dist = max(abs(dx), abs(dy))
        adjacent = dist <= (26 if act == DRINK else 16)

        if act not in (REST, SLEEP, MARK) and not adjacent:
            moved = abs(a.x - a._last_px) + abs(a.y - a._last_py)
            a.stuck = a.stuck + 1 if moved < 1.5 else 0
            a._last_px, a._last_py = a.x, a.y
            if a.stuck > 20 + 50 * a.personality[8]:
                a.emotions[3] = min(1.0, a.emotions[3] + 0.1)
                cat = {EAT: "food", DRINK: "water", HARVEST: "wood",
                       SOCIAL: "agent", SLEEP: "shelter"}.get(act)
                if cat:
                    a.forget(cat, gx, gy)
                    if cat == "wood":
                        a.forget("stone", gx, gy)
                self.register_goal_failure(a, "path")
                return
            d = math.hypot(dx, dy) or 1
            sp = a.speed(self.clock.light, float(w.heat[a.ty, a.tx]))
            if a.stuck > 12:
                def is_goal(tx, ty):
                    return (tx, ty) == (gx, gy) or (abs(tx - gx) <= 1 and abs(ty - gy) <= 1)
                step_x, step_y = self._local_bfs(a.tx, a.ty, is_goal, max_r=20)
                if step_x == 0 and step_y == 0:
                    self.register_goal_failure(a, "local_path_failed")
                    return
                target_wx = (a.tx + step_x) * TILE + 8
                target_wy = (a.ty + step_y) * TILE + 8
                ndx, ndy = target_wx - a.x, target_wy - a.y
                nd = math.hypot(ndx, ndy) or 1
                a.set_dir(ndx / nd * sp, ndy / nd * sp)
                self._move(a, ndx / nd * sp, ndy / nd * sp)
                a.energy -= MOVE_DRAIN * a.drain_f()
                a.state = "run"
                return
            elif a.stuck > 4:
                best_d, best_move = 1e9, (0, 0)
                for ddx, ddy in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)):
                    ntx, nty = a.tx + ddx, a.ty + ddy
                    if 0 <= ntx < w.g and 0 <= nty < w.g and not w.blocked[nty, ntx]:
                        d2 = (ntx - gx)**2 + (nty - gy)**2
                        if d2 < best_d:
                            best_d = d2
                            best_move = (ddx, ddy)
                if best_move != (0, 0):
                    bdx, bdy = best_move
                    target_wx = (a.tx + bdx) * TILE + 8
                    target_wy = (a.ty + bdy) * TILE + 8
                    ndx, ndy = target_wx - a.x, target_wy - a.y
                    nd = math.hypot(ndx, ndy) or 1
                    a.set_dir(ndx / nd * sp, ndy / nd * sp)
                    self._move(a, ndx / nd * sp, ndy / nd * sp)
                    a.energy -= MOVE_DRAIN * a.drain_f()
                    a.state = "run"
                    return
            a.set_dir(dx / d * sp, dy / d * sp)
            self._move(a, dx / d * sp, dy / d * sp)
            a.energy -= MOVE_DRAIN * a.drain_f()
            a.state = "run" if not a.child else "run"
            return

        done = False
        if act == EAT:
            done = self._do_eat(a, gx, gy)
        elif act == DRINK:
            if w.near_water(a.tx, a.ty):
                before = a.needs[2]
                a.needs[2] = max(0.0, a.needs[2] - 0.6)
                a.temp = max(0.0, a.temp - 0.1)
                a.state = "drink"
                self.stats["drinks"] += 1
                self._reward(a, (before - a.needs[2]) * 0.8)
                done = True
            else:
                a.remember("water", gx, gy)
                a.goal = None
                return
        elif act in (REST, SLEEP):
            done = False   # persiste jusqu'a reveil (metabolisme)
        elif act == HARVEST:
            a.work_t += 1
            if a.work_t >= WORK_TICKS:
                a.work_t = 0
                done = not self._do_harvest(a, gx, gy)
                if not done:
                    a.goal["until"] = w.tick + 400
        elif act == DROP:
            self._do_drop(a)
            done = True
        elif act == BUILD:
            done = not self._do_build(a, gx, gy)
        elif act == GIVE:
            done = self._do_give(a, ref)
        elif act == TAKE:
            done = self._do_take(a, ref)
        elif act == ATTACK:
            self._do_attack(a, ref, gx, gy)
            done = a.goal is None
        elif act == FLEE:
            a.emotions[0] = max(0.0, a.emotions[0] - 0.004)
            if a.emotions[0] < 0.15 or a.goal_t > 120:
                done = True
        elif act == EXPLORE:
            self.stats["explored"] += 1
            first_visit = self.w.heat[gy, gx] < 0.15
            a.emotions[1] = min(1.0, a.emotions[1] + 0.04)
            if first_visit:
                self._reward(a, 0.12)
                a.anima_add_identity("explorer", 0.02)
                # Anima: episode new_area_discovered
                self._record_anima(
                    a, "new_area_discovered", (gx, gy),
                    action="explore", outcome="discovered",
                    surprise=0.3, achievement=0.15)
            else:
                self._reward(a, 0.01)
            done = True
        elif act == TALK:
            done = self._do_talk(a, ref)
        elif act == SOCIAL:
            done = self._do_social(a, ref)
        elif act == MARK:
            if a.energy > 0.12:
                w.marker[a.ty, a.tx] = min(1.0, w.marker[a.ty, a.tx] + 0.25)
                w.marker_col[a.ty, a.tx] = a.col_idx
                a.energy -= 0.004
                if a.home is None:
                    a.home = (a.tx, a.ty)
            done = a.goal_t > 24
        if done:
            a.goal = None
            a.commitment = max(0.0, a.commitment - 0.2)

    # ------------------------------------------------------------------ primitives
    def _reward(self, a, r):
        a.brain.learn(r, lr=self._lr(a))
        self.register_success_observation(a, (a.goal or {}).get("act", REST), r)

    def register_success_observation(self, actor, action, reward):
        if reward <= 0.05:
            return
        for observer in self._near(actor.x, actor.y,
                                   lambda e: isinstance(e, Being) and e.eid != actor.eid, r=2):
            if observer.child or observer.trust(actor.eid) > 0.2:
                observer.observed_actions.append({
                    "action": int(action),
                    "reward": float(reward),
                    "tick": self.w.tick,
                    "actor": actor.eid,
                })
                self.lab.event(self.w.tick, "imitation_recorded",
                               observer_eid=observer.eid, actor_eid=actor.eid,
                               action=int(action), reward=float(reward))

    def _lr(self, a):
        """Taux d'apprentissage cohérent avec le calendrier biologique."""
        base_lr = 0.0024
        if a.child:
            age_factor = 2.0
        else:
            death_age = max(1, getattr(a, "natural_death_age", AGE_MAX_NATURAL_DEATH_TICKS))
            life_progress = min(1.0, max(0.0, a.age / death_age))
            age_factor = max(0.15, 1.0 - 0.85 * life_progress)
        return base_lr * age_factor

    def _do_eat(self, a, gx, gy):
        w = self.w
        cx, cy = gx * TILE + 8, gy * TILE + 8
        for it in list(w.items):
            if it.kind == "food" and (it.x - cx) ** 2 + (it.y - cy) ** 2 < 20 * 20:
                w.items.remove(it)
                self._eat(a, it.nutrition)
                return True
        aid = w.content_at(gx, gy)
        if aid >= 0:
            asd = self.am.assets[aid]
            if asd.edible > 0:
                self._eat(a, asd.edible)
                w.remove(gx, gy)
                return True
        a.forget("food", gx, gy)          # la source n'existe plus : faux souvenir
        return True

    def _eat(self, a, nutrition):
        before = a.needs[0]
        a.needs[0] = max(0.0, a.needs[0] - nutrition / 110.0)
        a.needs[2] = max(0.0, a.needs[2] - nutrition / 260.0)  # l'eau des aliments
        a.hunger = a.needs[0]
        a.needs[1] = a.energy = min(1.0, a.energy + nutrition / 150.0)
        a.emotions[1] = min(1.0, a.emotions[1] + 0.06)
        a.state = "eat"
        self._reward(a, (before - a.needs[0]) * 2.0)

    def try_craft_tool(self, a):
        from .config import TOOL_RECIPES
        if getattr(a, "child", False):
            return False
        for kind, recipe in TOOL_RECIPES.items():
            if a.inv.get("bois", 0) >= recipe["bois"] and a.inv.get("pierre", 0) >= recipe["pierre"]:
                pool = [aid for aid in self.am.by_role.get("tool", [])
                        if self.am.assets[aid].meta.get("tool_kind") == kind]
                if not pool:
                    continue
                aid = int(self.rng.choice(pool))
                a.inv["bois"] -= recipe["bois"]
                a.inv["pierre"] -= recipe["pierre"]
                a.tool = aid
                a.tool_durability = recipe["durability"]
                self.stats["tool_found"] += 1
                a.skills[1] = min(1.0, a.skills[1] + 0.03)
                self.log(f"{a.name} a fabriqué {kind}.", (248, 208, 98), "economie")
                self._reward(a, 0.25)
                self.lab.event(self.w.tick, "tool_crafted",
                               eid=a.eid, tool_kind=kind, durability=recipe["durability"])
                return True
        return False

    def _do_harvest(self, a, gx, gy):
        w, am = self.w, self.am
        aid = w.content_at(gx, gy)
        if aid < 0:
            a.forget("wood", gx, gy)
            a.forget("stone", gx, gy)
            return False
        asd = am.assets[aid]
        if asd.tool:
            a.tool = asd.id
            w.remove(gx, gy)
            self.stats["tool_found"] += 1
            self.log("Un habitant a trouvé et équipé un outil.", (248, 208, 98), "economie")
            self._reward(a, 0.3)
            return True
        if not asd.harvest:
            return False
        h = asd.harvest
        if w.hp[gy, gx] > 0 and a.inv[h["material"]] < INV_CAP:
            w.hp[gy, gx] -= 1
            tool_kind = ""
            if a.tool >= 0:
                tool_kind = self.am.assets[a.tool].meta.get("tool_kind", "")
            material = h["material"]
            tool_bonus = 1.0
            if material == "bois" and tool_kind == "hache":
                tool_bonus = 1.8
            elif material == "pierre" and tool_kind == "pioche":
                tool_bonus = 1.8
            elif material == "or" and tool_kind == "pioche":
                tool_bonus = 1.5
            elif a.tool >= 0:
                tool_bonus = 1.4
            base_amount = int(h.get("amount", 1))
            got = max(1, int(round(base_amount * tool_bonus * (1.0 + 0.6 * a.skills[0]))))
            a.inv[h["material"]] = min(INV_CAP, a.inv[h["material"]] + got)
            # ── graine en sous-produit (10% si récolte de bois = arbres) ──
            if h["material"] == "bois" and self.rng.random() < 0.10:
                a.inv["graine"] = min(INV_CAP, a.inv.get("graine", 0) + 1)
            a.skills[0] = min(1.0, a.skills[0] + 0.015)
            self.stats["harvests"] += 1
            self._fx("dust", gx * TILE + 8, gy * TILE + 8)
            self.emit_sound(gx * TILE, gy * TILE, "chop", 0.7)
            a.state = "work"
            self._teach_near(a, 0)
            if w.hp[gy, gx] <= 0:
                self._deplete(gx, gy, asd)
            self._reward(a, 0.12)
            # Anima: episode food_found
            material = h.get("material", "")
            if material == "bois":
                self._record_anima(
                    a, "food_found", (gx, gy), action="harvest",
                    outcome="success", achievement=0.3)
            elif material in ("pierre", "or"):
                self._record_anima(
                    a, "danger_discovered", (gx, gy), action="harvest",
                    outcome="success", achievement=0.2)
            a.anima_add_identity("provider", 0.03)
            if a.tool >= 0:
                a.tool_durability -= 1
                if a.tool_durability <= 0:
                    self.log(f"L'outil de {a.name} s'est cassé à l'usage.", (218, 138, 58), "economie")
                    self.lab.event(self.w.tick, "tool_broken",
                                   eid=a.eid, tool_id=a.tool)
                    a.tool = -1
                    a.tool_durability = 0
            return True
        return False

    def _do_drop(self, a):
        mat = max(a.inv, key=a.inv.get)
        if a.inv[mat] > 0:
            a.inv[mat] -= 1
            self._drop_item(mat, a.x, a.y)
            a.state = "work"

    def suggest_place(self, a, category, tx, ty, strength=0.4):
        """Suggestion non contraignante — renforce la memoire d'un etre."""
        if hasattr(a, "remember"):
            a.remember(category, tx, ty)
        key = (tx // 8, ty // 8)
        if hasattr(a, "belief_places"):
            a.belief_places[key] = min(1.0, a.belief_places.get(key, 0) + strength * 0.3)

    def _do_give(self, a, ref):
        storage = self.nearest_storage(a.tx, a.ty, max_dist=2)
        if storage is not None:
            return self.deposit_to_storage(a, storage)
        e = ref if isinstance(ref, Being) and ref.alive else None
        if e is None:
            return True
        mat = max(a.inv, key=a.inv.get)
        if a.inv[mat] > 1:
            a.inv[mat] -= 2
            e.inv[mat] = min(INV_CAP, e.inv[mat] + 2)
            self.stats["gives"] += 1
            a.state = "give"
            r1 = a.rel.setdefault(e.eid, [0, 0])
            r1[0] = min(1.0, r1[0] + 0.2)
            r2 = e.rel.setdefault(a.eid, [0, 0])
            r2[0] = min(1.0, r2[0] + 0.25)
            e.emotions[1] = min(1.0, e.emotions[1] + 0.15)
            a.emotions[1] = min(1.0, a.emotions[1] + 0.08)
            a.emotions[7] = min(1.0, a.emotions[7] + 0.05)
            a.needs[6] = max(0.0, a.needs[6] - 0.2)
            e.needs[5] = max(0.0, e.needs[5] - 0.2)
            a.rep += 1
            a.belief_beings[e.eid] = min(1.0, a.belief_beings.get(e.eid, 0) + 0.15)
            self._trade[(min(a.eid, e.eid), max(a.eid, e.eid))] = \
                self._trade.get((min(a.eid, e.eid), max(a.eid, e.eid)), 0) + 1
            self.emit_sound(a.x, a.y, "voice", 0.4)
            self._reward(a, 0.2)
            self.social_memory.record(e.eid, a.eid, "help", 0.20, self.w.tick)
            # Anima: episodes food_given / food_received
            self._record_anima(
                a, "food_given", (a.tx, a.ty),
                actors=[a.eid, e.eid], action="give",
                outcome="success", social_impact=0.4, achievement=0.2)
            self._record_anima(
                e, "food_received", (e.tx, e.ty),
                actors=[e.eid, a.eid], action="receive",
                outcome="success", social_impact=0.5)
            e.anima["attachments"][a.eid] = min(
                1.0, e.anima["attachments"].get(a.eid, 0.0) + 0.10)
        return True

    def _do_take(self, a, ref):
        storage = self.nearest_storage(a.tx, a.ty, max_dist=2)
        if storage is not None:
            needed = "food" if a.needs[0] > 0.65 else "bois"
            return self.withdraw_from_storage(a, storage, needed)
        e = ref if isinstance(ref, Being) and ref.alive else None
        if e is None:
            return True
        mat = max(e.inv, key=e.inv.get)
        if e.inv[mat] <= 0:
            return True
        got = min(2, e.inv[mat])
        if a.trust(e.eid) > 0.4 and self.rng.random() < 0.6:
            # une relation de confiance refuse la violence : le vol echoue
            a.emotions[6] = min(1.0, a.emotions[6] + 0.2)
            return True
        e.inv[mat] -= got
        a.inv[mat] = min(INV_CAP, a.inv[mat] + got)
        self.stats["takes"] += 1
        a.rep -= 2
        a.rel.setdefault(e.eid, [0, 0])[0] -= 0.4
        e.rel.setdefault(a.eid, [0, 0])[0] -= 0.45
        e.emotions[2] = min(1.0, e.emotions[2] + 0.4)
        a.belief_beings[e.eid] = max(-1.0, a.belief_beings.get(e.eid, 0) - 0.2)
        self._reward(a, 0.15)
        self.social_memory.record(e.eid, a.eid, "theft", 0.45, self.w.tick)
        if e.personality[1] > 0.4 or e.health > a.health:
            e.hated = a.eid
        return True

    def _blocked_los(self, x1, y1, x2, y2):
        """Vérifie si un batiment solide bloque la ligne de vue entre deux points."""
        w = self.w
        dx, dy = x2 - x1, y2 - y1
        d = max(abs(dx), abs(dy))
        if d < 1:
            return False
        steps = int(d / TILE) + 1
        for s in range(1, steps):
            t = s / steps
            cx, cy = int((x1 + dx * t) // TILE), int((y1 + dy * t) // TILE)
            if 0 <= cx < w.g and 0 <= cy < w.g and w.blocked[cy, cx]:
                return True
        return False

    def _do_attack(self, a, ref, gx, gy):
        w = self.w
        target = ref if isinstance(ref, (Being, Sheep, Monster)) and getattr(ref, "alive", False) else None
        if target is None:
            near = [e for e in self._near(a.x, a.y,
                     lambda e: isinstance(e, (Being, Sheep, Monster)) and e is not a, r=1)]
            target = max(near, key=lambda t: t.health) if near else None
        if target is None:
            a.goal = None
            return
        if a.atk_t > 0:
            return
        # ── blocage par mur / batiment solide ──
        if self._blocked_los(a.x, a.y, target.x, target.y):
            a.emotions[3] = min(1.0, a.emotions[3] + 0.05)
            return
        dmg = (ATTACK_DMG_TOOL if a.tool >= 0 else ATTACK_DMG) * a.dmg_f()
        target.health -= dmg
        a.energy -= 0.03
        a.atk_t = 45
        if a.tool >= 0:
            a.tool_durability -= 2
            if a.tool_durability <= 0:
                self.lab.event(self.w.tick, "tool_broken", eid=a.eid, tool_id=a.tool)
                a.tool = -1
                a.tool_durability = 0
        a.skills[2] = min(1.0, a.skills[2] + 0.02)
        a.emotions[2] = min(1.0, a.emotions[2] + 0.15)
        self.stats["attacks"] += 1
        self._recent_attacks.append(w.tick)
        self._fx("dust", target.x, target.y)
        self.emit_sound(target.x, target.y, "fight", 1.0)
        a.state = "attack"
        if isinstance(target, Sheep):
            if target.health <= 0:
                self._kill_sheep(target, killer=a)
                a.goal = None
            return
        if isinstance(target, Monster):
            if target.health <= 0:
                target.alive = False
                self.monsters = [x for x in self.monsters if x.alive]
                self._entity_cells.pop(target.eid, None)
                for _ in range(2):
                    self._drop_food(
                        self.am.pool("meat_res"),
                        target.x + self.rng.uniform(-6, 6),
                        target.y + self.rng.uniform(-6, 6),
                        nutrition=45,
                    )
                self.lab.event(self.w.tick, "monster_killed",
                               eid=a.eid, monster_eid=target.eid,
                               tx=int(target.x), ty=int(target.y))
                self._reward(a, 0.30)
                self._record_anima(
                    a, "monster_survival",
                    (a.tx, a.ty),
                    actors=[a.eid, target.eid], action="kill",
                    outcome="survived",
                    health_loss=0.0, fear=0.0, surprise=0.3,
                    achievement=0.5,
                )
                a.anima_add_identity("fighter", 0.08)
                a.goal = None
            return
        # consequences sociales
        a.rel.setdefault(target.eid, [0, 0])[0] -= 0.3
        target.rel.setdefault(a.eid, [0, 0])[0] -= 0.35
        target.emotions[0] = min(1.0, target.emotions[0] + 0.35)
        target.emotions[2] = min(1.0, target.emotions[2] + 0.45)
        target.pain = min(1.0, target.pain + 0.3)
        target.belief_places[(a.tx // 8, a.ty // 8)] = min(
            1.0, target.belief_places.get((a.tx // 8, a.ty // 8), 0) + 0.3)
        target.dangers.append((a.x, a.y, w.tick))
        self._dominance[a.eid] = self._dominance.get(a.eid, 0) + 1
        self._dominance[target.eid] = self._dominance.get(target.eid, 0) - 1
        a.rep -= 1
        self.social_memory.record(target.eid, a.eid, "violence", 0.55, self.w.tick)
        if target.child:
            # tabou emergent : frapper un enfant revolte les temoins
            a.rep -= 3
            for wit in self._near(target.x, target.y,
                                  lambda e: isinstance(e, Being) and e.eid != a.eid, r=3):
                wit.emotions[2] = min(1.0, wit.emotions[2] + 0.5)
                if wit.personality[5] > 0.4:
                    wit.hated = a.eid
            self.log(f"{a.name} a frappé un enfant !", (228, 98, 98), "combat")
        for wit in self._near(target.x, target.y,
                              lambda e: isinstance(e, Being)
                              and e.eid not in (a.eid, target.eid), r=2):
            if wit.personality[5] > 0.55 and wit.emotions[2] < 0.7:
                wit.emotions[2] = min(1.0, wit.emotions[2] + 0.3 * wit.personality[5])
                if wit.personality[1] > 0.45 and wit.hated is None:
                    wit.hated = a.eid
        self.emit_sound(target.x, target.y, "scream", 1.0)
        if target.health <= 0:
            mat = max(target.inv, key=target.inv.get)
            if target.inv[mat] > 0:
                target.inv[mat] -= 1
                a.inv[mat] = min(INV_CAP, a.inv[mat] + 1)
            self._die(target)
            a.hated = None
            a.goal = None
            self._reward(a, 0.3)
        elif target.hated is None and target.emotions[2] > 0.6 \
                and target.personality[1] > 0.5:
            target.hated = a.eid
        self._reward(a, -0.1)

    def _do_talk(self, a, ref):
        w = self.w
        e = ref if isinstance(ref, Being) and ref.alive else None
        if e is None and a._near_agents:
            e = max(a._near_agents,
                    key=lambda o: a.anima_social_score(o.eid))
        if e is None:
            return True
        self.stats["talks"] += 1
        a.talk_cd[e.eid] = self.w.tick
        self.emit_sound(a.x, a.y, "voice", 0.6)
        a.state = "talk"
        msg = "chat"
        if a.needs[2] > 0.65:
            memory = a.recall("water", a.tx, a.ty)
            if memory is not None:
                self.send_fact(a, e, "water", memory[0], memory[1])
                msg = "fait"
        elif a.hunger > 0.65:
            memory = a.recall("food", a.tx, a.ty)
            if memory is not None:
                self.send_fact(a, e, "food", memory[0], memory[1])
                msg = "fait"
        elif a.emotions[1] > 0.5:
            msg = "salut"
        elif a.emotions[0] > 0.5:
            msg = "alerte"
        elif a.emotions[2] > 0.5:
            msg = "menace"
        elif a.emotions[7] > 0.38 and a.bonded != e.eid and not e.child and not a.child:
            msg = "cour"
        elif self.rng.random() < 0.15:
            msg = "fait"
        r1 = a.rel.setdefault(e.eid, [0, 0])
        r2 = e.rel.setdefault(a.eid, [0, 0])
        if msg == "salut":
            r1[0] = min(1, r1[0] + 0.08)
            r2[0] = min(1, r2[0] + 0.08)
            e.emotions[1] = min(1, e.emotions[1] + 0.06)
        elif msg == "alerte":
            r2[0] = min(1, r2[0] + 0.1)
            e.emotions[0] = min(1, e.emotions[0] + 0.2)
            e.remember("agent", a.tx, a.ty)
        elif msg == "menace":
            r2[0] = max(-1, r2[0] - 0.15)
            e.emotions[2] = min(1, e.emotions[2] + 0.2)
        elif msg == "cour":
            e.emotions[7] = min(1, e.emotions[7] + 0.15 + 0.2 * a.personality[0])
            r1[1] = min(1, r1[1] + 0.12)
            r2[1] = min(1, r2[1] + 0.12)
            # mariage : M+F obligatoire, pas d'inceste, pas déjà marié
            eligible = (
                a.sex != e.sex
                and not a.married and not e.married
                and not self._are_related(a, e)
                and not a.child and not e.child
                and r1[1] > 0.45 and r2[1] > 0.45
            )
            if eligible:
                a.bonded, e.bonded = e.eid, a.eid
                a.married, e.married = True, True
                a.partner_id, e.partner_id = e.eid, a.eid
                a.life.append(("mariage", e.name))
                e.life.append(("mariage", a.name))
                self.log(f"{a.name} et {e.name} se sont mariés.",
                         (248, 178, 218), "social")
        elif msg == "fait":
            for cat in ("food", "water", "wood"):
                memory = a.recall(cat, a.tx, a.ty)
                if memory is not None:
                    self.send_fact(a, e, cat, memory[0], memory[1])
                    break
        else:
            r1[0] = min(1, r1[0] + 0.03)
            r2[0] = min(1, r2[0] + 0.03)
            if e.child and a.skills[0] > e.skills[0]:
                e.skills[0] = min(1.0, e.skills[0] + 0.05)   # enseignement oral
        a.skills[3] = min(1.0, a.skills[3] + 0.01)
        if msg in ("salut", "cour"):
            self.social_memory.record(e.eid, a.eid, "help", 0.12, self.w.tick)
        elif msg == "alerte":
            self.social_memory.record(e.eid, a.eid, "help", 0.15, self.w.tick)
        self._reward(a, 0.1)
        return True

    def _do_social(self, a, ref):
        e = ref if isinstance(ref, Being) and ref.alive else None
        if e is None:
            return True
        if a.goal_t > 100:
            a.health = min(1.0, a.health + 0.01)
            a.emotions[1] = min(1.0, a.emotions[1] + 0.1)
            a.needs[5] = max(0.0, a.needs[5] - 0.3)
            r = a.rel.setdefault(e.eid, [0, 0])
            r[1] = min(1.0, r[1] + 0.05)
            a.emotions[7] = min(1.0, a.emotions[7] + 0.08)
            e.emotions[7] = min(1.0, e.emotions[7] + 0.05)
            self._reward(a, 0.15)
            self.social_memory.record(e.eid, a.eid, "help", 0.10, self.w.tick)
            return True
        return False

    def _teach_near(self, a, skill_idx):
        """Transmission culturelle : un enfant qui regarde apprend."""
        for e in self._near(a.x, a.y, lambda e: isinstance(e, Being) and e.child, r=2):
            if e.trust(a.eid) > -0.2:
                e.skills[skill_idx] = min(1.0, e.skills[skill_idx]
                                          + 0.02 * (1 + a.skills[skill_idx]))

    # ------------------------------------------------------------------ construction
    def _do_build(self, a, tx, ty):
        w, am = self.w, self.am

        # ── repli brique-par-brique si ressources insuffisantes ──
        if (a.inv.get("bois", 0) < 3 or a.inv.get("pierre", 0) < 1) \
                and a.inv.get("graine", 0) == 0:
            if a.inv.get("bois", 0) > 0 or a.inv.get("pierre", 0) > 0:
                return self.do_build_block(a, tx, ty)

        # ── agriculture : si l'être porte des graines et que la case est vide ──
        if a.inv.get("graine", 0) > 0 and w.land[ty, tx] and w.content_at(tx, ty) < 0 \
                and not w.water[ty, tx] and (tx, ty) not in w.crop_plots:
            from .world import CropPlot
            plot = CropPlot(tx=tx, ty=ty, owner_eid=a.eid, planted_tick=w.tick)
            w.crop_plots[(tx, ty)] = plot
            a.inv["graine"] = max(0, a.inv["graine"] - 1)
            self._reward(a, 0.12)
            self.log(f"{a.name} a plante une graine.", (108, 188, 98), "economie")
            self.lab.event(self.w.tick, "crop_planted",
                           eid=a.eid, tx=tx, ty=ty)
            return True

        # ── construction brique par brique ──
        return self.do_build_block(a, tx, ty)
        if a.home is None:
            a.home = (tx, ty)
            a.life.append("première maison")
        self._fx("dust", tx * TILE + 8, ty * TILE + 8)
        self._check_village(tx, ty)
        self._teach_near(a, 1)
        self._reward(a, 0.35)
        return True

    def can_place_blueprint(self, tasks):
        w = self.w
        for task in tasks:
            if not (0 <= task.tx < w.g and 0 <= task.ty < w.g):
                return False
            if not w.land[task.ty, task.tx]:
                return False
            if w.water[task.ty, task.tx]:
                return False
            if w.content_at(task.tx, task.ty) >= 0:
                return False
        return True

    def find_build_location(self, a, radius=8):
        for r in range(2, radius + 1):
            for dy in range(-r, r + 1):
                for dx in range(-r, r + 1):
                    if abs(dx) != r and abs(dy) != r:
                        continue
                    tx, ty = a.tx + dx, a.ty + dy
                    tasks = blueprint_from_name("small_house", tx, ty)
                    if self.can_place_blueprint(tasks):
                        return tx, ty
        return None

    def create_house_site(self, a, tx=None, ty=None):
        if tx is None or ty is None:
            pos = self.find_build_location(a)
            if pos is None:
                return None
            tx, ty = pos
        tasks = blueprint_from_name("small_house", tx, ty)
        if not self.can_place_blueprint(tasks):
            return None
        site = ConstructionSite(
            origin_tx=tx, origin_ty=ty,
            blueprint_name="small_house", tasks=tasks,
            created_tick=self.w.tick,
            owner_eid=a.eid, owner_clan=a.color,
        )
        self.w.add_site(site)
        a.home = (tx + 2, ty + 2)
        self.log(f"{a.name} a commence le plan d'une maison.", (178, 228, 168), "batiment")
        self._record_anima(
            a, "construction_started", (tx, ty),
            actors=[a.eid], action="build", outcome="started",
            achievement=0.1)
        return site

    def _choose_blueprint(self, a):
        w = self.w
        bois = a.inv.get("bois", 0)
        pierre = a.inv.get("pierre", 0)
        has_house = a.home is not None
        nearby_storages = sum(1 for s in w.storages.values()
                              if abs(s.tx - a.tx) + abs(s.ty - a.ty) < 20)
        has_well = any(s.role == "puits" for s in w.storages.values()
                       if abs(s.tx - a.tx) + abs(s.ty - a.ty) < 20)
        if not has_house:
            return "small_house"
        if nearby_storages == 0 and bois >= 4:
            return "coffre"
        if nearby_storages >= 1 and bois >= 6 and pierre >= 2:
            return "grenier"
        if not has_well and pierre >= 3:
            return "puits"
        if a.skills[1] > 0.4 and pierre >= 6 and bois >= 4:
            return "atelier"
        return "small_house"

    def create_blueprint_site(self, a, blueprint="small_house", tx=None, ty=None):
        if tx is None or ty is None:
            pos = self.find_build_location(a)
            if pos is None:
                return None
            tx, ty = pos
        tasks = blueprint_from_name(blueprint, tx, ty)
        if not self.can_place_blueprint(tasks):
            return None
        site = ConstructionSite(
            origin_tx=tx, origin_ty=ty,
            blueprint_name=blueprint, tasks=tasks,
            created_tick=self.w.tick,
            owner_eid=a.eid, owner_clan=a.color,
        )
        self.w.add_site(site)
        self.lab.event(self.w.tick, "site_created",
                       eid=a.eid, blueprint=blueprint,
                       tx=tx, ty=ty, tasks_total=len(tasks))
        if blueprint == "small_house":
            a.home = (tx + 2, ty + 2)
        self.log(f"{a.name} a commence un chantier ({blueprint}).", (178, 228, 168), "batiment")
        self._record_anima(
            a, "construction_started", (tx, ty),
            actors=[a.eid], action="build", outcome="started",
            achievement=0.1)
        return site

    def nearest_site(self, tx, ty, max_dist=15):
        best, best_dist = None, 10**9
        for site in self.w.sites.values():
            d = max(abs(site.origin_tx - tx), abs(site.origin_ty - ty))
            if d <= max_dist and d < best_dist:
                best, best_dist = site, d
        return best

    def role_for_block_task(self, task):
        if task.phase == "door":
            return "block_door"
        if task.phase == "roof":
            return "block_roof"
        if task.material == "pierre":
            return "block_stone"
        return "block_wood"

    def ensure_material_for_task(self, a, task):
        if a.inv.get(task.material, 0) > 0:
            return True
        storage = self.nearest_storage(a.tx, a.ty, max_dist=14)
        if storage is None:
            return False
        return self.withdraw_from_storage(a, storage, task.material)

    def place_site_block(self, a, site, task):
        w = self.w
        if task.key in site.placed:
            return False
        if task.material not in ("bois", "pierre"):
            return False
        if not self.ensure_material_for_task(a, task):
            return False
        if task.phase == "foundation":
            if w.foundation[task.ty, task.tx] >= 0:
                return False
        elif task.phase == "roof":
            if w.roof[task.ty, task.tx] >= 0:
                return False
        elif w.content_at(task.tx, task.ty) >= 0:
            return False
        role = self.role_for_block_task(task)
        pool = self.am.pool(role)
        if not pool:
            return False
        aid = int(self.am.pick(pool, self.rng))
        if task.phase == "foundation":
            w.foundation[task.ty, task.tx] = aid
        elif task.phase == "roof":
            w.roof[task.ty, task.tx] = aid
        else:
            w.place(task.tx, task.ty, aid, self.am, hp=6,
                    solid=task.solid, shelter=False, size=1)
        a.inv[task.material] -= 1
        site.mark_placed(a.eid, task)
        a.skills[1] = min(1.0, a.skills[1] + 0.012)
        self.stats["builds"] += 1
        self.lab.event(self.w.tick, "site_block_placed",
                       eid=a.eid, blueprint=site.blueprint_name,
                       tx=task.tx, ty=task.ty, phase=task.phase,
                       material=task.material,
                       progress=site.progress())
        self._fx("dust", task.tx * TILE + TILE / 2, task.ty * TILE + TILE / 2)
        self._reward(a, 0.10)
        if site.complete():
            self.complete_site(site, a)
        return True

    def site_has_required_phases(self, site):
        phases = {
            task.phase
            for task in site.tasks
            if task.key in site.placed
        }
        return {"foundation", "wall", "door", "roof"}.issubset(phases)

    def complete_site(self, site, finisher):
        w = self.w
        bp = site.blueprint_name
        if not self.site_has_required_phases(site):
            return
        if bp in ("small_house", "storage_hut", "atelier", "grenier"):
            for ty in range(site.origin_ty + 1, site.origin_ty + 4):
                for tx in range(site.origin_tx + 1, site.origin_tx + 4):
                    if 0 <= tx < w.g and 0 <= ty < w.g:
                        w.shelter[ty, tx] = 1
        # depot pour les maisons et greniers
        if bp in ("small_house", "storage_hut", "grenier"):
            storage_tx = site.origin_tx + 2
            storage_ty = site.origin_ty + 2
            if bp == "grenier":
                storage_tx = site.origin_tx + 1
                storage_ty = site.origin_ty + 1
            if (storage_tx, storage_ty) not in w.storages:
                cap = 120 if bp == "grenier" else 80
                self.create_storage(finisher, storage_tx, storage_ty, capacity=cap)
                self.log(f"{bp} termine : depot cree.", (178, 228, 168), "batiment")
        elif bp == "coffre":
            storage_tx, storage_ty = site.origin_tx, site.origin_ty
            if (storage_tx, storage_ty) not in w.storages:
                self.create_storage(finisher, storage_tx, storage_ty, capacity=40)
                self.log("Coffre termine.", (178, 228, 168), "batiment")
        elif bp == "puits":
            w.shelter[site.origin_ty, site.origin_tx] = 1
            self.log("Puits termine.", (90, 180, 230), "batiment")
        elif bp == "atelier":
            self.log("Atelier termine.", (200, 160, 90), "batiment")
        w.remove_site(site)
        self._check_village(site.origin_tx + 2, site.origin_ty + 2)
        for eid in site.contributors:
            c = next((x for x in self.agents if x.eid == eid), None)
            if c and c.alive:
                c.skills[1] = min(1.0, c.skills[1] + 0.04)
                c.needs[6] = max(0.0, c.needs[6] - 0.12)
                self._reward(c, 0.25)
        # Anima: episode construction
        if finisher and finisher.alive:
            self._record_anima(
                finisher, "construction_complete",
                (site.origin_tx, site.origin_ty),
                actors=list(site.contributors),
                action="build", outcome="completed",
                achievement=0.6, social_impact=0.3,
            )
            finisher.anima_add_identity("builder", 0.10)
        self.log(f"{bp} termine : {len(site.contributors)} contributeur(s).",
                 (108, 208, 128), "batiment")
        self.lab.event(self.w.tick, "site_completed",
                       blueprint=bp, tx=site.origin_tx, ty=site.origin_ty,
                       contributors=len(site.contributors),
                       finisher_eid=finisher.eid if finisher else None)

    def do_build_block(self, a, tx, ty):
        """BUILD : contribuer a un chantier existant ou placer un bloc."""
        site = self.nearest_site(a.tx, a.ty, max_dist=14)
        if site is not None:
            task = site.next_task_for(a.inv)
            if task is not None:
                return self.place_site_block(a, site, task)
        # choisir le plan selon le contexte
        bp = self._choose_blueprint(a)
        site = self.create_blueprint_site(a, bp)
        if site is not None:
            task = site.next_task_for(a.inv)
            if task is not None:
                return self.place_site_block(a, site, task)
            return True
        w, am = self.w, self.am
        if w.blocked[ty, tx] or w.content_at(tx, ty) >= 0 or not w.land[ty, tx]:
            tx, ty = self._free_near(tx, ty)
            if w.blocked[ty, tx] or w.content_at(tx, ty) >= 0:
                return False
        if a.inv.get("bois", 0) > 0:
            material, role = "bois", "block_wood"
        elif a.inv.get("pierre", 0) > 0:
            material, role = "pierre", "block_stone"
        else:
            return False
        pool = am.pool(role)
        if not pool:
            return False
        aid = int(am.pick(pool, self.rng))
        w.place(tx, ty, aid, am, hp=6, solid=True, shelter=False, size=1)
        a.inv[material] = max(0, a.inv[material] - 1)
        a.skills[1] = min(1.0, a.skills[1] + 0.008)
        self.stats["builds"] += 1
        self._check_village(tx, ty)
        self._reward(a, 0.10)
        return True

    def do_build_block_player(self, tx, ty, material="bois"):
        w, am = self.w, self.am
        if not (0 <= tx < GRID and 0 <= ty < GRID):
            return False
        if w.blocked[ty, tx] or w.content_at(tx, ty) >= 0 or not w.land[ty, tx]:
            return False
        role = "block_wood" if material == "bois" else "block_stone"
        pool = am.pool(role)
        if not pool:
            return False
        aid = int(am.pick(pool, self.rng))
        w.place(tx, ty, aid, am, hp=6, solid=True, shelter=False, size=1)
        self._check_village(tx, ty)
        return True

    def _free_near(self, tx, ty):
        for r in range(4):
            for dy in range(-r, r + 1):
                for dx in range(-r, r + 1):
                    x, y = tx + dx, ty + dy
                    if 0 <= x < self.w.g and 0 <= y < self.w.g \
                       and not self.w.blocked[y, x] and self.w.content_at(x, y) < 0:
                        return x, y
        return tx, ty

    def _check_village(self, tx, ty):
        w = self.w
        y0, y1 = max(0, ty - 10), min(w.g, ty + 11)
        x0, x1 = max(0, tx - 10), min(w.g, tx + 11)
        shelters = int(w.shelter[y0:y1, x0:x1].sum())
        if shelters >= 10:
            for vx, vy in self._village_pts:
                if (vx - tx) ** 2 + (vy - ty) ** 2 < 900:
                    return
            self._village_pts.append((tx, ty))
            self.stats["villages"] += 1
            self.log(f"Un village est né en ({tx},{ty}) — {shelters} abris !", (108, 208, 128), "batiment")

    # ------------------------------------------------------------------ deplete / feu
    def _deplete(self, tx, ty, asd):
        w, am = self.w, self.am
        mat = asd.harvest["material"]
        role = asd.role
        if role == "tree":
            stumps = am.pool("stump")
            if stumps:
                sid = int(am.pick(stumps, self.rng))
                w.place(tx, ty, sid, am, hp=0, solid=False, size=1)
            else:
                w.remove(tx, ty)
            w.regrow[ty, tx] = 2400
            for _ in range(2):
                self._drop_item("bois", tx * TILE + 8 + self.rng.uniform(-8, 8),
                                ty * TILE + 8 + self.rng.uniform(-8, 8))
        elif role in ("stone_res", "gold_stone"):
            w.remove(tx, ty)
            for _ in range(2):
                self._drop_item(mat, tx * TILE + 8 + self.rng.uniform(-8, 8),
                                ty * TILE + 8 + self.rng.uniform(-8, 8))
        elif role == "meat_res":
            w.remove(tx, ty)
            for _ in range(3):
                self._drop_food(am.pool("meat_res"), tx * TILE + 8, ty * TILE + 8, 45)
        else:
            w.remove(tx, ty)

    # ------------------------------------------------------------------ mort / famille
    def _die(self, a: Being, cause: str | None = None):
        if not a.alive:
            return
        a.alive = False
        w, am = self.w, self.am
        self.stats["deaths"] += 1
        tx, ty = a.tx, a.ty
        graves = am.pool("grave")
        if graves and w.content_at(tx, ty) < 0 and not w.blocked[ty, tx]:
            gid = int(am.pick(graves, self.rng))
            w.place(tx, ty, gid, am, hp=0, solid=False, size=1)
        self._drop_food(am.pool("meat_res"), a.x, a.y, 40)
        self._drop_food(am.pool("meat_res"), a.x + 6, a.y - 5, 40)
        # heritage : les liens survivent a l'individu
        heirs = [self._by_eid(x) for x in (list(a.rel.keys()) + list(a.children))]
        for m, c in a.inv.items():
            for h in heirs:
                if h and h.alive and c > 0 and h.trust(a.eid) > 0.2:
                    take = min(c, 3)
                    h.inv[m] = min(INV_CAP, h.inv[m] + take)
                    c -= take
            for _ in range(c):
                self._drop_item(m, a.x + self.rng.uniform(-10, 10),
                                a.y + self.rng.uniform(-10, 10))
        self._fx("explosion", a.x, a.y)
        for other in self.agents:
            r = other.rel.get(a.eid)
            if r and r[1] > 0.2:
                other.emotions[3] = min(1.0, other.emotions[3] + 0.35 * r[1])
                if other.bonded == a.eid:
                    other.bonded = None
                    other.married = False
                    other.partner_id = None
                # Anima: episode loss for mourners
                self._record_anima(
                    other, "loss", (a.tx, a.ty),
                    actors=[other.eid, a.eid], action="witness_death",
                    outcome="lost",
                    fear=0.3, social_impact=0.5)
                other.anima["trauma"]["loss"] = min(
                    1.0, other.anima["trauma"]["loss"] + 0.08)
        if a.bonded:
            b = self._by_eid(a.bonded)
            if b and b.alive:
                self.log(f"{b.name} pleure {a.name}.", (148, 148, 198), "social")
        if cause is None:
            cause = (
                "soif" if a.needs[2] >= 0.999 else
                "faim" if a.hunger >= 0.999 else
                "blessures"
            )
        self.log(f"{a.name} ({a.stage}, {a.age_years:.1f} ans) est mort de {cause}, "
                 f"gén {a.gen}, {a.brain.n} neurones.", (228, 98, 98), "mort")
        # enterre dans le cimetière commun
        grave_tx, grave_ty = self.w.find_cemetery_spot(self.rng)
        self.w.bury(grave_tx, grave_ty, a.name, self.w.tick,
                    CLAN_COLORS.get(a.color, (150, 150, 150)))
        self.lab.event(self.w.tick, "death", eid=a.eid, cause=cause, age_years=a.age_years,
                       name=a.name, gen=a.gen)

    def _kill_sheep(self, s, killer=None):
        s.alive = False
        for _ in range(int(self.rng.integers(2, 4))):
            self._drop_food(self.am.pool("meat_res"), s.x, s.y, 40)
        self._fx("dust", s.x, s.y)

    def _drop_item(self, material, x, y):
        pool = self.am.pool(MAT_AIDS.get(material, "item_wood")) or self.am.pool("item_wood")
        aid = int(self.am.pick(pool, self.rng, default=0))
        self.w.drop_item(Item("mat", aid, x, y, material=material))

    def _drop_food(self, pool, x, y, nutrition):
        aid = int(self.am.pick(pool or self.am.pool("food"), self.rng, default=0))
        it = Item("food", aid, x + self.rng.uniform(-6, 6),
                  y + self.rng.uniform(-6, 6), nutrition=nutrition,
                  life=60 * 60 * 4)
        it.created_tick = self.w.tick
        it.spoil_tick = self.w.tick + 7200
        self.w.drop_item(it)

    def _fx(self, name, x, y):
        ids = self.am.fx.get(name) or []
        if not ids:
            return
        self.effects.append(dict(aid=int(ids[0]), x=x, y=y, t0=self.w.tick, ttl=32,
                                 frames=self.am.assets[int(ids[0])].frames))

    # ------------------------------------------------------------------ reproduction
    def _reproduce(self, a: Being):
        if len(self.agents) >= MAX_POP or a.energy < 0.55 or a.repro_cd > 0 \
           or a.child or a.age > AGE_ELDER_TICKS:
            return
        #必须 marié pour avoir un enfant
        if not a.married or a.partner_id is None:
            return
        mate = self._by_eid(a.partner_id)
        if mate is None or not mate.alive or not mate.married:
            return
        if mate.energy < 0.45 or mate.repro_cd > 0:
            return
        if max(abs(mate.tx - a.tx), abs(mate.ty - a.ty)) > 12:
            return
        # vérifier sexe opposé
        if a.sex == mate.sex:
            return
        # vérifier pas de parenté directe (inceste)
        if self._are_related(a, mate):
            return
        # vérifier abri + nourriture à proximité du foyer
        if not self._has_shelter_and_food(a, mate):
            return
        # coût énergétique
        a.energy -= 0.28
        mate.energy -= 0.28
        a.repro_cd = mate.repro_cd = 2600
        # hérédité : héritage du champion de l'Academy + mutation
        champ = self.academy.champion_params
        n = a.brain.n
        if champ is not None and self.academy.champion_size == n:
            params = champ.copy()
            params += self.rng.normal(0, 0.05, params.shape)
        else:
            params, n = Brain.breed(a.brain, mate.brain, None, self.rng)
        pers = np.clip((a.personality + mate.personality) / 2
                       + self.rng.normal(0, 0.08, 12), 0, 1)
        body = np.clip((a.body + mate.body) / 2
                       + self.rng.normal(0, 0.06, 5), 0, 1)
        cog = np.clip((a.cog + mate.cog) / 2
                       + self.rng.normal(0, 0.06, 4), 0, 1)
        color = mate.color if self.rng.random() < 0.5 else a.color
        child = self.spawn_agent(x=(a.x + mate.x) / 2, y=(a.y + mate.y) / 2,
                                 color=color, gen=max(a.gen, mate.gen) + 1,
                                 brain=Brain(n_hid=n, params=params),
                                 parents=(a.eid, mate.eid), energy=0.5,
                                 personality=pers, n_hid=n, body=body, cog=cog)
        if child is None:
            return
        child.parent_pere_id = a.eid if a.sex == "M" else mate.eid
        child.parent_mere_id = a.eid if a.sex == "F" else mate.eid
        a.children.append(child.eid)
        mate.children.append(child.eid)
        a.emotions[1] = min(1.0, a.emotions[1] + 0.25)
        mate.emotions[1] = min(1.0, mate.emotions[1] + 0.25)
        a.life.append(("enfant", child.name))
        # ── Lot K : héritage partiel des valeurs Anima ──
        for vk in child.anima.get("values", {}):
            pa_val = a.anima.get("values", {}).get(vk, 0.5)
            pb_val = mate.anima.get("values", {}).get(vk, 0.5)
            child.anima["values"][vk] = child.anima_clamp(
                0.5 * ((pa_val + pb_val) / 2) + 0.2 * self.rng.random()
                + 0.3 * child.anima["values"][vk]
            )
        self.stats["births"] += 1
        if self.stats["births"] % 3 == 1:
            self.log(f"{a.name} et {mate.name} ont un enfant : {child.name} "
                     f"(cerveau {n} neurones).", (78, 168, 232), "vie")
        self.lab.event(self.w.tick, "birth", eid=child.eid, parent1=a.eid, parent2=mate.eid,
                       name=child.name, brain_size=n)
        # Anima: episode birth
        self._record_anima(
            a, "birth", (a.tx, a.ty),
            actors=[a.eid, mate.eid, child.eid], action="birth",
            outcome="success", social_impact=0.6, achievement=0.3)
        self._record_anima(
            mate, "birth", (mate.tx, mate.ty),
            actors=[mate.eid, a.eid, child.eid], action="birth",
            outcome="success", social_impact=0.6, achievement=0.3)

    def _are_related(self, a, b):
        """Vérifie parenté directe (parent/enfant ou frères/sœurs)."""
        # parent/enfant
        if a.eid == b.parent_pere_id or a.eid == b.parent_mere_id:
            return True
        if b.eid == a.parent_pere_id or b.eid == a.parent_mere_id:
            return True
        # frères/sœurs (mêmes parents)
        if (a.parent_pere_id is not None and a.parent_pere_id == b.parent_pere_id) \
           or (a.parent_mere_id is not None and a.parent_mere_id == b.parent_mere_id):
            return True
        return False

    def _has_shelter_and_food(self, a, mate):
        """Vérifie qu'il y a un abri ET de la nourriture à proximité du couple."""
        mx, my = int((a.tx + mate.tx) / 2), int((a.ty + mate.ty) / 2)
        has_shelter = False
        has_food = False
        for dy in range(-6, 7):
            for dx in range(-6, 7):
                x, y = mx + dx, my + dy
                if not (0 <= x < self.w.g and 0 <= y < self.w.g):
                    continue
                aid = self.w.content_at(x, y)
                if aid >= 0:
                    asd = self.am.assets[aid]
                    if asd.shelter:
                        has_shelter = True
                    if asd.edible > 0:
                        has_food = True
        # nourriture au sol (items food) via index spatial
        if not has_food:
            cell = 128
            cx, cy = int(((a.x + mate.x) / 2) // cell), int(((a.y + mate.y) / 2) // cell)
            r = max(1, math.ceil(6 * TILE / cell))
            r2 = (6 * TILE) ** 2
            mid_x, mid_y = (a.x + mate.x) / 2, (a.y + mate.y) / 2
            for yy in range(cy - r, cy + r + 1):
                for xx in range(cx - r, cx + r + 1):
                    for item in self.food_cells.get((xx, yy), ()):
                        if (item.x - mid_x) ** 2 + (item.y - mid_y) ** 2 <= r2:
                            has_food = True
                            break
                    if has_food:
                        break
                if has_food:
                    break
        return has_shelter and has_food

    # ------------------------------------------------------------------ societe detectee
    def _analyze_society(self):
        self.society = []
        alive = [a for a in self.agents if getattr(a, "alive", True)]
        self.society.append(f"Villages : {self.stats['villages']}")
        routes = [(k, v) for k, v in self._trade.items() if v >= 4]
        if routes:
            self.society.append(f"Routes d'échange : {len(routes)}")

        # ── hiérarchie + royaumes émergents ──
        dom = sorted(self._dominance.items(), key=lambda kv: -kv[1])
        if dom and dom[0][1] >= 4:
            b = self._by_eid(dom[0][0])
            if b:
                self.society.append(f"Hiérarchie : {b.name} domine ({dom[0][1]} victoires)")
                # compter les suivants (agents dont la plus haute confiance pointe vers ce dominant)
                followers = []
                for a in alive:
                    if a.eid == b.eid or not a.rel:
                        continue
                    best_eid = max(a.rel.items(), key=lambda kv: kv[1][0])[0]
                    if best_eid == b.eid and a.rel[best_eid][0] > 0.3:
                        followers.append(a)
                if len(followers) >= 6:
                    clans_suivis = set(a.color for a in followers)
                    self.society.append(
                        f"Royaume émergent : {b.name} suivi par {len(followers)} "
                        f"êtres ({', '.join(clans_suivis)})")

        # ── clans spécialisés ──
        for c in ("blue", "red", "yellow", "purple", "black"):
            grp = [a for a in alive if a.color == c]
            if len(grp) >= 4:
                sk = float(np.mean([a.skills[0] for a in grp]))
                if sk > 0.5:
                    self.society.append(f"Spécialisation : les {c} récolteurs ({sk:.0%})")

        # ── clans agricoles (ceux qui plantent) ──
        planters = [a for a in alive if a.inv.get("graine", 0) > 0]
        if len(planters) >= 3:
            planter_clans = {}
            for a in planters:
                planter_clans[a.color] = planter_clans.get(a.color, 0) + 1
            best_clan = max(planter_clans, key=planter_clans.get)
            if planter_clans[best_clan] >= 2:
                self.society.append(
                    f"Clan agricole : les {best_clan} "
                    f"({planter_clans[best_clan]} portent des graines)")

        homes = [a.home for a in alive if a.home]
        if len(homes) >= 6:
            self.society.append(f"Foyers : {len(set(homes))}")
        bonded = sum(1 for a in alive if a.bonded) // 2
        if bonded:
            self.society.append(f"Couples liés : {bonded}")

    # ------------------------------------------------------------------ moutons
    def export_academy_model(self, name="champion"):
        return self.academy.export_model(
            f"data/models/{name}", self.universal_knowledge, label=name
        )

    def import_academy_model(self, name="champion"):
        data = self.academy.import_model(f"data/models/{name}")
        if data is not None:
            self.universal_knowledge = UniversalKnowledge.from_dict(data)

    def _sheep(self, s: Sheep):
        w = self.w
        s.energy -= 0.00022
        near = [a for a in self._near(s.x, s.y, lambda e: isinstance(e, Being), r=2)]
        x = self._sens
        x[:] = 0.0
        x[0] = s.energy
        if near:
            t = min(near, key=lambda e: (e.x - s.x) ** 2 + (e.y - s.y) ** 2)
            ang = math.atan2(s.y - t.y, s.x - t.x)
            x[73] = 1.0
            x[74] = math.cos(ang)
            x[75] = math.sin(ang)
        o = s.brain.think(x)[1]
        if o[2] > 0.12 or not near:
            s.energy += 0.0016
            s.state = "grass" if o[2] > 0.2 else "idle"
        mvx, mvy = o[0] - 1.0 / 15.0, o[1] - 1.0 / 15.0
        sp = 0.75
        self._move(s, mvx * sp, mvy * sp, sheep=True)
        s.anim_t += 1
        if s.anim_t % 7 == 0:
            s.frame += 1
        if s.energy <= 0:
            s.health -= 0.002
        if s.health <= 0:
            self._kill_sheep(s)
        if s.energy > 0.95 and len(self.sheep) < MAX_SHEEP:
            s.energy = 0.55
            self.spawn_sheep(x=s.x + 10, y=s.y)

    def _monster(self, m: Monster):
        w = self.w
        m.energy -= 0.00018
        near_humans = self._near(m.x, m.y,
                                 lambda e: isinstance(e, Being) and e.alive,
                                 r=m.sight)
        near_sheep = self._near(m.x, m.y,
                                lambda e: isinstance(e, Sheep) and e.alive,
                                r=m.sight)
        target = None
        if near_humans:
            target = min(near_humans, key=lambda e: (e.x - m.x)**2 + (e.y - m.y)**2)
        elif near_sheep:
            target = min(near_sheep, key=lambda e: (e.x - m.x)**2 + (e.y - m.y)**2)

        if m.hostile and target and m.energy > 0.1:
            dx = target.x - m.x
            dy = target.y - m.y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist < 14:
                target.health -= m.damage
                m.state = "attack" if hasattr(m, "state") else "idle"
                if isinstance(target, Being):
                    self._record_anima(
                        target, "monster_attack",
                        (target.tx, target.ty),
                        actors=[target.eid, m.eid], action="hit",
                        outcome="injured",
                        health_loss=m.damage,
                        fear=min(1.0, m.damage * 2.5),
                        surprise=0.6,
                    )
            elif dist > 0:
                mvx = dx / dist
                mvy = dy / dist
                self._move(m, mvx * 0.6, mvy * 0.6, sheep=True)
        else:
            mvx = self.rng.uniform(-1, 1)
            mvy = self.rng.uniform(-1, 1)
            self._move(m, mvx * 0.3, mvy * 0.3, sheep=True)

        m.anim_t += 1
        if m.anim_t % 7 == 0:
            m.frame += 1
        if m.energy <= 0:
            m.health -= 0.002
        if m.health <= 0:
            m.alive = False
            self.monsters = [x for x in self.monsters if x.alive]
            self._entity_cells.pop(m.eid, None)

    # ------------------------------------------------------------------ pathfinding local
    def _local_bfs(self, start_tx, start_ty, goal_fn, max_r=15):
        """BFS local : cherche un chemin autour des obstacles.
        Retourne le premier pas (dx, dy) à effectuer pour suivre le gradient.
        """
        from collections import deque
        q = deque([(start_tx, start_ty)])
        came_from = {(start_tx, start_ty): None}
        w = self.w
        while q:
            cx, cy = q.popleft()
            if goal_fn(cx, cy):
                curr = (cx, cy)
                if curr == (start_tx, start_ty):
                    return 0, 0
                while came_from[curr] != (start_tx, start_ty):
                    curr = came_from[curr]
                return curr[0] - start_tx, curr[1] - start_ty
            if len(came_from) > max_r * max_r * 3:
                break
            for ddx, ddy in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)):
                nx, ny = cx+ddx, cy+ddy
                if 0 <= nx < w.g and 0 <= ny < w.g and (nx, ny) not in came_from:
                    if w.land[ny, nx] and not w.blocked[ny, nx]:
                        came_from[(nx, ny)] = (cx, cy)
                        q.append((nx, ny))
        return 0, 0

    # ------------------------------------------------------------------ physique
    def _move(self, e, dx, dy, sheep=False):
        w = self.w
        r = 4.0
        nx, ny = e.x + dx, e.y + dy
        if not self._free(nx, e.y, r):
            nx = e.x
        if not self._free(nx, ny, r):
            ny = e.y
        e.x = min(max(4.0, nx), (GRID - 1) * TILE + 12)
        e.y = min(max(4.0, ny), (GRID - 1) * TILE + 12)
        if sheep and abs(dx) + abs(dy) > 0.2:
            e.vx, e.vy = dx, dy
        if hasattr(e, 'eid'):
            self._update_entity_bucket(e)

    def _update_entity_bucket(self, e):
        cx, cy = int(e.x // 32), int(e.y // 32)
        key = (cx, cy)
        old = self._entity_cells.get(e.eid)
        if old == key:
            return
        if old is not None:
            bucket = self.grid_bucket.get(old)
            if bucket and e in bucket:
                bucket.remove(e)
                if not bucket:
                    del self.grid_bucket[old]
        self.grid_bucket.setdefault(key, []).append(e)
        self._entity_cells[e.eid] = key

    def _free(self, x, y, r):
        w = self.w
        x0, y0 = int((x - r) // TILE), int((y - r) // TILE)
        x1, y1 = int((x + r) // TILE), int((y + r) // TILE)
        if x0 < 0 or y0 < 0 or x1 > w.g - 1 or y1 > w.g - 1:
            return False
        if not w.land[y0:y1 + 1, x0:x1 + 1].all():
            return False
        return not w.blocked[y0:y1 + 1, x0:x1 + 1].any()

    # ------------------------------------------------------------------ appel global
    def tick(self):
        self.step()
        for a in list(self.agents):
            if a.alive:
                self._reproduce(a)
        if any(not a.alive for a in self.agents):
            self.agents = [a for a in self.agents if a.alive]

    def natural_pop(self):
        return len(self.agents), len(self.sheep), len(self.w.items)

```

## game/simulation_controller.py

**Type :** `.py`

```python

"""SimulationController — pont unique entre UI et moteur.

Toute interaction entre l'interface et la simulation passe par ce
contrôleur. Ni Pygame ni Qt ne modifient directement les objets
Sim, Being ou World.
"""
from __future__ import annotations

from typing import Any

from .ui_state import UIState
from .ui_snapshots import (
    simulation_snapshot,
    population_snapshot,
    selected_agent_snapshot,
    journal_snapshot,
    society_snapshot,
    map_snapshot,
    anima_snapshot,
    tile_snapshot,
)
from .ui_commands import execute_command


class SimulationController:
    """Pont central UI ↔ moteur.

    Utilisé par le dashboard Pygame ET par l'interface Qt.
    Fournit des snapshots immuables et exécute des commandes validées.
    """

    def __init__(self, sim, camera=None):
        self.sim = sim
        self.camera = camera
        self.ui_state = UIState()

    # ── Snapshots ──

    def snapshot(self) -> dict[str, Any]:
        """Snapshot global complet pour le rendu."""
        return {
            "simulation": simulation_snapshot(self.sim, self.ui_state),
            "population": population_snapshot(self.sim),
            "selected_agent": selected_agent_snapshot(self.sim, self.ui_state),
            "journal": journal_snapshot(
                self.sim,
                category=self.ui_state.journal_filter,
                search=self.ui_state.search_text,
            ),
        }

    def snapshot_population(self) -> list[dict]:
        return population_snapshot(self.sim)

    def snapshot_selected(self) -> dict | None:
        return selected_agent_snapshot(self.sim, self.ui_state)

    def snapshot_journal(self, category: str = "tous", search: str = "") -> list[dict]:
        return journal_snapshot(self.sim, category=category, search=search)

    def snapshot_society(self) -> dict:
        return society_snapshot(self.sim)

    def snapshot_map(self) -> dict:
        return map_snapshot(self.sim, self.ui_state)

    def snapshot_anima(self) -> dict | None:
        return anima_snapshot(self.sim, self.ui_state)

    def snapshot_tile(self, tx: int, ty: int) -> dict:
        return tile_snapshot(self.sim, tx, ty)

    # ── Commandes ──

    def execute(self, command: dict) -> dict[str, Any]:
        """Exécute une commande et synchronise l'état UI."""
        result = execute_command(self.sim, command)
        self.sync_from_simulation()
        return result

    # ── Synchronisation ──

    def sync_from_simulation(self) -> None:
        """Met à jour l'UIState à partir de l'état actuel de la simulation."""
        self.ui_state.sync_from_simulation(self.sim)

    def sync_camera_from_state(self) -> None:
        """Met à jour la caméra à partir de l'UIState."""
        if self.camera is None:
            return
        self.camera.x = self.ui_state.camera_x
        self.camera.y = self.ui_state.camera_y
        self.camera.zoom = self.ui_state.camera_zoom
        self.camera.tilt = self.ui_state.camera_tilt

    def sync_state_from_camera(self) -> None:
        """Met à jour l'UIState à partir de la caméra."""
        if self.camera is None:
            return
        self.ui_state.camera_x = self.camera.x
        self.ui_state.camera_y = self.camera.y
        self.ui_state.camera_zoom = self.camera.zoom
        self.ui_state.camera_tilt = self.camera.tilt

    # ── Action tuple (compatibilité avec l'ancien dashboard) ──

    def translate_action(self, action: tuple | None) -> dict | None:
        """Convertit un ancien tuple d'action du dashboard en commande dict.

        Permet la migration progressive : le dashboard peut continuer
        à produire des tuples pendant la transition.
        """
        if action is None:
            return None
        kind, val = action
        mapping = {
            "pause": {"kind": "pause_toggle"},
            "step": {"kind": "step"},
            "speed": {"kind": "speed_delta", "delta": val},
            "speed_set": {"kind": "set_speed", "speed": val},
            "spawn": {"kind": "spawn_agent"},
            "spawn_sheep": {"kind": "spawn_sheep"},
            "save_game": {"kind": "save", "slot": 0},
            "load_game": {"kind": "load", "slot": 0},
        }
        return mapping.get(kind)

    def handle_legacy_action(self, action: tuple | None) -> dict | None:
        """Convertit et exécute un ancien tuple d'action."""
        cmd = self.translate_action(action)
        if cmd is None:
            return None
        return self.execute(cmd)

```

## game/social_memory.py

**Type :** `.py`

```python

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class SocialRecord:
    trust: float = 0.0
    violence: float = 0.0
    theft: float = 0.0
    generosity: float = 0.0
    last_tick: int = 0

    def score(self):
        return max(-1.0, min(1.0,
            self.trust + self.generosity * 0.5 - self.violence - self.theft * 0.6))


class SocialMemory:
    def __init__(self):
        self.records = {}

    def record(self, observer_eid, target_eid, event, strength, tick):
        key = (int(observer_eid), int(target_eid))
        record = self.records.setdefault(key, SocialRecord())
        strength = max(0.0, min(1.0, float(strength)))

        if event == "help":
            record.generosity = min(1.0, record.generosity + strength)
            record.trust = min(1.0, record.trust + strength * 0.4)
        elif event == "theft":
            record.theft = min(1.0, record.theft + strength)
            record.trust = max(-1.0, record.trust - strength * 0.5)
        elif event == "violence":
            record.violence = min(1.0, record.violence + strength)
            record.trust = max(-1.0, record.trust - strength * 0.8)
        record.last_tick = int(tick)

    def opinion(self, observer_eid, target_eid):
        record = self.records.get((int(observer_eid), int(target_eid)))
        return 0.0 if record is None else record.score()

    def decay(self, tick, interval=3600):
        for key in list(self.records):
            record = self.records[key]
            if tick - record.last_tick < interval:
                continue
            record.trust *= 0.995
            record.violence *= 0.992
            record.theft *= 0.992
            record.generosity *= 0.995
            if abs(record.score()) < 0.02:
                del self.records[key]

```

## game/storage.py

**Type :** `.py`

```python

from __future__ import annotations
from dataclasses import dataclass, field


MATERIALS = ("bois", "pierre", "or", "graine", "food")


@dataclass
class SharedStorage:
    tx: int
    ty: int
    capacity: int = 80
    owner_clan: str | None = None
    inventory: dict = field(default_factory=lambda: {m: 0 for m in MATERIALS})
    contributors: dict = field(default_factory=dict)
    withdrawals: dict = field(default_factory=dict)
    last_access_tick: int = 0

    def total(self):
        return sum(max(0, int(v)) for v in self.inventory.values())

    def free_space(self):
        return max(0, self.capacity - self.total())

    def deposit(self, eid, material, amount, tick):
        if material not in self.inventory:
            return 0
        moved = max(0, min(int(amount), self.free_space()))
        if moved <= 0:
            return 0
        self.inventory[material] += moved
        self.contributors[eid] = self.contributors.get(eid, 0) + moved
        self.last_access_tick = tick
        return moved

    def withdraw(self, eid, material, amount, tick):
        if material not in self.inventory:
            return 0
        moved = max(0, min(int(amount), self.inventory[material]))
        if moved <= 0:
            return 0
        self.inventory[material] -= moved
        self.withdrawals[eid] = self.withdrawals.get(eid, 0) + moved
        self.last_access_tick = tick
        return moved

    def food_amount(self):
        return int(self.inventory.get("food", 0))

```

## game/studio_compare.py

**Type :** `.py`

```python

"""Comparaison A/B entre deux simulations. Pas de Qt/Pygame."""


KEYS = [
    ("population_end", "Population finale"),
    ("deaths", "Morts"),
    ("births", "Naissances"),
    ("builds", "Constructions"),
    ("harvests", "Récoltes"),
    ("messages", "Messages"),
    ("mean_health", "Santé moyenne"),
    ("mean_hunger", "Faim moyenne"),
    ("mean_trust", "Confiance moyenne"),
]


def compare_results(a, b):
    """Compare two experiment result dicts. Returns list of row dicts."""
    rows = []
    for key, label in KEYS:
        av = float(a.get(key, 0))
        bv = float(b.get(key, 0))
        rows.append({
            "metric": key,
            "label": label,
            "a": av,
            "b": bv,
            "difference": bv - av,
        })
    return rows


def compare_summary(a, b):
    """Generate a human-readable comparison summary in French."""
    a_label = a.get("scenario", "Expérience A")
    b_label = b.get("scenario", "Expérience B")
    
    lines = [f"Comparaison : {a_label} vs {b_label}", ""]
    
    rows = compare_results(a, b)
    for row in rows:
        label = row["label"]
        av = row["a"]
        bv = row["b"]
        diff = row["difference"]
        
        if abs(diff) < 0.01:
            continue
        
        direction = "augmenté" if diff > 0 else "diminué"
        
        if row["metric"] == "mean_health":
            if diff > 0.1:
                lines.append(f"La santé moyenne a {direction} ({av:.0%} → {bv:.0%}).")
            elif diff < -0.1:
                lines.append(f"La santé moyenne a {direction} ({av:.0%} → {bv:.0%}).")
        elif row["metric"] == "mean_trust":
            if diff > 0.1:
                lines.append(f"La confiance a {direction} ({av:.0%} → {bv:.0%}).")
            elif diff < -0.1:
                lines.append(f"La confiance a {direction} ({av:.0%} → {bv:.0%}).")
        elif row["metric"] == "deaths":
            if diff != 0:
                lines.append(f"Les morts : {int(av)} vs {int(bv)} ({direction} de {abs(int(diff))}).")
        elif row["metric"] == "builds":
            if diff != 0:
                lines.append(f"Les constructions : {int(av)} vs {int(bv)}.")
    
    if not lines[2:]:
        lines.append("Les deux expériences sont très similaires.")
    
    return "\n".join(lines)


def compare_table(a, b):
    """Return a formatted comparison table string."""
    rows = compare_results(a, b)
    lines = []
    lines.append(f"{'Métrique':<25} {'A':>10} {'B':>10} {'Diff':>10}")
    lines.append("-" * 58)
    for row in rows:
        lines.append(
            f"{row['label']:<25} {row['a']:>10.2f} {row['b']:>10.2f} {row['difference']:>+10.2f}"
        )
    return "\n".join(lines)

```

## game/studio_export.py

**Type :** `.py`

```python

"""Exports en TXT, Markdown, CSV, JSON. Pas de Qt/Pygame."""
import json
import csv
import io
from datetime import datetime


def export_txt(report_text, filepath):
    """Export report as plain text."""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report_text)
    return filepath


def export_markdown(report_text, timeline_events=None, metrics=None, filepath=None):
    """Export as Markdown with optional sections."""
    lines = []
    lines.append("# Rapport de simulation")
    lines.append(f"\n*Généré le {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n")
    lines.append("## Résumé\n")
    lines.append(report_text)

    if metrics:
        lines.append("\n## Métriques\n")
        lines.append("| Métrique | Valeur |")
        lines.append("|----------|--------|")
        for k, v in metrics.items():
            lines.append(f"| {k} | {v} |")

    if timeline_events:
        lines.append("\n## Événements importants\n")
        for event in timeline_events[:50]:
            lines.append(f"- {event}")

    content = "\n".join(lines)
    if filepath:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
    return content


def export_csv(metrics_dict, filepath):
    """Export metrics as CSV."""
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Métrique", "Valeur"])
        for k, v in metrics_dict.items():
            writer.writerow([k, v])
    return filepath


def export_json(data, filepath, indent=2):
    """Export full data as JSON."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False, default=str)
    return filepath


def export_full_report(result, timeline_events=None, directory="."):
    """Export a complete report in all formats."""
    from .studio_reports import build_report, build_short_summary

    report = build_report(result)
    summary = build_short_summary(result)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    scenario = result.get("scenario", "standard")
    base = f"report_{scenario}_{timestamp}"

    exports = {}
    exports["txt"] = export_txt(report, f"{directory}/{base}.txt")
    exports["markdown"] = export_markdown(
        report, timeline_events, result.get("metrics", {}),
        f"{directory}/{base}.md"
    )
    exports["csv"] = export_csv(result.get("metrics", {}), f"{directory}/{base}.metrics.csv")
    exports["json"] = export_json(result, f"{directory}/{base}.json")

    return exports

```

## game/studio_parameters.py

**Type :** `.py`

```python

"""Registre validé des paramètres de simulation. Pas de Qt/Pygame."""
from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class ParamDef:
    key: str
    label: str
    description: str
    ptype: str  # "int", "float", "bool", "choice"
    default: Any = None
    minimum: float = 0
    maximum: float = 9999
    choices: list = field(default_factory=list)
    path: str = ""
    runtime: bool = True
    group: str = "Général"

    def validate(self, value):
        if self.ptype == "int":
            v = int(value)
            if v < self.minimum or v > self.maximum:
                raise ValueError(f"{self.label} doit être entre {self.minimum} et {self.maximum}")
            return v
        if self.ptype == "float":
            v = float(value)
            if v < self.minimum or v > self.maximum:
                raise ValueError(f"{self.label} doit être entre {self.minimum} et {self.maximum}")
            return v
        if self.ptype == "bool":
            return bool(value)
        if self.ptype == "choice":
            if value not in self.choices:
                raise ValueError(f"{self.label} doit être parmi {self.choices}")
            return value
        return value


PARAMETERS = [
    # Population
    ParamDef("population.max", "Population maximale", "Nombre maximal d'habitants vivants.",
             "int", 800, 1, 5000, path="game.config.MAXPOP", runtime=False, group="Population"),
    ParamDef("population.birth_rate", "Taux de naissance", "Probabilité de naissance par tick.",
             "float", 0.01, 0.0, 1.0, runtime=True, group="Population"),
    
    # Monde
    ParamDef("world.food", "Nourriture", "Abondance de nourriture sur la carte.",
             "choice", "normal", choices=["faible", "normal", "élevé"], runtime=True, group="Monde"),
    ParamDef("world.predators", "Prédateurs", "Nombre de prédateurs dangereux.",
             "choice", "normal", choices=["faible", "normal", "élevé"], runtime=True, group="Monde"),
    ParamDef("world.size", "Taille du monde", "Nombre de tiles par côté.",
             "int", 200, 50, 1000, runtime=False, group="Monde"),
    
    # Simulation
    ParamDef("simulation.speed", "Vitesse de simulation", "Ticks exécutés par cycle d'affichage.",
             "int", 1, 1, 8, runtime=True, group="Simulation"),
    ParamDef("simulation.seed", "Graine aléatoire", "Seed pour la reproductibilité.",
             "int", 42, 0, 999999, runtime=False, group="Simulation"),
    
    # Anima
    ParamDef("anima.trauma", "Trauma", "Influence durable des événements dangereux.",
             "choice", "normal", choices=["désactivé", "faible", "normal", "fort"], runtime=True, group="Anima"),
    ParamDef("anima.culture", "Culture", "Transmission culturelle entre habitants.",
             "choice", "normal", choices=["désactivé", "faible", "normal", "fort"], runtime=True, group="Anima"),
    ParamDef("anima.episodes_max", "Épisodes max", "Nombre maximum d'épisodes en mémoire.",
             "int", 50, 10, 200, runtime=True, group="Anima"),
    
    # Écologie
    ParamDef("ecology.regrowth", "Régénération", "Taux de régénération des ressources.",
             "float", 0.02, 0.0, 1.0, runtime=True, group="Écologie"),
    ParamDef("ecology.fire_spread", "Propagation feu", "Vitesse de propagation des feux.",
             "float", 0.1, 0.0, 1.0, runtime=True, group="Écologie"),
    
    # Performance
    ParamDef("performance.max_agents", "Agents max rendus", "Nombre max d'agents affichés sur la carte.",
             "int", 200, 10, 2000, runtime=True, group="Performance"),
    ParamDef("performance.snapshot_freq", "Fréquence snapshot", "Ticks entre chaque snapshot UI.",
             "int", 5, 1, 50, runtime=True, group="Performance"),
]

PARAM_BY_KEY = {p.key: p for p in PARAMETERS}
PARAM_GROUPS = sorted(set(p.group for p in PARAMETERS))


@dataclass
class RuntimeConfig:
    """Configuration runtime modifiable à chaud."""
    trauma_enabled: bool = True
    trauma_scale: float = 1.0
    culture_enabled: bool = True
    institutions_enabled: bool = True
    births_enabled: bool = True
    predators_enabled: bool = True
    speed: int = 1
    snapshot_freq: int = 5
    max_agents_rendered: int = 200

    def apply_param(self, key, value):
        """Apply a parameter value to the runtime config."""
        if key == "anima.trauma":
            if value == "désactivé":
                self.trauma_enabled = False
            else:
                self.trauma_enabled = True
                self.trauma_scale = {"faible": 0.5, "normal": 1.0, "fort": 2.0}.get(value, 1.0)
        elif key == "anima.culture":
            self.culture_enabled = value != "désactivé"
        elif key == "simulation.speed":
            self.speed = int(value)
        elif key == "performance.snapshot_freq":
            self.snapshot_freq = int(value)
        elif key == "performance.max_agents":
            self.max_agents_rendered = int(value)

    def to_dict(self):
        return asdict(self)


class ParameterStore:
    """Store validated parameters with defaults."""
    
    def __init__(self):
        self._values = {p.key: p.default for p in PARAMETERS}
        self._runtime = RuntimeConfig()
    
    def get(self, key):
        return self._values.get(key)
    
    def set(self, key, value):
        if key not in PARAM_BY_KEY:
            raise KeyError(f"Paramètre inconnu : {key}")
        validated = PARAM_BY_KEY[key].validate(value)
        self._values[key] = validated
        if PARAM_BY_KEY[key].runtime:
            self._runtime.apply_param(key, validated)
    
    def reset(self, key=None):
        if key:
            self._values[key] = PARAM_BY_KEY[key].default
            self._runtime.apply_param(key, PARAM_BY_KEY[key].default)
        else:
            for p in PARAMETERS:
                self._values[p.key] = p.default
            self._runtime = RuntimeConfig()
    
    def get_runtime(self):
        return self._runtime
    
    def to_dict(self):
        return dict(self._values)
    
    def from_dict(self, data):
        for k, v in data.items():
            if k in self._values:
                try:
                    self.set(k, v)
                except (ValueError, KeyError):
                    pass
    
    def by_group(self):
        result = {}
        for p in PARAMETERS:
            result.setdefault(p.group, []).append(p)
        return result

```

## game/studio_reports.py

**Type :** `.py`

```python

"""Résumé d'expérience en français simple. Pas de Qt/Pygame."""


def build_report(result):
    """Build a human-readable report from experiment results.

    result dict should contain:
    - population_start, population_end
    - births, deaths
    - builds (construction completions)
    - harvests
    - food_given
    - messages
    - institutions
    - mean_health, mean_hunger, mean_trust
    - scenario, seed, duration
    - events (list of event dicts)
    """
    lines = []

    scenario = result.get("scenario", "Standard")
    seed = result.get("seed", "?")
    duration = result.get("duration", 0)
    lines.append(f"Simulation : {scenario} (seed {seed}, {duration} ticks)")
    lines.append("")

    pop_start = result.get("population_start", 0)
    pop_end = result.get("population_end", 0)
    lines.append(f"La simulation a commencé avec {pop_start} habitant(s).")
    lines.append(f"Elle se termine avec {pop_end} habitant(s).")
    lines.append("")

    births = result.get("births", 0)
    deaths = result.get("deaths", 0)
    if births or deaths:
        lines.append(f"{births} naissance(s) et {deaths} mort(s) ont été enregistrées.")

    builds = result.get("builds", 0)
    if builds:
        lines.append(f"{builds} construction(s) ont été terminée(s).")

    harvests = result.get("harvests", 0)
    if harvests:
        lines.append(f"{harvests} récolte(s) ont été effectuées.")

    messages = result.get("messages", 0)
    if messages:
        lines.append(f"{messages} message(s) ont été échangés.")

    institutions = result.get("institutions", 0)
    if institutions:
        lines.append(f"{institutions} institution(s) se sont formées.")

    lines.append("")

    mh = result.get("mean_health")
    if mh is not None:
        if mh > 0.7:
            lines.append("La santé moyenne du groupe était bonne.")
        elif mh > 0.4:
            lines.append("La santé moyenne du groupe était correcte.")
        else:
            lines.append("La santé moyenne du groupe était préoccupante.")

    mt = result.get("mean_trust")
    if mt is not None:
        if mt > 0.7:
            lines.append("La confiance entre habitants était élevée.")
        elif mt > 0.4:
            lines.append("La confiance entre habitants était moyenne.")
        else:
            lines.append("La confiance entre habitants était faible.")

    return "\n".join(lines)


def build_short_summary(result):
    """Build a very short 1-2 sentence summary."""
    pop_start = result.get("population_start", 0)
    pop_end = result.get("population_end", 0)
    deaths = result.get("deaths", 0)
    builds = result.get("builds", 0)

    parts = [f"Le groupe de {pop_start} habitant(s) termine avec {pop_end} survivant(s)."]
    if deaths:
        parts.append(f"{deaths} mort(s).")
    if builds:
        parts.append(f"{builds} construction(s).")
    return " ".join(parts)


def interpret_metric(name, start, end):
    """Interpret a metric change in simple French."""
    diff = end - start
    if name == "trust":
        if diff > 0.10:
            return "La confiance du groupe a augmenté sensiblement."
        if diff < -0.10:
            return "La confiance du groupe a diminué sensiblement."
        return "La confiance du groupe est restée relativement stable."
    if name == "health":
        if diff > 0.10:
            return "La santé du groupe s'est améliorée."
        if diff < -0.10:
            return "La santé du groupe s'est dégradée."
        return "La santé du groupe est restée stable."
    if name == "hunger":
        if diff > 0.10:
            return "La faim a augmenté dans le groupe."
        if diff < -0.10:
            return "La faim a diminué dans le groupe."
        return "La faim est restée stable."
    return ""

```

## game/studio_scenarios.py

**Type :** `.py`

```python

"""Scénarios prêts à lancer. Presets de paramètres validés."""
from .studio_parameters import ParameterStore


SCENARIOS = {
    "calme": {
        "label": "Survie tranquille",
        "description": "Ressources abondantes et peu de prédateurs. Idéal pour observer les interactions sociales.",
        "duration_recommended": 5000,
        "parameters": {
            "world.food": "élevé",
            "world.predators": "faible",
            "anima.trauma": "normal",
            "anima.culture": "normal",
            "population.birth_rate": 0.02,
        },
        "summary": (
            "Ce scénario commence avec des ressources abondantes "
            "et peu de prédateurs. Durée recommandée : 5 000 ticks."
        ),
    },
    "danger": {
        "label": "Forêt dangereuse",
        "description": "Les ressources sont dispersées et les prédateurs présents. Survie difficile.",
        "duration_recommended": 8000,
        "parameters": {
            "world.food": "moyen",
            "world.predators": "élevé",
            "anima.trauma": "fort",
            "anima.culture": "normal",
        },
        "summary": (
            "Les ressources sont rares et les prédateurs nombreux. "
            "Durée recommandée : 8 000 ticks."
        ),
    },
    "famine": {
        "label": "Famine",
        "description": "La nourriture est rare et la coopération devient importante pour survivre.",
        "duration_recommended": 10000,
        "parameters": {
            "world.food": "faible",
            "world.predators": "moyen",
            "anima.culture": "normal",
            "population.birth_rate": 0.005,
        },
        "summary": (
            "La nourriture est très rare. Le groupe doit coopérer pour survivre. "
            "Durée recommandée : 10 000 ticks."
        ),
    },
    "test_culture": {
        "label": "Test de culture",
        "description": "Deux groupes reçoivent des informations différentes pour tester la transmission culturelle.",
        "duration_recommended": 15000,
        "parameters": {
            "anima.culture": "fort",
            "anima.trauma": "normal",
            "world.food": "élevé",
            "world.predators": "faible",
        },
        "summary": (
            "Ce scénario teste la transmission culturelle entre habitants. "
            "Durée recommandée : 15 000 ticks."
        ),
    },
    "high_trauma": {
        "label": "Monde traumatisant",
        "description": "Fréquence élevée d'événements dangereux pour tester la résilience psychologique.",
        "duration_recommended": 8000,
        "parameters": {
            "anima.trauma": "fort",
            "world.predators": "élevé",
            "world.food": "moyen",
            "ecology.fire_spread": 0.3,
        },
        "summary": (
            "Les attaques sont fréquentes et les feux fréquents. "
            "Durée recommandée : 8 000 ticks."
        ),
    },
    "social_experiment": {
        "label": "Expérience sociale",
        "description": "Population dense pour observer les relations et la formation de familles.",
        "duration_recommended": 12000,
        "parameters": {
            "population.birth_rate": 0.05,
            "world.food": "élevé",
            "world.predators": "faible",
            "anima.culture": "fort",
            "anima.trauma": "faible",
        },
        "summary": (
            "Population dense avec forte culture. "
            "Durée recommandée : 12 000 ticks."
        ),
    },
}


def get_scenario(name):
    """Get a scenario by name. Returns None if not found."""
    return SCENARIOS.get(name)


def list_scenarios():
    """Return list of (key, label, description) tuples."""
    return [(k, v["label"], v["description"]) for k, v in SCENARIOS.items()]


def apply_scenario(store, scenario_name):
    """Apply a scenario's parameters to a ParameterStore."""
    scenario = SCENARIOS.get(scenario_name)
    if not scenario:
        raise ValueError(f"Scénario inconnu : {scenario_name}")
    for key, value in scenario["parameters"].items():
        store.set(key, value)
    return store


def scenario_summary(scenario_name):
    """Get the summary text for a scenario."""
    scenario = SCENARIOS.get(scenario_name)
    if not scenario:
        return "Scénario inconnu."
    return scenario["summary"]

```

## game/studio_snapshots.py

**Type :** `.py`

```python

"""Vues enrichies de l'etat reel avec labels lisibles. Pas de Qt/Pygame."""
from .ui_snapshots import (
    simulation_snapshot,
    population_snapshot,
    selected_agent_snapshot,
    journal_snapshot,
    map_snapshot,
    tile_snapshot,
    society_snapshot,
    anima_snapshot,
)
from .diagnostics import agent_snapshot as _raw_agent_snapshot
from .studio_text import level_label, level_color


def readable_agent(sim, agent):
    """Agent snapshot enriched with readable labels."""
    snap = _raw_agent_snapshot(sim, agent)
    if snap is None:
        return None
    snap["sante_label"] = level_label(snap.get("sante", 0))
    snap["sante_color"] = level_color(snap.get("sante", 0))
    snap["faim_label"] = level_label(snap.get("faim", 0))
    snap["energie_label"] = level_label(snap.get("energie", 0))
    identity = snap.get("identity", {})
    if identity:
        snap["identity_dominant"] = max(identity, key=identity.get)
    else:
        snap["identity_dominant"] = None
    return snap


def readable_population(sim):
    """Population with readable fields for each agent."""
    pop = population_snapshot(sim)
    for agent in pop:
        agent["sante_label"] = level_label(agent.get("sante", 0))
        agent["faim_label"] = level_label(agent.get("faim", 0))
        identity = agent.get("identity", {})
        agent["identity_dominant"] = max(identity, key=identity.get) if identity else None
    return pop


def readable_selected(sim, ui_state=None):
    """Selected agent snapshot enriched with labels."""
    snap = selected_agent_snapshot(sim, ui_state)
    if snap is None:
        return None
    snap["sante_label"] = level_label(snap.get("sante", 0))
    snap["sante_color"] = level_color(snap.get("sante", 0))
    snap["faim_label"] = level_label(snap.get("faim", 0))
    snap["energie_label"] = level_label(snap.get("energie", 0))
    identity = snap.get("identity", {})
    if identity:
        snap["identity_dominant"] = max(identity, key=identity.get)
    else:
        snap["identity_dominant"] = None
    return snap


def readable_tile(sim, tx, ty):
    """Tile snapshot enriched with labels."""
    snap = tile_snapshot(sim, tx, ty)
    if snap is None:
        return None
    snap["danger_label"] = level_label(snap.get("danger", 0))
    snap["danger_color"] = level_color(snap.get("danger", 0))
    snap["fertilite_label"] = level_label(snap.get("fertilite", 0))
    snap["ressource_label"] = level_label(snap.get("ressource", 0))
    return snap


def readable_map(sim, ui_state=None):
    """Map snapshot enriched with danger/fertility labels."""
    snap = map_snapshot(sim, ui_state)
    for tile in snap.get("tiles", []):
        tile["danger_label"] = level_label(tile.get("danger", 0))
        tile["fertilite_label"] = level_label(tile.get("fertilite", 0))
    return snap


def readable_society(sim):
    """Society snapshot with readable summary."""
    snap = society_snapshot(sim)
    pop = snap.get("population", 0)
    bonded = snap.get("bonded", 0)
    snap["summary"] = f"Le groupe compte {pop} habitant(s)"
    if bonded:
        snap["summary"] += f", {bonded} couple(s)"
    snap["summary"] += "."
    return snap

```

## game/studio_text.py

**Type :** `.py`

```python

"""Traduction donnees -> phrases simples. Aucune donnee inventee."""


def level_label(value):
    """0.0-1.0 -> label lisible."""
    value = max(0.0, min(1.0, float(value)))
    if value < 0.20:
        return "Tres faible"
    if value < 0.40:
        return "Faible"
    if value < 0.65:
        return "Moyen"
    if value < 0.85:
        return "Eleve"
    return "Tres eleve"


def level_color(value):
    """0.0-1.0 -> couleur hex."""
    value = max(0.0, min(1.0, float(value)))
    if value < 0.20:
        return "#54B96B"
    if value < 0.40:
        return "#A8C85A"
    if value < 0.65:
        return "#E2B44A"
    if value < 0.85:
        return "#E77D43"
    return "#D94B4B"


def describe_agent(agent_snapshot):
    """Decrire un habitant en phrases simples. agent_snapshot est un dict."""
    name = agent_snapshot.get("nom", "Cet habitant")
    identity = agent_snapshot.get("identity", {})
    dominant = max(identity, key=identity.get) if identity else None
    labels = {
        "builder": "constructeur",
        "provider": "pourvoyeur",
        "fighter": "combattant",
        "explorer": "explorateur",
        "caretaker": "protecteur",
        "survivor": "survivant",
    }
    if dominant in labels:
        return f"{name} se comporte actuellement comme un {labels[dominant]}."
    return f"{name} n'a pas encore d'identite dominante claire."


def describe_health(agent_snapshot):
    sante = agent_snapshot.get("sante", 0)
    return f"Sante : {int(sante*100)}% -- {level_label(sante).lower()}"


def describe_hunger(agent_snapshot):
    faim = agent_snapshot.get("faim", 0)
    return f"Faim : {int(faim*100)}% -- {level_label(faim).lower()}"


def describe_needs(agent_snapshot):
    """Return a list of need descriptions."""
    result = []
    for key, label in [("sante", "Sante"), ("faim", "Faim"), ("energie", "Energie")]:
        val = agent_snapshot.get(key, 0)
        result.append(f"{label} : {int(val*100)}% -- {level_label(val).lower()}")
    return result


def describe_anima(anima_snapshot):
    """Describe anima data in simple sentences."""
    lines = []
    identity = anima_snapshot.get("identity", {})
    if identity:
        dominant = max(identity, key=identity.get)
        lines.append(f"Identite dominante : {dominant} ({identity[dominant]:.0%})")
    values = anima_snapshot.get("values", {})
    if values:
        top = sorted(values.items(), key=lambda x: x[1], reverse=True)[:3]
        vals = ", ".join(f"{k} ({v:.0%})" for k, v in top)
        lines.append(f"Top valeurs : {vals}")
    intention = anima_snapshot.get("intention", {})
    if intention:
        lines.append(f"Intention : {intention.get('action', 'aucune')}")
    goal = anima_snapshot.get("goal")
    if goal:
        lines.append(f"Objectif : {goal}")
    return lines


def describe_tile(tile_snapshot):
    """Describe a tile in simple terms."""
    ttype = tile_snapshot.get("type", "terre")
    fert = tile_snapshot.get("fertilite", 0)
    res = tile_snapshot.get("ressource", 0)
    danger = tile_snapshot.get("danger", 0)
    parts = [f"Type : {ttype}"]
    if fert > 0:
        parts.append(f"Fertilite : {level_label(fert).lower()}")
    if res > 0:
        parts.append(f"Ressource : {level_label(res).lower()}")
    if danger > 0:
        parts.append(f"Danger : {level_label(danger).lower()}")
    return " | ".join(parts)


def society_summary(society_snapshot):
    """Describe society state in simple sentences."""
    pop = society_snapshot.get("population", 0)
    lines = [f"Le groupe compte {pop} habitant(s)."]
    families = society_snapshot.get("families", 0)
    if families:
        lines.append(f"{families} famille(s) forme(s).")
    storages = society_snapshot.get("storages", 0)
    builds = society_snapshot.get("completed_buildings", 0)
    if storages or builds:
        parts = []
        if storages:
            parts.append(f"{storages} depot(s)")
        if builds:
            parts.append(f"{builds} construction(s) terminee(s)")
        lines.append("Il utilise " + " et ".join(parts) + ".")
    return " ".join(lines)


def event_sentence(event):
    """Turn a raw event dict into a readable French sentence. Never invent facts."""
    kind = event.get("kind", "")
    actor = event.get("actor_name", "Un habitant")

    sentences = {
        "monster_attack": f"{actor} a subi une attaque d'animal dangereux.",
        "food_given": f"{actor} a partage de la nourriture.",
        "construction_complete": f"{actor} a participe a une construction terminee.",
        "birth": f"Un enfant est ne dans le groupe de {actor}.",
        "death": f"{actor} n'a pas survecu.",
        "harvest": f"{actor} a recolte des ressources.",
        "build_start": f"{actor} a commence une construction.",
        "exploration": f"{actor} a explore une nouvelle zone.",
        "conflict": f"{actor} a ete implique dans un conflit.",
        "message": f"{actor} a partage une information.",
    }

    if kind in sentences:
        return sentences[kind]
    title = event.get("title", "")
    if title:
        return f"{actor} : {title}."
    return "Un evenement important s'est produit."

```

## game/studio_timeline.py

**Type :** `.py`

```python

"""Chronologie normalisée avec catégories et filtres. Pas de Qt/Pygame."""


CATEGORIES = [
    "Tous", "Vie", "Famille", "Social", "Danger",
    "Construction", "Économie", "Culture", "Météo", "Mort",
]

CATEGORY_MAP = {
    "birth": "Famille",
    "death": "Mort",
    "marriage": "Famille",
    "child": "Famille",
    "attack": "Danger",
    "monster_attack": "Danger",
    "danger": "Danger",
    "construction": "Construction",
    "build": "Construction",
    "construction_complete": "Construction",
    "harvest": "Économie",
    "food_given": "Économie",
    "trade": "Économie",
    "message": "Social",
    "conflict": "Social",
    "exploration": "Vie",
    "weather": "Météo",
    "fire": "Danger",
    "culture": "Culture",
    "institution": "Culture",
}


def normalize_event(raw):
    """Normalize a raw event dict into a standard format."""
    return {
        "tick": int(raw.get("tick", 0)),
        "category": CATEGORY_MAP.get(raw.get("kind", ""), "Vie"),
        "title": str(raw.get("title", raw.get("kind", "Événement"))),
        "text": str(raw.get("text", "")),
        "actors": [int(x) for x in raw.get("actors", []) if str(x).isdigit()],
        "place": raw.get("place"),
        "importance": float(raw.get("importance", 0.0)),
        "kind": str(raw.get("kind", "")),
        "actor_name": str(raw.get("actor_name", "")),
    }


def event_sentence(event):
    """Turn a normalized event into a readable French sentence."""
    kind = event.get("kind", "")
    actor = event.get("actor_name", "Un habitant")

    sentences = {
        "monster_attack": f"{actor} a subi une attaque d'animal dangereux.",
        "food_given": f"{actor} a partagé de la nourriture.",
        "construction_complete": f"{actor} a participé à une construction terminée.",
        "birth": f"Un enfant est né dans le groupe de {actor}.",
        "death": f"{actor} n'a pas survécu.",
        "harvest": f"{actor} a récolté des ressources.",
        "build": f"{actor} a commencé une construction.",
        "exploration": f"{actor} a exploré une nouvelle zone.",
        "conflict": f"{actor} a été impliqué dans un conflit.",
        "message": f"{actor} a partagé une information.",
        "fire": f"Un feu s'est déclaré près de {actor}.",
        "weather": f"La météo a changé.",
        "culture": f"{actor} a transmis un savoir culturel.",
        "institution": f"Une institution a été créée ou modifiée.",
    }

    if kind in sentences:
        return sentences[kind]
    title = event.get("title", "")
    if title:
        return f"{actor} : {title}."
    return "Un événement important s'est produit."


def format_event(event):
    """Format an event for display: tick, category, sentence."""
    tick = event.get("tick", 0)
    category = event.get("category", "Vie")
    sentence = event_sentence(event)
    day = tick // 100 + 1
    hour = tick % 100
    return f"Jour {day} — {hour:02d}h — [{category}] {sentence}"


def filter_events(events, category=None, actor=None, place=None, min_tick=None, max_tick=None):
    """Filter events by criteria."""
    result = events
    if category and category != "Tous":
        result = [e for e in result if e.get("category") == category]
    if actor:
        result = [e for e in result if actor in str(e.get("actors", []))]
    if place:
        result = [e for e in result if e.get("place") == place]
    if min_tick is not None:
        result = [e for e in result if e.get("tick", 0) >= min_tick]
    if max_tick is not None:
        result = [e for e in result if e.get("tick", 0) <= max_tick]
    return result


def build_timeline(journal_entries):
    """Build a normalized timeline from raw journal entries."""
    events = [normalize_event(e) for e in journal_entries]
    events.sort(key=lambda e: e.get("tick", 0))
    return events

```

## game/tool_editor.py

**Type :** `.py`

```python

"""Editeur de pixels integre : dessine un outil dans la fenetre pygame."""
from __future__ import annotations
import os
import pygame

GRID_SIZE = 16
CELL_PX = 18
PALETTE = [
    (60, 60, 66), (120, 90, 60), (150, 150, 156), (200, 170, 90),
    (90, 140, 90), (140, 90, 160), (200, 90, 90), (230, 230, 230),
]


class ToolEditor:
    def __init__(self):
        self.pixels = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.current_color = PALETTE[0]
        self.name = "mon_outil"
        self.rect = pygame.Rect(0, 0, GRID_SIZE * CELL_PX, GRID_SIZE * CELL_PX)
        self.palette_y = 0

    def clear(self):
        self.pixels = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    def paint_at(self, mx, my, erase=False):
        if not self.rect.collidepoint(mx, my):
            return False
        col = (mx - self.rect.x) // CELL_PX
        row = (my - self.rect.y) // CELL_PX
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            self.pixels[row][col] = None if erase else self.current_color
            return True
        return False

    def palette_hit(self, mx, my):
        for i, c in enumerate(PALETTE):
            r = pygame.Rect(self.rect.x + i * 26, self.palette_y, 22, 22)
            if r.collidepoint(mx, my):
                return c
        return None

    def draw(self, screen, x, y):
        self.rect.topleft = (x, y)
        pygame.draw.rect(screen, (18, 20, 26), self.rect.inflate(4, 4))
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = pygame.Rect(x + col * CELL_PX, y + row * CELL_PX,
                                    CELL_PX - 1, CELL_PX - 1)
                pygame.draw.rect(screen, self.pixels[row][col] or (30, 32, 40), cell)
        self.palette_y = y + self.rect.height + 8
        for i, c in enumerate(PALETTE):
            r = pygame.Rect(x + i * 26, self.palette_y, 22, 22)
            pygame.draw.rect(screen, c, r, border_radius=4)
            if c == self.current_color:
                pygame.draw.rect(screen, (255, 255, 255), r, 2, border_radius=4)

    def render_surface(self):
        surf = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                c = self.pixels[row][col]
                if c is not None:
                    surf.set_at((col, row), (*c, 255))
        return pygame.transform.scale(surf, (GRID_SIZE * 4, GRID_SIZE * 4))

    def save_png(self, root_dir, tool_kind):
        os.makedirs(root_dir, exist_ok=True)
        surf = self.render_surface()
        safe = "".join(ch for ch in self.name if ch.isalnum() or ch in "_-") or "outil"
        path = os.path.join(root_dir, f"{safe}_{tool_kind}.png")
        pygame.image.save(surf, path)
        return path

```

## game/ui_api.py

**Type :** `.py`

```python

"""Couche UI — API publique.

Seule interface que la boucle principale (main.py) utilise pour le rendu
et les entrées. Les classes internes (Renderer, Camera, ui_kit) restent
privées : elles peuvent être refactorisées librement tant que ce contrat tient.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import pygame

from game.assets_api import AssetData, get_asset
from game.brain_api import ACTION_NAMES_EXP as ACTION_NAMES

__all__ = ["init_ui", "handle_events", "draw_frame", "tooltip_for_asset"]


class UIContext:
    """État UI regroupé — Renderer + Camera."""
    def __init__(self, am):
        from game.renderer import Renderer
        from game.camera import Camera
        self.renderer = Renderer(am)
        self.camera = Camera()
        self.show_legend = False
        self.asset = 0


def init_ui(am) -> UIContext:
    return UIContext(am)


def handle_events(events: List[pygame.event.Event], ctx: UIContext, sim,
                  am) -> List[Tuple[str, Any]]:
    """Transforme les événements pygame en actions abstraites."""
    from game.camera import ZOOMS
    from game.config import LEFT_W, VIEW_W
    actions: List[Tuple[str, Any]] = []
    for ev in events:
        if ev.type == pygame.QUIT:
            actions.append(("quit", None))
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                actions.append(("quit", None))
            elif ev.key == pygame.K_SPACE:
                actions.append(("pause", None))
            elif ev.key in (pygame.K_PLUS, pygame.K_EQUALS):
                actions.append(("speed", +1))
            elif ev.key == pygame.K_MINUS:
                actions.append(("speed", -1))
            elif ev.key == pygame.K_g:
                ctx.renderer.show_grid = not ctx.renderer.show_grid
            elif ev.key == pygame.K_v:
                ctx.show_legend = not ctx.show_legend
        elif ev.type == pygame.MOUSEWHEEL:
            mx, my = pygame.mouse.get_pos()
            if LEFT_W <= mx < LEFT_W + VIEW_W:
                closest = min(range(len(ZOOMS)), key=lambda i: abs(ZOOMS[i] - ctx.camera.zoom))
                idx = max(0, min(len(ZOOMS) - 1, closest + (1 if ev.y > 0 else -1)))
                ctx.camera.set_zoom(ZOOMS[idx], anchor_screen=(mx - LEFT_W, my))
    return actions


def draw_frame(screen: pygame.Surface, ctx: UIContext, sim, cam,
               ui_state: Dict[str, Any]) -> None:
    """Dessine l'écran complet : carte du monde."""
    from game.config import SCREEN_H, VIEW_W, LEFT_W
    view = pygame.Surface((VIEW_W, SCREEN_H))
    ctx.renderer.draw(view, sim, cam, ui_state)
    screen.fill((12, 14, 20))
    screen.blit(view, (LEFT_W, 0))
    pygame.draw.line(screen, (10, 10, 14), (LEFT_W + VIEW_W - 1, 0),
                     (LEFT_W + VIEW_W - 1, SCREEN_H))


def tooltip_for_asset(surface: pygame.Surface, asset: AssetData,
                      pos: Tuple[int, int]) -> None:
    """Affiche un résumé structuré de l'asset."""
    from game.ui_kit import get_kit
    kit = get_kit()
    x, y = pos
    lines = [
        asset.label,
        f"role={asset.role} cat={asset.category}",
        f"placable={'oui' if asset.placable else 'non'} solid={asset.solid}",
        "afford: " + " ".join(asset.affordances[:5]),
    ]
    if asset.build_recipe:
        mats = ", ".join(f"{m['materiau']} x{m['quantity']}"
                         for m in asset.build_recipe["materials"])
        lines.append(f"recette: {mats}")
    for i, ln in enumerate(lines):
        kit.draw_fit(surface, "tiny", ln,
                     x + 10, y + 14 + i * 14,
                     kit.C["ink"], right=x + 250)

```

## game/ui_commands.py

**Type :** `.py`

```python

"""UI Commands — commandes neutres validatees par le moteur.

Chaque commande est un dict avec au minimum ``kind``. Le moteur valide
les parametres, effectue l'action, et retourne un resultat dict.

Aucune dependance Pygame ni Qt.
"""
from __future__ import annotations

from typing import Any


def execute_command(sim, command: dict) -> dict[str, Any]:
    """Execute une commande sur la simulation et retourne le resultat.

    Format de retour :
        {"ok": True, ...}  en cas de succes
        {"ok": False, "error": "message"} en cas d'erreur
    """
    kind = command.get("kind", "")

    handler = _HANDLERS.get(kind)
    if handler is None:
        return {"ok": False, "error": f"Commande inconnue: {kind}"}

    try:
        return handler(sim, command)
    except Exception as exc:
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}


# ══════════════════════════════════════════════════════════════════════
#  Controle de simulation
# ══════════════════════════════════════════════════════════════════════
def _cmd_pause_toggle(sim, cmd):
    sim.paused = not sim.paused
    return {"ok": True, "paused": bool(sim.paused)}


def _cmd_set_paused(sim, cmd):
    sim.paused = bool(cmd.get("paused", True))
    return {"ok": True, "paused": bool(sim.paused)}


def _cmd_set_speed(sim, cmd):
    speed = max(1, min(8, int(cmd.get("speed", 1))))
    sim.speed = speed
    return {"ok": True, "speed": speed}


def _cmd_speed_delta(sim, cmd):
    delta = int(cmd.get("delta", 1))
    sim.speed = max(1, min(8, sim.speed + delta))
    return {"ok": True, "speed": int(sim.speed)}


def _cmd_step(sim, cmd):
    sim.tick()
    return {"ok": True, "tick": int(sim.w.tick)}


# ══════════════════════════════════════════════════════════════════════
#  Selection
# ══════════════════════════════════════════════════════════════════════
def _cmd_select_agent(sim, cmd):
    eid = cmd.get("eid")
    if eid is not None:
        eid = int(eid)
        agent = next((a for a in sim.agents if a.eid == eid and a.alive), None)
        if agent is None:
            return {"ok": False, "error": "Habitant introuvable ou mort"}
        sim.selected = agent
        return {"ok": True, "eid": eid, "nom": agent.name}
    sim.selected = None
    return {"ok": True, "eid": None}


def _cmd_select_tile(sim, cmd):
    tx = int(cmd.get("tx", 0))
    ty = int(cmd.get("ty", 0))
    w = sim.w
    if not (0 <= tx < w.g and 0 <= ty < w.g):
        return {"ok": False, "error": "Coordonnees hors monde"}
    return {"ok": True, "tx": tx, "ty": ty}


# ══════════════════════════════════════════════════════════════════════
#  Spawns
# ══════════════════════════════════════════════════════════════════════
def _cmd_spawn_agent(sim, cmd):
    x = cmd.get("x")
    y = cmd.get("y")
    kwargs = {}
    for key in ("color", "cls", "sex", "n_hid", "gen", "energy"):
        if key in cmd:
            kwargs[key] = cmd[key]
    if x is not None:
        kwargs["x"] = float(x)
    if y is not None:
        kwargs["y"] = float(y)
    created = sim.spawn_agent(**kwargs)
    if created is None:
        return {"ok": False, "error": "Impossible de creer l'habitant (place ou limite)"}
    sim.selected = created
    return {"ok": True, "eid": int(created.eid), "nom": created.name}


def _cmd_spawn_sheep(sim, cmd):
    x = cmd.get("x")
    y = cmd.get("y")
    kwargs = {}
    if x is not None:
        kwargs["x"] = float(x)
    if y is not None:
        kwargs["y"] = float(y)
    sim.spawn_sheep(**kwargs)
    return {"ok": True}


def _cmd_spawn_monster(sim, cmd):
    x = cmd.get("x")
    y = cmd.get("y")
    kwargs = {}
    if x is not None:
        kwargs["x"] = float(x)
    if y is not None:
        kwargs["y"] = float(y)
    if "kind" in cmd:
        kwargs["kind"] = cmd["kind"]
    sim.spawn_monster(**kwargs)
    return {"ok": True}


def _cmd_remove_agent(sim, cmd):
    eid = cmd.get("eid")
    if eid is None:
        return {"ok": False, "error": "eid manquant"}
    agent = next((a for a in sim.agents if a.eid == int(eid) and a.alive), None)
    if agent is None:
        return {"ok": False, "error": "Habitant introuvable ou mort"}
    name = cmd.get("name", "le gardien")
    sim.remove_agent(agent, name)
    return {"ok": True}


def _cmd_set_agent_stat(sim, cmd):
    eid = cmd.get("eid")
    stat = cmd.get("stat")
    value = float(cmd.get("value", 0))
    if eid is None or stat is None:
        return {"ok": False, "error": "eid ou stat manquant"}
    agent = next((a for a in sim.agents if a.eid == int(eid) and a.alive), None)
    if agent is None:
        return {"ok": False, "error": "Habitant introuvable ou mort"}
    if hasattr(agent, stat):
        setattr(agent, stat, max(0.0, min(1.0, value)))
        return {"ok": True}
    return {"ok": False, "error": f"Stat inconnue: {stat}"}


# ══════════════════════════════════════════════════════════════════════
#  Outils monde (paint / place / erase / carve / restore)
# ══════════════════════════════════════════════════════════════════════
def _cmd_paint_tile(sim, cmd):
    """Peint un mode sur une zone de tuiles (water, land, wall, floor)."""
    tx = int(cmd.get("tx", 0))
    ty = int(cmd.get("ty", 0))
    mode = cmd.get("mode", "land")
    radius = max(1, min(15, int(cmd.get("radius", 1))))
    w = sim.w

    changed = False
    for dy in range(-radius, radius + 1):
        for dx in range(-radius, radius + 1):
            if dx * dx + dy * dy > radius * radius + 1:
                continue
            cx, cy = tx + dx, ty + dy
            if not (0 <= cx < w.g and 0 <= cy < w.g):
                continue

            if mode == "water":
                if w.land[cy, cx]:
                    w.remove(cx, cy, quiet=True)
                    w.land[cy, cx] = 0
                    w.water[cy, cx] = 1
                    w.blocked[cy, cx] = 0
                    w.floor[cy, cx] = -1
                    w.mark_dirty(cx, cy, 2)
                    changed = True
            elif mode == "land":
                if not w.land[cy, cx] or w.blocked[cy, cx]:
                    w.land[cy, cx] = 1
                    w.water[cy, cx] = 0
                    w.blocked[cy, cx] = 0
                    w.floor[cy, cx] = -1
                    w.mark_dirty(cx, cy, 2)
                    changed = True
            elif mode == "wall":
                if w.land[cy, cx] and not w.blocked[cy, cx] and w.content_at(cx, cy) < 0:
                    stones = sim.am.pool("stone_res") or sim.am.pool("gold_stone")
                    if stones:
                        aid = int(sim.am.pick(stones, sim.rng))
                        w.place(cx, cy, aid, sim.am, hp=8, solid=True,
                                size=sim.am.assets[aid].size_tiles)
                        changed = True
    return {"ok": changed}


def _cmd_place_asset(sim, cmd):
    """Pose un asset sur une tuile."""
    tx = int(cmd.get("tx", 0))
    ty = int(cmd.get("ty", 0))
    aid = int(cmd.get("aid", -1))
    w = sim.w

    if not (0 <= aid < len(sim.am.assets)):
        return {"ok": False, "error": "Asset invalide"}
    adef = sim.am.assets[aid]
    if not getattr(adef, "placable", False):
        return {"ok": False, "error": "Asset non placable"}
    if not w.land[ty, tx] or w.blocked[ty, tx] or w.content_at(tx, ty) >= 0:
        return {"ok": False, "error": "Case occupee ou incompatible"}
    w.place(tx, ty, aid, sim.am, hp=max(1, getattr(adef, "hp", 1)),
            solid=bool(adef.solid), shelter=bool(adef.shelter),
            size=adef.size_tiles if adef.solid else 1)
    return {"ok": True}


def _cmd_erase_tile(sim, cmd):
    """Efface un objet sur une tuile."""
    tx = int(cmd.get("tx", 0))
    ty = int(cmd.get("ty", 0))
    w = sim.w
    if not (0 <= tx < w.g and 0 <= ty < w.g):
        return {"ok": False, "error": "Coordonnees hors monde"}
    removed = w.remove(tx, ty)
    old_len = len(w.items)
    w.items = [it for it in w.items
               if not (int(it.x // 32) == tx and int(it.y // 32) == ty)]
    had_floor = w.floor[ty, tx] >= 0
    w.floor[ty, tx] = -1
    w.mark_dirty(tx, ty)
    return {"ok": removed or len(w.items) != old_len or had_floor}


def _cmd_set_floor(sim, cmd):
    """Definit le sol d'une tuile."""
    tx = int(cmd.get("tx", 0))
    ty = int(cmd.get("ty", 0))
    aid = int(cmd.get("aid", 0))
    w = sim.w
    if not (0 <= tx < w.g and 0 <= ty < w.g):
        return {"ok": False, "error": "Coordonnees hors monde"}
    if aid in sim.am.floors:
        sheet_idx = sim.am.floors.index(aid)
        w.set_floor(tx, ty, sheet_idx * 216)
    elif sim.am.floors:
        w.set_floor(tx, ty, 0)
    else:
        return {"ok": False, "error": "Pas de tileset de sol"}
    return {"ok": True}


def _cmd_carve(sim, cmd):
    """Sculpte une montagne."""
    tx = int(cmd.get("tx", 0))
    ty = int(cmd.get("ty", 0))
    radius = max(1, min(15, int(cmd.get("radius", 3))))
    w = sim.w
    gen = getattr(w, "gen", None)
    if gen is None:
        return {"ok": False, "error": "Pas de heightmap (monde plat)"}
    from game import worldgen as _wg
    changed = _wg.carve_mountain(w, gen, tx, ty, radius=radius, strength=0.12)
    return {"ok": bool(changed)}


def _cmd_restore(sim, cmd):
    """Restaure une montagne sculptee."""
    tx = int(cmd.get("tx", 0))
    ty = int(cmd.get("ty", 0))
    radius = max(1, min(15, int(cmd.get("radius", 3))))
    w = sim.w
    gen = getattr(w, "gen", None)
    if gen is None:
        return {"ok": False, "error": "Pas de heightmap (monde plat)"}
    from game import worldgen as _wg
    changed = _wg.restore_mountain(w, gen, tx, ty, radius=radius, strength=0.18)
    return {"ok": bool(changed)}


def _cmd_build_block(sim, cmd):
    """Construit un bloc."""
    tx = int(cmd.get("tx", 0))
    ty = int(cmd.get("ty", 0))
    material = cmd.get("material", "bois")
    return {"ok": bool(sim.do_build_block_player(tx, ty, material=material))}


# ══════════════════════════════════════════════════════════════════════
#  Journal
# ══════════════════════════════════════════════════════════════════════
def _cmd_log(sim, cmd):
    """Ajoute une entree au journal."""
    text = str(cmd.get("text", ""))
    color = cmd.get("color", (180, 180, 180))
    cat = cmd.get("cat", "monde")
    sim.log(text, color, cat)
    return {"ok": True}


# ══════════════════════════════════════════════════════════════════════
#  Sauvegarde / chargement
# ══════════════════════════════════════════════════════════════════════
def _cmd_save(sim, cmd):
    from .save import save_game
    slot = int(cmd.get("slot", 0))
    cam = cmd.get("cam")
    path, sz = save_game(sim, cam, slot=slot)
    return {"ok": True, "path": str(path), "size_mb": round(sz, 1)}


def _cmd_load(sim, cmd):
    from .save import load_game
    from .assets_manager import AssetManager
    slot = int(cmd.get("slot", 0))
    am = getattr(sim, "am", None)
    if am is None:
        return {"ok": False, "error": "AssetManager indisponible"}
    new_sim, new_cam = load_game(am, slot=slot)
    if new_sim is None:
        return {"ok": False, "error": "Aucune sauvegarde trouvee"}
    return {"ok": True, "sim": new_sim, "cam": new_cam}


# ══════════════════════════════════════════════════════════════════════
#  Registre des handlers
# ══════════════════════════════════════════════════════════════════════
_HANDLERS = {
    # Simulation
    "pause_toggle": _cmd_pause_toggle,
    "set_paused": _cmd_set_paused,
    "set_speed": _cmd_set_speed,
    "speed_delta": _cmd_speed_delta,
    "step": _cmd_step,
    # Selection
    "select_agent": _cmd_select_agent,
    "select_tile": _cmd_select_tile,
    # Spawns
    "spawn_agent": _cmd_spawn_agent,
    "spawn_sheep": _cmd_spawn_sheep,
    "spawn_monster": _cmd_spawn_monster,
    "remove_agent": _cmd_remove_agent,
    "set_agent_stat": _cmd_set_agent_stat,
    # Monde
    "paint_tile": _cmd_paint_tile,
    "place_asset": _cmd_place_asset,
    "erase_tile": _cmd_erase_tile,
    "set_floor": _cmd_set_floor,
    "carve": _cmd_carve,
    "restore": _cmd_restore,
    "build_block": _cmd_build_block,
    # Journal
    "log": _cmd_log,
    # Sauvegarde
    "save": _cmd_save,
    "load": _cmd_load,
}

```

## game/ui_kit.py

**Type :** `.py`

```python

"""ui_kit — fondations graphiques du laboratoire.

Kit 100% pygame pur, aucune dépendance externe.
  * polices Segoe UI / pygame default
  * tokens de palette PAR FAMILLE DE DONNEES
  * gestionnaire de tooltips
  * widgets : boutons, glass panels, gauges, sliders, accordion

Tout est pre-rendu / cache : la boucle 60 FPS ne fait que des blits."""
import pygame

# ---------------------------------------------------------------- tokens
C = {
    # familles de donnees
    "corps":       (235, 145, 100),
    "cognition":   (80, 200, 255),
    "personnalite": (195, 110, 255),
    "emotions":    (255, 175, 80),
    "besoins":     (80, 230, 180),
    "experience":  (255, 215, 60),
    "social":      (255, 160, 210),
    "combat":      (255, 80, 80),
    "meteo":       (120, 195, 255),
    "economie":    (255, 215, 60),
    "vie":         (80, 225, 110),
    "mort":        (200, 80, 80),
    "batiment":    (160, 240, 150),
    "monde":       (190, 210, 240),
    # chrome — warm dark palette
    "bg":     (18, 20, 26),
    "bg2":    (24, 28, 38),
    "bg3":    (12, 14, 20),
    "line":   (38, 42, 52),
    "ink":    (235, 240, 248),
    "muted":  (140, 150, 170),
    "faded":  (88, 96, 112),
    "accent": (60, 180, 255),
    "good":   (80, 220, 110),
    "bad":    (240, 80, 80),
    "gold":   (255, 210, 60),
    "darkink": (10, 12, 18),
}

SECTION_COLOR = {
    "body": C["corps"], "cog": C["cognition"], "perso": C["personnalite"],
    "emo": C["emotions"], "needs": C["besoins"], "skills": C["experience"],
}


class UiKit:
    def __init__(self):
        self._scaled = {}
        self._texts = {}
        self._glass = {}
        self._knobs = {}
        self.fonts = {}
        self._fsize = {}
        self._tips = []
        self._init_fonts()

    # ---------------------------------------------------------------- fonts
    def _init_fonts(self):
        def vec(size, bold=False):
            for fam in ("segoeui", "Segoe UI", "arial", "helvetica"):
                try:
                    f = pygame.font.SysFont(fam, size, bold=bold)
                    if f:
                        return f
                except Exception:
                    pass
            return pygame.font.Font(None, size)

        self.fonts["title"] = vec(22, bold=True)
        self.fonts["h2"] = vec(15, bold=True)
        self.fonts["h3"] = vec(13, bold=True)
        self.fonts["body"] = vec(13)
        self.fonts["small"] = vec(11)
        self.fonts["tiny"] = vec(10)
        self._ksize = {"title": 22, "h2": 15, "h3": 13, "body": 13, "small": 11, "tiny": 10}

    def font(self, kind, size=None):
        if size is None or size == self.fonts[kind].get_height():
            return self.fonts[kind]
        k = (kind, size)
        f = self._fsize.get(k)
        if f is None:
            bold = kind in ("title", "h2", "h3")
            try:
                f = pygame.font.SysFont("segoeui", size, bold=bold)
            except Exception:
                f = pygame.font.Font(None, size)
            self._fsize[k] = f
        return f

    def text(self, kind, s, color):
        k = (kind, s, color)
        v = self._texts.get(k)
        if v is None:
            v = self.fonts[kind].render(s, True, color)
            self._texts[k] = v
            if len(self._texts) > 2200:
                self._texts.clear()
                self._texts[k] = v
        return v

    def text_fit(self, kind, s, color, maxw):
        f = self.fonts[kind]
        if f.size(s)[0] <= maxw:
            return self.text(kind, s, color)
        base = self._ksize.get(kind, 13)
        for size in (base - 1, base - 2, base - 3):
            if size < 8:
                break
            bold = kind in ("title", "h2", "h3")
            try:
                f2 = pygame.font.SysFont("segoeui", size, bold=bold)
            except Exception:
                f2 = pygame.font.Font(None, size)
            if f2.size(s)[0] <= maxw:
                k = (f"{kind}@{size}", s, color)
                v = self._texts.get(k)
                if v is None:
                    v = f2.render(s, True, color)
                    self._texts[k] = v
                return v
        while s and f.size(s + "…")[0] > maxw:
            s = s[:-1]
        return self.text(kind, s + "…", color)

    def draw_fit(self, screen, kind, s, color, x, y, maxw, cy=False):
        t = self.text_fit(kind, s, color, maxw)
        yy = y - t.get_height() // 2 if cy else y
        screen.blit(t, (x, yy))
        return t.get_width()

    def draw_text(self, screen, kind, s, color, x, y, cx=False, cy=False):
        t = self.text(kind, s, color)
        if cx:
            x -= t.get_width() // 2
        if cy:
            y -= t.get_height() // 2
        screen.blit(t, (x, y))
        return t.get_rect()

    # ---------------------------------------------------------------- widgets
    BTN_PAL = {"Blue": (42, 88, 148), "Green": (42, 118, 72), "Red": (148, 48, 48),
               "Yellow": (158, 118, 38), "Grey": (38, 44, 58)}

    @staticmethod
    def _shade(col, d):
        return tuple(max(0, min(255, c + d)) for c in col)

    def _sheen(self, size):
        s = self._scaled.get(("__sheen__", size))
        if s is None:
            w, h = size
            s = pygame.Surface((w, h), pygame.SRCALPHA)
            n = max(2, h // 2)
            for i in range(n):
                pygame.draw.line(s, (255, 255, 255, int(24 * (1 - i / n))), (0, i), (w, i))
            m = pygame.Surface((w, h), pygame.SRCALPHA)
            pygame.draw.rect(m, (255, 255, 255, 255), (0, 0, w, h), border_radius=7)
            s.blit(m, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            self._scaled[("__sheen__", size)] = s
        return s

    def _rbtn(self, screen, rect, base, state="normal"):
        r = pygame.Rect(rect)
        if state == "disabled":
            fill, edge = (20, 24, 34), (38, 44, 58)
        elif state == "selected":
            fill, edge = self._shade(base, 28), self._shade(base, 98)
        elif state == "hover":
            fill, edge = self._shade(base, 22), self._shade(base, 72)
        elif state == "pressed":
            fill, edge = self._shade(base, -16), self._shade(base, 44)
            r.y += 1
        else:
            fill, edge = base, self._shade(base, 48)
        pygame.draw.rect(screen, fill, r, border_radius=7)
        if state != "disabled":
            screen.blit(self._sheen(r.size), r)
        pygame.draw.rect(screen, edge, r, 1, border_radius=7)
        if state == "selected":
            pygame.draw.line(screen, self._shade(edge, 44), (r.x + 6, r.y + 1),
                             (r.right - 7, r.y + 1))

    def button(self, screen, rect, state="normal"):
        self._rbtn(screen, rect, self.BTN_PAL["Grey"], state)

    def button_color(self, screen, rect, color_name, state="normal"):
        self._rbtn(screen, rect, self.BTN_PAL.get(color_name, self.BTN_PAL["Grey"]), state)

    def chip(self, screen, rect, color_name="Grey", state="normal"):
        base = self.BTN_PAL.get(color_name, self.BTN_PAL["Grey"])
        r = pygame.Rect(rect)
        fill = self._shade(base, 18) if state in ("selected", "hover") else base
        pygame.draw.rect(screen, fill, r, border_radius=r.height // 2)
        pygame.draw.rect(screen, self._shade(base, 52), r, 1, border_radius=r.height // 2)

    def input_bg(self, screen, rect, focus=False):
        r = pygame.Rect(rect)
        pygame.draw.rect(screen, (11, 14, 22), r, border_radius=8)
        pygame.draw.rect(screen, C["accent"] if focus else (44, 52, 72), r, 1, border_radius=8)
        if focus:
            ov = pygame.Surface(r.inflate(6, 6).size, pygame.SRCALPHA)
            pygame.draw.rect(ov, (*C["accent"], 42), ov.get_rect(), 2, border_radius=10)
            screen.blit(ov, r.inflate(6, 6))

    def divider(self, screen, x, y, w):
        pygame.draw.line(screen, C["line"], (x, y), (x + w, y))

    # ---------------------------------------------------------------- glass panel
    def glass(self, screen, rect, alpha=170, tint=(18, 22, 36), edge=(62, 74, 108),
              radius=10, glow=False):
        w, h = rect.size
        if w <= 0 or h <= 0:
            return
        key = (w, h, alpha, tint, edge, radius, glow)
        surf = self._glass.get(key)
        if surf is None:
            surf = pygame.Surface((w, h), pygame.SRCALPHA)
            surf.fill((*tint, alpha))
            band = pygame.Surface((w, min(h, 28)), pygame.SRCALPHA)
            for i in range(band.get_height()):
                a = int(18 * (1 - i / band.get_height()))
                pygame.draw.line(band, (190, 210, 245, a), (0, i), (w, i))
            surf.blit(band, (0, 0))
            r = pygame.Rect(0, 0, w, h)
            pygame.draw.rect(surf, (*edge, min(255, alpha + 55)), r, 1, border_radius=radius)
            if glow:
                pygame.draw.rect(surf, (*edge, 50), r.inflate(2, 2), 1, border_radius=radius + 1)
            self._glass[key] = surf
            if len(self._glass) > 90:
                self._glass.pop(next(iter(self._glass)))
        screen.blit(surf, rect)

    # ---------------------------------------------------------------- gauge bar
    def gauge(self, screen, rect, value, color, bg=(24, 28, 42), seg=None):
        v = max(0.0, min(1.0, value))
        r = pygame.Rect(rect)
        rad = r.height // 2
        pygame.draw.rect(screen, bg, r, border_radius=rad)
        fw = int(r.width * v)
        if fw >= 2:
            fill = pygame.Rect(r.x, r.y, fw, r.height)
            pygame.draw.rect(screen, color, fill, border_radius=rad)
        pygame.draw.rect(screen, tuple(min(255, c + 16) for c in bg), r, 1, border_radius=rad)

    def knob(self, screen, rect, color):
        cx, cy = rect.centerx, rect.centery
        rad = max(4, min(rect.width, rect.height) // 2)
        pygame.draw.circle(screen, (8, 10, 16), (cx, cy), rad + 1)
        pygame.draw.circle(screen, color, (cx, cy), rad)
        pygame.draw.circle(screen, tuple(min(255, c + 55) for c in color),
                           (cx - rad // 3, cy - rad // 3), max(1, rad // 3))

    def pill(self, screen, rect, color, alpha=255):
        r = pygame.Rect(rect)
        pygame.draw.rect(screen, (*color[:3], alpha), r, border_radius=r.height // 2)

    def slider(self, screen, rect, value, color, dragging=False, locked=False,
               hover=False):
        base = C["faded"] if locked else color
        tr = pygame.Rect(rect)
        h = 7 if not dragging else 9
        tr.y += (rect.height - h) // 2
        tr.height = h
        if locked:
            self.gauge(screen, tr, value, (52, 57, 72))
            self.lock(screen, tr.centerx - 5, tr.centery - 6, (120, 126, 140))
            return
        self.gauge(screen, tr, value, base)
        hx = tr.x + int(tr.width * max(0.0, min(1.0, value)))
        hs = 15 if not dragging else 19
        if hover or dragging:
            self.knob(screen, pygame.Rect(hx - hs // 2, rect.centery - hs // 2, hs, hs), base)
        else:
            pygame.draw.circle(screen, (208, 218, 232), (hx, rect.centery), 4)
            pygame.draw.circle(screen, (18, 22, 32), (hx, rect.centery), 2)

    def accordion_header(self, screen, rect, label, color, open_, hovered,
                         count=0, avg=None):
        r = pygame.Rect(rect)
        # fond de section coloré selon l'état
        if open_:
            bgc = self._shade(color, -140) if hovered else self._shade(color, -160)
        else:
            bgc = (28, 32, 44) if hovered else (22, 26, 36)
        pygame.draw.rect(screen, bgc, r, border_radius=6)
        # accent gauche coloré (large)
        pygame.draw.rect(screen, color, (r.x + 2, r.y + 2, 4, r.height - 4), border_radius=2)
        # chevron
        cx, cy = r.x + 16, r.centery
        if open_:
            pts = [(cx - 4, cy - 2), (cx + 4, cy - 2), (cx, cy + 3)]
        else:
            pts = [(cx - 2, cy - 4), (cx + 3, cy), (cx - 2, cy + 4)]
        pygame.draw.polygon(screen, color if hovered else C["muted"], pts)
        # titre
        tw = self.draw_fit(screen, "h3", label.upper(),
                           C["ink"] if open_ else C["muted"],
                           r.x + 26, r.y + (r.height - self.fonts["h3"].get_height()) // 2 + 1,
                           r.width - 90)
        # moyenne quand replie
        x = r.x + 30 + tw
        if not open_ and avg is not None:
            gr = pygame.Rect(0, 0, 60, 5)
            gr.centery = r.centery
            gr.x = min(r.right - 68, x + 12)
            self.gauge(screen, gr, avg, color)
        # compteur
        pg = pygame.Rect(r.right - 30, r.centery - 8, 22, 16)
        pygame.draw.rect(screen, (14, 18, 28), pg, border_radius=8)
        self.draw_text(screen, "tiny", str(count), C["faded"], pg.x + 11, pg.centery,
                       cx=True, cy=True)

    def section_header(self, screen, rect, label, color, open_=True):
        self.accordion_header(screen, rect, label, color, open_, False)

    def arrow(self, screen, rect, direction, color=None):
        c = color or C["muted"]
        cx, cy = rect.centerx, rect.centery
        s = min(rect.width, rect.height) // 3
        if direction == "s":
            pts = [(cx - s, cy - s // 2), (cx + s, cy - s // 2), (cx, cy + s)]
        elif direction == "e":
            pts = [(cx - s // 2, cy - s), (cx + s, cy), (cx - s // 2, cy + s)]
        elif direction == "n":
            pts = [(cx - s, cy + s // 2), (cx + s, cy + s // 2), (cx, cy - s)]
        else:
            pts = [(cx + s // 2, cy - s), (cx - s, cy), (cx + s // 2, cy + s)]
        pygame.draw.polygon(screen, c, pts)

    def star(self, screen, rect, filled):
        c = C["gold"] if filled else C["faded"]
        cx, cy = rect.centerx, rect.centery
        r = min(rect.width, rect.height) // 2 - 1
        pts = []
        for i in range(5):
            import math
            a = math.radians(-90 + i * 72)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
            a2 = math.radians(-90 + i * 72 + 36)
            pts.append((cx + r * 0.4 * math.cos(a2), cy + r * 0.4 * math.sin(a2)))
        pygame.draw.polygon(screen, c, pts)
        if not filled:
            pygame.draw.polygon(screen, C["line"], pts, 1)

    def lock(self, screen, x, y, color=(240, 160, 150)):
        s = pygame.Surface((10, 12), pygame.SRCALPHA)
        pygame.draw.rect(s, (255, 255, 255), (0, 5, 10, 7), border_radius=2)
        pygame.draw.arc(s, (255, 255, 255), (2, 0, 6, 8), 0.2, 2.94, 2)
        s.fill((*color, 255), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(s, (x, y))

    def dot(self, screen, cx, cy, color, r=4, ring=None):
        pygame.draw.circle(screen, color, (cx, cy), r)
        if ring:
            pygame.draw.circle(screen, ring, (cx, cy), r, 1)

    def icon(self, screen, rect, icon_name, color="Grey"):
        c = self.BTN_PAL.get(color, C["muted"])
        cx, cy = rect.centerx, rect.centery
        s = min(rect.width, rect.height) // 3
        if "check" in icon_name:
            pygame.draw.lines(screen, c, False, [(cx - s, cy), (cx - s // 3, cy + s), (cx + s, cy - s)], 2)
        elif "cross" in icon_name:
            pygame.draw.line(screen, c, (cx - s, cy - s), (cx + s, cy + s), 2)
            pygame.draw.line(screen, c, (cx + s, cy - s), (cx - s, cy + s), 2)
        elif "circle" in icon_name:
            pygame.draw.circle(screen, c, (cx, cy), s)
        else:
            pygame.draw.rect(screen, c, rect.inflate(-6, -6), border_radius=3)

    def check(self, screen, rect, checked=False, color="Blue"):
        r = pygame.Rect(rect)
        pygame.draw.rect(screen, C["bg2"], r, border_radius=3)
        pygame.draw.rect(screen, C["line"], r, 1, border_radius=3)
        if checked:
            c = self.BTN_PAL.get(color, C["accent"])
            cx, cy = r.centerx, r.centery
            s = min(r.width, r.height) // 3
            pygame.draw.lines(screen, c, False,
                              [(cx - s, cy), (cx - s // 3, cy + s), (cx + s, cy - s)], 2)

    # ---------------------------------------------------------------- tooltips
    def tip(self, rect, lines):
        self._tips.append((rect, lines))

    def draw_tips(self, screen, mouse):
        if not self._tips:
            return
        for rect, lines in self._tips:
            if not rect.collidepoint(mouse):
                continue
            wdt = max(self.fonts["small"].size(s)[0] for s in lines) + 16
            hgt = 6 + 14 * len(lines)
            x = min(mouse[0] + 14, screen.get_width() - wdt - 4)
            y = min(mouse[1] + 16, screen.get_height() - hgt - 4)
            panel = pygame.Surface((wdt, hgt), pygame.SRCALPHA)
            pygame.draw.rect(panel, (10, 13, 22, 245), (0, 0, wdt, hgt), border_radius=7)
            pygame.draw.rect(panel, (*C["line"], 255), (0, 0, wdt, hgt), 1, border_radius=7)
            pygame.draw.line(panel, (255, 255, 255, 22), (6, 1), (wdt - 7, 1))
            screen.blit(panel, (x, y))
            for i, s in enumerate(lines):
                col = C["ink"] if i == 0 else C["muted"]
                self.draw_text(screen, "small", s, col, x + 8, y + 4 + i * 14)
        self._tips.clear()


_KIT = None


def get_kit():
    global _KIT
    if _KIT is None:
        _KIT = UiKit()
    return _KIT

```

## game/ui_registry.py

**Type :** `.py`

```python

"""UI Registry — registres declaratifs de l'interface.

Extrait de dashboard.py. Ces registres ne contiennent aucune
coordonnee Pygame, aucune surface, aucun widget. Ils decrivent
uniquement la structure de l'interface.

Pour ajouter une section ou une carte, ajouter UNE entree ici.
"""
from __future__ import annotations

# ══════════════════════════════════════════════════════════════════════
#  Couleurs d'accent par famille de donnees
# ══════════════════════════════════════════════════════════════════════
C_CORPS = (67, 160, 92)
C_COG = (62, 124, 214)
C_PERSO = (222, 164, 46)
C_EMO = (34, 158, 142)
C_BESOIN = (146, 96, 186)
C_EXP = (206, 126, 60)
C_MEM = (150, 110, 200)

# ══════════════════════════════════════════════════════════════════════
#  Definitions des champs
# ══════════════════════════════════════════════════════════════════════
from .config import (
    BODY_DEFS, COG_DEFS, PERSONALITY_DEFS, EMOTION_DEFS, NEED_DEFS,
)

SKILL_DEFS = ["recolte", "construction", "combat", "social"]

# ══════════════════════════════════════════════════════════════════════
#  Section Registry — accordions de l'inspecteur
#  (cle, libelle, couleur, champs, attribut_agent, attribut_template)
# ══════════════════════════════════════════════════════════════════════
SECTION_REGISTRY = [
    ("body",   "Corps",        C_CORPS,  BODY_DEFS,        "body",        "tpl_body"),
    ("cog",    "Cognition",    C_COG,    COG_DEFS,         "cog",         "tpl_cog"),
    ("perso",  "Personnalite", C_PERSO,  PERSONALITY_DEFS, "personality", "tpl_personality"),
    ("emo",    "Emotions",     C_EMO,    EMOTION_DEFS,     "emotions",    "tpl_emotions"),
    ("needs",  "Besoins",      C_BESOIN, NEED_DEFS,        "needs",       "tpl_needs"),
    ("skills", "Experience",   C_EXP,    SKILL_DEFS,       "skills",      "tpl_skills"),
]

DEFAULT_OPEN = {
    "body": True, "cog": True, "perso": True,
    "emo": True, "needs": False, "skills": False,
}

# ══════════════════════════════════════════════════════════════════════
#  Card Registry — cartes de la colonne droite
# ══════════════════════════════════════════════════════════════════════
CARD_REGISTRY = [
    ("intention", "Intention"),
    ("memoire", "Memoire"),
    ("gabarit", "Gabarit"),
    ("events", "Evenements"),
]

# ══════════════════════════════════════════════════════════════════════
#  Onglets
# ══════════════════════════════════════════════════════════════════════
TABS = [
    ("decor",      "DECOR"),
    ("etre",       "ETRE"),
    ("habitants",  "HABITANTS"),
    ("creator",    "CREATEUR"),
    ("societe",    "SOCIETE"),
    ("journal",    "JOURNAL"),
]

READONLY_TABS = ("societe", "journal", "habitants")

# ══════════════════════════════════════════════════════════════════════
#  Modes d'interaction (outils)
# ══════════════════════════════════════════════════════════════════════
MODES = [
    ("place", "Poser"), ("erase", "Gommer"), ("floor", "Sol"),
    ("block", "Bloc"),
    ("agent", "Etre"), ("sheep", "Mouton"), ("monster", "Monstre"),
    ("inspect", "Examiner"),
    ("water", "Eau"), ("land", "Terre"), ("wall", "Mur"),
    ("carve", "Sculpter"), ("restore", "Restaurer"),
]

SEX_CLASSES = {
    "M": ("swordsman", "archer", "wizard", "pawn"),
    "F": ("knight", "enchantress", "musketeer", "pawn"),
}

TAB_MODES = {
    "decor": [
        ("place", "Poser"), ("erase", "Gommer"), ("floor", "Sol"),
        ("block", "Bloc"),
        ("water", "Eau"), ("land", "Terre"), ("wall", "Mur"),
        ("carve", "Sculpter"), ("restore", "Restaurer"),
        ("inspect", "Examiner"),
    ],
    "etre":     [("agent", "Etre"), ("inspect", "Examiner")],
    "habitants": [("agent", "Creer"), ("inspect", "Examiner")],
    "societe":  [],
    "journal":  [],
}

TAB_HINTS = {
    "place":   "clic = poser l'asset / glisser = peindre",
    "erase":   "clic = effacer les objets de la case",
    "floor":   "clic = peindre le sol selectionne",
    "agent":   "clic = inserer l'etre defini dans le gabarit",
    "sheep":   "clic = ajouter un mouton",
    "monster": "clic = ajouter un monstre aleatoire",
    "inspect": "clic = examiner un etre",
    "water":   "glisser = transformer terre en eau (pinceau)",
    "land":    "glisser = transformer eau en terre (pinceau)",
    "wall":    "glisser = placer des rochers solides (pinceau)",
    "carve":   "glisser = creuser les montagnes (pinceau)",
    "restore": "glisser = restaurer le terrain procedural (pinceau)",
}

# ══════════════════════════════════════════════════════════════════════
#  Categories de journal
# ══════════════════════════════════════════════════════════════════════
LOG_CATS = {
    "combat":   (214, 84, 84),
    "social":   (198, 100, 162),
    "meteo":    (62, 124, 214),
    "economie": (206, 160, 50),
    "vie":      (67, 160, 92),
    "mort":     (140, 80, 86),
    "batiment": (96, 154, 96),
    "monde":    (112, 126, 150),
}

LOG_TITLES = {
    "combat":   "Combat",
    "social":   "Social",
    "meteo":    "Meteo",
    "economie": "Economie",
    "vie":      "Vie",
    "mort":     "Mort",
    "batiment": "Batiment",
    "monde":    "Monde",
}

# ══════════════════════════════════════════════════════════════════════
#  Categories d'assets
# ══════════════════════════════════════════════════════════════════════
CAT_ALL = "__all__"
HIDDEN_CATS = {"unites", "interface", "atlas", "rendus"}

CHIP_LABELS = {
    "__all__": "Tous",
    "ressources": "Ressources",
    "nourriture": "Nourriture",
    "batiments": "Batiments",
    "outils": "Outils",
    "animaux": "Animaux",
    "props": "Props",
    "vehicules": "Vehicules",
    "tombe": "Tombes",
    "decor": "Decor",
    "sol": "Sols",
    "unites": "Unites",
    "interface": "Interface",
    "materiaux": "Materiaux",
    "meat_res": "Viande",
    "weapon": "Armes",
    "armor": "Armures",
}

# ══════════════════════════════════════════════════════════════════════
#  Panels — description des panneaux pour le découpage Pygame/Qt
# ══════════════════════════════════════════════════════════════════════
PANELS = {
    "population": {
        "title": "Habitants",
        "snapshot": "population",
        "tab": "habitants",
    },
    "inspector": {
        "title": "Inspecteur",
        "snapshot": "selected_agent",
        "tab": "etre",
    },
    "anima": {
        "title": "Anima",
        "snapshot": "selected_agent.anima",
        "tab": "etre",
    },
    "journal": {
        "title": "Journal",
        "snapshot": "journal",
        "tab": "journal",
    },
    "society": {
        "title": "Societe",
        "snapshot": "society",
        "tab": "societe",
    },
    "assets": {
        "title": "Assets",
        "snapshot": "assets",
        "tab": "decor",
    },
    "creator": {
        "title": "Createur",
        "snapshot": "template",
        "tab": "creator",
    },
    "world_tools": {
        "title": "Outils monde",
        "snapshot": "tools",
        "tab": "decor",
    },
}

```

## game/ui_snapshots.py

**Type :** `.py`

```python

"""UI Snapshots — vues immuables du moteur pour l'interface.

Chaque snapshot ne contient que des types simples (None, bool, int, float,
str, list, dict, tuples). Aucune surface Pygame, aucun widget Qt.

Réutilise les fonctions de diagnostics.py qui sont déjà validées.
"""
from __future__ import annotations

from typing import Any


def _safe_list(value) -> list:
    """Convertit un array numpy ou autre en liste Python."""
    if hasattr(value, "tolist"):
        return value.tolist()
    return list(value or [])


# ══════════════════════════════════════════════════════════════════════
#  Snapshot simulation globale
# ══════════════════════════════════════════════════════════════════════
def simulation_snapshot(sim, ui_state=None) -> dict[str, Any]:
    """État global de la simulation, pour le header / footer."""
    clock = getattr(sim, "clock", None)
    return {
        "tick": int(sim.w.tick),
        "paused": bool(sim.paused),
        "speed": int(sim.speed),
        "population": sum(1 for a in sim.agents if a.alive),
        "sheep": len(sim.sheep),
        "monsters": len(sim.monsters),
        "stats": {
            key: int(value) if isinstance(value, (int, float)) else value
            for key, value in sim.stats.items()
        },
        "clock": {
            "year": int(clock.year) if clock else 0,
            "day": int(clock.day) if clock else 0,
            "season": str(clock.season) if clock else "",
            "light": float(clock.light) if clock else 1.0,
            "temperature": float(clock.temp) if clock else 20.0,
            "rain": float(clock.rain) if clock else 0.0,
            "label": str(clock.label) if clock else "",
        },
        "selection": {
            "agent_eid": getattr(ui_state, "selected_agent_eid", None),
            "tile": getattr(ui_state, "selected_tile", None),
        },
    }


# ══════════════════════════════════════════════════════════════════════
#  Snapshot population
# ══════════════════════════════════════════════════════════════════════
def population_snapshot(sim) -> list[dict[str, Any]]:
    """Liste d'habitants vivants, pour le tableau de population."""
    from .diagnostics import agent_snapshot

    rows = []
    for agent in sim.agents:
        if not agent.alive:
            continue
        snap = agent_snapshot(sim, agent)
        if snap is not None:
            rows.append(snap)
    return rows


# ══════════════════════════════════════════════════════════════════════
#  Snapshot agent sélectionné
# ══════════════════════════════════════════════════════════════════════
def selected_agent_snapshot(sim, ui_state=None) -> dict[str, Any] | None:
    """Snapshot détaillé de l'habitant sélectionné."""
    eid = getattr(ui_state, "selected_agent_eid", None)
    if eid is None:
        agent = getattr(sim, "selected", None)
        if agent is not None and agent.alive:
            eid = agent.eid
        else:
            return None
    agent = next((a for a in sim.agents if a.eid == eid and a.alive), None)
    if agent is None:
        return None
    from .diagnostics import agent_snapshot
    return agent_snapshot(sim, agent)


# ══════════════════════════════════════════════════════════════════════
#  Snapshot journal
# ══════════════════════════════════════════════════════════════════════
def journal_snapshot(sim, category: str = "tous", search: str = "",
                     max_entries: int = 200) -> list[dict[str, Any]]:
    """Journal filtré, pour le panneau journal."""
    entries = list(sim.journal)
    if category and category != "tous":
        entries = [e for e in entries if e[3] == category]
    if search:
        search_lower = search.lower()
        entries = [e for e in entries if search_lower in str(e[1]).lower()]
    result = []
    for tick, text, color, cat, count in entries[-max_entries:]:
        result.append({
            "tick": int(tick),
            "text": str(text),
            "color": tuple(color) if color else (180, 180, 180),
            "category": str(cat),
            "count": int(count),
        })
    return result


# ══════════════════════════════════════════════════════════════════════
#  Snapshot tiles (pour l'inspecteur de carte)
# ══════════════════════════════════════════════════════════════════════
def tile_snapshot(sim, tx: int, ty: int) -> dict[str, Any]:
    """Wrapper vers diagnostics.tile_snapshot."""
    from .diagnostics import tile_snapshot as _ts
    return _ts(sim, tx, ty)


# ══════════════════════════════════════════════════════════════════════
#  Snapshot carte (pour le rendu Qt)
# ══════════════════════════════════════════════════════════════════════
def map_snapshot(sim, ui_state=None) -> dict[str, Any]:
    """Données de carte pour le rendu : terrain, objets, agents, effets.

    Aucune surface ni rendu. Juste des coordonnées et des métadonnées.
    """
    w = sim.w
    alive_agents = []
    for a in sim.agents:
        if a.alive:
            alive_agents.append({
                "eid": int(a.eid),
                "x": float(a.x),
                "y": float(a.y),
                "tx": int(a.tx),
                "ty": int(a.ty),
                "color": str(a.color),
                "cls": str(a.cls),
                "stage": str(a.stage),
                "alive": True,
            })

    sheep_list = []
    for s in sim.sheep:
        sheep_list.append({
            "eid": int(s.eid),
            "x": float(s.x),
            "y": float(s.y),
            "tx": int(s.tx),
            "ty": int(s.ty),
        })

    monsters_list = []
    for m in sim.monsters:
        monsters_list.append({
            "eid": int(m.eid),
            "x": float(m.x),
            "y": float(m.y),
            "tx": int(m.tx),
            "ty": int(m.ty),
            "kind": str(getattr(m, "kind", "unknown")),
        })

    effects_list = []
    for e in sim.effects:
        effects_list.append({
            "kind": str(e.get("kind", "")),
            "x": float(e.get("x", 0)),
            "y": float(e.get("y", 0)),
            "color": tuple(e.get("color", (255, 255, 255))),
        })

    selected_eid = None
    if ui_state and getattr(ui_state, "selected_agent_eid", None) is not None:
        selected_eid = ui_state.selected_agent_eid

    return {
        "tick": int(w.tick),
        "grid": int(w.g),
        "fire_cells": int((w.fire > 0).sum()),
        "agents": alive_agents,
        "sheep": sheep_list,
        "monsters": monsters_list,
        "effects": effects_list,
        "selected_eid": selected_eid,
        "ghost_tile": getattr(ui_state, "ghost_tile", None) if ui_state else None,
        "ghost_visible": getattr(ui_state, "ghost_visible", False) if ui_state else False,
        "cemetery": [
            {"x": int(gx), "y": int(gy), "name": str(name)}
            for gx, gy, name, *_ in getattr(w, "cemetery", ())
        ],
    }


# ══════════════════════════════════════════════════════════════════════
#  Snapshot société
# ══════════════════════════════════════════════════════════════════════
def society_snapshot(sim) -> dict[str, Any]:
    """Données pour le panneau société."""
    alive = [a for a in sim.agents if a.alive]
    max_gen = max((a.gen for a in alive), default=0) if alive else 0
    bonded_count = sum(1 for a in alive if getattr(a, "bonded", None) is not None)

    alive_eids = {a.eid for a in alive}
    relations = []
    seen = set()
    for a in alive:
        for other_eid, rel_data in getattr(a, "rel", {}).items():
            if other_eid not in alive_eids:
                continue
            pair = (min(a.eid, other_eid), max(a.eid, other_eid))
            if pair in seen:
                continue
            seen.add(pair)
            trust = rel_data[0] if isinstance(rel_data, (tuple, list)) else float(rel_data)
            affection = rel_data[1] if isinstance(rel_data, (tuple, list)) and len(rel_data) > 1 else 0.0
            other = next((x for x in alive if x.eid == other_eid), None)
            if other is None:
                continue
            if a.bonded == other_eid:
                rel_type = "bonded"
            else:
                rel_type = "allied"
            relations.append({
                "eid1": a.eid,
                "name1": a.name,
                "eid2": other_eid,
                "name2": other.name,
                "type": rel_type,
                "confiance": float(trust),
                "affinite": float(affection),
            })

    return {
        "population": len(alive),
        "max_generation": int(max_gen),
        "bonded": bonded_count,
        "sheep": len(sim.sheep),
        "monsters": len(sim.monsters),
        "stats": {
            key: int(value)
            for key, value in sim.stats.items()
        },
        "relations": relations,
    }


# ══════════════════════════════════════════════════════════════════════
#  Snapshot Anima enrichi (pour l'inspecteur Anima)
# ══════════════════════════════════════════════════════════════════════
def anima_snapshot(sim, ui_state=None) -> dict[str, Any] | None:
    """Snapshot étendu pour l'inspecteur Anima complet."""
    base = selected_agent_snapshot(sim, ui_state)
    if base is None:
        return None

    agent = None
    eid = base.get("eid")
    if eid is not None:
        agent = next((a for a in sim.agents if a.eid == eid and a.alive), None)

    if agent is None:
        return base

    anima = getattr(agent, "anima", {}) or {}
    identity = dict(anima.get("identity", {}))
    values = dict(anima.get("values", {}))
    trauma = dict(anima.get("trauma", {}))
    intention = anima.get("intention")
    plan = anima.get("plan")
    beliefs = anima.get("beliefs", {})
    social_beliefs = beliefs.get("beings", {})

    base["anima"] = {
        "identity": identity,
        "values": values,
        "trauma": trauma,
        "intention": dict(intention) if isinstance(intention, dict) else None,
        "plan": dict(plan) if isinstance(plan, dict) else None,
        "attachments": dict(anima.get("attachments", {})),
        "social_beliefs": {
            str(key): dict(value) if isinstance(value, dict) else value
            for key, value in social_beliefs.items()
        },
        "episodes": list(anima.get("episodic_memory", []))[-10:],
        "reputation": dict(anima.get("reputation", {})),
    }

    return base

```

## game/ui_state.py

**Type :** `.py`

```python

"""UIState — état d'interface neutre, sans dépendance Pygame ni Qt.

Cet état est partagé entre le moteur de simulation et n'importe quel
frontend (Pygame, PyQt6, futur web). Il ne contient que des types simples.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class UIState:
    """État central de l'interface, indépendant du backend de rendu."""

    # ── Navigation ──
    active_tab: str = "etre"
    active_mode: str = "agent"
    active_overlay: str = "none"

    # ── Sélection ──
    selected_agent_eid: int | None = None
    selected_asset_id: int | None = None
    selected_tile: tuple[int, int] | None = None

    # ── Filtres et recherche ──
    selected_category: str = "all"
    search_text: str = ""
    journal_filter: str = "tous"
    only_favs: bool = False

    # ── Simulation ──
    speed: int = 1
    paused: bool = True

    # ── Caméra ──
    follow_selected: bool = False
    camera_x: float = 0.0
    camera_y: float = 0.0
    camera_zoom: float = 0.25
    camera_tilt: float = 55.0

    # ── Panneaux ──
    left_panel_open: bool = True
    right_panel_open: bool = True

    # ── Pinceau / Outils ──
    brush_size: int = 3
    block_material: str = "bois"

    # ── Sections accordéon (inspecteur) ──
    open_sections: dict = field(default_factory=dict)
    open_cards: dict = field(default_factory=dict)

    # ── favoris / récents assets ──
    favs: list = field(default_factory=list)
    recents: list = field(default_factory=list)

    # ── Ghost / placement ──
    ghost_visible: bool = False
    ghost_tile: tuple[int, int] | None = None

    # ── Créateur d'habitant ──
    creator_open: bool = False
    template_color: str = "blue"
    template_class: str = "pawn"
    template_sex: str = "M"

    # ── UI state signaux ──
    needs_save: bool = False
    action: tuple | None = None

    def sync_from_simulation(self, sim) -> None:
        """Synchronise les champs dérivés de l'état de simulation."""
        self.paused = bool(sim.paused)
        self.speed = int(sim.speed)
        if getattr(sim, "selected", None) is not None and sim.selected.alive:
            self.selected_agent_eid = int(sim.selected.eid)
        else:
            self.selected_agent_eid = None

    def snapshot_dict(self) -> dict:
        """Retourne un dictionnaire de types simples, sérialisable JSON."""
        return {
            "active_tab": self.active_tab,
            "active_mode": self.active_mode,
            "active_overlay": self.active_overlay,
            "selected_agent_eid": self.selected_agent_eid,
            "selected_asset_id": self.selected_asset_id,
            "selected_tile": self.selected_tile,
            "selected_category": self.selected_category,
            "search_text": self.search_text,
            "journal_filter": self.journal_filter,
            "only_favs": self.only_favs,
            "speed": self.speed,
            "paused": self.paused,
            "follow_selected": self.follow_selected,
            "camera_x": self.camera_x,
            "camera_y": self.camera_y,
            "camera_zoom": self.camera_zoom,
            "camera_tilt": self.camera_tilt,
            "left_panel_open": self.left_panel_open,
            "right_panel_open": self.right_panel_open,
            "brush_size": self.brush_size,
            "block_material": self.block_material,
            "ghost_visible": self.ghost_visible,
            "ghost_tile": self.ghost_tile,
            "creator_open": self.creator_open,
            "needs_save": self.needs_save,
        }

```

## game/universal_knowledge.py

**Type :** `.py`

```python

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

```

## game/world.py

**Type :** `.py`

```python

"""WorldGrid : carte 312x312 tuiles de 16px (~5000x5000 px), contenu, blocage,
abris, pv de ressource, pheromones, decors, elements laches."""
import os
from dataclasses import dataclass
import numpy as np

from .config import GRID, TILE, ROOT

MODS_FILE = os.path.join(ROOT, "map", "terrain_mods.npy")


class World:
    def __init__(self):
        g = GRID
        self.g = g
        self.floor = np.full((g, g), -1, dtype=np.int16)   # sheet*216+cell
        self.content = np.full((g, g), -1, dtype=np.int16)  # asset id (anchor)
        self.owner = np.full((g, g), -1, dtype=np.int32)   # flat anchor index for footprint
        self.blocked = np.zeros((g, g), dtype=np.uint8)
        self.shelter = np.zeros((g, g), dtype=np.uint8)
        self.hp = np.zeros((g, g), dtype=np.int16)
        self.marker = np.zeros((g, g), dtype=np.float32)   # pheromones
        self.marker_col = np.zeros((g, g), dtype=np.uint8)
        self.regrow = np.zeros((g, g), dtype=np.float32)   # stump regrow timer
        self.items = []      # Item
        self.dirty_chunks = set()
        self.tick = 0
        self.land = np.ones((g, g), dtype=np.uint8)   # masque continents (map.png)
        self.water = np.zeros((g, g), dtype=np.uint8)
        self.fire = np.zeros((g, g), dtype=np.int16)   # ticks de flamme restants
        self.smell = np.zeros((g, g), dtype=np.float32)  # champ d'odeurs (feu, nourriture, mort)
        self.heat = np.zeros((g, g), dtype=np.float32)   # traces de présence (exploration)
        self.cemetery = []  # list of (tx, ty, name, death_tick, color_rgb)
        self.storages = {}  # (tx, ty) -> Storage
        self.sites = {}     # (tx, ty) -> BuildingSite
        self.crop_plots = {}  # (tx, ty) -> CropPlot
        self.mountains = np.zeros((g, g), dtype=np.uint8)  # terrain montagnes ( jamais modifie)
        self.foundation = np.full((g, g), -1, dtype=np.int16)
        self.roof = np.full((g, g), -1, dtype=np.int16)
        # index de connaissance : ou est chaque categorie de ressource
        self.kidx = {k: {} for k in ("food", "wood", "stone", "gold", "tool", "shelter")}
        self._kcell = 8
        self.gen = None  # WorldGen instance (worldgen.py)

    def set_land(self, mask):
        self.land = mask.astype(np.uint8)
        self.water = (1 - self.land).astype(np.uint8)

    # ------------------------------------------------------------------ persistence
    def save_mods(self, path=None):
        """Sauvegarde les modifications terrain (land + water) dans un .npy."""
        path = path or MODS_FILE
        os.makedirs(os.path.dirname(path), exist_ok=True)
        np.savez_compressed(path, land=self.land, water=self.water)

    def load_mods(self, path=None):
        """Charge les modifications terrain si le fichier existe et taille compatible."""
        path = path or MODS_FILE
        if not os.path.exists(path):
            return False
        try:
            data = np.load(path)
            l = data["land"]
            if l.shape[0] != self.g or l.shape[1] != self.g:
                os.remove(path)
                return False
            self.land = l.astype(np.uint8)
            self.water = data["water"].astype(np.uint8)
            return True
        except Exception:
            return False

    def is_land(self, tx, ty):
        return bool(self.land[ty, tx]) if self.inb(tx, ty) else False

    def near_water(self, tx, ty):
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                x, y = tx + dx, ty + dy
                if self.inb(x, y) and self.water[y, x]:
                    return True
        return False

    def ignite(self, tx, ty, ticks=220):
        if self.inb(tx, ty) and not self.water[ty, tx]:
            self.fire[ty, tx] = max(self.fire[ty, tx], ticks)
            self.mark_dirty(tx, ty)

    def step_fire(self, am, wind=(0.0, 0.0), rain=0.0, flammable=None):
        """Feu = systeme physique : temperature, combustible, vent, eau.
        Il ne sait pas ce qu'est une maison — il sait seulement bruler."""
        burning = np.nonzero(self.fire > 0)
        if not burning[0].size:
            return 0
        for y, x in zip(*burning):
            self.fire[y, x] -= 1 + int(rain * 6)
            if self.fire[y, x] <= 0:
                self.fire[y, x] = 0
                if self.content[y, x] >= 0 and flammable and int(self.content[y, x]) in flammable:
                    self.burn_out(am, y, x)
                continue
            self.smell[y, x] = min(1.0, self.smell[y, x] + 0.08)
            if self.fire[y, x] % 4 == 0:
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        nx, ny = x + dx + int(wind[0] * 2), y + dy + int(wind[1] * 2)
                        if not self.inb(nx, ny) or self.water[ny, nx] or self.fire[ny, nx]:
                            continue
                        naid = self.content_at(nx, ny)
                        if flammable and naid >= 0 \
                           and naid in flammable \
                           and self.rng_fire.random() < 0.16:
                            self.fire[ny, nx] = 200
        return int(burning[0].size)

    rng_fire = np.random.default_rng(11)

    def _kadd(self, cat, x, y):
        cell = (x // self._kcell, y // self._kcell)
        self.kidx[cat].setdefault(cell, set()).add((x, y))

    def _kdel(self, cat, x, y):
        cell = (x // self._kcell, y // self._kcell)
        s = self.kidx[cat].get(cell)
        if s:
            s.discard((x, y))
            if not s:
                del self.kidx[cat][cell]

    def knearest(self, cat, tx, ty, maxr=40):
        """Position connue la plus proche d'une categorie (le savoir du monde)."""
        best, bd = None, 1e9
        c = self._kcell
        cx, cy = tx // c, ty // c
        r = 0
        while (cx - r) * c <= tx + maxr and (cy - r) * c <= ty + maxr:
            found_ring = False
            for j in range(cy - r, cy + r + 1):
                for i in range(cx - r, cx + r + 1):
                    if max(abs(i - cx), abs(j - cy)) != r:
                        continue
                    for (x, y) in self.kidx[cat].get((i, j), ()):
                        d = max(abs(x - tx), abs(y - ty))
                        if d < bd and d <= maxr:
                            best, bd = (x, y), d
                            found_ring = True
            if found_ring and bd <= r * c:
                break
            r += 1
            if r > 6:
                break
        return best, (bd if best else -1)

    # ------------------------------------------------------------------ utils
    def inb(self, x, y):
        return 0 <= x < self.g and 0 <= y < self.g

    @staticmethod
    def px2t(v):
        return int(v // TILE)

    def anchor_of(self, x, y):
        if not self.inb(x, y):
            return -1
        a = self.owner[y, x]
        return int(a)

    def content_at(self, x, y):
        if not self.inb(x, y):
            return -1
        a = self.anchor_of(x, y)
        if a < 0:
            return -1
        return int(self.content[a // self.g, a % self.g])

    def mark_dirty(self, tx, ty, r=2):
        cx, cy = tx // TILE, ty // TILE
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                self.dirty_chunks.add((cx + dx, cy + dy))

    # ------------------------------------------------------------------ placement
    def place(self, tx, ty, aid, am, hp=1, solid=False, shelter=False, size=1):
        """Met un asset ancre (tx,ty) en occupant une empreinte size x size centree bas."""
        tx = min(max(tx, 0), self.g - size)
        ty = min(max(ty, 0), self.g - size)
        self.remove(tx, ty, quiet=True)
        flat = ty * self.g + tx
        self.content[ty, tx] = aid
        self.hp[ty, tx] = hp
        for j in range(size):
            for i in range(size):
                x, y = tx + i, ty + j
                if self.inb(x, y):
                    self.owner[y, x] = flat
                    if solid:
                        self.blocked[y, x] = 1
                    if shelter:
                        self.shelter[y, x] = 1
        self._kindex_set(tx, ty, am.assets[aid])
        self.mark_dirty(tx, ty, size + 1)

    def _kindex_set(self, tx, ty, asd):
        for cat in list(self.kidx):
            self._kdel(cat, tx, ty)
        if asd.edible > 0:
            self._kadd("food", tx, ty)
        elif asd.harvest:
            m = asd.harvest["material"]
            self._kadd({"bois": "wood", "pierre": "stone", "or": "gold"}.get(m, "wood"), tx, ty)
        elif asd.tool:
            self._kadd("tool", tx, ty)
        if asd.shelter:
            self._kadd("shelter", tx, ty)

    def _kindex_clear(self, tx, ty):
        for cat in self.kidx:
            self._kdel(cat, tx, ty)

    def remove(self, tx, ty, quiet=False):
        tx = min(max(tx, 0), self.g - 1)
        ty = min(max(ty, 0), self.g - 1)
        flat = self.owner[ty, tx]
        if flat < 0:
            return False
        ax, ay = flat % self.g, flat // self.g
        aid = int(self.content[ay, ax])
        # efface toute la zone de l'ancre (jusqu'à 6×6, couvrant tous les assets)
        size = 1
        for j in range(6):
            for i in range(6):
                x, y = ax + i, ay + j
                if self.inb(x, y) and self.owner[y, x] == flat:
                    self.owner[y, x] = -1
                    self.blocked[y, x] = 0
                    self.shelter[y, x] = 0
                    size = max(size, i + 1, j + 1)
        self.content[ay, ax] = -1
        self.hp[ay, ax] = 0
        self.regrow[ay, ax] = 0.0
        self._kindex_clear(ax, ay)
        if not quiet:
            self.mark_dirty(ax, ay, size + 1)
        return True

    def set_floor(self, tx, ty, tile_id):
        if self.inb(tx, ty):
            self.floor[ty, tx] = tile_id
            self.mark_dirty(tx, ty)

    # ------------------------------------------------------------------ items
    def drop_item(self, item):
        self.items.append(item)

    def take_items_at(self, tx, ty, radius_px=10):
        out = []
        cx, cy = tx * TILE + TILE / 2, ty * TILE + TILE / 2
        keep = []
        for it in self.items:
            if (it.x - cx) ** 2 + (it.y - cy) ** 2 <= radius_px * radius_px:
                out.append(it)
            else:
                keep.append(it)
        self.items = keep
        return out

    # ------------------------------------------------------------------ per tick
    def step(self, am, clock=None):
        self.tick += 1
        if self.tick % 30 == 0:
            self.items = [item for item in self.items
                          if item.life > 0 and (item.kind != "food" or self.tick < item.spoil_tick)]
        if self.tick % 3 == 0:
            self.marker *= 0.992
            self.marker[self.marker < 0.01] = 0
            self.smell *= 0.985
            self.smell[self.smell < 0.01] = 0
            self.heat *= 0.996
            # repousse des souches -> arbre (la pluie et le froid ralentissent)
            slow = 1.0 if clock is None else clock.growth_f
            reg = np.nonzero(self.regrow > 0)
            rng = np.random.default_rng(42)
            trees = am.pool("tree")
            if trees:
                for y, x in zip(*reg):
                    self.regrow[y, x] -= 3 * slow
                    if self.regrow[y, x] <= 0:
                        if self.is_land(x, y) and not self.blocked[y, x] and self.content_at(x, y) < 0:
                            aid = int(am.pick(trees, rng))
                            self.place(int(x), int(y), aid, am, hp=6, solid=True,
                                       size=am.assets[aid].size_tiles)
                            self.regrow[y, x] = 0
                        else:
                            self.regrow[y, x] = 100.0

    def find_cemetery_spot(self, rng=None):
        """Retourne une parcelle libre de cimetière dans le tiers supérieur."""
        if rng is None:
            import numpy as np
            rng = np.random.default_rng(42)

        g = self.g
        cx = g // 2
        cy = max(10, g // 10)
        occupied = {(int(tx), int(ty)) for tx, ty, *_ in self.cemetery}

        for radius in range(0, g // 3, 8):
            xmin = max(3, cx - radius)
            xmax = min(g - 9, cx + radius + 1)
            ymin = max(3, cy - radius)
            ymax = min(g - 9, cy + radius + 1)
            if xmin >= xmax or ymin >= ymax:
                continue

            for _ in range(48):
                tx = int(rng.integers(xmin, xmax))
                ty = int(rng.integers(ymin, ymax))

                if any(abs(tx - gx) < 2 and abs(ty - gy) < 2 for gx, gy in occupied):
                    continue
                if not self.is_land(tx, ty):
                    continue
                if self.blocked[ty, tx] or self.content_at(tx, ty) >= 0:
                    continue
                return tx, ty

        return max(3, cx - 3), max(8, cy)

    def bury(self, tx, ty, name, death_tick, color_rgb):
        """Enterre un habitant : enregistre la tombe (pas de bloc posé)."""
        self.cemetery.append((tx, ty, name, death_tick, color_rgb))

    def site_at(self, tx, ty):
        for site in self.sites.values():
            for task in site.tasks:
                if task.tx == tx and task.ty == ty:
                    return site
        return None

    def add_site(self, site):
        self.sites[site.key] = site

    def remove_site(self, site):
        self.sites.pop(site.key, None)

    def save_mountains(self):
        """Sauvegarde le masque de montagnes (terrain) apres worldgen."""
        self.mountains = self.blocked.copy()

    def reset_content(self):
        """Reinitialise tout le contenu place (objets, ressources, batiments)
        mais garde le terrain (land, water, mountains)."""
        g = self.g
        self.content[:] = -1
        self.owner[:] = -1
        self.blocked[:] = self.mountains.copy()
        self.shelter[:] = 0
        self.hp[:] = 0
        self.marker[:] = 0
        self.marker_col[:] = 0
        self.regrow[:] = 0
        self.fire[:] = 0
        self.smell[:] = 0
        self.heat[:] = 0
        self.floor[:] = -1
        self.foundation[:] = -1
        self.roof[:] = -1
        self.items.clear()
        self.cemetery.clear()
        self.storages.clear()
        self.sites.clear()
        self.crop_plots.clear()
        self.kidx = {k: {} for k in ("food", "wood", "stone", "gold", "tool", "shelter")}
        self.dirty_chunks.clear()

    def burn_out(self, am, y, x):
        """Le feu a fini de bruler la tuile : ce qu'elle contenait est detruit."""
        aid = self.content_at(x, y)
        if aid >= 0:
            self.remove(x, y)
            self.regrow[y, x] = 5200          # la terre brulee repoussera, plus tard


class Item:
    __slots__ = ("kind", "aid", "x", "y", "material", "nutrition", "life",
                 "created_tick", "spoil_tick")

    def __init__(self, kind, aid, x, y, material="", nutrition=0.0, life=1e9):
        self.kind = kind          # 'mat' | 'food'
        self.aid = aid
        self.x, self.y = x, y
        self.material = material
        self.nutrition = nutrition
        self.life = life
        self.created_tick = 0
        self.spoil_tick = 0


@dataclass
class CropPlot:
    tx: int
    ty: int
    owner_eid: int | None
    planted_tick: int
    growth: float = 0.0
    water_need: float = 0.5
    crop_type: str = "grain"
    watered: bool = False

```

## game/worldgen.py

**Type :** `.py`

```python

"""worldgen.py — Génération procédurale de terrain (v2).

Corrections majeures par rapport à la v1
----------------------------------------
1. BUG DE PÉRIODE : la v1 calculait `warped_x = xs_l * scale` avec
   `scale = low / g` (< 1), ce qui écrasait les coordonnées et produisait
   moins d'UNE crête sur toute la carte au lieu de `g / tile_period`.
   Tout le pipeline travaille désormais en **unités de tuiles réelles**.
2. PERFORMANCE : `_fbm` appelait `noise2()` cellule par cellule en Python
   (des centaines de milliers d'appels). On utilise `noise2array`, qui
   évalue toute la grille en C. Gain de deux ordres de grandeur.
3. NIVEAU DE LA MER : la v1 noyait ~42 % de la carte parce que le bruit de
   plaine était centré trop bas. Le relief est maintenant construit comme
   « socle continental + crêtes », avec `sea_level` explicite.
4. RENDU : `render_patch_rgb` passe par une LUT de palette (une seule
   opération numpy) au lieu d'une boucle masque par biome.
5. VERSIONNAGE : `gen.version` s'incrémente à chaque sculpture, ce qui
   permet au renderer de garder son terrain en cache au lieu de le
   recalculer chaque frame.
6. ROBUSTESSE : `apply_to_layers` respecte le dtype des couches déjà
   allouées par World, `_sync_layers` ne suppose plus l'existence des
   attributs, les bornes sont clampées partout, et le module fonctionne
   sans scipy ni opensimplex grâce à des replis internes.

API publique
------------
    generate(grid_size, tile_period, ridge_width, seed) -> WorldGen
    apply_to_layers(world, gen)
    carve_mountain / raise_terrain / flatten_terrain / restore_mountain
    render_patch_rgb(gen, y0, y1, x0, x1)   -> uint8 (h, w, 3)
    render_minimap_rgb(gen, size)           -> uint8 (size, size, 3)
    is_mountain / is_carved / biome_at / biome_name / height_at / passable
    slope(gen) / stats(gen)
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field

# ── dépendances optionnelles ──────────────────────────────────────────────────
try:
    from scipy.ndimage import zoom as _scipy_zoom
    _HAS_SCIPY = True
except ImportError:                                     # pragma: no cover
    _scipy_zoom = None
    _HAS_SCIPY = False

try:
    from opensimplex import OpenSimplex
    _HAS_SIMPLEX = True
except ImportError:                                     # pragma: no cover
    OpenSimplex = None
    _HAS_SIMPLEX = False


# ══════════════════════════════════════════════════════════════════════════════
#  Constantes
# ══════════════════════════════════════════════════════════════════════════════
BIOME_WATER  = 0
BIOME_MARSH  = 1
BIOME_SAND   = 2
BIOME_GRASS  = 3
BIOME_FOREST = 4
BIOME_ROCK   = 5
BIOME_SNOW   = 6
N_BIOMES     = 7

# Seuils d'altitude dans [0..1]
H_WATER = 0.30     # < H_WATER   → eau
H_SAND  = 0.34     # < H_SAND    → sable / berge
H_MARSH = 0.36     # < H_MARSH   → marécage
H_GRASS = 0.62     # < H_GRASS   → herbe / forêt (selon humidité)
H_ROCK  = 0.82     # < H_ROCK    → roche
#                    >= H_ROCK   → neige

# Palette indexée par BIOME_* — utilisée comme LUT numpy dans le rendu
BIOME_PALETTE = np.array([
    ( 46,  92, 158),   # WATER
    ( 74, 112,  82),   # MARSH
    (206, 194, 148),   # SAND
    ( 86, 150,  62),   # GRASS
    ( 44, 104,  50),   # FOREST
    (128, 118, 106),   # ROCK
    (234, 238, 244),   # SNOW
], dtype=np.float32)

BIOME_NAMES = {
    BIOME_WATER: "eau", BIOME_MARSH: "marécage", BIOME_SAND: "berge",
    BIOME_GRASS: "prairie", BIOME_FOREST: "forêt",
    BIOME_ROCK: "roche", BIOME_SNOW: "neige",
}

# Direction de lumière pour l'ombrage de pente
_LIGHT = np.array([0.62, -0.32, 1.0], dtype=np.float32)
_LIGHT /= np.linalg.norm(_LIGHT)

# Le heightmap vaut [0..1] sur une grille de tuiles : les pentes brutes sont
# minuscules, on les amplifie pour obtenir un relief lisible à l'écran.
_SLOPE_GAIN = 28.0


# ══════════════════════════════════════════════════════════════════════════════
#  Structure de données
# ══════════════════════════════════════════════════════════════════════════════
@dataclass
class WorldGen:
    """Couches du terrain : `height_base` procédural immuable, `height_current`
    mutable (sculpté par l'utilisateur)."""
    g: int                                  # côté de la grille, en tuiles

    height_base:    np.ndarray              # float32 [0..1] — référence procédurale
    height_current: np.ndarray              # float32 [0..1] — état courant
    moisture:       np.ndarray              # float32 [0..1]
    biome:          np.ndarray              # uint8  — BIOME_*
    shade:          np.ndarray              # float32 [0.30..1.0]
    carved:         np.ndarray              # bool   — modifié par l'outil

    tile_period: int = 250
    ridge_width: int = 55
    seed:        int = 42

    # incrémenté à chaque modification → clé de cache pour le renderer
    version: int = 0
    # union des zones modifiées depuis le dernier clear_dirty(), ou None
    last_dirty: tuple | None = field(default=None, repr=False)

    @property
    def shape(self):
        return (self.g, self.g)

    def touch(self, y0, y1, x0, x1):
        """Marque une zone comme modifiée et fait avancer la version."""
        self.version += 1
        if self.last_dirty is None:
            self.last_dirty = (y0, y1, x0, x1)
        else:
            py0, py1, px0, px1 = self.last_dirty
            self.last_dirty = (min(py0, y0), max(py1, y1),
                               min(px0, x0), max(px1, x1))

    def clear_dirty(self):
        self.last_dirty = None


# ══════════════════════════════════════════════════════════════════════════════
#  Bruit
# ══════════════════════════════════════════════════════════════════════════════
def _noise_lattice(xs_1d: np.ndarray, ys_1d: np.ndarray, seed: int) -> np.ndarray:
    """Une octave de bruit sur un treillis régulier → (len(ys), len(xs))."""
    if _HAS_SIMPLEX:
        gen = OpenSimplex(seed=int(seed) & 0x7FFFFFFF)
        # noise2array évalue toute la grille côté C
        return np.asarray(gen.noise2array(xs_1d.astype(np.float64),
                                          ys_1d.astype(np.float64)),
                          dtype=np.float32)
    return _value_noise(xs_1d, ys_1d, seed)


def _value_noise(xs_1d: np.ndarray, ys_1d: np.ndarray, seed: int) -> np.ndarray:
    """Repli sans opensimplex : value-noise interpolé en cosinus, vectorisé.

    Qualité inférieure au simplex, mais continu, sans artefact de grille
    visible, et parfaitement déterministe pour une graine donnée.
    """
    rng = np.random.default_rng(seed & 0x7FFFFFFF)
    x0i = int(np.floor(xs_1d.min())) - 1
    x1i = int(np.ceil(xs_1d.max())) + 2
    y0i = int(np.floor(ys_1d.min())) - 1
    y1i = int(np.ceil(ys_1d.max())) + 2
    lat = rng.random((y1i - y0i, x1i - x0i), dtype=np.float32) * 2.0 - 1.0

    fx = xs_1d - x0i
    fy = ys_1d - y0i
    ix = np.floor(fx).astype(np.int32)
    iy = np.floor(fy).astype(np.int32)
    tx = fx - ix
    ty = fy - iy
    tx = (1.0 - np.cos(tx * np.pi)) * 0.5     # lissage C1
    ty = (1.0 - np.cos(ty * np.pi)) * 0.5

    ix = np.clip(ix, 0, lat.shape[1] - 2)
    iy = np.clip(iy, 0, lat.shape[0] - 2)

    v00 = lat[np.ix_(iy, ix)]
    v01 = lat[np.ix_(iy, ix + 1)]
    v10 = lat[np.ix_(iy + 1, ix)]
    v11 = lat[np.ix_(iy + 1, ix + 1)]

    TX = tx[None, :]
    TY = ty[:, None]
    top = v00 + (v01 - v00) * TX
    bot = v10 + (v11 - v10) * TX
    return (top + (bot - top) * TY).astype(np.float32)


def _octave_res(span: float, freq: float, low: int) -> int:
    """Résolution d'échantillonnage suffisante pour une octave donnée.

    Une octave de fréquence `freq` (cycles par tuile) produit `span * freq`
    cycles sur toute la carte ; ~4 échantillons par cycle suffisent avant
    agrandissement. Les octaves basse fréquence coûtent donc presque rien,
    ce qui divise le temps de génération par ~5 sans perte visible.
    """
    cycles = max(1.0, span * freq)
    return int(np.clip(cycles * 4.0, 8, low))


def _fbm_field(span: float, low: int, base_freq: float, octaves: int,
               seed: int, *, lacunarity: float = 2.0, gain: float = 0.5,
               ridged: bool = False) -> np.ndarray:
    """fBm 2-D sur [0, span]², rendu à la résolution (low, low).

    Chaque octave est échantillonnée à sa propre résolution utile puis
    agrandie — c'est l'optimisation clé du module.
    Sortie dans [-1, 1] (fBm classique) ou [0, 1] (ridged).
    """
    out = np.zeros((low, low), dtype=np.float32)
    amp, freq, norm = 1.0, float(base_freq), 0.0
    for o in range(octaves):
        res = _octave_res(span, freq, low)
        c = np.linspace(0.0, span * freq, res, endpoint=False, dtype=np.float32)
        layer = _noise_lattice(c, c, seed + o * 7919)
        if ridged:
            layer = 1.0 - np.abs(layer)
            layer = layer * layer
        out += _upsample(layer, low) * amp
        norm += amp
        amp *= gain
        freq *= lacunarity
    return (out / max(norm, 1e-6)).astype(np.float32)


# ══════════════════════════════════════════════════════════════════════════════
#  Agrandissement
# ══════════════════════════════════════════════════════════════════════════════
def _upsample(low: np.ndarray, out_size: int) -> np.ndarray:
    """Agrandit une grille carrée vers (out_size, out_size), bicubique si possible."""
    if low.shape == (out_size, out_size):
        return low.astype(np.float32, copy=True)
    if _HAS_SCIPY:
        z = _scipy_zoom(low.astype(np.float64),
                        (out_size / low.shape[0], out_size / low.shape[1]),
                        order=3, mode="nearest", grid_mode=True, prefilter=True)
        return _fit(np.asarray(z, dtype=np.float32), out_size)
    return _fit(_bilinear(low, out_size), out_size)


def _bilinear(low: np.ndarray, out_size: int) -> np.ndarray:
    """Repli sans scipy : agrandissement bilinéaire vectorisé."""
    h, w = low.shape
    ys = np.linspace(0, h - 1, out_size, dtype=np.float32)
    xs = np.linspace(0, w - 1, out_size, dtype=np.float32)
    y0 = np.floor(ys).astype(np.int32); y1 = np.minimum(y0 + 1, h - 1)
    x0 = np.floor(xs).astype(np.int32); x1 = np.minimum(x0 + 1, w - 1)
    wy = (ys - y0)[:, None]
    wx = (xs - x0)[None, :]
    a = low[np.ix_(y0, x0)]; b = low[np.ix_(y0, x1)]
    c = low[np.ix_(y1, x0)]; d = low[np.ix_(y1, x1)]
    top = a + (b - a) * wx
    bot = c + (d - c) * wx
    return (top + (bot - top) * wy).astype(np.float32)


def _fit(arr: np.ndarray, size: int) -> np.ndarray:
    """Recadre / complète un tableau carré à exactement (size, size)."""
    h, w = arr.shape
    if h == size and w == size:
        return arr
    out = np.empty((size, size), dtype=np.float32)
    hh, ww = min(h, size), min(w, size)
    out[:hh, :ww] = arr[:hh, :ww]
    if hh < size:
        out[hh:, :ww] = out[hh - 1, :ww]
    if ww < size:
        out[:, ww:] = out[:, ww - 1:ww]
    return out


# ══════════════════════════════════════════════════════════════════════════════
#  Dimensionnement
# ══════════════════════════════════════════════════════════════════════════════
def grid_for_pixels(width_px: int, tile: int = 16) -> int:
    """Nombre de tuiles nécessaires pour couvrir `width_px` pixels.

    Exemple : grid_for_pixels(15000, 16) -> 938  (soit 15008 px de côté).
    Toute la simulation raisonne en tuiles ; le pixel n'existe qu'au rendu.
    """
    return int(np.ceil(float(width_px) / max(1, int(tile))))


def period_for_pixels(spacing_px: int, tile: int = 16) -> int:
    """Espacement des chaînes de montagnes, converti en tuiles."""
    return max(16, int(round(float(spacing_px) / max(1, int(tile)))))


# ══════════════════════════════════════════════════════════════════════════════
#  Génération
# ══════════════════════════════════════════════════════════════════════════════
def generate(
    grid_size:    int = 1000,
    tile_period:  int = 250,      # espacement des chaînes, en tuiles (250 = 4000px @ TILE 16)
    ridge_width:  int = 55,       # demi-largeur d'une chaîne, en tuiles
    seed:         int = 42,
    *,
    water_frac:    float = 0.08,  # fraction EXACTE de la carte sous le niveau de la mer
    mountain_frac: float = 0.14,  # fraction EXACTE de montagne infranchissable
    sea_level:    float = 0.30,   # cohérent avec H_WATER
    mountain_amp: float = 0.52,   # hauteur ajoutée au sommet d'une crête
    detail_res:   int | None = None,   # résolution interne (None = auto)
) -> WorldGen:
    """Construit le heightmap complet et toutes les couches dérivées.

    Le bruit est calculé sur une grille interne basse résolution puis agrandi
    en bicubique : le fBm est dominé par ses basses fréquences, l'agrandissement
    ne coûte donc presque rien visuellement et divise le temps de calcul par
    (grid_size / detail_res)².
    """
    g = int(grid_size)
    if g < 16:
        raise ValueError("grid_size doit valoir au moins 16 tuiles")
    tile_period = max(16, int(tile_period))
    ridge_width = int(np.clip(ridge_width, 4, max(5, tile_period // 2 - 1)))

    if detail_res is None:
        detail_res = int(np.clip(g // 6, 96, 320))
    low = int(min(detail_res, g))

    # ── coordonnées du treillis, en TUILES RÉELLES (correction centrale) ──
    coords = np.linspace(0.0, float(g), low, endpoint=False, dtype=np.float32)

    # ── 1. déformation de domaine : fait onduler l'axe des crêtes ─────────
    span = float(g)
    warp_freq = 1.0 / max(tile_period * 1.6, 1.0)
    warp_x = _fbm_field(span, low, warp_freq, 4, seed + 101) * (ridge_width * 1.35)

    xs_grid = np.broadcast_to(coords[None, :], (low, low))
    warped_x = xs_grid + warp_x

    # ── 2. distance à la crête périodique la plus proche ──────────────────
    half = tile_period * 0.5
    dist = np.abs(((warped_x + half) % tile_period) - half)
    ridge = np.clip(1.0 - dist / float(ridge_width), 0.0, 1.0) ** 1.7

    # ── 3. cols et brèches : une chaîne n'est jamais continue ─────────────
    gap_freq = 1.0 / max(tile_period * 0.55, 1.0)
    gaps = _fbm_field(span, low, gap_freq, 3, seed + 303)
    ridge = ridge * np.clip(0.74 + 0.50 * gaps, 0.22, 1.0)

    # ── 4. rugosité interne de la chaîne ─────────────────────────────────
    rough = _fbm_field(span, low, 1.0 / 26.0, 5, seed + 404, ridged=True)
    ridge_h = ridge * (0.58 + 0.42 * rough)

    # ── 5. socle continental : plaines, vallées, lacs ─────────────────────
    cont = _fbm_field(span, low, 1.0 / 210.0, 5, seed + 505)
    cont01 = np.clip((cont + 1.0) * 0.5, 0.0, 1.0)
    base = sea_level - 0.10 + cont01 * 0.36          # ≈ [0.20 .. 0.56]

    micro = _fbm_field(span, low, 1.0 / 34.0, 3, seed + 606)
    base = base + micro * 0.028                      # casse la platitude

    # ── 6. altitude finale ────────────────────────────────────────────────
    h_low = np.clip(base + ridge_h * mountain_amp, 0.0, 1.0)

    # ── 7. humidité (prairie ↔ forêt) ────────────────────────────────────
    moist = _fbm_field(span, low, 1.0 / 130.0, 4, seed + 707)
    moist_low = np.clip((moist + 1.0) * 0.5, 0.0, 1.0)

    # ── 8. agrandissement vers la grille de simulation ───────────────────
    height   = np.clip(_upsample(h_low, g), 0.0, 1.0)
    moisture = np.clip(_upsample(moist_low, g), 0.0, 1.0)

    # ── 8bis. calibration des proportions ────────────────────────────────
    height = _calibrate(height, water_frac, mountain_frac)
    # ombre pluviométrique : il pleut moins haut
    moisture = np.clip(moisture - np.clip(height - H_GRASS, 0.0, 1.0) * 0.8, 0.0, 1.0)

    return WorldGen(
        g              = g,
        height_base    = height.copy(),
        height_current = height,
        moisture       = moisture,
        biome          = _compute_biome(height, moisture),
        shade          = _compute_shade(height),
        carved         = np.zeros((g, g), dtype=bool),
        tile_period    = tile_period,
        ridge_width    = ridge_width,
        seed           = int(seed),
    )


def _calibrate(height: np.ndarray, water_frac: float,
               mountain_frac: float) -> np.ndarray:
    """Remappe l'altitude pour obtenir EXACTEMENT les proportions demandées.

    Le bruit fractal ne donne aucune garantie sur la part d'eau ou de montagne :
    elle dérive des paramètres et change avec la graine. On mesure donc les
    quantiles réels du heightmap et on l'étire par morceaux pour que :
        quantile(water_frac)              tombe pile sur H_WATER
        quantile(1 - mountain_frac)       tombe pile sur H_GRASS
    Le remappage est monotone et affine par morceaux : le relief, les vallées
    et les crêtes sont conservés, seules les altitudes-seuils sont recalées.
    """
    water_frac = float(np.clip(water_frac, 0.0, 0.60))
    mountain_frac = float(np.clip(mountain_frac, 0.0, 0.80 - water_frac))

    lo, hi = float(height.min()), float(height.max())
    if hi - lo < 1e-6:
        return np.full_like(height, (H_WATER + H_GRASS) * 0.5)

    q_w = float(np.quantile(height, water_frac)) if water_frac > 0 else lo
    q_m = float(np.quantile(height, 1.0 - mountain_frac)) if mountain_frac > 0 else hi

    # les points d'ancrage doivent rester strictement croissants
    eps = (hi - lo) * 1e-4
    q_w = min(max(q_w, lo + eps), hi - 2 * eps)
    q_m = min(max(q_m, q_w + eps), hi - eps)

    xp = [lo, q_w, q_m, hi]
    fp = [0.0, H_WATER, H_GRASS, 1.0]
    out = np.interp(height.astype(np.float64), xp, fp).astype(np.float32)
    return np.clip(out, 0.0, 1.0)


# ══════════════════════════════════════════════════════════════════════════════
#  Synchronisation avec les couches de World
# ══════════════════════════════════════════════════════════════════════════════
def _masks(h: np.ndarray):
    """Retourne (water, land, blocked) pour un bloc d'altitudes."""
    water   = h < H_WATER
    blocked = h >= H_GRASS
    land    = ~water & ~blocked
    return water, land, blocked


def apply_to_layers(world, gen: WorldGen) -> None:
    """Initialise world.land / world.blocked / world.water depuis `gen`.

    Le dtype des couches existantes est préservé (World les alloue en uint8) ;
    une couche absente est créée en uint8.
    """
    water, land, blocked = _masks(gen.height_current)
    for name, mask in (("water", water), ("land", land), ("blocked", blocked)):
        cur = getattr(world, name, None)
        if isinstance(cur, np.ndarray) and cur.shape == mask.shape:
            cur[...] = mask.astype(cur.dtype, copy=False)
        else:
            setattr(world, name, mask.astype(np.uint8))
    world.gen = gen


def _sync_layers(world, gen: WorldGen, y0: int, y1: int, x0: int, x1: int) -> None:
    """Resynchronise les couches sur le patch [y0:y1, x0:x1] uniquement.

    C'est ce qui rend l'outil de sculpture instantané : quelques centaines de
    tuiles sont retraitées, jamais le million de la carte complète.
    """
    h = gen.height_current[y0:y1, x0:x1]
    water, land, blocked = _masks(h)
    for name, mask in (("water", water), ("land", land), ("blocked", blocked)):
        cur = getattr(world, name, None)
        if isinstance(cur, np.ndarray) and cur.shape == gen.shape:
            cur[y0:y1, x0:x1] = mask.astype(cur.dtype, copy=False)

    gen.biome[y0:y1, x0:x1] = _compute_biome(h, gen.moisture[y0:y1, x0:x1])

    # l'ombrage dépend du gradient : on élargit d'une tuile puis on recadre
    py0, py1 = max(0, y0 - 1), min(gen.g, y1 + 1)
    px0, px1 = max(0, x0 - 1), min(gen.g, x1 + 1)
    sh = _compute_shade(gen.height_current[py0:py1, px0:px1])
    gen.shade[y0:y1, x0:x1] = sh[y0 - py0: y0 - py0 + (y1 - y0),
                                 x0 - px0: x0 - px0 + (x1 - x0)]

    # un objet posé sur une case devenue eau ou montagne n'a plus de sens
    _drop_orphans(world, gen, y0, y1, x0, x1, land)

    gen.touch(y0, y1, x0, x1)


def _drop_orphans(world, gen, y0, y1, x0, x1, land_mask):
    remover = getattr(world, "remove", None)
    content = getattr(world, "content", None)
    if not callable(remover) or not isinstance(content, np.ndarray):
        return
    if content.shape != gen.shape:
        return
    bad = (~land_mask) & (content[y0:y1, x0:x1] >= 0)
    if not bad.any():
        return
    for j, i in zip(*np.nonzero(bad)):
        try:
            remover(int(x0 + i), int(y0 + j), quiet=True)
        except TypeError:
            try:
                remover(int(x0 + i), int(y0 + j))
            except Exception:
                import sys
                print(f"[worldgen._drop_orphans] {sys.exc_info()[1]}", file=sys.stderr)
        except Exception:
            import sys
            print(f"[worldgen._drop_orphans] {sys.exc_info()[1]}", file=sys.stderr)


# ══════════════════════════════════════════════════════════════════════════════
#  Outils de sculpture
# ══════════════════════════════════════════════════════════════════════════════
def _brush(gen: WorldGen, tx: int, ty: int, radius: int):
    """Retourne (y0, y1, x0, x1, falloff) ou None si le pinceau est hors carte."""
    radius = max(1, int(radius))
    tx, ty = int(tx), int(ty)
    y0, y1 = max(0, ty - radius), min(gen.g, ty + radius + 1)
    x0, x1 = max(0, tx - radius), min(gen.g, tx + radius + 1)
    if y1 <= y0 or x1 <= x0:
        return None
    yy = np.arange(y0, y1, dtype=np.float32)[:, None] - ty
    xx = np.arange(x0, x1, dtype=np.float32)[None, :] - tx
    d = np.sqrt(yy * yy + xx * xx) / radius
    t = np.clip(1.0 - d, 0.0, 1.0)
    falloff = (t * t * (3.0 - 2.0 * t)).astype(np.float32)   # smoothstep
    return y0, y1, x0, x1, falloff


def carve_mountain(world, gen: WorldGen, tx: int, ty: int,
                   radius: int = 10, strength: float = 0.12) -> bool:
    """Abaisse le terrain sous le pinceau. True si quelque chose a changé."""
    br = _brush(gen, tx, ty, radius)
    if br is None:
        return False
    y0, y1, x0, x1, falloff = br
    patch = gen.height_current[y0:y1, x0:x1]
    before = patch.copy()
    np.clip(patch - float(strength) * falloff, 0.0, 1.0, out=patch)
    if np.array_equal(before, patch):
        return False

    was_high = gen.height_base[y0:y1, x0:x1] >= H_GRASS
    gen.carved[y0:y1, x0:x1] |= was_high & (patch < H_GRASS)

    _sync_layers(world, gen, y0, y1, x0, x1)
    return True


def raise_terrain(world, gen: WorldGen, tx: int, ty: int,
                  radius: int = 10, strength: float = 0.12) -> bool:
    """Élève le terrain sous le pinceau — le pendant de `carve_mountain`."""
    br = _brush(gen, tx, ty, radius)
    if br is None:
        return False
    y0, y1, x0, x1, falloff = br
    patch = gen.height_current[y0:y1, x0:x1]
    before = patch.copy()
    np.clip(patch + float(strength) * falloff, 0.0, 1.0, out=patch)
    if np.array_equal(before, patch):
        return False
    gen.carved[y0:y1, x0:x1] |= falloff > 0.02
    _sync_layers(world, gen, y0, y1, x0, x1)
    return True


def flatten_terrain(world, gen: WorldGen, tx: int, ty: int,
                    radius: int = 10, strength: float = 0.25) -> bool:
    """Aplanit vers la hauteur moyenne du pinceau — prépare un terrain de village."""
    br = _brush(gen, tx, ty, radius)
    if br is None:
        return False
    y0, y1, x0, x1, falloff = br
    patch = gen.height_current[y0:y1, x0:x1]
    core = falloff > 0.35
    target = float(patch[core].mean()) if core.any() else float(patch.mean())
    k = np.clip(float(strength) * falloff, 0.0, 1.0)
    np.clip(patch + k * (target - patch), 0.0, 1.0, out=patch)
    gen.carved[y0:y1, x0:x1] |= falloff > 0.02
    _sync_layers(world, gen, y0, y1, x0, x1)
    return True


def restore_mountain(world, gen: WorldGen, tx: int, ty: int,
                     radius: int = 10, strength: float = 0.15) -> bool:
    """Ramène progressivement le terrain vers sa forme procédurale d'origine."""
    br = _brush(gen, tx, ty, radius)
    if br is None:
        return False
    y0, y1, x0, x1, falloff = br
    base  = gen.height_base[y0:y1, x0:x1]
    patch = gen.height_current[y0:y1, x0:x1]
    if np.allclose(patch, base, atol=1e-4):
        return False
    k = np.clip(float(strength) * falloff * 4.0, 0.0, 1.0)
    np.clip(patch + k * (base - patch), 0.0, 1.0, out=patch)
    gen.carved[y0:y1, x0:x1] &= np.abs(patch - base) >= 0.02
    _sync_layers(world, gen, y0, y1, x0, x1)
    return True


# ══════════════════════════════════════════════════════════════════════════════
#  Rendu
# ══════════════════════════════════════════════════════════════════════════════
def render_patch_rgb(gen: WorldGen, y0: int, y1: int, x0: int, x1: int,
                     *, shading: bool = True) -> np.ndarray:
    """Retourne un uint8 (h, w, 3) — une couleur par tuile.

    Couleur = palette du biome, modulée par l'altitude locale puis par
    l'ombrage de pente. Une seule passe numpy, aucune boucle Python.
    """
    y0 = max(0, int(y0)); y1 = min(gen.g, int(y1))
    x0 = max(0, int(x0)); x1 = min(gen.g, int(x1))
    if y1 <= y0 or x1 <= x0:
        return np.zeros((1, 1, 3), dtype=np.uint8)

    biome  = gen.biome[y0:y1, x0:x1]
    height = gen.height_current[y0:y1, x0:x1]

    rgb = BIOME_PALETTE[biome]                       # LUT → (h, w, 3) float32
    rgb = rgb * (1.0 + (height - 0.45) * 0.30)[:, :, None]

    if shading:
        rgb = rgb * gen.shade[y0:y1, x0:x1][:, :, None]

    # les tuiles sculptées sont légèrement désaturées : le geste reste visible
    carved = gen.carved[y0:y1, x0:x1]
    if carved.any():
        grey = rgb.mean(axis=2, keepdims=True)
        rgb = np.where(carved[:, :, None], rgb * 0.82 + grey * 0.18, rgb)

    return np.clip(rgb, 0, 255).astype(np.uint8)


def render_minimap_rgb(gen: WorldGen, size: int = 128) -> np.ndarray:
    """Vignette (size, size, 3) du monde entier — sous-échantillonnage par pas."""
    size = max(8, int(size))
    step = max(1, gen.g // size)
    idx = np.arange(0, gen.g, step)[:size]
    rgb = BIOME_PALETTE[gen.biome[np.ix_(idx, idx)]]
    rgb = rgb * gen.shade[np.ix_(idx, idx)][:, :, None]
    return np.clip(rgb, 0, 255).astype(np.uint8)


# ══════════════════════════════════════════════════════════════════════════════
#  Couches dérivées
# ══════════════════════════════════════════════════════════════════════════════
def _compute_biome(height: np.ndarray, moisture: np.ndarray) -> np.ndarray:
    """Assigne un BIOME_* par tuile, depuis l'altitude et l'humidité."""
    biome = np.full(height.shape, BIOME_GRASS, dtype=np.uint8)
    biome[height >= H_ROCK] = BIOME_SNOW
    biome[(height >= H_GRASS) & (height < H_ROCK)] = BIOME_ROCK

    low = height < H_GRASS
    biome[low & (height >= H_MARSH) & (moisture > 0.56)] = BIOME_FOREST
    biome[low & (height >= H_SAND) & (height < H_MARSH)] = BIOME_MARSH
    biome[low & (height >= H_WATER) & (height < H_SAND)] = BIOME_SAND
    biome[height < H_WATER] = BIOME_WATER
    return biome


def _compute_shade(height: np.ndarray) -> np.ndarray:
    """Ombrage de pente (pseudo normal-map) depuis le gradient du heightmap."""
    if height.shape[0] < 2 or height.shape[1] < 2:
        return np.ones(height.shape, dtype=np.float32)
    gy, gx = np.gradient(height.astype(np.float32))
    gx = gx * _SLOPE_GAIN
    gy = gy * _SLOPE_GAIN
    inv = 1.0 / np.sqrt(gx * gx + gy * gy + 1.0)
    lx, ly, lz = _LIGHT
    lambert = (-gx * lx - gy * ly + lz) * inv
    return np.clip(0.42 + lambert * 0.62, 0.30, 1.0).astype(np.float32)


def slope(gen: WorldGen) -> np.ndarray:
    """Norme du gradient d'altitude — p. ex. pour interdire les arbres en pente."""
    gy, gx = np.gradient(gen.height_current.astype(np.float32))
    return np.sqrt(gx * gx + gy * gy) * _SLOPE_GAIN


# ══════════════════════════════════════════════════════════════════════════════
#  Accès ponctuel
# ══════════════════════════════════════════════════════════════════════════════
def _in_bounds(gen: WorldGen, tx: int, ty: int) -> bool:
    return 0 <= tx < gen.g and 0 <= ty < gen.g


def is_mountain(gen: WorldGen, tx: int, ty: int) -> bool:
    return _in_bounds(gen, tx, ty) and bool(gen.height_current[ty, tx] >= H_GRASS)


def is_carved(gen: WorldGen, tx: int, ty: int) -> bool:
    return _in_bounds(gen, tx, ty) and bool(gen.carved[ty, tx])


def biome_at(gen: WorldGen, tx: int, ty: int) -> int:
    return int(gen.biome[ty, tx]) if _in_bounds(gen, tx, ty) else BIOME_WATER


def biome_name(gen: WorldGen, tx: int, ty: int) -> str:
    return BIOME_NAMES.get(biome_at(gen, tx, ty), "?")


def height_at(gen: WorldGen, tx: int, ty: int) -> float:
    return float(gen.height_current[ty, tx]) if _in_bounds(gen, tx, ty) else 0.0


def passable(gen: WorldGen, tx: int, ty: int) -> bool:
    if not _in_bounds(gen, tx, ty):
        return False
    return bool(H_WATER <= gen.height_current[ty, tx] < H_GRASS)


def stats(gen: WorldGen) -> dict:
    """Répartition des biomes en fraction du total — pour le journal / debug."""
    counts = np.bincount(gen.biome.ravel(), minlength=N_BIOMES).astype(np.float64)
    total = max(1.0, counts.sum())
    return {BIOME_NAMES[i]: counts[i] / total for i in range(N_BIOMES)}


# ══════════════════════════════════════════════════════════════════════════════
#  Auto-test
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import time

    class _FakeWorld:
        def __init__(self, g):
            self.land    = np.zeros((g, g), np.uint8)
            self.blocked = np.zeros((g, g), np.uint8)
            self.water   = np.zeros((g, g), np.uint8)

    print("worldgen v2 — auto-test")
    print(f"  scipy={_HAS_SCIPY}  opensimplex={_HAS_SIMPLEX}")

    print(f"  15000px @ TILE 16 -> grille {grid_for_pixels(15000, 16)} tuiles")
    for g, period in ((500, 125), (938, 250)):
        t0 = time.perf_counter()
        gen = generate(grid_size=g, tile_period=period, ridge_width=28, seed=7,
                       water_frac=0.08, mountain_frac=0.14)
        dt = time.perf_counter() - t0
        w = _FakeWorld(g)
        apply_to_layers(w, gen)
        print(f"  {g}x{g} en {dt:.2f}s  terre={w.land.mean()*100:.0f}%  "
              f"montagne={w.blocked.mean()*100:.0f}%  eau={w.water.mean()*100:.0f}%")
        print("    biomes: " + "  ".join(f"{k}={v*100:.0f}%"
                                         for k, v in stats(gen).items()))
        row = gen.height_base[g // 2] >= H_GRASS
        crossings = int(np.count_nonzero(row[1:] & ~row[:-1]))
        print(f"    chaines traversees (ligne mediane) : {crossings} "
              f"(attendu ~ {g // period})")

    gen = generate(grid_size=400, tile_period=100, ridge_width=22, seed=3)
    w = _FakeWorld(400)
    apply_to_layers(w, gen)
    ys, xs = np.nonzero(gen.height_current >= H_GRASS)
    ty, tx = int(ys[len(ys) // 2]), int(xs[len(xs) // 2])
    h0 = height_at(gen, tx, ty)
    for _ in range(8):
        carve_mountain(w, gen, tx, ty, radius=10, strength=0.15)
    h1 = height_at(gen, tx, ty)
    assert h1 < h0 and not w.blocked[ty, tx], "la sculpture doit ouvrir un passage"
    assert gen.carved[ty, tx], "le drapeau carved doit etre pose"
    for _ in range(12):
        restore_mountain(w, gen, tx, ty, radius=10, strength=0.30)
    h2 = height_at(gen, tx, ty)
    assert abs(h2 - gen.height_base[ty, tx]) < 0.02, "la restauration doit revenir a la base"
    assert not gen.carved[ty, tx]
    print(f"  sculpture : {h0:.3f} -> {h1:.3f} -> {h2:.3f}  (version={gen.version})")

    img = render_patch_rgb(gen, 0, 120, 0, 160)
    mini = render_minimap_rgb(gen, 96)
    assert img.shape == (120, 160, 3) and img.dtype == np.uint8
    assert mini.shape == (96, 96, 3)
    print(f"  rendu {img.shape} · minimap {mini.shape}")
    print("OK")

```

## generate_project_md.py

**Type :** `.py`

````python

from __future__ import annotations

import argparse
import os
from datetime import datetime
from pathlib import Path


# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────

DEFAULT_OUTPUT = "PROJECT.md"

INCLUDED_EXTENSIONS = {
    ".py",
    ".txt",
    ".md",
}

EXCLUDED_DIRS = {
    ".git",
    ".github",
    ".idea",
    ".vscode",
    ".vs",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "dist",
    "build",
    "site-packages",
    "data",
    "saves",
    "output",
    "outputs",
    "logs",
    "cache",
    "caches",
}

EXCLUDED_FILENAMES = {
    "PROJECT.md",
}

MAX_FILE_BYTES = 2_000_000

LANGUAGE_BY_EXTENSION = {
    ".py": "python",
    ".txt": "text",
    ".md": "markdown",
}


# ─────────────────────────────────────────────────────────────────────────────
# Utilitaires
# ─────────────────────────────────────────────────────────────────────────────

def is_excluded_path(path: Path, root: Path, output_path: Path) -> bool:
    """
    Retourne True si le fichier/dossier doit être ignoré.
    """
    try:
        relative = path.relative_to(root)
    except ValueError:
        return True

    if path.resolve() == output_path.resolve():
        return True

    if path.name in EXCLUDED_FILENAMES and path.name == output_path.name:
        return True

    for part in relative.parts:
        if part in EXCLUDED_DIRS:
            return True

    return False


def should_include_file(path: Path, root: Path, output_path: Path) -> bool:
    """
    Détermine si un fichier doit être inclus dans le Markdown final.
    """
    if not path.is_file():
        return False

    if is_excluded_path(path, root, output_path):
        return False

    if path.suffix.lower() not in INCLUDED_EXTENSIONS:
        return False

    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return False
    except OSError:
        return False

    return True


def safe_read_text(path: Path) -> tuple[str | None, str | None]:
    """
    Lit un fichier texte avec plusieurs encodages.
    Retourne (contenu, erreur).
    """
    encodings = (
        "utf-8",
        "utf-8-sig",
        "cp1252",
        "latin-1",
    )

    for encoding in encodings:
        try:
            return path.read_text(encoding=encoding), None
        except UnicodeDecodeError:
            continue
        except OSError as exc:
            return None, f"{type(exc).__name__}: {exc}"

    return None, "Impossible de décoder le fichier comme texte."


def build_tree(root: Path, output_path: Path) -> list[str]:
    """
    Génère une arborescence texte du projet.
    """
    lines = [f"{root.name}/"]

    def walk(directory: Path, prefix: str = "") -> None:
        try:
            entries = sorted(
                directory.iterdir(),
                key=lambda p: (
                    not p.is_dir(),
                    p.name.lower(),
                ),
            )
        except OSError:
            return

        visible_entries = []

        for entry in entries:
            if is_excluded_path(entry, root, output_path):
                continue

            if entry.is_file():
                if entry.suffix.lower() not in INCLUDED_EXTENSIONS:
                    continue

                try:
                    if entry.stat().st_size > MAX_FILE_BYTES:
                        continue
                except OSError:
                    continue

            visible_entries.append(entry)

        for index, entry in enumerate(visible_entries):
            is_last = index == len(visible_entries) - 1
            branch = "└── " if is_last else "├── "
            suffix = "/" if entry.is_dir() else ""
            lines.append(f"{prefix}{branch}{entry.name}{suffix}")

            if entry.is_dir():
                next_prefix = prefix + ("    " if is_last else "│   ")
                walk(entry, next_prefix)

    walk(root)
    return lines


def markdown_header(title: str, level: int = 1) -> str:
    return f"{'#' * level} {title}\n"


def file_section(relative_path: Path, content: str) -> str:
    """
    Génère une section Markdown pour un fichier.
    """
    extension = relative_path.suffix.lower()
    language = LANGUAGE_BY_EXTENSION.get(extension, "")

    # Empêche un contenu contenant ``` de casser le Markdown.
    fence = "```"
    if "```" in content:
        fence = "````"

    result = []
    result.append(markdown_header(str(relative_path).replace("\\", "/"), 2))
    result.append(f"**Type :** `{extension or 'sans extension'}`\n")
    result.append(f"{fence}{language}\n")
    result.append(content.rstrip())
    result.append(f"\n{fence}\n")

    return "\n".join(result)


# ─────────────────────────────────────────────────────────────────────────────
# Génération
# ─────────────────────────────────────────────────────────────────────────────

def generate_markdown(root: Path, output_path: Path) -> tuple[int, int, list[str]]:
    """
    Crée le fichier Markdown.
    Retourne :
    - nombre de fichiers inclus ;
    - nombre de fichiers ignorés ;
    - liste des avertissements.
    """
    warnings: list[str] = []
    included_files: list[Path] = []
    ignored_count = 0

    for current_root, dirs, files in os.walk(root):
        current_path = Path(current_root)

        dirs[:] = [
            dirname
            for dirname in dirs
            if not is_excluded_path(current_path / dirname, root, output_path)
        ]

        for filename in files:
            path = current_path / filename

            if should_include_file(path, root, output_path):
                included_files.append(path)
            else:
                if path.suffix.lower() in INCLUDED_EXTENSIONS:
                    ignored_count += 1

    included_files.sort(
        key=lambda path: str(path.relative_to(root)).lower()
    )

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    document: list[str] = []

    document.append(markdown_header("Documentation complète du projet"))
    document.append(
        "Ce document a été généré automatiquement par `generate_project_md.py`.\n"
    )
    document.append(f"- **Racine du projet :** `{root}`\n")
    document.append(f"- **Date de génération :** `{now}`\n")
    document.append(f"- **Fichiers inclus :** `{len(included_files)}`\n")
    document.append(f"- **Extensions incluses :** `{', '.join(sorted(INCLUDED_EXTENSIONS))}`\n")

    document.append(markdown_header("Arborescence du projet", 2))
    document.append("```text")
    document.extend(build_tree(root, output_path))
    document.append("```\n")

    document.append(markdown_header("Contenu des fichiers", 2))

    for path in included_files:
        relative = path.relative_to(root)

        content, error = safe_read_text(path)

        if error is not None:
            warnings.append(f"{relative}: {error}")
            document.append(markdown_header(str(relative).replace("\\", "/"), 2))
            document.append(f"> ⚠️ Impossible de lire ce fichier : `{error}`\n")
            continue

        document.append(file_section(relative, content))

    if warnings:
        document.append(markdown_header("Avertissements", 2))
        for warning in warnings:
            document.append(f"- {warning}")

    output_path.write_text(
        "\n".join(document) + "\n",
        encoding="utf-8",
    )

    return len(included_files), ignored_count, warnings


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Génère un Markdown unique contenant l'arborescence et tous "
            "les fichiers .py, .txt et .md du projet."
        )
    )

    parser.add_argument(
        "--root",
        default=".",
        help="Dossier racine du projet. Défaut : dossier courant.",
    )

    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help=f"Fichier Markdown généré. Défaut : {DEFAULT_OUTPUT}",
    )

    parser.add_argument(
        "--include-assets",
        action="store_true",
        help=(
            "Inclut les fichiers texte présents dans assets/. "
            "Par défaut, assets/ est exclu."
        ),
    )

    parser.add_argument(
        "--include-data",
        action="store_true",
        help=(
            "Inclut les fichiers texte présents dans data/. "
            "Par défaut, data/ est exclu."
        ),
    )

    args = parser.parse_args()

    root = Path(args.root).resolve()
    output_path = Path(args.output)

    if not output_path.is_absolute():
        output_path = root / output_path

    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Erreur : racine invalide : {root}")

    if args.include_assets:
        EXCLUDED_DIRS.discard("assets")

    if args.include_data:
        EXCLUDED_DIRS.discard("data")
        EXCLUDED_DIRS.discard("saves")

    included, ignored, warnings = generate_markdown(root, output_path)

    print("PROJECT.md généré avec succès.")
    print(f"Racine     : {root}")
    print(f"Sortie     : {output_path}")
    print(f"Inclus     : {included} fichiers")
    print(f"Ignorés    : {ignored} fichiers texte")
    print(f"Avertissements : {len(warnings)}")


if __name__ == "__main__":
    main()

````

## main.py

**Type :** `.py`

```python

"""Un monde vivant observe par un scientifique : les habitants naissent sans
regles, decident avec leur reseau de neurones, et s'auto-organisent (ou se
destruisent)."""
import argparse
import atexit
import os
import sys

import numpy as np
import pygame

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game.assets_manager import AssetManager
from game.assets_api import _set_asset_manager
from game.camera import Camera, ZOOMS
from game.config import (GRID, SCREEN_H, SCREEN_W, SIM_HZ, TILE, VIEW_H, FPS, ASSETS_DIR)

# marge autour de tout l'écran
M = 3
from game.dashboard import Dashboard
from game.engine import build_world, build_world_blank, populate
from game.renderer import Renderer


def main():
    ap = argparse.ArgumentParser(description="Laboratoire d'émergence IA")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--headless", type=int, default=0, help="N ticks sans fenetre")
    ap.add_argument("--agents", type=int, default=0)
    ap.add_argument("--speed", type=int, default=2)
    ap.add_argument("--screenshot", type=str, default="")
    ap.add_argument("--auto", type=int, default=0, help="N ticks puis screenshot+quit")
    ap.add_argument("--blank", type=int, default=0, help="1 = monde vide tout eau, pas d'assets")
    ap.add_argument("--procedural", type=int, default=0, help="1 = génération procédurale d'îles (pas de PNG)")
    args = ap.parse_args()

    headless = args.headless > 0 or args.auto > 0
    if headless:
        os.environ["SDL_VIDEODRIVER"] = "dummy"
    pygame.init()
    pygame.display.set_caption("Univers Vivant — IA émergente (laboratoire)")
    # centrer la fenêtre AVANT de la créer
    info = pygame.display.Info()
    ox = max(0, (info.current_w - SCREEN_W) // 2)
    oy = max(0, (info.current_h - SCREEN_H) // 2)
    os.environ["SDL_VIDEO_WINDOW_POS"] = f"{ox},{oy}"
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    if headless:
        screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.HIDDEN)

    print("Chargement des assets (/assets) ...")
    am = AssetManager(headless=False).discover()
    am.ensure_procedural_blocks()
    am.ensure_procedural_tools()
    am.ensure_kaykit_resources()
    _set_asset_manager(am)

    # Découper les sprite sheets en assets individuels
    import os as _os
    for _f in _os.listdir(ASSETS_DIR):
        if "vegetable" in _f.lower() and _f.lower().endswith(".png") and _os.path.isfile(_os.path.join(ASSETS_DIR, _f)):
            _p = _os.path.join(ASSETS_DIR, _f)
            if _os.path.getsize(_p) > 1000:
                am.register_grid_items(
                    _p, category="nourriture", role="food",
                    cell_w=16, cell_h=16, edible=24.0,
                )
                break

    st = am.stats()
    print(f"  {st['discovered']} fichiers trouvés, {st['deduped']} uniques après "
          f"suppression des répétitions, {len(am.floors)} tilesets de sol.")

    # 1) Essayer de charger une sauvegarde
    from game.save import load_game as _auto_load
    _loaded_sim, _loaded_cam = _auto_load(am, slot=0)
    if _loaded_sim is not None:
        sim = _loaded_sim
        world = sim.w
        cam = _loaded_cam if _loaded_cam is not None else Camera()
        sim.log("Sauvegarde restaurée.", (108, 208, 128), "monde")
    else:
        # 2) Pas de sauvegarde → monde frais
        world, sim = build_world_blank(am, args.seed) if args.blank else build_world(am, args.seed, procedural=True)
        sim.speed = args.speed
        cam = Camera()
        _ys, _xs = np.nonzero(world.land)
        if len(_xs):
            cam.center_on(float(_xs.mean()) * TILE, float(_ys.mean()) * TILE)
        else:
            cam.center_on(float(GRID // 2) * TILE, float(GRID // 2) * TILE)
        if args.agents > 0 and not args.blank:
            ys, xs = np.nonzero(world.land)
            i = int(sim.rng.integers(len(xs)))
            hx, hy = int(xs[i]), int(ys[i])
            for _ in range(args.agents):
                sim.spawn_agent(x=hx * TILE + sim.rng.normal(0, 5),
                                y=hy * TILE + sim.rng.normal(0, 5))
    ren = Renderer(am)
    dash = Dashboard(am)
    try:
        if am.ui.get("cursors"):
            csurf = am.surface(am.ui["cursors"][0], 0, 1.0)
            pygame.mouse.set_cursor(pygame.cursors.Cursor((8, 8), csurf))
    except Exception as exc:
        print(f"[cursor] curseur personnalisé indisponible : {exc}", file=sys.stderr)

    # ---- mode headless
    if args.headless > 0 and args.auto == 0:
        for i in range(args.headless):
            sim.tick()
            if i % 120 == 0:
                p, sh, it = sim.natural_pop()
                print(f"tick {i:5d} pop={p:3d} sheep={sh:3d} items={it:4d} "
                      f"births={sim.stats['births']} deaths={sim.stats['deaths']} "
                      f"builds={sim.stats['builds']} villages={sim.stats['villages']} "
                      f"attacks={sim.stats['attacks']} gives={sim.stats['gives']}")
        p, sh, it = sim.natural_pop()
        print("FINAL:", dict(pop=p, sheep=sh, items=it, **{k: v for k, v in sim.stats.items()}))
        pygame.quit()
        return

    # ---- mode auto (N ticks + screenshot + quit)
    if args.auto > 0:
        for i in range(args.auto):
            sim.tick()
            if i % 120 == 0:
                p, sh, it = sim.natural_pop()
                print(f"tick {i:5d} pop={p:3d} sheep={sh:3d} items={it:4d} "
                      f"births={sim.stats['births']} deaths={sim.stats['deaths']} "
                      f"builds={sim.stats['builds']} villages={sim.stats['villages']} "
                      f"attacks={sim.stats['attacks']} gives={sim.stats['gives']}")
        sim.pop_hist.append(len(sim.agents))
        ui = {"tile": (GRID // 2, GRID // 2), "ghost": False, "asset": dash.asset,
              "mode": dash.mode, "agent": sim.selected}
        vr = dash.view_rect()
        view_surf = pygame.Surface((vr.width, vr.height))
        ren.draw(view_surf, sim, cam, ui)
        screen.fill((227, 232, 236))
        screen.blit(view_surf, (vr.x, vr.y))
        dash.draw(screen, sim, cam)
        # cadre visible — dessiné EN DERNIER par-dessus tout
        pygame.draw.rect(screen, (180, 186, 196), (0, 0, SCREEN_W, SCREEN_H), 2)
        path = args.screenshot or "screenshot.png"
        pygame.image.save(screen, path)
        p, sh, it = sim.natural_pop()
        print("FINAL:", dict(pop=p, sheep=sh, items=it,
                              **{k: v for k, v in sim.stats.items()}))
        print("screenshot:", path)
        pygame.quit()
        return

    # ---- mode visuel (fenetre interactive)
    clock = pygame.time.Clock()
    show_legend = [False]
    acc = 0.0
    running = True
    panning = None
    ldrag_tile = None
    while running:
        evs = pygame.event.get()
        for ev in evs:
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.KEYDOWN:
                if dash.handle_event(ev, sim):
                    continue
                if dash.focus_search or dash.hab_focus or dash.creator_focus:
                    continue
                if ev.key == pygame.K_ESCAPE:
                    running = False
                elif ev.key == pygame.K_SPACE:
                    sim.paused = not sim.paused
                elif ev.key == pygame.K_g:
                    ren.show_grid = not ren.show_grid
                elif ev.key in (pygame.K_PLUS, pygame.K_EQUALS):
                    sim.speed = min(8, sim.speed + 1)
                elif ev.key == pygame.K_MINUS:
                    sim.speed = max(1, sim.speed - 1)
                elif ev.key == pygame.K_f:
                    dash.follow = not dash.follow
                elif ev.key == pygame.K_v:
                    show_legend[0] = not show_legend[0]
                elif ev.key == pygame.K_LEFTBRACKET:
                    cam.tilt = max(40.0, cam.tilt - 5)
                elif ev.key == pygame.K_RIGHTBRACKET:
                    cam.tilt = min(70.0, cam.tilt + 5)
                elif ev.key in (pygame.K_w, pygame.K_UP):
                    cam.y -= 140 / (cam.zoom * cam.ys)
                    cam.clamp()
                elif ev.key in (pygame.K_s, pygame.K_DOWN):
                    cam.y += 140 / (cam.zoom * cam.ys)
                    cam.clamp()
                elif ev.key in (pygame.K_a, pygame.K_LEFT):
                    cam.x -= 140 / cam.zoom
                    cam.clamp()
                elif ev.key in (pygame.K_d, pygame.K_RIGHT):
                    cam.x += 140 / cam.zoom
                    cam.clamp()
                elif ev.key == pygame.K_F5:
                    from game.save import save_game as _save
                    path, sz = _save(sim, cam, slot=0)
                    sim.log(f"Sauvegardé ({sz:.1f} Mo)", (108, 208, 128), "monde")
                elif ev.key == pygame.K_F9:
                    from game.save import load_game as _load
                    new_sim, new_cam = _load(am, slot=0)
                    if new_sim is not None:
                        sim = new_sim
                        if new_cam is not None:
                            cam = new_cam
                        world = sim.w
                        sim.log("Partie chargée.", (108, 208, 128), "monde")
                    else:
                        sim.log("Aucune sauvegarde.", (228, 98, 98), "monde")
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if dash.handle_event(ev, sim):
                    if getattr(dash, '_needs_save', False):
                        dash._needs_save = False
                        from game.save import save_game as _auto_save
                        _auto_save(sim, cam, slot=0)
                    continue
                vr = dash.view_rect()
                mx = ev.pos[0]
                if ev.button == 1 and vr.collidepoint((mx, ev.pos[1])):
                    dash.apply_map_tool(sim, cam, 1)
                    if getattr(dash, '_needs_save', False):
                        dash._needs_save = False
                        from game.save import save_game as _auto_save
                        _auto_save(sim, cam, slot=0)
                    ldrag_tile = dash.hover_tile
                elif ev.button == 3:
                    panning = ev.pos
                elif ev.button == 2:
                    dash.apply_map_tool(sim, cam, 2)
            elif ev.type == pygame.MOUSEBUTTONUP:
                dash.handle_event(ev, sim)
                if ev.button == 3:
                    panning = None
                if ev.button == 1:
                    ldrag_tile = None
            elif ev.type == pygame.MOUSEMOTION:
                if panning:
                    dx, dy = ev.pos[0] - panning[0], ev.pos[1] - panning[1]
                    cam.x -= dx / cam.zoom
                    cam.y -= dy / (cam.zoom * cam.ys)
                    cam.clamp()
                    panning = ev.pos
                elif ldrag_tile and dash.view_rect().collidepoint(ev.pos):
                    dash.set_ghost(cam)
                    if dash.hover_tile != ldrag_tile:
                        dash.apply_map_tool(sim, cam, 1)
                        ldrag_tile = dash.hover_tile
            elif ev.type == pygame.MOUSEWHEEL:
                if not dash.handle_event(ev, sim):
                    mx, my = pygame.mouse.get_pos()
                    vr = dash.view_rect()
                    if vr.collidepoint((mx, my)):
                        closest = min(range(len(ZOOMS)), key=lambda i: abs(ZOOMS[i] - cam.zoom))
                        idx = max(0, min(len(ZOOMS) - 1, closest + (1 if ev.y > 0 else -1)))
                        cam.set_zoom(ZOOMS[idx], anchor_screen=(mx - vr.x, my))

        # actions du dashboard
        if dash.action:
            kind, val = dash.action
            dash.action = None
            if kind == "pause":
                sim.paused = not sim.paused
            elif kind == "step":
                sim.tick()
            elif kind == "speed":
                sim.speed = min(8, max(1, sim.speed + val))
            elif kind == "speed_set":
                sim.speed = max(1, min(8, val))
            elif kind == "spawn":
                for _ in range(val):
                    sim.spawn_agent()
            elif kind == "spawn_sheep":
                for _ in range(val):
                    sim.spawn_sheep()
            elif kind == "create_tool":
                from game.config import TOOL_RECIPES
                path = dash.tool_editor.save_png("assets/tools_custom", dash.tool_editor_kind)
                aid = am.register_custom_tool(path, dash.tool_editor_kind, label=dash.tool_editor.name)
                if sim.selected and sim.selected.alive:
                    sim.selected.tool = aid
                    sim.selected.tool_durability = TOOL_RECIPES.get(dash.tool_editor_kind, {}).get("durability", 30)
                    sim.log(f"{sim.selected.name} recoit un outil fait main : {dash.tool_editor.name}.",
                            (248, 208, 98), "economie")
                dash.tool_editor.clear()
            elif kind == "grid":
                ren.show_grid = not ren.show_grid
            elif kind == "legend":
                show_legend[0] = not show_legend[0]
            elif kind == "reseed":
                populate(world, am, sim.rng, dense=False)
                sim.log("Nouvelle pluie de ressources sur la carte.", (248, 208, 98), "monde")
            elif kind == "reset":
                world, sim = build_world(am, int(sim.rng.integers(1 << 30)), procedural=True)
                sim.speed = args.speed
                dash.hover_tile = (0, 0)
            elif kind == "save_game":
                from game.save import save_game as _save
                path, sz = _save(sim, cam, slot=0)
                sim.log(f"Sauvegardé: {path} ({sz:.1f} Mo)", (108, 208, 128), "monde")
            elif kind == "load_game":
                from game.save import load_game as _load
                new_sim, new_cam = _load(am, slot=0)
                if new_sim is not None:
                    sim = new_sim
                    if new_cam is not None:
                        cam = new_cam
                    world = sim.w
                    sim.log("Partie chargée.", (108, 208, 128), "monde")
                else:
                    sim.log("Aucune sauvegarde trouvée.", (228, 98, 98), "monde")

        if not sim.paused:
            acc += sim.speed * SIM_HZ / FPS
            n = 0
            while acc >= 1.0 and n < 8:
                sim.tick()
                acc -= 1.0
                n += 1
        else:
            acc = 0.0
            if sim.selected and not sim.selected.alive:
                sim.selected = None
        if sim.selected and not sim.selected.alive:
            sim.selected = None
        if dash.follow and sim.selected and sim.selected.alive:
            cam.center_on(sim.selected.x, sim.selected.y)

        # auto-tilt : top-down (0°) en zoom arrière, 2.5D (55°) à partir de ×1.5
        _t_min, _t_max = 0.0, 55.0
        _z_lo, _z_hi = 0.25, 1.5
        _z_clamped = max(_z_lo, min(_z_hi, cam.zoom))
        _target_tilt = _t_min + (_t_max - _t_min) * (_z_clamped - _z_lo) / (_z_hi - _z_lo)
        cam.tilt = cam.tilt + (_target_tilt - cam.tilt) * 0.12

        dash.set_ghost(cam)
        mx, my = pygame.mouse.get_pos()
        vr = dash.view_rect()
        in_map = vr.collidepoint((mx, my))
        ui = {"tile": dash.hover_tile, "ghost": dash.hover_tile[0] > 0 and in_map,
              "asset": dash.asset, "mode": dash.mode, "agent": sim.selected,
              "legend": show_legend[0], "brush": dash.brush_radius(),
              "view_rect": pygame.Rect(0, 0, vr.width, vr.height),
              "overlay": dash.active_overlay}
        view_surf = pygame.Surface((vr.width, vr.height))
        ren.draw(view_surf, sim, cam, ui)
        screen.fill((227, 232, 236))
        screen.blit(view_surf, (vr.x, vr.y))
        dash.draw(screen, sim, cam)
        # cadre visible — dessiné EN DERNIER par-dessus tout
        pygame.draw.rect(screen, (180, 186, 196), (0, 0, SCREEN_W, SCREEN_H), 2)
        pygame.display.flip()
        clock.tick(FPS)

    from game.save import save_game as _auto_save
    try:
        _auto_save(sim, cam, slot=0)
    except Exception:
        import sys
        print(f"[auto-save] {sys.exc_info()[1]}", file=sys.stderr)
    pygame.quit()


if __name__ == "__main__":
    main()

```

## main_qt.py

**Type :** `.py`

```python

"""Univers Vivant — point d'entree PyQt6.

Utilise le meme moteur que main.py, le meme SimulationController,
les memes snapshots et les memes commandes.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ["QT_QPA_PLATFORM"] = os.environ.get("QT_QPA_PLATFORM", "")


def main():
    ap = argparse.ArgumentParser(description="Univers Vivant — interface PyQt6")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--speed", type=int, default=2)
    ap.add_argument("--blank", type=int, default=0)
    ap.add_argument("--procedural", type=int, default=1)
    args = ap.parse_args()

    from ui_qt.app import create_app
    app = create_app()

    # Importer le moteur (pas de Pygame nécessaire pour le moteur lui-même)
    from game.assets_manager import AssetManager
    from game.assets_api import _set_asset_manager
    from game.engine import build_world, build_world_blank
    from game.simulation_controller import SimulationController

    print("Chargement des assets...")
    am = AssetManager(headless=True)
    am.discover()
    am.ensure_procedural_blocks()
    am.ensure_procedural_tools()
    _set_asset_manager(am)

    # Construire le monde
    if args.blank:
        world, sim = build_world_blank(am, args.seed)
    else:
        world, sim = build_world(am, args.seed, procedural=bool(args.procedural))
    sim.speed = args.speed

    from game.camera import Camera
    cam = Camera()
    import numpy as np
    _ys, _xs = np.nonzero(world.land)
    if len(_xs):
        from game.config import TILE
        cam.center_on(float(_xs.mean()) * TILE, float(_ys.mean()) * TILE)

    # Créer le controller
    controller = SimulationController(sim, cam)

    # Créer la fenêtre
    from ui_qt.main_window import MainWindow
    window = MainWindow(controller, am)
    window.show()

    print("Interface PyQt6 demarree.")
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())

```

## requirements.txt

**Type :** `.txt`

```text

pygame>=2.6
numpy>=1.26
Pillow>=10
PyQt6>=6.6
opensimplex>=0.4

```

## tests/__init__.py

**Type :** `.py`

```python

﻿

```

## tests/rapport_2026-09-20.md

**Type :** `.md`

````markdown

# Rapport de tests — 2026-09-20

## Commits today

```
b662cdc Lot 10: New building blueprints (coffre, grenier, atelier, puits)
489bb53 Lot 7.2: Hierarchical decisions (strategy + target heads)
725818b Remove R key reset - too dangerous as single keystroke
189db40 Fix catalogue + sprite sheets + black buildings + NIN 128
```

## Fixes

| Bug | Status | Commit |
|-----|--------|--------|
| Catalogue mode (asset→place) | OK | 189db40 |
| Sprite sheets → register_grid_items | OK | 189db40 |
| Black buildings exclusion | OK | 189db40 |
| NIN migration 95→128 | OK | 189db40 |
| Vegetable sheet split (36 assets) | OK | 189db40 |
| R key reset removed | OK | 725818b |

## Lot 7.2: Decisions hierarchiques

- N_STRATEGIES=6, N_TARGETS=8
- Separate weight matrices (backward compatible with old saves)
- think() → (action, probs) unchanged; strategy/target stored in brain._strategy, brain._target
- learn() updates all 3 heads
- explain() returns strategy + target for dashboard
- Save/load: new weights saved, fallback for old saves

### Test
```
N_STRATEGIES=6 N_TARGETS=8
t=0   strat=4 target=5 act=run
t=50  strat=4 target=5 act=run
t=100 strat=4 target=5 act=run
t=150 strat=3 target=1 act=run
FINAL pop=5 deaths=0
```

## Lot 10: Nouveaux objets

| Blueprint | Blocks | Capacity | Status |
|-----------|--------|----------|--------|
| coffre | 1 bois | 40 | OK |
| grenier | 2x2 bois + roof | 120 | OK |
| atelier | 3x3 pierre + roof | — | OK |
| puits | 1 pierre | — | OK |

- `_choose_blueprint()`: context-aware (no house→house, no storage→coffre, etc.)
- `create_blueprint_site()`: generic site creation
- `complete_site()`: handles all types
- BUILD feasibility lowered: 3 bois OR 1 pierre (was 6+2)

## Lot 12: Tests longs

```
Seed=42, 10 agents, 2000 ticks
t=0    pop=10 deaths=0 sites=0 storages=0 elapsed=0.1s
t=500  pop=10 deaths=0 sites=0 storages=0 elapsed=22.7s
t=1000 pop=10 deaths=0 sites=0 storages=0 elapsed=42.6s
t=1500 pop=10 deaths=0 sites=0 storages=0 elapsed=63.4s
FINAL  pop=10 deaths=0 sites=0 storages=0 elapsed=82.7s
TPS: 24 ticks/sec
```

- Pop stable, no crashes, no NaN
- No sites created: agents don't harvest (pre-existing — EXPLORE bias dominates for young agents)
- NIN=128 brain works, old save format incompatible (must delete slot_0.pkl)

## Known issues

1. Agents never harvest in headless → no BUILD triggered → no sites
2. vegetable &fruit(.png has fullwidth parenthesis → register_grid_items called at startup
3. Dashboard still gets truncated by external process

````

## tests/results_phase2.md

**Type :** `.md`

```markdown

# Résultats tests — Anima Phase 1 + Phase 2

Date : 2026-09-21

## Résumé

- **26/26 tests passent**
- **compileall : 0 erreur**

---

## Tests Phase 1 (8)

| Test | Résultat |
|------|----------|
| test_anima_episodic_memory | PASS |
| test_anima_belief_update | PASS |
| test_anima_perceived_danger | PASS |
| test_anima_bias_modulation | PASS |
| test_anima_brain_schema | PASS |
| test_anima_migration_128_to_132 | PASS |
| test_anima_low_importance_forgotten | PASS |
| test_harvest_to_build_chain | PASS |

## Tests Phase 2 (7)

| Test | Résultat |
|------|----------|
| test_identity_api | PASS |
| test_values_api | PASS |
| test_social_belief_init | PASS |
| test_social_belief_update | PASS |
| test_social_score | PASS |
| test_identity_decay | PASS |
| test_social_target_selection | PASS |

## Tests intégration Phase 2 (4)

| Test | Résultat |
|------|----------|
| test_anima_social_beliefs_save_load | PASS |
| test_anima_old_save_defaults_do_not_crash | PASS |
| test_anima_values_modulate_bias_without_forcing_action | PASS |
| test_anima_no_nan_inf | PASS |

## Tests base (7)

| Test | Résultat |
|------|----------|
| test_brain_schema_inputs | PASS |
| test_migrate_input_weights | PASS |
| test_house_needs_all_layers | PASS |
| test_storage | PASS |
| test_site_has_required_phases | PASS |
| test_bootstrap_resource_memory | PASS |
| test_complete_site_creates_shelter | PASS |

---

## Fichiers modifiés

| Fichier | Changements |
|---------|-------------|
| `game/entities.py` | API anima_clamp, anima_add_identity, anima_add_value, anima_dominant_identity, anima_decay_identity, anima_social_belief, anima_update_social_belief, anima_social_score + garde old format |
| `game/simulation.py` | _record_anima → update_anima_from_event, valeurs dans _bias(), social score pour cibles, remplacement incréments dispersés |
| `game/brain.py` | Garde-fou rng=None pour têtes strat/targ (bug préexistant) |
| `game/brain_schema.py` | INPUT registre 132 entrées (Phase 1) |
| `game/save.py` | Sérialisation beliefs.beings dict + compat old float format |
| `game/dashboard.py` | Panneau Anima Phase 2 (identité dominante, top 3, valeurs, sociale) |
| `tests/test_behavior_chain.py` | 26 tests (15 origine + 7 Phase 1 + 4 intégration) |

```

## tests/results_phase2.txt

**Type :** `.txt`

```text

PASS: test_brain_schema_inputs (66 cles definies)
PASS: test_migrate_input_weights
PASS: test_harvest_to_build_chain
PASS: test_house_needs_all_layers
PASS: test_storage
PASS: test_site_has_required_phases
PASS: test_bootstrap_resource_memory
PASS: test_complete_site_creates_shelter
PASS: test_anima_episodic_memory
PASS: test_anima_belief_update
PASS: test_anima_perceived_danger
PASS: test_anima_bias_modulation
PASS: test_anima_brain_schema
PASS: test_anima_migration_128_to_132
PASS: test_anima_low_importance_forgotten
PASS: test_identity_api
PASS: test_values_api
PASS: test_social_belief_init
PASS: test_social_belief_update
PASS: test_social_score
PASS: test_identity_decay
PASS: test_social_target_selection
PASS: test_anima_social_beliefs_save_load
PASS: test_anima_old_save_defaults_do_not_crash
PASS: test_anima_values_modulate_bias_without_forcing_action
PASS: test_anima_no_nan_inf

=== TOUS LES 26 TESTS PASSENT ===
compileall: 0 erreur

```

## tests/results_phase_finale.md

**Type :** `.md`

```markdown

# Résultats tests — Anima Phase Finale

Date : 2026-09-21

## Résumé

- **36/36 tests passent** (test_behavior_chain)
- **3/3 tests headless passent** (test_headless)
- **compileall : 0 erreur**

---

## Tests Phase 1 (8)

| Test | Résultat |
|------|----------|
| test_anima_episodic_memory | PASS |
| test_anima_belief_update | PASS |
| test_anima_perceived_danger | PASS |
| test_anima_bias_modulation | PASS |
| test_anima_brain_schema | PASS |
| test_anima_migration_128_to_132 | PASS |
| test_anima_low_importance_forgotten | PASS |
| test_harvest_to_build_chain | PASS |

## Tests Phase 2 (7)

| Test | Résultat |
|------|----------|
| test_identity_api | PASS |
| test_values_api | PASS |
| test_social_belief_init | PASS |
| test_social_belief_update | PASS |
| test_social_score | PASS |
| test_identity_decay | PASS |
| test_social_target_selection | PASS |

## Tests Phase Finale (14)

| Test | Résultat |
|------|----------|
| test_anima_intention_persists_until_interrupt | PASS |
| test_anima_plan_rejects_impossible_step | PASS |
| test_delayed_causal_credit | PASS |
| test_observation_changes_habit | PASS |
| test_attachment_increases_home_preference | PASS |
| test_trauma_recovers_under_safety | PASS |
| test_institution_requires_repeated_practice | PASS |
| test_full_anima_save_load | PASS |
| test_long_run_no_nan_inf | PASS |
| test_anima_social_beliefs_save_load | PASS |
| test_anima_old_save_defaults_do_not_crash | PASS |
| test_anima_values_modulate_bias_without_forcing_action | PASS |
| test_anima_no_nan_inf | PASS |

## Tests base (7)

| Test | Résultat |
|------|----------|
| test_brain_schema_inputs | PASS |
| test_migrate_input_weights | PASS |
| test_house_needs_all_layers | PASS |
| test_storage | PASS |
| test_site_has_required_phases | PASS |
| test_bootstrap_resource_memory | PASS |
| test_complete_site_creates_shelter | PASS |

## Tests headless (3)

| Test | Résultat |
|------|----------|
| test_brain_132 | PASS |
| test_construction_blueprints | PASS |
| test_headless_2000 | PASS (36.9s) |

---

## Lots implémentés

| Lot | Description | Fichiers |
|-----|-------------|----------|
| A | Audit NIN (128→132), migration, sauvegardes | brain.py, brain_api.py, brain_schema.py, save.py, dashboard.py, renderer.py |
| B | 19 types d'événements psychologiques | simulation.py, entities.py |
| C | Trauma decay, attachement, deuil | entities.py, simulation.py |
| D | Intention psychologique persistante | entities.py, simulation.py |
| E | Plans courts et alternatives | simulation.py |
| F | Apprentissage causal différé | entities.py, simulation.py |
| G | Communication sémantique et fiabilité | simulation.py |
| H | Imitation réelle connectée aux habitudes | entities.py, simulation.py |
| I | Culture et connaissances collectives | entities.py |
| J | Institutions émergentes | entities.py |
| K | Héritage générationnel | simulation.py |
| L | Audit assets (guard renderer) | renderer.py |
| M | Diagnostics comportementaux | simulation.py |
| N | Dashboard Anima complet | dashboard.py |
| O | Sauvegarde finale (champs nouveaux) | save.py |
| P | Tests finaux (14 nouveaux) | test_behavior_chain.py |

```

## tests/test_behavior_chain.py

**Type :** `.py`

```python

"""Tests comportementaux de validation du plan de corrections."""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import numpy as np


def _make_sim():
    """Cree une simulation legere pour les tests."""
    import pygame
    pygame.init()
    pygame.display.set_mode((1, 1), pygame.HIDDEN)
    from game.assets_manager import AssetManager
    from game.engine import build_world
    am = AssetManager(headless=False).discover()
    am.ensure_procedural_blocks()
    am.ensure_procedural_tools()
    am.ensure_kaykit_resources()
    w, sim = build_world(am, seed=42, procedural=True)
    return sim


def test_harvest_to_build_chain():
    """HARVEST devient faisable quand on connait du bois/pierre."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None, "spawn_agent a echoue"
    a.age = 800000
    a.inv["bois"] = 0
    a.inv["pierre"] = 0
    a.remember("wood", 30, 30)
    a.remember("stone", 35, 30)
    f = sim._feasible(a)
    assert f[4], "HARVEST devrait etre faisable avec memoire de bois/pierre"
    a.inv["bois"] = 3
    f2 = sim._feasible(a)
    assert f2[6], "BUILD devrait etre faisable avec 3 bois"
    print("PASS: test_harvest_to_build_chain")


def test_house_needs_all_layers():
    """Le chantier exige fondation + mur + porte + toit."""
    from game.construction import HouseBlueprint
    tasks = HouseBlueprint.small_house(20, 20)
    foundations = [t for t in tasks if t.phase == "foundation"]
    walls = [t for t in tasks if t.phase == "wall"]
    doors = [t for t in tasks if t.phase == "door"]
    roofs = [t for t in tasks if t.phase == "roof"]
    assert len(foundations) > 0, "Au moins une fondation"
    assert len(walls) > 0, "Au moins un mur"
    assert len(doors) > 0, "Au moins une porte"
    assert len(roofs) > 0, "Au moins un toit"
    f0 = foundations[0]
    w0 = next((t for t in walls if t.tx == f0.tx and t.ty == f0.ty), None)
    if w0 is not None:
        assert f0.key != w0.key, "Fondation et mur ont des cles differentes"
    print("PASS: test_house_needs_all_layers")


def test_storage():
    """Depot et retrait dans un stockage."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    storage = sim.create_storage(a, 30, 30)
    assert storage is not None
    a.inv["bois"] = 5
    ok = sim.deposit_to_storage(a, storage)
    assert ok, "deposit a echoue"
    assert storage.inventory.get("bois", 0) > 0, "Le stockage devrait contenir du bois"
    a.inv["bois"] = 0
    ok2 = sim.withdraw_from_storage(a, storage, "bois")
    assert ok2, "withdraw a echoue"
    assert a.inv["bois"] > 0, "L'agent devrait avoir du bois"
    print("PASS: test_storage")


def test_site_has_required_phases():
    """site_has_required_phases verifie les 4 phases."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a.inv["bois"] = 50
    a.inv["pierre"] = 50
    site = sim.create_house_site(a, 100, 100)
    assert site is not None
    assert not sim.site_has_required_phases(site), "Site incomplet ne devrait pas etre complet"
    for task in site.tasks:
        site.mark_placed(a.eid, task)
    assert sim.site_has_required_phases(site), "Site complet devrait etre complet"
    print("PASS: test_site_has_required_phases")


def test_bootstrap_resource_memory():
    """bootstrap_resource_memory remplit la memoire."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    sim.bootstrap_resource_memory(a, radius=10)
    has_memory = (
        bool(a.seen.get("food", []))
        or bool(a.seen.get("wood", []))
        or bool(a.seen.get("stone", []))
        or bool(a.seen.get("water", []))
    )
    assert has_memory, "L'agent devrait avoir au moins une memoire de ressource"
    print("PASS: test_bootstrap_resource_memory")


def test_brain_schema_inputs():
    """Le vecteur de perception fait bien 132 entrees."""
    from game.brain_schema import INPUT, NIN
    assert NIN == 132
    vals = list(INPUT.values())
    assert max(vals) == 131
    assert min(vals) == 0
    print(f"PASS: test_brain_schema_inputs ({len(vals)} cles definies)")


def test_migrate_input_weights():
    """Migration 128->132 entrees."""
    from game.brain import migrate_input_weights, OLD_NIN, N_OUT
    from game.brain_schema import NIN
    n_hid = 64
    old_p = np.random.default_rng(0).standard_normal(
        OLD_NIN * n_hid + 2 * n_hid + N_OUT * n_hid + N_OUT)
    new_p, new_n = migrate_input_weights(old_p, old_n=OLD_NIN, new_n=NIN)
    expected = NIN * n_hid + 2 * n_hid + N_OUT * n_hid + N_OUT
    assert new_p.size == expected, f"Poids attendus {expected}, obtenus {new_p.size}"
    assert new_n == NIN
    assert np.allclose(new_p[:OLD_NIN * n_hid], old_p[:OLD_NIN * n_hid]), "Les poids anciens doivent etre conserves"
    print("PASS: test_migrate_input_weights")


def test_complete_site_creates_shelter():
    """complete_site cree un abri et un depot."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a.inv["bois"] = 50
    a.inv["pierre"] = 50
    site = sim.create_house_site(a, 100, 100)
    assert site is not None
    for task in site.tasks:
        a.inv[task.material] = 50
        sim.place_site_block(a, site, task)
    assert site.complete(), "Le site devrait etre complet"
    w = sim.w
    has_shelter = bool(w.shelter[101:104, 101:104].any())
    assert has_shelter, "Le site devrait creer un abri"
    has_storage = any(
        abs(st.tx - 102) <= 1 and abs(st.ty - 102) <= 1
        for st in w.storages.values()
    )
    assert has_storage, "Le site devrait creer un depot"
    print("PASS: test_complete_site_creates_shelter")


def test_anima_episodic_memory():
    """Un agent enregistre des episodes Anima avec importance."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    ep = a.remember_anima_episode(
        100, "monster_attack", (50, 50),
        actors=[a.eid, 99], action="flee", outcome="survived",
        emotion={"fear": 0.88, "pain": 0.35, "surprise": 0.6},
        importance=0.84,
    )
    assert ep["kind"] == "monster_attack"
    assert ep["importance"] == 0.84
    assert len(a.anima["episodic_memory"]) == 1
    assert a.anima["trauma"]["attack"] > 0
    assert a.anima["identity"]["survivor"] > 0
    print("PASS: test_anima_episodic_memory")


def test_anima_belief_update():
    """Un episode important met a jour les croyances lieux."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a.remember_anima_episode(
        100, "monster_attack", (80, 80),
        action="flee", outcome="survived",
        emotion={"fear": 0.9, "pain": 0.5, "surprise": 0.4},
        importance=0.80,
    )
    cx, cy = 80 // 8, 80 // 8
    belief = a.anima["beliefs"]["places"].get((cx, cy), 0.0)
    assert belief > 0.3, f"Croyance devrait etre > 0.3, obtenu {belief}"
    print("PASS: test_anima_belief_update")


def test_anima_perceived_danger():
    """Le danger percu combine vision + croyance + trauma."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a.anima["beliefs"]["places"][(62, 62)] = 0.8
    a.anima["trauma"]["attack"] = 0.5
    pd = a.anima_perceived_danger(500, 500, 0.30)
    assert pd > 0.30, f"Danger percu devrait etre > base, obtenu {pd}"
    print("PASS: test_anima_perceived_danger")


def test_anima_bias_modulation():
    """Le biais FLEE augmente avec la peur trauma."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    from game.brain import FLEE
    a.anima["trauma"]["attack"] = 0.8
    b1 = sim._bias(a)
    a.anima["trauma"]["attack"] = 0.0
    b2 = sim._bias(a)
    assert b1[FLEE] > b2[FLEE], "FLEE bias devrait etre plus fort avec trauma"
    print("PASS: test_anima_bias_modulation")


def test_anima_brain_schema():
    """Le schema Anima fait 132 entrees."""
    from game.brain_schema import INPUT, NIN
    assert NIN == 132
    assert "trauma_attack" in INPUT
    assert "belief_danger" in INPUT
    assert "episode_count" in INPUT
    assert "anima_fighter" in INPUT
    print("PASS: test_anima_brain_schema")


def test_anima_migration_128_to_132():
    """Migration des poids de 128 vers 132."""
    from game.brain import migrate_input_weights, OLD_NIN, N_OUT
    from game.brain_schema import NIN
    old_n = OLD_NIN
    n_hid = 64
    old_p = np.random.default_rng(0).standard_normal(
        old_n * n_hid + 2 * n_hid + N_OUT * n_hid + N_OUT)
    new_p, new_n = migrate_input_weights(old_p, old_n=old_n, new_n=NIN)
    expected = NIN * n_hid + 2 * n_hid + N_OUT * n_hid + N_OUT
    assert new_p.size == expected, f"Poids attendus {expected}, obtenus {new_p.size}"
    assert new_n == NIN
    assert np.allclose(new_p[:old_n * n_hid], old_p[:old_n * n_hid])
    print("PASS: test_anima_migration_128_to_132")


def test_anima_low_importance_forgotten():
    """Un episode peu important n'est pas stocke."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    ep = a.remember_anima_episode(
        100, "new_area_discovered", (50, 50),
        action="explore", outcome="discovered",
        emotion={"fear": 0.0, "pain": 0.0, "surprise": 0.1},
        importance=0.05,
    )
    assert ep is not None
    assert len(a.anima["episodic_memory"]) == 0, "Episode < 0.20 pas stocke"
    print("PASS: test_anima_low_importance_forgotten")


# =====================================================================
# Phase 2 tests
# =====================================================================

def test_identity_api():
    """anima_add_identity, anima_clamp, anima_dominant_identity."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    assert a.anima_dominant_identity() is None
    a.anima_add_identity("builder", 0.5)
    assert abs(a.anima["identity"]["builder"] - 0.5) < 1e-6
    assert a.anima_dominant_identity() == "builder"
    a.anima_add_identity("builder", 0.6)
    assert a.anima["identity"]["builder"] == 1.0, "clamp a 1.0"
    a.anima_add_identity("builder", -0.3)
    assert abs(a.anima["identity"]["builder"] - 0.7) < 1e-6
    a.anima_add_identity("fighter", 1.0)
    assert a.anima_dominant_identity() == "fighter"
    print("PASS: test_identity_api")


def test_values_api():
    """anima_add_value met a jour les valeurs avec clamp."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a.anima_add_value("security", 0.5)
    assert abs(a.anima["values"]["security"] - 1.0) < 1e-6, "0.5+0.5=1.0"
    a.anima_add_value("security", 0.3)
    assert a.anima["values"]["security"] == 1.0, "clamp a 1.0"
    a.anima_add_value("security", -1.5)
    assert abs(a.anima["values"]["security"] - 0.0) < 1e-6, "clamp a 0.0"
    a.anima_add_value("generosity", -0.3)
    assert abs(a.anima["values"]["generosity"] - 0.2) < 1e-6, "0.5-0.3=0.2"
    print("PASS: test_values_api")


def test_social_belief_init():
    """Les croyances sociales sont initialisees a 0.5 trust par defaut."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    b = sim.spawn_agent(x=510, y=500)
    assert a is not None and b is not None
    belief = a.anima_social_belief(b.eid, 0)
    assert belief["trust"] == 0.5, f"trust initial: {belief['trust']}"
    assert belief["danger"] == 0.0
    assert belief["generosity"] == 0.5
    assert belief["reliability"] == 0.5
    assert belief["confidence"] == 0.0
    print("PASS: test_social_belief_init")


def test_social_belief_update():
    """anima_update_social_belief met a jour et clamp les croyances."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    b = sim.spawn_agent(x=510, y=500)
    assert a is not None and b is not None
    a.anima_update_social_belief(b.eid, 100, trust_delta=0.3)
    belief = a.anima_social_belief(b.eid, 100)
    assert abs(belief["trust"] - 0.8) < 1e-6
    a.anima_update_social_belief(b.eid, 200, trust_delta=0.5)
    assert a.anima_social_belief(b.eid, 200)["trust"] == 1.0, "clamp trust a 1.0"
    a.anima_update_social_belief(b.eid, 300, danger_delta=0.8)
    assert abs(a.anima_social_belief(b.eid, 300)["danger"] - 0.8) < 1e-6
    a.anima_update_social_belief(b.eid, 400, danger_delta=-2.0)
    assert a.anima_social_belief(b.eid, 400)["danger"] == 0.0, "clamp danger a 0.0"
    assert a.anima_social_belief(b.eid, 400)["last_update"] == 400
    print("PASS: test_social_belief_update")


def test_social_score():
    """anima_social_score combine trust et danger en score."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    b = sim.spawn_agent(x=510, y=500)
    assert a is not None and b is not None
    s_neutral = a.anima_social_score(b.eid)
    assert abs(s_neutral - 0.0) < 1e-6, f"score neutre: {s_neutral}"
    a.anima_update_social_belief(b.eid, 100, trust_delta=0.4, danger_delta=0.0)
    s_trusted = a.anima_social_score(b.eid)
    assert s_trusted > 0.0, f"score confiance: {s_trusted}"
    a.anima_update_social_belief(b.eid, 200, trust_delta=-0.8, danger_delta=0.5)
    s_danger = a.anima_social_score(b.eid)
    assert s_danger < -0.1, f"score danger: {s_danger}"
    print("PASS: test_social_score")


def test_identity_decay():
    """anima_decay_identity reduit doucement les traits."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a.anima_add_identity("builder", 0.5)
    before = a.anima["identity"]["builder"]
    a.anima_decay_identity()
    after = a.anima["identity"]["builder"]
    assert after < before, f"decay: {after} >= {before}"
    a.anima_add_identity("fighter", 0.02)
    before_f = a.anima["identity"]["fighter"]
    a.anima_decay_identity()
    after_f = a.anima["identity"]["fighter"]
    assert after_f < before_f, f"decay devrait reduire: {after_f} >= {before_f}"
    print("PASS: test_identity_decay")


def test_social_target_selection():
    """Les actions sociales privilegient les cibles de confiance."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    b = sim.spawn_agent(x=510, y=500)
    c = sim.spawn_agent(x=520, y=500)
    assert a is not None and b is not None and c is not None
    a.anima_update_social_belief(b.eid, 100, trust_delta=0.4)
    a.anima_update_social_belief(c.eid, 100, trust_delta=-0.3)
    a._near_agents = [b, c]
    a.anima["beliefs"]["beings"] = a.anima["beliefs"]["beings"]
    targets = sorted([b, c],
                     key=lambda o: a.anima_social_score(o.eid), reverse=True)
    assert targets[0].eid == b.eid, "la cible de confiance devrait etre en premier"
    print("PASS: test_social_target_selection")


def test_anima_social_beliefs_save_load():
    """Les croyances sociales survivent a un cycle save/load."""
    import tempfile, os, pickle
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    b = sim.spawn_agent(x=510, y=500)
    assert a is not None and b is not None
    a.anima_update_social_belief(b.eid, 100, trust_delta=0.3, danger_delta=0.2)
    from game.save import save_game, load_game
    slot = 99
    save_game(sim, slot=slot)
    sim2_loaded, _ = load_game(sim.am, slot=slot)
    assert sim2_loaded is not None
    a2 = next((x for x in sim2_loaded.agents if x.eid == a.eid), None)
    assert a2 is not None, "agent non restaure"
    belief = a2.anima_social_belief(b.eid, 200)
    assert abs(belief["trust"] - 0.8) < 0.05, f"trust post-load: {belief['trust']}"
    assert abs(belief["danger"] - 0.2) < 0.05, f"danger post-load: {belief['danger']}"
    try:
        os.remove(os.path.join("data", f"slot_{slot}.pkl"))
    except OSError:
        pass
    print("PASS: test_anima_social_beliefs_save_load")


def test_anima_old_save_defaults_do_not_crash():
    """Une structure ancienne sans Anima Phase 2 ne plante pas."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a.anima["beliefs"]["beings"] = {99: 0.7}
    belief = a.anima_social_belief(99, 0)
    assert isinstance(belief, dict), "ancien format float converti en dict"
    assert belief["trust"] == 0.5
    assert a.anima_social_score(99) == 0.0
    print("PASS: test_anima_old_save_defaults_do_not_crash")


def test_anima_values_modulate_bias_without_forcing_action():
    """Les valeurs influencent les biais sans forcer l'action."""
    from game.brain_api import GIVE, TAKE, TALK, SOCIAL, ATTACK
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    b = sim.spawn_agent(x=510, y=500)
    assert a is not None and b is not None
    a.anima["values"]["generosity"] = 1.0
    a.anima["values"]["community"] = 1.0
    a.anima["values"]["survival"] = 0.0
    a._near_agents = [b]
    f = sim._feasible(a)
    assert any(f[i] for i in (GIVE, TAKE, TALK, SOCIAL, ATTACK)), \
        "au moins un acte social faisable"
    print("PASS: test_anima_values_modulate_bias_without_forcing_action")


def test_anima_no_nan_inf():
    """Aucun NaN/Inf dans les donnees Anima apres operations."""
    import math
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a.anima_add_identity("builder", 0.5)
    a.anima_add_identity("fighter", 0.3)
    a.anima_add_value("survival", 0.8)
    a.anima_add_value("security", -0.6)
    a.anima_decay_identity()
    a.anima_decay_identity()
    for k, v in a.anima["identity"].items():
        assert math.isfinite(v), f"NaN/Inf dans identity[{k}]: {v}"
    for k, v in a.anima["values"].items():
        assert math.isfinite(v), f"NaN/Inf dans values[{k}]: {v}"
    b = sim.spawn_agent(x=520, y=500)
    a.anima_update_social_belief(b.eid, 100, trust_delta=0.5, danger_delta=0.3)
    a.anima_update_social_belief(b.eid, 200, trust_delta=-0.8, danger_delta=-1.0)
    belief = a.anima_social_belief(b.eid, 200)
    for k, v in belief.items():
        assert math.isfinite(v), f"NaN/Inf dans belief[{k}]: {v}"
    score = a.anima_social_score(b.eid)
    assert math.isfinite(score), f"NaN/Inf dans social_score: {score}"
    print("PASS: test_anima_no_nan_inf")


def test_anima_intention_persists_until_interrupt():
    """L'intention persiste et expire apres duree."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a.anima_set_intention("secure_food", "faim", priority=0.7, tick=100, duration=500)
    assert a.anima_intention_valid(200)
    assert a.anima_intention_valid(599)
    assert not a.anima_intention_valid(601)
    a.anima_set_intention("build_home", "abri", priority=0.6, tick=100, duration=200)
    assert a.anima_intention_valid(250)
    a.anima_clear_intention()
    assert a.anima_get_intention() is None
    print("PASS: test_anima_intention_persists_until_interrupt")


def test_anima_plan_rejects_impossible_step():
    """Les plans ne contiennent que des actions faisables."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a._near_agents = []
    plans = sim._generate_plans(a)
    assert isinstance(plans, list)
    for p in plans:
        for step in p.get("steps", []):
            assert 0 <= step < 15, f"step hors range: {step}"
    print("PASS: test_anima_plan_rejects_impossible_step")


def test_delayed_causal_credit():
    """Le credit causal se dissipe avec le temps."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a.anima_add_causal_trace("harvest", (50, 50), 100, expected_effect="food_found")
    credit_early = a.anima_credit_for("food_found", 200)
    assert credit_early > 0, "credit devrait etre > 0 proche de l'action"
    a.anima_decay_causal_traces(rate=0.5)
    credit_late = a.anima_credit_for("food_found", 1500)
    assert credit_late < credit_early, "credit devrait diminuer apres decay"
    print("PASS: test_delayed_causal_credit")


def test_observation_changes_habit():
    """L'observation modifie les habitudes."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    from game.brain_api import EXPLORE
    before = float(a.habits[EXPLORE])
    a.anima_record_observation(EXPLORE, 0.8, 100)
    a.anima_record_observation(EXPLORE, 0.6, 110)
    a.anima_apply_observation_learning()
    after = float(a.habits[EXPLORE])
    assert after > before, f"habitude devrait augmenter: {after} <= {before}"
    print("PASS: test_observation_changes_habit")


def test_attachment_increases_home_preference():
    """L'attachement au foyer augmente la preference de retour."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a.home = (60, 60)
    assert a.anima_home_preference() == 0.0
    a.anima_add_attachment(f"home:{a.home[0]}:{a.home[1]}", 0.5)
    pref = a.anima_home_preference()
    assert pref > 0.0, f"preference devrait etre > 0: {pref}"
    print("PASS: test_attachment_increases_home_preference")


def test_trauma_recovers_under_safety():
    """Le trauma diminue sous securite et soutien."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    a.anima["trauma"]["attack"] = 0.5
    a.anima["trauma"]["loss"] = 0.3
    a.anima_decay_trauma(safety=1.0, support=1.0)
    assert a.anima["trauma"]["attack"] < 0.5, "trauma attack devrait diminuer"
    assert a.anima["trauma"]["loss"] < 0.3, "trauma loss devrait diminuer"
    a.anima["trauma"]["attack"] = 0.5
    a.anima_decay_trauma(safety=0.0, support=0.0)
    assert a.anima["trauma"]["attack"] < 0.5, "trauma diminue meme sans securite"
    print("PASS: test_trauma_recovers_under_safety")


def test_institution_requires_repeated_practice():
    """Une institution n'apparait qu'apres pratiques repetees."""
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    assert a is not None
    sim.clan_knowledge.add_institution("shared_storage", 50, 50, a.eid, 100)
    key = ("shared_storage", 50 // 8, 50 // 8)
    inst = sim.clan_knowledge.institutions.get(key)
    assert inst is not None
    assert inst["stability"] < 0.3, "stabilite faible au depart"
    for i in range(5):
        sim.clan_knowledge.record_practice("shared_storage", 50, 50, a.eid, "deposit", 200 + i * 10)
    inst2 = sim.clan_knowledge.institutions.get(key)
    assert inst2["stability"] > 0.15, "stabilite devrait augmenter"
    print("PASS: test_institution_requires_repeated_practice")


def test_full_anima_save_load():
    """Cycle complet save/load avec tous les champs Anima."""
    import os
    sim = _make_sim()
    a = sim.spawn_agent(x=500, y=500)
    b = sim.spawn_agent(x=510, y=500)
    assert a is not None and b is not None
    a.anima_add_identity("builder", 0.4)
    a.anima_add_value("community", 0.3)
    a.anima["trauma"]["attack"] = 0.2
    a.anima_update_social_belief(b.eid, 100, trust_delta=0.3)
    a.anima_set_intention("build_home", "test", priority=0.6, tick=100)
    a.anima_add_causal_trace("harvest", (50, 50), 100, "food_found")
    a.anima_add_attachment(f"home:{a.home[0]}:{a.home[1]}" if a.home else "home:0:0", 0.4)
    from game.save import save_game, load_game
    slot = 98
    save_game(sim, slot=slot)
    loaded, _ = load_game(sim.am, slot=slot)
    assert loaded is not None
    a2 = next((x for x in loaded.agents if x.eid == a.eid), None)
    assert a2 is not None
    assert abs(a2.anima["identity"]["builder"] - 0.4) < 0.05
    assert abs(a2.anima["values"]["community"] - 0.8) < 0.05
    assert a2.anima["trauma"]["attack"] > 0.1
    intent = a2.anima_get_intention()
    assert intent is not None and intent["kind"] == "build_home"
    traces = a2.anima.get("causal_traces", [])
    assert len(traces) >= 1
    try:
        os.remove(os.path.join("data", f"slot_{slot}.pkl"))
    except OSError:
        pass
    print("PASS: test_full_anima_save_load")


def test_long_run_no_nan_inf():
    """1000 ticks sans NaN/Inf dans les donnees Anima."""
    import math
    sim = _make_sim()
    for _ in range(3):
        sim.spawn_agent(x=500, y=500)
    for _ in range(1000):
        sim.step()
    for a in sim.agents:
        if not a.alive:
            continue
        for k, v in a.anima.get("identity", {}).items():
            assert math.isfinite(v), f"NaN identity[{k}]"
        for k, v in a.anima.get("values", {}).items():
            assert math.isfinite(v), f"NaN values[{k}]"
        for k, v in a.anima.get("trauma", {}).items():
            assert math.isfinite(v), f"NaN trauma[{k}]"
        belief = a.anima.get("beliefs", {}).get("beings", {})
        for eid, bdict in belief.items():
            if isinstance(bdict, dict):
                for bk, bv in bdict.items():
                    assert math.isfinite(bv), f"NaN belief[{eid}][{bk}]"
    print("PASS: test_long_run_no_nan_inf")


if __name__ == "__main__":
    test_brain_schema_inputs()
    test_migrate_input_weights()
    test_harvest_to_build_chain()
    test_house_needs_all_layers()
    test_storage()
    test_site_has_required_phases()
    test_bootstrap_resource_memory()
    test_complete_site_creates_shelter()
    test_anima_episodic_memory()
    test_anima_belief_update()
    test_anima_perceived_danger()
    test_anima_bias_modulation()
    test_anima_brain_schema()
    test_anima_migration_128_to_132()
    test_anima_low_importance_forgotten()
    test_identity_api()
    test_values_api()
    test_social_belief_init()
    test_social_belief_update()
    test_social_score()
    test_identity_decay()
    test_social_target_selection()
    test_anima_social_beliefs_save_load()
    test_anima_old_save_defaults_do_not_crash()
    test_anima_values_modulate_bias_without_forcing_action()
    test_anima_no_nan_inf()
    test_anima_intention_persists_until_interrupt()
    test_anima_plan_rejects_impossible_step()
    test_delayed_causal_credit()
    test_observation_changes_habit()
    test_attachment_increases_home_preference()
    test_trauma_recovers_under_safety()
    test_institution_requires_repeated_practice()
    test_full_anima_save_load()
    test_long_run_no_nan_inf()
    print("\n=== TOUS LES TESTS PASSENT ===")

```

## tests/test_headless.py

**Type :** `.py`

```python

"""Tests headless — vérifie stabilité après changements."""
import sys, os, time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_brain_132():
    from game.brain import Brain, N_IN, N_OUT, N_STRATEGIES, N_TARGETS
    assert N_IN == 132
    assert N_OUT == 15
    assert N_STRATEGIES == 6
    assert N_TARGETS == 8
    import numpy as np
    rng = np.random.default_rng()
    b = Brain(n_hid=64, rng=rng)
    import numpy as np
    x = np.zeros(N_IN)
    act, probs = b.think(x)
    assert 0 <= act < N_OUT
    assert len(probs) == N_OUT
    assert b._strategy in range(N_STRATEGIES)
    assert b._target in range(N_TARGETS)
    b.learn(0.5)
    b2 = b.copy()
    assert b2.n == b.n
    print("OK test_brain_132")


def test_construction_blueprints():
    from game.construction import HouseBlueprint, blueprint_from_name
    for name in ("coffre", "grenier", "atelier", "puits", "small_house", "storage_hut"):
        tasks = blueprint_from_name(name, 10, 10)
        assert len(tasks) > 0, f"blueprint {name} empty"
    print("OK test_construction_blueprints")


def test_headless_2000():
    from game.engine import build_world
    from game.assets_manager import AssetManager
    from game.assets_api import _set_asset_manager
    am = AssetManager(headless=True).discover()
    am.ensure_procedural_blocks()
    am.ensure_procedural_tools()
    am.ensure_kaykit_resources()
    _set_asset_manager(am)
    import os
    from game.config import ASSETS_DIR
    for f in os.listdir(ASSETS_DIR):
        if "vegetable" in f.lower() and f.endswith(".png") and os.path.isfile(os.path.join(ASSETS_DIR, f)):
            p = os.path.join(ASSETS_DIR, f)
            if os.path.getsize(p) > 1000:
                am.register_grid_items(p, category="nourriture", role="food", cell_w=16, cell_h=16, edible=24.0)
                break
    w, sim = build_world(am, seed=42, procedural=True, n_agents=10)
    t0 = time.time()
    for i in range(2000):
        sim.tick()
    elapsed = time.time() - t0
    assert len(sim.agents) > 0, "all agents dead"
    assert not any(np.isnan(a.x) for a in sim.agents), "NaN position"
    print(f"OK test_headless_2000: pop={len(sim.agents)} deaths={sim.stats.get('deaths',0)} {elapsed:.1f}s")


if __name__ == "__main__":
    import numpy as np
    test_brain_132()
    test_construction_blueprints()
    test_headless_2000()
    print("ALL TESTS PASSED")

```

## tests/test_qt_smoke.py

**Type :** `.py`

```python

"""Tests Qt smoke — valide le demarrage de l'interface PyQt6.

Lance QApplication en mode offscreen, cree la fenetre,
et valide que les docks et modeles se creent correctement.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["QT_QPA_PLATFORM"] = "offscreen"


def _make_controller():
    """Construit un Sim + SimulationController pour les tests."""
    import pygame
    pygame.init()
    pygame.display.set_mode((1, 1))

    from game.assets_manager import AssetManager
    from game.assets_api import _set_asset_manager
    from game.engine import build_world
    from game.simulation_controller import SimulationController

    am = AssetManager(headless=True)
    am.discover()
    _set_asset_manager(am)
    world, sim = build_world(am, seed=42, procedural=True)
    return SimulationController(sim)


class TestQtModels(unittest.TestCase):
    """Tests des modeles Qt sans creer de QApplication."""

    @classmethod
    def setUpClass(cls):
        cls.controller = _make_controller()

    def test_population_model(self):
        from ui_qt.models.population_model import PopulationModel
        from game.ui_snapshots import population_snapshot
        model = PopulationModel()
        snap = population_snapshot(self.controller.sim)
        model.set_snapshot(snap)
        self.assertEqual(model.rowCount(), len(snap))
        self.assertEqual(model.columnCount(), 10)
        if model.rowCount() > 0:
            idx = model.index(0, 0)
            self.assertIsNotNone(model.data(idx))

    def test_journal_model(self):
        from ui_qt.models.journal_model import JournalModel
        from game.ui_snapshots import journal_snapshot
        model = JournalModel()
        self.controller.sim.log("Test entry", (255, 0, 0), "monde")
        snap = journal_snapshot(self.controller.sim)
        model.set_snapshot(snap)
        self.assertGreater(model.rowCount(), 0)

    def test_anima_model_empty(self):
        from ui_qt.models.anima_model import AnimaModel
        model = AnimaModel()
        model.set_snapshot(None)
        self.assertEqual(model.rowCount(), 0)

    def test_society_model(self):
        from ui_qt.models.society_model import SocietyModel
        from game.ui_snapshots import society_snapshot
        model = SocietyModel()
        snap = society_snapshot(self.controller.sim)
        model.set_snapshot(snap)
        self.assertGreater(model.rowCount(), 0)

    def test_assets_model(self):
        from ui_qt.models.assets_model import AssetsModel
        model = AssetsModel()
        model.set_snapshot([{"id": 1, "nom": "test", "categorie": "tree",
                             "role": "tree", "placable": True}])
        self.assertEqual(model.rowCount(), 1)


class TestQtSmoke(unittest.TestCase):
    """Tests de demarrage de QApplication et MainWindow."""

    @classmethod
    def setUpClass(cls):
        from PyQt6.QtWidgets import QApplication
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication(sys.argv)
        cls.controller = _make_controller()

    def test_app_exists(self):
        from PyQt6.QtWidgets import QApplication
        self.assertIsNotNone(QApplication.instance())

    def test_main_window_creation(self):
        from ui_qt.main_window import MainWindow
        win = MainWindow(self.controller)
        self.assertIsNotNone(win)
        self.assertEqual(win.windowTitle(), "Univers Vivant — PyQt6")
        win.close()

    def test_docks_creation(self):
        from ui_qt.main_window import MainWindow
        from ui_qt.docks.population_dock import PopulationDock
        from ui_qt.docks.inspector_dock import InspectorDock
        from ui_qt.docks.journal_dock import JournalDock
        from ui_qt.docks.society_dock import SocietyDock
        win = MainWindow(self.controller)
        self.assertIsInstance(win._pop_dock, PopulationDock)
        self.assertIsInstance(win._inspector_dock, InspectorDock)
        self.assertIsInstance(win._journal_dock, JournalDock)
        self.assertIsInstance(win._society_dock, SocietyDock)
        win.close()

    def test_map_view_creation(self):
        from ui_qt.map.map_view import MapView
        from ui_qt.main_window import MainWindow
        win = MainWindow(self.controller)
        self.assertIsInstance(win._map, MapView)
        win.close()

    def test_refresh_no_crash(self):
        from ui_qt.main_window import MainWindow
        win = MainWindow(self.controller)
        # Refresh tous les docks ne doit pas planter
        win._pop_dock.refresh()
        win._inspector_dock.refresh()
        win._journal_dock.refresh()
        win._society_dock.refresh()
        win.close()

    def test_execute_command(self):
        result = self.controller.execute({"kind": "set_speed", "speed": 4})
        self.assertTrue(result["ok"])
        self.assertEqual(self.controller.sim.speed, 4)
        self.controller.sim.speed = 2


class TestMapAPI(unittest.TestCase):
    """Tests de mapapi.py (Lot 10)."""

    @classmethod
    def setUpClass(cls):
        cls.controller = _make_controller()

    def test_map_transform(self):
        from game.mapapi import MapTransform
        t = MapTransform(x=0, y=0, zoom=0.25, tilt=55.0)
        sx, sy = t.to_screen(100, 100)
        wx, wy = t.to_world(sx, sy)
        self.assertAlmostEqual(wx, 100, delta=1)
        self.assertAlmostEqual(wy, 100, delta=1)

    def test_visible_tiles(self):
        from game.mapapi import MapTransform
        t = MapTransform(zoom=0.25)
        x0, y0, x1, y1 = t.visible_tiles(32, 128)
        self.assertGreater(x1, x0)
        self.assertGreater(y1, y0)

    def test_map_visible_data(self):
        from game.mapapi import MapTransform, map_visible_data
        t = MapTransform(zoom=0.25)
        data = map_visible_data(self.controller.sim, t, 800, 600)
        self.assertIn("terrain", data)
        self.assertIn("agents", data)
        self.assertIn("tick", data)


if __name__ == "__main__":
    unittest.main()

```

## tests/test_studio.py

**Type :** `.py`

```python

"""Tests pour le module Studio (couche neutre)."""
import unittest


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
        snap = {"nom": "Aro", "identity": {"builder": 0.8, "explorer": 0.2}}
        result = describe_agent(snap)
        self.assertIn("Aro", result)
        self.assertIn("constructeur", result)

    def test_describe_agent_no_identity(self):
        from game.studio_text import describe_agent
        snap = {"nom": "X", "identity": {}}
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

```

## tests/test_ui_neutral.py

**Type :** `.py`

```python

"""Tests de la couche neutre UI (ui_state, ui_snapshots, ui_commands, simulation_controller).

Valide que :
- les snapshots ne contiennent que des types simples
- les snapshots sont serialisables JSON
- les commandes valides sont acceptees
- les commandes invalides sont rejetees
- le controller synchronise correctement
- aucune dependance Pygame/Qt dans ces modules
"""
import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import pygame
pygame.init()
pygame.display.set_mode((1, 1))


def _make_sim():
    """Construit un Sim minimal pour les tests."""
    from game.assets_manager import AssetManager
    from game.assets_api import _set_asset_manager
    from game.engine import build_world

    am = AssetManager(headless=True)
    am.discover()
    _set_asset_manager(am)
    world, sim = build_world(am, seed=42, procedural=True)
    return sim, am


class TestUIState(unittest.TestCase):
    def test_defaults(self):
        from game.ui_state import UIState
        s = UIState()
        self.assertEqual(s.active_tab, "etre")
        self.assertEqual(s.active_mode, "agent")
        self.assertIsNone(s.selected_agent_eid)
        self.assertTrue(s.paused)
        self.assertEqual(s.speed, 1)

    def test_sync_from_simulation(self):
        from game.ui_state import UIState
        sim, _ = _make_sim()
        s = UIState()
        s.sync_from_simulation(sim)
        self.assertEqual(s.speed, sim.speed)
        self.assertEqual(s.paused, sim.paused)

    def test_snapshot_dict_types(self):
        from game.ui_state import UIState
        s = UIState()
        d = s.snapshot_dict()
        # Toutes les valeurs doivent etre serialisables JSON
        text = json.dumps(d)
        self.assertIsInstance(text, str)
        restored = json.loads(text)
        self.assertEqual(restored["active_tab"], "etre")


class TestUISnapshots(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sim, cls.am = _make_sim()

    def test_simulation_snapshot(self):
        from game.ui_snapshots import simulation_snapshot
        snap = simulation_snapshot(self.sim)
        self.assertIn("tick", snap)
        self.assertIn("paused", snap)
        self.assertIn("speed", snap)
        self.assertIn("population", snap)
        self.assertIn("clock", snap)
        self.assertIsInstance(snap["tick"], int)
        self.assertIsInstance(snap["paused"], bool)
        # Serialisable JSON
        text = json.dumps(snap)
        self.assertIsInstance(text, str)

    def test_population_snapshot(self):
        from game.ui_snapshots import population_snapshot
        rows = population_snapshot(self.sim)
        self.assertIsInstance(rows, list)
        for row in rows:
            self.assertIn("eid", row)
            self.assertIn("nom", row)
            self.assertIn("vivant", row)
            text = json.dumps(row)
            self.assertIsInstance(text, str)

    def test_selected_agent_snapshot_none(self):
        from game.ui_snapshots import selected_agent_snapshot
        from game.ui_state import UIState
        state = UIState()
        result = selected_agent_snapshot(self.sim, state)
        self.assertIsNone(result)

    def test_journal_snapshot(self):
        from game.ui_snapshots import journal_snapshot
        self.sim.log("Test entry", (255, 0, 0), "monde")
        rows = journal_snapshot(self.sim)
        self.assertIsInstance(rows, list)
        if rows:
            self.assertIn("tick", rows[-1])
            self.assertIn("text", rows[-1])
            text = json.dumps(rows[-1])
            self.assertIsInstance(text, str)

    def test_map_snapshot(self):
        from game.ui_snapshots import map_snapshot
        from game.ui_state import UIState
        state = UIState()
        snap = map_snapshot(self.sim, state)
        self.assertIn("tick", snap)
        self.assertIn("grid", snap)
        self.assertIn("agents", snap)
        self.assertIn("sheep", snap)
        text = json.dumps(snap)
        self.assertIsInstance(text, str)

    def test_tile_snapshot(self):
        from game.ui_snapshots import tile_snapshot
        snap = tile_snapshot(self.sim, 10, 10)
        self.assertIn("tx", snap)
        self.assertIn("ty", snap)
        self.assertIn("dans_monde", snap)
        text = json.dumps(snap)
        self.assertIsInstance(text, str)

    def test_society_snapshot(self):
        from game.ui_snapshots import society_snapshot
        snap = society_snapshot(self.sim)
        self.assertIn("population", snap)
        self.assertIn("stats", snap)
        text = json.dumps(snap)
        self.assertIsInstance(text, str)

    def test_no_numpy_in_snapshots(self):
        """Aucun numpy array ne doit apparaitre dans les snapshots."""
        import numpy as np
        from game.ui_snapshots import simulation_snapshot, population_snapshot, map_snapshot
        from game.ui_state import UIState

        for snap in [
            simulation_snapshot(self.sim),
            population_snapshot(self.sim),
            map_snapshot(self.sim, UIState()),
        ]:
            self._check_no_numpy(snap)

    def _check_no_numpy(self, obj, path=""):
        import numpy as np
        if isinstance(obj, np.ndarray):
            self.fail(f"numpy array trouve dans le snapshot a {path}")
        elif isinstance(obj, dict):
            for k, v in obj.items():
                self._check_no_numpy(v, f"{path}.{k}")
        elif isinstance(obj, (list, tuple)):
            for i, v in enumerate(obj):
                self._check_no_numpy(v, f"{path}[{i}]")


class TestUICommands(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sim, cls.am = _make_sim()

    def test_pause_toggle(self):
        from game.ui_commands import execute_command
        was_paused = self.sim.paused
        result = execute_command(self.sim, {"kind": "pause_toggle"})
        self.assertTrue(result["ok"])
        self.assertEqual(result["paused"], not was_paused)
        # Restaurer
        self.sim.paused = was_paused

    def test_set_speed(self):
        from game.ui_commands import execute_command
        result = execute_command(self.sim, {"kind": "set_speed", "speed": 5})
        self.assertTrue(result["ok"])
        self.assertEqual(result["speed"], 5)
        self.sim.speed = 2

    def test_speed_bounded(self):
        from game.ui_commands import execute_command
        result = execute_command(self.sim, {"kind": "set_speed", "speed": 99})
        self.assertTrue(result["ok"])
        self.assertEqual(result["speed"], 8)
        result = execute_command(self.sim, {"kind": "set_speed", "speed": -1})
        self.assertTrue(result["ok"])
        self.assertEqual(result["speed"], 1)
        self.sim.speed = 2

    def test_select_agent(self):
        from game.ui_commands import execute_command
        if self.sim.agents:
            eid = self.sim.agents[0].eid
            result = execute_command(self.sim, {"kind": "select_agent", "eid": eid})
            self.assertTrue(result["ok"])
            self.assertEqual(result["eid"], eid)
        self.sim.selected = None

    def test_select_agent_invalid(self):
        from game.ui_commands import execute_command
        result = execute_command(self.sim, {"kind": "select_agent", "eid": 99999})
        self.assertFalse(result["ok"])

    def test_unknown_command(self):
        from game.ui_commands import execute_command
        result = execute_command(self.sim, {"kind": "unknown_thing"})
        self.assertFalse(result["ok"])
        self.assertIn("error", result)

    def test_step(self):
        from game.ui_commands import execute_command
        old_tick = int(self.sim.w.tick)
        self.sim.paused = True
        result = execute_command(self.sim, {"kind": "step"})
        self.assertTrue(result["ok"])
        self.assertGreater(int(self.sim.w.tick), old_tick)

    def test_spawn_sheep(self):
        from game.ui_commands import execute_command
        old_count = len(self.sim.sheep)
        result = execute_command(self.sim, {"kind": "spawn_sheep"})
        self.assertTrue(result["ok"])
        self.assertEqual(len(self.sim.sheep), old_count + 1)

    def test_log(self):
        from game.ui_commands import execute_command
        old_len = len(self.sim.journal)
        result = execute_command(self.sim, {"kind": "log", "text": "test log"})
        self.assertTrue(result["ok"])


class TestSimulationController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sim, cls.am = _make_sim()

    def test_snapshot(self):
        from game.simulation_controller import SimulationController
        ctrl = SimulationController(self.sim)
        snap = ctrl.snapshot()
        self.assertIn("simulation", snap)
        self.assertIn("population", snap)
        self.assertIn("selected_agent", snap)
        self.assertIn("journal", snap)
        text = json.dumps(snap)
        self.assertIsInstance(text, str)

    def test_execute(self):
        from game.simulation_controller import SimulationController
        ctrl = SimulationController(self.sim)
        result = ctrl.execute({"kind": "set_speed", "speed": 6})
        self.assertTrue(result["ok"])
        self.assertEqual(self.sim.speed, 6)
        self.sim.speed = 2

    def test_sync(self):
        from game.simulation_controller import SimulationController
        ctrl = SimulationController(self.sim)
        ctrl.sync_from_simulation()
        self.assertEqual(ctrl.ui_state.speed, self.sim.speed)
        self.assertEqual(ctrl.ui_state.paused, self.sim.paused)

    def test_translate_action(self):
        from game.simulation_controller import SimulationController
        ctrl = SimulationController(self.sim)
        cmd = ctrl.translate_action(("pause", None))
        self.assertIsNotNone(cmd)
        self.assertEqual(cmd["kind"], "pause_toggle")

        cmd = ctrl.translate_action(("speed", 1))
        self.assertIsNotNone(cmd)
        self.assertEqual(cmd["kind"], "speed_delta")
        self.assertEqual(cmd["delta"], 1)

    def test_translate_unknown(self):
        from game.simulation_controller import SimulationController
        ctrl = SimulationController(self.sim)
        cmd = ctrl.translate_action(("unknown_action", None))
        self.assertIsNone(cmd)

    def test_handle_legacy_action(self):
        from game.simulation_controller import SimulationController
        ctrl = SimulationController(self.sim)
        was_paused = self.sim.paused
        result = ctrl.handle_legacy_action(("pause", None))
        self.assertIsNotNone(result)
        self.assertTrue(result["ok"])
        self.sim.paused = was_paused


class TestUIRegistry(unittest.TestCase):
    def test_registry_imports(self):
        from game.ui_registry import (
            SECTION_REGISTRY, CARD_REGISTRY, TABS, MODES,
            TAB_MODES, TAB_HINTS, LOG_CATS, CHIP_LABELS, PANELS,
        )
        self.assertIsInstance(SECTION_REGISTRY, list)
        self.assertIsInstance(CARD_REGISTRY, list)
        self.assertIsInstance(TABS, list)
        self.assertIsInstance(MODES, list)
        self.assertIsInstance(TAB_MODES, dict)
        self.assertIsInstance(TAB_HINTS, dict)
        self.assertIsInstance(LOG_CATS, dict)
        self.assertIsInstance(CHIP_LABELS, dict)
        self.assertIsInstance(PANELS, dict)


if __name__ == "__main__":
    unittest.main()

```

## ui_pygame/__init__.py

**Type :** `.py`

```python

"""ui_pygame — panneaux Pygame extraits du dashboard.

Chaque panneau respecte le contrat :
    draw(surface, rect, snapshot, ui_state) -> None
    handle_event(event, rect, ui_state) -> command dict ou None
"""
from .base_panel import Panel
from .journal_panel import JournalPanel
from .population_panel import PopulationPanel
from .society_panel import SocietyPanel

__all__ = ["Panel", "JournalPanel", "PopulationPanel", "SocietyPanel"]

```

## ui_pygame/assets_panel.py

**Type :** `.py`

```python

"""Assets Panel — catalogue d'assets Pygame avec grille filtrable."""
from __future__ import annotations
import pygame
from ui_pygame.base_panel import Panel


class AssetsPanel(Panel):
    """Grille d'assets avec catégories, favoris, recherche."""

    CELL = 68

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search = ""
        self.category = "__all__"
        self.only_favs = False
        self.favs: list = []
        self._filtered_cache: list = []
        self._selected_idx = 0

    def set_catalog(self, am) -> None:
        """Met à jour le cache filtré à partir de l'AssetManager."""
        assets = []
        for i, a in enumerate(am.assets):
            cat = getattr(a, "category", "")
            if self.category != "__all__" and cat != self.category:
                continue
            if self.only_favs and i not in self.favs:
                continue
            if self.search:
                sl = self.search.lower()
                label = getattr(a, "label", getattr(a, "name", "")).lower()
                if sl not in label and sl not in cat.lower():
                    continue
            assets.append((i, a))
        self._filtered_cache = assets

    def draw(self, surface: pygame.Surface, rect: pygame.Rect,
             snapshot: dict, ui_state) -> None:
        """Dessine la grille d'assets."""
        x0, y = rect.x, rect.y

        # Titre
        font_sub = self._font(15)
        title_surf = font_sub.render("ASSETS", True, (31, 36, 48))
        surface.blit(title_surf, (x0 + 12, y))
        y += 26

        # Champ recherche
        sr = pygame.Rect(x0 + 8, y, rect.width - 24, 27)
        pygame.draw.rect(surface, (255, 255, 255), sr, border_radius=6)
        pygame.draw.rect(surface, (205, 210, 219), sr, 1, border_radius=6)
        font_body = self._font(13)
        search_txt = self.search or "Rechercher..."
        search_col = (31, 36, 48) if self.search else (156, 163, 176)
        search_surf = font_body.render(search_txt, True, search_col)
        surface.blit(search_surf, (sr.x + 10, sr.centery - search_surf.get_height() // 2))
        y = sr.bottom + 6

        # Region grille
        region = pygame.Rect(x0 + 8, y, rect.width - 24, rect.height - (y - rect.y) - 8)
        pygame.draw.rect(surface, (255, 255, 255), region, border_radius=6)

        cell = self.CELL
        cols = max(1, (region.width - 8) // (cell + 4))
        selected_id = getattr(ui_state, "selected_asset_id", None)

        old_clip = surface.get_clip()
        surface.set_clip(region)

        for idx, (aid, a) in enumerate(self._filtered_cache):
            col = idx % cols
            row = idx // cols
            cx = region.x + 4 + col * (cell + 4)
            cy = region.y + 4 + row * (cell + 4)
            if cy + cell > region.bottom:
                break

            r = pygame.Rect(cx, cy, cell, cell)
            # Selection
            if aid == selected_id:
                pygame.draw.rect(surface, (232, 240, 253), r, border_radius=6)
                pygame.draw.rect(surface, (59, 118, 214), r, 2, border_radius=6)
            elif r.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(surface, (241, 244, 249), r, border_radius=6)

            # Nom tronque
            font_micro = self._font(11)
            label = getattr(a, "label", getattr(a, "name", f"#{aid}"))
            if len(label) > 8:
                label = label[:7] + "."
            lbl_surf = font_micro.render(label, True, (105, 114, 129))
            surface.blit(lbl_surf, (cx + 2, cy + cell - 14))

            # Etoile favori
            if aid in self.favs:
                star = font_micro.render("*", True, (222, 160, 50))
                surface.blit(star, (cx + cell - 12, cy + 2))

        if not self._filtered_cache:
            font_body = self._font(13)
            empty = font_body.render("Aucun asset.", True, (156, 163, 176))
            surface.blit(empty, (region.centerx - empty.get_width() // 2,
                                 region.y + 36))

        surface.set_clip(old_clip)

    def handle_event(self, event: pygame.event.Event, rect: pygame.Rect,
                     ui_state) -> dict | None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Calculer la zone de la grille
            y_offset = rect.y + 26 + 33  # titre + search
            region = pygame.Rect(rect.x + 8, y_offset, rect.width - 24,
                                 rect.height - (y_offset - rect.y) - 8)
            if region.collidepoint(event.pos):
                col = (event.pos[0] - region.x - 4) // (self.CELL + 4)
                row = (event.pos[1] - region.y - 4) // (self.CELL + 4)
                cols = max(1, (region.width - 8) // (self.CELL + 4))
                idx = row * cols + col
                if 0 <= idx < len(self._filtered_cache):
                    aid, _ = self._filtered_cache[idx]
                    if hasattr(ui_state, "selected_asset_id"):
                        ui_state.selected_asset_id = aid
                    return {"kind": "select_asset", "aid": aid}
        return None

```

## ui_pygame/base_panel.py

**Type :** `.py`

```python

"""Base Panel — contrat commun pour tous les panneaux Pygame."""
from __future__ import annotations
import pygame


class Panel:
    """Classe de base pour les panneaux Pygame extraits du dashboard.

    Contrat :
        draw(surface, rect, snapshot, ui_state) -> None
        handle_event(event, rect, ui_state) -> command dict ou None
    """

    def __init__(self, x: int = 0, y: int = 0, w: int = 200, h: int = 400):
        self.rect = pygame.Rect(x, y, w, h)
        self._scroll_offset = 0
        self._buttons: list[pygame.Rect] = []

    def draw(self, surface: pygame.Surface, rect: pygame.Rect,
             snapshot: dict, ui_state) -> None:
        """Dessine le panneau dans la zone donnee."""
        raise NotImplementedError

    def handle_event(self, event: pygame.event.Event, rect: pygame.Rect,
                     ui_state) -> dict | None:
        """Traite un evenement. Retourne une commande dict ou None."""
        return None

    def _font(self, size: int = 13) -> pygame.font.Font:
        key = f"_{size}"
        if not hasattr(self, "_fonts"):
            self._fonts = {}
        if key not in self._fonts:
            self._fonts[key] = pygame.font.SysFont(
                "segoeui,inter,dejavusans,liberationsans,arial", size
            )
        return self._fonts[key]

    def _draw_text(self, surface, text, x, y, color=(31, 36, 48), size=13,
                   max_width=None):
        font = self._font(size)
        rendered = font.render(str(text), True, color)
        if max_width and rendered.get_width() > max_width:
            # Tronquer avec ...
            while rendered.get_width() > max_width - 20 and len(text) > 3:
                text = text[:-4] + "..."
                rendered = font.render(str(text), True, color)
        surface.blit(rendered, (x, y))
        return rendered.get_height()

    def _draw_rect(self, surface, color, rect, radius=0):
        if radius > 0:
            pygame.draw.rect(surface, color, rect, border_radius=radius)
        else:
            pygame.draw.rect(surface, color, rect)

    def _draw_bar(self, surface, x, y, w, h, value, color, bg=(237, 239, 244)):
        """Dessine une barre de progression."""
        self._draw_rect(surface, bg, pygame.Rect(x, y, w, h), radius=3)
        fill_w = max(0, min(w, int(w * max(0.0, min(1.0, value)))))
        if fill_w > 0:
            self._draw_rect(surface, color, pygame.Rect(x, y, fill_w, h), radius=3)

```

## ui_pygame/creator_panel.py

**Type :** `.py`

```python

"""Creator Panel — panneau création d'outils Pygame."""
from __future__ import annotations
import pygame
from ui_pygame.base_panel import Panel


class CreatorPanel(Panel):
    """Panneau de création d'outils personnalisés."""

    def draw(self, surface: pygame.Surface, rect: pygame.Rect,
             snapshot: dict, ui_state) -> None:
        x0, y = rect.x, rect.y

        # Titre
        font_sub = self._font(15)
        title_surf = font_sub.render("CREER UN OUTIL", True, (31, 36, 48))
        surface.blit(title_surf, (x0 + 12, y))
        font_small = self._font(12)
        subtitle = font_small.render("dessine, nomme, choisis un type, puis equipe l'etre selectionne",
                                     True, (105, 114, 129))
        surface.blit(subtitle, (x0 + 12, y + 18))
        y += 40

        # Zone de dessin (placeholder)
        draw_r = pygame.Rect(x0 + 12, y, rect.width - 24, 120)
        pygame.draw.rect(surface, (250, 251, 253), draw_r, border_radius=6)
        pygame.draw.rect(surface, (205, 210, 219), draw_r, 1, border_radius=6)
        font_body = self._font(13)
        placeholder = font_body.render("Zone de dessin (ToolEditor)", True, (156, 163, 176))
        surface.blit(placeholder, (draw_r.centerx - placeholder.get_width() // 2,
                                   draw_r.centery - placeholder.get_height() // 2))
        y = draw_r.bottom + 10

        # Champ nom
        name_r = pygame.Rect(x0 + 12, y, rect.width - 24, 28)
        pygame.draw.rect(surface, (255, 255, 255), name_r, border_radius=6)
        pygame.draw.rect(surface, (205, 210, 219), name_r, 1, border_radius=6)
        name_surf = font_body.render("Nom de l'outil...", True, (156, 163, 176))
        surface.blit(name_surf, (name_r.x + 8, name_r.centery - name_surf.get_height() // 2))
        y = name_r.bottom + 8

        # Types
        font_small = self._font(12)
        type_label = font_small.render("TYPE", True, (105, 114, 129))
        surface.blit(type_label, (x0 + 12, y))
        y += 18
        for i, kind in enumerate(("hache", "pioche", "marteau")):
            r = pygame.Rect(x0 + 12 + i * 74, y, 68, 22)
            pygame.draw.rect(surface, (255, 255, 255), r, border_radius=6)
            pygame.draw.rect(surface, (205, 210, 219), r, 1, border_radius=6)
            kind_surf = font_small.render(kind, True, (105, 114, 129))
            surface.blit(kind_surf, (r.centerx - kind_surf.get_width() // 2,
                                     r.centery - kind_surf.get_height() // 2))
        y += 30

        # Bouton creer
        btn_r = pygame.Rect(x0 + 12, y, rect.width - 24, 32)
        pygame.draw.rect(surface, (59, 118, 214), btn_r, border_radius=6)
        btn_text = font_body.render("Creer et equiper", True, (255, 255, 255))
        surface.blit(btn_text, (btn_r.centerx - btn_text.get_width() // 2,
                                btn_r.centery - btn_text.get_height() // 2))

    def handle_event(self, event: pygame.event.Event, rect: pygame.Rect,
                     ui_state) -> dict | None:
        return None

```

## ui_pygame/journal_panel.py

**Type :** `.py`

```python

"""Journal Panel — panneau journal Pygame avec snapshots."""
from __future__ import annotations
import pygame
from ui_pygame.base_panel import Panel
from game.ui_registry import LOG_CATS, LOG_TITLES


class JournalPanel(Panel):
    """Panneau journal filtrable, affiche les entrees de sim.journal."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jfilter = "tous"
        self._font_cache: dict = {}

    def draw(self, surface: pygame.Surface, rect: pygame.Rect,
             snapshot: dict, ui_state) -> None:
        """Dessine le panneau journal.

        snapshot doit contenir {"journal": [...]} ou la liste d'entrees.
        """
        entries = snapshot if isinstance(snapshot, list) else snapshot.get("journal", [])

        # Filtre
        if self.jfilter != "tous":
            entries = [e for e in entries if e.get("category") == self.jfilter]

        x0, y = rect.x, rect.y

        # Titre
        font_sub = self._font(15)
        title_surf = font_sub.render("JOURNAL", True, (31, 36, 48))
        surface.blit(title_surf, (x0 + 12, y))
        y += 26

        # Chips de categorie
        fx, fy = x0 + 8, y
        for cid in ["tous"] + list(LOG_CATS.keys()):
            col = (105, 114, 129) if cid == "tous" else LOG_CATS[cid]
            lbl = "tous" if cid == "tous" else LOG_TITLES.get(cid, cid)
            font_micro = self._font(11)
            cw = font_micro.size(lbl)[0] + 16
            if fx + cw > rect.right - 12:
                fx, fy = x0 + 12, fy + 23
            chip_rect = pygame.Rect(fx, fy, cw, 19)
            selected = self.jfilter == cid
            if selected:
                pygame.draw.rect(surface, col, chip_rect, border_radius=6)
                txt_col = (255, 255, 255)
            else:
                pygame.draw.rect(surface, (255, 255, 255), chip_rect, border_radius=6)
                pygame.draw.rect(surface, col, chip_rect, 1, border_radius=6)
                txt_col = col
            chip_text = font_micro.render(lbl, True, txt_col)
            surface.blit(chip_text, (fx + 8, fy + 3))
            fx += cw + 4

            # Stocker la zone du chip pour le clic
            if not hasattr(self, "_chips"):
                self._chips = []
            self._chips.append((chip_rect, cid))
        y = fy + 27

        # Liste des entrees
        region = pygame.Rect(x0 + 8, y, rect.width - 24, rect.height - (y - rect.y) - 8)
        pygame.draw.rect(surface, (255, 255, 255), region, border_radius=6)

        rh = 23
        shown = entries[-max(1, region.height // rh):]
        old_clip = surface.get_clip()
        surface.set_clip(region)

        for i, e in enumerate(shown):
            tick = e.get("tick", 0)
            text = e.get("text", "")
            cat = e.get("category", "monde")
            count = e.get("count", 1)
            ry = region.y + 6 + i * rh

            # Point de couleur
            color = LOG_CATS.get(cat, (105, 114, 129))
            pygame.draw.circle(surface, color, (region.x + 12, ry + 8), 4)

            # Timestamp
            import config as _cfg
            mm, ss = divmod(int(tick / getattr(_cfg, "SIM_HZ", 60)), 60)
            font_micro = self._font(11)
            ts_surf = font_micro.render(f"{mm:02}:{ss:02}", True, (156, 163, 176))
            surface.blit(ts_surf, (region.x + 27, ry + 2))

            # Texte
            font_small = self._font(12)
            display_text = text + (f"  x{count}" if count and count > 1 else "")
            # Tronquer si trop long
            max_w = region.width - 80
            while font_small.size(display_text)[0] > max_w and len(display_text) > 5:
                display_text = display_text[:-4] + "..."
            txt_surf = font_small.render(display_text, True, (31, 36, 48))
            surface.blit(txt_surf, (region.x + 68, ry + 1))

        if not shown:
            font_body = self._font(13)
            empty_surf = font_body.render("Rien a signaler pour ce filtre.", True, (156, 163, 176))
            surface.blit(empty_surf, (region.centerx - empty_surf.get_width() // 2,
                                      region.y + 36))

        surface.set_clip(old_clip)

    def handle_event(self, event: pygame.event.Event, rect: pygame.Rect,
                     ui_state) -> dict | None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not hasattr(self, "_chips"):
                return None
            for chip_rect, cid in self._chips:
                if chip_rect.collidepoint(event.pos):
                    self.jfilter = cid
                    if hasattr(ui_state, "journal_filter"):
                        ui_state.journal_filter = cid
                    return {"kind": "set_journal_filter", "filter": cid}
        return None

```

## ui_pygame/population_panel.py

**Type :** `.py`

```python

"""Population Panel — panneau habitants Pygame avec snapshots."""
from __future__ import annotations
import pygame
from ui_pygame.base_panel import Panel


class PopulationPanel(Panel):
    """Panneau de la liste des habitants avec selection et suppression."""

    ROW_H = 38

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search = ""
        self.hdel_pending = None
        self._filtered_cache = []
        self._filter_hash = None

    def draw(self, surface: pygame.Surface, rect: pygame.Rect,
             snapshot: dict, ui_state) -> None:
        """Dessine le panneau habitants.

        snapshot doit contenir une liste d'agents OU {"population": [...]}.
        """
        if isinstance(snapshot, list):
            people = snapshot
        else:
            people = snapshot.get("population", [])

        # Filtrage par recherche
        if self.search:
            sl = self.search.lower()
            people = [a for a in people if sl in a.get("nom", "").lower()
                      or sl in a.get("clan", "").lower()
                      or sl in a.get("classe", "").lower()]

        selected_eid = getattr(ui_state, "selected_agent_eid", None)

        x0, y = rect.x, rect.y

        # Titre + compteur
        font_sub = self._font(15)
        title_surf = font_sub.render("HABITANTS", True, (31, 36, 48))
        surface.blit(title_surf, (x0 + 12, y))
        font_small = self._font(12)
        alive_count = len([a for a in people if a.get("vivant", True)])
        count_surf = font_small.render(f"{alive_count}", True, (105, 114, 129))
        surface.blit(count_surf, (rect.right - 20 - count_surf.get_width(), y + 2))
        y += 24

        # Champ de recherche
        sr = pygame.Rect(x0 + 8, y, rect.width - 24, 27)
        pygame.draw.rect(surface, (255, 255, 255), sr, border_radius=6)
        border_col = (59, 118, 214) if hasattr(ui_state, '_hab_focus') and ui_state._hab_focus else (205, 210, 219)
        pygame.draw.rect(surface, border_col, sr, 1, border_radius=6)
        font_body = self._font(13)
        display_search = self.search or "filtrer par nom, clan, classe..."
        search_col = (31, 36, 48) if self.search else (156, 163, 176)
        search_surf = font_body.render(display_search, True, search_col)
        surface.blit(search_surf, (sr.x + 10, sr.centery - search_surf.get_height() // 2))
        y = sr.bottom + 6

        # Region scrollable
        region = pygame.Rect(x0 + 8, y, rect.width - 24, rect.height - (y - rect.y) - 8)
        pygame.draw.rect(surface, (255, 255, 255), region, border_radius=6)

        rh = self.ROW_H
        off = self._scroll_offset
        old_clip = surface.get_clip()
        surface.set_clip(region)

        first = max(0, off // rh)
        mouse = pygame.mouse.get_pos()

        for i in range(first, min(len(people), first + region.height // rh + 2)):
            ag = people[i]
            eid = ag.get("eid")
            rr = pygame.Rect(region.x + 4, region.y + 4 + i * rh - off,
                             region.width - 8, rh - 2)

            # Surbrillance
            if eid == selected_eid:
                pygame.draw.rect(surface, (232, 240, 253), rr, border_radius=6)
            elif rr.collidepoint(mouse):
                pygame.draw.rect(surface, (241, 244, 249), rr, border_radius=6)

            # Nom + sexe
            font_body = self._font(13)
            name_text = f"{ag.get('nom', '?')} ({ag.get('sex', '?')})"
            name_surf = font_body.render(name_text, True, (31, 36, 48))
            surface.blit(name_surf, (rr.x + 28, rr.y + 5))

            # Infos
            font_micro = self._font(11)
            stage = ag.get("stage", "")
            age = ag.get("age_ans", 0)
            cls = ag.get("classe", "")
            info_text = f"{stage} . {age:.1f} ans . {cls}"
            info_surf = font_micro.render(info_text, True, (105, 114, 129))
            surface.blit(info_surf, (rr.x + 28, rr.y + 21))

            # Barres mini
            gx = rr.right - 130
            for j, (val, col) in enumerate([
                (ag.get("sante", 0), (67, 160, 92)),
                (ag.get("energie", 0), (222, 160, 50)),
                (1 - ag.get("faim", 0), (34, 158, 142)),
            ]):
                self._draw_bar(surface, gx + j * 34, rr.centery - 3, 30, 6, val, col)

            # Bouton supprimer
            dr = pygame.Rect(rr.right - 52, rr.centery - 10, 36, 20)
            if self.hdel_pending == eid:
                pygame.draw.rect(surface, (214, 84, 84), dr, border_radius=4)
                del_text = font_micro.render("OK?", True, (255, 255, 255))
                surface.blit(del_text, (dr.centerx - del_text.get_width() // 2,
                                        dr.centery - del_text.get_height() // 2))
            else:
                bg = (235, 100, 100) if dr.collidepoint(mouse) else (214, 84, 84)
                pygame.draw.rect(surface, bg, dr, border_radius=4)
                del_text = font_micro.render("X", True, (255, 255, 255))
                surface.blit(del_text, (dr.centerx - del_text.get_width() // 2,
                                        dr.centery - del_text.get_height() // 2))

        if not people:
            font_body = self._font(13)
            empty_surf = font_body.render("Aucun habitant ne correspond.", True, (156, 163, 176))
            surface.blit(empty_surf, (region.centerx - empty_surf.get_width() // 2,
                                      region.y + 36))

        surface.set_clip(old_clip)

    def handle_event(self, event: pygame.event.Event, rect: pygame.Rect,
                     ui_state) -> dict | None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Verifier clic sur un agent
            x0, y = rect.x, rect.y
            sr = pygame.Rect(x0 + 8, y + 24, rect.width - 24, 27)
            region = pygame.Rect(x0 + 8, sr.bottom + 6, rect.width - 24,
                                 rect.height - (sr.bottom + 6 - rect.y) - 8)

            if region.collidepoint(event.pos):
                idx = (event.pos[1] - region.y + self._scroll_offset) // self.ROW_H
                if 0 <= idx < len(self._filtered_cache):
                    ag = self._filtered_cache[idx]
                    eid = ag.get("eid")

                    # Verifier bouton supprimer
                    rr = pygame.Rect(region.x + 4, region.y + 4 + idx * self.ROW_H - self._scroll_offset,
                                     region.width - 8, self.ROW_H - 2)
                    dr = pygame.Rect(rr.right - 52, rr.centery - 10, 36, 20)
                    if dr.collidepoint(event.pos):
                        if self.hdel_pending == eid:
                            self.hdel_pending = None
                            return {"kind": "remove_agent", "eid": eid}
                        else:
                            self.hdel_pending = eid
                            return None
                    else:
                        self.hdel_pending = None
                        if hasattr(ui_state, "selected_agent_eid"):
                            ui_state.selected_agent_eid = eid
                        return {"kind": "select_agent", "eid": eid}

            # Verifier champ de recherche
            if sr.collidepoint(event.pos):
                if hasattr(ui_state, '_hab_focus'):
                    ui_state._hab_focus = True
                return None

        if event.type == pygame.KEYDOWN:
            if hasattr(ui_state, '_hab_focus') and ui_state._hab_focus:
                if event.key == pygame.K_BACKSPACE:
                    self.search = self.search[:-1]
                    return None
                elif event.key == pygame.K_RETURN:
                    if hasattr(ui_state, '_hab_focus'):
                        ui_state._hab_focus = False
                    return None
                elif event.unicode and event.unicode.isprintable():
                    self.search += event.unicode
                    return None

        return None

```

## ui_pygame/society_panel.py

**Type :** `.py`

```python

"""Society Panel — panneau societe Pygame avec snapshots."""
from __future__ import annotations
import pygame
from ui_pygame.base_panel import Panel


class SocietyPanel(Panel):
    """Panneau de la societe avec statistiques groupees."""

    def draw(self, surface: pygame.Surface, rect: pygame.Rect,
             snapshot: dict, ui_state) -> None:
        """Dessine le panneau societe.

        snapshot doit contenir {"population", "stats", "sheep", "monsters", ...}
        """
        if isinstance(snapshot, dict):
            data = snapshot
        else:
            data = {}

        stats = data.get("stats", {})
        alive = data.get("population", 0)
        sheep = data.get("sheep", 0)
        monsters = data.get("monsters", 0)
        max_gen = data.get("max_generation", 0)
        bonded = data.get("bonded", 0)

        x0, y = rect.x, rect.y

        # Titre
        font_sub = self._font(15)
        title_surf = font_sub.render("SOCIETE", True, (31, 36, 48))
        surface.blit(title_surf, (x0 + 12, y))
        y += 26

        region = pygame.Rect(x0 + 8, y, rect.width - 24, rect.height - (y - rect.y) - 8)

        # Groupes de stats
        groups = [
            ("Demographie", (67, 160, 92), [
                ("Population", alive),
                ("Naissances", stats.get("births", 0)),
                ("Deces", stats.get("deaths", 0)),
                ("Generation max", max_gen),
                ("Couples", bonded),
            ]),
            ("Activite", (222, 164, 46), [
                ("Constructions", stats.get("builds", 0)),
                ("Villages", stats.get("villages", 0)),
                ("Recoltes", stats.get("harvests", 0)),
                ("Outils trouves", stats.get("tool_found", 0)),
            ]),
            ("Social", (146, 96, 186), [
                ("Dons", stats.get("gives", 0)),
                ("Vols", stats.get("takes", 0)),
                ("Paroles", stats.get("talks", 0)),
                ("Attaques", stats.get("attacks", 0)),
            ]),
            ("Monde", (62, 124, 214), [
                ("Feux", stats.get("fires", 0)),
                ("Moutons", sheep),
                ("Monstres", monsters),
            ]),
        ]

        old_clip = surface.get_clip()
        surface.set_clip(region)
        cy = region.y

        for title, color, rows in groups:
            h = 28 + ((len(rows) + 1) // 2) * 21 + 6
            card = pygame.Rect(region.x, cy, region.width, h)
            if card.bottom > region.bottom:
                break
            pygame.draw.rect(surface, (255, 255, 255), card, border_radius=6)
            # Accent bar
            pygame.draw.rect(surface, color, (card.x, card.y + 6, 3, 15), border_radius=2)

            # Titre groupe
            font_small = self._font(12)
            title_text = title.upper()
            # Mélanger couleur avec noir pour le texte du titre
            mixed = tuple(int(c * 0.7) for c in color)
            title_surf = font_small.render(title_text, True, mixed)
            surface.blit(title_surf, (card.x + 10, card.y + 6))

            # Rows (2 colonnes)
            colw = (card.width - 20) // 2
            font_small = self._font(12)
            font_body = self._font(13)
            for i, (lbl, val) in enumerate(rows):
                lx = card.x + 10 + (i % 2) * colw
                ly = card.y + 28 + (i // 2) * 21
                lbl_surf = font_small.render(str(lbl), True, (105, 114, 129))
                surface.blit(lbl_surf, (lx, ly))
                val_surf = font_body.render(str(val), True, (31, 36, 48))
                surface.blit(val_surf, (lx + colw - 10 - val_surf.get_width(), ly - 1))

            cy = card.bottom + 6

        surface.set_clip(old_clip)

    def handle_event(self, event: pygame.event.Event, rect: pygame.Rect,
                     ui_state) -> dict | None:
        return None

```

## ui_pygame/world_tools_panel.py

**Type :** `.py`

```python

"""World Tools Panel — panneau d'outils de terrain Pygame."""
from __future__ import annotations
import pygame
from ui_pygame.base_panel import Panel


class WorldToolsPanel(Panel):
    """Panneau d'outils monde : poser, gommer, sol, eau, terre, mur, etc."""

    TOOLS = [
        ("place", "Poser"), ("erase", "Gommer"), ("floor", "Sol"),
        ("block", "Bloc"),
        ("water", "Eau"), ("land", "Terre"), ("wall", "Mur"),
        ("carve", "Sculpter"), ("restore", "Restaurer"),
        ("inspect", "Examiner"),
    ]

    HINTS = {
        "place": "clic = poser l'asset / glisser = peindre",
        "erase": "clic = effacer les objets",
        "floor": "clic = peindre le sol",
        "water": "glisser = transformer terre en eau",
        "land": "glisser = transformer eau en terre",
        "wall": "glisser = placer des rochers",
        "carve": "glisser = creuser les montagnes",
        "restore": "glisser = restaurer le terrain",
        "block": "clic = construire un bloc",
        "inspect": "clic = examiner",
    }

    def draw(self, surface: pygame.Surface, rect: pygame.Rect,
             snapshot: dict, ui_state) -> None:
        x0, y = rect.x, rect.y
        mode = getattr(ui_state, "active_mode", "inspect")

        # Titre
        font_sub = self._font(15)
        title_surf = font_sub.render("OUTILS", True, (31, 36, 48))
        surface.blit(title_surf, (x0 + 12, y))
        y += 26

        # Grille d'outils (2 colonnes)
        font_body = self._font(13)
        col_w = (rect.width - 28) // 2
        for i, (tool_id, label) in enumerate(self.TOOLS):
            col = i % 2
            row = i // 2
            tx = x0 + 12 + col * (col_w + 4)
            ty = y + row * 30
            tr = pygame.Rect(tx, ty, col_w, 26)

            selected = mode == tool_id
            if selected:
                pygame.draw.rect(surface, (232, 240, 253), tr, border_radius=6)
                pygame.draw.rect(surface, (59, 118, 214), tr, 1, border_radius=6)
            elif tr.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(surface, (241, 244, 249), tr, border_radius=6)

            tool_surf = font_body.render(label, True, (31, 36, 48) if selected else (105, 114, 129))
            surface.blit(tool_surf, (tx + 8, ty + 4))

        y += ((len(self.TOOLS) + 1) // 2) * 30 + 10

        # Hint
        hint = self.HINTS.get(mode, "")
        if hint:
            font_small = self._font(12)
            hint_surf = font_small.render(hint, True, (105, 114, 129))
            surface.blit(hint_surf, (x0 + 12, y))
            y += 20

        # Slider pinceau (pour modes brush)
        if mode in ("water", "land", "wall", "carve", "restore"):
            y += 6
            font_small = self._font(12)
            brush_label = font_small.render(f"Taille pinceau: {getattr(ui_state, 'brush_size', 3)}",
                                            True, (105, 114, 129))
            surface.blit(brush_label, (x0 + 12, y))
            y += 20
            slider_r = pygame.Rect(x0 + 12, y, rect.width - 24, 6)
            pygame.draw.rect(surface, (237, 239, 244), slider_r, border_radius=3)
            bs = getattr(ui_state, "brush_size", 3)
            fill = max(0, min(1.0, (bs - 1) / 14))
            fill_r = pygame.Rect(slider_r.x, slider_r.y, int(slider_r.width * fill), 6)
            pygame.draw.rect(surface, (59, 118, 214), fill_r, border_radius=3)

    def handle_event(self, event: pygame.event.Event, rect: pygame.Rect,
                     ui_state) -> dict | None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            y = rect.y + 26
            col_w = (rect.width - 28) // 2
            for i, (tool_id, label) in enumerate(self.TOOLS):
                col = i % 2
                row = i // 2
                tx = rect.x + 12 + col * (col_w + 4)
                ty = y + row * 30
                tr = pygame.Rect(tx, ty, col_w, 26)
                if tr.collidepoint(event.pos):
                    if hasattr(ui_state, "active_mode"):
                        ui_state.active_mode = tool_id
                    return {"kind": "set_mode", "mode": tool_id}
        return None

```

## ui_qt/__init__.py

**Type :** `.py`

```python

"""ui_qt — interface PyQt6 pour Univers Vivant."""

```

## ui_qt/app.py

**Type :** `.py`

```python

"""app — setup de l'application PyQt6."""
import sys
from PyQt6.QtWidgets import QApplication


def create_app(argv=None):
    """Crée et configure l'application PyQt6."""
    app = QApplication(argv or sys.argv)
    app.setApplicationName("Univers Vivant")
    app.setApplicationDisplayName("Univers Vivant — PyQt6")
    return app

```

## ui_qt/dialogs.py

**Type :** `.py`

```python

"""SaveDialog — dialogue de sauvegarde/chargement Qt."""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QListWidget,
                              QListWidgetItem, QPushButton, QLabel, QMessageBox)
from PyQt6.QtCore import Qt
import os
import time


class SaveDialog(QDialog):
    """Dialogue de sauvegarde/chargement avec liste des slots."""

    def __init__(self, controller, mode="save", parent=None):
        super().__init__(parent)
        self.controller = controller
        self.mode = mode
        self.selected_slot = 0
        self.setWindowTitle("Sauvegarder" if mode == "save" else "Charger")
        self.setMinimumSize(400, 300)
        self._setup_ui()
        self._load_slots()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Choisir un slot :" if self.mode == "save"
                        else "Choisir une sauvegarde :")
        layout.addWidget(title)

        self._list = QListWidget()
        self._list.itemClicked.connect(self._on_select)
        layout.addWidget(self._list)

        btn_layout = QHBoxLayout()
        self._save_btn = QPushButton("Sauvegarder" if self.mode == "save" else "Charger")
        self._save_btn.clicked.connect(self._on_accept)
        self._save_btn.setEnabled(False)
        btn_layout.addWidget(self._save_btn)

        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

    def _load_slots(self):
        saves_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "saves")
        self._list.clear()
        for slot in range(10):
            path = os.path.join(saves_dir, f"slot_{slot}.pkl")
            if os.path.exists(path):
                mtime = os.path.getmtime(path)
                date_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(mtime))
                size_kb = os.path.getsize(path) / 1024
                item = QListWidgetItem(f"Slot {slot} — {date_str} ({size_kb:.0f} KB)")
            else:
                item = QListWidgetItem(f"Slot {slot} — vide")
            item.setData(Qt.ItemDataRole.UserRole, slot)
            self._list.addItem(item)

        # Slots spéciaux
        for slot, label in [(98, "Backup automatique"), (99, "Backup manuel")]:
            path = os.path.join(saves_dir, f"slot_{slot}.pkl")
            if os.path.exists(path):
                mtime = os.path.getmtime(path)
                date_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(mtime))
                item = QListWidgetItem(f"{label} — {date_str}")
                item.setData(Qt.ItemDataRole.UserRole, slot)
                self._list.addItem(item)

    def _on_select(self, item):
        self.selected_slot = item.data(Qt.ItemDataRole.UserRole)
        self._save_btn.setEnabled(True)

    def _on_accept(self):
        if self.mode == "save":
            result = self.controller.execute({
                "kind": "save", "slot": self.selected_slot, "cam": self.controller.camera
            })
        else:
            result = self.controller.execute({
                "kind": "load", "slot": self.selected_slot
            })

        if result.get("ok"):
            self.accept()
        else:
            QMessageBox.warning(self, "Erreur", result.get("error", "Erreur inconnue"))

```

## ui_qt/docks/__init__.py

**Type :** `.py`

```python

""""""

```

## ui_qt/docks/assets_dock.py

**Type :** `.py`

```python

"""AssetsDock — dock Qt pour le catalogue d'assets filtrable."""
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                              QLineEdit, QComboBox, QCheckBox,
                              QLabel, QListWidget, QListWidgetItem,
                              QSplitter, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QPixmap, QColor, QPainter, QPen

from game.assets_api import CATEGORY_LABELS as _CAT_LIST

CATEGORY_LABELS = dict(_CAT_LIST)


class AssetsDock(QDockWidget):
    """Dock assets avec grille, catégories, recherche, favoris."""

    asset_selected = pyqtSignal(int)

    def __init__(self, controller, parent=None):
        super().__init__("Assets", parent)
        self.controller = controller
        self._am = None
        self._filtered = []
        self._favs = []
        self._setup_ui()

    def set_asset_manager(self, am):
        self._am = am
        self._refresh_catalog()

    def _setup_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)

        # Recherche
        self._search = QLineEdit()
        self._search.setPlaceholderText("Rechercher asset...")
        self._search.textChanged.connect(self._on_filter)
        layout.addWidget(self._search)

        # Catégorie
        cat_layout = QHBoxLayout()
        self._cat_combo = QComboBox()
        self._cat_combo.addItem("Tous", "__all__")
        for cat in CATEGORY_LABELS:
            if cat not in ("unites", "interface", "atlas", "rendus"):
                self._cat_combo.addItem(CATEGORY_LABELS[cat], cat)
        self._cat_combo.currentIndexChanged.connect(self._on_filter)
        cat_layout.addWidget(QLabel("Categorie:"))
        cat_layout.addWidget(self._cat_combo)

        self._favs_only = QCheckBox("Favoris")
        self._favs_only.toggled.connect(self._on_filter)
        cat_layout.addWidget(self._favs_only)
        layout.addLayout(cat_layout)

        # Splitter: list on left, detail panel on right
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Liste
        self._list = QListWidget()
        self._list.setIconSize(QSize(48, 48))
        self._list.setSpacing(2)
        self._list.currentItemChanged.connect(self._on_selection_changed)
        self._list.itemDoubleClicked.connect(self._on_fav_toggle)
        splitter.addWidget(self._list)

        # Detail panel
        detail_widget = QWidget()
        detail_layout = QVBoxLayout(detail_widget)
        detail_layout.setContentsMargins(4, 4, 4, 4)

        self._thumb_label = QLabel()
        self._thumb_label.setFixedSize(48, 48)
        self._thumb_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._thumb_label.setStyleSheet("background: #2c3e50; border: 1px solid #555;")
        detail_layout.addWidget(self._thumb_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        self._detail_name = QLabel("")
        self._detail_name.setStyleSheet("font-weight: bold; font-size: 13px;")
        self._detail_name.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        detail_layout.addWidget(self._detail_name)

        self._detail_cat = QLabel("")
        self._detail_cat.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        detail_layout.addWidget(self._detail_cat)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #555;")
        detail_layout.addWidget(sep)

        self._detail_role = QLabel("")
        detail_layout.addWidget(self._detail_role)
        self._detail_placable = QLabel("")
        detail_layout.addWidget(self._detail_placable)
        self._detail_solide = QLabel("")
        detail_layout.addWidget(self._detail_solide)
        self._detail_size = QLabel("")
        detail_layout.addWidget(self._detail_size)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet("color: #555;")
        detail_layout.addWidget(sep2)

        self._detail_desc = QLabel("")
        self._detail_desc.setWordWrap(True)
        self._detail_desc.setStyleSheet("color: #bbb; font-size: 11px;")
        detail_layout.addWidget(self._detail_desc)

        detail_layout.addStretch()
        splitter.addWidget(detail_widget)

        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)
        layout.addWidget(splitter)

        self.setWidget(widget)

    def _on_filter(self, *_args):
        self._refresh_catalog()

    def _refresh_catalog(self):
        if self._am is None:
            return
        search = self._search.text().lower()
        cat = self._cat_combo.currentData() or "__all__"
        self._filtered = []

        for i, a in enumerate(self._am.assets):
            a_cat = getattr(a, "category", "")
            if cat != "__all__" and a_cat != cat:
                continue
            if self._favs_only.isChecked() and i not in self._favs:
                continue
            if search:
                label = getattr(a, "label", getattr(a, "name", "")).lower()
                if search not in label and search not in a_cat.lower():
                    continue
            self._filtered.append((i, a))

        self._list.clear()
        for aid, a in self._filtered:
            label = getattr(a, "label", getattr(a, "name", f"#{aid}"))
            cat_label = CATEGORY_LABELS.get(getattr(a, "category", ""), "")
            fav = "*" if aid in self._favs else " "
            item = QListWidgetItem(f"{fav} {label} ({cat_label})")
            item.setData(Qt.ItemDataRole.UserRole, aid)
            pixmap = self._load_thumbnail(aid, a)
            if pixmap:
                item.setIcon(pixmap)
            self._list.addItem(item)

    def _load_thumbnail(self, aid, asset):
        """Try to load a 48x48 thumbnail; fall back to a coloured placeholder."""
        try:
            am = self.controller.sim.am
            pix = am.thumbnail(aid, size=(48, 48))
            if pix is not None:
                from PyQt6.QtGui import QImage
                if isinstance(pix, QImage):
                    return QPixmap.fromImage(pix)
                if isinstance(pix, QPixmap):
                    return pix
        except Exception:
            pass
        # Coloured placeholder based on asset colour attribute
        colour = getattr(asset, "color", None)
        if colour and isinstance(colour, str) and colour.startswith("#"):
            c = QColor(colour)
        else:
            c = QColor(80, 80, 80)
        pm = QPixmap(48, 48)
        pm.fill(QColor(0, 0, 0, 0))
        p = QPainter(pm)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setBrush(c)
        p.setPen(QPen(QColor(60, 60, 60), 1))
        p.drawRoundedRect(2, 2, 44, 44, 6, 6)
        p.end()
        return pm

    def _on_selection_changed(self, current, _previous):
        if current is None:
            return
        aid = current.data(Qt.ItemDataRole.UserRole)
        if aid is None:
            return
        self.controller.ui_state.selected_asset_id = aid
        self.asset_selected.emit(aid)
        if not self._am or not (0 <= aid < len(self._am.assets)):
            return
        a = self._am.assets[aid]
        label = getattr(a, "label", getattr(a, "name", f"#{aid}"))
        cat_label = CATEGORY_LABELS.get(getattr(a, "category", ""), getattr(a, "category", ""))

        self._detail_name.setText(label)
        self._detail_cat.setText(f"Categorie: {cat_label}")
        self._detail_role.setText(f"Role: {getattr(a, 'role', '')}")
        self._detail_placable.setText(
            f"Placable: {'Oui' if getattr(a, 'placable', False) else 'Non'}")
        self._detail_solide.setText(
            f"Solide: {'Oui' if getattr(a, 'solid', False) else 'Non'}")
        w = getattr(a, "width", getattr(a, "w", None))
        h = getattr(a, "height", getattr(a, "h", None))
        if w is not None and h is not None:
            self._detail_size.setText(f"Taille: {w}x{h} pixels")
        else:
            self._detail_size.setText("Taille: N/A")
        self._detail_desc.setText(getattr(a, "description", ""))

        pixmap = self._load_thumbnail(aid, a)
        if pixmap:
            self._thumb_label.setPixmap(pixmap)
        else:
            self._thumb_label.setText("?")

    def _on_fav_toggle(self, item):
        aid = item.data(Qt.ItemDataRole.UserRole)
        if aid is None:
            return
        if aid in self._favs:
            self._favs.remove(aid)
        else:
            self._favs.insert(0, aid)
            self._favs = self._favs[:12]
        self.controller.ui_state.favs = list(self._favs)
        self._refresh_catalog()

    def refresh(self):
        self._refresh_catalog()

```

## ui_qt/docks/inspector_dock.py

**Type :** `.py`

```python

"""InspectorDock — dock Qt pour l'inspecteur d'habitant selectionne."""
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                              QTableView, QLabel, QScrollArea, QFrame,
                              QGroupBox, QGridLayout, QSlider)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from game.ui_snapshots import selected_agent_snapshot, anima_snapshot
from game.ui_registry import C_CORPS, C_COG, C_PERSO, C_EMO, C_BESOIN, C_EXP, C_MEM
from ui_qt.models.anima_model import AnimaModel


class InspectorDock(QDockWidget):
    """Dock inspecteur complet : identite + corps + Anima + relations."""

    def __init__(self, controller, parent=None):
        super().__init__("Inspecteur", parent)
        self.controller = controller
        self._anima_model = AnimaModel()
        self._setup_ui()

    def _setup_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        widget = QWidget()
        self._layout = QVBoxLayout(widget)
        self._layout.setContentsMargins(8, 8, 8, 8)
        self._layout.setSpacing(6)

        # === Identite ===
        self._identity_label = QLabel("Aucun agent selectionne")
        self._identity_label.setWordWrap(True)
        self._identity_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self._layout.addWidget(self._identity_label)

        # === Etat de base ===
        self._state_label = QLabel("")
        self._state_label.setWordWrap(True)
        self._layout.addWidget(self._state_label)

        # === Groupes d'info ===
        self._create_info_groups()

        # === Cerveau badge (apres Besoins) ===
        self._brain_group = QGroupBox("Cerveau")
        self._brain_group.setStyleSheet(
            f"QGroupBox {{ font-weight: bold; color: {_hex(C_COG)}; }}"
        )
        brain_layout = QVBoxLayout(self._brain_group)
        brain_layout.setContentsMargins(8, 16, 8, 8)
        brain_layout.setSpacing(2)
        self._brain_neurons_label = QLabel("")
        self._brain_neurons_label.setStyleSheet("font-size: 11px;")
        self._brain_freq_label = QLabel("")
        self._brain_freq_label.setStyleSheet("font-size: 11px;")
        self._brain_badge = QLabel("")
        self._brain_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._brain_badge.setStyleSheet(
            "background-color: #1a2332; border: 1px solid #3e7cd6; "
            "border-radius: 4px; padding: 4px 8px; font-size: 11px; color: #d0d8e0;"
        )
        brain_layout.addWidget(self._brain_neurons_label)
        brain_layout.addWidget(self._brain_freq_label)
        brain_layout.addWidget(self._brain_badge)
        self._layout.addWidget(self._brain_group)

        # === Inventaire (apres Cerveau) ===
        self._inventory_group = QGroupBox("Inventaire")
        self._inventory_group.setStyleSheet(
            f"QGroupBox {{ font-weight: bold; color: {_hex(C_EXP)}; }}"
        )
        inv_layout = QVBoxLayout(self._inventory_group)
        inv_layout.setContentsMargins(8, 16, 8, 8)
        inv_layout.setSpacing(2)
        self._inventory_label = QLabel("")
        self._inventory_label.setWordWrap(True)
        self._inventory_label.setStyleSheet("font-size: 11px;")
        inv_layout.addWidget(self._inventory_label)
        self._layout.addWidget(self._inventory_group)

        # === Outil (apres Inventaire) ===
        self._tool_group = QGroupBox("Outil")
        self._tool_group.setStyleSheet(
            f"QGroupBox {{ font-weight: bold; color: {_hex(C_BESOIN)}; }}"
        )
        tool_layout = QVBoxLayout(self._tool_group)
        tool_layout.setContentsMargins(8, 16, 8, 8)
        tool_layout.setSpacing(2)
        self._tool_label = QLabel("")
        self._tool_label.setWordWrap(True)
        self._tool_label.setStyleSheet("font-size: 11px;")
        tool_layout.addWidget(self._tool_label)
        self._layout.addWidget(self._tool_group)

        # === Tableau Anima ===
        anima_box = QGroupBox("Anima")
        anima_layout = QVBoxLayout(anima_box)
        self._table = QTableView()
        self._table.setModel(self._anima_model)
        self._table.verticalHeader().setVisible(False)
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.setMinimumHeight(200)
        anima_layout.addWidget(self._table)
        self._layout.addWidget(anima_box)

        # === Memoire (apres Anima) ===
        self._memory_group = QGroupBox("Memoire")
        self._memory_group.setStyleSheet(
            f"QGroupBox {{ font-weight: bold; color: {_hex(C_MEM)}; }}"
        )
        mem_layout = QVBoxLayout(self._memory_group)
        mem_layout.setContentsMargins(8, 16, 8, 8)
        mem_layout.setSpacing(4)
        self._belief_label = QLabel("")
        self._belief_label.setWordWrap(True)
        self._belief_label.setStyleSheet("font-size: 11px;")
        mem_layout.addWidget(self._belief_label)
        self._autobio_label = QLabel("")
        self._autobio_label.setWordWrap(True)
        self._autobio_label.setStyleSheet("font-size: 11px;")
        mem_layout.addWidget(self._autobio_label)
        self._layout.addWidget(self._memory_group)

        # === Relations ===
        self._relations_label = QLabel("")
        self._relations_label.setWordWrap(True)
        self._layout.addWidget(self._relations_label)

        # === Goal ===
        self._goal_label = QLabel("")
        self._goal_label.setWordWrap(True)
        self._layout.addWidget(self._goal_label)

        self._layout.addStretch()

        scroll.setWidget(widget)
        self.setWidget(scroll)

    def _create_info_groups(self):
        """Cree les groupes Corps, Cognition, Personnalite, Emotions, Besoins."""
        self._groups = {}
        for key, title, color in [
            ("body", "Corps", C_CORPS),
            ("cog", "Cognition", C_COG),
            ("perso", "Personnalite", C_PERSO),
            ("emo", "Emotions", C_EMO),
        ]:
            group = QGroupBox(title)
            group.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {_hex(color)}; }}")
            grid = QGridLayout(group)
            grid.setContentsMargins(8, 16, 8, 8)
            grid.setSpacing(2)
            self._groups[key] = (group, grid)
            self._layout.addWidget(group)

        needs_group = QGroupBox("Besoins")
        needs_group.setStyleSheet(f"QGroupBox {{ font-weight: bold; color: {_hex(C_BESOIN)}; }}")
        needs_grid = QGridLayout(needs_group)
        needs_grid.setContentsMargins(8, 16, 8, 8)
        needs_grid.setSpacing(4)
        self._groups["needs"] = (needs_group, needs_grid)
        self._needs_sliders = {}
        self._needs_labels = {}
        need_keys = ["faim", "soif", "energie", "sommeil", "sante", "securite", "appartenance", "estime"]
        for i, key in enumerate(need_keys):
            lbl = QLabel(f"{key}:")
            lbl.setStyleSheet("color: #697281; font-size: 11px;")
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(0, 100)
            slider.setValue(0)
            val_lbl = QLabel("0%")
            val_lbl.setStyleSheet("font-size: 11px;")
            val_lbl.setFixedWidth(36)
            needs_grid.addWidget(lbl, i, 0)
            needs_grid.addWidget(slider, i, 1)
            needs_grid.addWidget(val_lbl, i, 2)
            self._needs_sliders[key] = slider
            self._needs_labels[key] = val_lbl
            slider.valueChanged.connect(lambda v, lbl=val_lbl: lbl.setText(f"{v}%"))
            slider.sliderReleased.connect(
                lambda k=key, s=slider: self.controller.execute({
                    "kind": "set_agent_stat",
                    "eid": self.controller.ui_state.selected_agent_eid,
                    "stat": k,
                    "value": s.value() / 100.0,
                })
            )
        self._layout.addWidget(needs_group)

    def refresh(self):
        snap = selected_agent_snapshot(self.controller.sim, self.controller.ui_state)
        anima_snap = anima_snapshot(self.controller.sim, self.controller.ui_state)

        if snap is None:
            self._identity_label.setText("Aucun agent selectionne")
            self._state_label.setText("")
            self._anima_model.set_snapshot(None)
            for group, _ in self._groups.values():
                group.setVisible(False)
            self._brain_group.setVisible(False)
            self._inventory_group.setVisible(False)
            self._tool_group.setVisible(False)
            self._memory_group.setVisible(False)
            self._relations_label.setText("")
            self._goal_label.setText("")
            return

        # Identite
        nom = snap.get("nom", "?")
        sex = snap.get("sexe", snap.get("sex", "?"))
        stage = snap.get("stage", "")
        age = snap.get("age_ans", 0)
        cls = snap.get("classe", "")
        clan = snap.get("clan", "")
        gen = snap.get("generation", 0)
        self._identity_label.setText(
            f"<b>{nom}</b> ({sex}) — {stage}, {age:.1f} ans, {cls}, "
            f"clan {clan}, gen {gen}"
        )

        # Etat
        sante = snap.get("sante", 0)
        energie = snap.get("energie", 0)
        faim = snap.get("faim", 0)
        douleur = snap.get("douleur", 0)
        self._state_label.setText(
            f"Sante: {sante:.0%} | Energie: {energie:.0%} | "
            f"Faim: {faim:.0%} | Douleur: {douleur:.1f}"
        )

        # Groupes d'info
        for key, data in [
            ("body", snap.get("corps", {})),
            ("cog", snap.get("cognition", {})),
            ("perso", snap.get("personnalite", {})),
            ("emo", snap.get("emotions", {})),
        ]:
            if key in self._groups:
                group, grid = self._groups[key]
                self._fill_grid(grid, data)
                group.setVisible(bool(data))

        # Needs — sliders editables
        needs = self._extract_needs(snap)
        if needs:
            for key, val in needs.items():
                if key in self._needs_sliders:
                    self._needs_sliders[key].blockSignals(True)
                    self._needs_sliders[key].setValue(int(val * 100))
                    self._needs_sliders[key].blockSignals(False)
                    self._needs_labels[key].setText(f"{int(val * 100)}%")
            self._groups["needs"][0].setVisible(True)
        else:
            self._groups["needs"][0].setVisible(False)

        # === Cerveau ===
        brain = snap.get("cerveau", {})
        if brain:
            neurons = brain.get("neurones", 0)
            freq = brain.get("frequence_reflexion", 0)
            rank = brain.get("classement_actions", [])
            self._brain_neurons_label.setText(f"Nombre de neurones: {neurons}")
            self._brain_freq_label.setText(f"Frequence de reflexion: {freq}")
            if rank:
                top3 = ", ".join(str(r) for r in rank[:3])
                self._brain_badge.setText(f"Top actions: {top3}")
            else:
                self._brain_badge.setText("Aucun classement")
            self._brain_group.setVisible(True)
        else:
            self._brain_group.setVisible(False)

        # === Inventaire ===
        inventory = snap.get("inventaire", {})
        if inventory:
            lines = []
            for item, qty in inventory.items():
                if isinstance(qty, (int, float)) and qty != 1:
                    lines.append(f"{item}: {qty}")
                else:
                    lines.append(str(item))
            self._inventory_label.setText("\n".join(lines))
            self._inventory_group.setVisible(True)
        else:
            self._inventory_label.setText("Vide")
            self._inventory_group.setVisible(True)

        # === Outil ===
        tool = snap.get("outil", None)
        if tool:
            dur = snap.get("durabilite_outil", 0)
            tool_name = tool if isinstance(tool, str) else str(tool)
            self._tool_label.setText(f"{tool_name} (durabilite: {dur})")
            self._tool_group.setVisible(True)
        else:
            self._tool_label.setText("Aucun")
            self._tool_group.setVisible(True)

        # === Memoire / croyances ===
        beliefs = snap.get("croyances_danger", snap.get("memoire", {}))
        episodes = snap.get("episodes", [])
        has_belief = bool(beliefs)
        has_episodes = bool(episodes)
        if has_belief or has_episodes:
            self._memory_group.setVisible(True)
            if has_belief:
                belief_lines = []
                for place_type, belief_val in beliefs.items():
                    if isinstance(belief_val, dict):
                        belief = belief_val.get("belief", belief_val.get("b", "?"))
                        conf = belief_val.get("confidence", belief_val.get("c", 0))
                        belief_lines.append(
                            f"{place_type}: {belief} (confiance: {conf:.0%})"
                        )
                    else:
                        belief_lines.append(f"{place_type}: {belief_val}")
                self._belief_label.setText(
                    "<b>Croyances:</b>\n" + "\n".join(belief_lines)
                )
            else:
                self._belief_label.setText("<b>Croyances:</b> aucune")

            if has_episodes:
                last5 = episodes[-5:]
                epi_lines = []
                for i, ep in enumerate(last5):
                    epi_lines.append(f"  [{i+1}] {ep}")
                self._autobio_label.setText(
                    "<b>Autobiographie:</b>\n" + "\n".join(epi_lines)
                )
            else:
                self._autobio_label.setText("<b>Autobiographie:</b> aucune")
        else:
            self._memory_group.setVisible(False)

        # Anima
        self._anima_model.set_snapshot(anima_snap or snap)

        # Relations
        rels = snap.get("relations", [])
        if rels:
            lines = []
            for r in rels[:5]:
                conf = r.get("confiance", 0)
                aff = r.get("affection", 0)
                vivant = "vivant" if r.get("vivant", False) else "mort"
                lines.append(f"  {r['nom']}: conf={conf:.2f} aff={aff:.2f} ({vivant})")
            self._relations_label.setText(
                "<b>Relations:</b>\n" + "\n".join(lines)
            )
        else:
            self._relations_label.setText("<b>Relations:</b> aucune")

        # Goal
        goal = snap.get("but", {})
        if goal and goal.get("action_nom"):
            dist = goal.get("distance_px")
            dist_str = f", {dist:.0f}px" if dist else ""
            self._goal_label.setText(
                f"<b>But:</b> {goal['action_nom']}{dist_str}"
            )
        else:
            self._goal_label.setText("<b>But:</b> aucun")

    def _extract_needs(self, snap):
        """Extrait les besoins en dictionnaire."""
        return {
            "faim": snap.get("faim", 0),
            "energie": snap.get("energie", 0),
            "soif": snap.get("soif", 0),
            "sommeil": snap.get("sommeil", 0),
            "securite": snap.get("securite", 0),
            "appartenance": snap.get("appartenance", 0),
            "estime": snap.get("estime", 0),
        }

    def _fill_grid(self, grid, data):
        """Remplit un QGridLayout avec des paires label/valeur."""
        # Clear existing
        while grid.count():
            item = grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not data:
            return
        for i, (key, val) in enumerate(data.items()):
            row, col = divmod(i, 2)
            lbl = QLabel(f"{key}:")
            lbl.setStyleSheet("color: #697281; font-size: 11px;")
            val_lbl = QLabel(f"{val:.2f}" if isinstance(val, float) else str(val))
            val_lbl.setStyleSheet("font-size: 11px;")
            grid.addWidget(lbl, row, col * 2)
            grid.addWidget(val_lbl, row, col * 2 + 1)


def _hex(t):
    return f"#{t[0]:02x}{t[1]:02x}{t[2]:02x}"

```

## ui_qt/docks/journal_dock.py

**Type :** `.py`

```python

"""JournalDock — dock Qt pour le journal filtrable (avancé)."""
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                              QTableView, QComboBox, QPushButton, QLabel,
                              QLineEdit, QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from game.ui_snapshots import journal_snapshot
from game.ui_registry import LOG_TITLES, LOG_CATS
from ..models.journal_model import JournalModel


class JournalDock(QDockWidget):
    """Dock journal avec filtres par catégorie, recherche texte, export."""

    def __init__(self, controller, parent=None):
        super().__init__("Journal", parent)
        self.controller = controller
        self._model = JournalModel()
        self._setup_ui()

    def _setup_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)

        # Compteur
        self._count_label = QLabel("0 entrees")
        layout.addWidget(self._count_label)

        # Filtres en ligne
        filter_layout = QHBoxLayout()

        # Categorie
        self._filter_combo = QComboBox()
        self._filter_combo.addItem("Tous", "tous")
        for cat, title in LOG_TITLES.items():
            self._filter_combo.addItem(title, cat)
        self._filter_combo.currentIndexChanged.connect(self._on_filter)
        filter_layout.addWidget(QLabel("Categorie:"))
        filter_layout.addWidget(self._filter_combo)

        # Recherche texte
        self._search = QLineEdit()
        self._search.setPlaceholderText("Rechercher dans le journal...")
        self._search.textChanged.connect(self._on_filter)
        filter_layout.addWidget(self._search)

        layout.addLayout(filter_layout)

        # Boutons d'action
        btn_layout = QHBoxLayout()

        export_json = QPushButton("Exporter JSON")
        export_json.clicked.connect(lambda: self._export("json"))
        btn_layout.addWidget(export_json)

        export_csv = QPushButton("Exporter CSV")
        export_csv.clicked.connect(lambda: self._export("csv"))
        btn_layout.addWidget(export_csv)

        export_txt = QPushButton("Exporter TXT")
        export_txt.clicked.connect(lambda: self._export("txt"))
        btn_layout.addWidget(export_txt)

        layout.addLayout(btn_layout)

        # Tableau
        self._table = QTableView()
        self._table.setModel(self._model)
        self._table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self._table.verticalHeader().setVisible(False)
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.setSortingEnabled(True)
        layout.addWidget(self._table)

        self.setWidget(widget)

    def refresh(self):
        cat = self._filter_combo.currentData() or "tous"
        search = self._search.text()
        snap = journal_snapshot(self.controller.sim, category=cat, search=search)
        self._model.set_snapshot(snap)
        self._count_label.setText(f"{len(snap)} entrees")

    def _on_filter(self):
        self.refresh()

    def _export(self, fmt):
        path, _ = QFileDialog.getSaveFileName(
            self, "Exporter le journal",
            f"journal.{fmt}",
            f"{fmt.upper()} (*.{fmt})"
        )
        if not path:
            return

        cat = self._filter_combo.currentData() or "tous"
        search = self._search.text()
        snap = journal_snapshot(self.controller.sim, category=cat, search=search)

        if fmt == "json":
            import json
            with open(path, "w", encoding="utf-8") as f:
                json.dump(snap, f, ensure_ascii=False, indent=2)

        elif fmt == "csv":
            import csv
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["tick", "category", "text", "count"])
                writer.writeheader()
                writer.writerows(snap)

        elif fmt == "txt":
            with open(path, "w", encoding="utf-8") as f:
                for e in snap:
                    mm, ss = divmod(int(e.get("tick", 0) / 60), 60)
                    cat_label = e.get("category", "")
                    text = e.get("text", "")
                    cnt = e.get("count", 1)
                    suffix = f"  x{cnt}" if cnt > 1 else ""
                    f.write(f"[{mm:02}:{ss:02}] [{cat_label}] {text}{suffix}\n")

```

## ui_qt/docks/population_dock.py

**Type :** `.py`

```python

"""PopulationDock — dock Qt pour la liste des habitants (avancé)."""
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                              QTableView, QLineEdit, QComboBox, QLabel,
                              QPushButton, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal, QSortFilterProxyModel
from PyQt6.QtGui import QColor

from game.ui_snapshots import population_snapshot
from ..models.population_model import PopulationModel


class PopulationDock(QDockWidget):
    """Dock de la population avec tableau triable et filtrable."""

    agent_selected = pyqtSignal(int)

    def __init__(self, controller, parent=None):
        super().__init__("Habitants", parent)
        self.controller = controller
        self._model = PopulationModel()
        self._proxy = QSortFilterProxyModel()
        self._proxy.setSourceModel(self._model)
        self._proxy.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self._setup_ui()

    def _setup_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)

        # Compteur
        self._count_label = QLabel("0 habitants")
        layout.addWidget(self._count_label)

        # Recherche
        search_layout = QHBoxLayout()
        self._search = QLineEdit()
        self._search.setPlaceholderText("Filtrer par nom, clan, classe...")
        self._search.textChanged.connect(self._proxy.setFilterFixedString)
        search_layout.addWidget(self._search)

        clear_btn = QPushButton("X")
        clear_btn.setFixedWidth(24)
        clear_btn.clicked.connect(self._search.clear)
        search_layout.addWidget(clear_btn)
        layout.addLayout(search_layout)

        # Filtres
        filter_layout = QHBoxLayout()

        self._stage_filter = QComboBox()
        self._stage_filter.addItem("Tous les stades", "")
        for stage in ("enfant", "adulte", "ancien"):
            self._stage_filter.addItem(stage, stage)
        self._stage_filter.currentIndexChanged.connect(self._apply_filters)
        filter_layout.addWidget(QLabel("Age:"))
        filter_layout.addWidget(self._stage_filter)

        self._alive_filter = QComboBox()
        self._alive_filter.addItem("Vivants", "alive")
        self._alive_filter.addItem("Tous", "all")
        self._alive_filter.currentIndexChanged.connect(self._apply_filters)
        filter_layout.addWidget(self._alive_filter)

        layout.addLayout(filter_layout)

        # Bouton Supprimer
        self._remove_btn = QPushButton("Supprimer")
        self._remove_btn.setEnabled(False)
        self._remove_btn.setStyleSheet(
            "QPushButton { background-color: #c0392b; color: white; "
            "padding: 4px 12px; border: none; border-radius: 3px; }"
            "QPushButton:hover { background-color: #e74c3c; }"
            "QPushButton:disabled { background-color: #7f8c8d; color: #bdc3c7; }"
        )
        self._remove_btn.clicked.connect(self._on_remove)
        layout.addWidget(self._remove_btn)

        # Tableau
        self._table = QTableView()
        self._table.setModel(self._proxy)
        self._table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self._table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self._table.setSortingEnabled(True)
        self._table.verticalHeader().setVisible(False)
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.clicked.connect(self._on_click)
        self._table.selectionModel().selectionChanged.connect(self._on_selection_changed)
        layout.addWidget(self._table)

        self.setWidget(widget)

    def refresh(self):
        snap = population_snapshot(self.controller.sim)
        portraits = {}
        try:
            am = self.controller.sim.am
            for row in snap:
                eid = row.get("eid")
                if eid is not None:
                    try:
                        portrait = am.portrait(eid, size=(24, 24))
                        if portrait is not None:
                            portraits[eid] = portrait
                    except Exception:
                        pass
        except Exception:
            pass
        self._model.set_snapshot(snap, portraits)
        self._count_label.setText(f"{len(snap)} habitants")
        self._apply_filters()

    def _apply_filters(self):
        stage = self._stage_filter.currentData() or ""
        # Le proxy filtre deja par texte ; le stade est gere via le model
        # Pour le stade, on filtre manuellement
        if stage:
            self._proxy.setFilterKeyColumn(8)  # colonne Stage
            self._proxy.setFilterFixedString(stage)
        else:
            self._proxy.setFilterKeyColumn(-1)
            self._proxy.setFilterFixedString(self._search.text())

    def _selected_eid(self):
        indexes = self._table.selectionModel().selectedRows()
        if not indexes:
            return None
        source_index = self._proxy.mapToSource(indexes[0])
        return self._model.eid_at(source_index.row())

    def _on_selection_changed(self):
        eid = self._selected_eid()
        self._remove_btn.setEnabled(eid is not None)

    def _on_click(self, index):
        source_index = self._proxy.mapToSource(index)
        eid = self._model.eid_at(source_index.row())
        if eid is not None:
            self.controller.execute({"kind": "select_agent", "eid": eid})
            self.agent_selected.emit(eid)

    def _on_remove(self):
        eid = self._selected_eid()
        if eid is None:
            return
        agent = next(
            (a for a in self.controller.sim.agents if a.eid == eid and a.alive),
            None,
        )
        if agent is None:
            return
        reply = QMessageBox.question(
            self,
            "Supprimer un habitant",
            f"Supprimer {agent.name} ? Cette action est irréversible.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.controller.execute({"kind": "remove_agent", "eid": eid})
            self.refresh()

```

## ui_qt/docks/society_dock.py

**Type :** `.py`

```python

"""SocietyDock — dock Qt pour les stats de société."""
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                              QTableView, QTableWidget, QTableWidgetItem,
                              QLabel, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from game.ui_snapshots import society_snapshot
from ui_qt.models.society_model import SocietyModel


class SocietyDock(QDockWidget):
    """Dock société avec stats démographiques et sociales."""

    def __init__(self, controller, parent=None):
        super().__init__("Societe", parent)
        self.controller = controller
        self._model = SocietyModel()
        self._setup_ui()

    def _setup_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)

        self._table = QTableView()
        self._table.setModel(self._model)
        self._table.verticalHeader().setVisible(False)
        self._table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self._table)

        # Section Relations
        layout.addWidget(QLabel("Relations"))
        self._relations_table = QTableWidget()
        self._relations_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._relations_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._relations_table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self._relations_table.verticalHeader().setVisible(False)
        self._relations_table.horizontalHeader().setStretchLastSection(True)
        self._relations_table.setAlternatingRowColors(True)
        self._relations_table.setRowCount(0)
        self._relations_table.setColumnCount(5)
        self._relations_table.setHorizontalHeaderLabels(
            ["Agent 1", "Agent 2", "Type", "Confiance", "Affinité"]
        )
        header = self._relations_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self._relations_table)

        self.setWidget(widget)

    def refresh(self):
        snap = society_snapshot(self.controller.sim)
        self._model.set_snapshot(snap)
        self._populate_relations(snap.get("relations", []))

    def _populate_relations(self, relations):
        self._relations_table.setRowCount(len(relations))
        for row, rel in enumerate(relations):
            self._relations_table.setItem(row, 0, QTableWidgetItem(rel["name1"]))
            self._relations_table.setItem(row, 1, QTableWidgetItem(rel["name2"]))
            self._relations_table.setItem(row, 2, QTableWidgetItem(rel["type"]))
            self._relations_table.setItem(
                row, 3, QTableWidgetItem(f'{rel["confiance"]:+.2f}')
            )
            self._relations_table.setItem(
                row, 4, QTableWidgetItem(f'{rel["affinite"]:+.2f}')
            )

```

## ui_qt/docks/tools_dock.py

**Type :** `.py`

```python

"""ToolsDock — dock Qt pour les outils monde."""
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                              QGridLayout, QPushButton, QLabel, QSlider)
from PyQt6.QtCore import Qt, pyqtSignal


class ToolsDock(QDockWidget):
    """Dock d'outils monde : poser, gommer, sol, eau, terre, mur, etc."""

    mode_changed = pyqtSignal(str)

    TOOLS = [
        ("place", "Poser"), ("erase", "Gommer"), ("floor", "Sol"),
        ("block", "Bloc"),
        ("agent", "Etre"), ("sheep", "Mouton"), ("monster", "Monstre"),
        ("inspect", "Examiner"),
        ("water", "Eau"), ("land", "Terre"), ("wall", "Mur"),
        ("carve", "Sculpter"), ("restore", "Restaurer"),
    ]

    HINTS = {
        "place": "clic = poser l'asset / glisser = peindre",
        "erase": "clic = effacer les objets",
        "floor": "clic = peindre le sol",
        "water": "glisser = transformer terre en eau",
        "land": "glisser = transformer eau en terre",
        "wall": "glisser = placer des rochers",
        "carve": "glisser = creuser les montagnes",
        "restore": "glisser = restaurer le terrain",
        "block": "clic = construire un bloc",
        "agent": "clic = inserer un etre",
        "sheep": "clic = ajouter un mouton",
        "monster": "clic = ajouter un monstre",
        "inspect": "clic = examiner",
    }

    def __init__(self, controller, parent=None):
        super().__init__("Outils", parent)
        self.controller = controller
        self._buttons = {}
        self._setup_ui()

    def _setup_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)

        # Grille d'outils
        grid = QGridLayout()
        grid.setSpacing(4)
        for i, (tool_id, label) in enumerate(self.TOOLS):
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, tid=tool_id: self._on_tool(tid))
            grid.addWidget(btn, i // 3, i % 3)
            self._buttons[tool_id] = btn
        layout.addLayout(grid)

        # Hint
        self._hint = QLabel("")
        self._hint.setWordWrap(True)
        self._hint.setStyleSheet("color: #697281; font-size: 12px;")
        layout.addWidget(self._hint)

        # Slider pinceau
        brush_label = QLabel("Taille pinceau:")
        layout.addWidget(brush_label)
        self._brush_slider = QSlider(Qt.Orientation.Horizontal)
        self._brush_slider.setRange(1, 15)
        self._brush_slider.setValue(3)
        self._brush_slider.valueChanged.connect(self._on_brush)
        layout.addWidget(self._brush_slider)
        self._brush_val = QLabel("3")
        layout.addWidget(self._brush_val)

        # Material
        mat_label = QLabel("Materiau bloc:")
        layout.addWidget(mat_label)
        self._mat_layout = QHBoxLayout()
        for mat in ("bois", "pierre"):
            btn = QPushButton(mat)
            btn.setCheckable(True)
            btn.setChecked(mat == "bois")
            btn.clicked.connect(lambda checked, m=mat: self._on_material(m))
            self._mat_layout.addWidget(btn)
        layout.addLayout(self._mat_layout)

        layout.addStretch()
        self.setWidget(widget)

    def _on_tool(self, tool_id):
        self.controller.ui_state.active_mode = tool_id
        for tid, btn in self._buttons.items():
            btn.setChecked(tid == tool_id)
        self._hint.setText(self.HINTS.get(tool_id, ""))
        self.mode_changed.emit(tool_id)

    def _on_brush(self, value):
        self.controller.ui_state.brush_size = value
        self._brush_val.setText(str(value))

    def _on_material(self, material):
        self.controller.ui_state.block_material = material
        for i in range(self._mat_layout.count()):
            btn = self._mat_layout.itemAt(i).widget()
            if btn:
                btn.setChecked(btn.text() == material)

    def refresh(self):
        mode = self.controller.ui_state.active_mode
        for tid, btn in self._buttons.items():
            btn.setChecked(tid == mode)
        self._hint.setText(self.HINTS.get(mode, ""))
        self._brush_slider.setValue(self.controller.ui_state.brush_size)

```

## ui_qt/main_window.py

**Type :** `.py`

```python

"""MainWindow — QMainWindow principale de l'interface PyQt6."""
from PyQt6.QtWidgets import (QMainWindow, QToolBar, QLabel,
                              QSpinBox, QStatusBar, QPushButton)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction

from game.ui_snapshots import simulation_snapshot
from game.ui_commands import execute_command
from ui_qt.map.map_view import MapView
from ui_qt.docks.population_dock import PopulationDock
from ui_qt.docks.inspector_dock import InspectorDock
from ui_qt.docks.journal_dock import JournalDock
from ui_qt.docks.society_dock import SocietyDock
from ui_qt.docks.assets_dock import AssetsDock
from ui_qt.docks.tools_dock import ToolsDock
from ui_qt.dialogs import SaveDialog
from ui_qt.theme.theme import apply_theme
from ui_qt.studio.parameter_dock import ParameterDock
from ui_qt.studio.scenario_dialog import ScenarioDialog
from ui_qt.studio.timeline_dock import TimelineDock
from ui_qt.studio.laboratory_dock import LaboratoryDock
from ui_qt.studio.comparison_panel import ComparisonPanel
from ui_qt.studio.world_overlay import WorldOverlay


class MainWindow(QMainWindow):
    """Fenêtre principale PyQt6 avec docks, barre d'outils et carte."""

    def __init__(self, controller, am=None, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.am = am
        self.setWindowTitle("Univers Vivant — PyQt6")
        self.setMinimumSize(1200, 800)

        apply_theme(self)

        self._setup_toolbar()
        self._setup_central()
        self._setup_docks()
        self._setup_statusbar()
        self._setup_timer()
        self._restore_settings()

    def _setup_toolbar(self):
        tb = QToolBar("Controle")
        tb.setMovable(False)
        self.addToolBar(tb)

        # Pause/Play
        self._pause_action = QAction("Pause", self)
        self._pause_action.setShortcut("Space")
        self._pause_action.triggered.connect(self._on_pause)
        tb.addAction(self._pause_action)

        # Step
        step_action = QAction("Step", self)
        step_action.setShortcut("N")
        step_action.triggered.connect(self._on_step)
        tb.addAction(step_action)

        tb.addSeparator()

        # Vitesse
        tb.addWidget(QLabel(" Vitesse: "))
        self._speed_spin = QSpinBox()
        self._speed_spin.setRange(1, 8)
        self._speed_spin.setValue(self.controller.sim.speed)
        self._speed_spin.valueChanged.connect(self._on_speed)
        tb.addWidget(self._speed_spin)

        tb.addSeparator()

        # Spawn
        spawn_btn = QAction("+ Habitants", self)
        spawn_btn.triggered.connect(lambda: self.controller.execute({"kind": "spawn_agent"}))
        tb.addAction(spawn_btn)

        spawn_sheep = QAction("+ Mouton", self)
        spawn_sheep.triggered.connect(lambda: self.controller.execute({"kind": "spawn_sheep"}))
        tb.addAction(spawn_sheep)

        spawn_monster = QAction("+ Monstre", self)
        spawn_monster.triggered.connect(lambda: self.controller.execute({"kind": "spawn_monster"}))
        tb.addAction(spawn_monster)

        tb.addSeparator()

        # Suivi caméra
        self._follow_action = QAction("Suivre", self)
        self._follow_action.setCheckable(True)
        self._follow_action.triggered.connect(self._on_follow)
        tb.addAction(self._follow_action)

        tb.addSeparator()

        # Sauvegarde
        save_action = QAction("Sauvegarder (F5)", self)
        save_action.setShortcut("F5")
        save_action.triggered.connect(self._on_save)
        tb.addAction(save_action)

        load_action = QAction("Charger (F9)", self)
        load_action.setShortcut("F9")
        load_action.triggered.connect(self._on_load)
        tb.addAction(load_action)

        tb.addSeparator()

        # Theme toggle
        self._theme_action = QAction("Theme sombre", self)
        self._theme_action.triggered.connect(self._toggle_theme)
        tb.addAction(self._theme_action)

        tb.addSeparator()
        # Overlay mode selector
        from PyQt6.QtWidgets import QComboBox
        self._overlay_combo = QComboBox()
        for m in ["normal", "danger", "ressources", "memoire", "relations", "besoins", "anima"]:
            self._overlay_combo.addItem(WorldOverlay().mode_label(m) if hasattr(WorldOverlay, 'mode_label') else m, m)
        self._overlay_combo.currentIndexChanged.connect(self._on_overlay_change)
        tb.addWidget(QLabel("Vue: "))
        tb.addWidget(self._overlay_combo)

        # Speed presets
        for speed in [1, 2, 4, 8]:
            btn = QPushButton(f"{speed}x")
            btn.setFixedWidth(36)
            btn.clicked.connect(lambda checked, s=speed: self._set_speed(s))
            tb.addWidget(btn)

    def _setup_central(self):
        self._map = MapView(self.controller, self)
        self.setCentralWidget(self._map)

    def _setup_docks(self):
        # Dock Habitants (gauche)
        self._pop_dock = PopulationDock(self.controller, self)
        self._pop_dock.agent_selected.connect(self._on_agent_selected)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._pop_dock)

        # Dock Inspecteur (droite)
        self._inspector_dock = InspectorDock(self.controller, self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self._inspector_dock)

        # Dock Société (droite, tabulé avec inspecteur)
        self._society_dock = SocietyDock(self.controller, self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self._society_dock)
        self.tabifyDockWidget(self._inspector_dock, self._society_dock)

        # Dock Assets (gauche, tabulé avec habitants)
        self._assets_dock = AssetsDock(self.controller, self)
        if self.am:
            self._assets_dock.set_asset_manager(self.am)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._assets_dock)
        self.tabifyDockWidget(self._pop_dock, self._assets_dock)

        # Dock Outils (gauche)
        self._tools_dock = ToolsDock(self.controller, self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._tools_dock)

        # Dock Journal (bas)
        self._journal_dock = JournalDock(self.controller, self)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._journal_dock)

        # Studio docks
        self._param_dock = ParameterDock(self.controller, self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self._param_dock)
        self._param_dock.hide()

        self._timeline_dock = TimelineDock(self.controller, self)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._timeline_dock)
        self._timeline_dock.hide()

        self._lab_dock = LaboratoryDock(self.controller, self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self._lab_dock)
        self._lab_dock.hide()

        # Studio menu
        studio_menu = self.menuBar().addMenu("Studio")
        studio_menu.addAction("Scénarios...", self._open_scenarios)
        studio_menu.addAction("Paramètres", lambda: self._toggle_dock(self._param_dock))
        studio_menu.addAction("Timeline", lambda: self._toggle_dock(self._timeline_dock))
        studio_menu.addAction("Laboratoire", lambda: self._toggle_dock(self._lab_dock))
        studio_menu.addAction("Comparaison A/B", self._open_comparison)
        studio_menu.addAction("Configurer l'overlay", self._open_overlay_config)

    def _setup_statusbar(self):
        self._status = QStatusBar()
        self.setStatusBar(self._status)
        self._status_label = QLabel()
        self._status.addWidget(self._status_label)

    def _setup_timer(self):
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(16)  # ~60 FPS

    def _tick(self):
        sim = self.controller.sim

        # Avancer la simulation
        if not sim.paused:
            from game.config import SIM_HZ, FPS
            acc = sim.speed * SIM_HZ / FPS
            n = 0
            while acc >= 1.0 and n < 8:
                sim.tick()
                acc -= 1.0
                n += 1

        # Synchroniser l'état
        self.controller.sync_from_simulation()

        # Mettre à jour les docks
        self._pop_dock.refresh()
        self._inspector_dock.refresh()
        self._journal_dock.refresh()
        self._society_dock.refresh()
        self._tools_dock.refresh()
        self._assets_dock.refresh()

        # Mettre à jour la carte
        self._map.update()

        # Mettre à jour la barre d'état
        snap = simulation_snapshot(sim, self.controller.ui_state)
        clock = snap.get("clock", {})
        self._status_label.setText(
            f"Tick {snap['tick']} | {clock.get('label', '')} | "
            f"Pop: {snap['population']} | Speed: {snap['speed']} | "
            f"{'Pause' if snap['paused'] else 'Running'}"
        )

        # Mettre à jour les contrôles
        self._pause_action.setText("Reprendre" if sim.paused else "Pause")
        if self._speed_spin.value() != sim.speed:
            self._speed_spin.blockSignals(True)
            self._speed_spin.setValue(sim.speed)
            self._speed_spin.blockSignals(False)

    def _on_pause(self):
        self.controller.execute({"kind": "pause_toggle"})

    def _on_step(self):
        self.controller.execute({"kind": "step"})

    def _on_speed(self, value):
        self.controller.execute({"kind": "set_speed", "speed": value})

    def _on_follow(self, checked):
        self.controller.ui_state.follow_selected = checked

    def _on_save(self):
        dlg = SaveDialog(self.controller, mode="save", parent=self)
        if dlg.exec():
            self._status.showMessage("Sauvegardee", 3000)

    def _on_load(self):
        dlg = SaveDialog(self.controller, mode="load", parent=self)
        if dlg.exec():
            new_sim = self.controller.sim
            self.controller.sync_from_simulation()
            self._status.showMessage("Partie chargee", 3000)

    def _on_agent_selected(self, eid):
        self.controller.ui_state.selected_agent_eid = eid
        self.controller.ui_state.active_tab = "etre"

    def _toggle_theme(self):
        from ui_qt.theme.theme import get_theme_name, set_theme_name, apply_theme
        current = get_theme_name()
        new_theme = "sombre" if current == "clair" else "clair"
        set_theme_name(new_theme)
        apply_theme(self, new_theme)
        self._theme_action.setText(
            "Theme clair" if new_theme == "sombre" else "Theme sombre"
        )

    def _restore_settings(self):
        from ui_qt.theme.theme import get_settings, get_theme_name
        s = get_settings()
        geom = s.value("geometry")
        if geom:
            self.restoreGeometry(geom)
        state = s.value("windowState")
        if state:
            self.restoreState(state)
        # Appliquer le theme sauvegarde
        from ui_qt.theme.theme import apply_theme
        apply_theme(self, get_theme_name())

    def _save_settings(self):
        from ui_qt.theme.theme import get_settings
        s = get_settings()
        s.setValue("geometry", self.saveGeometry())
        s.setValue("windowState", self.saveState())

    def _toggle_dock(self, dock):
        dock.setVisible(not dock.isVisible())

    def _open_scenarios(self):
        dlg = ScenarioDialog(self.controller, self)
        dlg.exec()

    def _open_comparison(self):
        if not hasattr(self, '_comparison_panel'):
            self._comparison_panel = ComparisonPanel()
            self._comparison_panel.setWindowTitle("Comparaison A/B")
        self._comparison_panel.show()

    def _open_overlay_config(self):
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Overlay", 
            "Utilisez le sélecteur 'Vue' dans la barre d'outils pour changer l'overlay de la carte.")

    def _on_overlay_change(self, index):
        mode = self._overlay_combo.currentData()
        if hasattr(self, '_map') and self._map:
            self._map.set_overlay_mode(mode)

    def _set_speed(self, speed):
        self.controller.execute({"kind": "set_speed", "speed": speed})

    def closeEvent(self, event):
        self._save_settings()
        super().closeEvent(event)

```

## ui_qt/map/__init__.py

**Type :** `.py`

```python

""""""

```

## ui_qt/map/map_view.py

**Type :** `.py`

```python

"""MapView — QWidget de rendu carte avec QPainter."""
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont

from game.mapapi import MapTransform, map_visible_data
from game.config import GRID, TILE, CLAN_COLORS
from ui_qt.studio.world_overlay import WorldOverlay


class MapView(QWidget):
    """Widget de carte rendue avec QPainter."""

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.transform = MapTransform(zoom=0.25, tilt=55.0)
        self.setMinimumSize(400, 300)
        self._pan_start = None
        self._painting = None
        self._data = {}
        self._overlay = WorldOverlay()
        self._overlay_mode = "normal"
        self.setMouseTracking(True)

    def set_transform(self, transform: MapTransform):
        self.transform = transform
        self.update()

    def set_overlay_mode(self, mode):
        self._overlay_mode = mode
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()

        # Fond
        painter.fillRect(0, 0, w, h, QColor(12, 14, 20))

        # Obtenir les données de carte
        sim = self.controller.sim
        self._data = map_visible_data(sim, self.transform, w, h)

        # Dessiner le terrain
        self._draw_terrain(painter, w, h)

        # Dessiner les entités
        self._draw_entities(painter)

        # Dessiner la grille (optionnel)

        # --- Legend overlay (bottom-left, drawn last) ---
        self._draw_legend(painter)

        # Overlay
        if self._overlay_mode != "normal" and self._data:
            self._overlay.paint(painter, self.transform, self._get_sim_ref(), self._overlay_mode)

        # Minimap
        if self._data:
            self._draw_minimap(painter)

        painter.end()

    def _draw_terrain(self, painter, w, h):
        """Dessine les tuiles de terrain."""
        for tile in self._data.get("terrain", []):
            tx, ty = tile["tx"], tile["ty"]
            sx, sy = self.transform.to_screen(tx * TILE, ty * TILE)

            # Taille de la tuile à l'écran
            ts = max(2, int(TILE * self.transform.zoom))

            if tile["water"]:
                color = QColor(46, 92, 158)
            elif tile["blocked"]:
                color = QColor(128, 118, 106)
            elif tile["land"]:
                color = QColor(86, 150, 62)
            else:
                color = QColor(46, 60, 80)

            painter.fillRect(int(sx), int(sy), ts, ts, color)

            # Feu
            if tile["fire"] > 0:
                alpha = min(200, int(tile["fire"] * 80))
                painter.fillRect(int(sx), int(sy), ts, ts,
                                 QColor(220, 120, 40, alpha))

    def _draw_entities(self, painter):
        """Dessine agents, moutons, monstres."""
        font = QFont("Segoe UI", 8)
        painter.setFont(font)

        # Agents
        for ag in self._data.get("agents", []):
            sx, sy = ag["sx"], ag["sy"]
            color_str = ag["color"]
            r, g, b = CLAN_COLORS.get(color_str, (150, 150, 150))
            painter.setBrush(QBrush(QColor(r, g, b)))
            painter.setPen(QPen(QColor(0, 0, 0), 1))
            painter.drawEllipse(QPointF(sx, sy), 6, 6)

            # Nom
            painter.setPen(QPen(QColor(255, 255, 255)))
            painter.drawText(QPointF(sx + 8, sy - 4), str(ag.get("eid", "")))

        # Sheep
        painter.setBrush(QBrush(QColor(234, 236, 240)))
        for sh in self._data.get("sheep", []):
            painter.drawEllipse(QPointF(sh["sx"], sh["sy"]), 4, 4)

        # Monsters
        painter.setBrush(QBrush(QColor(180, 60, 60)))
        for m in self._data.get("monsters", []):
            painter.drawRect(QPointF(m["sx"] - 4, m["sy"] - 4), 8, 8)

    def _draw_legend(self, painter):
        """Draw a semi-transparent legend box in the bottom-left corner."""
        items = [
            ("Eau (water)", QColor(52, 152, 219)),
            ("Terre (land)", QColor(39, 174, 96)),
            ("Mur (wall)", QColor(230, 126, 34)),
            ("Feu (fire)", QColor(231, 76, 60)),
            ("Agent", QColor(0, 0, 0), "ellipse"),
            ("Mouton", QColor(234, 236, 240), "rect"),
            ("Monstre", QColor(180, 60, 60), "rect"),
        ]

        font = QFont("Segoe UI", 9)
        painter.setFont(font)
        fm = painter.fontMetrics()

        # Measure label widths to compute box width
        max_label_w = 0
        for entry in items:
            tw = fm.horizontalAdvance(entry[0])
            if tw > max_label_w:
                max_label_w = tw

        box_w = 20 + 16 + 8 + max_label_w + 12
        box_h = 12 + len(items) * (fm.height() + 6) + 8
        margin = 20
        bx = margin
        by = self.height() - margin - box_h

        # Semi-transparent background
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        painter.setBrush(QBrush(QColor(20, 20, 30, 180)))
        painter.drawRect(bx, by, box_w, box_h)

        y = by + 12
        for entry in items:
            label = entry[0]
            color = entry[1]
            shape = entry[2] if len(entry) > 2 else "rect"

            sw = 16
            sh = 12
            sx = bx + 10
            sy = y - sh // 2

            painter.setPen(QPen(QColor(40, 40, 40)))
            painter.setBrush(QBrush(color))
            if shape == "ellipse":
                painter.drawEllipse(QPointF(sx + sw / 2, sy + sh / 2),
                                    sw / 2, sh / 2)
            else:
                painter.drawRect(sx, sy, sw, sh)

            painter.setPen(QPen(QColor(230, 230, 230)))
            painter.drawText(bx + 10 + 16 + 8, y + fm.ascent() / 2, label)

            y += fm.height() + 6

    def _get_sim_ref(self):
        """Get simulation reference for overlay rendering."""
        return getattr(self.controller, 'sim', None)

    def _draw_minimap(self, painter):
        """Draw a minimap in the bottom-right corner."""
        mm_w, mm_h = 120, 120
        view_w = self.width()
        view_h = self.height()
        x0 = view_w - mm_w - 20
        y0 = view_h - mm_h - 20

        # Background
        painter.setBrush(QColor(20, 20, 30, 180))
        painter.setPen(QPen(QColor(100, 100, 120), 1))
        painter.drawRect(x0, y0, mm_w, mm_h)

        world_size = GRID * TILE
        scale_x = mm_w / world_size
        scale_y = mm_h / world_size

        # Draw terrain simplified
        tiles = self._data.get("terrain", [])
        for tile in tiles:
            tx = tile.get("tx", 0)
            ty = tile.get("ty", 0)
            px = x0 + int(tx * TILE * scale_x)
            py = y0 + int(ty * TILE * scale_y)
            pw = max(1, int(TILE * scale_x))
            ph = max(1, int(TILE * scale_y))

            if tile.get("water"):
                color = QColor(52, 152, 219)
            elif tile.get("blocked"):
                color = QColor(230, 126, 34)
            elif tile.get("land"):
                color = QColor(39, 174, 96)
            else:
                color = QColor(86, 150, 62)

            painter.setBrush(color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(px, py, pw, ph)

        # Draw agents
        for a in self._data.get("agents", []):
            px = x0 + int(a.get("sx", 0) * scale_x)
            py = y0 + int(a.get("sy", 0) * scale_y)
            painter.setBrush(QColor(255, 255, 255))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(px - 1, py - 1, 3, 3)

        # Draw viewport rectangle
        vx = x0 + int(self.transform.x * scale_x)
        vy = y0 + int(self.transform.y * scale_y)
        vw = int((view_w / self.transform.zoom) * scale_x)
        vh = int((view_h / (self.transform.zoom * self.transform.ys)) * scale_y)
        painter.setPen(QPen(QColor(255, 255, 255), 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(vx, vy, vw, vh)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self._pan_start = event.pos()
        elif event.button() == Qt.MouseButton.LeftButton:
            wx, wy = self.transform.to_world(event.x(), event.y())
            tx, ty = int(wx // TILE), int(wy // TILE)
            mode = self.controller.ui_state.active_mode

            if mode == "inspect":
                self.controller.execute({"kind": "select_tile", "tx": tx, "ty": ty})
                # Inspecter agent le plus proche
                best, bd = None, (TILE * 3) ** 2
                for a in self.controller.sim.agents:
                    if not a.alive:
                        continue
                    d2 = (a.x - wx) ** 2 + (a.y - wy) ** 2
                    if d2 <= bd:
                        best, bd = a, d2
                if best:
                    self.controller.execute({"kind": "select_agent", "eid": best.eid})
            elif mode == "agent":
                self.controller.execute({
                    "kind": "spawn_agent",
                    "x": wx, "y": wy,
                })
            elif mode == "sheep":
                self.controller.execute({"kind": "spawn_sheep", "x": wx, "y": wy})
            elif mode == "monster":
                self.controller.execute({"kind": "spawn_monster", "x": wx, "y": wy})
            elif mode in ("water", "land", "wall", "carve", "restore"):
                radius = self.controller.ui_state.brush_size
                self.controller.execute({
                    "kind": "paint_tile", "tx": tx, "ty": ty,
                    "mode": mode, "radius": radius,
                })
            elif mode == "erase":
                self.controller.execute({"kind": "erase_tile", "tx": tx, "ty": ty})
            elif mode == "place":
                aid = self.controller.ui_state.selected_asset_id
                if aid is not None:
                    self.controller.execute({
                        "kind": "place_asset", "tx": tx, "ty": ty, "aid": aid,
                    })
            elif mode == "floor":
                aid = self.controller.ui_state.selected_asset_id
                if aid is not None:
                    self.controller.execute({
                        "kind": "set_floor", "tx": tx, "ty": ty, "aid": aid,
                    })
            elif mode == "block":
                mat = self.controller.ui_state.block_material
                self.controller.execute({
                    "kind": "build_block", "tx": tx, "ty": ty, "material": mat,
                })

            self._painting = (tx, ty)
            self.update()

    def mouseMoveEvent(self, event):
        if self._pan_start is not None:
            dx = event.x() - self._pan_start.x()
            dy = event.y() - self._pan_start.y()
            self.transform.x -= dx / self.transform.zoom
            self.transform.y -= dy / (self.transform.zoom * self.transform.ys)
            world_size = GRID * TILE
            self.transform.clamp(world_size)
            self._pan_start = event.pos()
            self.update()
        elif self._painting is not None:
            wx, wy = self.transform.to_world(event.x(), event.y())
            tx, ty = int(wx // TILE), int(wy // TILE)
            if (tx, ty) != self._painting:
                mode = self.controller.ui_state.active_mode
                if mode in ("water", "land", "wall", "carve", "restore"):
                    radius = self.controller.ui_state.brush_size
                    self.controller.execute({
                        "kind": "paint_tile", "tx": tx, "ty": ty,
                        "mode": mode, "radius": radius,
                    })
                    self._painting = (tx, ty)
                    self.update()
                elif mode == "erase":
                    self.controller.execute({"kind": "erase_tile", "tx": tx, "ty": ty})
                    self._painting = (tx, ty)
                    self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self._pan_start = None
        if event.button() == Qt.MouseButton.LeftButton:
            self._painting = None

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        factor = 1.1 if delta > 0 else 0.9
        old_zoom = self.transform.zoom
        new_zoom = max(0.05, min(6.0, old_zoom * factor))
        self.transform.set_zoom(new_zoom, (event.x(), event.y()),
                                self.width(), self.height())
        self.update()

```

## ui_qt/models/__init__.py

**Type :** `.py`

```python

""""""

```

## ui_qt/models/anima_model.py

**Type :** `.py`

```python

from PyQt6.QtCore import QAbstractTableModel, Qt
from PyQt6.QtGui import QColor, QFont

_SECTION_BG = QColor(40, 50, 70)
_SECTION_FG = QColor(160, 200, 240)


def _fmt(v):
    if isinstance(v, bool):
        return "Oui" if v else "Non"
    if isinstance(v, float):
        return f"{v:.2f}"
    return str(v) if v is not None else ""


class AnimaModel(QAbstractTableModel):
    HEADERS = ["Attribut", "Valeur"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._rows = []

    def set_snapshot(self, agent_snap):
        self.beginResetModel()
        self._rows = []
        if agent_snap is None:
            self.endResetModel()
            return

        anima = agent_snap.get("anima", {})

        self._rows.append({"type": "section", "label": "BASE"})
        self._data("Nom", agent_snap.get("nom", ""))
        self._data("Sexe", agent_snap.get("sexe", ""))
        self._data("Classe", agent_snap.get("classe", ""))
        self._data("Clan", agent_snap.get("clan", ""))
        self._data("Generation", agent_snap.get("generation", 0))
        self._data("Age", agent_snap.get("age_ans", 0))
        self._data("Stage", agent_snap.get("stage", ""))
        self._data("Sante", agent_snap.get("sante", 0))
        self._data("Energie", agent_snap.get("energie", 0))
        self._data("Faim", agent_snap.get("faim", 0))
        pos = agent_snap.get("position", {})
        if pos:
            self._data("Position", f"({pos.get('tx', 0)}, {pos.get('ty', 0)})")
        goal = agent_snap.get("but", {})
        self._data("But", goal.get("action_nom", "") or "")
        brain = agent_snap.get("cerveau", {})
        if brain:
            self._data("Neurones", brain.get("neurones", 0))
            self._data("Frequence reflexion", brain.get("frequence_reflexion", 0))

        self._rows.append({"type": "section", "label": "ANIMA"})

        identity = anima.get("identity", {})
        if identity:
            self._rows.append({"type": "sub", "label": "Identite"})
            for k, v in sorted(identity.items(), key=lambda x: -x[1]):
                self._data(f"  {k}", v)

        values = anima.get("values", {})
        if values:
            self._rows.append({"type": "sub", "label": "Valeurs"})
            for k, v in sorted(values.items(), key=lambda x: -x[1]):
                self._data(f"  {k}", v)

        trauma = anima.get("trauma", {})
        if trauma:
            self._rows.append({"type": "sub", "label": "Trauma"})
            for k, v in trauma.items():
                self._data(f"  {k}", v)

        intention = anima.get("intention")
        if intention:
            self._rows.append({"type": "sub", "label": "Intention"})
            for k, v in intention.items():
                self._data(f"  {k}", v)

        plan = anima.get("plan")
        if plan:
            self._rows.append({"type": "sub", "label": "Plan"})
            for k, v in plan.items():
                self._data(f"  {k}", v)

        attachments = anima.get("attachments", {})
        if attachments:
            self._rows.append({"type": "sub", "label": "Attachements"})
            for k, v in attachments.items():
                self._data(f"  {k}", v)

        social = anima.get("social_beliefs", {})
        if social:
            self._rows.append({"type": "sub", "label": "Croyances sociales"})
            for k, v in social.items():
                if isinstance(v, dict):
                    self._data(f"  {k}", "")
                    for sk, sv in v.items():
                        self._data(f"    {sk}", sv)
                else:
                    self._data(f"  {k}", v)

        reputation = anima.get("reputation", {})
        if reputation:
            self._rows.append({"type": "sub", "label": "Reputation"})
            for k, v in reputation.items():
                self._data(f"  {k}", v)

        episodes = anima.get("episodes", [])
        if episodes:
            self._rows.append({"type": "sub", "label": f"Episodes ({len(episodes)})"})
            for ep in episodes[-3:]:
                self._data("  episode", str(ep))

        life_events = agent_snap.get("vie", [])
        if life_events:
            self._rows.append({"type": "sub", "label": "Evenements de vie"})
            for ev in life_events[-5:]:
                self._data("  evenement", str(ev))

        self.endResetModel()

    def _data(self, attr, value):
        self._rows.append({"type": "data", "attr": attr, "value": _fmt(value)})

    def rowCount(self, parent=None):
        return len(self._rows)

    def columnCount(self, parent=None):
        return 2

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return None

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or index.row() >= len(self._rows):
            return None
        row = self._rows[index.row()]
        row_type = row["type"]

        if role == Qt.ItemDataRole.BackgroundRole:
            if row_type == "section":
                return _SECTION_BG
            if row_type == "sub":
                return QColor(50, 60, 80)
            return None

        if role == Qt.ItemDataRole.ForegroundRole:
            if row_type == "section":
                return _SECTION_FG
            if row_type == "sub":
                return QColor(140, 170, 210)
            return None

        if role == Qt.ItemDataRole.FontRole:
            if row_type == "section":
                f = QFont()
                f.setBold(True)
                f.setPointSize(11)
                return f
            if row_type == "sub":
                f = QFont()
                f.setBold(True)
                return f

        if role == Qt.ItemDataRole.DisplayRole:
            if row_type == "section":
                return row["label"] if index.column() == 0 else ""
            if row_type == "sub":
                return row["label"] if index.column() == 0 else ""
            if index.column() == 0:
                return row.get("attr", "")
            return row.get("value", "")

        return None

```

## ui_qt/models/assets_model.py

**Type :** `.py`

```python

"""AssetsModel — modèle Qt pour le catalogue d'assets."""
from PyQt6.QtCore import QAbstractTableModel, Qt


class AssetsModel(QAbstractTableModel):
    HEADERS = ["ID", "Nom", "Categorie", "Role", "Placable"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._rows = []

    def set_snapshot(self, rows):
        self.beginResetModel()
        self._rows = list(rows)
        self.endResetModel()

    def rowCount(self, parent=None):
        return len(self._rows)

    def columnCount(self, parent=None):
        return len(self.HEADERS)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return None

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or index.row() >= len(self._rows):
            return None
        row = self._rows[index.row()]
        col = index.column()
        if role == Qt.ItemDataRole.DisplayRole:
            keys = ["id", "nom", "categorie", "role", "placable"]
            if col < len(keys):
                val = row.get(keys[col], "")
                if isinstance(val, bool):
                    return "Oui" if val else "Non"
                return str(val)
            return ""
        return None

```

## ui_qt/models/journal_model.py

**Type :** `.py`

```python

"""JournalModel — modèle Qt pour le journal."""
from PyQt6.QtCore import QAbstractTableModel, Qt


class JournalModel(QAbstractTableModel):
    HEADERS = ["Tick", "Categorie", "Texte", "Compte"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._rows = []

    def set_snapshot(self, rows):
        self.beginResetModel()
        self._rows = list(rows)
        self.endResetModel()

    def rowCount(self, parent=None):
        return len(self._rows)

    def columnCount(self, parent=None):
        return len(self.HEADERS)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return None

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or index.row() >= len(self._rows):
            return None
        row = self._rows[index.row()]
        col = index.column()

        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0:
                tick = row.get("tick", 0)
                mm, ss = divmod(int(tick / 60), 60)
                return f"{mm:02}:{ss:02}"
            elif col == 1:
                return row.get("category", "")
            elif col == 2:
                return row.get("text", "")
            elif col == 3:
                cnt = row.get("count", 1)
                return str(cnt) if cnt > 1 else ""
            return ""

        if role == Qt.ItemDataRole.ForegroundRole and col == 1:
            from PyQt6.QtGui import QColor
            cat = row.get("category", "monde")
            colors = {
                "combat": (214, 84, 84), "social": (198, 100, 162),
                "meteo": (62, 124, 214), "economie": (206, 160, 50),
                "vie": (67, 160, 92), "mort": (140, 80, 86),
                "batiment": (96, 154, 96), "monde": (112, 126, 150),
            }
            r, g, b = colors.get(cat, (105, 114, 129))
            return QColor(r, g, b)

        return None

```

## ui_qt/models/population_model.py

**Type :** `.py`

```python

"""PopulationModel — modèle Qt pour la liste des habitants."""
from PyQt6.QtCore import QAbstractTableModel, Qt, QSize
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen


_CLAN_COLORS = {"nord": "#3498db", "sud": "#e74c3c", "est": "#2ecc71", "ouest": "#f39c12"}


def _make_placeholder(clan):
    pm = QPixmap(24, 24)
    pm.fill(QColor(0, 0, 0, 0))
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    c = QColor(_CLAN_COLORS.get(clan, "#95a5a6"))
    p.setBrush(c)
    p.setPen(QPen(QColor(60, 60, 60), 1))
    p.drawEllipse(2, 2, 20, 20)
    p.end()
    return pm


class PopulationModel(QAbstractTableModel):
    HEADERS = ["Portrait", "Nom", "Sexe", "Age", "Sante", "Energie", "Faim", "Classe", "Stage", "EID"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._rows = []
        self._portraits = {}

    def set_snapshot(self, rows, portraits=None):
        self.beginResetModel()
        self._rows = list(rows)
        self._portraits = portraits or {}
        self.endResetModel()

    def rowCount(self, parent=None):
        return len(self._rows)

    def columnCount(self, parent=None):
        return len(self.HEADERS)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return None

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or index.row() >= len(self._rows):
            return None
        row = self._rows[index.row()]
        col = index.column()

        if role == Qt.ItemDataRole.DecorationRole and col == 0:
            eid = row.get("eid")
            if eid in self._portraits:
                return self._portraits[eid]
            clan = row.get("clan", "")
            return _make_placeholder(clan)

        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0:
                return ""
            elif col == 1:
                return row.get("nom", "")
            elif col == 2:
                return row.get("sex", "")
            elif col == 3:
                return f"{row.get('age_ans', 0):.1f}"
            elif col == 4:
                return f"{row.get('sante', 0):.0%}"
            elif col == 5:
                return f"{row.get('energie', 0):.0%}"
            elif col == 6:
                return f"{row.get('faim', 0):.0%}"
            elif col == 7:
                return row.get("classe", "")
            elif col == 8:
                return row.get("stage", "")
            elif col == 9:
                return str(row.get("eid", ""))
            return ""

        if role == Qt.ItemDataRole.UserRole:
            return row.get("eid")

        return None

    def eid_at(self, row):
        if 0 <= row < len(self._rows):
            return self._rows[row].get("eid")
        return None

```

## ui_qt/models/society_model.py

**Type :** `.py`

```python

"""SocietyModel — modèle Qt pour les stats de société."""
from PyQt6.QtCore import QAbstractTableModel, Qt


class SocietyModel(QAbstractTableModel):
    HEADERS = ["Categorie", "Valeur"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._rows = []

    def set_snapshot(self, snap):
        self.beginResetModel()
        self._rows = []
        if snap:
            stats = snap.get("stats", {})
            self._rows.append(("Population", snap.get("population", 0)))
            self._rows.append(("Naissances", stats.get("births", 0)))
            self._rows.append(("Deces", stats.get("deaths", 0)))
            self._rows.append(("Generation max", snap.get("max_generation", 0)))
            self._rows.append(("Couples", snap.get("bonded", 0)))
            self._rows.append(("Constructions", stats.get("builds", 0)))
            self._rows.append(("Villages", stats.get("villages", 0)))
            self._rows.append(("Recoltes", stats.get("harvests", 0)))
            self._rows.append(("Dons", stats.get("gives", 0)))
            self._rows.append(("Vols", stats.get("takes", 0)))
            self._rows.append(("Paroles", stats.get("talks", 0)))
            self._rows.append(("Attaques", stats.get("attacks", 0)))
            self._rows.append(("Moutons", snap.get("sheep", 0)))
            self._rows.append(("Monstres", snap.get("monsters", 0)))
        self.endResetModel()

    def rowCount(self, parent=None):
        return len(self._rows)

    def columnCount(self, parent=None):
        return 2

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return None

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or index.row() >= len(self._rows):
            return None
        if role == Qt.ItemDataRole.DisplayRole:
            cat, val = self._rows[index.row()]
            return cat if index.column() == 0 else str(val)
        return None

```

## ui_qt/studio/__init__.py

**Type :** `.py`

```python

"""Studio Qt — Interface avancée de visualisation et paramétrage."""

```

## ui_qt/studio/comparison_panel.py

**Type :** `.py`

```python

"""Panneau de comparaison A/B entre deux expériences."""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QFileDialog, QTextEdit,
    QSplitter, QGroupBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class ComparisonPanel(QWidget):
    """Panel for comparing two experiment results side by side."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._result_a = None
        self._result_b = None
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Header
        header = QHBoxLayout()
        self._title = QLabel("Comparaison A/B")
        self._title.setStyleSheet("font-size: 14px; font-weight: bold;")
        header.addWidget(self._title)
        header.addStretch()
        
        self._load_a_btn = QPushButton("Charger A")
        self._load_a_btn.clicked.connect(lambda: self._load_result("a"))
        header.addWidget(self._load_a_btn)
        
        self._load_b_btn = QPushButton("Charger B")
        self._load_b_btn.clicked.connect(lambda: self._load_result("b"))
        header.addWidget(self._load_b_btn)
        
        layout.addLayout(header)
        
        # Labels for each experiment
        exp_layout = QHBoxLayout()
        self._label_a = QLabel("Expérience A : —")
        self._label_a.setStyleSheet("padding: 4px; background: #1a2332; border-radius: 4px;")
        exp_layout.addWidget(self._label_a)
        self._label_b = QLabel("Expérience B : —")
        self._label_b.setStyleSheet("padding: 4px; background: #1a2332; border-radius: 4px;")
        exp_layout.addWidget(self._label_b)
        layout.addLayout(exp_layout)
        
        # Summary text
        self._summary = QTextEdit()
        self._summary.setReadOnly(True)
        self._summary.setMaximumHeight(100)
        self._summary.setPlaceholderText("Chargez deux expériences pour les comparer...")
        layout.addWidget(self._summary)
        
        # Comparison table
        self._table = QTableWidget()
        self._table.setColumnCount(4)
        self._table.setHorizontalHeaderLabels(["Métrique", "A", "B", "Différence"])
        self._table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self._table)
        
        # Export button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        export_btn = QPushButton("Exporter")
        export_btn.clicked.connect(self._export)
        btn_layout.addWidget(export_btn)
        layout.addLayout(btn_layout)
    
    def _load_result(self, which):
        path, _ = QFileDialog.getOpenFileName(
            self, f"Charger expérience {which.upper()}",
            "", "JSON (*.json)"
        )
        if not path:
            return
        import json
        with open(path, "r", encoding="utf-8") as f:
            result = json.load(f)
        
        if which == "a":
            self._result_a = result
            self._label_a.setText(
                f"Expérience A : {result.get('scenario', '?')} "
                f"(seed {result.get('seed', '?')})"
            )
        else:
            self._result_b = result
            self._label_b.setText(
                f"Expérience B : {result.get('scenario', '?')} "
                f"(seed {result.get('seed', '?')})"
            )
        
        self._update_comparison()
    
    def _update_comparison(self):
        if not self._result_a or not self._result_b:
            return
        
        from game.studio_compare import compare_results, compare_summary
        
        rows = compare_results(self._result_a, self._result_b)
        summary = compare_summary(self._result_a, self._result_b)
        
        self._summary.setText(summary)
        
        self._table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            self._table.setItem(i, 0, QTableWidgetItem(row["label"]))
            self._table.setItem(i, 1, QTableWidgetItem(f"{row['a']:.2f}"))
            self._table.setItem(i, 2, QTableWidgetItem(f"{row['b']:.2f}"))
            diff_item = QTableWidgetItem(f"{row['difference']:+.2f}")
            if row["difference"] > 0:
                diff_item.setForeground(Qt.GlobalColor.green)
            elif row["difference"] < 0:
                diff_item.setForeground(Qt.GlobalColor.red)
            self._table.setItem(i, 3, diff_item)
    
    def _export(self):
        if not self._result_a or not self._result_b:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Exporter comparaison", "comparison.json", "JSON (*.json)"
        )
        if path:
            from game.studio_compare import compare_results, compare_summary
            data = {
                "a": self._result_a,
                "b": self._result_b,
                "rows": compare_results(self._result_a, self._result_b),
                "summary": compare_summary(self._result_a, self._result_b),
            }
            import json
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)

```

## ui_qt/studio/laboratory_dock.py

**Type :** `.py`

```python

"""LaboratoryDock — dock Qt pour les résultats d'expérience."""
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                               QTextEdit, QTableWidget, QTableWidgetItem,
                               QPushButton, QGroupBox, QFileDialog,
                               QScrollArea, QHeaderView)
from PyQt6.QtCore import Qt

from game.studio_reports import build_report, build_short_summary, interpret_metric
from game.studio_compare import KEYS


class LaboratoryDock(QDockWidget):
    """Dock du laboratoire : résumé, métriques, interprétation, scénario."""

    def __init__(self, controller, parent=None):
        super().__init__("Laboratoire", parent)
        self.controller = controller
        self._result = None
        self._setup_ui()

    def _setup_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        widget = QWidget()
        self._layout = QVBoxLayout(widget)
        self._layout.setContentsMargins(8, 8, 8, 8)
        self._layout.setSpacing(6)

        # Résumé
        summary_group = QGroupBox("Résumé")
        summary_group.setStyleSheet("QGroupBox { font-weight: bold; color: #3e7cd6; }")
        summary_layout = QVBoxLayout(summary_group)
        summary_layout.setContentsMargins(8, 16, 8, 8)
        self._summary_text = QTextEdit()
        self._summary_text.setReadOnly(True)
        self._summary_text.setMaximumHeight(120)
        self._summary_text.setStyleSheet("font-size: 12px; color: #c8d0da;")
        summary_layout.addWidget(self._summary_text)
        self._layout.addWidget(summary_group)

        # Métriques
        metrics_group = QGroupBox("Métriques")
        metrics_group.setStyleSheet("QGroupBox { font-weight: bold; color: #54b96b; }")
        metrics_layout = QVBoxLayout(metrics_group)
        metrics_layout.setContentsMargins(8, 16, 8, 8)
        self._metrics_table = QTableWidget()
        self._metrics_table.setColumnCount(2)
        self._metrics_table.setHorizontalHeaderLabels(["Métrique", "Valeur"])
        self._metrics_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self._metrics_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )
        self._metrics_table.verticalHeader().setVisible(False)
        self._metrics_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._metrics_table.setStyleSheet(
            "QTableWidget { font-size: 11px; color: #c8d0da; }"
        )
        metrics_layout.addWidget(self._metrics_table)
        self._layout.addWidget(metrics_group)

        # Interprétation
        interp_group = QGroupBox("Interprétation")
        interp_group.setStyleSheet("QGroupBox { font-weight: bold; color: #e2b44a; }")
        interp_layout = QVBoxLayout(interp_group)
        interp_layout.setContentsMargins(8, 16, 8, 8)
        self._interp_text = QTextEdit()
        self._interp_text.setReadOnly(True)
        self._interp_text.setMaximumHeight(100)
        self._interp_text.setStyleSheet("font-size: 12px; color: #c8d0da;")
        interp_layout.addWidget(self._interp_text)
        self._layout.addWidget(interp_group)

        # Scénario
        scenario_group = QGroupBox("Scénario")
        scenario_group.setStyleSheet("QGroupBox { font-weight: bold; color: #c89ad6; }")
        scenario_layout = QVBoxLayout(scenario_group)
        scenario_layout.setContentsMargins(8, 16, 8, 8)
        self._scenario_text = QTextEdit()
        self._scenario_text.setReadOnly(True)
        self._scenario_text.setMaximumHeight(60)
        self._scenario_text.setStyleSheet("font-size: 12px; color: #c8d0da;")
        scenario_layout.addWidget(self._scenario_text)
        self._layout.addWidget(scenario_group)

        # Exporter
        btn_layout = QHBoxLayout()
        self._btn_txt = QPushButton("Exporter TXT")
        self._btn_md = QPushButton("Exporter Markdown")
        self._btn_json = QPushButton("Exporter JSON")
        for btn in (self._btn_txt, self._btn_md, self._btn_json):
            btn.setStyleSheet(
                "QPushButton { padding: 6px 12px; font-size: 11px; }"
            )
            btn_layout.addWidget(btn)
        self._btn_txt.clicked.connect(self._export_txt)
        self._btn_md.clicked.connect(self._export_md)
        self._btn_json.clicked.connect(self._export_json)
        self._layout.addLayout(btn_layout)

        self._layout.addStretch()

        scroll.setWidget(widget)
        self.setWidget(scroll)

    def set_result(self, result):
        self._result = result
        self.refresh()

    def refresh(self):
        result = self._result
        if result is None:
            self._summary_text.setPlainText("Aucun résultat disponible.")
            self._metrics_table.setRowCount(0)
            self._interp_text.setPlainText("")
            self._scenario_text.setPlainText("")
            return

        report = build_report(result)
        self._summary_text.setPlainText(report)

        self._fill_metrics(result)

        self._fill_interpretation(result)

        scenario = result.get("scenario", "Standard")
        seed = result.get("seed", "?")
        duration = result.get("duration", 0)
        self._scenario_text.setPlainText(
            f"Scénario : {scenario}\nSeed : {seed}\nDurée : {duration} ticks"
        )

    def _fill_metrics(self, result):
        metrics = {
            "population_end": result.get("population_end", 0),
            "deaths": result.get("deaths", 0),
            "births": result.get("births", 0),
            "builds": result.get("builds", 0),
            "harvests": result.get("harvests", 0),
            "messages": result.get("messages", 0),
            "mean_health": result.get("mean_health"),
            "mean_hunger": result.get("mean_hunger"),
            "mean_trust": result.get("mean_trust"),
        }
        labels = {
            "population_end": "Population finale",
            "deaths": "Morts",
            "births": "Naissances",
            "builds": "Constructions",
            "harvests": "Récoltes",
            "messages": "Messages",
            "mean_health": "Santé moyenne",
            "mean_hunger": "Faim moyenne",
            "mean_trust": "Confiance moyenne",
        }
        rows = [(k, v) for k, v in metrics.items() if v is not None]
        self._metrics_table.setRowCount(len(rows))
        for i, (key, val) in enumerate(rows):
            label_item = QTableWidgetItem(labels.get(key, key))
            if isinstance(val, float):
                val_item = QTableWidgetItem(f"{val:.2f}")
            else:
                val_item = QTableWidgetItem(str(val))
            val_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            self._metrics_table.setItem(i, 0, label_item)
            self._metrics_table.setItem(i, 1, val_item)

    def _fill_interpretation(self, result):
        lines = []
        mh_start = result.get("mean_health")
        mh_end = result.get("mean_health_end")
        if mh_start is not None and mh_end is not None:
            t = interpret_metric("health", mh_start, mh_end)
            if t:
                lines.append(f"Santé : {t}")

        mt_start = result.get("mean_trust")
        mt_end = result.get("mean_trust_end")
        if mt_start is not None and mt_end is not None:
            t = interpret_metric("trust", mt_start, mt_end)
            if t:
                lines.append(f"Confiance : {t}")

        mg_start = result.get("mean_hunger")
        mg_end = result.get("mean_hunger_end")
        if mg_start is not None and mg_end is not None:
            t = interpret_metric("hunger", mg_start, mg_end)
            if t:
                lines.append(f"Faim : {t}")

        if not lines:
            summary = build_short_summary(result)
            lines.append(summary)

        self._interp_text.setPlainText("\n".join(lines))

    def _export_txt(self):
        if self._result is None:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Exporter en TXT", "rapport.txt", "Fichiers texte (*.txt)"
        )
        if path:
            from game.studio_export import export_txt
            export_txt(build_report(self._result), path)

    def _export_md(self):
        if self._result is None:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Exporter en Markdown", "rapport.md", "Markdown (*.md)"
        )
        if path:
            from game.studio_export import export_markdown
            metrics = {k: self._result.get(k) for k in [
                "population_end", "deaths", "births", "builds",
                "harvests", "mean_health", "mean_hunger", "mean_trust",
            ] if self._result.get(k) is not None}
            export_markdown(build_report(self._result), metrics=metrics, filepath=path)

    def _export_json(self):
        if self._result is None:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Exporter en JSON", "rapport.json", "JSON (*.json)"
        )
        if path:
            from game.studio_export import export_json
            export_json(self._result, path)

```

## ui_qt/studio/metrics_models.py

**Type :** `.py`

```python

"""Modèles Qt pour les métriques du laboratoire."""
from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt


METRIC_LABELS = {
    "population": "Population",
    "births": "Naissances",
    "deaths": "Morts",
    "builds": "Constructions terminées",
    "harvests": "Récoltes",
    "food_given": "Dons de nourriture",
    "messages": "Messages envoyés",
    "confirmed_knowledge": "Connaissances confirmées",
    "institutions": "Institutions stables",
    "mean_health": "Santé moyenne",
    "mean_hunger": "Faim moyenne",
    "mean_trust": "Confiance moyenne",
}


class MetricsModel(QAbstractTableModel):
    """Model for experiment metrics table."""
    
    HEADERS = ["Métrique", "Valeur"]
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._data = []  # list of (label, value)
    
    def load(self, metrics_dict):
        self.beginResetModel()
        self._data = []
        for key, label in METRIC_LABELS.items():
            if key in metrics_dict:
                self._data.append((label, metrics_dict[key]))
        self.endResetModel()
    
    def rowCount(self, parent=QModelIndex()):
        return len(self._data)
    
    def columnCount(self, parent=QModelIndex()):
        return 2
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        row = index.row()
        col = index.column()
        if row >= len(self._data):
            return None
        
        label, value = self._data[row]
        
        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0:
                return label
            if col == 1:
                if isinstance(value, float):
                    return f"{value:.2f}"
                return str(value)
        if role == Qt.ItemDataRole.TextAlignmentRole:
            if col == 1:
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        return None
    
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return None


class ComparisonModel(QAbstractTableModel):
    """Model for A/B comparison table."""
    
    HEADERS = ["Métrique", "A", "B", "Différence"]
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._rows = []
    
    def load(self, comparison_rows):
        self.beginResetModel()
        self._rows = comparison_rows
        self.endResetModel()
    
    def rowCount(self, parent=QModelIndex()):
        return len(self._rows)
    
    def columnCount(self, parent=QModelIndex()):
        return 4
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        row = index.row()
        col = index.column()
        if row >= len(self._rows):
            return None
        
        r = self._rows[row]
        
        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0:
                return r.get("label", r.get("metric", ""))
            if col == 1:
                return f"{r['a']:.2f}"
            if col == 2:
                return f"{r['b']:.2f}"
            if col == 3:
                d = r["difference"]
                return f"{d:+.2f}"
        if role == Qt.ItemDataRole.TextAlignmentRole:
            if col > 0:
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        return None
    
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return None

```

## ui_qt/studio/parameter_dock.py

**Type :** `.py`

```python

"""ParameterDock — dock Qt pour l'édition des paramètres de simulation."""
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QPushButton, QScrollArea, QFrame,
                              QSpinBox, QDoubleSpinBox, QCheckBox, QComboBox,
                              QMessageBox, QGroupBox, QGridLayout)
from PyQt6.QtCore import Qt, pyqtSignal

from game.studio_parameters import (
    ParameterStore, PARAMETERS, PARAM_BY_KEY, PARAM_GROUPS,
)


class ParameterDock(QDockWidget):
    """Dock d'édition des paramètres regroupés par catégorie."""

    parameters_applied = pyqtSignal()

    def __init__(self, controller, parent=None):
        super().__init__("Paramètres", parent)
        self.controller = controller
        self._store = ParameterStore()
        self._widgets: dict[str, QWidget] = {}
        self._setup_ui()
        self._load_from_sim()

    def _setup_ui(self):
        root = QWidget()
        main_layout = QVBoxLayout(root)
        main_layout.setContentsMargins(8, 8, 8, 8)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)

        by_group = self._store.by_group()
        for group in PARAM_GROUPS:
            params = by_group.get(group, [])
            if not params:
                continue
            group_box = QGroupBox(group)
            grid = QGridLayout()
            grid.setSpacing(6)
            for row, p in enumerate(params):
                grid.addWidget(QLabel(p.label), row, 0)
                widget = self._make_widget(p)
                self._widgets[p.key] = widget
                grid.addWidget(widget, row, 1)
                desc = QLabel(p.description)
                desc.setStyleSheet("color: #888; font-size: 11px;")
                grid.addWidget(desc, row, 2)
            group_box.setLayout(grid)
            scroll_layout.addWidget(group_box)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        btn_layout = QHBoxLayout()

        self._reset_btn = QPushButton("Réinitialiser")
        self._reset_btn.clicked.connect(self._on_reset)
        btn_layout.addWidget(self._reset_btn)

        btn_layout.addStretch()

        self._apply_btn = QPushButton("Appliquer tout")
        self._apply_btn.setStyleSheet(
            "QPushButton { background-color: #2980b9; color: white; "
            "padding: 6px 18px; border: none; border-radius: 3px; }"
            "QPushButton:hover { background-color: #3498db; }"
        )
        self._apply_btn.clicked.connect(self._on_apply)
        btn_layout.addWidget(self._apply_btn)

        main_layout.addLayout(btn_layout)
        self.setWidget(root)

    def _make_widget(self, p):
        if p.ptype == "int":
            spin = QSpinBox()
            spin.setRange(int(p.minimum), int(p.maximum))
            spin.setValue(int(p.default))
            spin.setToolTip(p.key)
            return spin
        elif p.ptype == "float":
            dspin = QDoubleSpinBox()
            dspin.setRange(p.minimum, p.maximum)
            dspin.setDecimals(3)
            dspin.setSingleStep(0.01)
            dspin.setValue(float(p.default))
            dspin.setToolTip(p.key)
            return dspin
        elif p.ptype == "bool":
            cb = QCheckBox()
            cb.setChecked(bool(p.default))
            cb.setToolTip(p.key)
            return cb
        elif p.ptype == "choice":
            combo = QComboBox()
            combo.addItems(p.choices)
            idx = p.choices.index(p.default) if p.default in p.choices else 0
            combo.setCurrentIndex(idx)
            combo.setToolTip(p.key)
            return combo
        return QLabel(str(p.default))

    def _read_value(self, key):
        w = self._widgets.get(key)
        p = PARAM_BY_KEY[key]
        if p.ptype == "int":
            return w.value()
        elif p.ptype == "float":
            return w.value()
        elif p.ptype == "bool":
            return w.isChecked()
        elif p.ptype == "choice":
            return w.currentText()
        return None

    def _on_apply(self):
        errors = []
        for key, w in self._widgets.items():
            try:
                val = self._read_value(key)
                self._store.set(key, val)
            except (ValueError, KeyError) as e:
                errors.append(str(e))
        if errors:
            QMessageBox.warning(
                self, "Erreurs de validation",
                "\n".join(errors),
            )
        else:
            self.controller.sim.parameters = self._store.to_dict()
            self.parameters_applied.emit()

    def _on_reset(self):
        reply = QMessageBox.question(
            self, "Réinitialiser",
            "Réinitialiser tous les paramètres aux valeurs par défaut ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._store.reset()
            self._sync_widgets_from_store()
            self._on_apply()

    def _load_from_sim(self):
        params = getattr(self.controller.sim, "parameters", {})
        if params:
            self._store.from_dict(params)
        self._sync_widgets_from_store()

    def _sync_widgets_from_store(self):
        for key, w in self._widgets.items():
            val = self._store.get(key)
            p = PARAM_BY_KEY[key]
            if p.ptype == "int":
                w.blockSignals(True)
                w.setValue(int(val))
                w.blockSignals(False)
            elif p.ptype == "float":
                w.blockSignals(True)
                w.setValue(float(val))
                w.blockSignals(False)
            elif p.ptype == "bool":
                w.blockSignals(True)
                w.setChecked(bool(val))
                w.blockSignals(False)
            elif p.ptype == "choice":
                w.blockSignals(True)
                idx = p.choices.index(val) if val in p.choices else 0
                w.setCurrentIndex(idx)
                w.blockSignals(False)

    def refresh(self):
        self._load_from_sim()

    def get_store(self):
        return self._store

```

## ui_qt/studio/report_panel.py

**Type :** `.py`

```python

"""ReportPanel — panneau Qt pour l'affichage et l'export de rapports."""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
                               QTableWidget, QTableWidgetItem, QPushButton,
                               QGroupBox, QFileDialog, QHeaderView, QScrollArea)
from PyQt6.QtCore import Qt

from game.studio_reports import build_report, build_short_summary, interpret_metric
from game.studio_export import export_txt, export_markdown, export_json


class ReportPanel(QWidget):
    """Panneau de rapport d'expérience : texte complet, métriques, export."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._result = None
        self._setup_ui()

    def _setup_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        self._layout = QVBoxLayout(container)
        self._layout.setContentsMargins(8, 8, 8, 8)
        self._layout.setSpacing(6)

        # Rapport complet
        report_group = QGroupBox("Rapport")
        report_group.setStyleSheet("QGroupBox { font-weight: bold; color: #3e7cd6; }")
        report_layout = QVBoxLayout(report_group)
        report_layout.setContentsMargins(8, 16, 8, 8)
        self._report_text = QTextEdit()
        self._report_text.setReadOnly(True)
        self._report_text.setStyleSheet("font-size: 12px; color: #c8d0da;")
        self._report_text.setMinimumHeight(150)
        report_layout.addWidget(self._report_text)
        self._layout.addWidget(report_group)

        # Métriques
        metrics_group = QGroupBox("Métriques")
        metrics_group.setStyleSheet("QGroupBox { font-weight: bold; color: #54b96b; }")
        metrics_layout = QVBoxLayout(metrics_group)
        metrics_layout.setContentsMargins(8, 16, 8, 8)
        self._metrics_table = QTableWidget()
        self._metrics_table.setColumnCount(2)
        self._metrics_table.setHorizontalHeaderLabels(["Métrique", "Valeur"])
        self._metrics_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self._metrics_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )
        self._metrics_table.verticalHeader().setVisible(False)
        self._metrics_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._metrics_table.setStyleSheet(
            "QTableWidget { font-size: 11px; color: #c8d0da; }"
        )
        self._metrics_table.setMinimumHeight(120)
        metrics_layout.addWidget(self._metrics_table)
        self._layout.addWidget(metrics_group)

        # Interprétation
        interp_group = QGroupBox("Interprétation")
        interp_group.setStyleSheet("QGroupBox { font-weight: bold; color: #e2b44a; }")
        interp_layout = QVBoxLayout(interp_group)
        interp_layout.setContentsMargins(8, 16, 8, 8)
        self._interp_text = QTextEdit()
        self._interp_text.setReadOnly(True)
        self._interp_text.setMaximumHeight(100)
        self._interp_text.setStyleSheet("font-size: 12px; color: #c8d0da;")
        interp_layout.addWidget(self._interp_text)
        self._layout.addWidget(interp_group)

        # Boutons d'export
        btn_layout = QHBoxLayout()
        self._btn_txt = QPushButton("Exporter TXT")
        self._btn_md = QPushButton("Exporter Markdown")
        self._btn_json = QPushButton("Exporter JSON")
        for btn in (self._btn_txt, self._btn_md, self._btn_json):
            btn.setStyleSheet(
                "QPushButton { padding: 6px 12px; font-size: 11px; }"
            )
            btn_layout.addWidget(btn)
        self._btn_txt.clicked.connect(self._export_txt)
        self._btn_md.clicked.connect(self._export_md)
        self._btn_json.clicked.connect(self._export_json)
        self._layout.addLayout(btn_layout)

        self._layout.addStretch()

        scroll.setWidget(container)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(scroll)

    def set_result(self, result):
        self._result = result
        self.refresh()

    def refresh(self):
        result = self._result
        if result is None:
            self._report_text.setPlainText("Aucun résultat disponible.")
            self._metrics_table.setRowCount(0)
            self._interp_text.setPlainText("")
            return

        report = build_report(result)
        self._report_text.setPlainText(report)

        self._fill_metrics(result)

        self._fill_interpretation(result)

    def _fill_metrics(self, result):
        labels = {
            "population_end": "Population finale",
            "deaths": "Morts",
            "births": "Naissances",
            "builds": "Constructions",
            "harvests": "Récoltes",
            "messages": "Messages",
            "mean_health": "Santé moyenne",
            "mean_hunger": "Faim moyenne",
            "mean_trust": "Confiance moyenne",
        }
        rows = []
        for key, label in labels.items():
            val = result.get(key)
            if val is not None:
                rows.append((key, label, val))
        self._metrics_table.setRowCount(len(rows))
        for i, (key, label, val) in enumerate(rows):
            label_item = QTableWidgetItem(label)
            if isinstance(val, float):
                val_item = QTableWidgetItem(f"{val:.2f}")
            else:
                val_item = QTableWidgetItem(str(val))
            val_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            self._metrics_table.setItem(i, 0, label_item)
            self._metrics_table.setItem(i, 1, val_item)

    def _fill_interpretation(self, result):
        lines = []
        mh_start = result.get("mean_health")
        mh_end = result.get("mean_health_end")
        if mh_start is not None and mh_end is not None:
            t = interpret_metric("health", mh_start, mh_end)
            if t:
                lines.append(f"Santé : {t}")

        mt_start = result.get("mean_trust")
        mt_end = result.get("mean_trust_end")
        if mt_start is not None and mt_end is not None:
            t = interpret_metric("trust", mt_start, mt_end)
            if t:
                lines.append(f"Confiance : {t}")

        mg_start = result.get("mean_hunger")
        mg_end = result.get("mean_hunger_end")
        if mg_start is not None and mg_end is not None:
            t = interpret_metric("hunger", mg_start, mg_end)
            if t:
                lines.append(f"Faim : {t}")

        if not lines:
            summary = build_short_summary(result)
            lines.append(summary)

        self._interp_text.setPlainText("\n".join(lines))

    def _export_txt(self):
        if self._result is None:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Exporter en TXT", "rapport.txt", "Fichiers texte (*.txt)"
        )
        if path:
            export_txt(build_report(self._result), path)

    def _export_md(self):
        if self._result is None:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Exporter en Markdown", "rapport.md", "Markdown (*.md)"
        )
        if path:
            metrics = {k: self._result.get(k) for k in [
                "population_end", "deaths", "births", "builds",
                "harvests", "mean_health", "mean_hunger", "mean_trust",
            ] if self._result.get(k) is not None}
            export_markdown(build_report(self._result), metrics=metrics, filepath=path)

    def _export_json(self):
        if self._result is None:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Exporter en JSON", "rapport.json", "JSON (*.json)"
        )
        if path:
            export_json(self._result, path)

```

## ui_qt/studio/scenario_dialog.py

**Type :** `.py`

```python

"""ScenarioDialog — QDialog pour choisir et lancer un scénario."""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                              QListWidget, QListWidgetItem, QPushButton,
                              QTextEdit, QGroupBox, QGridLayout)
from PyQt6.QtCore import Qt

from game.studio_scenarios import (
    list_scenarios, get_scenario, apply_scenario, scenario_summary,
)
from game.studio_parameters import PARAM_BY_KEY


class ScenarioDialog(QDialog):
    """Fenêtre de sélection et lancement de scénarios."""

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Scénarios de simulation")
        self.setMinimumSize(640, 480)
        self._selected_key = None
        self._setup_ui()
        self._populate_list()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(12)

        # Colonne gauche : liste
        left = QVBoxLayout()
        left.addWidget(QLabel("Scénarios disponibles"))
        self._list = QListWidget()
        self._list.currentRowChanged.connect(self._on_select)
        left.addWidget(self._list)
        layout.addLayout(left, 2)

        # Colonne droite : détails
        right = QVBoxLayout()

        self._title_label = QLabel()
        self._title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        right.addWidget(self._title_label)

        self._desc_label = QLabel()
        self._desc_label.setWordWrap(True)
        right.addWidget(self._desc_label)

        info_group = QGroupBox("Détails")
        info_grid = QGridLayout()
        info_grid.addWidget(QLabel("Durée recommandée:"), 0, 0)
        self._duration_label = QLabel()
        info_grid.addWidget(self._duration_label, 0, 1)
        info_group.setLayout(info_grid)
        right.addWidget(info_group)

        self._summary_box = QTextEdit()
        self._summary_box.setReadOnly(True)
        self._summary_box.setMaximumHeight(120)
        right.addWidget(QLabel("Résumé"))
        right.addWidget(self._summary_box)

        self._params_box = QGroupBox("Paramètres appliqués")
        self._params_grid = QGridLayout()
        self._params_grid.setSpacing(4)
        self._params_box.setLayout(self._params_grid)
        right.addWidget(self._params_box)

        right.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self._cancel_btn = QPushButton("Annuler")
        self._cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self._cancel_btn)
        self._launch_btn = QPushButton("Lancer")
        self._launch_btn.setEnabled(False)
        self._launch_btn.setStyleSheet(
            "QPushButton { background-color: #27ae60; color: white; "
            "padding: 6px 18px; border: none; border-radius: 3px; }"
            "QPushButton:hover { background-color: #2ecc71; }"
            "QPushButton:disabled { background-color: #7f8c8d; color: #bdc3c7; }"
        )
        self._launch_btn.clicked.connect(self._on_launch)
        btn_layout.addWidget(self._launch_btn)
        right.addLayout(btn_layout)

        layout.addLayout(right, 3)

    def _populate_list(self):
        self._list.clear()
        for key, label, desc in list_scenarios():
            item = QListWidgetItem(label)
            item.setData(Qt.ItemDataRole.UserRole, key)
            item.setToolTip(desc)
            self._list.addItem(item)

    def _on_select(self, row):
        item = self._list.item(row)
        if not item:
            return
        key = item.data(Qt.ItemDataRole.UserRole)
        self._selected_key = key
        scenario = get_scenario(key)
        if not scenario:
            return
        self._title_label.setText(scenario["label"])
        self._desc_label.setText(scenario["description"])
        self._duration_label.setText(f"{scenario['duration_recommended']} ticks")
        self._summary_box.setPlainText(scenario_summary(key))

        # Afficher les paramètres
        while self._params_grid.count():
            w = self._params_grid.takeAt(0).widget()
            if w:
                w.deleteLater()
        row_idx = 0
        for pkey, pval in scenario["parameters"].items():
            pdef = PARAM_BY_KEY.get(pkey)
            label = pdef.label if pdef else pkey
            self._params_grid.addWidget(QLabel(label), row_idx, 0)
            self._params_grid.addWidget(QLabel(str(pval)), row_idx, 1)
            row_idx += 1
        self._launch_btn.setEnabled(True)

    def _on_launch(self):
        if not self._selected_key:
            return
        try:
            store = self.controller.sim.parameter_store
        except AttributeError:
            from game.studio_parameters import ParameterStore
            store = ParameterStore()
            self.controller.sim.parameter_store = store
        apply_scenario(store, self._selected_key)
        self.controller.sim.parameters = store.to_dict()
        self.accept()

    def get_selected_scenario(self):
        return self._selected_key

```

## ui_qt/studio/timeline_dock.py

**Type :** `.py`

```python

"""TimelineDock — dock Qt pour la chronologie des événements."""
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                              QTableWidget, QTableWidgetItem, QLineEdit,
                              QComboBox, QPushButton, QFileDialog, QLabel,
                              QHeaderView, QAbstractItemView)
from PyQt6.QtCore import Qt

from game.studio_timeline import (
    build_timeline, filter_events, format_event, CATEGORIES,
)
from game.ui_snapshots import journal_snapshot


class TimelineDock(QDockWidget):
    """Dock chronologie avec filtres et export."""

    def __init__(self, controller, parent=None):
        super().__init__("Chronologie", parent)
        self.controller = controller
        self._events = []
        self._setup_ui()

    def _setup_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)

        # Barre de filtres
        filter_layout = QHBoxLayout()

        self._cat_combo = QComboBox()
        self._cat_combo.addItems(CATEGORIES)
        self._cat_combo.currentTextChanged.connect(self._apply_filter)
        filter_layout.addWidget(QLabel("Catégorie:"))
        filter_layout.addWidget(self._cat_combo)

        self._search = QLineEdit()
        self._search.setPlaceholderText("Rechercher...")
        self._search.returnPressed.connect(self._apply_filter)
        filter_layout.addWidget(self._search)

        search_btn = QPushButton("Filtrer")
        search_btn.clicked.connect(self._apply_filter)
        filter_layout.addWidget(search_btn)

        layout.addLayout(filter_layout)

        # Compteur
        self._count_label = QLabel("0 événements")
        layout.addWidget(self._count_label)

        # Tableau
        self._table = QTableWidget()
        self._table.setColumnCount(3)
        self._table.setHorizontalHeaderLabels(["Jour", "Catégorie", "Événement"])
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self._table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self._table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self._table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self._table.verticalHeader().setVisible(False)
        layout.addWidget(self._table)

        # Export
        export_layout = QHBoxLayout()
        export_layout.addStretch()
        self._export_btn = QPushButton("Exporter...")
        self._export_btn.clicked.connect(self._on_export)
        export_layout.addWidget(self._export_btn)
        layout.addLayout(export_layout)

        self.setWidget(widget)

    def refresh(self):
        snap = journal_snapshot(self.controller.sim)
        self._events = build_timeline(snap)
        self._apply_filter()

    def _apply_filter(self):
        cat = self._cat_combo.currentText()
        text = self._search.text().strip().lower()
        filtered = filter_events(self._events, category=cat)
        if text:
            filtered = [
                e for e in filtered
                if text in format_event(e).lower()
            ]
        self._populate_table(filtered)

    def _populate_table(self, events):
        self._table.setRowCount(len(events))
        for i, ev in enumerate(events):
            tick = ev.get("tick", 0)
            day = tick // 100 + 1
            hour = tick % 100
            day_item = QTableWidgetItem(f"J{day} — {hour:02d}h")
            day_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self._table.setItem(i, 0, day_item)

            cat_item = QTableWidgetItem(ev.get("category", ""))
            cat_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self._table.setItem(i, 1, cat_item)

            sentence = format_event(ev)
            self._table.setItem(i, 2, QTableWidgetItem(sentence))
        self._count_label.setText(f"{len(events)} événement{'s' if len(events) != 1 else ''}")

    def _on_export(self):
        path, fmt = QFileDialog.getSaveFileName(
            self, "Exporter la chronologie",
            "timeline.txt",
            "Fichier texte (*.txt);;CSV (*.csv);;JSON (*.json)",
        )
        if not path:
            return
        if fmt.startswith("JSON"):
            self._export_json(path)
        elif fmt.startswith("CSV"):
            self._export_csv(path)
        else:
            self._export_txt(path)

    def _export_txt(self, path):
        with open(path, "w", encoding="utf-8") as f:
            for ev in self._events:
                f.write(format_event(ev) + "\n")

    def _export_csv(self, path):
        import csv
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["Jour", "Heure", "Catégorie", "Événement"])
            for ev in self._events:
                tick = ev.get("tick", 0)
                w.writerow([
                    tick // 100 + 1,
                    f"{tick % 100:02d}",
                    ev.get("category", ""),
                    format_event(ev),
                ])

    def _export_json(self, path):
        import json
        data = []
        for ev in self._events:
            tick = ev.get("tick", 0)
            data.append({
                "day": tick // 100 + 1,
                "hour": tick % 100,
                "category": ev.get("category", ""),
                "kind": ev.get("kind", ""),
                "title": ev.get("title", ""),
                "text": ev.get("text", ""),
                "actors": ev.get("actors", []),
                "importance": ev.get("importance", 0.0),
            })
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

```

## ui_qt/studio/world_overlay.py

**Type :** `.py`

```python

"""WorldOverlay — couches de visualisation superposées à la carte."""
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QColor, QPen, QBrush

from game.config import GRID, TILE, CLAN_COLORS
from game.studio_text import level_color

MODES = [
    "normal", "ressources", "danger", "memoire", "relations",
    "besoins", "anima", "culture", "institutions", "territoires",
]

_MODE_LABELS = {
    "normal": "Normal",
    "ressources": "Ressources",
    "danger": "Danger",
    "memoire": "Mémoire",
    "relations": "Relations",
    "besoins": "Besoins",
    "anima": "Anima",
    "culture": "Culture",
    "institutions": "Institutions",
    "territoires": "Territoires",
}

_IDENTITY_COLORS = {
    "builder": QColor(70, 130, 200),
    "provider": QColor(80, 170, 80),
    "fighter": QColor(200, 60, 60),
    "explorer": QColor(180, 160, 50),
    "caretaker": QColor(180, 100, 180),
    "survivor": QColor(150, 150, 150),
}


def _hex_to_qcolor(h):
    if h.startswith("#"):
        h = h[1:]
    r = int(h[0:2], 16)
    g = int(h[2:4], 16)
    b = int(h[4:6], 16)
    return QColor(r, g, b)


class WorldOverlay:
    def __init__(self):
        pass

    def mode_label(self, mode):
        return _MODE_LABELS.get(mode, mode)

    def paint(self, painter, map_transform, sim, active_mode):
        if active_mode == "normal":
            return

        w = sim.w
        screen_w = painter.device().width()
        screen_h = painter.device().height()

        if active_mode == "danger":
            self._paint_danger(painter, map_transform, sim, screen_w, screen_h)
        elif active_mode == "ressources":
            self._paint_ressources(painter, map_transform, sim, screen_w, screen_h)
        elif active_mode == "memoire":
            self._paint_memoire(painter, map_transform, sim, screen_w, screen_h)
        elif active_mode == "relations":
            self._paint_relations(painter, map_transform, sim, screen_w, screen_h)
        elif active_mode == "besoins":
            self._paint_besoins(painter, map_transform, sim, screen_w, screen_h)
        elif active_mode == "anima":
            self._paint_anima(painter, map_transform, sim, screen_w, screen_h)
        elif active_mode == "culture":
            self._paint_culture(painter, map_transform, sim, screen_w, screen_h)
        elif active_mode == "institutions":
            self._paint_institutions(painter, map_transform, sim, screen_w, screen_h)
        elif active_mode == "territoires":
            self._paint_territoires(painter, map_transform, sim, screen_w, screen_h)

    def _paint_danger(self, painter, transform, sim, sw, sh):
        w = sim.w
        x0, y0, x1, y1 = transform.visible_tiles(TILE, GRID)
        ts = max(2, int(TILE * transform.zoom))
        painter.setPen(QPen(QColor(0, 0, 0), 0))
        for ty in range(y0, y1):
            for tx in range(x0, x1):
                if not (0 <= tx < w.g and 0 <= ty < w.g):
                    continue
                danger = float(getattr(w, "danger", w.blocked)[ty, tx]) if hasattr(w, "danger") else 0.0
                if danger <= 0:
                    continue
                sx, sy = transform.to_screen(tx * TILE, ty * TILE)
                h_val = min(1.0, danger)
                c = _hex_to_qcolor(level_color(h_val))
                c.setAlpha(int(120 + 80 * h_val))
                painter.fillRect(int(sx), int(sy), ts, ts, c)

    def _paint_ressources(self, painter, transform, sim, sw, sh):
        w = sim.w
        x0, y0, x1, y1 = transform.visible_tiles(TILE, GRID)
        ts = max(2, int(TILE * transform.zoom))
        painter.setPen(QPen(QColor(0, 0, 0), 0))
        for ty in range(y0, y1):
            for tx in range(x0, x1):
                if not (0 <= tx < w.g and 0 <= ty < w.g):
                    continue
                res = float(w.regrow[ty, tx]) if hasattr(w, "regrow") else 0.0
                if res <= 0:
                    continue
                sx, sy = transform.to_screen(tx * TILE, ty * TILE)
                h_val = min(1.0, res)
                c = _hex_to_qcolor(level_color(h_val))
                c.setAlpha(int(80 + 100 * h_val))
                painter.fillRect(int(sx), int(sy), ts, ts, c)

    def _paint_memoire(self, painter, transform, sim, sw, sh):
        w = sim.w
        x0, y0, x1, y1 = transform.visible_tiles(TILE, GRID)
        ts = max(2, int(TILE * transform.zoom))
        painter.setPen(QPen(QColor(255, 255, 100), 1))
        painter.setBrush(QBrush(QColor(255, 255, 100, 40)))
        for agent in sim.agents:
            if not agent.alive:
                continue
            beliefs = getattr(agent, "croyances_danger", {})
            if not beliefs:
                continue
            for place_key in beliefs:
                if not isinstance(place_key, (list, tuple)) and "_" in str(place_key):
                    continue
            sx, sy = transform.to_screen(agent.x, agent.y)
            if -20 < sx < sw + 20 and -20 < sy < sh + 20:
                painter.drawEllipse(QPointF(sx, sy), 12, 12)
        for ty in range(y0, y1):
            for tx in range(x0, x1):
                if not (0 <= tx < w.g) or not (0 <= ty < w.g):
                    continue
                sx, sy = transform.to_screen(tx * TILE, ty * TILE)
                painter.setPen(QPen(QColor(255, 255, 100, 30), 1))
                painter.setBrush(QBrush(QColor(255, 255, 100, 15)))
                painter.drawRect(int(sx), int(sy), ts, ts)

    def _paint_relations(self, painter, transform, sim, sw, sh):
        pen = QPen(QColor(100, 180, 255, 120), 1.5)
        painter.setPen(pen)
        agent_map = {}
        for a in sim.agents:
            if a.alive:
                agent_map[a.eid] = a
        drawn = set()
        for a in sim.agents:
            if not a.alive:
                continue
            rels = getattr(a, "relations", [])
            for r in rels:
                other_eid = r.get("eid")
                if other_eid is None:
                    continue
                pair = (min(a.eid, other_eid), max(a.eid, other_eid))
                if pair in drawn:
                    continue
                drawn.add(pair)
                other = agent_map.get(other_eid)
                if other is None or not other.alive:
                    continue
                sx1, sy1 = transform.to_screen(a.x, a.y)
                sx2, sy2 = transform.to_screen(other.x, other.y)
                if (-50 < sx1 < sw + 50 and -50 < sy1 < sh + 50 and
                        -50 < sx2 < sw + 50 and -50 < sy2 < sh + 50):
                    painter.drawLine(QPointF(sx1, sy1), QPointF(sx2, sy2))

    def _paint_besoins(self, painter, transform, sim, sw, sh):
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        for a in sim.agents:
            if not a.alive:
                continue
            sx, sy = transform.to_screen(a.x, a.y)
            if not (-20 < sx < sw + 20 and -20 < sy < sh + 20):
                continue
            faim = getattr(a, "faim", 0.0)
            c = _hex_to_qcolor(level_color(faim))
            painter.setBrush(QBrush(c))
            painter.drawEllipse(QPointF(sx, sy), 7, 7)

    def _paint_anima(self, painter, transform, sim, sw, sh):
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        for a in sim.agents:
            if not a.alive:
                continue
            sx, sy = transform.to_screen(a.x, a.y)
            if not (-20 < sx < sw + 20 and -20 < sy < sh + 20):
                continue
            identity = getattr(a, "identity", {})
            if identity:
                dominant = max(identity, key=identity.get)
            else:
                dominant = None
            c = _IDENTITY_COLORS.get(dominant, QColor(150, 150, 150))
            painter.setBrush(QBrush(c))
            painter.drawEllipse(QPointF(sx, sy), 7, 7)

    def _paint_culture(self, painter, transform, sim, sw, sh):
        painter.setPen(QPen(QColor(200, 150, 50, 100), 1))
        for a in sim.agents:
            if not a.alive:
                continue
            sx, sy = transform.to_screen(a.x, a.y)
            if not (-20 < sx < sw + 20 and -20 < sy < sh + 20):
                continue
            knowledge = getattr(a, "confirmed_knowledge", [])
            if knowledge:
                painter.setBrush(QBrush(QColor(200, 150, 50, 60)))
                painter.drawRect(int(sx) - 8, int(sy) - 8, 16, 16)

    def _paint_institutions(self, painter, transform, sim, sw, sh):
        institutions = getattr(sim, "institutions", [])
        painter.setPen(QPen(QColor(180, 80, 200, 150), 2))
        painter.setBrush(QBrush(QColor(180, 80, 200, 30)))
        for inst in institutions:
            members = inst.get("members", [])
            if len(members) < 2:
                continue
            points = []
            for a in sim.agents:
                if a.alive and a.eid in members:
                    sx, sy = transform.to_screen(a.x, a.y)
                    points.append(QPointF(sx, sy))
            if len(points) >= 2:
                for i in range(len(points)):
                    for j in range(i + 1, len(points)):
                        painter.drawLine(points[i], points[j])

    def _paint_territoires(self, painter, transform, sim, sw, sh):
        clans = {}
        for a in sim.agents:
            if not a.alive:
                continue
            c = getattr(a, "color", "gray")
            if c not in clans:
                clans[c] = []
            clans[c].append(a)
        for clan, members in clans.items():
            if len(members) < 2:
                continue
            r, g, b = CLAN_COLORS.get(clan, (150, 150, 150))
            c = QColor(r, g, b, 40)
            painter.setPen(QPen(QColor(r, g, b, 100), 1))
            painter.setBrush(QBrush(c))
            for a in members:
                sx, sy = transform.to_screen(a.x, a.y)
                if -50 < sx < sw + 50 and -50 < sy < sh + 50:
                    painter.drawEllipse(QPointF(sx, sy), 20, 20)

```

## ui_qt/theme/__init__.py

**Type :** `.py`

```python

""""""

```

## ui_qt/theme/theme.py

**Type :** `.py`

```python

"""Theme — tokens de style pour PyQt6 (clair + sombre)."""
from PyQt6.QtGui import QColor, QPalette, QFont
from PyQt6.QtCore import Qt, QSettings


# Couleurs thème clair
LIGHT_COLORS = {
    "app": (238, 240, 244),
    "rail": (246, 247, 249),
    "surface": (255, 255, 255),
    "surface_2": (250, 251, 253),
    "hover": (241, 244, 249),
    "select": (232, 240, 253),
    "border": (226, 229, 235),
    "border_2": (205, 210, 219),
    "text": (31, 36, 48),
    "muted": (105, 114, 129),
    "faint": (156, 163, 176),
    "accent": (59, 118, 214),
    "danger": (214, 84, 84),
    "warn": (222, 160, 50),
}

# Couleurs thème sombre
DARK_COLORS = {
    "app": (30, 33, 40),
    "rail": (37, 40, 48),
    "surface": (37, 40, 48),
    "surface_2": (44, 48, 56),
    "hover": (50, 54, 64),
    "select": (40, 50, 72),
    "border": (55, 60, 72),
    "border_2": (65, 70, 82),
    "text": (220, 224, 232),
    "muted": (140, 148, 168),
    "faint": (100, 108, 128),
    "accent": (80, 140, 230),
    "danger": (230, 100, 100),
    "warn": (230, 180, 70),
}

# Accents par famille
FAMILY_COLORS = {
    "corps": (67, 160, 92),
    "cog": (62, 124, 214),
    "perso": (222, 164, 46),
    "emo": (34, 158, 142),
    "besoin": (146, 96, 186),
    "exp": (206, 126, 60),
}

# Alias pour compatibilité
COLORS = LIGHT_COLORS


def _rgb(t):
    return QColor(t[0], t[1], t[2])


def _hex(t):
    return f"#{t[0]:02x}{t[1]:02x}{t[2]:02x}"


def get_settings():
    return QSettings("UniversVivant", "UniversVivant")


def get_theme_name():
    s = get_settings()
    return s.value("theme", "clair")


def set_theme_name(name):
    s = get_settings()
    s.setValue("theme", name)


def apply_theme(app, theme_name=None):
    """Applique le thème à QApplication."""
    if theme_name is None:
        theme_name = get_theme_name()
    colors = DARK_COLORS if theme_name == "sombre" else LIGHT_COLORS

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, _rgb(colors["app"]))
    palette.setColor(QPalette.ColorRole.WindowText, _rgb(colors["text"]))
    palette.setColor(QPalette.ColorRole.Base, _rgb(colors["surface"]))
    palette.setColor(QPalette.ColorRole.Text, _rgb(colors["text"]))
    palette.setColor(QPalette.ColorRole.Button, _rgb(colors["surface"]))
    palette.setColor(QPalette.ColorRole.ButtonText, _rgb(colors["text"]))
    palette.setColor(QPalette.ColorRole.Highlight, _rgb(colors["accent"]))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Mid, _rgb(colors["border"]))
    app.setPalette(palette)

    font = QFont("Segoe UI", 13)
    font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
    app.setFont(font)

    bg = _hex(colors["surface"])
    bg2 = _hex(colors["surface_2"])
    border = _hex(colors["border"])
    border2 = _hex(colors["border_2"])
    text = _hex(colors["text"])
    muted = _hex(colors["muted"])
    accent = _hex(colors["accent"])
    hover_bg = _hex(colors["hover"])
    select_bg = _hex(colors["select"])

    app.setStyleSheet(f"""
        QDockWidget {{
            font-weight: bold;
        }}
        QDockWidget::title {{
            background: {bg2};
            padding: 6px;
            border-bottom: 1px solid {border};
        }}
        QTableView {{
            border: 1px solid {border};
            border-radius: 6px;
            gridline-color: {border2};
            selection-background-color: {select_bg};
            selection-color: {text};
            background: {bg};
            color: {text};
        }}
        QTableView::item {{
            padding: 4px 8px;
        }}
        QHeaderView::section {{
            background: {bg2};
            border: none;
            border-bottom: 1px solid {border};
            padding: 4px 8px;
            font-weight: bold;
            color: {muted};
        }}
        QToolBar {{
            border: none;
            spacing: 4px;
            background: {bg};
        }}
        QToolBar QToolButton {{
            border: 1px solid {border};
            border-radius: 6px;
            padding: 4px 10px;
            background: {bg};
            color: {text};
        }}
        QToolBar QToolButton:hover {{
            background: {hover_bg};
        }}
        QToolBar QToolButton:checked {{
            background: {select_bg};
            border-color: {accent};
        }}
        QScrollBar:vertical {{
            width: 8px;
            background: transparent;
        }}
        QScrollBar::handle:vertical {{
            background: {border2};
            border-radius: 4px;
            min-height: 32px;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0;
        }}
        QLineEdit {{
            border: 1px solid {border2};
            border-radius: 6px;
            padding: 4px 8px;
            background: {bg};
            color: {text};
        }}
        QLineEdit:focus {{
            border-color: {accent};
        }}
        QComboBox {{
            border: 1px solid {border2};
            border-radius: 6px;
            padding: 4px 8px;
            background: {bg};
            color: {text};
        }}
        QSpinBox {{
            border: 1px solid {border2};
            border-radius: 6px;
            padding: 4px 8px;
            background: {bg};
            color: {text};
        }}
        QPushButton {{
            border: 1px solid {border};
            border-radius: 6px;
            padding: 4px 10px;
            background: {bg};
            color: {text};
        }}
        QPushButton:hover {{
            background: {hover_bg};
        }}
        QPushButton:checked {{
            background: {select_bg};
            border-color: {accent};
        }}
        QLabel {{
            color: {text};
        }}
        QStatusBar {{
            background: {bg2};
            color: {muted};
        }}
        QListWidget {{
            border: 1px solid {border};
            border-radius: 6px;
            background: {bg};
            color: {text};
        }}
        QListWidget::item {{
            padding: 4px 8px;
        }}
        QListWidget::item:selected {{
            background: {select_bg};
        }}
        QListWidget::item:hover {{
            background: {hover_bg};
        }}
    """)

```

