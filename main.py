from __future__ import annotations
from dataclasses import dataclass, field
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
    obstacles: Iterable[Tuple[int, int]] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        self._obstacles: Set[Tuple[int, int]] = {
            (x % self.width, y % self.height) for (x, y) in self.obstacles
        }

    def wrap(self, pos: Position) -> Position:
        return Position(pos.x % self.width, pos.y % self.height)

    def has_obstacle(self, pos: Position) -> bool:
        return (pos.x % self.width, pos.y % self.height) in self._obstacles


@dataclass
class Buggy:
    planet: Moon
    position: Position
    direction: Direction

    def turn_left(self) -> None:
        self.direction = self.direction.left()

    def turn_right(self) -> None:
        self.direction = self.direction.right()

    def _step(self, sign: int, *, check_obstacles: bool) -> bool:
        dx, dy = self.direction.vector
        nxt = self.planet.wrap(
            Position(self.position.x + sign * dx, self.position.y + sign * dy),
        )
        if check_obstacles and self.planet.has_obstacle(nxt):
            return False
        self.position = nxt
        return True

    def move_forward(self) -> None:
        #közvetlen hívásnál nicsn akadály észlelés
        self._step(+1, check_obstacles=False)

    def move_backward(self) -> None:
        self._step(-1, check_obstacles= False)

    def execute(self, commands: str)   -> ExecutionResult:
        processed = 0
        blocked = False
        obstacle_pos = None
        remaining = ""

        for idx, c in enumerate(commands):
            cl = c.lower()
            if cl == "l":
                self.turn_left()
                processed += 1
            elif cl == "r":
                self.turn_right()
                processed += 1
            elif cl == "f":
                ok = self._step(+1, check_obstacles=True)
                if not ok:
                    blocked = True
                    dx, dy = self.direction.vector
                    obstacle_pos = self.planet.wrap(Position(self.position.x + dx, self.position.y + dy))
                    remaining = commands[idx:]  # a blokkoló utasítástól kezdve
                    break
                processed += 1
            elif cl == "b":
                ok = self._step(-1, check_obstacles=True)
                if not ok:
                    blocked = True
                    dx, dy = self.direction.vector
                    obstacle_pos = self.planet.wrap(Position(self.position.x - dx, self.position.y - dy))
                    remaining = commands[idx:]  # a blokkoló utasítástól kezdve
                    break
                processed += 1
            else:
                # ismeretlen parancs: no-op (nem növeljük processed-et),
                # de NEM kerül a remaining-be, mert végrehajtás szempontból feldolgoztuk.
                continue

            # ha nem történt break (nem blokk), a remaining maradjon üresen
        return ExecutionResult(
            position=self.position,
            direction=self.direction.value,
            blocked=blocked,
            obstacles=obstacle_pos,
            processed=processed,
            remaining=remaining,
        )
