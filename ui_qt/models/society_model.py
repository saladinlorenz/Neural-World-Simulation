"""SocietyModel — modèle Qt pour les stats de société."""
from PyQt6.QtCore import QAbstractTableModel, Qt


class SocietyModel(QAbstractTableModel):
    HEADERS = ["Categorie", "Valeur"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._rows = []

    def set_snapshot(self, snap):
        self.beginResetModel()
        self._rows = []
        if snap:
            stats = snap.get("stats", {})
            self._rows.append(("Population", snap.get("population", 0)))
            self._rows.append(("Naissances", stats.get("births", 0)))
            self._rows.append(("Deces", stats.get("deaths", 0)))
            self._rows.append(("Generation max", snap.get("max_generation", 0)))
            self._rows.append(("Couples", snap.get("bonded", 0)))
            self._rows.append(("Constructions", stats.get("builds", 0)))
            self._rows.append(("Villages", stats.get("villages", 0)))
            self._rows.append(("Recoltes", stats.get("harvests", 0)))
            self._rows.append(("Dons", stats.get("gives", 0)))
            self._rows.append(("Vols", stats.get("takes", 0)))
            self._rows.append(("Paroles", stats.get("talks", 0)))
            self._rows.append(("Attaques", stats.get("attacks", 0)))
            self._rows.append(("Moutons", snap.get("sheep", 0)))
            self._rows.append(("Monstres", snap.get("monsters", 0)))
        self.endResetModel()

    def rowCount(self, parent=None):
        return len(self._rows)

    def columnCount(self, parent=None):
        return 2

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return None

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or index.row() >= len(self._rows):
            return None
        if role == Qt.ItemDataRole.DisplayRole:
            cat, val = self._rows[index.row()]
            return cat if index.column() == 0 else str(val)
        return None
