from PIL import Image, ImageOps
import os
from aqt import mw

def capture_screenshot_with_pillow():
    # capture the screen using anki's primary screen
    screen = mw.app.primaryScreen()
    if screen is None:
        raise RuntimeError("no screen found.")
    
    screenshot = screen.grabWindow(0)  # grab the entire screen
    temp_path = os.path.join(mw.pm.addonFolder(), "screenshot_temp.png")
    screenshot.save(temp_path, "PNG")  # save temporary raw screenshot
    
    # open the temporary screenshot with pillow
    image = Image.open(temp_path)
    os.remove(temp_path)  # remove the temporary file after opening
    return image

def convert_image(image, output_path, format="PNG"):
    # example: convert to grayscale and resize (customize as needed)
    image = ImageOps.grayscale(image)
    image = image.resize((800, 600))  # resizing to 800x600
    
    # save the converted image
    image.save(output_path, format)

