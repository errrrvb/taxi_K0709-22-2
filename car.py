class Car:
    service_classes = 'economy', 'comfort', 'comfort+', 'business', 'premium'

    def __init__(self, model: str, reg_number: str, service_class: str) -> None:
        self.model, self.reg_number, self.service_class = model, reg_number, service_class

    @property
    def service_class(self) -> str:
        return self._service_class
    
    @service_class.setter
    def service_class(self, new_class) -> None:
        if new_class not in self.service_classes:
            raise ValueError(f'cannot set {new_class} class for car {self.model} {self.reg_number}')
        self._service_class = new_class

    def __str__(self) -> str:
        return f'{self.__class__.__name__} {self.model} {self.reg_number} {self.service_class}'
