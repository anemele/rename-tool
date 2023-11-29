import glob
from itertools import chain
from os.path import isdir, isfile


def preprocess(func):
    def wrapper(*file: str, only_file: bool = False, only_dir: bool = False):
        file_list = chain.from_iterable(map(glob.iglob, file))
        if only_file:
            file_list = filter(isfile, file_list)
        if only_dir:
            file_list = filter(isdir, file_list)

        for f in file_list:
            func(f)

    return wrapper
