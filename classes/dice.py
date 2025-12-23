import logging
import random

logger = logging.getLogger(__name__)


class Dice:

    def __init__(self, _faces: int) -> None:

        faces_allowed = [4, 6, 8, 10, 12, 20, 100]

        if isinstance(_faces, bool) or not isinstance(_faces, int):
            raise TypeError(f"Number of faces must be an integer, got {type(_faces).__name__}")

        if _faces not in faces_allowed :
            raise ValueError("A dice must have have one of those 4, 6, 8, 10, 12, 20, 100 faces")

        self.faces = _faces
        logger.debug("Dice created with %s faces", self.faces)

    def roll(self) -> int:
        result = random.randint(1, self.faces)
        logger.debug("Dice roll: faces=%s result=%s", self.faces, result)
        return result

    def roll_with_advantage(self) -> int:
        first = self.roll()
        second = self.roll()
        return max(first, second)

    def roll_with_disadvantage(self) -> int:
        first = self.roll()
        second = self.roll()
        return min(first, second)

