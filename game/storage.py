from __future__ import annotations
from dataclasses import dataclass, field


MATERIALS = ("bois", "pierre", "or", "graine", "food")


@dataclass
class SharedStorage:
    tx: int
    ty: int
    capacity: int = 80
    owner_clan: str | None = None
    inventory: dict = field(default_factory=lambda: {m: 0 for m in MATERIALS})
    contributors: dict = field(default_factory=dict)
    withdrawals: dict = field(default_factory=dict)
    last_access_tick: int = 0

    def total(self):
        return sum(max(0, int(v)) for v in self.inventory.values())

    def free_space(self):
        return max(0, self.capacity - self.total())

    def deposit(self, eid, material, amount, tick):
        if material not in self.inventory:
            return 0
        moved = max(0, min(int(amount), self.free_space()))
        if moved <= 0:
            return 0
        self.inventory[material] += moved
        self.contributors[eid] = self.contributors.get(eid, 0) + moved
        self.last_access_tick = tick
        return moved

    def withdraw(self, eid, material, amount, tick):
        if material not in self.inventory:
            return 0
        moved = max(0, min(int(amount), self.inventory[material]))
        if moved <= 0:
            return 0
        self.inventory[material] -= moved
        self.withdrawals[eid] = self.withdrawals.get(eid, 0) + moved
        self.last_access_tick = tick
        return moved

    def food_amount(self):
        return int(self.inventory.get("food", 0))
