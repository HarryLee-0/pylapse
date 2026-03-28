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
        self.tray = tray

        self.thread = None
        self.running = False

        self.dir = None
        self.time = None
        self.frames = 0

        self.tray.title = "ready {}RSPF @{}FPTS".format(RSPF, FPTS)

    def start(self):
        if self.running: return
        self.time = str(math.floor(time.time()))
        self.dir = TEMP_SAVE_DIR.join(self.time)
        os.mkdir(self.dir)

        self.thread:Thread = Thread(target=self.snap, daemon=True)
        self.thread.start()
        self.running = True

        self.tray.title = "live!"

    def snap(self):
        start = time.time()
        while self.running:
            temp = ImageGrab.grab()
            temp = cv2.cvtColor(numpy.array(temp), cv2.COLOR_RGB2BGR)
            temp.save(Image.fromarray(self.dir.join(TEMP_IMAGE_STYLE(self.frames))))
            self.temp = temp
            self.frames += 1
            self.tray.title = "{} frames, {}s".format(self.frames, math.floor(time.time()-start))
            time.sleep(RSPF)

    def stopReset(self):
        if not(self.running): return
        self.running = False

        if self.frames > 0:
            height, width, layers = self.temp.shape
            video = cv2.VideoWriter(self.time, cv2.VideoWriter_fourcc(*'mp4v'), FPTS, (width, height))
            for i in range(self.frames):
                video.write(cv2.imread(TEMP_IMAGE_STYLE(i)))
                self.tray.title = "video {}/{} frames".format(i, self.frames)
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
timelapse.tray = tray
tray.run()