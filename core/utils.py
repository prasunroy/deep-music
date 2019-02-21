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
def extract_audio(src, dst, start=0, duration=-1, bitrate=192, overwrite=False,
                  verbose=False):
    """Extracts audio from a video.
    
    Args:
        src      : Path to source video file.
        dst      : Path to target audio file.
        start    : Start position in seconds. Defaults to 0.
        duration : Duration of the extracted audio clip. For values <= 0 full
                   audio clip is extracted. Defaults to -1.
        bitrate  : Bit rate of target audio in KHz. Possible values are 8, 16,
                   24, 32, 40, 48, 64, 80, 96, 112, 128, 160, 192, 224, 256,
                   or 320. Defaults to 192.
        overwrite: Flag for overwriting target audio file. Defaults to False.
        verbose  : Flag for verbose mode. Defaults to False.
    
    """
    options = ['ffmpeg']
    if start >= 0 and duration >= 1:
        options.append('-ss {} -i {} -t {}'.format(start, src, duration))
    else:
        options.append('-i {}'.format(src))
    options.append('-b:a {}k'.format(bitrate))
    options.append('-vn')
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


# remove audio from a video
def extract_video(src, dst, start=0, duration=-1, overwrite=False,
                  verbose=False):
    """Removes audio from a video.
    
    Args:
        src      : Path to source video file.
        dst      : Path to target video file.
        start    : Start position in seconds. Defaults to 0.
        duration : Duration of the extracted video clip. For values <= 0 full
                   video clip is extracted. Defaults to -1.
        overwrite: Flag for overwriting target video file. Defaults to False.
        verbose  : Flag for verbose mode. Defaults to False.
    
    """
    options = ['ffmpeg']
    if start >= 0 and duration >= 1:
        options.append('-ss {} -i {} -t {}'.format(start, src, duration))
    else:
        options.append('-i {}'.format(src))
    options.append('-c copy')
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


# download video from YouTube
def download_video(ytid, out_dir=None, out_fmt=None, verbose=False):
    """Downloads video from YouTube.
    
    Args:
        ytid    : YouTube video identifier.
        out_dir : Download directory. Uses current working directory if not
                  specified. Defaults to None.
        out_fmt : Target video format. Uses FFMPEG to convert downloaded video
                  into specified format. Skips conversion if not specified.
                  Defaults to None.
        verbose : Flag for verbose mode. Defaults to False.
    
    """
    options = ['youtube-dl']
    if not out_dir is None:
        options.append('-o "{}/%(id)s.%(ext)s"'.format(out_dir))
    else:
        options.append('-o "%(id)s.%(ext)s"')
    if not out_fmt is None:
        options.append('--recode-video {}'.format(out_fmt))
    if not verbose:
        options.append('--quiet --no-warnings')
    options.append('https://www.youtube.com/watch?v={}'.format(ytid))
    
    command = ' '.join(options)
    subprocess.call(command, shell=True)
    return
