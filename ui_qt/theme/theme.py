"""Theme — tokens de style pour PyQt6 (clair + Neural Lab sombre)."""
from PyQt6.QtGui import QColor, QPalette, QFont
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtWidgets import QApplication


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

# Couleurs thème sombre classique. Le rendu sombre est desormais pris en
# charge par NEURAL_DARK (Lot A) ; ce dictionnaire reste publique pour les
# eventuels usages exterieurs qui l'importent encore.
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

# Palette Neural Lab (Lot A) — valeurs hex exactes du plan UX/UI.
NEURAL_DARK = {
    "app": "#0B0F14",
    "surface": "#121922",
    "surface2": "#19222D",
    "surface3": "#202B38",
    "border": "#2A394A",
    "border_soft": "#1D2835",
    "text": "#E7EDF5",
    "muted": "#91A0B2",
    "disabled": "#5C6878",
    "accent": "#4CC9F0",
    "accent_hover": "#74D9F5",
    "anima": "#A78BFA",
    "life": "#62D394",
    "warning": "#F6BD60",
    "danger": "#FF6B6B",
    "selection": "#F8E16C",
    "success": "#62D394",
    "focus": "#4CC9F0",
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
    # Lot A : Neural Lab (sombre) est le theme par defaut. Le theme clair
    # reste disponible via le bouton « Theme » de la barre d'outils.
    return s.value("theme", "sombre")


def set_theme_name(name):
    s = get_settings()
    s.setValue("theme", name)


def get_theme_background():
    """Couleur de fond d'une fenetre de premier plan sans parent.

    La feuille Neural Lab rend ``QWidget`` transparent ; un widget sans
    parent (ex. ``ComparisonPanel``) n'aurait alors aucun fond peint.
    On lui pose donc un fond explicite avec la couleur « app » du theme
    actif (regle a selectionneur d'identifiant, qui l'emporte sur
    ``QWidget``).
    """
    if get_theme_name() == "sombre":
        return NEURAL_DARK["app"]
    return _hex(LIGHT_COLORS["app"])


def _light_palette():
    """QPalette du theme clair (roles historiques)."""
    colors = LIGHT_COLORS
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
    return palette


def _neural_palette():
    """QPalette du theme Neural Lab (hex → QColor)."""
    c = NEURAL_DARK
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(c["app"]))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(c["text"]))
    palette.setColor(QPalette.ColorRole.Base, QColor(c["surface"]))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(c["surface2"]))
    palette.setColor(QPalette.ColorRole.Text, QColor(c["text"]))
    palette.setColor(QPalette.ColorRole.Button, QColor(c["surface2"]))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(c["text"]))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(c["accent"]))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(c["app"]))
    palette.setColor(QPalette.ColorRole.Mid, QColor(c["border"]))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(c["muted"]))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(c["surface2"]))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(c["text"]))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text,
                     QColor(c["disabled"]))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText,
                     QColor(c["disabled"]))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText,
                     QColor(c["disabled"]))
    return palette


def _classic_stylesheet(colors):
    """Feuille de style historique (clair), inchangee."""
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

    return f"""
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
    """


def neural_lab_stylesheet(c):
    """Feuille de style Neural Lab (Lot A).

    Reprend le stylesheet du plan et couvre TOUTES les regles du stylesheet
    classique (QToolTip, QSlider, QProgressBar, QSplitter, QComboBox popup,
    QListView, QDockWidget, QTableView, QLineEdit/QSpinBox, etats de
    QPushButton, QTabBar, barres de defilement...) avec la palette Neural.

    ``c`` est un dictionnaire de couleurs hex (NEURAL_DARK).
    """
    return f"""
    * {{
        font-family: "Segoe UI", "Inter", "Noto Sans", sans-serif;
        font-size: 13px;
        color: {c['text']};
    }}

    QWidget {{
        background: transparent;
    }}

    QMainWindow {{
        background: {c['app']};
    }}

    QMainWindow::separator {{
        background: {c['border']};
        width: 2px;
        height: 2px;
    }}

    QDialog {{
        background: {c['app']};
    }}

    QToolTip {{
        background: {c['surface2']};
        color: {c['text']};
        border: 1px solid {c['border']};
        padding: 6px 9px;
        border-radius: 6px;
        opacity: 235;
    }}

    QMenuBar {{
        background: {c['surface']};
        color: {c['text']};
        border-bottom: 1px solid {c['border_soft']};
    }}

    QMenuBar::item {{
        padding: 6px 10px;
        background: transparent;
    }}

    QMenuBar::item:selected {{
        background: {c['surface2']};
        border-radius: 5px;
    }}

    QMenuBar::item:disabled {{
        color: {c['disabled']};
    }}

    QMenu {{
        background: {c['surface2']};
        color: {c['text']};
        border: 1px solid {c['border']};
        border-radius: 7px;
        padding: 5px;
    }}

    QMenu::item {{
        padding: 7px 24px 7px 12px;
        border-radius: 5px;
        color: {c['text']};
    }}

    QMenu::item:selected {{
        background: #123D4A;
    }}

    QMenu::item:disabled {{
        color: {c['disabled']};
    }}

    QMenu::separator {{
        height: 1px;
        background: {c['border']};
        margin: 5px 10px;
    }}

    QTabWidget::pane {{
        border: none;
    }}

    QTabBar::tab {{
        background: transparent;
        color: {c['muted']};
        padding: 7px 14px;
        border: none;
        border-bottom: 2px solid transparent;
    }}

    QTabBar::tab:hover {{
        color: {c['text']};
    }}

    QTabBar::tab:selected {{
        color: {c['text']};
        border-bottom-color: {c['accent']};
    }}

    QGroupBox {{
        background: {c['surface']};
        color: {c['muted']};
        border: 1px solid {c['border_soft']};
        border-radius: 8px;
        margin-top: 12px;
        padding: 12px 8px 8px 8px;
        font-weight: 600;
    }}

    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 10px;
        padding: 0 6px;
        color: {c['muted']};
        font-weight: 600;
    }}

    QCheckBox, QRadioButton {{
        color: {c['text']};
        spacing: 8px;
    }}

    QSlider::groove:horizontal {{
        height: 4px;
        background: {c['border']};
        border-radius: 2px;
    }}

    QSlider::handle:horizontal {{
        width: 16px;
        height: 16px;
        margin: -6px 0;
        border-radius: 8px;
        background: {c['accent']};
    }}

    QSlider::handle:horizontal:hover {{
        background: {c['accent_hover']};
    }}

    QProgressBar {{
        border: 1px solid {c['border']};
        border-radius: 5px;
        background: {c['surface2']};
        color: {c['text']};
        text-align: center;
        min-height: 12px;
        max-height: 14px;
        font-size: 10px;
    }}

    QProgressBar::chunk {{
        background: {c['accent']};
        border-radius: 4px;
    }}

    QSplitter::handle {{
        background: transparent;
    }}

    QSplitter::handle:hover {{
        background: {c['surface3']};
    }}

    QToolButton, QPushButton {{
        background: {c['surface2']};
        border: 1px solid {c['border']};
        border-radius: 7px;
        padding: 6px 10px;
        min-height: 20px;
        color: {c['text']};
    }}

    QToolButton:hover, QPushButton:hover {{
        background: {c['surface3']};
        border-color: {c['accent']};
    }}

    QToolButton:pressed, QPushButton:pressed {{
        background: #0E4F63;
    }}

    QToolButton:checked, QPushButton:checked {{
        background: #123D4A;
        border-color: {c['accent']};
        color: {c['accent_hover']};
    }}

    QToolButton:disabled, QPushButton:disabled {{
        color: {c['disabled']};
        background: {c['surface2']};
    }}

    QPushButton:default {{
        background: {c['accent']};
        border-color: {c['accent']};
        color: {c['app']};
        font-weight: 600;
    }}

    QPushButton:default:hover {{
        background: {c['accent_hover']};
    }}

    QPushButton[role="primary"] {{
        background: #0C5268;
        border-color: {c['accent']};
        color: white;
        font-weight: 600;
    }}

    QPushButton[role="primary"]:hover {{
        background: {c['accent_hover']};
        color: white;
    }}

    QPushButton[role="danger"] {{
        background: #55282D;
        border-color: {c['danger']};
        color: #FFE9E9;
    }}

    QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
        background: {c['surface2']};
        border: 1px solid {c['border']};
        border-radius: 6px;
        padding: 5px 8px;
        selection-background-color: #12465A;
        selection-color: {c['text']};
        color: {c['text']};
    }}

    QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
        border-color: {c['focus']};
    }}

    QComboBox::drop-down {{
        border: none;
        width: 22px;
    }}

    QComboBox QAbstractItemView {{
        background: {c['surface2']};
        color: {c['text']};
        border: 1px solid {c['border']};
        selection-background-color: #123D4A;
        selection-color: {c['text']};
        outline: none;
        padding: 4px;
    }}

    QTableView, QTableWidget, QTreeWidget, QListWidget, QListView {{
        background: {c['surface']};
        border: 1px solid {c['border']};
        border-radius: 8px;
        gridline-color: {c['border_soft']};
        alternate-background-color: {c['surface2']};
        selection-background-color: #123D4A;
        selection-color: {c['text']};
        color: {c['text']};
    }}

    QTableView::item {{
        padding: 4px 8px;
    }}

    QHeaderView::section {{
        background: {c['surface2']};
        color: {c['muted']};
        border: none;
        border-bottom: 1px solid {c['border']};
        padding: 7px 8px;
        font-weight: 600;
    }}

    QListWidget::item {{
        padding: 4px 8px;
    }}

    QListWidget::item:selected {{
        background: #123D4A;
    }}

    QListWidget::item:hover {{
        background: {c['surface3']};
    }}

    QListView::item {{
        border-radius: 6px;
        padding: 4px;
    }}

    QListView::item:selected {{
        background: #123D4A;
    }}

    QListView::item:hover:!selected {{
        background: {c['surface3']};
    }}

    QDockWidget {{
        background: {c['surface']};
        border: 1px solid {c['border_soft']};
        font-weight: bold;
        color: {c['text']};
    }}

    QDockWidget::title {{
        background: {c['surface2']};
        color: {c['text']};
        padding: 8px 10px;
        font-weight: 600;
        border-bottom: 1px solid {c['border']};
    }}

    QDockWidget::close-button, QDockWidget::float-button {{
        border: none;
        border-radius: 4px;
        padding: 2px;
        background: transparent;
        min-height: 0;
        min-width: 0;
    }}

    QDockWidget::close-button:hover, QDockWidget::float-button:hover {{
        background: {c['surface3']};
    }}

    QToolBar {{
        background: {c['surface']};
        border: none;
        border-bottom: 1px solid {c['border']};
        spacing: 5px;
        padding: 5px 8px;
    }}

    QStatusBar {{
        background: {c['surface']};
        border-top: 1px solid {c['border']};
        color: {c['muted']};
        padding: 3px 8px;
    }}

    QStatusBar::item {{
        border: none;
    }}

    QStatusBar QLabel {{
        color: {c['muted']};
        background: transparent;
    }}

    QScrollBar:vertical {{
        width: 9px;
        background: transparent;
        margin: 2px;
    }}

    QScrollBar::handle:vertical {{
        background: {c['border']};
        border-radius: 4px;
        min-height: 30px;
    }}

    QScrollBar::handle:vertical:hover {{
        background: {c['muted']};
    }}

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    QScrollBar:horizontal {{
        height: 9px;
        background: transparent;
        margin: 2px;
    }}

    QScrollBar::handle:horizontal {{
        background: {c['border']};
        border-radius: 4px;
        min-width: 30px;
    }}

    QScrollBar::handle:horizontal:hover {{
        background: {c['muted']};
    }}

    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}

    QScrollBar::add-page, QScrollBar::sub-page {{
        background: transparent;
    }}

    QLabel {{
        color: {c['text']};
    }}

    QTextEdit, QPlainTextEdit {{
        background: {c['surface2']};
        color: {c['text']};
        border: 1px solid {c['border']};
        border-radius: 6px;
        selection-background-color: #12465A;
        selection-color: {c['text']};
    }}
    """


def apply_theme(app, theme_name=None):
    """Applique le theme au widget recu ET a la QApplication complete.

    Signature et API (``get_theme_name`` / ``set_theme_name``) conservees :
    le bouton « Theme » de la barre d'outils reste fonctionnel. La feuille
    de style est aussi posee sur ``QApplication`` pour que les dialogues
    sans parent (ex. ComparisonPanel) heritent du thème Neural Lab.
    """
    if theme_name is None:
        theme_name = get_theme_name()

    if theme_name == "sombre":
        palette = _neural_palette()
        sheet = neural_lab_stylesheet(NEURAL_DARK)
    else:
        palette = _light_palette()
        sheet = _classic_stylesheet(LIGHT_COLORS)

    font = QFont("Segoe UI", 13)
    font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)

    app.setPalette(palette)
    app.setFont(font)
    app.setStyleSheet(sheet)

    app_qt = QApplication.instance()
    if app_qt is not None:
        app_qt.setPalette(palette)
        app_qt.setFont(font)
        app_qt.setStyleSheet(sheet)
