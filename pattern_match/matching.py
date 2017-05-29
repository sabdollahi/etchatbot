"""Interface module for tasks pattern matching and info extraction."""
from pattern_match import errors
from pattern_match import task1


def match_and_info(task_number, goal_number, user_input):
    """Public interface for pattern_match module.

    Args:
      task_number: the number of the task desired.
      goal_number: the number of the goal desired.
      user_input: Spacy doc of the user input to process.

    Returns:
      Match object.
    """
    errors.check_input(user_input)
    return __task(task_number).goal(goal_number)(user_input)


def __task(number):
    """Private interface for getting tasks by number.

    Usage from calling code:
    from pattern_match import match
    is_match, info = match.task(1).goal(1)(user_input)

    Args:
      number: the task number sought.

    Returns:
      Module containing matching code for the task. The intended
        usage is to call goal(number) on this module.

    Raises:
      InvalidKeyError: if the number passed is not in the set of
        expected task numbers.
    """
    tasks = {
        1: task1}
    if number not in tasks.keys():
        raise errors.InvalidKeyError(number, tasks.keys())
    return tasks[number]
