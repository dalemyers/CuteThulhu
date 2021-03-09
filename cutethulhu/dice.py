import random
from typing import Optional

random.seed()


class Die:
    def __init__(
        self, max: int, *, min: Optional[int] = 1, step: Optional[int] = 1
    ) -> None:
        self.max = max
        self.min = min
        self.step = step

    def roll(self) -> int:
        return random.randrange(self.min, self.max, self.step)


class D10P(Die):
    def __init__(self):
        super().__init__(max=100, min=0, step=10)


class D10(Die):
    def __init__(self) -> None:
        super().__init__(10)

d10 = D10()
d10p = D10P()
