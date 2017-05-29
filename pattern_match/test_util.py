"""Utilities for testing."""


def assertion(actual, expected, info):
    """Wrapper for assert that provides debug info.

    Args:
      actual: actual result.
      expected: expected result.
      info: info (string) to print for debugging.
    """
    try:
        assert actual == expected
    except AssertionError:
        print('Assertion failed for: %s\n'
              'Actual: %s'
              'Expected: %s' % (info, actual, expected))


def test_matches(matches, non_matches, match_fn):
    """Utility for testing against a regex.

    Decided at this stage not to evaluate info for
    non-match classes. They are not evaluated by the
    individual functions in case of a non-match anyway.

    Args:
      matches: a list of tuples (spacy doc, info) that
        should match the regex, and be the info extracted.
      non_matches: a list of tuples (spacy doc, info) that
        should not match the regex.
      match_fn: the matching function to evaluate.
    """
    print('Testing matches for %s...' % match_fn.__name__)
    for user_input, info in matches:
        result = match_fn(user_input)
        assertion(result.match, True, user_input.text)
        assertion(info, result.info, user_input.text)
    for user_input, info in non_matches:
        result = match_fn(user_input)
        assertion(result.match, False, user_input.text)
    print('Testing completed.')
