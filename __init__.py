from aqt import mw
from aqt.utils import showInfo
from aqt.qt import QShortcut, QKeySequence
import os

def capture_screenshot():
    # capture the whole screen using aqt's primary screen
    screen = mw.app.primaryScreen()
    if screen is None:
        showInfo("no screen found.")
        return None

    screenshot = screen.grabWindow(0)  # capture the whole screen
    
    # specify file format and name
    file_name = "screenshot.png"
    file_path = os.path.join(mw.col.media.dir(), file_name)
    
    # save the screenshot to anki's media folder
    screenshot.save(file_path, "PNG")
    
    return file_name

def add_screenshot_to_last_card():
    # get the last-added note
    note_ids = mw.col.db.list("SELECT id FROM notes ORDER BY id DESC LIMIT 1")
    if not note_ids:
        showInfo("no notes found.")
        return

    note = mw.col.get_note(note_ids[0])

    # capture screenshot and add it to the note
    img_file = capture_screenshot()
    if not img_file:
        return

    note.fields[0] += f'<img src="{img_file}">'  # assume field[0] is used
    note.flush()  # save changes
    
    showInfo("screenshot added to the last card.")

def setup_hotkey():
    # define a hotkey (e.g., Ctrl+Shift+S)
    shortcut = QShortcut(QKeySequence("Ctrl+Shift+S"), mw)
    shortcut.activated.connect(add_screenshot_to_last_card)

# set up the hotkey when the add-on loads
setup_hotkey()

