import os

def get_dir(directory):
    """
    Creates the given directory if it does not exist.

    :param directory: The path to the directory.
    :return: The path to the directory.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory
