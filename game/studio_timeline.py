"""Chronologie normalisée avec catégories et filtres. Pas de Qt/Pygame."""
import re

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

#: Modèles structurés : uniquement quand ``kind`` ET (si besoin) ``actor_name``
#: sont renseignés — les tuples du journal moteur n'ont ni l'un ni l'autre.
_KIND_SENTENCES = {
    "monster_attack": "{actor} a subi une attaque d'animal dangereux.",
    "food_given": "{actor} a partagé de la nourriture.",
    "construction_complete": "{actor} a participé à une construction terminée.",
    "birth": "Un enfant est né dans le groupe de {actor}.",
    "death": "{actor} n'a pas survécu.",
    "harvest": "{actor} a récolté des ressources.",
    "build": "{actor} a commencé une construction.",
    "exploration": "{actor} a exploré une nouvelle zone.",
    "conflict": "{actor} a été impliqué dans un conflit.",
    "message": "{actor} a partagé une information.",
    "fire": "Un feu s'est déclaré près de {actor}.",
    "weather": "La météo a changé.",
    "culture": "{actor} a transmis un savoir culturel.",
    "institution": "Une institution a été créée ou modifiée.",
}


def category_label(category, default=""):
    """Libellé d'affichage d'un id du registre (libellé, sinon id brut)."""
    meta = JOURNAL_CATEGORIES.get(str(category or ""))
    if not meta:
        return str(category or default)
    return str(meta.get("label") or category or default)


def normalize_event(raw):
    """Normalize a raw event dict into a standard format.

    Sans ``kind`` explicite (entrées du journal moteur), la catégorie est
    conservée telle quelle plutôt que d'être forcée à « life ». Le ``count``
    du journal (agrégation des doublons) est conservé tel quel.
    """
    kind = str(raw.get("kind", ""))
    return {
        "tick": int(raw.get("tick", 0)),
        "category": CATEGORY_MAP.get(kind, raw.get("category") or "life"),
        "title": str(raw.get("title") or raw.get("text") or kind or "Événement"),
        "text": str(raw.get("text", "")),
        "actors": [int(x) for x in raw.get("actors", []) if str(x).isdigit()],
        "place": raw.get("place"),
        "importance": float(raw.get("importance") or 0.0),
        "kind": kind,
        "actor_name": str(raw.get("actor_name", "")),
        "count": max(1, int(raw.get("count") or 1)),
    }


def _finish(sentence):
    """Ponctuation finale : une phrase ne se termine jamais sans point."""
    s = str(sentence).strip()
    if s and s[-1] not in ".!?…»":
        s += "."
    return s


def _sentence_termine(text):
    """« small_house termine : depot cree. » → « Construction small_house terminée : depot cree. »"""
    t = str(text).strip()
    m = re.match(r"^([A-Za-z_]\w*)\s+termine\s*:\s*(.*)$", t)
    if m:
        rest = str(m.group(2)).strip().rstrip(".")
        base = f"Construction {m.group(1)} terminée"
        return f"{base} : {rest}" if rest else f"{base}."
    m = re.match(r"^(Coffre|Puits|Atelier)\s+termine\.?$", t)
    if m:
        return f"Construction terminée : {m.group(1)}."
    return t


#: Motifs réellement écrits par ``Simulation.log`` (lu dans simulation.py) :
#: (regex, transformateur) — le texte brut est déjà une phrase, on le garde.
_TEXT_RULES = (
    # 1. Décès : « Luna (adulte, 12.4 ans) est mort de faim, gén 3, 12 neurones. »
    (re.compile(r"^[A-ZÀ-Ý][\w'’.-]*(?:\s+[A-ZÀ-Ý][\w'’.-]*)*\s+\([^)]*\)\s+est mort\b"),
     lambda t: t),
    # 2. Naissance : « Ava et Bob ont un enfant : Tom ! »
    (re.compile(r"\bont un enfant\s*:"), lambda t: t),
    # 3. Union / refus : « … se sont mariés ! », « … sont liés. », « … refuse la proposition de … »
    (re.compile(r"\bse sont mariés\b|\bsont liés\b|\brefuse la proposition\b"), lambda t: t),
    # 4. Météo / monde : « La foudre a allumé un feu. »
    (re.compile(r"^(?:La foudre|La pluie|Il pleut|Un orage|La sécheresse|La neige|Monde )"),
     lambda t: t),
    # 5. Social / conflit : « X trahi par Y : … », « X parle à Y : … », « X a frappé un enfant ! »
    (re.compile(r"\btrahi par\b|\bparle à\b|\ba frappé\b|s'entredéchirent|\bpleure\b"),
     lambda t: t),
    # 6. Accord manquant du moteur : « X a commence … » → « X a commencé … »
    (re.compile(r"\ba commence\b"), lambda t: t.replace(" a commence ", " a commencé ")),
    # 7. Accord manquant : « X a plante une graine. » → « X a planté une graine. »
    (re.compile(r"\ba plante\b"), lambda t: t.replace(" a plante ", " a planté ")),
    # 8. Chantier fini : « Coffre termine. » / « small_house termine : depot cree. »
    (re.compile(r"^[A-Za-z_]\w*\s+termine\b|^(?:Coffre|Puits|Atelier)\s+termine\b"),
     _sentence_termine),
)


def _sentence_from_text(text):
    """Phrase issue du texte brut, ou ``None`` si aucun motif ne matche."""
    t = str(text or "").strip()
    if not t:
        return None
    for pattern, transform in _TEXT_RULES:
        if pattern.search(t):
            return _finish(transform(t))
    return None


def event_sentence(event):
    """Turn a normalized event into a readable French sentence.

    Priorité : ``kind``/``actor_name`` (modèles structurés) → motifs réels du
    journal moteur → repli « Libellé catégorie — texte ». Jamais de
    « Un habitant : » quand le texte porte déjà un nom.
    """
    kind = str(event.get("kind") or "")
    actor = str(event.get("actor_name") or "").strip()
    text = str(event.get("text") or "").strip()
    count = max(1, int(event.get("count") or 1))
    template = _KIND_SENTENCES.get(kind)

    sentence = None

    # 1) kind + acteur explicites : modèles structurés existants.
    if template is not None and ("{actor}" not in template or actor):
        sentence = template.format(actor=actor)

    # 2) Motifs écrits par le moteur (décès, naissance, chantier, météo…).
    if sentence is None:
        sentence = _sentence_from_text(text)

    # 3) Repli : libellé de catégorie — texte.
    if sentence is None:
        if text:
            sentence = f"{category_label(event.get('category'), 'Événement')} — {text}"
        elif template is not None:
            sentence = template.format(actor=actor or "Un habitant")
        else:
            sentence = "Un événement important s'est produit."

    sentence = _finish(sentence)
    if count > 1:
        sentence = f"{sentence} (×{count})"
    return sentence


def format_event(event):
    """Format an event for display: tick, category, sentence."""
    tick = event.get("tick", 0)
    category = event.get("category", "life")
    sentence = event_sentence(event)
    day = tick // 100 + 1
    hour = tick % 100
    return f"Jour {day} — {hour:02d}h — [{category}] {sentence}"


def filter_events(events, category=None, actor=None, place=None,
                  min_tick=None, max_tick=None):
    """Filter events by criteria (catégorie, acteur, lieu, fourchette de ticks).

    ``importance`` n'est pas pris en charge ici : filtrage côté client.
    """
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
