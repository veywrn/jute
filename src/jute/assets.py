import os
import sys


def _find_assets_dir(path, distance=2):
    targets = ('assets',)

    while distance >= 0 and os.path.isdir(path):
        for target in targets:
            test_path = os.path.join(path, target)
            if os.path.isdir(test_path):
                return test_path
        path = os.path.dirname(path)
        distance -= 1

    raise NotADirectoryError(path)


DIRECTORY = _find_assets_dir(os.path.dirname(os.path.realpath(sys.argv[0])))
