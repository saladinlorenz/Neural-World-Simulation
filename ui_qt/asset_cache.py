"""QtAssetCache — cache de QPixmap pour les sprites du moteur.

``AssetManager`` fournit déjà un LRU d'images PIL (``_surf_cache``, 2600
entrées). Ce cache ajoute l'étape suivante : la conversion en QPixmap,
coûteuse et refaite à chaque frame sans lui.

Décision clé : **l'échelle ne fait pas partie de la clé**. Le zoom est un
flottant continu (0,08 – 4,0) ; une clé ``(aid, frame, scale)`` viderait le
cache à chaque cran de molette. On met en cache le pixmap natif et on laisse
``QPainter`` le redimensionner au blit.
"""
from __future__ import annotations

from collections import OrderedDict

from PyQt6.QtGui import QPixmap

from ui_qt.qtimage import pil_to_pixmap


class QtAssetCache:
    """LRU de QPixmap indexé par ``(aid, frame)``."""

    def __init__(self, max_entries: int = 1500):
        self._cache: "OrderedDict[tuple, QPixmap]" = OrderedDict()
        self._max = max(16, int(max_entries))
        self._shadow: QPixmap | None = None

    # ------------------------------------------------------------------ accès

    def pixmap(self, am, aid: int, frame: int = 0) -> QPixmap | None:
        """Pixmap natif d'un asset. ``None`` si l'aid est invalide."""
        try:
            aid = int(aid)
        except (TypeError, ValueError):
            return None
        if not (0 <= aid < len(am.assets)):
            return None

        frame = max(0, int(frame))
        key = (aid, frame)
        hit = self._cache.get(key)
        if hit is not None:
            self._cache.move_to_end(key)
            return hit

        asset = am.assets[aid]
        frames = max(1, int(getattr(asset, "frames", 1) or 1))
        try:
            image = am.surface(aid, frame % frames, 1.0)
        except Exception:
            return None
        if image is None:
            return None

        pixmap = pil_to_pixmap(image)
        self._cache[key] = pixmap
        if len(self._cache) > self._max:
            self._cache.popitem(last=False)
        return pixmap

    def pixmap_from_pil(self, image) -> QPixmap | None:
        """Conversion hors cache, pour les portraits et vignettes."""
        if image is None:
            return None
        try:
            return pil_to_pixmap(image)
        except Exception:
            return None

    def shadow(self, am) -> QPixmap | None:
        """Pixmap d'ombre unique, réutilisé mis à l'échelle sous chaque sprite."""
        if self._shadow is not None:
            return self._shadow
        aid = getattr(am, "shadow", None)
        if aid is None:
            return None
        self._shadow = self.pixmap(am, aid, 0)
        return self._shadow

    # ------------------------------------------------------------------ cycle

    def clear(self) -> None:
        """À appeler après un chargement : les ``aid`` sont positionnels."""
        self._cache.clear()
        self._shadow = None

    def __len__(self) -> int:
        return len(self._cache)
