"""WorldOverlay — couches de visualisation superposées à la carte."""
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
    def __init__(self):
        pass

    def mode_label(self, mode):
        return _MODE_LABELS.get(mode, mode)

    def paint(self, painter, map_transform, sim, active_mode):
        if active_mode == "normal":
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
        x0, y0, x1, y1 = transform.visible_tiles(TILE, GRID)
        ts = max(2, int(TILE * transform.zoom))
        painter.setPen(QPen(QColor(0, 0, 0), 0))
        for ty in range(y0, y1):
            for tx in range(x0, x1):
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
        x0, y0, x1, y1 = transform.visible_tiles(TILE, GRID)
        ts = max(2, int(TILE * transform.zoom))
        painter.setPen(QPen(QColor(0, 0, 0), 0))
        for ty in range(y0, y1):
            for tx in range(x0, x1):
                if not (0 <= tx < w.g and 0 <= ty < w.g):
                    continue
                res = float(w.regrow[ty, tx]) if hasattr(w, "regrow") else 0.0
                if res <= 0:
                    continue
                sx, sy = transform.to_screen(tx * TILE, ty * TILE)
                h_val = min(1.0, res)
                c = _hex_to_qcolor(level_color(h_val))
                c.setAlpha(int(80 + 100 * h_val))
                painter.fillRect(int(sx), int(sy), ts, ts, c)

    def _paint_memoire(self, painter, transform, sim, sw, sh):
        w = sim.w
        x0, y0, x1, y1 = transform.visible_tiles(TILE, GRID)
        ts = max(2, int(TILE * transform.zoom))
        painter.setPen(QPen(QColor(255, 255, 100), 1))
        painter.setBrush(QBrush(QColor(255, 255, 100, 40)))
        for agent in sim.agents:
            if not agent.alive:
                continue
            beliefs = getattr(agent, "croyances_danger", {})
            if not beliefs:
                continue
            for place_key in beliefs:
                if not isinstance(place_key, (list, tuple)) and "_" in str(place_key):
                    continue
            sx, sy = transform.to_screen(agent.x, agent.y)
            if -20 < sx < sw + 20 and -20 < sy < sh + 20:
                painter.drawEllipse(QPointF(sx, sy), 12, 12)
        for ty in range(y0, y1):
            for tx in range(x0, x1):
                if not (0 <= tx < w.g) or not (0 <= ty < w.g):
                    continue
                sx, sy = transform.to_screen(tx * TILE, ty * TILE)
                painter.setPen(QPen(QColor(255, 255, 100, 30), 1))
                painter.setBrush(QBrush(QColor(255, 255, 100, 15)))
                painter.drawRect(int(sx), int(sy), ts, ts)

    def _paint_relations(self, painter, transform, sim, sw, sh):
        pen = QPen(QColor(100, 180, 255, 120), 1.5)
        painter.setPen(pen)
        agent_map = {}
        for a in sim.agents:
            if a.alive:
                agent_map[a.eid] = a
        drawn = set()
        for a in sim.agents:
            if not a.alive:
                continue
            rels = getattr(a, "relations", [])
            for r in rels:
                other_eid = r.get("eid")
                if other_eid is None:
                    continue
                pair = (min(a.eid, other_eid), max(a.eid, other_eid))
                if pair in drawn:
                    continue
                drawn.add(pair)
                other = agent_map.get(other_eid)
                if other is None or not other.alive:
                    continue
                sx1, sy1 = transform.to_screen(a.x, a.y)
                sx2, sy2 = transform.to_screen(other.x, other.y)
                if (-50 < sx1 < sw + 50 and -50 < sy1 < sh + 50 and
                        -50 < sx2 < sw + 50 and -50 < sy2 < sh + 50):
                    painter.drawLine(QPointF(sx1, sy1), QPointF(sx2, sy2))

    def _paint_besoins(self, painter, transform, sim, sw, sh):
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        for a in sim.agents:
            if not a.alive:
                continue
            sx, sy = transform.to_screen(a.x, a.y)
            if not (-20 < sx < sw + 20 and -20 < sy < sh + 20):
                continue
            faim = getattr(a, "faim", 0.0)
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
            identity = getattr(a, "identity", {})
            if identity:
                dominant = max(identity, key=identity.get)
            else:
                dominant = None
            c = _IDENTITY_COLORS.get(dominant, QColor(150, 150, 150))
            painter.setBrush(QBrush(c))
            painter.drawEllipse(QPointF(sx, sy), 7, 7)

    def _paint_culture(self, painter, transform, sim, sw, sh):
        painter.setPen(QPen(QColor(200, 150, 50, 100), 1))
        for a in sim.agents:
            if not a.alive:
                continue
            sx, sy = transform.to_screen(a.x, a.y)
            if not (-20 < sx < sw + 20 and -20 < sy < sh + 20):
                continue
            knowledge = getattr(a, "confirmed_knowledge", [])
            if knowledge:
                painter.setBrush(QBrush(QColor(200, 150, 50, 60)))
                painter.drawRect(int(sx) - 8, int(sy) - 8, 16, 16)

    def _paint_institutions(self, painter, transform, sim, sw, sh):
        institutions = getattr(sim, "institutions", [])
        painter.setPen(QPen(QColor(180, 80, 200, 150), 2))
        painter.setBrush(QBrush(QColor(180, 80, 200, 30)))
        for inst in institutions:
            members = inst.get("members", [])
            if len(members) < 2:
                continue
            points = []
            for a in sim.agents:
                if a.alive and a.eid in members:
                    sx, sy = transform.to_screen(a.x, a.y)
                    points.append(QPointF(sx, sy))
            if len(points) >= 2:
                for i in range(len(points)):
                    for j in range(i + 1, len(points)):
                        painter.drawLine(points[i], points[j])

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
