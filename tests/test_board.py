import pytest
from Chess import Board


def test_pos_to_str():
    assert Board.pos_to_str((4, 5)) == "d5"


def test_pos_to_str_err():
    with pytest.raises(ValueError):
        Board.pos_to_str((9, 2))
