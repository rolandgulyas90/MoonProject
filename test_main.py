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

def test_processed_counts_turns_and_stops_on_obstacle():
    moon = Moon(5, 5, obstacles = [(2,0)])
    b = Buggy(moon, Position(0,0), Direction.E)
    res = b.execute("rlff")
    # az első két turn lefutott
    assert b.direction == Direction.E
    # az első f sikerült, poz (1,0)
    assert b.position == Position(1, 0)
    # a második f blokkolt (2,0 obstacle)
    assert res.blocked is True
    assert res.obstacles == Position(2,0)
    # processed = 3 (r,l,f), remaining = "f"
    assert res.processed == 3
    assert res.remaining == "f"

def test_ignoring_unknown_orders():
    planet = Moon(5, 5, obstacles=[(2, 2)])
    b = Buggy(planet, Position(0, 0), Direction.E)

    res = b.execute("xlyrfz")
    assert res.processed == 3  # csak l, r, f számít
    assert res.blocked is False
    assert res.remaining == ""  # nem blokkolt, feldolgozott mindent
    assert b.position == Position(1, 0)

def test_stops_at_first_of_multiple_obstacles():
    moon = Moon(5, 5, obstacles=[(1, 0), (2, 0)])
    b = Buggy(moon, Position(0, 0), Direction.E)

    res = b.execute("fff")
    # már az első f célmezője (1,0) akadály -> azonnal megáll
    assert res.blocked is True
    assert res.obstacles == Position(1, 0)
    assert res.processed == 0
    assert res.remaining == "fff"
    assert b.position == Position(0, 0)  # nem mozdult
    assert res.direction == "E"

def test_many_backward_wraps_negative_direction():
    moon = Moon(5, 5, [])
    b = Buggy(moon, Position(0, 0), Direction.W)

    res = b.execute("b" * 6)
    assert res.blocked is False
    assert b.position == Position(1, 0)

def test_wrap_forward_hits_obstacle_and_blocks():
    # (4,2) kelet felé "f" -> wrap után (0,2), ahol akadály van
    moon = Moon(5, 5, obstacles=[(0, 2)])
    b = Buggy(moon, Position(4, 2), Direction.E)

    res = b.execute("f")
    assert res.blocked is True
    assert res.obstacles == Position(0, 2)
    assert b.position == Position(4, 2)
    assert res.processed == 0
    assert res.remaining == "f"
    assert res.direction == "E"

def test_wrap_backward_hits_obstacle_and_blocks():
    # (0,2) kelet irányban "b" -> nyugatra lépne wrap-pel (4,2), ott akadály
    moon = Moon(5, 5, obstacles=[(4, 2)])
    b = Buggy(moon, Position(0, 2), Direction.E)

    res = b.execute("b")
    assert res.blocked is True
    assert res.obstacles == Position(4, 2)
    assert b.position == Position(0, 2)
    assert res.processed == 0
    assert res.remaining == "b"
    assert res.direction == "E"