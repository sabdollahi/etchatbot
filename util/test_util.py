"""Utilities for testing."""


def assertion(actual, expected, info):
    """Wrapper for assert that provides debug info.

    Args:
      actual: actual result.
      expected: expected result.
      info: info (string) to print for debugging.
    """
    success = False
    try:
        assert actual == expected
        success = True
    except AssertionError:
        print('Assertion failed for: %s\n'
              'Actual: %s\n'
              'Expected: %s' % (info, actual, expected))
    return success


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
    print('------\nTesting matches for %s...' % match_fn.__name__)
    success = True
    for user_input, info in matches:
        result = match_fn(user_input)
        s1 = assertion(result.match, True, user_input.text)
        s2 = assertion(info, result.info, user_input.text)
        if not s1 or not s2:
            success = False
    for user_input in non_matches:
        result = match_fn(user_input)
        s1 = assertion(result.match, False, user_input.text)
        if not s1:
            success = False
    if success:
        print('*** OK ***\n')
    else:
        print('*** FAILED ***\n')
