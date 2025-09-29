from main import Buggy, Moon, Direction, Position

def test_initial_state():
    planet = Planet(width = 5, height  5, obstacles=[])
    b = Buggy(planet=planet, position=Position(2, 3),direction=Direction.N)
    assert b.position == Position(2, 3)
    assert b.direction == Direction.N