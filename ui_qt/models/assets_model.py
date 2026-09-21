"""AssetsModel — modèle Qt pour le catalogue d'assets."""
from PyQt6.QtCore import QAbstractTableModel, Qt


class AssetsModel(QAbstractTableModel):
    HEADERS = ["ID", "Nom", "Categorie", "Role", "Placable"]

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
            keys = ["id", "nom", "categorie", "role", "placable"]
            if col < len(keys):
                val = row.get(keys[col], "")
                if isinstance(val, bool):
                    return "Oui" if val else "Non"
                return str(val)
            return ""
        return None
