
class RegistrationNumber:
    def __init__(self, number: str, letters: str, region: int, country: str):
        self.number, self.letters, self.region, self.country = \
            number, letters, region, country

    def __str__(self) -> str:
        return f'{self.letters} {self.number} {self.region} {self.country}'
