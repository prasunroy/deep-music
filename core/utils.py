# -*- coding: utf-8 -*-
"""
Utility functions.
Created on Tue Feb 12 22:00:00 2019
Author: Prasun Roy | CVPRU-ISICAL (http://www.isical.ac.in/~cvpr)
GitHub: https://github.com/prasunroy/deep-music

"""

# imports
import subprocess

# download a video from YouTube
def download_video(ytid, out_dir='.', verbose=False):
    """Downloads a video from YouTube.
    
    Args:
        ytid   : YouTube video identifier.
        out_dir: Download directory. Defaults to current working directory.
        verbose: Execute in verbose mode. Defaults to False.
    
    """
    options = ['youtube-dl']
    options.append('-o "{}/%(id)s.%(ext)s"'.format(out_dir))
    if not verbose:
        options.append('--quiet --no-warnings')
    options.append('https://www.youtube.com/watch?v={}'.format(ytid))
    command = ' '.join(options)
    subprocess.call(command, shell=True)
    return

# recode media
def recode_media(src, dst, start=0, length=0, width=0, height=0, fps=0,
                 bitrate_v=0, bitrate_a=0, no_video=False, no_audio=False,
                 copy_v=False, copy_a=False, overwrite=False, verbose=False):
    """Recodes media.
    
    Args:
        src      : Path to source media file.
        dst      : Path to target media file.
        start    : Start position in seconds. Ignored if <= 0
        length   : Length of recoded media in seconds. Ignored if <= 0.
        width    : Frame width of recoded video. Ignored if <= 0.
        height   : Frame height of recoded video. Ignored if <= 0.
        fps      : Frame rate of recoded video. Ignored if <= 0.
        bitrate_v: Bit rate of recoded video stream in KHz. Ignored if <= 0.
        bitrate_a: Bit rate of recoded audio stream in KHz. Ignored if <= 0.
        no_video : Drop video stream. Defaults to False.
        no_audio : Drop audio stream. Defaults to False.
        copy_v   : Copy video stream directly from source. Defaults to False.
        copy_a   : Copy audio stream directly from source. Defaults to False.
        overwrite: Overwrite target media file. Defaults to False.
        verbose  : Execute in verbose mode. Defaults to False.
    
    """
    options = ['ffmpeg']
    options.append('-i {}'.format(src))
    if start >= 0:
        options.append('-ss {}'.format(start))
    if length > 0:
        options.append('-t {}'.format(length))
    if width > 0 and height > 0:
        options.append('-s {}x{}'.format(width, height))
    if fps > 0:
        options.append('-r {}'.format(fps))
    if bitrate_v > 0:
        options.append('-b:v {}k'.format(bitrate_v))
    if bitrate_a > 0:
        options.append('-b:a {}k'.format(bitrate_a))
    if copy_v:
        options.append('-c:v copy')
    if copy_a:
        options.append('-c:a copy')
    if no_video:
        options.append('-vn')
    if no_audio:
        options.append('-an')
    if overwrite:
        options.append('-y')
    else:
        options.append('-n')
    if verbose:
        options.append('-v info')
    else:
        options.append('-v quiet')
    options.append(dst)
    command = ' '.join(options)
    subprocess.call(command, shell=True)
    return
