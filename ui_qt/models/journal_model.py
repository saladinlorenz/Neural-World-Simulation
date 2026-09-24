"""JournalModel — modèle Qt pour le journal."""
from PyQt6.QtCore import QAbstractTableModel, Qt
from PyQt6.QtGui import QColor

from game.ui_registry import JOURNAL_CATEGORIES

#: Categories « entrée importante » (Lot G), mappees sur les vrais ids du
#: registre JOURNAL_CATEGORIES (game/ui_registry.py) et sur ce que le moteur
#: logge reellement dans ``sim.log`` :
#: naissance → life (simulation.py, categorie reelle du bulletin de naissance)
#:   + family (correspondance kind→categorie de studio_timeline.py) ;
#: mort → death ; attaque → combat ; chantier achevé → building ;
#: incendie → danger (pas « weather » : cette categorie mélange aussi pluie
#:   et neige, on ne veut pas marquer chaque bulletin météo) ;
#: institution / culture → culture (meme correspondance timeline).
#: ids « family », « danger » et « culture » gardes au cas ou : ils sont
#: produits par le normaliseur de timeline et par les futures entrees.
IMPORTANT_CATEGORIES = frozenset({
    "life", "family", "death", "danger", "combat", "building", "culture",
})

#: Pastille des entrees importantes (ambree, palette Neural Lab).
IMPORTANT_COLOR = QColor(246, 189, 96)


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
        # Entree importante (Lot G) : pastille coloree devant le texte.
        # Le prefixe n'existe qu'en affichage : le tri (UserRole) et les
        # exports (journal_snapshot) voient le texte brut.
        important = row.get("category", "") in IMPORTANT_CATEGORIES

        if role == Qt.ItemDataRole.DisplayRole:
            if col == 0:
                tick = row.get("tick", 0)
                mm, ss = divmod(int(tick / 60), 60)
                return f"{mm:02}:{ss:02}"
            elif col == 1:
                cat = row.get("category", "")
                return JOURNAL_CATEGORIES.get(cat, {}).get("label", cat)
            elif col == 2:
                text = row.get("text", "")
                return f"● {text}" if important else text
            elif col == 3:
                cnt = row.get("count", 1)
                return str(cnt) if cnt > 1 else ""
            return ""

        if role == Qt.ItemDataRole.ForegroundRole and col == 1:
            from PyQt6.QtGui import QColor
            cat = row.get("category", "world")
            meta = JOURNAL_CATEGORIES.get(cat)
            if meta is None:
                return QColor(105, 114, 129)
            hex_color = meta["color"].lstrip("#")
            return QColor(int(hex_color[0:2], 16),
                          int(hex_color[2:4], 16),
                          int(hex_color[4:6], 16))

        if (role == Qt.ItemDataRole.ForegroundRole and col == 2
                and important):
            # Meme teinte que la pastille : l'entree ressort du fond sombre.
            return QColor(IMPORTANT_COLOR)

        if role == Qt.ItemDataRole.UserRole:
            # Valeurs brutes : le tri d'un proxy Qt compare ce rôle, sinon
            # « 10:00 » se classerait avant « 9:00 ».
            if col == 0:
                return int(row.get("tick", 0))
            if col == 1:
                cat = row.get("category", "")
                return JOURNAL_CATEGORIES.get(cat, {}).get("label", cat)
            if col == 2:
                return row.get("text", "")
            if col == 3:
                return int(row.get("count", 1))
            return None

        return None
