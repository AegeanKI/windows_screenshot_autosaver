from os import environ, rename, path, walk, remove
from shutil import move
from configparser import ConfigParser
from PIL.ImageGrab import grabclipboard

config_filename = "config.ini"

def get_monitored_directory():
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

def get_directory_information(directory_name):
    return next(walk(directory_name))

def get_absolute_path(filename):
    return path.abspath(path.join(path.dirname(__file__), filename))

def get_file_from_clipboard(filetype="PNG"):
    filename = f"tmp.{filetype}"
    img = grabclipboard()
    img.save(filename, filetype)
    return filename

def get_hotkeys():
    config_parser = get_config_parser()
    config = dict(config_parser.items("HOTKEYS"))
    return config

def delete_file(filename):
    remove(filename)