"""Matching input patterns for Task 1."""
import re
from pattern_match import common_regex, test_util, models, errors
import spacy
from util import pos


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
      Match object.
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
    return models.Match(user_input, match, user_name)


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
      Match object.
    """
    errors.check_input(user_input)
    r = r'^Nice to meet you, too(.)?'
    match = re.match(r, user_input.text) is not None
    return models.Match(user_input, match, None)


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
    - What about adjective modifiers for the state? very happy,
      super tired, not good, etc...?

    Args:
      user_input: the user input (string).

    Returns:
      Match objects.
    """
    r = r"^(I'm |I am )?(?P<state>([A-Z]{1}[a-z]*)|[a-z-]*)(, thank you|, thanks)?(.)?$"
    match = False
    state = None
    pattern_match = re.match(r, user_input.text)
    if pattern_match is not None:
        state = pattern_match.group(2)
        # state should be an adjective
        state_tok = next(t for t in user_input if t.text == state)
        if state_tok.tag_ in pos.ADJECTIVES:
            match = True
    return models.Match(user_input, match, state)


#
# Testing


def test_match_name(nlp):
    matches = [
        (nlp("My name's Tim."), 'Tim'),
        (nlp('My name is Bob'), 'Bob'),
        (nlp("It's Henry."), 'Henry'),
        (nlp('It is Frank'), 'Frank'),
        (nlp("I'm Hank"), 'Hank'),
        (nlp('I am Joe.'), 'Joe'),
        (nlp('Satan.'), 'Satan')]
    non_matches = [
        (nlp('What is your name?'), None),   # far out
        (nlp('My name is tim.'), None),      # missing capital
        (nlp('My nome it Tim'), 'Tim')]      # spelling mistakes
    test_util.test_matches(matches, non_matches, match_name)


def test_match_nice_to_meet_you(nlp):
    matches = [
        (nlp('Nice to meet you, too'), None),
        (nlp('Nice to meet you, too.'), None)]
    non_matches = [
        (nlp('Nice to meet you too'), None)]  # missing comma
    test_util.test_matches(matches, non_matches, match_nice_to_meet_you)


def test_match_how_are_you_response(nlp):
    matches = [
        (nlp('I am happy, thank you'), 'happy'),
        (nlp("I'm good, thanks"), 'good'),
        (nlp('I am fine.'), 'fine'),
        (nlp("I'm sad"), 'sad'),
        (nlp('Healthy, thank you.'), 'Healthy'),
        (nlp('Hungry'), 'Hungry'),
        (nlp('I am happy, thanks.'), '')]
    non_matches = [
        (nlp('I am banana, thank you.'), 'banana'),   # not an adjective
        (nlp('I am fine thank you.'), 'fine'),        # no comma
        (nlp('I am a small village near the sea, thank you.'), None)  # loco
    ]
    test_util.test_matches(matches, non_matches, match_how_are_you_response)


if __name__ == '__main__':
    # run all tests
    nlp = spacy.load('en')
    test_match_name(nlp)
    test_match_nice_to_meet_you(nlp)
    test_match_how_are_you_response(nlp)
