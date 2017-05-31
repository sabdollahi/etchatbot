"""Commonly required regular expressions."""
import re

import spacy

from pattern_match import errors
from util import test_util

NAME = r'(?P<first_name>[A-Z][a-z]*)(?P<last_name>\s[A-Z][a-z]*)?'


def name(user_input):
    """Determines if the user input matches a name pattern.

    Args:
      user_input: spacy doc of the user input.
    Returns:
      Boolean indicating whether the input matches the pattern
        for a name.
    Raises:
      ArgumentError: if the user_input is not a spacy doc.
    """
    errors.check_input(user_input)
    regex = r'^(?P<first_name>[A-Z][a-z]*)(?P<last_name>\s[A-Z][a-z]*)?$'
    return re.match(regex, user_input.text) is not None


def test_name():
    nlp = spacy.load('en')
    matches = [
        nlp('Tim'),
        nlp('Tim Niven')]
    non_matches = [
        nlp('TimNiven'),
        nlp('Tim  Niven')]
    test_util.test_matches(
        matches=matches,
        non_matches=non_matches,
        match_fn=name)


if __name__ == '__main__':
    test_name()
