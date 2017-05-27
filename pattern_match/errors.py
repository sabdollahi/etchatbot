"""Custom errors for this module."""


class Error(Exception):
    """Base error class for custom errors."""
    pass


class ArgumentError(Error):
    """An invalid argument was passed.

    Attributes:
      argument_type: the type of the argument passed.
      expected_argument_type: the type expected.
    """

    def __init__(self, argument_type, expected_argument_type):
        self.argument_type = argument_type
        self.expected_argument_type = expected_argument_type
