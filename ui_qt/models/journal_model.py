"""JournalModel — modèle Qt pour le journal."""
from PyQt6.QtCore import QAbstractTableModel, Qt


class JournalModel(QAbstractTableModel):
    HEADERS = ["Tick", "Categorie", "Texte", "Compte"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._rows = []

    def set_snapshot(self, rows):
        self.beginResetModel()
        self._rows = list(rows)
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

        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0:
                tick = row.get("tick", 0)
                mm, ss = divmod(int(tick / 60), 60)
                return f"{mm:02}:{ss:02}"
            elif col == 1:
                return row.get("category", "")
            elif col == 2:
                return row.get("text", "")
            elif col == 3:
                cnt = row.get("count", 1)
                return str(cnt) if cnt > 1 else ""
            return ""

        if role == Qt.ItemDataRole.ForegroundRole and col == 1:
            from PyQt6.QtGui import QColor
            cat = row.get("category", "monde")
            colors = {
                "combat": (214, 84, 84), "social": (198, 100, 162),
                "meteo": (62, 124, 214), "economie": (206, 160, 50),
                "vie": (67, 160, 92), "mort": (140, 80, 86),
                "batiment": (96, 154, 96), "monde": (112, 126, 150),
            }
            r, g, b = colors.get(cat, (105, 114, 129))
            return QColor(r, g, b)

        return None
