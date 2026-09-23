"""SaveDialog — dialogue de sauvegarde/chargement Qt."""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QListWidget,
                              QListWidgetItem, QPushButton, QLabel, QMessageBox)
from PyQt6.QtCore import Qt
import os
import time


class SaveDialog(QDialog):
    """Dialogue de sauvegarde/chargement avec liste des slots."""

    def __init__(self, controller, mode="save", parent=None):
        super().__init__(parent)
        self.controller = controller
        self.mode = mode
        self.selected_slot = 0
        self.setWindowTitle("Sauvegarder" if mode == "save" else "Charger")
        self.setMinimumSize(400, 300)
        self._setup_ui()
        self._load_slots()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Choisir un slot :" if self.mode == "save"
                        else "Choisir une sauvegarde :")
        layout.addWidget(title)

        self._list = QListWidget()
        self._list.itemClicked.connect(self._on_select)
        layout.addWidget(self._list)

        btn_layout = QHBoxLayout()
        self._save_btn = QPushButton("Sauvegarder" if self.mode == "save" else "Charger")
        self._save_btn.clicked.connect(self._on_accept)
        self._save_btn.setEnabled(False)
        btn_layout.addWidget(self._save_btn)

        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

    def _load_slots(self):
        saves_dir = os.path.join(os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))), "data", "saves")
        self._list.clear()
        for slot in range(10):
            path = os.path.join(saves_dir, f"slot_{slot}.pkl")
            if os.path.exists(path):
                mtime = os.path.getmtime(path)
                date_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(mtime))
                size_kb = os.path.getsize(path) / 1024
                item = QListWidgetItem(f"Slot {slot} — {date_str} ({size_kb:.0f} KB)")
            else:
                item = QListWidgetItem(f"Slot {slot} — vide")
            item.setData(Qt.ItemDataRole.UserRole, slot)
            self._list.addItem(item)

        # Slots spéciaux
        for slot, label in [(98, "Backup automatique"), (99, "Backup manuel")]:
            path = os.path.join(saves_dir, f"slot_{slot}.pkl")
            if os.path.exists(path):
                mtime = os.path.getmtime(path)
                date_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(mtime))
                item = QListWidgetItem(f"{label} — {date_str}")
                item.setData(Qt.ItemDataRole.UserRole, slot)
                self._list.addItem(item)

    def _on_select(self, item):
        self.selected_slot = item.data(Qt.ItemDataRole.UserRole)
        self._save_btn.setEnabled(True)

    def _on_accept(self):
        if self.mode == "save":
            result = self.controller.execute({
                "kind": "save", "slot": self.selected_slot, "cam": self.controller.camera
            })
        else:
            result = self.controller.execute({
                "kind": "load", "slot": self.selected_slot
            })

        if result.get("ok"):
            self.accept()
        else:
            QMessageBox.warning(self, "Erreur", result.get("error", "Erreur inconnue"))
