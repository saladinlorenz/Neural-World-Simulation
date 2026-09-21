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
