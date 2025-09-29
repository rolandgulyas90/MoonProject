from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Optional

@dataclass(frozen=True)
class Position:
    x: int
    y: int

class Direction(str, Enum):
    N = "N"
    S = "S"
    E = "E"
    W = "W"

@dataclass
class Moon:
    width: int
    height: int
    obstacles: list[tuple[int, int]]

@dataclass
class Buggy:
    planet: Moon
    position: Position
    direction: Direction