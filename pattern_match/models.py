"""Useful classes for pattern_match module."""
from pattern_match import errors


class Match:
    """Class to wrap info from match functions.

    Attributes:
      user_input: SpaCy doc input pattern.
      match: Bool indicating whether the pattern was a match.
      info: String info extracted from the answer where available;
        else None.
    """

    def __init__(self, user_input, match, info):
        errors.check_input(user_input)
        self.input = input
        self.match = match
        self.info = info
