# -*- coding: utf-8 -*-
"""
Download data from AudioSet (https://research.google.com/audioset).
Created on Sun Feb 24 11:00:00 2019
Author: Prasun Roy | CVPRU-ISICAL (http://www.isical.ac.in/~cvpr)
GitHub: https://github.com/prasunroy/deep-music

"""


# imports
import glob
import os
import pandas
import re
from core.utils import download_video
from core.utils import recode_media


# AudioSet api endpoint url
API_URL = 'http://storage.googleapis.com/us_audioset/youtube_corpus/v1/csv/'


# find labels
def find_labels(keywords):
    results = {'labels': [], 'dnames': []}
    pattern = '|'.join(['\\b' + keyword + '\\b' for keyword in keywords])
    df = pandas.read_csv(API_URL + 'class_labels_indices.csv')
    for label, dname in zip(df['mid'].values, df['display_name'].values):
        if len(re.findall(pattern, dname, re.IGNORECASE)) > 0:
            results['labels'].append(label)
            results['dnames'].append(dname)
    return results


# find videos
def find_videos(labels):
    results = []
    pattern = '|'.join(labels)
    df_1 = pandas.read_csv(API_URL + 'eval_segments.csv',
                           sep=', ', header=2, engine='python')
    df_2 = pandas.read_csv(API_URL + 'balanced_train_segments.csv',
                           sep=', ', header=2, engine='python')
    df_3 = pandas.read_csv(API_URL + 'unbalanced_train_segments.csv',
                           sep=', ', header=2, engine='python')
    df = pandas.concat([df_1, df_2, df_3])
    for ytid, start, end, labels in df.values:
        if len(re.findall(pattern, labels, re.IGNORECASE)) > 0:
            results.append((ytid, start, end - start))
    return results


# download AudioSet
def download_audioset():
    keywords = input('[INPUT] Enter keywords (comma separated): ')
    if keywords == '':
        print('[ERROR] No keywords provided')
        return
    keywords = [keyword.strip() for keyword in keywords.split(',')]
    print('[DEBUG] Searching keywords...')
    result = find_labels(keywords)
    labels = result['labels']
    dnames = result['dnames']
    if len(labels) == 0 and len(dnames) == 0:
        print('[ERROR] No videos found with specified keywords')
        return
    dnames = '\n\t+ '.join([''] + dnames)
    print('[DEBUG] Including videos with following tags: {}'.format(dnames))
    print('[DEBUG] Searching videos... ', end='')
    videos = find_videos(labels)
    print('{} found'.format(len(videos)), end='')
    n_vids = input('[INPUT] Maximum number of videos to download: ')
    if not n_vids.isdigit():
        print('[ERROR] Expected a positive integer')
        return
    n_vids = min(int(n_vids), len(videos))
    print('[DEBUG] Selected {} videos'.format(n_vids), end='')
    outdir = input('[INPUT] Output directory: ')
    if outdir == '':
        outdir = './audioset'
    path_r = os.path.join(outdir, 'audioset')
    path_v = os.path.join(outdir, 'audioset/video')
    path_a = os.path.join(outdir, 'audioset/audio')
    for directory in [path_r, path_v, path_a]:
        if not os.path.isdir(directory):
            os.makedirs(directory)
    n_done = 0
    for ytid, start, length in videos:
        print('\r[DEBUG] Downloading and converting videos... {} of {} '\
              .format(n_done + 1, n_vids), end='')
        try:
            download_video(ytid, path_r)
            src_v = glob.glob(path_r + '/{}.*'.format(ytid))[0]
            dst_v = path_v + '/{}.mp4'.format(ytid)
            dst_a = path_a + '/{}.aac'.format(ytid)
            recode_media(src_v, dst_v, start, length, overwrite=True)
            recode_media(src_v, dst_a, start, length, overwrite=True)
            os.remove(src_v)
            n_done += 1
        except:
            pass
        if n_done >= n_vids:
            print('\n[DEBUG] Finished')
            break
    return


if __name__ == '__main__':
    download_audioset()
