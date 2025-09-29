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

    def left(self) -> "Direction":
        return {
            Direction.N: Direction.W,
            Direction.W: Direction.S,
            Direction.S: Direction.E,
            Direction.E: Direction.N,
        }[self]

    def right(self) -> "Direction":
        return {
            Direction.N: Direction.E,
            Direction.W: Direction.S,
            Direction.S: Direction.W,
            Direction.E: Direction.N,
        }[self]

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

    def turn_left(self) -> None:
        self.direction = self.direction.left()

    def turn_right(self) -> None:
        self.direction = self.direction.right()
