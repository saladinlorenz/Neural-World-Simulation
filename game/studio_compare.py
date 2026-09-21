"""Comparaison A/B entre deux simulations. Pas de Qt/Pygame."""


KEYS = [
    ("population_end", "Population finale"),
    ("deaths", "Morts"),
    ("births", "Naissances"),
    ("builds", "Constructions"),
    ("harvests", "Récoltes"),
    ("messages", "Messages"),
    ("mean_health", "Santé moyenne"),
    ("mean_hunger", "Faim moyenne"),
    ("mean_trust", "Confiance moyenne"),
]


def compare_results(a, b):
    """Compare two experiment result dicts. Returns list of row dicts."""
    rows = []
    for key, label in KEYS:
        av = float(a.get(key, 0))
        bv = float(b.get(key, 0))
        rows.append({
            "metric": key,
            "label": label,
            "a": av,
            "b": bv,
            "difference": bv - av,
        })
    return rows


def compare_summary(a, b):
    """Generate a human-readable comparison summary in French."""
    a_label = a.get("scenario", "Expérience A")
    b_label = b.get("scenario", "Expérience B")
    
    lines = [f"Comparaison : {a_label} vs {b_label}", ""]
    
    rows = compare_results(a, b)
    for row in rows:
        label = row["label"]
        av = row["a"]
        bv = row["b"]
        diff = row["difference"]
        
        if abs(diff) < 0.01:
            continue
        
        direction = "augmenté" if diff > 0 else "diminué"
        
        if row["metric"] == "mean_health":
            if diff > 0.1:
                lines.append(f"La santé moyenne a {direction} ({av:.0%} → {bv:.0%}).")
            elif diff < -0.1:
                lines.append(f"La santé moyenne a {direction} ({av:.0%} → {bv:.0%}).")
        elif row["metric"] == "mean_trust":
            if diff > 0.1:
                lines.append(f"La confiance a {direction} ({av:.0%} → {bv:.0%}).")
            elif diff < -0.1:
                lines.append(f"La confiance a {direction} ({av:.0%} → {bv:.0%}).")
        elif row["metric"] == "deaths":
            if diff != 0:
                lines.append(f"Les morts : {int(av)} vs {int(bv)} ({direction} de {abs(int(diff))}).")
        elif row["metric"] == "builds":
            if diff != 0:
                lines.append(f"Les constructions : {int(av)} vs {int(bv)}.")
    
    if not lines[2:]:
        lines.append("Les deux expériences sont très similaires.")
    
    return "\n".join(lines)


def compare_table(a, b):
    """Return a formatted comparison table string."""
    rows = compare_results(a, b)
    lines = []
    lines.append(f"{'Métrique':<25} {'A':>10} {'B':>10} {'Diff':>10}")
    lines.append("-" * 58)
    for row in rows:
        lines.append(
            f"{row['label']:<25} {row['a']:>10.2f} {row['b']:>10.2f} {row['difference']:>+10.2f}"
        )
    return "\n".join(lines)
