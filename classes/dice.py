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

    def roll(self) -> int:
        result = random.randint(1, self._faces)
        logger.debug("Dice roll: faces=%s result=%s", self._faces, result)
        return result

    def roll_with_advantage(self) -> int:
        first = self.roll()
        second = self.roll()
        return max(first, second)

    def roll_with_disadvantage(self) -> int:
        first = self.roll()
        second = self.roll()
        return min(first, second)

