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
