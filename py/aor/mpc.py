from subprocess import *

def cmd(cmd):
	p = Popen('mpc ' +, shell=True, stdout=PIPE)
	output = p.communicate()[0]
	return output

def stats():
	s =  cmd('stats')
	l = s.split('\n')
	return {"artists": int(l[0][8:]),
			"albums": int(l[1][7:]),
			"songs": int(l[2][6:]),
			"play_time": l[4][10:],
			"uptime": l[5][7:],
			"db_updated": l[6][11:],
			"db_play_time": l[7][13:]
		}

def song():
	return cmd('mpc current')

def title_status():
	s =  cmd('')
	if(s[0:6] != "volume"):
		a = s.split('\n')
		d = a[1]
	else:
		d = ""
	status = {}
	if(d!=""):
		status["position"] = d[11:16] 
		status["time"] = d[19:28]
		if(d[:9] == "[paused]"):
			status["title"] = d[10:]
		elif(d[:9] == "[playing]"):
			status["title"] = d[11:]
		else:
			status["title"] = " "
	else:
		status["title"] = " "
		status["position"] = "asd" 
		status["time"] = "00:00:00"
	#print status["title"]
	return status

def mpd_status():
	s =  cmd('')
	if(s[0:6] != "volume"):
		a = s.split('\n')
		l = a[2]
	else:
		l = s
	status = {"volume": l[7:10],"repeat": l[22:25],"random": l[36:39],"single": l[50:53],"consume": l[65:68],"position": "xx/xx","title": ""}
 	return status

def playlist(inc,length = 4):
	p =  mpc_cmd('playlist')
	playlist = p.split('\n')
	partlist = []
	if(inc>=len(playlist)):
		inc = 0
	if(len(playlist)> inc+length):
		for i in range(inc,inc+length):
			partlist.append(playlist[i])
	else:
		for i in range(inc,len(playlist)):
			partlist.append(playlist[i])
		#print inc+length-len(playlist)
		for i in range(inc+length-len(playlist)+1):
			partlist.append(playlist[i])
	return partlist