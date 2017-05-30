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
      user_input: the user input (SpaCy doc)

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
    info = None
    for r in regexs:
        pattern_match = re.match(r, user_input.text)
        if pattern_match:
            match = True
            info = pattern_match.group(1)
    return models.Match(user_input, match, info)


def match_nice_to_meet_you(user_input):
    """Match user input pattern for task 1.2.

    PATTERN MATCHED:
    BOT: Nice to meet you.
    USR: Nice to meet you, too.

    INFO RETURNED:
    None.

    Args:
      user_input: the user input (SpaCy doc).

    Returns:
      Match object.
    """
    r = r'^Nice to meet you, too(.)?'
    match = False
    info = None
    if re.match(r, user_input.text):
        match = True
    return models.Match(user_input, match, info)


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
      user_input: the user input (SpaCy doc).

    Returns:
      Match objects.
    """
    r = r"^(I'm |I am )?" \
        r"(?P<state>([A-Z]{1}[a-z]*)|[a-z-]*)" \
        r"(, thank you|, thanks)?(.)?$"
    match = False
    info = None
    pattern_match = re.match(r, user_input.text)
    if pattern_match is not None:
        info = pattern_match.group(2)
        # state should be an adjective
        state_tok = next(t for t in user_input if t.text == info)
        if state_tok.tag_ in pos.ADJECTIVES:
            match = True
    return models.Match(user_input, match, info)


def match_where_are_you_from_response(user_input):
    """Match user input pattern for task 1.4.

        PATTERN MATCHED:
        BOT: Where are you from?
        USR: [options]
        I am from {Place}
        I'm from {Place}
        {Place}
        [/options]

        INFO RETURNED:
        Where the user is from.

        ISSUES:
        - What if the respond with an ethnicity: e.g. I'm Taiwanese?
        - To really validate this input we need to make sure they
          say a place, e.g. "Taiwan", and not something silly like
          "Earth".

        Args:
          user_input: the user input (SpaCy doc).

        Returns:
          Match objects.
        """
    r = r"$(I'm from |I am from )?%s(.)?^" % common_regex.NAME  # same as place
    match = False
    info = None
    pattern_match = re.match(r, user_input.text)
    if pattern_match:
        match = True
        info = pattern_match.group(2)
    return models.Match(user_input, match, info)

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
        nlp('What is your name?'),   # far out
        nlp('My name is tim.'),      # missing capital
        nlp('My nome it Tim')]      # spelling mistakes
    test_util.test_matches(matches, non_matches, match_name)


def test_match_nice_to_meet_you(nlp):
    matches = [
        (nlp('Nice to meet you, too'), None),
        (nlp('Nice to meet you, too.'), None)]
    non_matches = [
        nlp('Nice to meet you too')]  # missing comma
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
        nlp('I am banana, thank you.'),                        # not an adj.
        nlp('I am fine thank you.'),                           # no comma
        nlp('I am a small village near the sea, thank you.')]  # loco
    test_util.test_matches(matches, non_matches, match_how_are_you_response)


def test_match_where_are_your_from_response(nlp):
    matches = [
        (nlp('I am from New Zealand'), 'New Zealand'),
        (nlp("I'm from Taiwan."), 'Taiwan'),
        (nlp('Iran.'), 'Iran')]
    non_matches = [
        nlp('I am an elephant'),
        nlp('I am Taiwan.'),
        nlp('I am from taiwan')]
    test_util.test_matches(matches,
                           non_matches,
                           match_where_are_you_from_response)
