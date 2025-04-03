import os
import json
from aqt import mw
from aqt.utils import showInfo
from aqt.qt import QShortcut, QKeySequence
from .image_utils import capture_screenshot_with_pillow, convert_image

# path to the add-on's configuration file
CONFIG_PATH = os.path.join(mw.pm.addonFolder(), "your-addon-name", "config.json")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        default_config = {"image_field_name": "Front"}
        with open(CONFIG_PATH, "w") as f:
            json.dump(default_config, f, indent=4)
        return default_config
    
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def add_screenshot_to_last_card():
    # load configuration
    config = load_config()
    field_name = config.get("image_field_name", "Front")

    # get the last-added note
    note_ids = mw.col.db.list("SELECT id FROM notes ORDER BY id DESC LIMIT 1")
    if not note_ids:
        showInfo("no notes found.")
        return

    note = mw.col.get_note(note_ids[0])

    # find the field index by name
    try:
        field_index = note.model()["flds"].index(next(f for f in note.model()["flds"] if f["name"] == field_name))
    except StopIteration:
        showInfo(f"field '{field_name}' not found in the note model.")
        return

    # capture and convert screenshot
    try:
        raw_image = capture_screenshot_with_pillow()
        output_path = os.path.join(mw.col.media.dir(), "screenshot.png")
        convert_image(raw_image, output_path)  # apply pillow processing
    except Exception as e:
        showInfo(f"error capturing or converting screenshot: {e}")
        return

    # add the image to the note
    note.fields[field_index] += f'<img src="screenshot.png">'
    note.flush()  # save changes
    
    showInfo(f"screenshot added to field '{field_name}'.")

def setup_hotkey():
    shortcut = QShortcut(QKeySequence("Ctrl+Shift+S"), mw)
    shortcut.activated.connect(add_screenshot_to_last_card)

# set up the hotkey when the add-on loads
setup_hotkey()

