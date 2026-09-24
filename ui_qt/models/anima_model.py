from PyQt6.QtCore import QAbstractTableModel, Qt
from PyQt6.QtGui import QColor, QFont

_SECTION_BG = QColor(40, 50, 70)
_SECTION_FG = QColor(160, 200, 240)


def _fmt(v):
    if isinstance(v, bool):
        return "Oui" if v else "Non"
    if isinstance(v, float):
        return f"{v:.2f}"
    return str(v) if v is not None else ""


class AnimaModel(QAbstractTableModel):
    HEADERS = ["Attribut", "Valeur"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self._rows = []

    def set_snapshot(self, agent_snap):
        self.beginResetModel()
        self._rows = []
        if agent_snap is None:
            self.endResetModel()
            return

        anima = agent_snap.get("anima", {})

        self._rows.append({"type": "section", "label": "BASE"})
        self._data("Nom", agent_snap.get("name", ""))
        self._data("Sexe", agent_snap.get("sex", ""))
        self._data("Classe", agent_snap.get("class", ""))
        self._data("Clan", agent_snap.get("clan", ""))
        self._data("Generation", agent_snap.get("generation", 0))
        self._data("Age", agent_snap.get("age_years", 0))
        self._data("Stage", agent_snap.get("stage", ""))
        needs = agent_snap.get("needs_named", {}) or {}
        self._data("Sante", agent_snap.get("health", 0))
        self._data("Energie", needs.get("énergie", 0))
        self._data("Faim", needs.get("faim", 0))
        pos = agent_snap.get("position", {})
        if pos:
            self._data("Position", f"({pos.get('tx', 0)}, {pos.get('ty', 0)})")
        goal = agent_snap.get("goal", {})
        self._data("But", goal.get("action_name", "") or "")
        brain = agent_snap.get("brain", {})
        if brain:
            self._data("Neurones", brain.get("neurons", 0))
            self._data("Frequence reflexion", brain.get("think_frequency", 0))

        self._rows.append({"type": "section", "label": "ANIMA"})

        identity = anima.get("identity", {})
        if identity:
            self._rows.append({"type": "sub", "label": "Identite"})
            for k, v in sorted(identity.items(), key=lambda x: -x[1]):
                self._data(f"  {k}", v)

        values = anima.get("values", {})
        if values:
            self._rows.append({"type": "sub", "label": "Valeurs"})
            for k, v in sorted(values.items(), key=lambda x: -x[1]):
                self._data(f"  {k}", v)

        trauma = anima.get("trauma", {})
        if trauma:
            self._rows.append({"type": "sub", "label": "Trauma"})
            for k, v in trauma.items():
                self._data(f"  {k}", v)

        intention = anima.get("intention")
        if intention:
            self._rows.append({"type": "sub", "label": "Intention"})
            for k, v in intention.items():
                self._data(f"  {k}", v)

        plan = anima.get("plan")
        if plan:
            self._rows.append({"type": "sub", "label": "Plan"})
            for k, v in plan.items():
                self._data(f"  {k}", v)

        attachments = anima.get("attachments", {})
        if attachments:
            self._rows.append({"type": "sub", "label": "Attachements"})
            for k, v in attachments.items():
                self._data(f"  {k}", v)

        social = anima.get("social_beliefs", {})
        if social:
            self._rows.append({"type": "sub", "label": "Croyances sociales"})
            for k, v in social.items():
                if isinstance(v, dict):
                    self._data(f"  {k}", "")
                    for sk, sv in v.items():
                        self._data(f"    {sk}", sv)
                else:
                    self._data(f"  {k}", v)

        reputation = anima.get("reputation", {})
        if reputation:
            self._rows.append({"type": "sub", "label": "Reputation"})
            for k, v in reputation.items():
                self._data(f"  {k}", v)

        episodes = anima.get("episodes", [])
        if episodes:
            self._rows.append({"type": "sub", "label": f"Episodes ({len(episodes)})"})
            for ep in episodes[-3:]:
                self._data("  episode", str(ep))

        life_events = agent_snap.get("life", [])
        if life_events:
            self._rows.append({"type": "sub", "label": "Evenements de vie"})
            for ev in life_events[-5:]:
                self._data("  evenement", str(ev))

        self.endResetModel()

    def _data(self, attr, value):
        self._rows.append({"type": "data", "attr": attr, "value": _fmt(value)})

    def rowCount(self, parent=None):
        return len(self._rows)

    def columnCount(self, parent=None):
        return 2

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.HEADERS[section]
        return None

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or index.row() >= len(self._rows):
            return None
        row = self._rows[index.row()]
        row_type = row["type"]

        if role == Qt.ItemDataRole.BackgroundRole:
            if row_type == "section":
                return _SECTION_BG
            if row_type == "sub":
                return QColor(50, 60, 80)
            return None

        if role == Qt.ItemDataRole.ForegroundRole:
            if row_type == "section":
                return _SECTION_FG
            if row_type == "sub":
                return QColor(140, 170, 210)
            return None

        if role == Qt.ItemDataRole.FontRole:
            if row_type == "section":
                f = QFont()
                f.setBold(True)
                f.setPointSize(11)
                return f
            if row_type == "sub":
                f = QFont()
                f.setBold(True)
                return f

        if role == Qt.ItemDataRole.DisplayRole:
            if row_type == "section":
                return row["label"] if index.column() == 0 else ""
            if row_type == "sub":
                return row["label"] if index.column() == 0 else ""
            if index.column() == 0:
                return row.get("attr", "")
            return row.get("value", "")

        return None
