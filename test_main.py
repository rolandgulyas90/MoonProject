from main import Buggy, Moon, Direction, Position

def test_initial_state():
    planet = Moon(width = 5, height = 5, obstacles=[])
    b = Buggy(planet=planet, position=Position(2, 3),direction=Direction.N)
    assert b.position == Position(2, 3)
    assert b.direction == Direction.N

def test_turning_left_and_right():
    planet = Moon(5, 5, [])
    b = Buggy(planet, Position(0,0), Direction.N)

    b.turn_right(); assert b.direction == Direction.E
    b.turn_right(); assert b.direction == Direction.S
    b.turn_right(); assert b.direction == Direction.W
    b.turn_right(); assert b.direction == Direction.N

    b.turn_left(); assert b.direction == Direction.E
    b.turn_left(); assert b.direction == Direction.S
    b.turn_left(); assert b.direction == Direction.W
    b.turn_left(); assert b.direction == Direction.N