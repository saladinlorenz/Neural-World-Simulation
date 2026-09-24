"""Theme — tokens de style pour PyQt6 (clair + sombre)."""
from PyQt6.QtGui import QColor, QPalette, QFont
from PyQt6.QtCore import Qt, QSettings


# Couleurs thème clair
LIGHT_COLORS = {
    "app": (238, 240, 244),
    "rail": (246, 247, 249),
    "surface": (255, 255, 255),
    "surface_2": (250, 251, 253),
    "hover": (241, 244, 249),
    "select": (232, 240, 253),
    "border": (226, 229, 235),
    "border_2": (205, 210, 219),
    "text": (31, 36, 48),
    "muted": (105, 114, 129),
    "faint": (156, 163, 176),
    "accent": (59, 118, 214),
    "danger": (214, 84, 84),
    "warn": (222, 160, 50),
}

# Couleurs thème sombre
DARK_COLORS = {
    "app": (30, 33, 40),
    "rail": (37, 40, 48),
    "surface": (37, 40, 48),
    "surface_2": (44, 48, 56),
    "hover": (50, 54, 64),
    "select": (40, 50, 72),
    "border": (55, 60, 72),
    "border_2": (65, 70, 82),
    "text": (220, 224, 232),
    "muted": (140, 148, 168),
    "faint": (100, 108, 128),
    "accent": (80, 140, 230),
    "danger": (230, 100, 100),
    "warn": (230, 180, 70),
}

# Accents par famille
FAMILY_COLORS = {
    "corps": (67, 160, 92),
    "cog": (62, 124, 214),
    "perso": (222, 164, 46),
    "emo": (34, 158, 142),
    "besoin": (146, 96, 186),
    "exp": (206, 126, 60),
}

# Alias pour compatibilité
COLORS = LIGHT_COLORS


def _rgb(t):
    return QColor(t[0], t[1], t[2])


def _hex(t):
    return f"#{t[0]:02x}{t[1]:02x}{t[2]:02x}"


def _mix(c1, c2, t):
    return tuple(round(a + (b - a) * t) for a, b in zip(c1, c2))


def get_settings():
    return QSettings("UniversVivant", "UniversVivant")


def get_theme_name():
    s = get_settings()
    return s.value("theme", "clair")


def set_theme_name(name):
    s = get_settings()
    s.setValue("theme", name)


def apply_theme(app, theme_name=None):
    """Applique le thème à QApplication."""
    if theme_name is None:
        theme_name = get_theme_name()
    colors = DARK_COLORS if theme_name == "sombre" else LIGHT_COLORS

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, _rgb(colors["app"]))
    palette.setColor(QPalette.ColorRole.WindowText, _rgb(colors["text"]))
    palette.setColor(QPalette.ColorRole.Base, _rgb(colors["surface"]))
    palette.setColor(QPalette.ColorRole.Text, _rgb(colors["text"]))
    palette.setColor(QPalette.ColorRole.Button, _rgb(colors["surface"]))
    palette.setColor(QPalette.ColorRole.ButtonText, _rgb(colors["text"]))
    palette.setColor(QPalette.ColorRole.Highlight, _rgb(colors["accent"]))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.Mid, _rgb(colors["border"]))
    app.setPalette(palette)

    font = QFont("Segoe UI", 13)
    font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
    app.setFont(font)

    bg = _hex(colors["surface"])
    bg2 = _hex(colors["surface_2"])
    app_bg = _hex(colors["app"])
    border = _hex(colors["border"])
    border2 = _hex(colors["border_2"])
    text = _hex(colors["text"])
    muted = _hex(colors["muted"])
    faint = _hex(colors["faint"])
    accent = _hex(colors["accent"])
    hover_bg = _hex(colors["hover"])
    select_bg = _hex(colors["select"])
    accent_hover = _hex(_mix(colors["accent"], (255, 255, 255), 0.18))

    app.setStyleSheet(f"""
        QMainWindow::separator {{
            background: {border};
            width: 2px;
            height: 2px;
        }}
        QToolTip {{
            background: {bg2};
            color: {text};
            border: 1px solid {border2};
            padding: 6px 9px;
            border-radius: 6px;
            opacity: 235;
        }}
        QMenu {{
            background: {bg};
            color: {text};
            border: 1px solid {border};
            border-radius: 8px;
            padding: 6px;
        }}
        QMenu::item {{
            padding: 6px 28px 6px 28px;
            border-radius: 5px;
        }}
        QMenu::item:selected {{
            background: {select_bg};
        }}
        QMenu::item:disabled {{
            color: {faint};
        }}
        QMenu::separator {{
            height: 1px;
            background: {border};
            margin: 5px 10px;
        }}
        QTabWidget::pane {{
            border: none;
        }}
        QTabBar::tab {{
            background: transparent;
            color: {muted};
            padding: 7px 14px;
            border: none;
            border-bottom: 2px solid transparent;
        }}
        QTabBar::tab:hover {{
            color: {text};
        }}
        QTabBar::tab:selected {{
            color: {text};
            border-bottom-color: {accent};
        }}
        QGroupBox {{
            color: {muted};
            border: 1px solid {border};
            border-radius: 8px;
            margin-top: 14px;
            padding-top: 10px;
            font-weight: bold;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 10px;
            padding: 0 4px;
        }}
        QCheckBox, QRadioButton {{
            color: {text};
            spacing: 8px;
        }}
        QSlider::groove:horizontal {{
            height: 4px;
            background: {border};
            border-radius: 2px;
        }}
        QSlider::handle:horizontal {{
            width: 16px;
            height: 16px;
            margin: -6px 0;
            border-radius: 8px;
            background: {accent};
        }}
        QSlider::handle:horizontal:hover {{
            background: {accent_hover};
        }}
        QProgressBar {{
            border: 1px solid {border};
            border-radius: 5px;
            background: {bg2};
            color: {text};
            text-align: center;
            min-height: 12px;
            max-height: 14px;
            font-size: 10px;
        }}
        QProgressBar::chunk {{
            background: {accent};
            border-radius: 4px;
        }}
        QSplitter::handle {{
            background: transparent;
        }}
        QSplitter::handle:hover {{
            background: {select_bg};
        }}
        QComboBox::drop-down {{
            border: none;
            width: 22px;
        }}
        QComboBox QAbstractItemView {{
            background: {bg};
            color: {text};
            border: 1px solid {border2};
            selection-background-color: {select_bg};
            selection-color: {text};
            outline: none;
            padding: 4px;
        }}
        QDialog {{
            background: {app_bg};
        }}
        QStatusBar::item {{
            border: none;
        }}
        QStatusBar QLabel {{
            color: {muted};
            background: transparent;
        }}
        QDockWidget {{
            font-weight: bold;
            color: {text};
        }}
        QDockWidget::title {{
            background: {bg2};
            padding: 6px;
            border-bottom: 1px solid {border};
        }}
        QTableView {{
            border: 1px solid {border};
            border-radius: 6px;
            gridline-color: {border2};
            selection-background-color: {select_bg};
            selection-color: {text};
            background: {bg};
            color: {text};
        }}
        QTableView::item {{
            padding: 4px 8px;
        }}
        QHeaderView::section {{
            background: {bg2};
            border: none;
            border-bottom: 1px solid {border};
            padding: 4px 8px;
            font-weight: bold;
            color: {muted};
        }}
        QToolBar {{
            border: none;
            spacing: 4px;
            background: {bg};
        }}
        QToolBar QToolButton {{
            border: 1px solid {border};
            border-radius: 6px;
            padding: 4px 10px;
            background: {bg};
            color: {text};
        }}
        QToolBar QToolButton:hover {{
            background: {hover_bg};
        }}
        QToolBar QToolButton:checked {{
            background: {select_bg};
            border-color: {accent};
        }}
        QScrollBar:vertical {{
            width: 8px;
            background: transparent;
        }}
        QScrollBar::handle:vertical {{
            background: {border2};
            border-radius: 4px;
            min-height: 32px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {faint};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0;
        }}
        QScrollBar:horizontal {{
            height: 8px;
            background: transparent;
        }}
        QScrollBar::handle:horizontal {{
            background: {border2};
            border-radius: 4px;
            min-width: 32px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background: {faint};
        }}
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0;
        }}
        QScrollBar::add-page, QScrollBar::sub-page {{
            background: transparent;
        }}
        QLineEdit {{
            border: 1px solid {border2};
            border-radius: 6px;
            padding: 4px 8px;
            background: {bg};
            color: {text};
        }}
        QLineEdit:focus {{
            border-color: {accent};
        }}
        QComboBox {{
            border: 1px solid {border2};
            border-radius: 6px;
            padding: 4px 8px;
            background: {bg};
            color: {text};
        }}
        QSpinBox {{
            border: 1px solid {border2};
            border-radius: 6px;
            padding: 4px 8px;
            background: {bg};
            color: {text};
        }}
        QPushButton {{
            border: 1px solid {border};
            border-radius: 6px;
            padding: 4px 10px;
            background: {bg};
            color: {text};
        }}
        QPushButton:hover {{
            background: {hover_bg};
        }}
        QPushButton:checked {{
            background: {select_bg};
            border-color: {accent};
        }}
        QPushButton:default {{
            background: {accent};
            border-color: {accent};
            color: white;
            font-weight: bold;
        }}
        QPushButton:default:hover {{
            background: {accent_hover};
        }}
        QPushButton:disabled {{
            color: {faint};
            background: {bg2};
        }}
        QLabel {{
            color: {text};
        }}
        QStatusBar {{
            background: {bg2};
            color: {muted};
        }}
        QListWidget {{
            border: 1px solid {border};
            border-radius: 6px;
            background: {bg};
            color: {text};
        }}
        QListWidget::item {{
            padding: 4px 8px;
        }}
        QListWidget::item:selected {{
            background: {select_bg};
        }}
        QListWidget::item:hover {{
            background: {hover_bg};
        }}
        QListView {{
            border: 1px solid {border};
            border-radius: 6px;
            background: {bg};
            color: {text};
        }}
        QListView::item {{
            border-radius: 6px;
            padding: 4px;
        }}
        QListView::item:selected {{
            background: {select_bg};
        }}
        QListView::item:hover:!selected {{
            background: {hover_bg};
        }}
        QDockWidget::close-button, QDockWidget::float-button {{
            border: none;
            border-radius: 4px;
            padding: 2px;
        }}
        QDockWidget::close-button:hover, QDockWidget::float-button:hover {{
            background: {hover_bg};
        }}
    """)
