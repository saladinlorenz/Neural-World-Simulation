"""Journal d'erreurs techniques — remplace les except Exception: pass.

Les erreurs critiques sont visibles dans stderr ET dans le fichier de log
data/logs/univers_vivant.log, sans arrêter la simulation.
"""
from __future__ import annotations

import logging
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "data" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "univers_vivant.log"

logger = logging.getLogger("univers_vivant")
logger.setLevel(logging.INFO)

if not logger.handlers:
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def report_error(context: str, exc: Exception, sim=None):
    """Log une erreur technique sans arrêter la simulation."""
    message = f"{context}: {type(exc).__name__}: {exc}"
    logger.exception(message)
    print(f"[ERROR] {message}")
    if sim is not None:
        try:
            sim.log(f"Erreur technique [{context}] : {type(exc).__name__}",
                    (214, 84, 84), "monde")
        except Exception:
            pass
