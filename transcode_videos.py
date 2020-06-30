#! /usr/bin/env python3

import subprocess
import math
import os
import errno
import re
import threading
import time
from multiprocessing import Process, Queue

"""
run follow while using ubuntu once:
sudo mv /bin/sh /bin/sh.orig
sudo ln -s /bin/bash /bin/sh
"""

FFMPEG = '/root/bin/ffmpeg'
FFPROBE = '/root/bin/ffprobe'
THREADS = 4

def get_video_length(video_file):
    cmd = [FFPROBE,
           '-i', video_file,
           '-show_entries', 'format=duration',
           '-loglevel', 'quiet',
           '-print_format', 'csv="p=0"']
    result = subprocess.check_output(' '.join(cmd), shell=True)
    video_length = float(result[:-1])
    return video_length

get_split_duration = lambda video_length, split_nums: math.ceil(float(video_length) / float(split_nums)  )

def split_video(video_file, split_duration, output_dir, split_video_name, extension='.mp4'):
    """
    before spliting, create output_dir if not exist,
    raise error if video_file is not exist
    """
    if os.path.isfile(video_file) is False:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), video_file)
        return

    if os.path.exists(output_dir) is False:
        os.mkdir(output_dir)
    elif os.path.isfile(output_dir) is True:
        raise NotADirectoryError(errno.ENOTDIR, os.strerror(errno.ENOTDIR), output_dir)
        return

    """
    split video by duration
    """
    
    cmd = [FFMPEG, 
           '-loglevel', 'quiet',
           '-i', video_file,
           '-c', 'copy',
           '-f', 'segment', '-segment_time', str(split_duration),
           '-reset_timestamps', '1',
           '-y', os.path.join(output_dir, split_video_name+'_%03d'+extension)]
    
    """
    remove file if name is split_video_name_%03d+extension
    """
    filelist = os.listdir(output_dir)
    pattern = '\d{3}'
    target_match_length = 3
    for filename in filelist:
        if filename.startswith(split_video_name+'_') \
            and filename.endswith(extension):
            rest = filename.replace(split_video_name+'_','')
            rest = rest.replace(extension, '')
            if len(rest) == target_match_length:
                if re.match(pattern, rest):
                    os.remove(os.path.join(output_dir, filename)) 
    
    subprocess.run(cmd)
    """
    return the list of split video(s)
    """
    result_files = list()
    filelist = os.listdir(output_dir)
    for filename in filelist:
        if filename.startswith(split_video_name+'_') \
            and filename.endswith(extension):
            rest = filename.replace(split_video_name+'_','')
            rest = rest.replace(extension, '')
            if len(rest) == target_match_length:
                if re.match(pattern, rest):
                    result_files.append(filename)
    return result_files

def transcode_with_ffmpeg(input_video, output_video, input_param=None, transcode_param=None):
    """
    transcode one
    """
    cmd = [FFMPEG, '-loglevel', 'quiet']
    if input_param is not None:
        cmd += input_param.split(' ')
    cmd += ['-i', input_video]
    if transcode_param is not None:
        cmd += transcode_param.split(' ')
    cmd += ['-y', output_video]
    subprocess.run(cmd)
    return

def transcode_videos(input_videos, output_videos, input_param=None, transcode_param=None):
    if len(input_videos) != len(output_videos):
        return None
    process_num = len(input_videos)
    process_list = list()
    for i in range(process_num):
        input_video = input_videos.pop()
        output_video = output_videos.pop()
        proc = Process(target=transcode_with_ffmpeg, 
                       args=(input_video, output_video, input_param, transcode_param, ))
        process_list.append(proc)
        proc.start()
    for proc in process_list:
        proc.join()
    return output_videos

def merge_video(input_videos, output_video):
    video_list_file = 'merge.txt'
    with open(video_list_file, mode='w') as f:
        for input_video in input_videos:
            f.writelines('file '+input_video+'\n')
    cmd = [FFMPEG, 
          '-loglevel', 'quiet',
          '-f', 'concat',
          '-safe', '0',
          '-i', video_list_file,
          '-c', 'copy',
          '-fflags', '+genpts',
          '-y', output_video]
    subprocess.run(cmd)
    return

if __name__ == '__main__':
    video_file = 'game.flv'
    video_length = get_video_length(video_file)
    print( video_length )
    duration = get_split_duration(video_length, 4)
    print(duration)
    result_files = split_video(video_file, duration, './', 'split_test')
    #result_files = ['split_test_000.mp4', 'split_test_001.mp4', 'split_test_002.mp4', 'split_test_003.mp4']
    print(result_files)
    output_videos = ['merge_test1.mp4','merge_test2.mp4','merge_test3.mp4','merge_test4.mp4']
    #transcode_videos(result_files, output_videos, transcode_param='-c:v libd264') 
    
    merge_video(output_videos, 'test4m.mp4')
