import os
from PIL import Image

TRAY_IMAGE_PATH = os.path.join("tray.png")
TRAY_IMAGE = Image.open(TRAY_IMAGE_PATH).convert("RGBA")

TEMP_SAVE_DIR = lambda x, y: os.path.join("temp", x) if y==None else os.path.join("temp", x, y)
TEMP_IMAGE_STYLE = lambda x: "frames_{:05d}".format(x)
OUT_SAVE_DIR = lambda x: os.path.join("out") if x==None else os.path.join("out", x)


FPTS = 30 # frames per timelapse second
RSPF = 1/FPTS # real seconds between frames
print("SETTINGS: [INFO] 1 timelapse second is {} real seconds".format(RSPF*FPTS))