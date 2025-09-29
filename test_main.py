from main import Buggy, Moon, Direction, Position
from dataclasses import dataclass

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

    b.turn_left(); assert b.direction == Direction.W
    b.turn_left(); assert b.direction == Direction.S
    b.turn_left(); assert b.direction == Direction.E
    b.turn_left(); assert b.direction == Direction.N

def test_forward_and_backward():
    planet = Moon(10, 10, [])
    b = Buggy(planet, Position(3,3), Direction.N)

    b.move_forward()
    assert b.position == Position(3,4)

    b.turn_right()
    b.move_forward()
    assert b.position == Position(4,4)

    b.move_backward()
    assert b.position == Position(3,4)

def test_wraparound_edges_forward():
    planet = Moon(5, 5, [])
    # West-> x:0-ról balra lépve a túloldalon bukkan fel (x:4)
    b = Buggy(planet, Position(0,2), Direction.W)
    b.move_forward()
    assert b.position == Position(4,2)

    # South-> y:0-ról lefelé lépve a túloldalon bukkan fel (y:4)
    b = Buggy(planet, Position(1,0), Direction.S)
    b.move_forward()
    assert b.position == Position(1,4)

    # East-> x:4-ről jobbra lépve x:0
    b= Buggy(planet, Position(4,1), Direction.E)
    b.move_forward()
    assert b.position == Position(0,1)

    # North-> y:4-ről felfelé lépve y:0
    b = Buggy(planet, Position(3,4), Direction.N)
    b.move_forward()
    assert b.position == Position(3,0)

def test_wraparound_edges_backward():
    planet = Moon(5, 5, [])
    # West irány esetén kelet felé lépünk
    b = Buggy(planet, Position(4, 1), Direction.W)
    b.move_backward()
    assert b.position == Position(0, 1)

    # Backward North irány esetén dél felé lépünk
    b = Buggy(planet, Position(2, 0), Direction.N)
    b.move_backward()
    assert b.position == Position(2, 4)

def test_obstacle_blocks_first_step_and_reports():
    planet = Moon(5, 5, obstacles = [(1,0)])
    b = Buggy(planet, Position(0,0), Direction.E)

    res = b.execute("f")
    assert b.position == Position(0,0)
    assert res.blocked == True
    assert res.obstacles == Position(1,0)
    assert res.processed == 0
    assert res.remaining == "f"
    assert res.direction == "E"

def test_stops_on_first_obstacle_in_longer_sequence():
    planet = Moon(5, 5, obstacles = [(2,2)])
    b = Buggy(planet, Position(0,2), Direction.E)

    res = b.execute("ffrff")
    assert b.position == Position(1,2)
    assert res.blocked == True
    assert res.obstacles == Position(2,2)
    assert res.processed == 1
    assert res.remaining == "frff"
    assert res.direction == "E"