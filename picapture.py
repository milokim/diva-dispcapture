import os 
import sys

def clean_files():
	os.system("rm demo.h264 demo.mp4")

def hdmi_capture(time):
	cmd = "raspivid -o demo.h264 -t " + str(time) + " -md 1 -awb off -ex off -awbg 1.0,1.0"
	os.system(cmd)

def convert_to_mp4():
	cmd = "MP4Box -fps 30 -add demo.h264 demo.mp4"
	os.system(cmd)

if __name__ == '__main__':
	clean_files()
	options = sys.argv

	# Default recording time is 10 sec
	recording_ms = 10000
	if '-t' in options:
		index = options.index('-t') + 1
		recording_ms = int(options[index])

	hdmi_capture(recording_ms)
	convert_to_mp4()
