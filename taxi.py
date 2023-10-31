class InsufficientFunds(Exception):
    def __init__(self, amount: float, client) -> None:
        super().__init__(f'{client.name} could not pay {amount}')

class Client:
    def __init__(self, name: str, balance: float) -> None:
        self.name, self.balance = name, balance
        self.__user_scores = []

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

    def pay(self, amount: float) -> None:
        if self.balance < amount:
            raise InsufficientFunds(amount, self)
        self.balance -= amount

    @property
    def rating(self) -> float:
        last_rides = self.__user_scores[-40:]
        return round(sum(last_rides) / len(last_rides), 2) if self.__user_scores else 5.

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.name}, rating: {self.rating}'

class RegistrationNumber:
    def __init__(self, number: str, letters: str, region: int, country: str):
        self.number, self.letters, self.region, self.country = \
            number, letters, region, country

    def __str__(self) -> str:
        return f'{self.letters} {self.number} {self.region} {self.country}'

class Car:
    # NOTE debatable
    __service_classes = 'economy', 'comfort', 'comfort+', 'business', 'premium'

    def __init__(self, model: str, reg_number: str, service_class: str) -> None:
        self.model, self.reg_number, self.service_class = model, reg_number, service_class

    @property
    def service_class(self) -> str:
        return self._service_class
    
    @service_class.setter
    def service_class(self, new_class) -> None:
        if new_class not in self.__service_classes:
            raise ValueError(f'cannot set {new_class} class for car {self.model} {self.reg_number}')
        self._service_class = new_class

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.model} {self.reg_number} {self.service_class}'

vehlawseepehd = Car('АИСТ', RegistrationNumber('001', 'ГАМ', 123, 'RU'), 'economy')
print(vehlawseepehd)
