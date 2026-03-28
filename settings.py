import os
from PIL import Image

TRAY_IMAGE_PATH = os.path.join("tray.png")
TRAY_IMAGE = Image.open(TRAY_IMAGE_PATH).convert("RGBA")

TEMP_SAVE_DIR = os.path.join("temp")
TEMP_IMAGE_STYLE = lambda x: "frames_{:05f}".format(x)


FPTS = 30 # frames per timelapse second
RSPF = 2 # real seconds between frames
print("SETTINGS: [INFO] 1 timelapse second is {} real seconds".format(RSPF*FPTS))