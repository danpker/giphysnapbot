"""Code for validating invocations against the rules."""


def number_of_words(string):
    """Return the number of words in a string.

    :param string: The string to check
    """
    return len(string.strip().split(" "))
