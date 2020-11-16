import time
import threading
import os
from lib.client import Client
import _thread
import threading
from multiprocessing import Queue
from hoster import Battle #ability to open battles
from lib.quirks.autohost_factory import AutohostFactory #ability to change credential to host battles
from termcolor import colored

password = b'password'
map_file = 'comet_catcher_redux.sd7'
mod_file = '0465683c70018f80a17b92ed78174d19.sdz'
engineName = 'Spring'
engineVersion = '104.0.1-1435-g79d77ca maintenance'
mapName = 'Comet Catcher Redux'
roomName = 'Test Room'
gameName = 'Zero-K v1.8.3.5'
q = Queue()
battlePort = 2000
startDir = os.getcwd()




if __name__ == "__main__":

	print(colored('[INFO]', 'green'), colored('Main: Initing.', 'white'))
	client = Client(battlePort,startDir)
	autohost=AutohostFactory()
	
	client.login('Autohost_CTL',password)
	print(colored('[INFO]', 'green'), colored('Autohost_CTL: Logging in', 'white'))
	client.clearBuffer('Autohost_CTL')
	
	client.joinChat('bus')
	print(colored('[INFO]', 'green'), colored('Autohost_CTL: Joining Battle Chat.', 'white'))
	client.clearBuffer('Autohost_CTL')
	
	_thread.start_new_thread( client.keepalive,('Autohost_CTL',))
	client.clearBuffer('Autohost_CTL')
	
	gameParas = {'dataType': 'gem', 'action': 'default', 'title':'default'}

# ,'gemType': 'default', 'isPasswded': False, 'passwd':"", 'mapFile': 'comet_catcher_redux.sd7', 'modFile': '0465683c70018f80a17b92ed78174d19.sdz', 'engineName': 'Spring', 'engineVersion': '104.0.1-1435-g79d77ca maintenance', 'mapName': 'Comet Catcher Redux', 'roomName': 'Test Room', 'gameName': 'Zero-K v1.8.3.5'
	
	while True:
		#client.ping('Autohost_CTL')
		msg=client.sysCTLTrigger('Autohost_CTL').split()
		i=3
		#print ('i is '+str(i))
		#print ('printing msg')
		#print (msg)
		if msg[3] == 'sysctl': #applet for sysctl
			
			if msg[4] == 'gem': #applet for game actions
				gameParas['dataType']='gem'
				while i<len(msg):
					if msg[i] == 'host':
						gameParas['action']='host'
					if msg[i] == 'title':
						gameParas['title']=msg[i+1]
					i=i+1
				#print(gameParas)
				if gameParas['action']=='host':
					print("hosting")
					battle = Battle(startDir,q, autohost, password, map_file, mod_file, engineName, engineVersion, mapName,roomName, gameName, battlePort)  # change username, password annd room name everytime call this line
					time.sleep(1)
					battle.start()
					
					
		
	
	

	#time.sleep(10)
	#battle2 = Battle(startDir,q, autohost, password, map_file, mod_file, engineName, engineVersion, mapName, 'aaa', gameName, battlePort)  # change username, and room name everytime call this line
	#time.sleep(1)
	#battle2.start()
	
	print(colored('[INFO]', 'green'), colored('Main: Halting.', 'white'))
	time.sleep(10)

