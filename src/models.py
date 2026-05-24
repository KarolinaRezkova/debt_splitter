from dataclasses import dataclass

@dataclass
class Expense:
    id: str
    description: str
    amount: float
    paid_by: str      # Name of the person who paid
    involved: list[str]  # List of names sharing this expense

    @property
    def is_valid(self) -> bool:
        return self.amount > 0 and len(self.involved) > 0
