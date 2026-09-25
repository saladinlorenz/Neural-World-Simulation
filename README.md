# 🧠🌍 Neural World Simulation

### An open-ended artificial-life laboratory for building, observing, and experimenting with autonomous neural societies.

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/UI-PyQt6_Studio-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![NumPy](https://img.shields.io/badge/engine-NumPy_%2B_PIL-orange.svg)](https://numpy.org/)
[![Reinforcement Learning](https://img.shields.io/badge/learning-REINFORCE_%2B_Elman_RNN-purple.svg)](#-decision-and-learning)
[![License Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-lightgrey.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#-contributing)

![Living world — procedural terrain, inhabitants, ecology and resources on a 1000×1000 map](docs/img/hero.png)

> **No scripted quests. No assigned professions. No omniscient agents.**
>
> Neural World Simulation is a persistent artificial-life environment in which inhabitants perceive only a partial world, form memories from lived experience, choose among feasible possibilities, learn from consequences, build material and social structures, and leave a history behind.
>
> The project is built for people who want to explore a difficult question: **what kinds of individual and collective behavior emerge when learning agents must survive, remember, cooperate, compete, build, communicate, and adapt inside a world that does not assign them a script?**

---

## Why contribute?

Most agent simulations choose one of two paths:

- a compact benchmark with a narrow task and a clear reward;
- a game-like simulation with many visible systems but mostly scripted agents.

**Neural World Simulation aims at the space between them.** It is a long-running, inspectable world where learning agents are constrained by bodies, resources, geography, local information, social relationships, and physical consequences.

This repository is an opportunity to contribute to a project that combines:

```text
Artificial life
+ multi-agent learning
+ procedural ecology
+ social simulation
+ neural decision-making
+ explainability
+ experimental tooling
+ a real desktop laboratory interface
```

It is not a finished product pretending to be complete. It is an active research-engineering project with meaningful open problems in performance, learning, memory, social emergence, ecology, visualization, testing, reproducibility, and human-readable diagnostics.

If you enjoy asking “what happens if we make this rule real?” rather than only “can we make this feature look good?”, this project is for you.

---

## What is Neural World Simulation?

Neural World Simulation is a Python-based artificial-life and multi-agent simulation platform.

A simulation run contains:

- a persistent 1,000 × 1,000 tile procedural world;
- a configurable population of neural inhabitants, sheep, predators, resources, structures, and environmental processes;
- agents with bodies, needs, emotions, personality, memory, skills, inventory, social relationships, and recurrent neural brains;
- a world engine that validates every action against terrain, distance, affordances, tools, inventory, danger, and other physical constraints;
- a PyQt6 Studio that makes the world observable, editable, repeatable, comparable, and exportable.

A run can start with a tiny population for close behavioral debugging, a standard population for observation, a large population for scaling experiments, or an empty world for controlled world-building.

```bash
# Minimal behavior inspection
python mainqt.py --agents 2 --sheep 2 --seed 7

# Standard living-world run
python mainqt.py --agents 60 --sheep 40 --seed 7

# Larger experiment; practical limits depend on enabled systems and hardware
python mainqt.py --agents 300 --sheep 120 --seed 7

# Empty world for manual setup and controlled experiments
python mainqt.py --blank 1
```

The population is not fixed. Screenshot commands may use a chosen population for demonstration, but the simulation itself is configurable.

---

## Autonomous inhabitants

### Freedom is not randomness

The inhabitants are designed to have **situated decision freedom**.

They are not assigned a role such as farmer, builder, guard, explorer, or healer. They do not receive a mandatory quest. They are not told what narrative to enact.

Instead, each inhabitant has a current situation:

```text
Body state
+ hunger / thirst / fatigue / safety
+ emotions and personality
+ local perception
+ remembered places
+ social relations
+ inventory and tools
+ active intentions
+ terrain and physical constraints
```

From that situation, it can select among coherent possibilities.

A hungry inhabitant might:

- eat food that is already available;
- move toward a remembered food source;
- harvest a nearby resource;
- follow a trusted inhabitant;
- return to storage or a shelter;
- share, request, take, avoid danger, flee, or explore;
- make a different choice because its personality, fear, curiosity, social state, memory, or learned experience differs.

The important point is that the simulation should not decide the result in advance. It offers a world of possibilities; each inhabitant chooses a feasible path through that world.

### The engine contract

```text
Limited perception + memory + needs + emotion + personality + relations
                                  ↓
                           neural proposal
                                  ↓
                   candidate / intention / target selection
                                  ↓
              world checks physical and social feasibility
                                  ↓
          real consequence in world, body, inventory and relations
                                  ↓
                 experience, reward, memory and future learning
```

The neural brain can propose. The world decides whether the action can happen.

This protects the simulation from fake intelligence:

- an inhabitant cannot eat absent food;
- it cannot harvest through an obstacle;
- it cannot build without materials;
- it cannot reach a place it does not know or cannot physically access;
- it cannot receive a social benefit from an interaction that did not occur;
- the UI cannot invent a state that is not present in the engine.

---

## Decision and learning

Each inhabitant owns an **Elman recurrent neural network** with a persistent internal context state. Brain topology is fixed at birth; learning modifies parameters throughout life.

| Component | Current implementation direction |
|---|---|
| Perception vector | 132 structured inputs |
| Primitive actions | 15 world-validated actions |
| Strategic heads | 6 higher-level strategy choices |
| Target heads | 8 target categories |
| Learning | Online REINFORCE with short eligibility traces |
| Individuality | Personality, body, cognition, social history, habits, skills, memory, neural state |
| Explainability | Action ranking, strategy, target, goals, state, memories and diagnostics exposed to the Studio |

### Current primitive action vocabulary

```text
Rest · Sleep · Eat · Drink · Harvest · Drop · Build · Give · Take
Attack · Flee · Explore · Talk · Mark · Social
```

These primitives are intentionally small. They are the building blocks of larger life patterns.

For example, a meaningful food expedition is not a magical `GET_FOOD` command:

```text
Remember a resource
→ travel through the world
→ verify the resource exists
→ harvest or pick up
→ eat if urgent
→ otherwise return toward shelter, storage, or group
→ update memory from the outcome
```

This is one of the central contributor opportunities: turn existing primitives into robust, inspectable composed activities without replacing the world’s physical constraints.

---

## The inhabitants as complete simulation entities

Each `Being` combines several layers that are usually separate in smaller simulations.

### Body and survival

- health, pain, temperature, age, life stage, natural death limits;
- hunger, energy, thirst, sleep, safety, belonging, esteem;
- strength, endurance, mobility, senses, recovery;
- inventory, carrying capacity, tools, tool durability, resource costs;
- shelter bonus, weather effects, starvation, thirst, fatigue, rest and sleep recovery.

### Mind and individuality

- recurrent neural state and online learning;
- cognition traits: memory, anticipation, imagination, attention;
- personality traits: sociability, aggression, curiosity, caution, patience, empathy, impulsivity, trust, persistence, ambition, generosity, discipline;
- emotions: fear, joy, anger, sadness, stress, surprise, disgust, affection;
- habits, skills, identity, values, trauma, episodic memory, life history, self-esteem, reputation and causal traces.

### Social life

- parents, children, partner, family and clan membership;
- trust, affinity, hostility, generosity, theft, violence and social memory;
- following, talking, giving, taking, mourning, marking and social interaction;
- clan knowledge and verified universal knowledge;
- cultural claims and repeated practices that can form institutions;
- shared storage and material cooperation.

The ambition is not to claim human-level minds. The ambition is to make social and individual behavior structurally richer than a finite-state NPC loop while remaining inspectable.

---

## A large world with local knowledge

The world is intentionally large:

```text
1,000 × 1,000 tiles
16,000 × 16,000 world pixels at 16 px per tile
```

This scale supports a design principle that is difficult to demonstrate in tiny arenas:

```text
The world can be large.
An individual’s knowledge remains local.
Exploration, memory, communication, routes, settlement, and regional resources matter.
```

### Terrain and climate

- procedural water, shorelines, marshes, grassland, forests, rock, snow and mountains;
- moisture and slope-aware biome distribution;
- editable terrain with water, land, walls, floors, carving and restoration;
- day/night cycle, seasons, temperature, rain, wind, storms and lightning;
- pheromones, exploration traces, regrowth, fire and smoke;
- terrain chunks and caches for responsive map rendering.

### Ecology and material pressure

- localized food/resource sites, forests, quarries, gold, tools and meat;
- sheep and predators;
- tool-gated harvesting, durability and carrying capacity;
- resource depletion and regrowth direction;
- spreading fire and flammable world contents;
- crops, water needs, storage, building sites, structures and graves.

### Why regional ecology matters

A useful world is not one where every tile has everything.

The project is moving toward regions and resource sites where a place can be strategically meaningful:

```text
Forest → wood, berries, mushrooms, cover, possible danger
Plain → settlement space, crops, routes, limited wild food
Water → drinking, fishing opportunities, travel constraint
Rock / mountain → stone, ore, difficult movement, scarce food
Shelter / storage → security, rest, collective material memory
```

This creates reasons for exploration, travel, knowledge sharing, conflict, exchange, construction, and settlement.

---

## 🔬 PyQt6 Studio: inspect, intervene, experiment

![PyQt6 Studio — live map, agent inspector, population docks, journal with export](docs/img/interface.png)

Neural World Simulation is also a desktop laboratory application. The Studio is designed to expose engine reality rather than hide it behind a game interface.

## Live map and world tools

- zoomable and tilting world view;
- terrain cache, chunk rendering, minimap, legend and camera follow;
- inhabitants, sheep, predators, resources, storage, crops, construction, graves and effects;
- day/night, rain, lightning, fire glow and social effects;
- tile inspection;
- terrain editing: water, land, walls, floors, blocks, carving, restoration, erase and asset placement;
- inhabitant, sheep and predator spawning;
- custom tool creation and asset selection;
- undo/redo for world edits.

## Population and inspection panels

### Population

- searchable and sortable population table;
- age-stage and living/dead filters;
- direct selection from the table or the map;
- creation and removal workflows.

### Inspector

The inspector is a diagnostic surface for a selected inhabitant. It can expose:

- identity, age, clan, family and relationships;
- body, cognition, personality, emotions and needs;
- health, hunger, thirst, energy, pain, sleep and safety state;
- skills, habits, inventory, equipped tool and durability;
- active goal, target, distance, duration, state and blocked information;
- personal memories, beliefs, known places and danger information;
- social relations, trust and affinity;
- identity, values, trauma, episodic memory, plans and reputation;
- neural size, decision frequency, action ranking, strategy and target data;
- evaluated action possibilities and activity data where available.

### Anima

The Anima view provides a higher-level view of each inhabitant’s lived state:

- dominant identity;
- values and motivations;
- trauma and danger beliefs;
- intentions and short plans;
- episodic/autobiographical memory;
- reputation and social state.

## Society, journal and timeline

### Society

- population and family indicators;
- social relations;
- storage, construction and institution state;
- collective practices and group-level information.

### Journal

- categorized engine events;
- filtering, text search and sorting;
- JSON, CSV and TXT export;
- readable world history without inventing facts.

### Timeline

- normalized events across life, family, social, danger, construction, economy, culture, weather and death;
- category and text filtering;
- time-oriented investigation of a simulation run.

## Laboratory panels

| Studio panel | Purpose |
|---|---|
| **Parameters** | Edit runtime population, world, simulation, Anima, ecology and performance parameters |
| **Scenarios** | Apply controlled presets such as calm, danger, famine, culture, trauma and social experiments |
| **Laboratory report** | Build readable summaries and metrics from a run |
| **Comparison** | Compare A/B experiment results, differences and interpretation |
| **Timeline** | Inspect event sequences and history |
| **Overlays** | Examine resources, danger, memory, relations, needs, Anima, culture, institutions and territories |
| **Exports** | Produce JSON, CSV, TXT and report-friendly data |

The laboratory is central to the project. A contributor should be able to ask:

```text
What did the inhabitant perceive?
What did it remember?
Which options were feasible?
Why did it choose this goal?
What happened physically?
What changed in its body, memory, relation, inventory or world?
Did the group benefit?
```

---

## Research potential

The simulation can support experiments rather than only screenshots.

| Question | Example experiment |
|---|---|
| Does memory improve survival? | Same seed and world, compare memory-enabled vs memory-constrained agents |
| Does social knowledge reduce redundant exploration? | Compare local-only runs with clan/social knowledge enabled |
| Does scarcity increase cooperation or conflict? | Adjust food and predator parameters; track gifts, thefts, attacks, storage and mortality |
| Does resource clustering affect settlement? | Compare localized resource sites against uniform resource distributions |
| Do traumatic events create long-term avoidance? | Run danger scenarios and inspect beliefs, routes, fear and memory overlays |
| Does learning improve behavior? | Compare active REINFORCE learning against frozen-brain controls |
| Does culture persist across generations? | Compare transmission and Academy settings over long runs |
| Which world constraints produce stable groups? | Vary shelter, storage, danger, terrain and resource arrangements |

The project does not claim that every result is automatically “emergent intelligence.” It is designed to make attribution possible:

```text
World rule
vs
feasibility condition
vs
memory
vs
social relation
vs
personality bias
vs
neural decision
vs
learning outcome
```

That distinction is important for credible artificial-life work.

---

## 🚀 Quickstart

```bash
git clone https://github.com/saladinlorenz/Neural-World-Simulation.git
cd Neural-World-Simulation
pip install -r requirements.txt
```

Run a small observation world:

```bash
python mainqt.py --agents 2 --sheep 2 --seed 7
```

Run a populated world:

```bash
python mainqt.py --agents 60 --sheep 40 --seed 7
```

Run an empty editable world:

```bash
python mainqt.py --blank 1
```

Set initial simulation speed:

```bash
python mainqt.py --agents 60 --sheep 40 --seed 7 --speed 4
```

### Headless screenshots

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

The headless screenshot command uses explicitly chosen demonstration values. It does not impose a fixed project population.

### Tests

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
│   PyQt6 application entry point.
│   Creates the world, seeds life, creates SimulationController and MainWindow.
│
├── game/
│   ├── engine.py
│   │   Procedural world creation, ecological placement and life seeding.
│   ├── simulation.py
│   │   Core living-world contract: sensing, feasibility, goals, movement,
│   │   actions, metabolism, rewards, social processes and world updates.
│   ├── brain.py / brainapi.py / brainschema.py
│   │   Elman RNN, REINFORCE, structured 132-input schema,
│   │   action/strategy/target heads and explanation support.
│   ├── entities.py
│   │   Being, Sheep, Monster, body/mind/social state and ClanKnowledge.
│   ├── world.py / worldgen.py / resourcesites.py
│   │   NumPy world layers, procedural terrain, fire, crops, storage,
│   │   construction state and localized ecological sites.
│   ├── actioncandidate.py
│   │   Candidate variants derived from perception and memory.
│   ├── affordancedefinitions.py / assetsmanager.py / assetsapi.py
│   │   Asset semantics, affordances, tools, resources and recipes.
│   ├── construction.py / storage.py / socialmemory.py
│   │   Buildings, material storage and social records.
│   ├── universalknowledge.py / academy.py
│   │   Verified shared knowledge and learned-brain/cultural support.
│   ├── lab.py / history.py
│   │   Event recording, experimental history and reporting data.
│   ├── mapapi.py / mapcache.py
│   │   Map transforms, terrain caches and chunk rendering support.
│   ├── save.py / invariants.py
│   │   Persistence and world consistency support.
│   └── simulationcontroller.py / uicommands.py / uistate.py / uisnapshots.py
│       Validated bridge between engine and Studio UI.
│
├── uiqt/
│   ├── mainwindow.py
│   │   Studio shell: toolbar, menus, docks, timers, status and theme.
│   ├── map/
│   │   Map view, terrain chunks, minimap, effects and overlay integration.
│   ├── docks/
│   │   Inspector, population, journal, society, tile, tools and assets panels.
│   ├── studio/
│   │   Parameters, scenarios, timeline, laboratory, reports, comparison,
│   │   export and overlays.
│   ├── dialogs/
│   │   Save/load, inhabitant creation and custom tool editor.
│   └── models/ / assetcache.py / qtimage.py
│       Qt data models, thumbnail/pixmap caches and image conversion.
│
├── assets/
│   Visual packs, terrain, sprites, portraits, tools and fallbacks.
├── tests/
│   Behavior, activity, assets, terrain, save/load, overlays, UI and soak tests.
├── tools/
│   Headless screenshot and documentation tooling.
└── docs/img/
    README images: hero.png and interface.png.
```

---

## Performance and scaling

The project deliberately keeps a large world and rich agent state. Performance work therefore focuses on removing repeated work rather than deleting systems.

Current foundations include:

- NumPy arrays for terrain and world layers;
- local resource indexing;
- entity spatial buckets;
- terrain image cache and 64 × 64 chunks;
- visible-region rendering;
- rendering budgets for broad map views;
- snapshot-driven Studio panels;
- bounded event and memory structures;
- headless execution for longer experiments.

High-impact contribution opportunities include:

- profiling the simulation, brain, perception, UI and render pipeline;
- improving cache invalidation;
- reducing duplicate snapshot/model refreshes;
- vectorizing safe hot paths;
- improving local spatial queries;
- preserving full information while adapting visual level of detail to zoom;
- designing reproducible long-run benchmarks.

The rule is simple:

```text
Do not make the simulation smaller to make it faster.
Make it stop doing the same work twice.
```

---

## Open contribution areas

### Agent autonomy and cognition

- verified spatial memory with confidence, decay, source provenance and local revalidation;
- regional exploration driven by need, familiarity, danger and curiosity;
- composed activities: food expeditions, return-to-shelter, transport, helping and supply behavior;
- stronger social knowledge transfer without omniscience;
- causal experiences connecting actions to outcomes;
- improved action-candidate generation and explainability;
- social attention, graph neural networks or carefully benchmarked alternatives.

### Ecology and world simulation

- richer regional resource distribution, depletion and regrowth;
- fishing, hunting and improved animal behavior;
- agriculture, production chains and material transformation;
- routes, settlements, migration and exchange;
- weather, climate and disaster experiments;
- new assets that include real affordances and physical consequences.

### Studio and visualization

- better decision, memory and causal overlays;
- readable experiment reports;
- population and social-network visualization;
- timeline investigation tools;
- stronger asset browser and map-editing workflows;
- accessibility, keyboard navigation and English UI coverage.

### Research infrastructure

- deterministic replay from seed and command/event log;
- Gymnasium-compatible environment wrapper;
- parameter sweeps and experiment orchestration;
- baseline comparisons: frozen learning, REINFORCE, PPO/actor-critic;
- result datasets, reproducible notebooks and benchmark scenarios;
- long-run reliability and performance profiling.

---

## Contributing

Contributors are welcome from artificial life, complex systems, multi-agent RL, simulation engineering, procedural generation, NumPy optimization, PyQt6, visualization, testing, pixel art, documentation, and scientific computing.

You do not need to understand every system before contributing. The repository contains opportunities at different levels:

| Contributor interest | Useful starting point |
|---|---|
| New to the project | Improve a label, help text, export sentence, scenario description or translation |
| Python / tests | Add a targeted regression test for an existing behavior |
| Procedural generation | Tune biome rules, resource-site placement or terrain readability |
| AI / ALife | Improve a bounded perception, memory, candidate or composed-activity mechanism |
| Performance | Profile a hot path, avoid duplicate work, improve cache invalidation |
| PyQt6 | Improve inspector readability, tables, filters, docking, keyboard navigation or report views |
| Artist / asset integrator | Add categorized assets, sprite mappings, visual states or fallbacks |
| Researcher | Add an experiment scenario, metric, comparison, report or reproducible benchmark |

### Contribution principles

1. Keep pull requests focused and reviewable.
2. Preserve the engine contract:

   ```text
   Brain proposes.
   World validates.
   Consequences are real.
   UI displays engine data.
   ```

3. Do not give agents information they could not physically perceive, remember, or receive.
4. Do not add global map scans or population-squared work to the per-tick path.
5. Reuse existing spatial indexes, world caches and UI snapshots before introducing new infrastructure.
6. Preserve save compatibility whenever practical.
7. Add a regression test for changed behavior whenever practical.
8. Do not remove a feature to improve performance; remove redundant computation instead.

### Good first issues

- Add a construction blueprint with real material requirements and an observable world consequence.
- Improve a biome/resource-site rule while preserving deterministic seeds.
- Add a truthful inspector field or readable timeline sentence.
- Add a test for an existing behavior chain.
- Improve a Studio export or laboratory interpretation sentence.
- Add an asset classification rule, fallback sprite or affordance definition.
- Improve a cache or refresh path without changing behavior.
- Translate a UI area or improve contributor documentation.

### Discuss first

Open an issue or discussion before major changes to:

- `brain.py`, `brainschema.py`, neural dimensions or learning algorithm;
- save format, migration or deterministic replay;
- global tick scheduling;
- spatial indexes and cache invalidation;
- core action feasibility/world validation;
- population/reproduction systems;
- systems that could accidentally create omniscient agents.

---

## Adding a capability correctly

A new label is not a new capability. A real capability needs a complete world contract:

```text
Target / asset
→ affordance
→ feasibility requirements
→ perception or memory path
→ candidate / intention
→ execution
→ real consequence
→ journal / diagnostic / test
```

For example, adding a harvestable plant should answer:

- How does an inhabitant physically perceive or remember it?
- Which tool, distance, energy, terrain or season constraints apply?
- What world object changes after harvesting?
- What enters inventory or affects needs?
- How can the attempt fail?
- Which event and diagnostic state should be observable afterward?

This is how contributors help the project grow without creating “fake actions” that appear in the UI but do not affect the simulation.

---

## Development status

The project already contains a substantial living-world foundation, Studio interface, diagnostics, save/load support, scenarios, exports, and regression coverage. It is still experimental and actively evolving.

A green test suite means a known contract has remained intact. It does not prove that every behavior is intelligent, scientifically validated, or fully optimized.

That honesty is intentional. The project welcomes contributors who want to help turn ambitious systems into measurable, reproducible, inspectable artificial-life experiments.

---

## Keywords

`artificial life` · `ALife` · `multi-agent systems` · `multi-agent reinforcement learning` · `MARL` · `emergent behavior` · `open-ended simulation` · `agent-based modeling` · `neuroevolution` · `Elman recurrent network` · `REINFORCE` · `procedural world generation` · `OpenSimplex` · `PyQt6` · `NumPy` · `digital ecology` · `computational sociology` · `cultural transmission` · `artificial society` · `simulation laboratory` · `neural agents` · `complex systems` · `colony simulation` · `procedural simulation`

---

## License

Apache-2.0 — see [LICENSE](LICENSE).

Asset packs in `assets/` retain their original licenses and attribution requirements. Consult bundled license files for CraftPix, Kenney, KayKit, Tiny Swords, and other included sources before redistribution.
