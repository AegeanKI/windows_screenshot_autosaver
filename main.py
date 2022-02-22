import os
import time
import shutil
import configparser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

config_file = "config.ini"
username = os.environ.get("USERNAME")
source_directory = f"C:\\Users\\{username}\\AppData\\Local\\Packages\\MicrosoftWindows.Client.CBS_cw5n1h2txyewy\\TempState\ScreenClip"

class CustomEventHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.store = True
        self.config_parser = configparser.ConfigParser()

    def get_target_directory(self):
        self.config_parser.read(config_file, encoding="utf-8")
        config = dict(self.config_parser.items("DEFAULT"))
        return config["target_directory"]

    def on_created(self, event):
        filename = event.src_path
        if not filename.endswith(".png"):
            return
        self.store = not self.store
        if not self.store:
            return

        target_directory = self.get_target_directory()
        _, _, files = next(os.walk(target_directory))
        new_filename = f"{target_directory}\\{len(files)}.png"
        time.sleep(1)
        if source_directory[0] != target_directory[0]:
            shutil.move(filename, new_filename)
        else:
            os.rename(filename, new_filename)

if __name__ == "__main__":
    event_handler = CustomEventHandler()
    observer = Observer()
    observer.schedule(event_handler, source_directory)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()