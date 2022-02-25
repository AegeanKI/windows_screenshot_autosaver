To package into EXE, use the `pyinstaller` command as below
```py
pyinstaller -n screenautosaver -w --onefile --add-data="images/bitmaps/auto.png;." --add-data="images/icons/icon_wxWidgets.ico;." --icon="images/icons/auto.ico" gui.py
```