from functools import reduce  # forward compatibility for Python 3
import operator
import os

def get_by_path(root, items):
    """
    Access a nested object in root by item sequence.
    https://stackoverflow.com/a/14692747/11878912
    """
    return reduce(operator.getitem, items, root)

def set_by_path(root, items, value):
    """
    Set a value in a nested object in root by item sequence.
    https://stackoverflow.com/a/14692747/11878912
    """
    get_by_path(root, items[:-1])[items[-1]] = value

def del_by_path(root, items):
    """
    Delete a key-value in a nested object in root by item sequence.
    https://stackoverflow.com/a/14692747/11878912
    """
    del get_by_path(root, items[:-1])[items[-1]]

def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    https://code.activestate.com/recipes/577879-create-a-nested-dictionary-from-oswalk/
    """
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir

    return dir