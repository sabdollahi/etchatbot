"""Matching input patterns for Task 1."""
import re
from pattern_match import common_regex
from pattern_match import test_util
from pattern_match import errors
import spacy


def goal(number):
    """Interface for getting match method per goal.

    Usage from calling code:
    from pattern_match import match  # imports all task files
    is_match, info = match.task(1).goal(1)(user_input)

    Args:
      number: the goal number.

    Returns:
      function accepting a SpaCy document of user input,
        which returns a tuple (bool, info) containing a
        bool indicating whether the input is a match to
        the requirements, and optionally any info that
        needs to be extracted from the input.

    Raises:
      InvalidKeyError: if the goal number is not in the set of
        expected values.
    """
    goals = {
        1: match_name,
        2: match_nice_to_meet_you,
        3: match_how_are_you_response}
    if number not in goals.keys():
        raise errors.InvalidKeyError(number, goals.keys())
    return goals[number]


def match_name(user_input):
    """Match user input pattern for task 1.1.

    PATTERN MATCHED:
    BOT: What's your name?
    USR: [options]
    My name's ____.
    My name is ____.
    It's ____.
    It is ____.
    I'm ____.
    I am ____.
    ____.
    [/options]

    INFO RETURNED:
    The user's name.

    ISSUES:
    - Deal with punctuation - i.e. full stop?
    - What if they forget to capitalize their name?

    Args:
      user_input: the user input (string)

    Returns:
      is_match, info: Boolean indicating a match for the
        desired pattern(s); the user's name.
    """
    regexs = [
        r"^My name's %s(.)?$" % common_regex.NAME,
        r'^My name is %s(.)?$' % common_regex.NAME,
        r"^It's %s(.)?$" % common_regex.NAME,
        r'^It is %s(.)?$' % common_regex.NAME,
        r"^I'm %s(.)?$" % common_regex.NAME,
        r'^I am %s(.)?$' % common_regex.NAME,
        r'^%s(.)?$' % common_regex.NAME
    ]
    match = False
    user_name = None
    for r in regexs:
        match = re.match(r, user_input.text)
        if match:
            match = True
        if match:
            user_name = match.group(1)
    return match, user_name


def match_nice_to_meet_you(user_input):
    """Match user input pattern for task 1.2.

    PATTERN MATCHED:
    BOT: Nice to meet you.
    USR: Nice to meet you, too.

    INFO RETURNED:
    None.

    Args:
      user_input: the user input (string).

    Returns:
      is_match, info: Boolean indicating a match for the
        desired pattern(s); None.
    """
    errors.check_input(user_input)
    r = r'^Nice to meet you, too(.)?'
    return re.match(r, user_input.text) is not None, None


def match_how_are_you_response(user_input):
    """Match user input pattern for task 1.3.

    PATTERN MATCHED:
    BOT: How are you today?
    USR: [options]
    I am {state}(, thank you)?
    I'm {state}(, thank you)
    {state}(, thank you)
    [/options]

    INFO RETURNED:
    The user's state.

    ISSUES:
    - There is a lot of potential variation in the state.
      Therefore make this a regex group, extract it, and process
      it separately.
    - Acceptable states are defined as adjectives of less than
      15 characters.

    Args:
      user_input: the user input (string).

    Returns:
      is_match, info: Boolean indicating a match for the
        desired pattern(s); user state.
    """
    r = r"((I am)|(I'm))?(?P<state>[a-z]{,15})(, thank you)?(.)?"
    pattern_match = re.match(r, user_input.text)
    if pattern_match:
        state = pattern_match.group(1)

    return False


#
# Testing


def test_match_name():
    # test cases for match_name
    nlp = spacy.load('en')
    matches = [
        nlp("My name's Tim."),
        nlp('My name is Tim'),
        nlp("It's Tim."),
        nlp('It is Tim'),
        nlp("I'm Tim"),
        nlp('I am Tim.'),
        nlp('Tim.')]
    non_matches = [
        nlp('What is your name?'),  # far out
        nlp('My name is tim.'),     # missing capital, how to deal with this?
        nlp('My nome it Tim')]      # spelling mistakes
    test_util.test_matches(matches, non_matches, match_name)


def test_match_nice_to_meet_you():
    # test cases for match_nice_to_meet_you
    nlp = spacy.load('en')
    matches = [
        nlp('Nice to meet you, too'),
        nlp('Nice to meet you, too.')]
    non_matches = [
        nlp('Nice to meet you too')]  # missing comma
    test_util.test_matches(matches, non_matches, match_nice_to_meet_you)


if __name__ == '__main__':
    # run all tests
    test_match_name()
    test_match_nice_to_meet_you()