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


# ══════════════════════════════════════════════════════════════════════
#  Lot F.1 — paramètres Studio actifs (runtime Sim)
# ══════════════════════════════════════════════════════════════════════

#: Valeurs par défaut du dict ``Sim.runtime``.
DEFAULT_RUNTIME = {
    "max_population": 800,
    "regrowth_scale": 1.0,
    "fire_spread_scale": 1.0,
    "trauma_scale": 1.0,
    "trauma_enabled": True,
    "culture_enabled": True,
    "institutions_enabled": True,
    "births_enabled": True,
    "predators_enabled": True,
    "birth_rate": 0.01,
    "episodes_max": 50,
    "food_level": "normal",
    "predators_level": "normal",
    "max_agents_rendered": 200,
    "snapshot_frequency": 5,
}

#: Table explicite paramètre → cible ("sim" = attribut, "runtime" = dict).
#: Les clés de choix (anima.trauma / anima.culture) sont dérivées via
#: RuntimeConfig dans apply_parameters.
PARAMETER_TARGETS = {
    "simulation.speed": ("sim", "speed"),
    "population.max": ("runtime", "max_population"),
    "population.birth_rate": ("runtime", "birth_rate"),
    "ecology.regrowth": ("runtime", "regrowth_scale"),
    "ecology.fire_spread": ("runtime", "fire_spread_scale"),
    "anima.episodes_max": ("runtime", "episodes_max"),
    "performance.max_agents": ("runtime", "max_agents_rendered"),
    "performance.snapshot_freq": ("runtime", "snapshot_frequency"),
    "world.food": ("runtime", "food_level"),
    "world.predators": ("runtime", "predators_level"),
}


def apply_parameters(sim, store):
    """Applique le store validé au Sim : attributs + dict runtime.

    C'est le seul point de passage entre le dock Paramètres (ou un
    scénario) et la simulation en cours d'exécution.
    """
    values = store.to_dict()
    if getattr(sim, "runtime", None) is None:
        sim.runtime = dict(DEFAULT_RUNTIME)

    for key, value in values.items():
        target = PARAMETER_TARGETS.get(key)
        if target is None:
            continue
        scope, attr = target
        if scope == "sim":
            setattr(sim, attr, value)
        else:
            sim.runtime[attr] = value

    # Choix traduits en bool/float par RuntimeConfig.
    runtime_cfg = store.get_runtime()
    sim.runtime["trauma_enabled"] = runtime_cfg.trauma_enabled
    sim.runtime["trauma_scale"] = runtime_cfg.trauma_scale
    sim.runtime["culture_enabled"] = runtime_cfg.culture_enabled
    sim.runtime["snapshot_frequency"] = runtime_cfg.snapshot_freq
    sim.runtime["max_agents_rendered"] = runtime_cfg.max_agents_rendered

    sim.parameters = values
    sim.parameter_store = store
    return values
