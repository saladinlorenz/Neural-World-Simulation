"""Temps meteo : jour/nuit, saisons, pluie, vent, temperature.
Le monde vieillit : une foret laissee seule ne doit pas rester identique."""
import numpy as np

from .config import DAY_TICKS, DAYS_PER_SEASON, SEASONS


class Clock:
    def __init__(self, rng=None):
        self.rng = rng or np.random.default_rng(3)
        self.t = 0
        self.day = 0
        self.season = 0
        self.year = 0
        self.light = 1.0          # 0 nuit -> 1 jour
        self.temp = 0.6           # 0 glace -> 1 canicule
        self.rain = 0.0           # 0..1 intensite
        self.wind = (0.0, 0.0)
        self.growth_f = 1.0
        self._storm = 0
        #: Tick du dernier eclair : l'interface en deduit un flash de 3
        #: images sans tirer dans le rng du moteur a chaque frame de paint.
        self.lightning_tick = -10

    @property
    def day_frac(self):
        return (self.t % DAY_TICKS) / DAY_TICKS

    @property
    def is_night(self):
        return self.light < 0.35

    @property
    def is_winter(self):
        return self.season == 3

    def label(self):
        h = int(self.day_frac * 24)
        m = int((self.day_frac * 24 - h) * 60)
        return f"An {self.year+1} · {SEASONS[self.season]} · jour {self.day % (DAYS_PER_SEASON*4)+1} · {h:02}:{m:02}"

    def step(self):
        self.t += 1
        f = self.day_frac
        # lumiere : aube 0.05-0.25, jour, crépuscule 0.7-0.9
        if f < 0.05:
            self.light = 0.15 + f / 0.05 * 0.85
        elif f < 0.70:
            self.light = 1.0
        elif f < 0.85:
            self.light = 1.0 - (f - 0.70) / 0.15 * 0.85
        else:
            self.light = 0.15
        # cycle jour/nuit -> saison -> annee
        if f < 1.0 / DAY_TICKS:
            self.day += 1
            if self.day % DAYS_PER_SEASON == 0:
                self.season = (self.season + 1) % 4
                if self.season == 0:
                    self.year += 1
        # temperature saisonniere + diurne + bruit
        s_base = (0.85, 0.95, 0.6, 0.25)[self.season]
        self.temp = float(np.clip(s_base + 0.15 * (self.light - 0.5)
                                  + self.rng.normal(0, 0.02), 0, 1))
        self.growth_f = max(0.15, self.temp * (1.0 + 0.8 * self.rain)
                            - 0.25 * (self.season == 3))
        # meteo : etat machine (sec / nuage / pluie / orage)
        if self._storm > 0:
            self._storm -= 1
            self.rain = min(1.0, self.rain + 0.02)
        elif self.rain > 0:
            self.rain = max(0.0, self.rain - 0.004)
        elif self.rng.random() < 0.0012:
            self._storm = int(self.rng.integers(400, 1400))
            self.rain = 0.3
        ang = self.rng.uniform(0, 6.283) if self.rain > 0.5 else None
        if ang is not None:
            self.wind = (float(np.cos(ang)) * self.rain, float(np.sin(ang)) * self.rain)
        else:
            self.wind = (self.wind[0] * 0.98, self.wind[1] * 0.98)
        return self

    def lightning(self):
        """Eclairs pendant les orages — le feu n'est jamais scripted ailleurs."""
        return self.rain > 0.75 and self.rng.random() < 0.004
