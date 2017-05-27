"""Matching input patterns for Task 1."""
import re
import common_regex
import test_util
import spacy


def match_name(user_input):
    """Match user input pattern for task 1.a.

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

    Issues:
    - Deal with punctuation - i.e. full stop?
    - What if they forget to capitalize their name?

    Args:
      user_input: the user input (string)
    Returns:
      Boolean indicating a match for the desired pattern(s).
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
    for r in regexs:
        if re.match(r, user_input.text):
            match = True
    return match


def match_nice_to_meet_you(user_input):
    """Match user input pattern for task 1.b.

    BOT: Nice to meet you.
    USR: Nice to meet you, too.

    Args:
      user_input: the user input (string).
    Returns:
      Boolean indicating a match for the desired pattern(s).
    """
    r = r'^Nice to meet you, too(.)?'
    return re.match(r, user_input.text) is not None


def match_how_are_you_response(user_input):
    """Match user input pattern for task 1.c

    BOT: How are you today?
    USR: [options]
    I am {state}(, thank you)?
    I'm {state}(, thank you)
    {state}(, thank you)
    [/options]

    There is a lot of potential variation in the state.
    Therefore make this a regex group, extract it, and process
    it separately.

    Acceptable states are defined as adjectives of less than
    15 characters.

    Args:
      user_input: the user input (string).
    Returns:
      Boolean indicating a match for the desired pattern(s).
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
