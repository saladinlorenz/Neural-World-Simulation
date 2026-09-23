"""WorldHistory — undo/redo des outils monde (Lot D.5).

Un enregistrement = une boîte englobante + les tranches NumPy des tableaux
touchés, capturées AVANT mutation, + une copie des listes/dicts d'entités
(``items``, ``cemetery``, ``sites``, ``storages``, ``crop_plots``).

Un glisser de pinceau produit UNE seule entrée : ``begin`` ouvre un
enregistrement pendu, ``extend`` l'agrandit (les cellules déjà couvertes
gardent leur valeur d'origine grâce au masque), ``commit`` le pousse. Les
clics isolés (``group=None``) committent immédiatement.

Mémoire : les tranches gardent leur dtype d'origine ; la pile est bornée à
``max_entries`` enregistrements.
"""
from __future__ import annotations

import numpy as np

#: Tableaux monde capturés par chaque entrée d'historique.
HISTORY_ARRAYS = (
    "content", "owner", "blocked", "shelter", "hp", "floor",
    "land", "water", "mountains", "foundation", "roof", "regrow",
)

#: Listes / dicts d'entités restaurés tels quels (peu nombreux, copies légères).
HISTORY_LISTS = ("items", "cemetery")
HISTORY_DICTS = ("sites", "storages", "crop_plots")


def _clip_box(world, box):
    g = int(world.g)
    x0, y0, x1, y1 = (int(v) for v in box)
    x0, y0 = max(0, x0), max(0, y0)
    x1, y1 = min(g, x1), min(g, y1)
    if x1 <= x0 or y1 <= y0:
        return None
    return x0, y0, x1, y1


class _Entry:
    __slots__ = ("box", "mask", "before", "lists", "dicts")

    def __init__(self, box):
        self.box = box
        x0, y0, x1, y1 = box
        self.mask = np.zeros((y1 - y0, x1 - x0), dtype=bool)
        self.before: dict[str, np.ndarray] = {}
        self.lists: dict[str, list] = {}
        self.dicts: dict[str, dict] = {}


class WorldHistory:
    def __init__(self, max_entries: int = 50):
        self._max = max(1, int(max_entries))
        self._undo: list[_Entry] = []
        self._redo: list[_Entry] = []
        self._pending: _Entry | None = None
        self.pending_group = None

    # ------------------------------------------------------------------ état

    def has_pending(self) -> bool:
        return self._pending is not None

    def can_undo(self) -> bool:
        return bool(self._undo) or self._pending is not None

    def can_redo(self) -> bool:
        return bool(self._redo)

    def clear(self) -> None:
        self._undo.clear()
        self._redo.clear()
        self._pending = None
        self.pending_group = None

    # ------------------------------------------------------------------ capture

    def _capture_lists(self, world, entry: _Entry):
        for name in HISTORY_LISTS:
            value = getattr(world, name, None)
            if isinstance(value, list):
                entry.lists[name] = list(value)
        for name in HISTORY_DICTS:
            value = getattr(world, name, None)
            if isinstance(value, dict):
                entry.dicts[name] = dict(value)

    def _capture_region(self, world, entry: _Entry, box) -> None:
        """Copie l'état actuel des cellules de ``box`` non encore couvertes."""
        x0, y0, x1, y1 = entry.box
        nx0, ny0, nx1, ny1 = box
        oy, ox = ny0 - y0, nx0 - x0
        region = entry.mask[oy:oy + ny1 - ny0, ox:ox + nx1 - nx0]
        for name in HISTORY_ARRAYS:
            array = getattr(world, name, None)
            if array is None:
                continue
            stored = entry.before.get(name)
            if stored is None:
                stored = np.zeros((y1 - y0, x1 - x0), dtype=array.dtype)
                entry.before[name] = stored
            target = stored[oy:oy + ny1 - ny0, ox:ox + nx1 - nx0]
            current = array[ny0:ny1, nx0:nx1]
            target[~region] = current[~region]

    def begin(self, world, box, group=None) -> None:
        clipped = _clip_box(world, box)
        if clipped is None:
            return
        if self._pending is not None and group is not None \
                and group == self.pending_group:
            self.extend(world, clipped)
            return
        if self._pending is not None:
            self.commit()
        entry = _Entry(clipped)
        self._capture_region(world, entry, clipped)
        entry.mask[...] = True
        self._capture_lists(world, entry)
        self._pending = entry
        self.pending_group = group

    def extend(self, world, box) -> None:
        entry = self._pending
        if entry is None:
            self.begin(world, box)
            return
        clipped = _clip_box(world, box)
        if clipped is None:
            return
        x0, y0, x1, y1 = entry.box
        nx0, ny0, nx1, ny1 = clipped
        ux0, uy0 = min(x0, nx0), min(y0, ny0)
        ux1, uy1 = max(x1, nx1), max(y1, ny1)
        if (ux0, uy0, ux1, uy1) != (x0, y0, x1, y1):
            new_mask = np.zeros((uy1 - uy0, ux1 - ux0), dtype=bool)
            new_mask[y0 - uy0:y1 - uy0, x0 - ux0:x1 - ux0] = entry.mask
            entry.mask = new_mask
            for name, stored in entry.before.items():
                grown = np.zeros((uy1 - uy0, ux1 - ux0), dtype=stored.dtype)
                grown[y0 - uy0:y1 - uy0, x0 - ux0:x1 - ux0] = stored
                entry.before[name] = grown
            entry.box = (ux0, uy0, ux1, uy1)
        self._capture_region(world, entry, clipped)
        entry.mask[ny0 - uy0:ny1 - uy0, nx0 - ux0:nx1 - ux0] = True

    def discard(self) -> None:
        self._pending = None
        self.pending_group = None

    def commit(self) -> bool:
        if self._pending is None:
            return False
        self._undo.append(self._pending)
        del self._undo[:-self._max]
        self._pending = None
        self.pending_group = None
        self._redo.clear()
        return True

    # ------------------------------------------------------------------ application

    @staticmethod
    def _apply(world, entry: _Entry) -> None:
        x0, y0, x1, y1 = entry.box
        for name, stored in entry.before.items():
            array = getattr(world, name, None)
            if array is None or array.shape[0] < y1 or array.shape[1] < x1:
                continue
            array[y0:y1, x0:x1][entry.mask] = stored[entry.mask]
        for name, value in entry.lists.items():
            setattr(world, name, list(value))
        for name, value in entry.dicts.items():
            setattr(world, name, dict(value))
        world.mark_dirty(x0, y0)

    def _snapshot_entry(self, world, entry: _Entry) -> _Entry:
        """Entrée miroir portant l'état ACTUEL de la boîte (pour redo/undo)."""
        mirror = _Entry(entry.box)
        x0, y0, x1, y1 = entry.box
        for name in HISTORY_ARRAYS:
            array = getattr(world, name, None)
            if array is not None:
                mirror.before[name] = array[y0:y1, x0:x1].copy()
        mirror.mask[...] = True
        self._capture_lists(world, mirror)
        return mirror

    def undo(self, world) -> bool:
        if self._pending is not None:
            self.commit()
        if not self._undo:
            return False
        entry = self._undo.pop()
        self._redo.append(self._snapshot_entry(world, entry))
        del self._redo[:-self._max]
        self._apply(world, entry)
        return True

    def redo(self, world) -> bool:
        if not self._redo:
            return False
        entry = self._redo.pop()
        self._undo.append(self._snapshot_entry(world, entry))
        del self._undo[:-self._max]
        self._apply(world, entry)
        return True
