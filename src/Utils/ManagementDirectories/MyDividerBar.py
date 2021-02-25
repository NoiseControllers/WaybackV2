import sys


def my_divider_bar():
    if sys.platform == "darwin":
        # for mac
        separator = "/"
    else:
        # for window
        separator = "\\"

    return separator
