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
    name = agent_snapshot.get("name", "Cet habitant")
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
    health = agent_snapshot.get("health", 0)
    return f"Sante : {int(health*100)}% -- {level_label(health).lower()}"


def describe_hunger(agent_snapshot):
    hunger = (agent_snapshot.get("needs_named", {}) or {}).get("faim", 0)
    return f"Faim : {int(hunger*100)}% -- {level_label(hunger).lower()}"


def describe_needs(agent_snapshot):
    """Return a list of need descriptions."""
    needs = agent_snapshot.get("needs_named", {}) or {}
    result = []
    for key, label in [("health", "Sante"), ("faim", "Faim"),
                       ("énergie", "Energie")]:
        val = needs.get(key, agent_snapshot.get(key, 0))
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
