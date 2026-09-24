"""TileDock — examinateur de tuile (Lot D.6).

Affiche ``diagnostics.tile_snapshot`` pour la tuile sélectionnée en mode
« Examiner ». Toutes les données moteur (abri, feu, odeur, phéromone,
repousse, tombe, dépôt, chantier, biome, altitude, pente) deviennent
consultables depuis Qt.
"""
from __future__ import annotations

from PyQt6.QtWidgets import (QDockWidget, QStackedWidget, QTreeWidget,
                              QTreeWidgetItem)

from game.ui_snapshots import tile_snapshot
from ui_qt.widgets.empty_state import EmptyState

_LABELS = {
    "tx": "Tuile X",
    "ty": "Tuile Y",
    "terre": "Terre",
    "eau": "Eau",
    "bloque": "Bloquée",
    "abri": "Abri",
    "feu": "Feu",
    "odeur": "Odeur",
    "exploration": "Exploration",
    "pheromone": "Phéromone",
    "couleur_pheromone": "Couleur phéromone",
    "sol": "Sol",
    "objet": "Objet posé",
    "pv_objet": "PV objet",
    "repousse": "Repousse",
    "cimetiere": "Cimetière",
    "tombe": "Tombe",
    "stockage": "Dépôt",
    "chantier": "Chantier",
    "biome": "Biome",
    "altitude": "Altitude",
    "pente": "Pente",
    "nom": "Nom",
    "tick_deces": "Tick du décès",
    "couleur": "Couleur",
    "capacite": "Capacité",
    "inventaire": "Inventaire",
    "clan": "Clan",
    "remplissage": "Remplissage",
    "progression": "Progression",
    "manquant": "Matériaux manquants",
    "contributeurs": "Contributeurs",
    "blocs_poses": "Blocs posés",
    "blocs_total": "Blocs prévus",
}


def _label(key):
    return _LABELS.get(key, str(key))


def _fmt(value):
    if isinstance(value, bool):
        return "oui" if value else "non"
    if isinstance(value, float):
        return f"{value:.2f}"
    if isinstance(value, (list, tuple)):
        return ", ".join(_fmt(v) for v in value)
    if isinstance(value, dict):
        return ""
    return str(value)


class TileDock(QDockWidget):
    """Panneau d'inspection d'une tuile du monde."""

    def __init__(self, controller, parent=None):
        super().__init__("Tuile", parent)
        self.controller = controller
        self._tree = QTreeWidget()
        self._tree.setHeaderLabels(["Champ", "Valeur"])
        self._tree.setColumnCount(2)
        self._last_tile = None
        self._tree.addTopLevelItem(QTreeWidgetItem(
            ["Mode « Examiner » : cliquez une tuile.", ""]))

        # Lot E : vue vide persistante, basculée par refresh().
        self.empty_state = EmptyState(
            icon="⌖",
            title="Aucune tuile sélectionnée",
            message="Activez le mode « Examiner » puis cliquez une tuile du monde.",
        )
        self._stack = QStackedWidget()
        self._stack.addWidget(self.empty_state)
        self._stack.addWidget(self._tree)
        self.setWidget(self._stack)

    def refresh(self):
        tile = getattr(self.controller.ui_state, "selected_tile", None)
        if tile is None:
            if self._last_tile is not None:
                self._tree.clear()
                self._tree.addTopLevelItem(QTreeWidgetItem(
                    ["Mode « Examiner » : cliquez une tuile.", ""]))
                self._last_tile = None
            self.empty_state.set_state(
                "⌖",
                "Aucune tuile sélectionnée",
                "Activez le mode « Examiner » puis cliquez une tuile du monde.",
            )
            self._stack.setCurrentWidget(self.empty_state)
            return
        snap = tile_snapshot(self.controller.sim, tile[0], tile[1])
        self._last_tile = tuple(tile)
        self._tree.clear()
        for key, value in snap.items():
            self._tree.addTopLevelItem(self._item(key, value))
        self._tree.expandToDepth(1)

        # Lot E : hors monde -> vue vide (l'arbre reste rempli dessous).
        if not snap.get("dans_monde", True):
            self.empty_state.set_state(
                "⌖",
                "Tuile hors du monde",
                f"La tuile {tile[0]},{tile[1]} se trouve hors des limites du monde.",
            )
            self._stack.setCurrentWidget(self.empty_state)
        else:
            self._stack.setCurrentWidget(self._tree)

    def _item(self, key, value):
        item = QTreeWidgetItem([_label(key), _fmt(value)])
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                item.addChild(self._item(sub_key, sub_value))
        return item
