from src.models import Expense
from src.exceptions import MemberNotFoundError

class Group:
    def __init__(self, name: str):
        self.name = name
        self.members: set[str] = set()
        self.expenses: list[Expense] = []

    def add_member(self, name: str):
        """Adds a new member to the group."""
        if name:
            self.members.add(name.strip())

    def add_expense(self, expense: Expense):
        """Logs a new expense for the group."""
        # Flaw: Does not check if the expense is_valid using the model property.
        # Flaw: Does not verify if paid_by or involved people actually belong to self.members.
        self.expenses.append(expense)

    def remove_member(self, name: str) -> bool:
        """Removes a member from the group."""
        # Inconsistency: Returns a boolean status instead of throwing a MemberNotFoundError
        if name in self.members:
            self.members.remove(name)
            return True
        return False
