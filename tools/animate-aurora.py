#!/usr/bin/env python3
"""Render a quiet, seamless aurora loop from Vincent Guth's credited photo.

Requires Python 3, numpy, opencv-python-headless and ffmpeg with libx264.
Run from any directory; output goes into the theme's backgrounds directory.
"""

from pathlib import Path
import subprocess

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
WIDTH, HEIGHT = 1920, 1282
FPS, SECONDS = 24, 40


def prepare():
    photo = cv2.imread(str(ROOT / "backgrounds/1-aurora.jpg"))
    if photo is None:
        raise FileNotFoundError("backgrounds/1-aurora.jpg")
    photo = cv2.resize(photo, (WIDTH, HEIGHT), interpolation=cv2.INTER_AREA)
    base = photo.astype(np.float32)
    # Separate the broad curtains from fine detail. Adding only the change in
    # this blurred layer back to the photo leaves the original stars in place.
    curtains = cv2.GaussianBlur(base, (0, 0), 9)
    y, x = np.mgrid[:HEIGHT, :WIDTH].astype(np.float32)
    # Protect the forest, including the fine branches and a margin around them.
    dark = (np.max(base, axis=2) < 65) & (y > HEIGHT * 0.58)
    forest = cv2.dilate(dark.astype(np.float32), np.ones((17, 17), np.uint8))
    forest = cv2.GaussianBlur(forest, (0, 0), 8)
    # Fade movement into the violet upper sky and out near the foreground.
    sky = np.clip((y / HEIGHT - 0.12) / 0.25, 0, 1)
    sky *= np.clip((0.91 - y / HEIGHT) / 0.18, 0, 1)
    mask = (sky * (1 - forest))[..., None]
    return base, curtains, x, y, mask


def frame(phase, layers):
    base, curtains, x, y, mask = layers
    # Integer harmonics close the loop exactly at 40 seconds. Max sway is
    # about 20 pixels: visible over several seconds, with no camera movement.
    dx = 15 * np.sin(phase + y / HEIGHT * 5 + x / WIDTH * 2)
    dx += 5 * np.sin(2 * phase - y / HEIGHT * 4 + x / WIDTH * 5)
    dy = 5 * np.sin(phase + x / WIDTH * 6)
    moving = cv2.remap(curtains, x + dx, y + dy, cv2.INTER_LINEAR,
                       borderMode=cv2.BORDER_REFLECT_101)
    return np.clip(base + (moving - curtains) * mask, 0, 255).astype(np.uint8)


def main():
    output = ROOT / "backgrounds/2-aurora-animated.mp4"
    layers = prepare()
    command = [
        "ffmpeg", "-hide_banner", "-loglevel", "warning", "-y",
        "-f", "rawvideo", "-pixel_format", "bgr24",
        "-video_size", f"{WIDTH}x{HEIGHT}", "-framerate", str(FPS),
        "-i", "pipe:0", "-an", "-c:v", "libx264", "-preset", "slow",
        "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        str(output),
    ]
    encoder = subprocess.Popen(command, stdin=subprocess.PIPE)
    try:
        for index in range(FPS * SECONDS):
            encoder.stdin.write(frame(2 * np.pi * index / (FPS * SECONDS), layers).tobytes())
            if index % (FPS * 5) == 0:
                print(f"Rendered {index // FPS}/{SECONDS} seconds", flush=True)
        encoder.stdin.close()
        if encoder.wait():
            raise RuntimeError("ffmpeg failed")
    finally:
        if encoder.poll() is None:
            encoder.kill()
            encoder.wait()
    print(output)


if __name__ == "__main__":
    main()
