"""Code for validating invocations against the rules."""


DUPLICATE_TERM = "You cannot use the same invocation twice!"
TERM_LENGTH = "You must invoke using two words!"
REPEAT_WORD = "You cannot repeat a word!"
ILLEGAL_WORD = "You have used an illegal word!"


def is_violation(previous_term, current_term):
    """Return whether the `current_term` breaks any rules."""
    if previous_term == current_term:
        return DUPLICATE_TERM

    if number_of_words(current_term) != 2:
        return TERM_LENGTH

    if any_match(previous_term, current_term):
        return REPEAT_WORD

    if illegal_words(current_term):
        return ILLEGAL_WORD


def number_of_words(string):
    """Return the number of words in a string.

    :param string: The string to check
    """
    return len(string.split())


def any_match(first_string, second_string):
    """Return whether two strings share a word.

    :param first_string: The first string to check
    :param second_string: The second string to check
    """
    if first_string is None or second_string is None:
        return False
    for first_word in first_string.strip().split(" "):
        for second_word in second_string.strip().split(" "):
            if first_word == second_word:
                return True
    return False


ILLEGAL_WORDS = [
    "taylor",
    "swift",
]


def illegal_words(string):
    """Return wether `string` contains an illegal word.

    :param string:
    """
    for word in string.strip().split(" "):
        if word.lower() in ILLEGAL_WORDS:
            return True
    return False
