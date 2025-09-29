from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Iterable, Set, Tuple

@dataclass(frozen=True)
class Position:
    x: int
    y: int

class Direction(str, Enum):
    N = "N"; S = "S"; E = "E"; W = "W"

    def left(self) -> "Direction":
        i = _ORDER.index(self)
        return _ORDER[(i - 1 ) % 4]

    def right(self) -> "Direction":
        i = _ORDER.index(self)
        return _ORDER[(i + 1) % 4]

    @property
    def vector(self) -> tuple[int, int]:
        # y koordinátára váltás a fordulás miatt
        return{
            Direction.N: (0,1),
            Direction.E: (1,0),
            Direction.S: (0,-1),
            Direction.W: (-1,0),
        }[self]

_ORDER= (Direction.N, Direction.E, Direction.S, Direction.W)

@dataclass(frozen=True)
class ExecutionResult:
    position: Position
    direction: str
    blocked: bool
    obstacles: Optional[Position]
    processed: int
    remaining: str

    @property
    def obstacle(self) -> Optional[Position]:
        return self.obstacles

@dataclass
class Moon:
    width: int
    height: int
    obstacles: list[tuple[int, int]]

    def __post_init__(self) -> None:
        # Normalizálás és 0(1) keresés: list >set. modulo térképméret
        norm: Set[Tuple[int, int]] = {
            (x % self.width, y % self.height) for (x, y) in self.obstacles
        }
        self.obstacles = norm

    def wrap(self, pos: Position) -> Position:
        return Position(pos.x % self.width, pos.y % self.height)

    def has_obstacle(self, pos: Position) -> bool:
        return (pos.x % self.width, pos.y % self.height) in self.obstacles


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
        return self.planet.wrap(
            Position(self.position.x + sign * dx, self.position.y + sign * dy)
        )

    def move_forward(self) -> None:
        #közvetlen hívásnál nicsn akadály észlelés
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
                if self.planet.has_obstacle(nxt):
                    blocked = True
                    obstacle_pos = nxt
                    break #megáll, a blokkolo utasitast nem hajtja vegre, de ha nicns akadály lép
                self.position = nxt
                processed += 1
            else:
                #ismeretlen parancsot letiltjuk, ezzel nem növeljüök a processed változót
                pass

        remaining = commands[processed:]
        return ExecutionResult(
            position=self.position,
            direction=self.direction.value,
            blocked=blocked,
            obstacles=obstacle_pos,
            processed=processed,
            remaining=remaining,
        )
