from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Message:
    sender_eid: int
    receiver_eid: int
    kind: str
    category: str | None
    tx: int | None
    ty: int | None
    confidence: float
    tick: int
