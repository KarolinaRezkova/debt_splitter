class DebtAppError(Exception):
    """Base exception for the debt splitter application."""
    pass

class MemberNotFoundError(DebtAppError):
    """Raised when looking up a group member that does not exist."""
    pass
