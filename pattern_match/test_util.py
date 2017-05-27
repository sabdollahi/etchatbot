"""Utilities for testing."""


def assertion(actual, expected, info):
    """Wrapper for assert that provides debug info.

    Args:
      actual: actual result (boolean).
      expected: expected result (boolean).
      info: info (string) to print for debugging.
    """
    if expected:
        try:
            assert actual
        except AssertionError:
            print('Assertion failed for: %s\n'
                  'Expected True; Actual False.' % info)
    else:
        try:
            assert not actual
        except AssertionError:
            print('Assertion failed for: %s\n'
                  'Expected False; Actual True.' % info)


def test_matches(matches, non_matches, match_fn):
    """Utility for testing against a regex.

    Args:
      matches: a list of spacy docs that should match the regex.
      non_matches: a list of spacy docs that should not
        match the regex.
      match_fn: the matching function to evaluate.
    """
    print('Testing matches for %s...' % match_fn.__name__)
    for doc in matches:
        assertion(match_fn(doc), True, doc.text)
    for doc in non_matches:
        assertion(match_fn(doc), False, doc.text)
    print('Testing completed.')
