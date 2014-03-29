from appdirs import AppDirs
import os
import pickle

dirs = AppDirs("Tron", "CS")
config_file = os.path.join(dirs.user_data_dir, 'config.pickle')


def load():
    if not os.path.exists(config_file):
        return False
    with open(config_file, 'r') as f:
        return pickle.load(f)


def save(config):
    if not os.path.exists(os.path.dirname(config_file)):
        os.makedirs(os.path.dirname(config_file))
    with open(config_file, 'w+') as f:
        pickle.dump(config, f)
