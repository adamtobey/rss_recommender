import os
import json
import pathlib

DATA_DIR = "data"

class Data(object):
    @staticmethod
    def load(*names):
        *dirs, name = names
        with open(os.path.join(DATA_DIR, *dirs, "{}.json".format(name))) as inf:
            return json.load(inf)

    @staticmethod
    def save(data, *names):
        *dirs, name = names
        path = os.path.join(DATA_DIR, *dirs, "{}.json".format(name))
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as outf:
            json.dump(data, outf)
