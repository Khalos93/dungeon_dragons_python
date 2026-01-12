from classes.dice import Dice
import pytest
from unittest.mock import call

INVALID_INPUT = ['six', True, False, 3.5, -79.9]


@pytest.mark.parametrize("invalid_input", INVALID_INPUT)
def test_dice_rejects_non_integer_parameters(invalid_input):
    with pytest.raises(TypeError, match="Number of faces must be an integer"):
        Dice(invalid_input)


INVALID_DND_DICE = [0, 1, -5, 2, 3, 5, 15, 33, 70, 80, 89, 95]


@pytest.mark.parametrize("invalid_faces", INVALID_DND_DICE)
def test_dice_rejects_non_standard_dnd_dice(invalid_faces):
    with pytest.raises(ValueError):
        Dice(invalid_faces)


def test_roll(mocker):
    # Mock random.randint to always return 4
    mock_randint = mocker.patch("random.randint", return_value=4)
    dice = Dice(6)
    result, _ = dice.roll()
    assert result == 4
    assert mock_randint.call_count == 1
    assert mock_randint.call_args == call(1, 6)


def test_roll_with_advantage(mocker):
    # Mock random.randint to return 2 first, then 5
    mock_randint = mocker.patch("random.randint", side_effect=[2, 5])
    dice = Dice(6)
    result, _ = dice.roll_with_advantage()
    assert result == 5
    assert mock_randint.call_count == 2
    assert mock_randint.call_args_list == [call(1, 6), call(1, 6)]


def test_roll_with_disadvantage(mocker):
    # Mock random.randint to return 6 first, then 1
    mock_randint = mocker.patch("random.randint", side_effect=[6, 1])
    dice = Dice(6)
    result, _ = dice.roll_with_disadvantage()
    assert result == 1
    assert mock_randint.call_count == 2
    assert mock_randint.call_args_list == [call(1, 6), call(1, 6)]


def test_a_dice_can_be_rolled_multiple_times(mocker):
    # Mock random.randint to always return 4
    mock_randint = mocker.patch("random.randint", side_effect=[4, 6, 2])
    dice = Dice(6)
    total, rolls = dice.roll(times=3)
    assert total == 12
    assert rolls == [4, 6, 2]
    assert mock_randint.call_count == 3


@pytest.mark.parametrize("mocked_roll,modifier,result", [
    [2, 4, 6],
    [4, 6, 10],
    [2, -1, 1],
    [3, -5, 1]
])
def test_a_dice_with_modifier(mocked_roll, modifier, result, mocker):
    mock_randint = mocker.patch("random.randint", return_value=mocked_roll)
    dice = Dice(6)
    total, _ = dice.roll(modifier=modifier)
    assert total == result
    assert mock_randint.call_count == 1


@pytest.mark.parametrize("mocked_rolls,roll_times,modifier,result", [
    [[2, 4, 18], 3, 0, 18],
    [[1, 20, 11, 8, 7], 5, 0, 20],
    [[14, 13, 6], 3, 1, 15],
    [[2, 4, 18], 3, -1, 17]
])
def test_a_dice_should_be_rolled_n_times_and_the_best_roll_should_be_picked(mocked_rolls, roll_times, modifier, result,
                                                                            mocker):
    mock_randint = mocker.patch("random.randint", side_effect=mocked_rolls)
    dice = Dice(20)
    higher_roll, rolls = dice.best_of(rolls=roll_times, modifier=modifier)
    assert higher_roll == result
    assert rolls == mocked_rolls
    assert mock_randint.call_count == roll_times


@pytest.mark.parametrize("mocked_rolls,roll_times,modifier,result", [
    [[2, 4, 18], 3, 0, 2],
    [[1, 20, 11, 16, 2], 5, 0, 1],
    [[14, 13, 6], 3, 1, 7],
    [[14, 13, 6], 3, -1, 5],
])
def test_a_dice_should_be_rolled_n_times_and_the_worst_roll_should_be_picked(mocked_rolls, roll_times, modifier, result,
                                                                             mocker):
    mock_randint = mocker.patch("random.randint", side_effect=mocked_rolls)
    dice = Dice(20)
    higher_roll, rolls = dice.worst_of(rolls=roll_times, modifier=modifier)
    assert higher_roll == result
    assert rolls == mocked_rolls
    assert mock_randint.call_count == roll_times
