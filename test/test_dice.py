from classes.dice import Dice
import pytest


def test_dice_invalid_type():
    # Test string input
    with pytest.raises(TypeError, match="Number of faces must be an integer"):
        Dice("six")

    # Test boolean input
    with pytest.raises(TypeError, match="Number of faces must be an integer"):
        Dice(True)

    # Test float input
    with pytest.raises(TypeError, match="Number of faces must be an integer"):
        Dice(3.5)


def test_dice_invalid_faces_multiple():
    for invalid_faces in [0, 1, -5, 2, 5, 3, 70, 80, 95, 89, 15, 33]:
        with pytest.raises(ValueError):
            Dice(invalid_faces)


def test_roll(mocker):
    # Mock random.randint to always return 4
    mock_randint = mocker.patch("random.randint", return_value=4)
    dice = Dice(6)
    result = dice.roll()
    assert result == 4
    mock_randint.assert_called_once_with(1, 6)


def test_roll_with_advantage(mocker):
    # Mock random.randint to return 2 first, then 5
    mock_randint = mocker.patch("random.randint", side_effect=[2, 5])
    dice = Dice(6)
    result = dice.roll_with_advantage()
    assert result == 5
    assert mock_randint.call_count == 2


def test_roll_with_disadvantage(mocker):
    # Mock random.randint to return 6 first, then 1
    mock_randint = mocker.patch("random.randint", side_effect=[6, 1])
    dice = Dice(6)
    result = dice.roll_with_disadvantage()
    assert result == 1
    assert mock_randint.call_count == 2

