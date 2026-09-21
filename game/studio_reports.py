"""Résumé d'expérience en français simple. Pas de Qt/Pygame."""


def build_report(result):
    """Build a human-readable report from experiment results.

    result dict should contain:
    - population_start, population_end
    - births, deaths
    - builds (construction completions)
    - harvests
    - food_given
    - messages
    - institutions
    - mean_health, mean_hunger, mean_trust
    - scenario, seed, duration
    - events (list of event dicts)
    """
    lines = []

    scenario = result.get("scenario", "Standard")
    seed = result.get("seed", "?")
    duration = result.get("duration", 0)
    lines.append(f"Simulation : {scenario} (seed {seed}, {duration} ticks)")
    lines.append("")

    pop_start = result.get("population_start", 0)
    pop_end = result.get("population_end", 0)
    lines.append(f"La simulation a commencé avec {pop_start} habitant(s).")
    lines.append(f"Elle se termine avec {pop_end} habitant(s).")
    lines.append("")

    births = result.get("births", 0)
    deaths = result.get("deaths", 0)
    if births or deaths:
        lines.append(f"{births} naissance(s) et {deaths} mort(s) ont été enregistrées.")

    builds = result.get("builds", 0)
    if builds:
        lines.append(f"{builds} construction(s) ont été terminée(s).")

    harvests = result.get("harvests", 0)
    if harvests:
        lines.append(f"{harvests} récolte(s) ont été effectuées.")

    messages = result.get("messages", 0)
    if messages:
        lines.append(f"{messages} message(s) ont été échangés.")

    institutions = result.get("institutions", 0)
    if institutions:
        lines.append(f"{institutions} institution(s) se sont formées.")

    lines.append("")

    mh = result.get("mean_health")
    if mh is not None:
        if mh > 0.7:
            lines.append("La santé moyenne du groupe était bonne.")
        elif mh > 0.4:
            lines.append("La santé moyenne du groupe était correcte.")
        else:
            lines.append("La santé moyenne du groupe était préoccupante.")

    mt = result.get("mean_trust")
    if mt is not None:
        if mt > 0.7:
            lines.append("La confiance entre habitants était élevée.")
        elif mt > 0.4:
            lines.append("La confiance entre habitants était moyenne.")
        else:
            lines.append("La confiance entre habitants était faible.")

    return "\n".join(lines)


def build_short_summary(result):
    """Build a very short 1-2 sentence summary."""
    pop_start = result.get("population_start", 0)
    pop_end = result.get("population_end", 0)
    deaths = result.get("deaths", 0)
    builds = result.get("builds", 0)

    parts = [f"Le groupe de {pop_start} habitant(s) termine avec {pop_end} survivant(s)."]
    if deaths:
        parts.append(f"{deaths} mort(s).")
    if builds:
        parts.append(f"{builds} construction(s).")
    return " ".join(parts)


def interpret_metric(name, start, end):
    """Interpret a metric change in simple French."""
    diff = end - start
    if name == "trust":
        if diff > 0.10:
            return "La confiance du groupe a augmenté sensiblement."
        if diff < -0.10:
            return "La confiance du groupe a diminué sensiblement."
        return "La confiance du groupe est restée relativement stable."
    if name == "health":
        if diff > 0.10:
            return "La santé du groupe s'est améliorée."
        if diff < -0.10:
            return "La santé du groupe s'est dégradée."
        return "La santé du groupe est restée stable."
    if name == "hunger":
        if diff > 0.10:
            return "La faim a augmenté dans le groupe."
        if diff < -0.10:
            return "La faim a diminué dans le groupe."
        return "La faim est restée stable."
    return ""
