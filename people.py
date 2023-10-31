from typing import Optional, Any

from car import Car
from utils import Checkers, Position

class InsufficientFunds(Exception):
    def __init__(self, amount: float, client_name: str) -> None:
        super().__init__(f'{client_name} could not pay {amount}')

class Person:
    def __init__(self, name: str, balance: float, position: Optional[Position] = None) -> None:
        self.position = position if position else Position()
        self.name = name
        self.balance = balance
        self.__user_scores = []

    @property
    def position(self) -> Position:
        return self._position
    
    @position.setter
    def position(self, new_position: Position) -> None:
        Checkers.check_type(new_position, Position)
        self._position = new_position

    @property
    def balance(self) -> float:
        return self.__balance

    @balance.setter
    def balance(self, new_balance: float) -> None:
        if not isinstance(new_balance, float):
            raise TypeError(f'new balance value should be float, not {type(new_balance).__name__}')
        if new_balance < 0:
            raise ValueError(f'cannot set negative value as balance')
        self.__balance = new_balance

    @property
    def rating(self) -> float:
        last_rides = self.__user_scores[-40:]
        return round(sum(last_rides) / len(last_rides), 2) if self.__user_scores else 5.

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.name}, rating: {self.rating}'

class Client(Person):
    def pay(self, amount: float) -> None:
        if self.balance < amount:
            raise InsufficientFunds(amount, self.name)
        self.balance -= amount

class Driver(Person):
    __rating_per_class = 0.5

    def __init__(self, name: str, car: Car = None, position: Position = None) -> None:
        super().__init__(name, balance=0.0, position=position)
        self.car = car

    @staticmethod
    def check(driver: Any) -> None:
        Checkers.check_type(driver, Driver)

    @property
    def car(self) -> Car | None:
        return self._car

    @car.setter
    def car(self, new_car: Car) -> None:
        Checkers.check_type(new_car, Car)
        self._car = new_car

    @property
    def service_class(self) -> str:
        fine = int((5.0 - self.rating) // self.__rating_per_class)
        new_index = Car.service_classes.index(self.car.service_class) - fine
        return Car.service_classes[new_index] if new_index >= 0 else Car.service_classes[0]

    def __str__(self) -> str:
        return f'{super().__str__()} {self.car}'
