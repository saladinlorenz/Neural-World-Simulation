"""WorldOverlay — couches de visualisation superposées à la carte."""
import math

from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QColor, QPen, QBrush

from game.config import GRID, TILE, CLAN_COLORS
from game.studio_text import level_color

MODES = [
    "normal", "ressources", "danger", "memoire", "relations",
    "besoins", "anima", "culture", "institutions", "territoires",
]

_MODE_LABELS = {
    "normal": "Normal",
    "ressources": "Ressources",
    "danger": "Danger",
    "memoire": "Mémoire",
    "relations": "Relations",
    "besoins": "Besoins",
    "anima": "Anima",
    "culture": "Culture",
    "institutions": "Institutions",
    "territoires": "Territoires",
}

#: Modes exigeant un habitant sélectionné (Lot G.1).
CONTEXT_MODES = {"memoire", "danger", "relations", "besoins", "anima"}

_MODE_HELP = {
    "normal": "Rendu standard du monde.",
    "ressources": "Monde — densité de nourriture, bois et pierre.",
    "danger": "Habitant requis — feux, senteurs et dangers perçus.",
    "memoire": "Habitant requis — cellules de croyance et souvenirs.",
    "relations": "Habitant requis — liens de confiance et d'affinité.",
    "besoins": "Habitant requis — faim, soif, fatigue et douleur.",
    "anima": "Habitant requis — identité, valeurs et trauma.",
    "culture": "Monde — savoirs culturels partagés.",
    "institutions": "Monde — institutions émergentes.",
    "territoires": "Monde — villages et zones de domination.",
}

_IDENTITY_COLORS = {
    "builder": QColor(70, 130, 200),
    "provider": QColor(80, 170, 80),
    "fighter": QColor(200, 60, 60),
    "explorer": QColor(180, 160, 50),
    "caretaker": QColor(180, 100, 180),
    "survivor": QColor(150, 150, 150),
}


def _hex_to_qcolor(h):
    if h.startswith("#"):
        h = h[1:]
    r = int(h[0:2], 16)
    g = int(h[2:4], 16)
    b = int(h[4:6], 16)
    return QColor(r, g, b)


class WorldOverlay:
    #: Budget max d'itérations Python par frame pour les boucles tuile par
    #: tuile. Au-delà, on sous-échantillonne : sans cette limite, un overlay
    #: au zoom par défaut (100 000+ tuiles visibles) gèle l'interface.
    TILE_LOOP_BUDGET = 40000

    #: Cellules de croyance dessinées par habitant (l'overlay mémoire peut
    #: porter des centaines de cellules par agent sur un monde peuplé).
    BELIEF_CELLS_PER_AGENT = 24
    MEMORY_AGENT_BUDGET = 40
    CULTURE_CELL_BUDGET = 400
    INSTITUTION_BUDGET = 200

    def __init__(self):
        pass

    @classmethod
    def _tile_step(cls, x0, y0, x1, y1):
        count = max(1, (x1 - x0) * (y1 - y0))
        if count <= cls.TILE_LOOP_BUDGET:
            return 1
        return max(1, int(math.sqrt(count / cls.TILE_LOOP_BUDGET)))

    def mode_label(self, mode):
        return _MODE_LABELS.get(mode, mode)

    def mode_help(self, mode):
        """Aide contextuelle (tooltip) du mode d'overlay (Lot F.4)."""
        return _MODE_HELP.get(mode, "")

    def paint_message(self, painter, message):
        """Message centré (overlay sans sélection — Lot G.1)."""
        from PyQt6.QtCore import Qt
        painter.save()
        painter.setPen(QColor(220, 228, 240))
        painter.drawText(painter.window(),
                         Qt.AlignmentFlag.AlignCenter, message)
        painter.restore()

    def paint(self, painter, map_transform, sim, active_mode):
        if active_mode == "normal":
            return
        # Lot G.1 : mémoire/danger/relations/besoins/anima exigent un
        # habitant sélectionné ; les autres modes restent globaux.
        if active_mode in CONTEXT_MODES:
            agent = getattr(sim, "selected", None)
            if agent is None or not getattr(agent, "alive", False):
                self.paint_message(
                    painter,
                    "Sélectionnez un habitant pour cet overlay")
                return

        w = sim.w
        screen_w = painter.device().width()
        screen_h = painter.device().height()

        if active_mode == "danger":
            self._paint_danger(painter, map_transform, sim, screen_w, screen_h)
        elif active_mode == "ressources":
            self._paint_ressources(painter, map_transform, sim, screen_w, screen_h)
        elif active_mode == "memoire":
            self._paint_memoire(painter, map_transform, sim, screen_w, screen_h)
        elif active_mode == "relations":
            self._paint_relations(painter, map_transform, sim, screen_w, screen_h)
        elif active_mode == "besoins":
            self._paint_besoins(painter, map_transform, sim, screen_w, screen_h)
        elif active_mode == "anima":
            self._paint_anima(painter, map_transform, sim, screen_w, screen_h)
        elif active_mode == "culture":
            self._paint_culture(painter, map_transform, sim, screen_w, screen_h)
        elif active_mode == "institutions":
            self._paint_institutions(painter, map_transform, sim, screen_w, screen_h)
        elif active_mode == "territoires":
            self._paint_territoires(painter, map_transform, sim, screen_w, screen_h)

    def _paint_danger(self, painter, transform, sim, sw, sh):
        w = sim.w
        x0, y0, x1, y1 = transform.visible_tiles(TILE, GRID, sw, sh)
        step = self._tile_step(x0, y0, x1, y1)
        ts = max(2, int(TILE * transform.zoom) * step)
        painter.setPen(QPen(QColor(0, 0, 0), 0))
        for ty in range(y0, y1, step):
            for tx in range(x0, x1, step):
                if not (0 <= tx < w.g and 0 <= ty < w.g):
                    continue
                danger = 0.0
                if hasattr(w, "fire") and w.fire[ty, tx] > 0:
                    danger = max(danger, float(w.fire[ty, tx]))
                if hasattr(w, "smell") and w.smell[ty, tx] > 0:
                    danger = max(danger, float(w.smell[ty, tx]))
                if danger <= 0:
                    continue
                sx, sy = transform.to_screen(tx * TILE, ty * TILE)
                h_val = min(1.0, danger)
                c = _hex_to_qcolor(level_color(h_val))
                c.setAlpha(int(120 + 80 * h_val))
                painter.fillRect(int(sx), int(sy), ts, ts, c)

    def _paint_ressources(self, painter, transform, sim, sw, sh):
        w = sim.w
        x0, y0, x1, y1 = transform.visible_tiles(TILE, GRID, sw, sh)
        step = self._tile_step(x0, y0, x1, y1)
        ts = max(2, int(TILE * transform.zoom) * step)
        painter.setPen(QPen(QColor(0, 0, 0), 0))
        has_content = hasattr(w, "content")
        for ty in range(y0, y1, step):
            for tx in range(x0, x1, step):
                if not (0 <= tx < w.g and 0 <= ty < w.g):
                    continue
                res = float(w.regrow[ty, tx]) if hasattr(w, "regrow") else 0.0
                # Une repousse compte double ; un asset récoltable compte aussi,
                # sinon l'overlay reste vide tant qu'aucun arbre n'est coupé.
                if has_content and w.content[ty, tx] >= 0:
                    res = max(res, 0.45)
                if res <= 0:
                    continue
                sx, sy = transform.to_screen(tx * TILE, ty * TILE)
                h_val = min(1.0, res)
                c = _hex_to_qcolor(level_color(h_val))
                c.setAlpha(int(80 + 100 * h_val))
                painter.fillRect(int(sx), int(sy), ts, ts, c)

    def _paint_memoire(self, painter, transform, sim, sw, sh):
        """Cellules de croyance (danger mémorisé) + marqueurs d'habitants.

        ``Being.belief_places`` est indexé par cellule de 8 tuiles :
        ``(tx // 8, ty // 8) -> danger 0..1``.
        """
        cell = 8 * TILE
        cs = max(2, int(cell * transform.zoom))
        agents = [a for a in sim.agents if a.alive]
        selected = getattr(sim, "selected", None)
        selected_eid = getattr(selected, "eid", None) if selected is not None else None
        if len(agents) > self.MEMORY_AGENT_BUDGET:
            head = [a for a in agents if a.eid == selected_eid]
            agents = head + [a for a in agents
                             if a.eid != selected_eid][: self.MEMORY_AGENT_BUDGET - len(head)]

        painter.setPen(QPen(QColor(255, 255, 100, 90), 1))
        for agent in agents:
            beliefs = getattr(agent, "belief_places", None)
            if beliefs:
                for i, (key, danger) in enumerate(beliefs.items()):
                    if i >= self.BELIEF_CELLS_PER_AGENT:
                        break
                    if not isinstance(key, (tuple, list)) or len(key) != 2:
                        continue
                    try:
                        val = min(1.0, max(0.0, float(danger)))
                    except (TypeError, ValueError):
                        val = 0.0
                    sx, sy = transform.to_screen(key[0] * cell, key[1] * cell)
                    if not (-cs < sx < sw + cs and -cs < sy < sh + cs):
                        continue
                    c = QColor(255, 255, 100, int(30 + 120 * val))
                    painter.setBrush(QBrush(c))
                    painter.drawRect(int(sx), int(sy), cs, cs)
            sx, sy = transform.to_screen(agent.x, agent.y)
            if -20 < sx < sw + 20 and -20 < sy < sh + 20:
                painter.setBrush(QBrush(QColor(255, 255, 100, 60)))
                painter.drawEllipse(QPointF(sx, sy), 10, 10)

    def _paint_relations(self, painter, transform, sim, sw, sh):
        """Liens sociaux : ``Being.rel`` = ``{eid: [confiance, affection]}``."""
        agent_map = {a.eid: a for a in sim.agents if a.alive}
        drawn = set()
        for a in agent_map.values():
            rel = getattr(a, "rel", None)
            if not rel:
                continue
            sx1, sy1 = transform.to_screen(a.x, a.y)
            if not (-50 < sx1 < sw + 50 and -50 < sy1 < sh + 50):
                continue
            for other_eid, values in rel.items():
                pair = (min(a.eid, other_eid), max(a.eid, other_eid))
                if pair in drawn:
                    continue
                drawn.add(pair)
                other = agent_map.get(other_eid)
                if other is None:
                    continue
                try:
                    confiance = float(values[0])
                    affection = float(values[1]) if len(values) > 1 else 0.0
                except (TypeError, ValueError, IndexError):
                    continue
                sx2, sy2 = transform.to_screen(other.x, other.y)
                if not (-50 < sx2 < sw + 50 and -50 < sy2 < sh + 50):
                    continue
                score = (confiance + affection) / 2.0
                if score >= 0:
                    c = QColor(90, 200, 120, int(70 + 130 * min(1.0, score)))
                else:
                    c = QColor(230, 90, 90, int(70 + 130 * min(1.0, -score)))
                painter.setPen(QPen(c, 1.5))
                painter.drawLine(QPointF(sx1, sy1), QPointF(sx2, sy2))

    def _paint_besoins(self, painter, transform, sim, sw, sh):
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        for a in sim.agents:
            if not a.alive:
                continue
            sx, sy = transform.to_screen(a.x, a.y)
            if not (-20 < sx < sw + 20 and -20 < sy < sh + 20):
                continue
            faim = getattr(a, "hunger", 0.0)
            c = _hex_to_qcolor(level_color(faim))
            painter.setBrush(QBrush(c))
            painter.drawEllipse(QPointF(sx, sy), 7, 7)

    def _paint_anima(self, painter, transform, sim, sw, sh):
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        for a in sim.agents:
            if not a.alive:
                continue
            sx, sy = transform.to_screen(a.x, a.y)
            if not (-20 < sx < sw + 20 and -20 < sy < sh + 20):
                continue
            identity = (getattr(a, "anima", None) or {}).get("identity") or {}
            dominant = max(identity, key=identity.get) if identity else None
            c = _IDENTITY_COLORS.get(dominant, QColor(150, 150, 150))
            painter.setBrush(QBrush(c))
            painter.drawEllipse(QPointF(sx, sy), 7, 7)

    def _paint_culture(self, painter, transform, sim, sw, sh):
        """Savoirs partagés : culture de clan (cellules de 8 tuiles) et
        connaissance universelle (faits ponctuels vérifiés)."""
        cell = 8 * TILE
        cs = max(2, int(cell * transform.zoom))
        ck = getattr(sim, "clan_knowledge", None)
        culture = getattr(ck, "culture", None) if ck is not None else None
        if culture:
            painter.setPen(QPen(QColor(200, 150, 50, 120), 1))
            for i, (key, fact) in enumerate(culture.items()):
                if i >= self.CULTURE_CELL_BUDGET:
                    break
                if not isinstance(key, (tuple, list)) or len(key) != 3:
                    continue
                conf = fact.get("confidence", 0.0) if isinstance(fact, dict) else 0.0
                try:
                    conf = min(1.0, max(0.0, float(conf)))
                except (TypeError, ValueError):
                    conf = 0.0
                sx, sy = transform.to_screen(key[1] * cell, key[2] * cell)
                if not (-cs < sx < sw + cs and -cs < sy < sh + cs):
                    continue
                painter.setBrush(QBrush(QColor(200, 150, 50, int(25 + 120 * conf))))
                painter.drawRect(int(sx), int(sy), cs, cs)

        uk = getattr(sim, "universal_knowledge", None)
        places = getattr(uk, "places", None) if uk is not None else None
        if places:
            painter.setPen(QPen(QColor(120, 200, 230, 150), 1))
            painter.setBrush(QBrush(QColor(120, 200, 230, 90)))
            painted = 0
            for facts in places.values():
                for (tx, ty) in facts:
                    if painted >= self.CULTURE_CELL_BUDGET:
                        break
                    sx, sy = transform.to_screen(tx * TILE + TILE / 2, ty * TILE + TILE / 2)
                    if -cs < sx < sw + cs and -cs < sy < sh + cs:
                        painter.drawEllipse(QPointF(sx, sy), 5, 5)
                        painted += 1

    def _paint_institutions(self, painter, transform, sim, sw, sh):
        """Institutions de clan : ``{(kind, tx//8, ty//8): {members, trust, …}}``."""
        cell = 8 * TILE
        cs = max(2, int(cell * transform.zoom))
        ck = getattr(sim, "clan_knowledge", None)
        institutions = getattr(ck, "institutions", None) if ck is not None else None
        if not institutions:
            return
        agent_map = {a.eid: a for a in sim.agents if a.alive}
        for i, (key, inst) in enumerate(institutions.items()):
            if i >= self.INSTITUTION_BUDGET:
                break
            if not isinstance(key, (tuple, list)) or len(key) != 3:
                continue
            if not isinstance(inst, dict):
                continue
            sx, sy = transform.to_screen(key[1] * cell + cell / 2, key[2] * cell + cell / 2)
            if not (-cs < sx < sw + cs and -cs < sy < sh + cs):
                continue
            try:
                trust = min(1.0, max(0.0, float(inst.get("trust", 0.0))))
            except (TypeError, ValueError):
                trust = 0.0
            painter.setPen(QPen(QColor(180, 80, 200, 170), 2))
            painter.setBrush(QBrush(QColor(180, 80, 200, int(25 + 60 * trust))))
            painter.drawRect(int(sx - cs / 2), int(sy - cs / 2), cs, cs)

            points = []
            for eid in list(inst.get("members", []))[:8]:
                member = agent_map.get(eid)
                if member is None:
                    continue
                mx, my = transform.to_screen(member.x, member.y)
                if -50 < mx < sw + 50 and -50 < my < sh + 50:
                    points.append(QPointF(mx, my))
            painter.setPen(QPen(QColor(200, 130, 230, 110), 1))
            for p in points:
                painter.drawLine(QPointF(sx, sy), p)

    def _paint_territoires(self, painter, transform, sim, sw, sh):
        clans = {}
        for a in sim.agents:
            if not a.alive:
                continue
            c = getattr(a, "color", "gray")
            if c not in clans:
                clans[c] = []
            clans[c].append(a)
        for clan, members in clans.items():
            if len(members) < 2:
                continue
            r, g, b = CLAN_COLORS.get(clan, (150, 150, 150))
            c = QColor(r, g, b, 40)
            painter.setPen(QPen(QColor(r, g, b, 100), 1))
            painter.setBrush(QBrush(c))
            for a in members:
                sx, sy = transform.to_screen(a.x, a.y)
                if -50 < sx < sw + 50 and -50 < sy < sh + 50:
                    painter.drawEllipse(QPointF(sx, sy), 20, 20)
