from typing import Any, Self
import random
import math

class Checkers:
    @staticmethod
    def check_type(
            value: Any,
            classes: tuple[type] | type,
            message: str = 'value'
    ) -> None:
        if not isinstance(value, classes):
            if isinstance(classes, tuple):
                clnames = [class_.__name__ for class_ in classes]
            else:
                clnames = classes.__name__
            value_type = type(value).__name__
            raise TypeError(f'{message} should be instance of {clnames}, not {value_type}')

class Position:
    def __init__(self, x: float = 0., y: float = 0.) -> None:
        self.x, self.y = x, y

    @property
    def x(self) -> float:
        return self._x
    
    @x.setter
    def x(self, new_x) -> None:
        Checkers.check_type(new_x, float)
        self._x = new_x
    
    @property
    def y(self) -> float:
        return self._y
    
    @y.setter
    def y(self, new_y) -> None:
        Checkers.check_type(new_y, float)
        self._y = new_y

    def distance(self, other: Self) -> float:
        delta_x, delta_y = abs(self.x - other.x), abs(self.y - other.y)
        shortest = (delta_x ** 2 + delta_y ** 2) ** 0.5
        longest = delta_x + delta_y
        return round(random.uniform(shortest, longest), 3)

    def distance_with_traffic(self, other: Self) -> float:
        return self.distance(other) * random.choice([math.exp2(i / 100) for i in range(10, 350, 20)])
