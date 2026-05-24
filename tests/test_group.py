import pytest
from src.group import Group
from src.models import Expense


def test_add_expense_without_validation_bug():
    group = Group("Ski Trip")
    group.add_member("Alice")

    # An invalid expense (negative money, empty group) shouldn't be allowed
    bad_expense = Expense("e1", "Fake Entry", -50.0, "Alice", [])
    group.add_expense(bad_expense)

    assert len(group.expenses) == 1
