from main import Buggy, Moon, Direction, Position

def test_initial_state():
    planet = Moon(width=5, height=5, obstacles=[])
    b = Buggy(planet=planet, position=Position(2, 3), direction=Direction.N)
    assert b.position == Position(2, 3)
    assert b.direction == Direction.N

def test_move_left_and_right_are_turn_plus_step():
    planet = Moon(5, 5, [])
    b = Buggy(planet, Position(2, 2), Direction.N)

    # l: balra fordul (W) és előrelép -> (1,2), W
    res = b.execute("l")
    assert b.position == Position(1, 2)
    assert b.direction == Direction.W
    assert res.blocked is False
    assert res.processed == 1
    assert res.remaining == ""

    # r: jobbra fordul (W -> N), előrelép -> (1,3), N
    res = b.execute("r")
    assert b.position == Position(1, 3)
    assert b.direction == Direction.N # vissza fordul N felé
    assert res.blocked is False

def test_forward_and_backward_work_as_before():
    planet = Moon(10, 10, [])
    b = Buggy(planet, Position(3, 3), Direction.N)

    res = b.execute("f")
    assert b.position == Position(3, 4)
    assert res.blocked is False

    # hátra egyet
    res = b.execute("b")
    assert b.position == Position(3, 3)
    assert res.blocked is False

def test_wraparound_edges_forward_and_backward():
    planet = Moon(5, 5, [])

    # West irány, f: x:0 -> wrap -> x:4
    b = Buggy(planet, Position(0, 2), Direction.W)
    res = b.execute("f")
    assert b.position == Position(4, 2)
    assert res.blocked is False

    # South irány, f: y:0 -> wrap -> y:4
    b = Buggy(planet, Position(1, 0), Direction.S)
    res = b.execute("f")
    assert b.position == Position(1, 4)
    assert res.blocked is False

    # East irány, f: x:4 -> wrap -> x:0
    b = Buggy(planet, Position(4, 1), Direction.E)
    res = b.execute("f")
    assert b.position == Position(0, 1)
    assert res.blocked is False

    # North irány, f: y:4 -> wrap -> y:0
    b = Buggy(planet, Position(3, 4), Direction.N)
    res = b.execute("f")
    assert b.position == Position(3, 0)
    assert res.blocked is False

    # backward wrap
    b = Buggy(planet, Position(0, 2), Direction.E)
    res = b.execute("b")  # nyugatra hátra -> wrap (4,2)
    assert b.position == Position(4, 2)
    assert res.blocked is False

def test_obstacle_blocks_and_reports_forward():
    planet = Moon(5, 5, obstacles=[(1, 0)])
    b = Buggy(planet, Position(0, 0), Direction.E)

    res = b.execute("f")
    assert b.position == Position(0, 0)
    assert res.blocked is True
    assert res.obstacles == Position(1, 0)
    assert res.processed == 0
    assert res.remaining == "f"
    assert res.direction == "E"

def test_move_left_turns_then_blocks_on_obstacle_but_keeps_new_direction():
    # N -> (turn left) W; célmező (1,2) akadály → nem lép, de irány W marad
    planet = Moon(5, 5, obstacles=[(1, 2)])
    b = Buggy(planet, Position(2, 2), Direction.N)
    res = b.execute("l")

    assert res.blocked is True
    assert res.obstacles == Position(1, 2)
    assert b.position == Position(2, 2)       # nem mozdult
    assert b.direction == Direction.W          # de már W felé néz
    assert res.processed == 0
    assert res.remaining == "l"

def test_stops_on_first_obstacle_in_sequence():
    planet = Moon(5, 5, obstacles=[(2, 2)])
    b = Buggy(planet, Position(0, 2), Direction.E)

    # első f sikerül (1,2), második f blokkol (2,2)
    res = b.execute("ffrff")
    assert b.position == Position(1, 2)
    assert res.blocked is True
    assert res.obstacles == Position(2, 2)
    assert res.processed == 1
    assert res.remaining == "frff"
    assert res.direction == "E"

def test_ignoring_unknown_orders():
    planet = Moon(5, 5, obstacles=[(2, 2)])
    b = Buggy(planet, Position(0, 0), Direction.E)

    res = b.execute("xlyrfz")
    # értelmezett: l (turn+step), y (ignore), r (turn+step), f (step)
    # DE: ha bármelyik blokkolna, megállunk – itt nincs akadály az útban
    assert res.blocked is False
    assert b.position != Position(0, 0)  # haladt
    assert res.remaining == ""

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

def test_sequence_of_turn_steps_cycles_cleanly():
    planet = Moon(5, 5, [])
    b = Buggy(planet, Position(2, 2), Direction.N)
    # l (->W, (1,2)), r (->N, (1,3)), r (->E, (2,3)), l (->N, (2,4))
    res = b.execute("lrrl")
    assert res.blocked is False
    assert res.processed == 4
    assert res.remaining == ""
    assert b.position == Position(2, 4)
    assert b.direction == Direction.N

def test_blocked_l_keeps_new_direction_across_calls():
    # akadály balra: (1,2)
    planet = Moon(5, 5, obstacles=[(1, 2)])
    b = Buggy(planet, Position(2, 2), Direction.N)

    # első hívás: 'l' blokkol (irány W megmarad, poz marad)
    res1 = b.execute("l")
    assert res1.blocked is True
    assert res1.obstacles == Position(1, 2)
    assert b.position == Position(2, 2)
    assert b.direction == Direction.W
    assert res1.processed == 0
    assert res1.remaining == "l"

    # második hívás: 'f' is blokkol ugyanazon akadályon, irány továbbra is W
    res2 = b.execute("f")
    assert res2.blocked is True
    assert res2.obstacles == Position(1, 2)
    assert b.position == Position(2, 2)
    assert b.direction == Direction.W
    assert res2.processed == 0
    assert res2.remaining == "f"

def test_blocked_l_with_wrap_target():
    # 5x5-ös világban (0,4)-ről 'l' -> W irány, cél (-1,4) wrap -> (4,4)
    planet = Moon(5, 5, obstacles=[(4, 4)])
    b = Buggy(planet, Position(0, 4), Direction.N)
    res = b.execute("l")
    assert res.blocked is True
    assert res.obstacles == Position(4, 4)
    assert b.position == Position(0, 4)
    assert b.direction == Direction.W  # új irány megmarad
    assert res.processed == 0
    assert res.remaining == "l"

def test_processed_and_remaining_counts_mixed_on_block():
    # útvonal: l (wrap miatt 4,0), f (3,0), f (2,0) <-- itt akadály
    planet = Moon(5, 5, obstacles=[(2, 0)])
    b = Buggy(planet, Position(0, 0), Direction.N)
    res = b.execute("lffrbx")
    # végállapot blokk a 3. értelmezett parancson (index 2: 'f')
    assert res.blocked is True
    assert b.position == Position(3, 0)   # az első f-ig jutott
    assert b.direction == Direction.W
    assert res.processed == 2             # 'l' és az első 'f'
    assert res.remaining == "frbx"
    assert res.obstacles == Position(2, 0)

def test_case_insensitivity_and_space_ignored():
    planet = Moon(5, 5, [])
    b = Buggy(planet, Position(2, 2), Direction.N)
    res = b.execute(" L  f  r B ")
    # lépések: L -> W,(1,2); f -> (0,2); r -> N,(0,3); B -> dél felé hátra (N-ből) -> (0,2)
    assert res.blocked is False
    assert b.position == Position(0, 2)
    assert b.direction == Direction.N
    assert res.processed == 4
    assert res.remaining == ""

def test_backward_blocks_on_direct_obstacle():
    planet = Moon(5, 5, obstacles=[(1, 2)])
    b = Buggy(planet, Position(2, 2), Direction.E)
    res = b.execute("b")
    assert res.blocked is True
    assert res.obstacles == Position(1, 2)
    assert b.position == Position(2, 2)
    assert b.direction == Direction.E
    assert res.processed == 0
    assert res.remaining == "b"

def test_unknowns_do_not_increase_processed_before_block():
    planet = Moon(5, 5, obstacles=[(1, 0)])
    b = Buggy(planet, Position(0, 0), Direction.E)
    res = b.execute("xxf")  # az 'f' blokkol azonnal
    assert res.blocked is True
    assert res.processed == 0   # az 'x'-ek nem növelik
    assert res.remaining == "f"
    assert res.obstacles == Position(1, 0)

