import os


def ensure_dir(path: str) -> None:
    """Create the directory if it does not exist.

    Args:
        path (str): Absolute path to the directory.
    """
    if not os.path.exists(path):
        os.makedirs(path)
