import time
import tools
from os import walk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CustomEventHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self._need_to_store = False
        self._paused = False

    def on_created(self, event):
        if self._paused:
            return
        filename = event.src_path
        if not filename.endswith(".png"):
            return
        self._need_to_store = not self._need_to_store
        if not self._need_to_store:
            return
        time.sleep(1)
        tools.rename_file(filename, self.get_new_filename())
    
    def get_new_filename(self):
        target_directory = tools.get_target_directory()
        _, _, files = next(walk(target_directory))
        return f"{target_directory}\{len(files)}.png"

    def toggle_paused(self):
        self._paused = not self._paused

class AutoSaver():
    def __init__(self):
        self._event_handler = CustomEventHandler()
        self._observer = Observer()
        self._observer.schedule(self._event_handler, tools.get_source_directory())

    def start(self):
        self._observer.start()

    def toggle_paused(self):
        self._event_handler.toggle_paused()

    def stop(self):
        self._observer.stop()
        self._observer.join()


if __name__ == "__main__":
    autosaver = AutoSaver()
    autosaver.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        autosaver.stop()