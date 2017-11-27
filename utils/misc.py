import os
from datetime import datetime


def get_dir(dir):
    """
    Creates the given directory (and recursively, parent directories)
    if it does not exist.

    :param dir: The path to the directory.
    :return: The path to the directory.
    """
    if not os.path.exists(dir):
        if dir[-1] == '/': dir = dir[:-1]  # To make rpartition logic work
        parent, _, child = dir.rpartition('/')
        os.makedirs(os.path.join(get_dir(parent), child))
    return dir


def date_str():
    """
    Gets the current date as a string. Used to create unique directory names.

    :return: A string of the format YYYY-MM-DD.hh:mm:ss'
    """
    # [:-7] cuts off microseconds.
    return str(datetime.now()).replace(' ', '.')[:-7]
