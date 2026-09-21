"""AssetsDock — dock Qt pour le catalogue d'assets filtrable."""
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                              QLineEdit, QComboBox, QCheckBox,
                              QLabel, QListWidget, QListWidgetItem,
                              QSplitter, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QPixmap, QColor, QPainter, QPen, QIcon

from game.assets_api import CATEGORY_LABELS as _CAT_LIST

CATEGORY_LABELS = dict(_CAT_LIST)


class AssetsDock(QDockWidget):
    """Dock assets avec grille, catégories, recherche, favoris."""

    asset_selected = pyqtSignal(int)

    def __init__(self, controller, parent=None):
        super().__init__("Assets", parent)
        self.controller = controller
        self._am = None
        self._filtered = []
        self._favs = []
        self._setup_ui()

    def set_asset_manager(self, am):
        self._am = am
        self._refresh_catalog()

    def _setup_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(8, 8, 8, 8)

        # Recherche
        self._search = QLineEdit()
        self._search.setPlaceholderText("Rechercher asset...")
        self._search.textChanged.connect(self._on_filter)
        layout.addWidget(self._search)

        # Catégorie
        cat_layout = QHBoxLayout()
        self._cat_combo = QComboBox()
        self._cat_combo.addItem("Tous", "__all__")
        for cat in CATEGORY_LABELS:
            if cat not in ("unites", "interface", "atlas", "rendus"):
                self._cat_combo.addItem(CATEGORY_LABELS[cat], cat)
        self._cat_combo.currentIndexChanged.connect(self._on_filter)
        cat_layout.addWidget(QLabel("Categorie:"))
        cat_layout.addWidget(self._cat_combo)

        self._favs_only = QCheckBox("Favoris")
        self._favs_only.toggled.connect(self._on_filter)
        cat_layout.addWidget(self._favs_only)
        layout.addLayout(cat_layout)

        # Splitter: list on left, detail panel on right
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Liste
        self._list = QListWidget()
        self._list.setIconSize(QSize(48, 48))
        self._list.setSpacing(2)
        self._list.currentItemChanged.connect(self._on_selection_changed)
        self._list.itemDoubleClicked.connect(self._on_fav_toggle)
        splitter.addWidget(self._list)

        # Detail panel
        detail_widget = QWidget()
        detail_layout = QVBoxLayout(detail_widget)
        detail_layout.setContentsMargins(4, 4, 4, 4)

        self._thumb_label = QLabel()
        self._thumb_label.setFixedSize(48, 48)
        self._thumb_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._thumb_label.setStyleSheet("background: #2c3e50; border: 1px solid #555;")
        detail_layout.addWidget(self._thumb_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        self._detail_name = QLabel("")
        self._detail_name.setStyleSheet("font-weight: bold; font-size: 13px;")
        self._detail_name.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        detail_layout.addWidget(self._detail_name)

        self._detail_cat = QLabel("")
        self._detail_cat.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        detail_layout.addWidget(self._detail_cat)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #555;")
        detail_layout.addWidget(sep)

        self._detail_role = QLabel("")
        detail_layout.addWidget(self._detail_role)
        self._detail_placable = QLabel("")
        detail_layout.addWidget(self._detail_placable)
        self._detail_solide = QLabel("")
        detail_layout.addWidget(self._detail_solide)
        self._detail_size = QLabel("")
        detail_layout.addWidget(self._detail_size)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet("color: #555;")
        detail_layout.addWidget(sep2)

        self._detail_desc = QLabel("")
        self._detail_desc.setWordWrap(True)
        self._detail_desc.setStyleSheet("color: #bbb; font-size: 11px;")
        detail_layout.addWidget(self._detail_desc)

        detail_layout.addStretch()
        splitter.addWidget(detail_widget)

        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)
        layout.addWidget(splitter)

        self.setWidget(widget)

    def _on_filter(self, *_args):
        self._refresh_catalog()

    def _refresh_catalog(self):
        if self._am is None:
            return
        search = self._search.text().lower()
        cat = self._cat_combo.currentData() or "__all__"
        self._filtered = []

        for i, a in enumerate(self._am.assets):
            a_cat = getattr(a, "category", "")
            if cat != "__all__" and a_cat != cat:
                continue
            if self._favs_only.isChecked() and i not in self._favs:
                continue
            if search:
                label = getattr(a, "label", getattr(a, "name", "")).lower()
                if search not in label and search not in a_cat.lower():
                    continue
            self._filtered.append((i, a))

        self._list.clear()
        for aid, a in self._filtered:
            label = getattr(a, "label", getattr(a, "name", f"#{aid}"))
            cat_label = CATEGORY_LABELS.get(getattr(a, "category", ""), "")
            fav = "*" if aid in self._favs else " "
            item = QListWidgetItem(f"{fav} {label} ({cat_label})")
            item.setData(Qt.ItemDataRole.UserRole, aid)
            pixmap = self._load_thumbnail(aid, a)
            if pixmap:
                item.setIcon(QIcon(pixmap))
            self._list.addItem(item)

    def _load_thumbnail(self, aid, asset):
        """Try to load a 48x48 thumbnail; fall back to a coloured placeholder."""
        try:
            am = self.controller.sim.am
            pix = am.thumbnail(aid, size=(48, 48))
            if pix is not None:
                from PyQt6.QtGui import QImage
                if isinstance(pix, QImage):
                    return QPixmap.fromImage(pix)
                if isinstance(pix, QPixmap):
                    return pix
        except Exception:
            pass
        # Coloured placeholder based on asset colour attribute
        colour = getattr(asset, "color", None)
        if colour and isinstance(colour, str) and colour.startswith("#"):
            c = QColor(colour)
        else:
            c = QColor(80, 80, 80)
        pm = QPixmap(48, 48)
        pm.fill(QColor(0, 0, 0, 0))
        p = QPainter(pm)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setBrush(c)
        p.setPen(QPen(QColor(60, 60, 60), 1))
        p.drawRoundedRect(2, 2, 44, 44, 6, 6)
        p.end()
        return pm

    def _on_selection_changed(self, current, _previous):
        if current is None:
            return
        aid = current.data(Qt.ItemDataRole.UserRole)
        if aid is None:
            return
        self.controller.ui_state.selected_asset_id = aid
        self.asset_selected.emit(aid)
        if not self._am or not (0 <= aid < len(self._am.assets)):
            return
        a = self._am.assets[aid]
        label = getattr(a, "label", getattr(a, "name", f"#{aid}"))
        cat_label = CATEGORY_LABELS.get(getattr(a, "category", ""), getattr(a, "category", ""))

        self._detail_name.setText(label)
        self._detail_cat.setText(f"Categorie: {cat_label}")
        self._detail_role.setText(f"Role: {getattr(a, 'role', '')}")
        self._detail_placable.setText(
            f"Placable: {'Oui' if getattr(a, 'placable', False) else 'Non'}")
        self._detail_solide.setText(
            f"Solide: {'Oui' if getattr(a, 'solid', False) else 'Non'}")
        w = getattr(a, "width", getattr(a, "w", None))
        h = getattr(a, "height", getattr(a, "h", None))
        if w is not None and h is not None:
            self._detail_size.setText(f"Taille: {w}x{h} pixels")
        else:
            self._detail_size.setText("Taille: N/A")
        self._detail_desc.setText(getattr(a, "description", ""))

        pixmap = self._load_thumbnail(aid, a)
        if pixmap:
            self._thumb_label.setPixmap(pixmap)
        else:
            self._thumb_label.setText("?")

    def _on_fav_toggle(self, item):
        aid = item.data(Qt.ItemDataRole.UserRole)
        if aid is None:
            return
        if aid in self._favs:
            self._favs.remove(aid)
        else:
            self._favs.insert(0, aid)
            self._favs = self._favs[:12]
        self.controller.ui_state.favs = list(self._favs)
        self._refresh_catalog()

    def refresh(self):
        self._refresh_catalog()
