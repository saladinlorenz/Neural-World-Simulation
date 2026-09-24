"""Chronologie normalisée avec catégories et filtres. Pas de Qt/Pygame."""
from .ui_registry import JOURNAL_CATEGORIES, ALL_CATEGORIES

#: Ids du registre partagé (journal + timeline), sentinelle « all » en tête.
CATEGORIES = [ALL_CATEGORIES] + list(JOURNAL_CATEGORIES)

CATEGORY_MAP = {
    "birth": "family",
    "death": "death",
    "marriage": "family",
    "child": "family",
    "attack": "danger",
    "monster_attack": "danger",
    "danger": "danger",
    "construction": "building",
    "build": "building",
    "construction_complete": "building",
    "harvest": "economy",
    "food_given": "economy",
    "trade": "economy",
    "message": "social",
    "conflict": "social",
    "exploration": "life",
    "weather": "weather",
    "fire": "danger",
    "culture": "culture",
    "institution": "culture",
}


def normalize_event(raw):
    """Normalize a raw event dict into a standard format.

    Sans ``kind`` explicite (entrées du journal moteur), la catégorie est
    conservée telle quelle plutôt que d'être forcée à « life ».
    """
    kind = str(raw.get("kind", ""))
    return {
        "tick": int(raw.get("tick", 0)),
        "category": CATEGORY_MAP.get(kind, raw.get("category") or "life"),
        "title": str(raw.get("title") or raw.get("text") or kind or "Événement"),
        "text": str(raw.get("text", "")),
        "actors": [int(x) for x in raw.get("actors", []) if str(x).isdigit()],
        "place": raw.get("place"),
        "importance": float(raw.get("importance", 0.0)),
        "kind": kind,
        "actor_name": str(raw.get("actor_name", "")),
    }


def event_sentence(event):
    """Turn a normalized event into a readable French sentence."""
    kind = event.get("kind", "")
    actor = event.get("actor_name") or "Un habitant"

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
    category = event.get("category", "life")
    sentence = event_sentence(event)
    day = tick // 100 + 1
    hour = tick % 100
    return f"Jour {day} — {hour:02d}h — [{category}] {sentence}"


def filter_events(events, category=None, actor=None, place=None, min_tick=None, max_tick=None):
    """Filter events by criteria."""
    result = events
    if category and category != ALL_CATEGORIES:
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
