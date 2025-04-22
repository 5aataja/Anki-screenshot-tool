import sys
import os

addon_dir = os.path.dirname(__file__)
deps_path = os.path.join(addon_dir, "dependencies")
if deps_path not in sys.path:
    sys.path.insert(0, deps_path)

import json

# load config
default_config = {"image_format": "webp", "field_name": "Screenshot"}
config_path = os.path.join(addon_dir, "config.json")
try:
    with open(config_path, "r", encoding="utf-8") as f:
        config = {**default_config, **json.load(f)}
except Exception:
    config = default_config

from aqt import mw
from aqt.utils import showInfo
from aqt.qt import QShortcut, QKeySequence
from aqt.qt import QBuffer, QIODevice
from datetime import datetime
from PIL import Image
import io



def capture_screenshot_as_format(fmt="webp"):
    # grab screen via qt
    screen = mw.app.primaryScreen()
    if not screen:
        showInfo("no screen found")
        return None

    qpix = screen.grabWindow(0)
    buffer = QBuffer()
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    qpix.save(buffer, "PNG")  # qt only gives raw formats like PNG or BMP

    pil_img = Image.open(io.BytesIO(buffer.data()))
    buffer.close()

    # convert and save
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"snap_{ts}.{fmt}"
    path = os.path.join(mw.col.media.dir(), fname)

    pil_img.save(path, format=fmt.upper())

    return fname

def add_screenshot_to_last_card():
    note_ids = mw.col.db.list("SELECT id FROM notes ORDER BY id DESC LIMIT 1")
    if not note_ids:
        showInfo("no notes found.")
        return

    note = mw.col.get_note(note_ids[0])
    img = capture_screenshot_as_format(config["image_format"])
    if not img:
        return

    field_idx = next((i for i, fld in enumerate(note.note_type()["flds"]) if fld["name"] == config["field_name"]), 0)
    note.fields[field_idx] += f'<img src="{img}">'
    note.flush()

    showInfo(f"screenshot added: {img}")

def setup_hotkey():
    QShortcut(QKeySequence("Ctrl+Shift+S"), mw).activated.connect(add_screenshot_to_last_card)
  
setup_hotkey()
