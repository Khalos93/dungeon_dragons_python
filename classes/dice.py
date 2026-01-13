import logging
import random

logger = logging.getLogger(__name__)


class Dice:
    faces_allowed = [4, 6, 8, 10, 12, 20, 100]

    def __init__(self, faces: int) -> None:

        if isinstance(faces, bool) or not isinstance(faces, int):
            raise TypeError(f"Number of faces must be an integer, got {type(faces).__name__}")

        if faces not in self.faces_allowed:
            raise ValueError("A dice must have have one of those 4, 6, 8, 10, 12, 20, 100 faces")

        self._faces = faces
        logger.debug("Dice created with %s faces", self._faces)

    @staticmethod
    def _validate_int(value, name):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an integer, got {type(value).__name__}")

    def roll(self, times: int = 1, modifier: int = 0) -> tuple[int, list[int]]:
        self._validate_int(times, "Number of times")
        self._validate_int(modifier, "Modifier")

        if times < 1:
            raise ValueError(f"Number of times must be a positive number, got {times}")

        rolls = []
        for _ in range(times):
            roll = random.randint(1, self._faces)
            rolls.append(roll)
            logger.debug("Dice roll: faces=%s result=%s modifier=%s", self._faces, roll, modifier)

        total = sum(rolls) + modifier
        if total < 1:
            total = 1
        return total, rolls

    def roll_with_advantage(self) -> tuple[int, list[int]]:
        first, first_rolls = self.roll()
        second, second_rolls = self.roll()
        if first > second:
            return first, first_rolls
        else:
            return second, second_rolls

    def roll_with_disadvantage(self) -> tuple[int, list[int]]:
        first, first_rolls = self.roll()
        second, second_rolls = self.roll()
        if first < second:
            return first, first_rolls
        else:
            return second, second_rolls

    def best_of(self, rolls: int, modifier: int) -> tuple[int, list[int]]:
        _, results = self.roll(times=rolls, modifier=modifier)

        higher_roll = max(results) + modifier
        if higher_roll < 1:
            higher_roll = 1

        logger.debug(
            "Best-of result: rolls=%s modifier=%s final=%s",
            results,
            modifier,
            higher_roll,
        )
        return higher_roll, results

    def worst_of(self, rolls: int, modifier: int) -> tuple[int, list[int]]:
        _, results = self.roll(times=rolls, modifier=modifier)

        lower_roll = min(results) + modifier
        if lower_roll < 1:
            lower_roll = 1

        logger.debug(
            "Worst-of result: rolls=%s modifier=%s final=%s",
            results,
            modifier,
            lower_roll,
        )
        return lower_roll, results
