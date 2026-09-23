"""Conversions PIL / NumPy -> QImage / QPixmap.

Source unique partagée par la carte, les docks et les vignettes : la
conversion doit inclure ``.copy()``, car le tampon ``raw`` produit par
``tobytes`` est temporaire et serait libéré avant le rendu.
"""
from __future__ import annotations

from PyQt6.QtGui import QImage, QPixmap


def pil_to_qimage(image) -> QImage:
    """Convertit une image PIL (n'importe quel mode) en QImage RGBA8888."""
    rgba = image.convert("RGBA")
    raw = rgba.tobytes("raw", "RGBA")
    qimage = QImage(
        raw,
        rgba.width,
        rgba.height,
        rgba.width * 4,
        QImage.Format.Format_RGBA8888,
    )
    return qimage.copy()


def pil_to_pixmap(image) -> QPixmap:
    return QPixmap.fromImage(pil_to_qimage(image))


def rgb_to_qimage(rgb) -> QImage:
    """Convertit un tableau NumPy ``(H, W, 3)`` uint8 en QImage RGB888."""
    import numpy as np

    rgb = np.ascontiguousarray(rgb, dtype=np.uint8)
    height, width, channels = rgb.shape
    if channels != 3:
        raise ValueError("RGB attendu sous la forme H,W,3")

    qimage = QImage(
        rgb.data,
        width,
        height,
        width * 3,
        QImage.Format.Format_RGB888,
    )
    return qimage.copy()
