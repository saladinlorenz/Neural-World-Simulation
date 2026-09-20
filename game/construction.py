"""Construction progressive style Minecraft.

Un blueprint est une liste de cellules. Les habitants posent des blocs réels
un par un. Le chantier peut être partagé entre plusieurs habitants.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class BlockTask:
    tx: int
    ty: int
    material: str
    phase: str
    solid: bool = True


@dataclass
class ConstructionSite:
    origin_tx: int
    origin_ty: int
    blueprint_name: str
    tasks: list[BlockTask]
    placed: set[tuple[int, int]] = field(default_factory=set)
    contributors: dict[int, int] = field(default_factory=dict)
    created_tick: int = 0
    owner_eid: int | None = None
    owner_clan: str | None = None

    @property
    def key(self):
        return self.origin_tx, self.origin_ty

    def remaining_tasks(self) -> list[BlockTask]:
        return [task for task in self.tasks if (task.tx, task.ty) not in self.placed]

    def complete(self) -> bool:
        return len(self.placed) >= len(self.tasks)

    def progress(self) -> float:
        if not self.tasks:
            return 1.0
        return min(1.0, len(self.placed) / len(self.tasks))

    def missing_materials(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for task in self.remaining_tasks():
            out[task.material] = out.get(task.material, 0) + 1
        return out

    def next_task_for(self, inventory: dict[str, int]) -> BlockTask | None:
        """Priorité aux tâches que l'habitant peut réellement accomplir.

        Ordre : fondation → mur → porte → toit.
        """
        order = {"foundation": 0, "wall": 1, "door": 2, "roof": 3}
        tasks = sorted(self.remaining_tasks(), key=lambda t: order.get(t.phase, 9))
        for task in tasks:
            if inventory.get(task.material, 0) > 0:
                return task
        return None

    def mark_placed(self, eid: int, task: BlockTask):
        self.placed.add((task.tx, task.ty))
        self.contributors[eid] = self.contributors.get(eid, 0) + 1


class HouseBlueprint:
    """Fabrique des plans simples, réalistes et adaptables.

    Petite maison 5x5 :
    - sol intérieur 3x3,
    - murs sur contour,
    - ouverture centrale au sud (porte),
    - toit visuel sur contour supérieur.
    """

    @staticmethod
    def small_house(tx: int, ty: int, material: str = "bois") -> list[BlockTask]:
        tasks: list[BlockTask] = []
        width, height = 5, 5
        door_x = tx + width // 2
        door_y = ty + height - 1

        for y in range(ty, ty + height):
            for x in range(tx, tx + width):
                edge = x in (tx, tx + width - 1) or y in (ty, ty + height - 1)
                if edge:
                    tasks.append(BlockTask(x, y, "pierre", "foundation", solid=True))

        for y in range(ty, ty + height):
            for x in range(tx, tx + width):
                edge = x in (tx, tx + width - 1) or y in (ty, ty + height - 1)
                if not edge:
                    continue
                if x == door_x and y == door_y:
                    tasks.append(BlockTask(x, y, "bois", "door", solid=False))
                else:
                    tasks.append(BlockTask(x, y, material, "wall", solid=True))

        for x in range(tx, tx + width):
            tasks.append(BlockTask(x, ty, material, "roof", solid=False))

        return tasks

    @staticmethod
    def storage_hut(tx: int, ty: int) -> list[BlockTask]:
        """Petit bâtiment 3x3 utile pour futur dépôt collectif."""
        tasks: list[BlockTask] = []
        for y in range(ty, ty + 3):
            for x in range(tx, tx + 3):
                edge = x in (tx, tx + 2) or y in (ty, ty + 2)
                if edge:
                    tasks.append(BlockTask(x, y, "bois", "wall", solid=True))
        tasks.append(BlockTask(tx + 1, ty + 2, "bois", "door", solid=False))
        return tasks


def blueprint_from_name(name: str, tx: int, ty: int) -> list[BlockTask]:
    if name == "storage_hut":
        return HouseBlueprint.storage_hut(tx, ty)
    return HouseBlueprint.small_house(tx, ty)
