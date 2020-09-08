import subprocess
import time
import os


VIDEO_DIR = "./video"
VLC_CMD_BASE = [
    "vlc",
    "--no-audio",
    "--fullscreen",
    "--no-video-title-show",
    "--play-and-exit"
]
(_, _, filenames) = next(os.walk(VIDEO_DIR))

for f in filenames:
    video = os.path.join(VIDEO_DIR, f)
    cmd = VLC_CMD_BASE + [video]
    resp = subprocess.check_call(cmd)
    print('video done! waiting for 10 seconds before the next...')
    time.sleep(10)
