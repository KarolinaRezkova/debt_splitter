import pytest
from src.group import Group
from src.models import Expense
from src.calculator import DebtCalculator
from src.calculator import AdvancedDebtCalculator


def test_calculate_balances_basic():
    group = Group("Flatmates")
    group.add_member("Alice")
    group.add_member("Bob")
    group.add_member("Charlie")

    # Alice paid 90 for internet shared by everyone (30 each)
    # Alice net: +60, Bob net: -30, Charlie net: -30
    exp = Expense("e1", "Internet", 90.0, "Alice", ["Alice", "Bob", "Charlie"])
    group.add_expense(exp)

    calc = DebtCalculator(group)
    balances = calc.calculate_balances()

    assert balances["Alice"] == 60.0
    assert balances["Bob"] == -30.0
    assert balances["Charlie"] == -30.0


def test_advanced_calculator_weighted_split():
    group = Group("Dinner")
    group.add_member("Alice")
    group.add_member("Bob")

    # Alice paid 120, but Bob ate twice as much (Alice weight 1, Bob weight 2)
    # Alice should pay: 120 * (1/3) = 40. Bob should pay: 120 * (2/3) = 80.
    # Alice net: 120 - 40 = +80. Bob net: 0 - 80 = -80.
    exp = Expense("e_weight", "Steaks", 120.0, "Alice", ["Alice", "Bob"])
    group.add_expense(exp)

    calc = AdvancedDebtCalculator(group)
    custom_weights = {
        "e_weight": {"Alice": 1.0, "Bob": 2.0}
    }

    balances = calc.calculate_weighted_balances(custom_weights)
    assert balances["Alice"] == 80.0
    assert balances["Bob"] == -80.0


def test_advanced_calculator_percentage():
    group = Group("Roadtrip")
    group.add_member("Alice")
    group.add_member("Bob")

    exp = Expense("e_pct", "Fuel", 100.0, "Alice", ["Alice", "Bob"])
    group.add_expense(exp)

    calc = AdvancedDebtCalculator(group)
    percentages = {
        "e_pct": {"Alice": 0.5, "Bob": 0.5}
    }

    balances = calc.calculate_percentage_balances(percentages)

    # Alice paid 100, owes 50 -> net +50
    assert balances["Alice"] == 50.0
    # Bob owes 50 -> net -50
    assert balances["Bob"] == -50.0

