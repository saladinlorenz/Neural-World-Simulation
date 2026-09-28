"""Alertes rares, significatives et actionnables (WORLD ALIVE).

Pur : lit Sim/UI, ne modifie jamais. Chaque alerte porte une cause moteur
réelle, un habitant ou une zone cliquable, et un coût O(n_agents) borné.
L'UI calcule à ~5 Hz (dans _refresh_status) et le clic sélectionne /
centre — jamais de log spam, jamais de nouvel état moteur.
"""
from __future__ import annotations


SEV_ORDER = {"critical": 0, "warn": 1, "info": 2}

#: Seuils moteur (mêmes champs que simulation/décision : hunger, needs[2],
#: energy, health, stuck). Rares par construction : famine exige 3+.
FAMINE_COUNT = 3
FAMINE_LEVEL = 0.80
THIRST_COUNT = 2
THIRST_LEVEL = 0.80
STUCK_TICKS = 20
LOW_TPS = 10.0
MAX_ALERTS = 5


def _num(value, default=0.0) -> float:
    try:
        v = float(value)
    except (TypeError, ValueError):
        return default
    if v != v:  # NaN
        return default
    return v


def compute_alerts(sim, tps: float | None = None) -> list[dict]:
    """Calcule les alertes live. Toujours une liste (jamais None/lève)."""
    try:
        agents = [a for a in getattr(sim, "agents", []) if getattr(a, "alive", False)]
    except Exception:
        return []
    tick = 0
    try:
        tick = int(getattr(getattr(sim, "w", None), "tick", 0))
    except (TypeError, ValueError):
        tick = 0
    alerts: list[dict] = []

    # Famine locale : 3+ habitants > 80 % faim (cause : besoins réels).
    try:
        starving = [a for a in agents if _num(getattr(a, "hunger", 0.0)) > FAMINE_LEVEL]
        if len(starving) >= FAMINE_COUNT:
            worst = max(starving, key=lambda a: _num(getattr(a, "hunger", 0.0)))
            alerts.append({
                "id": "famine",
                "kind": "famine",
                "severity": "warn",
                "title": "Famine locale",
                "detail": "%d habitants > 80 %% faim" % len(starving),
                "eid": int(getattr(worst, "eid", -1)),
                "tx": int(getattr(worst, "tx", 0)),
                "ty": int(getattr(worst, "ty", 0)),
                "tick": tick,
            })
    except Exception:
        pass

    # Risque hydrique : 2+ habitants > 80 % soif.
    try:
        thirsty = [a for a in agents
                   if len(getattr(a, "needs", []) or []) > 2
                   and _num(a.needs[2]) > THIRST_LEVEL]
        if len(thirsty) >= THIRST_COUNT:
            worst = max(thirsty, key=lambda a: _num(a.needs[2]))
            alerts.append({
                "id": "thirst",
                "kind": "thirst",
                "severity": "warn",
                "title": "Risque hydrique",
                "detail": "%d habitants > 80 %% soif" % len(thirsty),
                "eid": int(getattr(worst, "eid", -1)),
                "tx": int(getattr(worst, "tx", 0)),
                "ty": int(getattr(worst, "ty", 0)),
                "tick": tick,
            })
    except Exception:
        pass

    # Blocage : un habitant bloqué depuis 20+ ticks (cause : stuck moteur).
    try:
        stuck = [a for a in agents if int(getattr(a, "stuck", 0) or 0) >= STUCK_TICKS]
        if stuck:
            worst = max(stuck, key=lambda a: int(getattr(a, "stuck", 0) or 0))
            alerts.append({
                "id": "stuck-%d" % int(getattr(worst, "eid", -1)),
                "kind": "stuck",
                "severity": "warn",
                "title": "Blocage",
                "detail": "%s bloqué depuis %d ticks" % (
                    str(getattr(worst, "name", "?")),
                    int(getattr(worst, "stuck", 0) or 0)),
                "eid": int(getattr(worst, "eid", -1)),
                "tx": int(getattr(worst, "tx", 0)),
                "ty": int(getattr(worst, "ty", 0)),
                "tick": tick,
            })
    except Exception:
        pass

    # Blessés critiques : santé < 35 % (cause : health réel).
    try:
        hurt = [a for a in agents if _num(getattr(a, "health", 1.0), 1.0) < 0.35]
        if hurt:
            worst = min(hurt, key=lambda a: _num(getattr(a, "health", 1.0), 1.0))
            alerts.append({
                "id": "hurt-%d" % int(getattr(worst, "eid", -1)),
                "kind": "hurt",
                "severity": "critical",
                "title": "Blessé critique",
                "detail": "%s à %d %%" % (
                    str(getattr(worst, "name", "?")),
                    int(_num(getattr(worst, "health", 0.0)) * 100)),
                "eid": int(getattr(worst, "eid", -1)),
                "tx": int(getattr(worst, "tx", 0)),
                "ty": int(getattr(worst, "ty", 0)),
                "tick": tick,
            })
    except Exception:
        pass

    # Instabilité : TPS sous la cible (cause : perf réelle, pas un seuil monde).
    try:
        if tps is not None and float(tps) < LOW_TPS:
            alerts.append({
                "id": "tps",
                "kind": "tps",
                "severity": "info",
                "title": "Simulation lente",
                "detail": "%.1f TPS < %.0f cible" % (float(tps), LOW_TPS),
                "eid": None,
                "tx": None,
                "ty": None,
                "tick": tick,
            })
    except (TypeError, ValueError):
        pass

    alerts.sort(key=lambda r: (SEV_ORDER.get(r.get("severity", "info"), 9),
                               str(r.get("id", ""))))
    return alerts[:MAX_ALERTS]


def alert_button_text(alerts: list[dict]) -> str:
    """Libellé compact du bouton d'alerte (jamais vide, jamais lève)."""
    try:
        if not alerts:
            return "✓ Calme"
        top = alerts[0]
        sev = top.get("severity", "info")
        icon = "●" if sev == "critical" else ("▲" if sev == "warn" else "○")
        extra = "+%d" % (len(alerts) - 1) if len(alerts) > 1 else ""
        return "%s %s%s" % (icon, str(top.get("title", "Alerte")), extra)
    except Exception:
        return "✓ Calme"
