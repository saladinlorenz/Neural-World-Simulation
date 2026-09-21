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
