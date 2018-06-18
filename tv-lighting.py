import colorsys
import subprocess
import sys
import time

print ('Starting TV Lighting')

while True:
	# Get screenshot
	subprocess.call(["lib/raspi2png/raspi2png", "--compression", "0", "--height", "300"])
	
	# Analyse for RGB
	command = "convert /home/pi/Desktop/tv-lighting/snapshot.png -scale 1x1\! -format '%[pixel:u]' info:-"
	process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
	output = process.communicate()
	
	#print ('RGB values are:')
	analysis = output[0]
	#print analysis
	
	# Convert to HSL
	split_str = analysis.split("(") # ['srgb', '102,102,105)']
	split_str = split_str[1].split(")") # ['102,102,105', '']
	split_str = split_str[0].split(",")  #['102,102,105']
	
	r = int(split_str[0])
	g = int(split_str[1])
	b = int(split_str[2])
	
	#print ("RGB is:")
	print r, g, b
	
	# Convert RGB into colorspace
	r, g, b = [x/255.0 for x in r, g, b]
	
	hls = colorsys.rgb_to_hls(r, g, b)
	hue = float(hls[0])*360
	light = float(hls[1])*100
	saturation = float(hls[2])*100
	
	#print ("Hue (360), Saturation (%), Light (%) are:")
	#print str(hue), str(saturation), str(light)
	
	# Send command to light
	cmd = """curl -X PUT --header "Content-Type:Application/json" --header "authorization: 092-94-999" http://192.168.31.95:51826/characteristics --data '{"characteristics":[{"aid":41,"iid":12,"value":""" + str(hue) + """},{"aid":41,"iid":13,"value":""" + str(saturation) + """ }]}'
	"""
	cmd_dining_table = """curl -X PUT --header "Content-Type:Application/json" --header "authorization: 092-94-999" http://192.168.31.95:51826/characteristics --data '
{"characteristics":[{"aid":38,"iid":12,"value":""" + str(hue) + """},{"aid":38,"iid":13,"value":""" + str(saturation) + """ }]}'
        """
	process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	#process = subprocess.Popen(cmd_dining_table, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	
	time.sleep(1)
