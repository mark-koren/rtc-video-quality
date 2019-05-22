#!/usr/bin/env python3
import argparse
import subprocess
import os
import pdb
import skvideo.io
from video_presets import *

#Define presets here

parser = argparse.ArgumentParser()

parser.add_argument('-p', '--preset', type=str, default=None)
parser.add_argument('-v', '--videos', nargs='*', default = [])
parser.add_argument('-a', '--attempts', type=int, default=3)
parser.add_argument('-c', '--convert', nargs='*', default = [])
# parser.add_argument('-c', '--clean', nargs='*', default = [])
clean_arg = parser.add_mutually_exclusive_group(required=False)
clean_arg.add_argument('--clean', dest='clean', action='store_true')
clean_arg.add_argument('--no-clean', dest='clean', action='store_false')
parser.set_defaults(clean=False)

clean_arg = parser.add_mutually_exclusive_group(required=False)
clean_arg.add_argument('--force', dest='force', action='store_true')
clean_arg.add_argument('--no-force', dest='force', action='store_false')
parser.set_defaults(force=False)

args = parser.parse_args()

# if len(args.clean) > 0:
# 	for extension in args.clean:
# 		subprocess.call(['rm', '*.' + extension])

if args.clean:
	subprocess.call('rm *.y4m*', shell=True)

video_list = []
# print(args.preset)
if args.preset is not None:
	video_list = globals()[args.preset.upper()]

for vid in args.videos:
	video_list.append(vid)

fail_list = []
for vid in video_list:
	vid_name = vid.split("/")[-1]
	if not args.force and os.path.isfile('./' + vid_name):
		print("File exists: ", vid_name, " -- skipping (use --force to force download)")
		wget_succesful = True
	else:
		attempt = 0
		wget_succesful = False
		while attempt < args.attempts and not wget_succesful:
			attempt += 1
			wget_succesful = (subprocess.call(['wget', vid]) == 0)

	if not wget_succesful:
		fail_list.append(vid)
		print("error code", wget_succesful)
	else:
		for vid_format in args.convert:
			metadata = skvideo.io.ffprobe(skvideo.io.FFmpegReader(vid_name, {}, {}))
			pdb.set_trace()
			convert_succesful = (subprocess.call(['ffmpeg', '-i', vid_name, vid_name.split('.')[0] + '.' + vid_format]) == 0)
			if not convert_succesful:
				print("Failed to convert file: ", vid_name, " -- target: ", vid_name.split('.')[0] + '.' + vid_format)

for vid in fail_list:
	print("Failed to get: ", vid)



	