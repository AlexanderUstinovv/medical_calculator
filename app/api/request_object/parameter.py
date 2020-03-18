from typing import List


class UserParameter:
    def __init__(self, id: int, value: float):
        self.id = id
        self.value = value


class UserMedicalProcedure:
    def __init__(self, id: int, parameters: List[UserParameter]):
        self.id = id
        self.parameters = parameters


class UserMedicalProcedures:
    def __init__(self, procedures: List[UserMedicalProcedure]):
        self.procedures = procedures
