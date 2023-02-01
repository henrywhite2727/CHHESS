import pytest
from numpy.random import randint
from ..src.game import objects


@pytest.fixture
def rand_pos():
    return objects.Position((randint(1, 8), randint(1, 8)), mode=1)


def test_Position__str__(rand_pos: objects.Position) -> None:
    assert str(rand_pos) == chr(rand_pos.file + ord("a") - 1) + str(rand_pos.rank)


def test_Position_index(rand_pos: objects.Position) -> None:
    assert rand_pos.index() == (rand_pos.rank - 1, rand_pos.file - 1)


def test_Position_err_0() -> None:
    with pytest.raises(ValueError):
        objects.Position((randint(9, 100), randint(9, 100)), mode=0)


def test_Position_err_1() -> None:
    with pytest.raises(ValueError):
        objects.Position((randint(9, 100), randint(9, 100)), mode=1)


def test_Position_err_2() -> None:
    with pytest.raises(ValueError):
        objects.Position((chr(randint(9, 100) + ord("a")), randint(9, 100)), mode=2)


def test_Position_err_3() -> None:
    with pytest.raises(ValueError):
        objects.Position("i4", mode=3)
