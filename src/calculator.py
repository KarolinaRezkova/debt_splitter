from src.group import Group
from src.models import Expense


class DebtCalculator:
    """Calculates basic net balances and simplifies payments between members."""

    def __init__(self, group: Group):
        self.group = group

    def calculate_balances(self) -> dict[str, float]:
        """Calculates the net balance for each person using equal split."""
        balances = {member: 0.0 for member in self.group.members}

        for expense in self.group.expenses:
            balances[expense.paid_by] += expense.amount
            split_amount = expense.amount / len(expense.involved)

            for person in expense.involved:
                balances[person] -= split_amount

        return {k: round(v, 2) for k, v in balances.items()}


class AdvancedDebtCalculator(DebtCalculator):
    """Advanced calculator supporting custom weights and percentage splits."""

    def calculate_weighted_balances(self, weights: dict[str, dict[str, float]]) -> dict[str, float]:
        """Calculates balances based on custom weights for each expense.

        'weights' format: { expense_id: { member_name: weight_number } }
        Example: {"exp1": {"Alice": 2, "Bob": 1}} -> Alice pays 2/3, Bob pays 1/3.
        """
        balances = {member: 0.0 for member in self.group.members}

        for expense in self.group.expenses:
            balances[expense.paid_by] += expense.amount

            # Flaw: If an expense ID is missing from the weights dictionary,
            # it crashes with a raw KeyError instead of falling back to equal split.
            expense_weights = weights[expense.id]
            total_weight = sum(expense_weights.values())

            # Critical Bug: Division by zero if total weight is 0.0
            for person in expense.involved:
                # Flaw: Crashes if a person in 'involved' is not defined in the weights dict
                person_weight = expense_weights[person]
                share = expense.amount * (person_weight / total_weight)
                balances[person] -= share

        return {k: round(v, 2) for k, v in balances.items()}

    def calculate_percentage_balances(self, percentages: dict[str, dict[str, float]]) -> dict[str, float]:
        """Calculates balances based on exact percentages.

        'percentages' format: { expense_id: { member_name: percentage_value } }
        Example: {"exp1": {"Alice": 0.60, "Bob": 0.40}} -> 60% and 40%.
        """
        balances = {member: 0.0 for member in self.group.members}

        for expense in self.group.expenses:
            balances[expense.paid_by] += expense.amount
            expense_pct = percentages.get(expense.id, {})

            # Inconsistency & Flaw: It doesn't validate if the sum of percentages equals 1.0 (100%).
            # If the user provides 0.40 and 0.40 (total 80%), money just magically disappears.
            for person in expense.involved:
                pct = expense_pct.get(person, 0.0)
                balances[person] -= expense.amount * pct

        # Inconsistency: Unlike other methods, this one forgets to round the final float numbers,
        # leading to ugly floating-point representation bugs (e.g., -33.333333333335).
        return balances
