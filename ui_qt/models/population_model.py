"""PopulationModel — modèle Qt pour la liste des habitants."""
from PyQt6.QtCore import QAbstractTableModel, Qt, QSize
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen

from game.config import CLAN_COLORS


def _pct(value) -> float:
    """Pourcentage sûr : la valeur est bornée à [0, 1] avant mise en forme.

    Une santé ou un besoin hors bornes (négatif, > 1) ne doit jamais
    s'afficher comme « -386 % » ou « 140 % ».
    """
    try:
        v = float(value)
    except (TypeError, ValueError):
        return 0.0
    if v != v:  # NaN
        return 0.0
    return max(0.0, min(1.0, v))


def _make_placeholder(clan):
    pm = QPixmap(24, 24)
    pm.fill(QColor(0, 0, 0, 0))
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    rgb = CLAN_COLORS.get(clan, (150, 150, 150))
    c = QColor(*rgb)
    p.setBrush(c)
    p.setPen(QPen(QColor(60, 60, 60), 1))
    p.drawEllipse(2, 2, 20, 20)
    p.end()
    return pm


class PopulationModel(QAbstractTableModel):
    HEADERS = ["Portrait", "Nom", "Sexe", "Age", "Sante", "Energie", "Faim", "Classe", "Stage", "EID"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._rows = []
        self._portraits = {}
        self._current_revision = -1
        self._filter_signature = ""

    def set_snapshot(self, rows, portraits=None, revision=-1, filter_signature=""):
        # Only reset if revision changed or filter signature changed
        if revision != self._current_revision or filter_signature != self._filter_signature:
            self.beginResetModel()
            self._rows = list(rows)
            self._portraits = portraits or {}
            self._current_revision = revision
            self._filter_signature = filter_signature
            self.endResetModel()
        else:
            # Data changed but revision same - update in place if possible
            if len(self._rows) == len(rows):
                self._rows = list(rows)
                self._portraits = portraits or {}
                self.dataChanged.emit(self.index(0, 0), self.index(len(rows) - 1, 9))

    def rowCount(self, parent=None):
        return len(self._rows)

    def columnCount(self, parent=None):
        return len(self.HEADERS)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return None

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or index.row() >= len(self._rows):
            return None
        row = self._rows[index.row()]
        col = index.column()

        if role == Qt.ItemDataRole.DecorationRole and col == 0:
            eid = row.get("eid")
            if eid in self._portraits:
                return self._portraits[eid]
            clan = row.get("clan", "")
            return _make_placeholder(clan)

        if role == Qt.ItemDataRole.DisplayRole:
            needs = row.get("needs_named", {}) or {}
            if col == 0:
                return ""
            elif col == 1:
                name = row.get("name", "")
                # Les décédés viennent du tampon Sim.deceased : les marquer,
                # sinon « Tous » ressemble exactement à « Vivants ».
                return name if row.get("alive", True) else f"† {name}"
            elif col == 2:
                return row.get("sex", "")
            elif col == 3:
                return f"{row.get('age_years', 0):.1f}"
            elif col == 4:
                return f"{_pct(row.get('health', 0)):.0%}"
            elif col == 5:
                return f"{_pct(needs.get('énergie', 0)):.0%}"
            elif col == 6:
                return f"{_pct(needs.get('faim', 0)):.0%}"
            elif col == 7:
                return row.get("class", "")
            elif col == 8:
                return row.get("stage", "")
            elif col == 9:
                return str(row.get("eid", ""))
            return ""

        if role == Qt.ItemDataRole.UserRole:
            return row.get("eid")

        return None

    def eid_at(self, row):
        if 0 <= row < len(self._rows):
            return self._rows[row].get("eid")
        return None
