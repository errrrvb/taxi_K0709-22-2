import random
import time

from car import Car
from people import Client, Driver
from utils import Position, Checkers

class Ride:
    __km_cost = 80

    def __init__(
            self,
            client: Client,
            driver: Driver,
            destination: Position,
    ) -> None:
        self.client, self.driver, self.destination = client, driver, destination
        self._start, self._end = None, None
        self.__time_exception = type('TimeAlreadyDefined', (Exception,), {})
        self.__set_cost()
    
    def __set_cost(self) -> None:
        coeff = 1 + Car.service_classes.index(self.driver.service_class) / 10
        self.cost = round(self.client.position.distance(self.destination) * self.__km_cost * coeff, 2)

    def raise_time(self, msg: str) -> None:
        raise self.__time_exception(f'ride {msg} has already been defined')

    def start(self) -> None:
        if self._start:
            self.raise_time('start')
        self._start = time.time()

    def end(self) -> None:
        if self._end:
            self.raise_time('end')
        self._end = time.time()

    @property
    def duration(self) -> float | None:
        if self._end and self._start:
            return self._end - self._start
        return None

    def __str__(self) -> str:
        ride = f'Ride for {self.client.name} with {self.driver} to {self.destination}'
        duration = f'{self.duration} seconds long' if self.duration else ''
        return f'{ride} {duration}'


class Taxi:
    __rating_max_diff = 0.4
    __tax_rate = 0.13
    __acceptance_prob = 80

    def __init__(self) -> None:
        self.__drivers = []
        self.__clients = []
        self.__rides = []
        self.__archive_rides = []
        self.__taxes, self.__profit = 0, 0

    @property
    def drivers(self) -> list[Driver]:
        return self.__drivers

    @drivers.setter
    def drivers(self, new_drivers: list[Driver]) -> None:
        for driver in new_drivers:
            Checkers.check_type(driver, Driver)
        self.__drivers = new_drivers

    def add_driver(self, driver: Driver) -> None:
        Checkers.check_type(driver, Driver)
        self.__drivers.append(driver)

    def remove_driver(self, driver: Driver) -> None:
        Checkers.check_type(driver, Driver)
        if driver not in self.__drivers:
            raise ValueError(f'driver {driver.name} is not present in taxi drivers')
        self.__drivers.remove(driver)

    @property
    def clients(self) -> list[Client]:
        return self.__clients

    @clients.setter
    def clients(self, new_clients: list[Client]) -> None:
        for client in new_clients:
            Checkers.check_type(client, Client)
        self.__clients = new_clients

    def add_client(self, client: Client) -> None:
        Checkers.check_type(client, Client)
        self.__clients.append(client)

    def remove_client(self, client: Client) -> None:
        Checkers.check_type(client, Client)
        if client not in self.__clients:
            raise ValueError(f'Client {client.name} is not present in taxi clients')
        self.__clients.remove(client)

    def find_driver(self, client: Client) -> Driver:
        def priority(driver: Driver) -> float:
            dist = client.position.distance(driver.position)
            rating_delta = abs(client.rating - driver.rating)
            return dist / 10 + dist * rating_delta

        lower, upper = client.rating - self.__rating_max_diff, client.rating + self.__rating_max_diff
        fst_priority, snd_priority = [], []
        for driver in self.__drivers:
            if driver.rating < upper and driver.rating > lower:
                fst_priority.append(driver)
            else:
                snd_priority.append(driver)

        for drivers in fst_priority, snd_priority:
            drivers = sorted(drivers, key=priority)
            for driver in drivers:
                if random.randint(0, 99) < self.__acceptance_prob:
                    return driver
        return None

    def process_ride(self, client: Client, destination: Position) -> None:
        driver = self.find_driver(client)
        ride = Ride(client, driver, destination)
        self.__rides.append(ride)
        print(ride)

        ride.start()
        time.sleep(Position.distance(client.position, ride.destination) // 10)
        ride.end()

        client.pay(ride.cost)
        salary = round(ride.cost / 2, 2)
        tax = round(salary * self.__tax_rate, 2)
        self.__taxes += tax
        driver.balance += salary - tax
        self.__profit += ride.cost - salary

        self.__rides.remove(ride)
        self.__archive_rides.append(ride)

from car import RegistrationNumber

taxi = Taxi()
reg = RegistrationNumber('123', 'СВД', 123, 'RU')
names = ['Никифоров', 'Роганов', 'Цверкунов']
drivers = []
i = 0
for name in names:
    drivers.append(Driver(name, Car('Tesla', reg, 'comfort'), Position(float(i), float(i))))
    i += 1
client = Client('Маланин', 1000.)
taxi.add_client(client)
taxi.drivers = drivers
taxi.process_ride(client, Position(3., 3.))
