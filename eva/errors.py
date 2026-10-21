"""Errors that describe invalid user requests, so callers can report them without crashing."""


class InvalidQueryError(ValueError):
    """Raised when what the user asked for cannot be answered (bad year, unknown country, ...)."""
