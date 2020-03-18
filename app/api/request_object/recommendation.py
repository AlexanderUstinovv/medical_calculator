from typing import List


class Parameter:
    def __init__(self, id: int, name: str, measurement: str):
        self.id = id
        self.name = name
        self.measurement = measurement


class Recommendation:
    def __init__(self, id: int, name: str, parameters: List[Parameter]):
        self.id = id
        self.name = name
        self.parameters = parameters


class Recommendations:
    def __init__(self, recommendations: list):
        self.recommendations = recommendations
