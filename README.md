# 🧠🌍 Neural World Simulation

### An open-ended artificial-life laboratory where autonomous inhabitants perceive, decide, remember, learn, build, cooperate, compete, and shape a persistent world.

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/UI-PyQt6_Studio-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![NumPy](https://img.shields.io/badge/engine-NumPy_%2B_PIL-orange.svg)](https://numpy.org/)
[![Reinforcement Learning](https://img.shields.io/badge/learning-REINFORCE_%2B_Elman_RNN-purple.svg)](#-decision-and-learning)
[![License Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-lightgrey.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#-contributing)

![Living world — procedural terrain, inhabitants, ecology and resources on a 1000×1000 map](docs/img/hero.png)

> **No assigned jobs. No scripted quests. No omniscient inhabitants.**
>
> Neural World Simulation is a persistent artificial-life environment and laboratory application. The world may begin with a very small group, a large population, or an empty editable map. Each inhabitant has limited perception, individual memory, needs, emotions, personality, relations, an inventory, and a learning recurrent neural brain. It is free to choose among coherent possibilities, but the world validates every attempt against physical reality.
>
> The simulation does not tell an inhabitant to become a farmer, builder, explorer, parent, fighter, or helper. These are possible life patterns that may become useful because of scarcity, danger, relationships, accumulated knowledge, local opportunities, and lived experience.

*🇫🇷 Une présentation française détaillée est disponible plus bas : [En français](#-en-français).* 

---

## Executive summary

**Neural World Simulation** is an open-ended multi-agent artificial-life project built in Python. It combines:

- a large, persistent 2D procedural world;
- autonomous inhabitants with bounded perception and individual neural decision systems;
- physical resources, survival pressure, ecology, construction, social relations, memory, culture, and history;
- a PyQt6 laboratory interface for observation, parameterization, experimentation, diagnostics, comparison, and export.

It is not designed as a conventional game with objectives imposed by a designer. It is designed as a **simulation instrument**: a contributor or researcher can create a controlled world, choose a seed and parameters, let inhabitants act, inspect why a decision occurred, compare scenarios, and export the resulting data.

Population is a runtime choice, not a fixed claim. A world can be launched with a handful of inhabitants for debugging and close observation, with dozens for everyday experiments, or with larger populations within the configured runtime limits and available machine performance.

---

## Autonomous decision freedom

The central design goal is not merely to give agents many named actions. It is to give them **decision freedom within a real world**.

An inhabitant is not restricted to a fixed script such as:

```text
worker → harvest
builder → build
guard → attack
```

Instead, the inhabitant receives local facts and possibilities:

```text
I am hungry.
I am tired.
A predator is close.
I remember water in another area.
A relative is nearby.
I have wood in my inventory.
A shelter is known.
A resource can be harvested.
A friend appears injured.
A region is unfamiliar.
```

From this state, it can select a coherent response. For example, faced with hunger and danger, different inhabitants may:

- flee first and search for food later;
- eat immediately if food is available;
- follow a trusted inhabitant toward a remembered resource;
- seek shelter because energy is too low;
- ask, give, take, cooperate, or compete depending on relations and personality;
- explore when no safe known option is available;
- return toward a known home, storage place, or group.

The system therefore aims for **situated autonomy**, not arbitrary randomness. Freedom is constrained by perception, memory, body, terrain, tools, danger, inventory, social context, and physical feasibility.

### The decision contract

```text
Local perception + memories + needs + emotions + personality + relations
                                ↓
                         neural proposal
                                ↓
                   feasible actions and targets
                                ↓
                     world validates reality
                                ↓
          consequence in body, inventory, world and relations
                                ↓
              experience, reward, memory and future learning
```

The brain can request an intention; it cannot create impossible outcomes. The world checks distance, target availability, terrain, obstruction, affordances, tools, energy, carrying capacity, inventory, social conditions, and danger before executing the consequence.

---

## Why this project matters

| Dimension | What the project provides |
|---|---|
| 🧠 **Individual agency** | Each inhabitant has its own recurrent neural brain, body, personality, emotions, needs, experiences, memories, habits, skills, social ties, and history. |
| 👁️ **Bounded knowledge** | Agents use nearby perception, personal memory, clan knowledge, and confirmed shared knowledge. They do not read the full world state. |
| ⚙️ **Validated action** | Neural intentions are proposals. The engine validates physical and social feasibility before any world consequence exists. |
| 🌾 **Meaningful pressure** | Hunger, thirst, fatigue, weather, shelter, resources, tools, inventory capacity, danger, and distance make choices meaningful. |
| 🏘️ **Emergent social life** | Families, clans, relations, gifts, grief, reputation, cultural facts, repeated practices, storage, construction, and institutions can develop in the same world. |
| 🗺️ **Large territory** | A 1,000 × 1,000-tile procedural world supports regions, exploration, local knowledge, resource distribution, settlement, and future migration. |
| 🔬 **Laboratory operation** | The PyQt6 Studio supports direct observation, controlled intervention, experiments, parameter tuning, scenario comparison, reporting, and export. |
| 🧪 **Inspectable behavior** | The project exposes decisions, goals, memories, needs, relations, inventory, events, timelines, overlays, and reports instead of treating agents as opaque entities. |

---

## World scale and population

The map is intentionally large:

```text
1,000 × 1,000 tiles
16,000 × 16,000 world pixels at 16 px/tile
```

This scale is not decorative. It allows inhabitants to have local knowledge, unknown regions, resource concentrations, routes, danger zones, settlement locations, and reasons to travel.

Population is configurable at launch and through the application workflow:

```bash
# Small observation/debugging run
python mainqt.py --agents 2 --sheep 2 --seed 7

# Standard living-world run
python mainqt.py --agents 60 --sheep 40 --seed 7

# Larger experiment, subject to configured limits and machine performance
python mainqt.py --agents 300 --sheep 120 --seed 7

# Empty editable world
python mainqt.py --blank 1
```

The engine has configurable upper limits for inhabitants, sheep, predators, rendering budgets, snapshots, and runtime parameters. The actual practical population depends on the enabled systems, visible UI panels, zoom level, resource density, neural decision frequency, and available CPU/RAM.

---

## The inhabitant model

Every inhabitant is represented by more than a neural network.

### Body and survival

- health, pain, body temperature, age and life stage;
- hunger, energy, thirst, sleep, safety, belonging and esteem;
- strength, endurance, mobility, senses and recovery;
- inventory, carrying capacity, tools and tool durability;
- shelter effects, starvation, thirst, fatigue and recovery.

### Mind and individuality

- recurrent neural state and online learned weights;
- cognition traits: memory, anticipation, imagination and attention;
- personality traits: sociability, aggression, curiosity, caution, patience, empathy, impulsivity, trust, persistence, ambition, generosity and discipline;
- emotional state: fear, joy, anger, sadness, stress, surprise, disgust and affection;
- habits, skills, identity, values, trauma, episodic memories and autobiographical events.

### Social existence

- family, parents, children, partner and group links;
- trust, affinity, hostility, generosity, theft, violence and reputation;
- clan membership and clan-level knowledge;
- social interactions: following, talking, giving, taking, socializing, mourning, marking and cooperation;
- cultural claims and emerging institutions tied to repeated practices.

---

## Decision and learning

### Neural architecture

Each inhabitant owns an **Elman recurrent neural network**. Its architecture is fixed at birth; the weights learn during life.

| Component | Current system |
|---|---|
| Sensory representation | 132 structured channels |
| Primitive actions | 15 world-validated actions |
| Strategy heads | 6 strategic tendencies |
| Target heads | 8 target categories |
| Learning method | Online REINFORCE with eligibility traces |
| Adaptation | Lived reward, age-modulated learning, habits, memory, emotions and personality |
| Explainability | Action probabilities, selected strategy/target, goals and diagnostics available to the Studio |

### Primitive actions

```text
Rest · Sleep · Eat · Drink · Harvest · Drop · Build · Give · Take
Attack · Flee · Explore · Talk · Mark · Social
```

These are deliberately primitive. A visible behavior such as “prepare an expedition,” “return to shelter,” “help a relative,” “supply a storage site,” or “found a settlement” should be built from multiple world-validated steps rather than a magical one-shot command.

### Perception and memory

The 132-input representation includes body state, needs, emotions, personality, cognition, habits, skills, local perception, social context, resource memory, time, weather, inventory, tools, spatial context, and Anima-related state.

A key rule is that an agent should use what it can legitimately know:

```text
Nearby perception
+ personally witnessed places
+ social/clan knowledge
+ verified shared facts
≠ global map omniscience
```

---

## The world

### Procedural terrain and climate

The procedural world includes:

- water, shorelines, marshes, grassland, forests, rock, snow and mountains;
- moisture and slope-aware biome placement;
- lakes, mountain chains, passability and editable terrain;
- day/night cycle, seasons, temperature, rain, wind, storms and lightning;
- fire, smoke, regrowth, pheromones and exploration traces;
- terrain chunks and caches for efficient rendering.

### Resources and ecology

- food, bushes, trees, stone, gold, tools, meat, water and shelter;
- localized food/resource sites and regrowth support;
- sheep populations and predators;
- tool-gated harvesting, durability and carrying limits;
- fires that propagate through flammable contents;
- crops, water needs, storage, resource depletion and recovery.

### Construction and material world

Inhabitants can interact with:

- construction sites and task-based blueprints;
- houses, chests, granaries, workshops, wells and related structures;
- shared storage, deposits and withdrawals;
- crops and agricultural plots;
- graves, mourned places, markers and territorial signals;
- user-placed assets and editable map layers.

---

## 🔬 The PyQt6 Laboratory Studio

![PyQt6 Studio — live map, agent inspector, population docks, journal with export](docs/img/interface.png)

The application is a laboratory interface, not only a viewer. It is built to make the backend observable and controllable.

## Live world view

- zoomable and tilting map;
- terrain rendering with cache and chunk support;
- minimap, legend, camera follow and selection;
- inhabitants, sheep, predators, resources, construction, storage, graves and effects;
- night, rain, lightning, fire glow and social effects;
- edit tools for terrain, water, land, walls, floors, blocks, carving, restoration, placement and deletion.

## Population panel

- sortable inhabitant table;
- name search;
- age-stage and alive/dead filters;
- selection and removal workflow;
- direct route to the selected inhabitant’s diagnostic state.

## Agent inspector

The inspector is intended to be a truthful diagnostic view of a selected inhabitant. It can expose:

- identity, age, family and clan;
- body, cognition, personality, emotions and needs;
- health, pain, energy, hunger, thirst and sleep;
- skills, habits, inventory, equipped tool and durability;
- current state, goal, target, distance, duration and blocked state;
- memory, beliefs, known places, relations, trust and affinity;
- identity, values, trauma, episodic memories, plans and reputation;
- neural size, decision frequency, action ranking, strategy and target information;
- current activity and evaluated possibilities when available.

## Journal and timeline

- categorized world events;
- filters and search;
- normalized timeline for life, family, social, danger, construction, economy, culture, weather and death;
- JSON, CSV and TXT export;
- readable event sentences for investigation and reporting.

## Society panel

- population and family state;
- relations and group-level information;
- storage, construction and institutions;
- clan-oriented knowledge and collective practices.

## Assets, tools and map editing

- searchable asset catalog;
- category filters and favorites;
- asset details: role, category, affordances, size and placement constraints;
- tool editor for custom tools;
- map painting, placement, erase, floor, wall, terrain carving and restoration;
- undo/redo for world edits.

## Studio laboratory panels

| Panel | Purpose |
|---|---|
| **Parameters** | Tune population, world, simulation, Anima, ecology and performance runtime parameters |
| **Scenarios** | Apply controlled presets such as calm, danger, famine, culture, trauma and social experiments |
| **Timeline** | Filter and inspect normalized events over simulated time |
| **Laboratory report** | Summarize population change, births, deaths, construction, harvests, health, hunger and trust |
| **Comparison** | Compare two experimental results across metrics and differences |
| **Overlays** | Inspect resources, danger, memory, relations, needs, Anima, culture, institutions and territories |
| **Exports** | Generate JSON, CSV, TXT and report-oriented outputs |

The Studio is designed so contributors can ask: **what happened, why did it happen, what did the agent know, what action was feasible, and what changed after it acted?**

---

## Research and experimentation

Neural World Simulation supports controlled experiments, not only visual observation.

Examples:

| Research question | Example procedure |
|---|---|
| Does memory improve survival? | Same seed, same population, compare memory-enabled and memory-constrained parameters |
| Does sharing knowledge reduce duplicated exploration? | Compare isolated inhabitants with social/clan transmission enabled |
| Does resource clustering alter settlement behavior? | Compare clustered resource sites against more uniform distributions |
| Does danger create avoidant culture? | Repeat danger scenarios and inspect memories, beliefs, routes and overlays |
| Does learning matter? | Compare active REINFORCE learning against frozen neural weights |
| Does scarcity change social behavior? | Track gifts, thefts, attacks, storage and mortality under different food levels |
| Which conditions produce stable groups? | Compare trust, family, shelter and resource configurations |

The project does not claim that every outcome is automatically “emergent intelligence.” It tries to expose enough state that contributors can separate:

```text
world rule
vs
physical feasibility
vs
memory
vs
social context
vs
personality
vs
neural proposal
vs
learned result
```

---

## 🚀 Quickstart

```bash
git clone https://github.com/saladinlorenz/Neural-World-Simulation.git
cd Neural-World-Simulation
pip install -r requirements.txt
```

Run a small world for close observation:

```bash
python mainqt.py --agents 2 --sheep 2 --seed 7
```

Run a standard populated world:

```bash
python mainqt.py --agents 60 --sheep 40 --seed 7
```

Run an empty editable world:

```bash
python mainqt.py --blank 1
```

Set initial speed:

```bash
python mainqt.py --agents 60 --sheep 40 --seed 7 --speed 4
```

### Headless capture

```bash
python tools/screenshot.py \
  --out docs/img/hero.png \
  --ticks 350 \
  --agents 140 \
  --sheep 60 \
  --monsters 6 \
  --zoom 1.3

python tools/screenshot.py \
  --out docs/img/interface.png \
  --window \
  --zoom 1.1
```

The screenshot command uses a chosen demonstration population; it does **not** define a fixed population for the project.

### Run tests

```bash
python -m pytest tests -x -q
```

```bash
python -m compileall game uiqt tests mainqt.py
```

---

## Architecture

```text
mainqt.py
│   PyQt6 entry point: world creation, life seeding, controller and Studio.
│
├── game/
│   ├── engine.py
│   │   Procedural world construction, resource placement, population seeding.
│   ├── simulation.py
│   │   Core world loop: sensing, feasible actions, goals, movement,
│   │   metabolism, execution, learning signals, social/ecological state.
│   ├── brain.py / brainapi.py / brainschema.py
│   │   Elman RNN, REINFORCE, 132 inputs, action/strategy/target heads.
│   ├── entities.py
│   │   Being, Sheep, Monster, personal state, social state, ClanKnowledge.
│   ├── world.py / worldgen.py / resourcesites.py
│   │   Grid layers, terrain, biomes, fire, crops, storage, ecological sites.
│   ├── actioncandidate.py
│   │   Contextual action variants from local perception and memory.
│   ├── affordancedefinitions.py / assetsmanager.py / assetsapi.py
│   │   Assets, physical affordances, recipes and semantic catalog.
│   ├── construction.py / storage.py / socialmemory.py
│   │   Buildings, material economy and social event records.
│   ├── universalknowledge.py / academy.py
│   │   Verified shared facts and learned-brain/cultural transmission support.
│   ├── lab.py / history.py
│   │   Event recording, world history and experiment-oriented information.
│   ├── mapapi.py / mapcache.py
│   │   Map abstractions, terrain cache and chunk rendering support.
│   ├── save.py / history.py / invariants.py
│   │   Persistence, history and consistency support.
│   └── uicommands.py / uistate.py / uisnapshots.py /
│       simulationcontroller.py
│       Validated UI bridge, snapshots, commands, undo/redo and controller.
│
├── uiqt/
│   ├── mainwindow.py
│   │   Studio shell, menus, toolbar, status, timers and docks.
│   ├── map/
│   │   MapView, terrain chunks, minimap, effects and overlay integration.
│   ├── docks/
│   │   Inspector, population, journal, society, assets, tools and tile views.
│   ├── studio/
│   │   Parameters, scenarios, timeline, laboratory, comparison and overlays.
│   ├── dialogs/
│   │   Save/load, inhabitant creation and tool editor.
│   └── models/ / assetcache.py / qtimage.py
│       Qt models, image conversion and cached visual assets.
│
├── assets/
│   Asset packs, sprites, portraits, terrain, tools and fallbacks.
├── tests/
│   Behavior, activity, terrain, save/load, overlay, UI and soak coverage.
├── tools/
│   Screenshot and project-documentation tooling.
└── docs/img/
    README images: hero.png and interface.png.
```

---

## Performance model

The project aims to preserve a large world and rich agents without representing every detail as a Python object at every frame.

Current design directions include:

- NumPy arrays for world layers;
- spatial resource indexing;
- entity spatial buckets;
- terrain cache and 64 × 64 chunks;
- visible-region rendering and agent render budgets;
- snapshot-driven UI panels;
- bounded histories and event streams;
- headless operation for long experiments.

Performance remains an important contributor area. Good optimizations preserve capabilities while removing duplicate work: unnecessary scans, duplicate candidates, repeated snapshots, hidden-dock refreshes, uncached terrain rebuilds, and excessive per-frame object construction.

---

## Roadmap

### Agent capabilities

- [ ] Verified spatial memory with confidence, decay and source provenance
- [ ] Regional exploration driven by needs, danger and familiarity
- [ ] Persistent composed activities: food expeditions, return-to-shelter, transport and helping behavior
- [ ] More social knowledge transfer and bounded cultural learning
- [ ] Causal experience traces linking actions, outcomes and later preferences
- [ ] Richer diagnostics for why an agent selected or rejected a possibility

### Ecology and society

- [ ] More structured resource regions, depletion and regrowth
- [ ] Fishing, hunting and richer animal behavior
- [ ] Expanded agriculture, transport and production chains
- [ ] Routes, migration, multi-settlement life and exchange
- [ ] Stronger climate/disaster scenarios

### Research and performance

- [ ] Profiling view for simulation, brain, perception, UI and rendering cost
- [ ] Vectorized tick paths and optional Numba experiments
- [ ] Gymnasium-compatible `NeuralWorldEnv` wrapper for SB3 / CleanRL
- [ ] Deterministic replay from seed plus command/event log
- [ ] Expanded parameter sweeps and experiment reports
- [ ] PPO / actor-critic benchmark against the current REINFORCE baseline

### Studio and community

- [ ] English/French localization improvements
- [ ] More explanation overlays and decision visualizations
- [ ] Browser observation/dashboard experiments
- [ ] Better contributor documentation for actions, assets, affordances and scenarios
- [ ] More visual assets and biome presentation work

---

## Contributing

Contributors are welcome from artificial life, complex systems, multi-agent RL, simulation engineering, procedural generation, NumPy performance, PyQt6, testing, visualization, pixel art, documentation, and translation.

### Workflow

```bash
# Fork the repository
# Create a branch: feat/my-feature or fix/my-bug
python -m pytest tests -x -q
# Open a focused pull request
```

### Contribution principles

1. Keep pull requests small and focused.
2. Preserve the engine contract: the brain proposes, the world validates, consequences are real, the UI displays real engine data.
3. Do not give inhabitants omniscient information.
4. Do not add global scans to per-tick logic.
5. Use existing spatial indexes and caches before creating another layer.
6. Add or update a regression test when behavior changes.
7. Keep simulation and UI concerns separated.
8. Do not remove features to gain performance; remove redundant work instead.

### Good first issues

| Area | Contribution ideas |
|---|---|
| Ecology | Tune a biome, add a small resource-site rule, improve regrowth behavior |
| Assets | Add a semantic asset mapping, improve sprite fallback or add an affordance |
| Construction | Add a blueprint with clear materials and world effects |
| Diagnostics | Improve truthful explanation, event wording, overlays or inspector display |
| Tests | Add a regression test for a behavior chain or save compatibility |
| Studio | Improve report wording, exports, parameter descriptions or scenario controls |
| Performance | Profile a hot path, improve cache invalidation, avoid duplicate UI refreshes |
| Translation | Translate a dock, help text, scenario or documentation section |

### Systems requiring discussion first

Please open an issue or discussion before large changes to:

- neural architecture, input schema or learning algorithm;
- save format and compatibility;
- global tick scheduling;
- spatial indexes and cache invalidation;
- action feasibility/world validation;
- deterministic behavior and replay;
- population/reproduction rules;
- changes that could give agents information they could not perceive or learn.

---

## Example: adding a real capability

A world interaction is complete only when all of these exist:

```text
Target or asset
→ semantic affordance
→ feasibility requirements
→ perception or memory path
→ candidate / intention
→ world execution
→ physical consequence
→ diagnostic / event / regression coverage
```

For example, adding a harvestable plant should answer:

- Can an agent physically perceive or remember it?
- Which terrain, distance, tool, energy or season constraints apply?
- Which world object changes after harvesting?
- What is added to inventory or changed in needs?
- How can the attempt fail?
- Which consequence should appear in the journal and inspector?

This approach protects the project from “fake actions”: labels that appear in the UI but have no real world consequence.

---

## 🇫🇷 En français

### Présentation

**Neural World Simulation** est un laboratoire de vie artificielle et de simulation multi-agents. Il propose un monde persistant dans lequel chaque habitant possède un corps, des besoins, des émotions, une personnalité, des souvenirs, des relations, un inventaire, des compétences et un cerveau neuronal récurrent qui apprend pendant sa vie.

Le projet n’impose pas de métiers tels que fermier, constructeur, explorateur ou gardien. Les habitants sont libres de choisir des possibilités cohérentes avec leur état et leur environnement : se reposer, chercher une ressource, fuir, explorer, construire, donner, suivre, parler, protéger un proche ou retourner vers un abri.

Cette liberté n’est pas une liberté magique. Chaque décision reste limitée par ce que l’habitant perçoit, ce qu’il a mémorisé, son énergie, ses besoins, les relations sociales, le terrain, les outils, l’inventaire et les règles physiques du monde.

### Contrat du moteur

```text
Perception locale + mémoire + besoins + émotions + personnalité
→ proposition du cerveau
→ vérification de faisabilité par le monde
→ conséquence réelle
→ expérience, mémoire et apprentissage
```

Le cerveau propose une intention. Le monde décide si l’action est réellement possible. Ainsi, aucun habitant ne peut récolter une ressource absente, traverser un obstacle sans capacité, construire sans matériaux ou connaître une région qu’il n’a jamais perçue ou apprise.

### Carte, population et liberté d’expérimentation

La carte fait **1 000 × 1 000 tuiles**. Elle peut être utilisée avec une petite population pour observer précisément les décisions, avec une population standard pour faire vivre un monde, ou avec une population plus grande selon les limites de runtime et les performances de la machine.

Le projet n’affirme pas qu’il contient toujours 140 habitants : ce nombre peut être utilisé pour une capture ou une démonstration. L’utilisateur choisit son scénario et sa population de départ.

### Studio laboratoire PyQt6

Le Studio sert à observer et expérimenter :

- carte avec zoom, inclinaison, mini-carte, suivi et effets ;
- liste de population et sélection d’habitants ;
- inspecteur : corps, cognition, personnalité, émotions, besoins, mémoire, relations, inventaire, outils, intentions et cerveau ;
- panneaux Anima, société, journal, chronologie et laboratoire ;
- overlays : ressources, danger, mémoire, relations, besoins, Anima, culture, institutions et territoires ;
- paramètres runtime, scénarios, comparaisons A/B, rapports et exports ;
- outils pour créer habitants, moutons, monstres, assets, outils et terrain ;
- pause, step, vitesse, sauvegarde, chargement, undo/redo.

### Contributions

Les contributions sont bienvenues pour la vie artificielle, le ML multi-agent, la performance NumPy, PyQt6, la génération procédurale, les tests, les assets, les visualisations, la documentation et la traduction.

La règle fondamentale à préserver est :

```text
Le cerveau propose.
Le monde vérifie.
Les conséquences sont réelles.
L’interface affiche les vraies données du moteur.
```

---

## Keywords

`artificial life` · `ALife` · `multi-agent systems` · `multi-agent reinforcement learning` · `MARL` · `emergent behavior` · `open-ended simulation` · `agent-based modeling` · `neuroevolution` · `Elman recurrent network` · `REINFORCE` · `procedural world generation` · `OpenSimplex` · `PyQt6` · `NumPy` · `digital ecology` · `computational sociology` · `cultural transmission` · `artificial society` · `simulation laboratory` · `neural agents` · `complex systems` · `colony simulation` · `procedural simulation`

---

## License

Apache-2.0 — see [LICENSE](LICENSE).

Asset packs under `assets/` retain their original authors’ licenses and attribution requirements. Consult the license files bundled with CraftPix, Kenney, KayKit, Tiny Swords, and other included asset sources before redistribution.
