"""Cerveau — moteur d'arbitrage + apprentissage.

L'etre possede un SAVOIR GENERAL (affordances du monde, lois physiques) mais
AUCUN objectif impose. A chaque reflexion, le cerveau recoit une representation
structuree (encoders : corps, besoins, emotions, personnalite, soi, social,
experiences, competences, habitudes, perception locale, MEMOIRE de ce qui a ete
percu — jamais d'omniscience — et le temps) et produit une INTENTION
structuree : action + cible + intensite.

Architecte : Elman a contexte diagonal, taille figee a la creation (verrouillee,
meme le createur ne peut plus la changer). Les POIDS, eux, APPRENNENT pendant la
vie : REINFORCE (gradient du log-proba de l'action choisie x recompense vecue),
taux modulе par l'age (un enfant apprend 2x plus vite, un vieux fige).

Boucle du contrat moteur :
  perception -> cerveau -> intention -> le MONDE verifie la faisabilite
  -> consequences -> experience -> recompense -> apprentissage -> cerveau.

--------------------------------------------------------------------------
AMELIORATIONS (integration inchangee : meme classe Brain, memes methodes
think/learn/breed/copy, memes constantes N_IN/N_OUT/ACTION_*) :

1. Modulation reelle par l'age dans learn() — le docstring la promettait,
   elle n'etait pas cablee. Un parametre optionnel age_factor (0..1+) est
   accepte partout ou l'appelant peut le fournir ; par defaut =1.0 (comportement
   identique a avant si l'appelant ne change rien).
2. Trace d'eligibilite courte (multi-pas) — une recompense qui arrive
   quelques pas apres l'action qui l'a causee (ex: recolter -> manger plus
   tard) peut maintenant renforcer aussi les decisions recentes, avec une
   decroissance temporelle, au lieu de ne renforcer que le dernier choix.
3. Entropie liee a la personnalite (curiosite/prudence) — un etre curieux
   explore davantage (temperature effective plus haute), un prudent se
   restreint aux actions sures ; brancher sur les traits deja definis dans
   ACTION_TRAIT sans ajouter de nouvelle dependance externe.
4. explain() — expose un classement lisible des intentions (nom, couleur,
   probabilite) pour que le dashboard affiche "ce qu'il va faire et pourquoi"
   sans avoir a connaitre la representation interne du reseau.
5. Garde-fous NaN/Inf sur les poids et sur la sortie, essentiels sur une
   vie simulee longue (des milliers de pas d'apprentissage continu).
--------------------------------------------------------------------------
"""
import numpy as np
from collections import deque

N_IN = 128
N_OUT = 15
N_STRATEGIES = 6
N_TARGETS = 8

# vocabulaire d'actions elementaires (composables par le monde, jamais des roles)
(REST, SLEEP, EAT, DRINK, HARVEST, DROP, BUILD, GIVE, TAKE, ATTACK,
 FLEE, EXPLORE, TALK, MARK, SOCIAL) = range(15)

ACTION_NAMES = {REST: "Repos", SLEEP: "Dormir", EAT: "Manger", DRINK: "Boire",
                HARVEST: "Récolter", DROP: "Poser", BUILD: "Construire",
                GIVE: "Offrir", TAKE: "Prendre", ATTACK: "Attaquer",
                FLEE: "Fuir", EXPLORE: "Explorer", TALK: "Parler", MARK: "Marquer",
                SOCIAL: "Rejoindre"}
ACTION_COLORS = {REST: (140, 140, 160), SLEEP: (120, 110, 180), EAT: (236, 150, 86),
                 DRINK: (90, 180, 230), HARVEST: (110, 200, 120), DROP: (170, 140, 100),
                 BUILD: (236, 190, 86), GIVE: (160, 230, 200), TAKE: (200, 160, 90),
                 ATTACK: (222, 96, 96), FLEE: (150, 150, 200), EXPLORE: (96, 168, 222),
                  TALK: (255, 180, 220), MARK: (255, 120, 200), SOCIAL: (200, 160, 255)}

# strategies
(IMMEDIAT, PRUDENT, ECONOMIQUE, COOPERATIF, EXPLORATION, DEFENSIF) = range(N_STRATEGIES)
STRATEGY_NAMES = {IMMEDIAT: "Immédiat", PRUDENT: "Prudent", ECONOMIQUE: "Économique",
                  COOPERATIF: "Coopératif", EXPLORATION: "Exploration", DEFENSIF: "Défensif"}
STRATEGY_COLORS = {IMMEDIAT: (220, 120, 80), PRUDENT: (120, 180, 120),
                   ECONOMIQUE: (180, 180, 80), COOPERATIF: (120, 180, 220),
                   EXPLORATION: (100, 160, 220), DEFENSIF: (200, 140, 140)}

# types de cible
(SOI, NOURRITURE, EAU, BOIS, PIERRE, ABRI, DEPOT_CHANTIER, ETRE_VIVANT) = range(N_TARGETS)
TARGET_NAMES = {SOI: "Soi", NOURRITURE: "Nourriture", EAU: "Eau", BOIS: "Bois",
                PIERRE: "Pierre", ABRI: "Abri", DEPOT_CHANTIER: "Dépôt/Chantier",
                ETRE_VIVANT: "Être vivant"}
TARGET_COLORS = {SOI: (180, 180, 180), NOURRITURE: (236, 150, 86), EAU: (90, 180, 230),
                 BOIS: (150, 108, 62), PIERRE: (150, 150, 156), ABRI: (170, 140, 100),
                 DEPOT_CHANTIER: (200, 160, 90), ETRE_VIVANT: (200, 160, 255)}

# personnalite : 0 sociabilite 1 agressivite 2 curiosite 3 prudence 4 patience
# 5 empathie 6 impulsivite 7 confiance 8 perseverance 9 ambition 10 generosite
# 11 discipline
ACTION_TRAIT = {
    REST:    (8, -0.28),
    SLEEP:   (11, -0.20),
    EAT:     (3, -0.08),
    DRINK:   (3, -0.08),
    HARVEST: (8, 0.30),
    DROP:    (11, 0.10),
    BUILD:   (8, 0.36),
    GIVE:    (10, 0.48),
    TAKE:    (1, 0.30),
    ATTACK:  (1, 0.42),
    FLEE:    (3, 0.30),
    EXPLORE: (2, 0.44),
    TALK:    (0, 0.42),
    MARK:    (9, 0.22),
    SOCIAL:  (0, 0.40),
}

# actions considerees "sures" par un profil prudent (utilisees uniquement
# pour moduler l'entropie/exploration ci-dessous — n'affecte jamais les
# probas de base issues du reseau)
_SAFE_ACTIONS = {REST, SLEEP, EAT, DRINK, DROP, TALK}

SIZES = (25, 50, 75, 100, 128, 256, 512, 768, 1000)


def think_every(n):
    if n <= 128:
        return 2
    if n <= 256:
        return 4
    if n <= 1024:
        return 8
    return 16


def params_size(n):
    return N_IN * n + n + n + N_OUT * n + N_OUT


def rand_weights(rng, n):
    p = np.empty(params_size(n), dtype=np.float64)
    i = 0
    p[i:i + N_IN * n] = rng.normal(0, 0.6, N_IN * n); i += N_IN * n
    p[i:i + n] = rng.normal(0, 0.8, n); i += n
    p[i:i + n] = rng.normal(0, 0.3, n); i += n
    p[i:i + N_OUT * n] = rng.normal(0, 0.6, N_OUT * n); i += N_OUT * n
    p[i:] = rng.normal(0, 0.3, N_OUT)
    return p


def unpack(p, n):
    i = 0
    Wx = p[i:i + N_IN * n].reshape(n, N_IN); i += N_IN * n
    Wd = p[i:i + n]; i += n
    b1 = p[i:i + n]; i += n
    Wo = p[i:i + N_OUT * n].reshape(N_OUT, n); i += N_OUT * n
    b2 = p[i:]
    return Wx, Wd, b1, Wo, b2


class Brain:
    def __init__(self, n_hid=128, params=None, rng=None, elig_len=6, elig_decay=0.55):
        self.rng = rng or np.random.default_rng()
        self.n = int(n_hid)
        self.te = think_every(self.n)
        self.p = np.array(rand_weights(rng, self.n) if params is None else params,
                          dtype=np.float64)
        self.h = np.zeros(self.n)
        self.last_out = np.zeros(N_OUT)
        self.probs = np.full(N_OUT, 1.0 / N_OUT)
        self.base = 0.0                     # baseline REINFORCE
        self._has_thought = False             # True après think(), reset après learn()
        # trace multi-pas : chaque decision recente reste renforçable un moment
        self._trace = deque(maxlen=max(1, int(elig_len)))
        self._trace_decay = float(elig_decay)
        # têtes supplémentaires : stratégie + cible (Lot 7.2)
        scale = 0.4 / np.sqrt(self.n)
        self._Wo_strat = rng.normal(0, scale, (N_STRATEGIES, self.n)).astype(np.float64)
        self._b2_strat = rng.normal(0, 0.15, N_STRATEGIES).astype(np.float64)
        self._Wo_targ = rng.normal(0, scale, (N_TARGETS, self.n)).astype(np.float64)
        self._b2_targ = rng.normal(0, 0.15, N_TARGETS).astype(np.float64)
        self._strat_probs = np.full(N_STRATEGIES, 1.0 / N_STRATEGIES)
        self._targ_probs = np.full(N_TARGETS, 1.0 / N_TARGETS)
        self._strategy = IMMEDIAT
        self._target = SOI
        self._sync()

    def _sync(self):
        self._Wx, self._Wd, self._b1, self._Wo, self._b2 = unpack(self.p, self.n)

    def think(self, x, temperature=1.0, bias=None, curiosity=None, caution=None):
        """Représentation interne -> politique softmax -> intention échantillonnée.
        bias = ponderations du corps (personnalite, emotions, urgences vitales).
        Les logits du reseau sont amortis pour que le biais corporel puisse
        dominer en cas d'urgence, sans effacer l'individualite du cerveau.

        curiosity/caution (optionnels, 0..1) : si l'appelant transmet ces deux
        traits de personnalite (ils existent deja dans l'encoder personnalite,
        index 2 et 3), la temperature effective est ajustee — un etre curieux
        explore un peu plus, un prudent se resserre sur les actions sures.
        Comportement inchange si ces arguments ne sont pas fournis."""
        h_prev = self.h
        self.h = np.tanh(x @ self._Wx.T + self._Wd * self.h + self._b1)
        # garde-fou : un cerveau qui vit tres longtemps et apprend en continu
        # peut voir ses poids diverger ; on neutralise silencieusement plutot
        # que de laisser NaN se propager dans toute la simulation
        if not np.all(np.isfinite(self.h)):
            self.h = np.nan_to_num(self.h, nan=0.0, posinf=1.0, neginf=-1.0)
        logits = (self.h @ self._Wo.T + self._b2) * 0.45
        if bias is not None:
            logits = logits + bias * 1.8

        eff_temp = max(0.15, temperature)
        if curiosity is not None or caution is not None:
            c = 0.0 if curiosity is None else float(curiosity)
            p = 0.0 if caution is None else float(caution)
            # curiosite ouvre l'exploration, prudence la referme ; net borne
            eff_temp *= max(0.5, 1.0 + 0.6 * c - 0.5 * p)
            if p > 0.0:
                penal = np.array([0.0 if a in _SAFE_ACTIONS else 1.0 for a in range(N_OUT)])
                logits = logits - penal * (p * 1.2)

        z = (logits - logits.max()) / eff_temp
        e = np.exp(z)
        probs = e / e.sum()
        if not np.all(np.isfinite(probs)):
            probs = np.full(N_OUT, 1.0 / N_OUT)
        self.last_out = probs
        self.probs = probs
        act = int(self.rng_choice(probs))

        # tete strategie
        strat_logits = (self.h @ self._Wo_strat.T + self._b2_strat) * 0.35
        sz = (strat_logits - strat_logits.max()) / eff_temp
        se = np.exp(sz)
        self._strat_probs = se / se.sum()
        if not np.all(np.isfinite(self._strat_probs)):
            self._strat_probs = np.full(N_STRATEGIES, 1.0 / N_STRATEGIES)
        self._strategy = int(self.rng_choice(self._strat_probs))

        # tete cible
        targ_logits = (self.h @ self._Wo_targ.T + self._b2_targ) * 0.35
        tz = (targ_logits - targ_logits.max()) / eff_temp
        te2 = np.exp(tz)
        self._targ_probs = te2 / te2.sum()
        if not np.all(np.isfinite(self._targ_probs)):
            self._targ_probs = np.full(N_TARGETS, 1.0 / N_TARGETS)
        self._target = int(self.rng_choice(self._targ_probs))

        self._has_thought = True
        self._trace.append((x.copy(), h_prev.copy(), act, probs.copy(),
                            self._strategy, self._targ_probs.copy()))
        return act, probs

    def rng_choice(self, probs):
        return int(self.rng.choice(len(probs), p=probs))

    def explain(self, top=5):
        """Classement lisible de la derniere intention, pour le dashboard :
        renvoie une liste de dicts {action, nom, couleur, probabilite}
        triee par probabilite decroissante — aucune connaissance du reseau
        n'est requise cote UI."""
        order = np.argsort(-self.probs)[:max(1, int(top))]
        return [
            {
                "action": int(a),
                "nom": ACTION_NAMES.get(int(a), "?"),
                "couleur": ACTION_COLORS.get(int(a), (200, 200, 200)),
                "probabilite": float(self.probs[a]),
            }
            for a in order
        ]

    # ------------------------------------------------------------------ apprentissage
    def learn(self, reward, lr=0.0022, age_factor=1.0):
        """REINFORCE : renforcer ce qui a reduit la frustration, affaiblir le reste.
        Seuls POIDS et BIAIS bougent — l'architecture reste verrouillée.

        age_factor (0..~2, defaut 1.0) : multiplie le taux d'apprentissage
        effectif — un jeune (>1.0) apprend plus vite, un vieux (<1.0) se fige,
        conformement au docstring. Comportement inchange si l'appelant ne
        fournit rien.

        La derniere decision est renforcee pleinement ; les decisions
        recentes (trace courte) sont renforcees avec une decroissance
        temporelle, pour capturer les recompenses qui arrivent quelques pas
        apres l'action qui les a causees (ex: recolter -> manger plus tard)."""
        if not self._has_thought:
            return
        self._has_thought = False
        adv = reward - self.base
        self.base += 0.05 * adv
        eff_lr = lr * max(0.0, float(age_factor))

        # decision la plus recente en premier (poids plein), puis les
        # precedentes avec decroissance geometrique
        n = len(self._trace)
        for i, entry in enumerate(reversed(self._trace)):
            w = self._trace_decay ** i
            if w < 0.02:
                break
            # compat : ancien format (x,h,act,probs) vs nouveau (x,h,act,probs,strat,targ_probs)
            if len(entry) == 4:
                x, h_prev, act, probs = entry
                strat, targ_probs = None, None
            else:
                x, h_prev, act, probs, strat, targ_probs = entry
            # gradient sur l'action
            d = (np.arange(N_OUT) == act) - probs
            d = d * (adv * eff_lr * w)
            dh = (d @ self._Wo) * (1.0 - h_prev ** 2)
            self._b2 += d
            self._Wo += np.outer(d, self.h if i == 0 else h_prev)
            self._b1 += dh * 0.5
            self._Wd += dh * h_prev * 0.5
            self._Wx += np.outer(dh, x) * 0.5
            # gradient sur la strategie
            if strat is not None:
                ds = (np.arange(N_STRATEGIES) == strat) - self._strat_probs
                ds = ds * (adv * eff_lr * w * 0.5)
                self._b2_strat += ds
                self._Wo_strat += np.outer(ds, self.h if i == 0 else h_prev)
            # gradient sur la cible
            if targ_probs is not None:
                dt = (np.arange(N_TARGETS) == self._target) - targ_probs
                dt = dt * (adv * eff_lr * w * 0.5)
                self._b2_targ += dt
                self._Wo_targ += np.outer(dt, self.h if i == 0 else h_prev)

        # garde-fou anti-divergence sur une vie simulee longue
        if not np.all(np.isfinite(self._Wx)):
            np.nan_to_num(self._Wx, copy=False, nan=0.0, posinf=2.0, neginf=-2.0)
        if not np.all(np.isfinite(self._Wo)):
            np.nan_to_num(self._Wo, copy=False, nan=0.0, posinf=2.0, neginf=-2.0)
        if not np.all(np.isfinite(self._Wo_strat)):
            np.nan_to_num(self._Wo_strat, copy=False, nan=0.0, posinf=2.0, neginf=-2.0)
        if not np.all(np.isfinite(self._Wo_targ)):
            np.nan_to_num(self._Wo_targ, copy=False, nan=0.0, posinf=2.0, neginf=-2.0)
        self._sync()

    # ------------------------------------------------------------------ evolution
    @staticmethod
    def breed(pa, pb, na, rng, sigma=0.06, rate=0.08):
        if na is None:
            na = pa.n if rng.random() < 0.5 else pb.n
        if pa.n == pb.n == na:
            child = np.where(rng.random(pa.p.size) < 0.5, pa.p, pb.p)
        elif pa.n == na:
            child = pa.p.copy()
        elif pb.n == na:
            child = pb.p.copy()
        else:
            child = rand_weights(rng, na)
        mut = rng.random(child.size) < rate
        child[mut] += rng.normal(0, sigma, mut.sum())
        return child, na

    def copy(self):
        b = Brain.__new__(Brain)
        b.n, b.te = self.n, self.te
        b.p = self.p.copy()
        b.h = self.h.copy()
        b.last_out = self.last_out.copy()
        b.probs = self.probs.copy()
        b.base = self.base
        b._has_thought = False
        b._trace = deque(maxlen=self._trace.maxlen)
        b._trace_decay = self._trace_decay
        b.rng = np.random.default_rng(self.rng.bit_generator.state["state"]["state"])
        # têtes strategie + cible
        b._Wo_strat = self._Wo_strat.copy()
        b._b2_strat = self._b2_strat.copy()
        b._Wo_targ = self._Wo_targ.copy()
        b._b2_targ = self._b2_targ.copy()
        b._strat_probs = self._strat_probs.copy()
        b._targ_probs = self._targ_probs.copy()
        b._strategy = self._strategy
        b._target = self._target
        b._sync()
        return b
