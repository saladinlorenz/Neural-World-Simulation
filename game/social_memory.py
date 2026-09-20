from __future__ import annotations
from dataclasses import dataclass


@dataclass
class SocialRecord:
    trust: float = 0.0
    violence: float = 0.0
    theft: float = 0.0
    generosity: float = 0.0
    last_tick: int = 0

    def score(self):
        return max(-1.0, min(1.0,
            self.trust + self.generosity * 0.5 - self.violence - self.theft * 0.6))


class SocialMemory:
    def __init__(self):
        self.records = {}

    def record(self, observer_eid, target_eid, event, strength, tick):
        key = (int(observer_eid), int(target_eid))
        record = self.records.setdefault(key, SocialRecord())
        strength = max(0.0, min(1.0, float(strength)))

        if event == "help":
            record.generosity = min(1.0, record.generosity + strength)
            record.trust = min(1.0, record.trust + strength * 0.4)
        elif event == "theft":
            record.theft = min(1.0, record.theft + strength)
            record.trust = max(-1.0, record.trust - strength * 0.5)
        elif event == "violence":
            record.violence = min(1.0, record.violence + strength)
            record.trust = max(-1.0, record.trust - strength * 0.8)
        record.last_tick = int(tick)

    def opinion(self, observer_eid, target_eid):
        record = self.records.get((int(observer_eid), int(target_eid)))
        return 0.0 if record is None else record.score()

    def decay(self, tick, interval=3600):
        for key in list(self.records):
            record = self.records[key]
            if tick - record.last_tick < interval:
                continue
            record.trust *= 0.995
            record.violence *= 0.992
            record.theft *= 0.992
            record.generosity *= 0.995
            if abs(record.score()) < 0.02:
                del self.records[key]
