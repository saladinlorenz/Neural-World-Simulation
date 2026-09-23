"""PopulationModel — modèle Qt pour la liste des habitants."""
from PyQt6.QtCore import QAbstractTableModel, Qt, QSize
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen

from game.config import CLAN_COLORS


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

    def set_snapshot(self, rows, portraits=None):
        self.beginResetModel()
        self._rows = list(rows)
        self._portraits = portraits or {}
        self.endResetModel()

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
            if col == 0:
                return ""
            elif col == 1:
                nom = row.get("nom", "")
                # Les décédés viennent du tampon Sim.deceased : les marquer,
                # sinon « Tous » ressemble exactement à « Vivants ».
                return nom if row.get("vivant", True) else f"† {nom}"
            elif col == 2:
                return row.get("sexe", row.get("sex", ""))
            elif col == 3:
                return f"{row.get('age_ans', 0):.1f}"
            elif col == 4:
                return f"{row.get('sante', 0):.0%}"
            elif col == 5:
                return f"{row.get('energie', 0):.0%}"
            elif col == 6:
                return f"{row.get('faim', 0):.0%}"
            elif col == 7:
                return row.get("classe", "")
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
