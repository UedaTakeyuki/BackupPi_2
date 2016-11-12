# coding:utf-8
# Copy Right Atelier Grenouille  © 2015 -
#

import sys 
import subprocess
import time
import traceback
import json

sh_df="df"
sh_clean=""
def df():
	p = subprocess.Popen(sh_df, stdout=subprocess.PIPE, shell=True)
	results = p.stdout.readlines()
	cols={}
	for line in results:
		columns = line.split()
		if columns[0] != "tmpfs" and columns[0] != "Filesystem" and "/dev/sda" in columns[0]:
			cols[columns[0]] = {'Filesystem':columns[0],
													'1K-blocks':columns[1], 
													'Used':columns[2],
													'Available':columns[3],
													'Use%':columns[4],
													'Mounted_on':columns[5]
													}
		#print columns
	return cols

def start_clean(sda):
	try:
		p = subprocess.Popen('sudo sh -c "cat /dev/zero > '+sda["Mounted_on"]+'/boo"', stdout=subprocess.PIPE, shell=True)
	except:
		info=sys.exc_info()
		print "Unexpected error:"+ traceback.format_exc(info[0])
		print traceback.format_exc(info[1])
		print traceback.format_exc(info[2])
	while True:
		sda_now = df()[sda["Filesystem"]]
		print sda_now
		if sda_now['Available'] == "0":
			#time.sleep(1)
#			break_clean(sda_now)
			break
		time.sleep(5)

def break_clean(sda):
	try:
		p = subprocess.check_call('sudo pkill -9 -f "/dev/zero"',shell=True)
	except:
		info=sys.exc_info()
		print "Unexpected error:"+ traceback.format_exc(info[0])
#		print traceback.format_exc(info[1])
#		print traceback.format_exc(info[2])
	finish_clean(sda)

def finish_clean(sda):
	try:
		p = subprocess.check_call('sudo rm '+sda["Mounted_on"]+'/boo', stdout=subprocess.PIPE, shell=True)
	except:
		info=sys.exc_info()
		print "Unexpected error:"+ traceback.format_exc(info[0])
#		print traceback.format_exc(info[1])
#		print traceback.format_exc(info[2])
	print "clean " + sda["Mounted_on"] + "is finished!"

def json_dump(arr1):
	return json.dumps(arr1,sort_keys=True)

if __name__ == '__main__':
	sdas=df()
	start_clean(sdas["/dev/sda1"])
	start_clean(sdas["/dev/sda2"])
	print json_dump(sdas)

#	while True:
#		sda2 = df()["/dev/sda2"]
#		print sda2
#		if sda2['Available'] == "0":
#			#time.sleep(1)
#			break_clean(sda2)
#			break
#		time.sleep(5)
