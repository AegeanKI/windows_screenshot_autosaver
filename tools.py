from os import environ, rename
from shutil import move
from configparser import ConfigParser

config_filename = "config.ini"

def get_source_directory():
    username = environ.get("USERNAME")
    return f"C:\\Users\{username}\AppData\Local\Packages\MicrosoftWindows.Client.CBS_cw5n1h2txyewy\TempState\ScreenClip"

def get_config_parser():
    config_parser = ConfigParser()
    config_parser.read(config_filename, encoding="utf-8")
    return config_parser

def get_target_directory():
    config_parser = get_config_parser()
    config = dict(config_parser.items("DEFAULT"))
    return config["target_directory"]

def update_target_directory(dir):
    config_parser = get_config_parser()
    config_parser.set("DEFAULT", "target_directory", dir)
    with open(config_filename, 'w+') as f:
        config_parser.write(f)

def rename_file(old_filename, new_filename):
    if old_filename[0] != new_filename[0]: # different disk
        move(old_filename, new_filename)
    else:
        rename(old_filename, new_filename)