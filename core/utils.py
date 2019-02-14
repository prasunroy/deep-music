# -*- coding: utf-8 -*-
"""
Utility functions.
Created on Tue Feb 12 22:00:00 2019
Author: Prasun Roy | CVPRU-ISICAL (http://www.isical.ac.in/~cvpr)
GitHub: https://github.com/prasunroy/deep-music

"""


# imports
import subprocess


# extract audio from a video
def extract_audio(src, dst, bitrate=192, overwrite=False, verbose=False):
    """Extracts audio from a video.
    
    Args:
        src      : Path to source video file.
        dst      : Path to target audio file.
        bitrate  : Bit rate of target audio in KHz. Possible values are 8, 16,
                   24, 32, 40, 48, 64, 80, 96, 112, 128, 160, 192, 224, 256,
                   or 320. Defaults to 192.
        overwrite: Flag for overwriting target audio file. Defaults to False.
        verbose  : Flag for verbose mode. Defaults to False.
    
    """
    command = 'ffmpeg -i {} -b:a {}k -vn {} -v {} {}'.format(src, bitrate, '-y' if overwrite else '-n', 'info' if verbose else 'quiet', dst)
    subprocess.call(command)
    return


# remove audio from a video
def extract_video(src, dst, overwrite=False, verbose=False):
    """Removes audio from a video.
    
    Args:
        src      : Path to source video file.
        dst      : Path to target video file.
        overwrite: Flag for overwriting target video file. Defaults to False.
        verbose  : Flag for verbose mode. Defaults to False.
    
    """
    command = 'ffmpeg -i {} -c copy -an {} -v {} {}'.format(src, '-y' if overwrite else '-n', 'info' if verbose else 'quiet', dst)
    subprocess.call(command)
    return
