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
