import os
from PIL import Image

TRAY_IDLE_IMAGE = Image.open(os.path.join("trayIdle.png")).convert("RGBA")
TRAY_ACTIVE_IMAGE_1 = Image.open(os.path.join("trayActive1.png")).convert("RGBA")
TRAY_ACTIVE_IMAGE_2 = Image.open(os.path.join("trayActive2.png")).convert("RGBA")

OUT_SAVE_DIR = lambda x: os.path.join("out") if x==None else os.path.join("out", x)


FPTS = 30 # frames per timelapse second
RSPF = 0.5 # real seconds between frames
print("SETTINGS: [INFO] 1 timelapse second is {} real seconds".format(RSPF*FPTS))