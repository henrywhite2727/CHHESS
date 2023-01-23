import pytest
from numpy.random import randint
from ..CHHESS.Chess import Board


@pytest.fixture
def rand_pos():
    return (randint(1, 8), randint(1, 8))


def test_pos_to_str(rand_pos):
    assert Board.pos_to_str(rand_pos) == chr(rand_pos[0] + ord("a") - 1) + str(
        rand_pos[1]
    )


def test_pos_to_str_err():
    with pytest.raises(ValueError):
        Board.pos_to_str((randint(9, 100), randint(9, 100)))


def test_str_to_pos(rand_pos):
    assert (
        Board.str_to_pos(chr(rand_pos[0] + ord("a") - 1) + str(rand_pos[1])) == rand_pos
    )


def test_str_to_pos_err():
    with pytest.raises(ValueError):
        Board.str_to_pos("i4")


def test_pos_to_ind(rand_pos):
    assert Board.pos_to_ind(rand_pos) == (rand_pos[1] - 1, rand_pos[0] - 1)


def test_ind_to_pos(rand_pos):
    assert Board.ind_to_pos((rand_pos[1] - 1, rand_pos[0] - 1)) == rand_pos
