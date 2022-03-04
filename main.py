import tools
import keyboard 
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CustomEventHandler(FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self._paused = False
        self._previous_file = None

    def on_created(self, event):
        if self._paused or not event.src_path.endswith(".json"):
            return
        filename = tools.get_file_from_clipboard()
        new_filename = self.get_new_filename()
        tools.rename_file(filename, new_filename)
        self._previous_file = new_filename

    def get_new_filename(self):
        target_directory = tools.get_target_directory()
        _, _, files = tools.get_directory_information(target_directory)
        return f"{target_directory}\{len(files)}.png"

    def toggle_paused(self):
        self._paused = not self._paused

class AutoSaver():
    def __init__(self):
        self._event_handler = CustomEventHandler()
        self._observer = Observer()
        self._observer.schedule(self._event_handler, tools.get_monitored_directory())
        hotkeys = tools.get_hotkeys()
        keyboard.add_hotkey(hotkeys["delete_previous"], self.delete_previous) 
        keyboard.add_hotkey(hotkeys["toggle_paused"], self.toggle_paused)

    def start(self):
        self._observer.start()

    def toggle_paused(self):
        self._event_handler.toggle_paused()

    def delete_previous(self):
        if not self._event_handler._previous_file:
            return
        tools.delete_file(self._event_handler._previous_file)
        self._event_handler._previous_file = None

    def stop(self):
        self._observer.stop()
        self._observer.join()

    def get_status(self):
        return self._event_handler._paused