from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageGrab
from settings import *
import time
import math
from threading import Thread
import cv2, numpy

class Timelapse:
    def __init__(self):
        self.tray = None

        self.thread = None
        self.running = False

        self.timeStr = None
        self.time = None
        self.frames = 0
        
        self.videoDir = None
        self.video:cv2.VideoWriter = None

    def start(self):
        if self.running: return
        self.time = time.time()
        self.timeStr = str(math.floor(self.time))
        self.videoDir = OUT_SAVE_DIR("{}.mp4".format(self.timeStr))
        
        os.makedirs(OUT_SAVE_DIR(None), exist_ok=True)

        temp = ImageGrab.grab()
        width, height = temp.size
        self.video = cv2.VideoWriter(self.videoDir, cv2.VideoWriter_fourcc(*'mp4v'), FPTS, (width, height))

        self.thread:Thread = Thread(target=self.snap, daemon=True)
        self.running = True
        self.thread.start()

        self.tray.icon = TRAY_ACTIVE_IMAGE_1
        self.tray.title = "live!"

    def snap(self):
        start = time.time()
        while self.running:
            if (self.time + RSPF < time.time()):
                self.time += RSPF
                temp = ImageGrab.grab()
                temp = cv2.cvtColor(numpy.array(temp), cv2.COLOR_RGB2BGR)
                self.video.write(temp)

                self.frames += 1
                self.tray.title = "{} frames, {}s".format(self.frames-1, math.floor(time.time()-start))

                self.tray.icon = TRAY_ACTIVE_IMAGE_1 if self.frames%2==0 else TRAY_ACTIVE_IMAGE_2
            time.sleep(0.01)

    def stopReset(self):
        if not(self.running): return
        self.running = False

        if self.thread:
            self.thread.join()

        if self.video:
            self.video.release()

        try: cv2.destroyAllWindows()
        except: pass

        self.tray.icon = TRAY_IDLE_IMAGE
        self.tray.title = "ready"

        self.videoDir = None
        self.frames = 0
    
    def quit(self):
        self.stopReset()
        tray.stop()


timelapse = Timelapse()

tray = Icon("Timelapse", TRAY_IDLE_IMAGE)

menu = Menu(
    MenuItem("Start", timelapse.start),
    MenuItem("Stop", timelapse.stopReset),
    MenuItem("Save and Quit", timelapse.quit)
)
tray.menu=menu

tray.title = "ready {}RSPF @{}FPTS".format(round(RSPF*100)/100, FPTS)
timelapse.tray = tray

tray.run()