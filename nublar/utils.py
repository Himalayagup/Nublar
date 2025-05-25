def removing_slashes(path: str) -> str:
    """
    Remove leading and trailing slashes from the given path.

    This is useful when you want to normalize a file or directory path
    by removing unnecessary slashes at the beginning or end.

    :param path: The input path to be modified (string).
    :return: A new string with leading and trailing slashes removed.
    """
    # Strip leading and trailing slashes from the path
    return path.strip("/")  # Removes slashes from both ends of the string
