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
            Direction.E: Direction.S,
            Direction.S: Direction.W,
            Direction.W: Direction.N,
        }[self]
    
def _dir_vector(d: Direction) -> tuple[int, int]:
    # y koordinátára váltás a fordulás miatt
    return{
        Direction.N: (0,1),
        Direction.E: (1,0),
        Direction.S: (0,-1),
        Direction.W: (-1,0),
    }[d]

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

    def move_forward(self) -> None:
        dx, dy = _dir_vector(self.direction)
        self.position = Position(self.position.x + dx, self.position.y + dy)

    def move_backward(self) -> None:
        dx, dy = _dir_vector(self.direction)
        self.position = Position(self.position.x - dx, self.position.y - dy)
