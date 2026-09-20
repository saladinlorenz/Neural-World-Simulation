"""Construction progressive avec tâches à identité unique.

Chaque phase d'une même tuile a son propre identifiant :
- fondation (niveau 0)
- mur/porte (niveau 1)
- toit (niveau 2)

Ainsi, poser une fondation ne termine jamais automatiquement le mur.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class BlockTask:
    tx: int
    ty: int
    material: str
    phase: str
    layer: int
    solid: bool = True

    @property
    def key(self):
        return self.tx, self.ty, self.layer, self.phase


@dataclass
class ConstructionSite:
    origin_tx: int
    origin_ty: int
    blueprint_name: str
    tasks: list[BlockTask]
    placed: set[tuple[int, int, int, str]] = field(default_factory=set)
    contributors: dict[int, int] = field(default_factory=dict)
    created_tick: int = 0
    owner_eid: int | None = None
    owner_clan: str | None = None

    @property
    def key(self):
        return self.origin_tx, self.origin_ty

    def remaining_tasks(self):
        return [task for task in self.tasks if task.key not in self.placed]

    def complete(self):
        return len(self.placed) >= len(self.tasks)

    def progress(self):
        return 1.0 if not self.tasks else min(1.0, len(self.placed) / len(self.tasks))

    def missing_materials(self):
        result = {}
        for task in self.remaining_tasks():
            result[task.material] = result.get(task.material, 0) + 1
        return result

    def next_task_for(self, inventory):
        order = {"foundation": 0, "wall": 1, "door": 1, "roof": 2}
        for task in sorted(self.remaining_tasks(), key=lambda t: (t.layer, order.get(t.phase, 9))):
            if inventory.get(task.material, 0) > 0:
                return task
        return None

    def mark_placed(self, eid, task):
        self.placed.add(task.key)
        self.contributors[eid] = self.contributors.get(eid, 0) + 1


class HouseBlueprint:
    """Plans de bâtiments composés de tâches ordonnées."""

    @staticmethod
    def small_house(tx, ty, wall_material="bois"):
        tasks = []
        width, height = 5, 5
        door_x = tx + width // 2
        door_y = ty + height - 1

        for y in range(ty, ty + height):
            for x in range(tx, tx + width):
                edge = x in (tx, tx + width - 1) or y in (ty, ty + height - 1)
                if edge:
                    tasks.append(BlockTask(x, y, "pierre", "foundation", layer=0, solid=True))

        for y in range(ty, ty + height):
            for x in range(tx, tx + width):
                edge = x in (tx, tx + width - 1) or y in (ty, ty + height - 1)
                if not edge:
                    continue
                if x == door_x and y == door_y:
                    tasks.append(BlockTask(x, y, "bois", "door", layer=1, solid=False))
                else:
                    tasks.append(BlockTask(x, y, wall_material, "wall", layer=1, solid=True))

        for x in range(tx, tx + width):
            tasks.append(BlockTask(x, ty, "bois", "roof", layer=2, solid=False))

        return tasks

    @staticmethod
    def storage_hut(tx, ty):
        tasks = []
        for y in range(ty, ty + 3):
            for x in range(tx, tx + 3):
                edge = x in (tx, tx + 2) or y in (ty, ty + 2)
                if edge:
                    tasks.append(BlockTask(x, y, "bois", "wall", layer=1, solid=True))
        tasks.append(BlockTask(tx + 1, ty + 2, "bois", "door", layer=1, solid=False))
        return tasks


def blueprint_from_name(name, tx, ty):
    if name == "storage_hut":
        return HouseBlueprint.storage_hut(tx, ty)
    return HouseBlueprint.small_house(tx, ty)
