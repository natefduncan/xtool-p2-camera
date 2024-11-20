import os
from dotenv import load_dotenv
import requests as r
from multiprocessing import Process
import time
from ffmpeg import FFmpeg

load_dotenv()

XTOOL_HOST=os.getenv("XTOOL_HOST")
XTOOL_IMAGE_URL=f"http://{XTOOL_HOST}:8329/camera/snap"
VIDEO_DEVICE=os.getenv("VIDEO_DEVICE")
IMAGE_PATH="/tmp/xtool_snap.jpg"

def start_image_capture(url, image_path, loop=1):
    while True:
        image_data = r.get(url).content
        with open(image_path, "wb") as f:
            f.write(image_data)
        time.sleep(loop)

def start_ffmpeg(input_path, output_device):
    ffmpeg = (
        FFmpeg()
        .option("re").option("loop", 1)
        # "ffmpeg -loop 1 -re -i /tmp/xtool_snap.jpg -f v4l2 -vcodec rawvideo -pix_fmt yuv420p /dev/video2"
        .input(input_path)
        .output(output_device, {"f": "v4l2", "vcodec": "rawvideo", "pix_fmt": "yuv420p"})
    )
    ffmpeg.execute()


if __name__ == "__main__":
    p1 = Process(target=start_image_capture, args=(XTOOL_IMAGE_URL, IMAGE_PATH,))
    p1.start()
    p2 = Process(target=start_ffmpeg, args=(IMAGE_PATH, VIDEO_DEVICE))
    p2.start()
