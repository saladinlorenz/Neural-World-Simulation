"""ui_pygame — panneaux Pygame extraits du dashboard.

Chaque panneau respecte le contrat :
    draw(surface, rect, snapshot, ui_state) -> None
    handle_event(event, rect, ui_state) -> command dict ou None
"""
from .base_panel import Panel
from .journal_panel import JournalPanel
from .population_panel import PopulationPanel
from .society_panel import SocietyPanel

__all__ = ["Panel", "JournalPanel", "PopulationPanel", "SocietyPanel"]
