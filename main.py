from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageGrab
from settings import *
import time
import math
from threading import Thread
import cv2, numpy

class Timelapse:
    def __init__(self):
        self.temp:Image = None
        self.tray = None

        self.thread = None
        self.running = False

        self.dir = None
        self.time = None
        self.frames = 0

    def start(self):
        if self.running: return
        self.time = str(math.floor(time.time()))
        self.dir = lambda x: TEMP_SAVE_DIR(self.time, x)
        os.makedirs(self.dir(None), exist_ok=True)

        self.thread:Thread = Thread(target=self.snap, daemon=True)
        self.running = True
        self.thread.start()

        self.tray.title = "live!"

    def snap(self):
        start = time.time()
        while self.running:
            temp = ImageGrab.grab()
            temp.save(self.dir(TEMP_IMAGE_STYLE(self.frames) + ".png"))
            self.temp = temp
            self.frames += 1
            self.tray.title = "{} frames, {}s".format(self.frames-1, math.floor(time.time()-start))
            time.sleep(RSPF)

    def stopReset(self):
        if not(self.running): return
        self.running = False

        if self.frames > 0:
            os.makedirs(OUT_SAVE_DIR(None), exist_ok=True)
            width, height = self.temp.size
            video = cv2.VideoWriter(OUT_SAVE_DIR(self.time+".mp4"), cv2.VideoWriter_fourcc(*'mp4v'), FPTS, (width, height))
            for i in range(self.frames-1):
                frame = cv2.imread(self.dir(TEMP_IMAGE_STYLE(i) + ".png"))
                if frame is None:
                    print("missing frame {}!".format(i))
                    continue
                video.write(frame)
                self.tray.title = "video {}/{} frames".format(i, self.frames-1)
            video.release()
            try: cv2.destroyAllWindows()
            except: pass

        self.dir = None
        self.frames = 0


timelapse = Timelapse()

tray = Icon("Timelapse", TRAY_IMAGE)

menu = Menu(
    MenuItem("Start", timelapse.start),
    MenuItem("Stop", timelapse.stopReset),
    MenuItem("Quit", tray.stop), 
)
tray.menu=menu

tray.title = "ready {}RSPF @{}FPTS".format(RSPF, FPTS)
timelapse.tray = tray

tray.run()