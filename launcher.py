#!/usr/bin/python
import subprocess, os, time, traceback


print "Starting Display"
os.chdir("/home/pi/matrix/rpi-rgb-led-matrix/python/samples")

while True:
    try:
        command = ["sudo", "python", "sbff_launch_test.py"]
        subprocess.call(command)
    except Exception, e:
        traceback.print_exc()
    	time.sleep(0.1)
