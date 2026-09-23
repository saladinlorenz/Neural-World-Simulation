"""ToolEditorDialog — éditeur d'outil pixel 16x16 (Lot D.2).

Reprend la logique de l'ancien ``game/tool_editor.py`` Pygame : grille
16x16, palette 8 couleurs, gomme, aperçu, enregistrement PNG dans
``assets/tools_custom/`` — désormais via la commande ``create_tool``.
"""
from __future__ import annotations

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QColor, QImage, QPainter, QPen, QPixmap
from PyQt6.QtWidgets import (QComboBox, QDialog, QFormLayout, QGridLayout,
                              QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                              QMessageBox, QPushButton, QVBoxLayout, QWidget)

from game.config import TOOL_RECIPES

GRID_SIZE = 16
CELL_PX = 18
PALETTE = [
    (60, 60, 66), (120, 90, 60), (150, 150, 156), (200, 170, 90),
    (90, 140, 90), (140, 90, 160), (200, 90, 90), (230, 230, 230),
]
EMPTY_BG = QColor(30, 32, 40)


class PixelCanvas(QWidget):
    """Grille 16x16 peinte à la souris ; bouton droit = gomme."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixels = [None] * (GRID_SIZE * GRID_SIZE)
        self.current_color = PALETTE[0]
        self.erasing = False
        self._dragging = False
        self.setFixedSize(GRID_SIZE * CELL_PX, GRID_SIZE * CELL_PX)
        self.setMouseTracking(True)

    def clear(self):
        self.pixels = [None] * (GRID_SIZE * GRID_SIZE)
        self.update()

    def _cell(self, pos: QPoint):
        col, row = pos.x() // CELL_PX, pos.y() // CELL_PX
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            return row * GRID_SIZE + col
        return None

    def paint_at(self, pos: QPoint, erase=False):
        index = self._cell(pos)
        if index is None:
            return
        self.pixels[index] = None if erase else (*self.current_color, 255)
        self.update()

    def mousePressEvent(self, event):
        self._dragging = True
        self.paint_at(event.position().toPoint(),
                      erase=self.erasing
                      or event.button() == Qt.MouseButton.RightButton)

    def mouseMoveEvent(self, event):
        if self._dragging:
            self.paint_at(event.position().toPoint(),
                          erase=self.erasing or bool(
                              event.buttons() & Qt.MouseButton.RightButton))

    def mouseReleaseEvent(self, event):
        self._dragging = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(18, 20, 26))
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                pixel = self.pixels[row * GRID_SIZE + col]
                color = QColor(*pixel[:3]) if pixel else EMPTY_BG
                painter.fillRect(col * CELL_PX, row * CELL_PX,
                                 CELL_PX - 1, CELL_PX - 1, color)
        painter.setPen(QPen(QColor(255, 255, 255, 40), 1))
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)
        painter.end()

    def image(self) -> QImage:
        image = QImage(GRID_SIZE, GRID_SIZE, QImage.Format.Format_RGBA8888)
        image.fill(QColor(0, 0, 0, 0))
        for index, pixel in enumerate(self.pixels):
            if pixel:
                image.setPixel(index % GRID_SIZE, index // GRID_SIZE,
                               QColor(*pixel[:3], pixel[3]).rgba())
        return image


class ToolEditorDialog(QDialog):
    """Dessine un outil, l'enregistre et l'enregistre au catalogue."""

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Éditeur d'outil")
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)

        left = QVBoxLayout()
        self._canvas = PixelCanvas(self)
        left.addWidget(self._canvas)

        palette = QHBoxLayout()
        self._palette_buttons = []
        for color in PALETTE:
            button = QPushButton()
            button.setFixedSize(26, 26)
            button.setStyleSheet(
                "background-color: rgb(%d,%d,%d); border-radius: 4px;"
                % color)
            button.clicked.connect(
                lambda checked, c=color, b=button: self._pick_color(c, b))
            palette.addWidget(button)
            self._palette_buttons.append(button)
        erase = QPushButton("Gomme")
        erase.setFixedSize(52, 26)
        erase.setToolTip("Bouton droit sur la grille = gomme aussi")
        erase.clicked.connect(lambda: self._pick_color(None, erase))
        palette.addWidget(erase)
        self._palette_buttons.append(erase)
        palette.addStretch(1)
        left.addLayout(palette)
        self._pick_color(PALETTE[0], self._palette_buttons[0])

        clear_btn = QPushButton("Tout effacer")
        clear_btn.clicked.connect(self._canvas.clear)
        left.addWidget(clear_btn)
        layout.addLayout(left)

        right = QVBoxLayout()
        form = QGroupBox("Outil")
        form_layout = QFormLayout(form)
        self._name = QLineEdit("mon_outil")
        self._name.setMaxLength(32)
        form_layout.addRow("Nom", self._name)
        self._kind = QComboBox()
        self._kind.addItems(sorted(TOOL_RECIPES))
        form_layout.addRow("Type", self._kind)
        right.addWidget(form)

        preview_box = QGroupBox("Aperçu")
        preview_layout = QVBoxLayout(preview_box)
        self._preview = QLabel()
        self._preview.setFixedSize(96, 96)
        self._preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.addWidget(self._preview)
        right.addWidget(preview_box)

        right.addStretch(1)
        save_btn = QPushButton("Enregistrer l'outil")
        save_btn.clicked.connect(self._on_save)
        right.addWidget(save_btn)
        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(self.reject)
        right.addWidget(cancel_btn)
        layout.addLayout(right)

        self._canvas.update.connect if False else None
        self._canvas.installEventFilter(self)

    def _pick_color(self, color, button):
        self._canvas.current_color = color
        if color is None:
            self._canvas.current_color = PALETTE[0]
            self._erase_mode = True
        else:
            self._erase_mode = False
        for candidate in self._palette_buttons:
            candidate.setStyleSheet(candidate.styleSheet().replace(
                "border: 2px solid white;", ""))
        button.setStyleSheet(button.styleSheet() + " border: 2px solid white;")

    def eventFilter(self, obj, event):
        if obj is self._canvas and event.type() in (
                event.Type.Paint, event.Type.MouseButtonRelease):
            self._refresh_preview()
        return super().eventFilter(obj, event)

    def _refresh_preview(self):
        pixmap = QPixmap.fromImage(self._canvas.image()).scaled(
            96, 96, Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.FastTransformation)
        self._preview.setPixmap(pixmap)

    def _on_save(self):
        pixels = [pixel or (0, 0, 0, 0) for pixel in self._canvas.pixels]
        if not any(pixel[3] for pixel in pixels):
            QMessageBox.warning(self, "Outil vide",
                                "Dessinez au moins un pixel avant d'enregistrer.")
            return
        result = self.controller.execute({
            "kind": "create_tool",
            "pixels": [list(pixel) for pixel in pixels],
            "name": self._name.text().strip() or "outil",
            "tool_kind": self._kind.currentText(),
        })
        if not result.get("ok"):
            QMessageBox.warning(self, "Erreur",
                                result.get("error", "Erreur inconnue"))
            return
        self.created_aid = result.get("aid")
        self.created_path = result.get("path")
        self.accept()
