from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional

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


@dataclass(frozen=True)
class ExecutionResult:
    position: Position
    direction: str
    blocked: bool
    obstace: Optional[Position]
    processed: int
    remaining: str

def _dir_vector(d: Direction) -> tuple[int, int]:
    # y koordinátára váltás a fordulás miatt
    return{
        Direction.N: (0,1),
        Direction.E: (1,0),
        Direction.S: (0,-1),
        Direction.W: (-1,0),
    }[d]

def _wrap(planet: Moon, pos: Position) -> Position:
    return Position(pos.x % planet.width, pos.y % planet.height)

def _has_obstacle(planet: Moon, pos: Position) -> bool:
    return (pos.x % planet.width, pos.y % planet.height) in planet.obstacles

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

    def _next(self, sign: int) -> Position:
        dx, dy = _dir_vector(self.direction)
        return _wrap(self.planet, Position(self.position.x + dx * sign, self.position.y + dy * sign))

    def move_forward(self) -> None:
        self.position = self._next(+1)

    def move_backward(self) -> None:
        self.position = self._next(-1)

    def execute(self, commands: str)   -> ExecutionResult:
        processed = 0
        blocked = False
        obstacle_pos: Optional[Position] = None

        for c in commands:
            cl = c.lower()
            if cl == "l":
                self.turn_left()
                processed += 1
            elif cl == "r":
                self.turn_right()
                processed += 1
            elif cl in ("f","b"):
                sign = +1 if cl == "f" else -1
                nxt = self._next(sign)
                if _has_obstacle(self.planet, nxt):
                    blocked = True
                    obstacle_pos = nxt
                    break #megáll, a blokkolo utasitast nem hajtja vegre, de ha nicns akadály lép
                self.position = nxt
                processed += 1
            else:
                #ismeretlen parancsot letiltjuk, ezzen nem növeljüök a processed változót
                pass

        remaining = commands[processed:]
        return ExecutionResult(
            position=self.position,
            direction=self.direction.value,
            blocked=blocked,
            obstace=obstacle_pos,
            processed=processed,
            remaining=remaining,
        )
