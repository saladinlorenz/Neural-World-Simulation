"""Modèles Qt pour les métriques du laboratoire."""
from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt


METRIC_LABELS = {
    "population": "Population",
    "births": "Naissances",
    "deaths": "Morts",
    "builds": "Constructions terminées",
    "harvests": "Récoltes",
    "food_given": "Dons de nourriture",
    "messages": "Messages envoyés",
    "confirmed_knowledge": "Connaissances confirmées",
    "institutions": "Institutions stables",
    "mean_health": "Santé moyenne",
    "mean_hunger": "Faim moyenne",
    "mean_trust": "Confiance moyenne",
}


class MetricsModel(QAbstractTableModel):
    """Model for experiment metrics table."""
    
    HEADERS = ["Métrique", "Valeur"]
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._data = []  # list of (label, value)
    
    def load(self, metrics_dict):
        self.beginResetModel()
        self._data = []
        for key, label in METRIC_LABELS.items():
            if key in metrics_dict:
                self._data.append((label, metrics_dict[key]))
        self.endResetModel()
    
    def rowCount(self, parent=QModelIndex()):
        return len(self._data)
    
    def columnCount(self, parent=QModelIndex()):
        return 2
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        row = index.row()
        col = index.column()
        if row >= len(self._data):
            return None
        
        label, value = self._data[row]
        
        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0:
                return label
            if col == 1:
                if isinstance(value, float):
                    return f"{value:.2f}"
                return str(value)
        if role == Qt.ItemDataRole.TextAlignmentRole:
            if col == 1:
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        return None
    
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return None


class ComparisonModel(QAbstractTableModel):
    """Model for A/B comparison table."""
    
    HEADERS = ["Métrique", "A", "B", "Différence"]
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._rows = []
    
    def load(self, comparison_rows):
        self.beginResetModel()
        self._rows = comparison_rows
        self.endResetModel()
    
    def rowCount(self, parent=QModelIndex()):
        return len(self._rows)
    
    def columnCount(self, parent=QModelIndex()):
        return 4
    
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        row = index.row()
        col = index.column()
        if row >= len(self._rows):
            return None
        
        r = self._rows[row]
        
        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0:
                return r.get("label", r.get("metric", ""))
            if col == 1:
                return f"{r['a']:.2f}"
            if col == 2:
                return f"{r['b']:.2f}"
            if col == 3:
                d = r["difference"]
                return f"{d:+.2f}"
        if role == Qt.ItemDataRole.TextAlignmentRole:
            if col > 0:
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        return None
    
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return None
