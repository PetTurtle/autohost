import time
import _thread
import threading
from multiprocessing import Queue
from lib.client import Client
from lib.quirks.unitSync import UnitSync
from termcolor import colored

class Battle(threading.Thread):

	def __init__(self,startDir,q, autohostFactory, password, map_file, mod_file, engineName, engineVersion, mapName, roomName, gameName,battlePort):
		threading.Thread.__init__(self)
		
		self.username = autohostFactory.new_autohost()

		print(colored('[INFO]', 'green'), colored(self.username+': Autohost account received!.', 'white'))
		self.password=password
		self.map_file=map_file
		self.mod_file=mod_file
		self.engineName=engineName
		self.engineVersion=engineVersion
		self.mapName=mapName
		self.roomName=roomName
		self.gameName=gameName
		self.q=q
		self.battlePort=battlePort
		self.startDir=startDir
		
	def run(self):

		print(colored('[INFO]', 'green'), colored(self.username+': Loading unitsync.', 'white'))
		unitSync = UnitSync( self.startDir+'/engine/libunitsync.so')
		unitSync.startHeshThread(self.map_file,self.mod_file)
		unit_sync = unitSync.getResult()


		
		client = Client(self.battlePort,self.startDir)
		
		client.login(self.username,self.password)

		print(colored('[INFO]', 'green'), colored(self.username+': Logging in', 'white'))
		client.clearBuffer(self.username)
		
		client.openBattle(0, 0, '*', self.battlePort, 5, unit_sync['modHesh'], 1, unit_sync['mapHesh'], self.engineName, self.engineVersion, self.mapName,  self.roomName, self.gameName)
		print(colored('[INFO]', 'green'), colored(self.username+': Opening Battle.', 'white'))
		client.clearBuffer(self.username)

		
		_thread.start_new_thread( client.keepalive,(self.username,))
		client.clearBuffer(self.username)
		
		client.joinChat('bus')
		print(colored('[INFO]', 'green'), colored(self.username+': Joining Battle Chat.', 'white'))
		client.clearBuffer(self.username)
		
		#try:
		#_thread.start_new_thread( client.observeChat,(self.username,))
		print(colored('[INFO]', 'green'), colored(self.username+': Monitoring Battle Chat.(idling)', 'white'))
		#except:
		#	print ("Error: unable to observe chat")
		
		
		

			
		



		return	

#sock.close()
