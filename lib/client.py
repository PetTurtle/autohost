from base64 import b64encode
from hashlib import md5
from lib.quirks.network import Network
from lib.quirks.unitSync import UnitSync
from serverlauncher import ServerLauncher
from termcolor import colored
import time



class Client():

	def __init__(self, battlePort, startDir):
		
		self.network = Network()
		self.network.connect('127.0.0.1')
		self.battlePort=battlePort
		self.startDir=startDir
	
	def sysCTLTrigger(self,username):
		#print("trigger running")
		self.network.receive()
		#return "word to split"
		if self.network.hasCmd():
			print("network has cmd!")
			chatBuffer=self.network.nextCmd()
			#self.network.receive()
			if 'sysctl' in chatBuffer:
				#print("trigger triggered!")
				return chatBuffer
			elif self.network.hasCmd():
				chatBuffer=self.network.nextCmd()
				if 'sysctl' in chatBuffer:
					#print("rescan!")
					return chatBuffer
				elif self.network.hasCmd():
					chatBuffer=self.network.nextCmd()
					if 'sysctl' in chatBuffer:
						#print("rescan #2!")
						return chatBuffer
					else:
						print("3 scans returned nothing, probably not a cmd line!")
						return "3 scans returned nothing, probably not a cmd line!"
		print("probably an empty line!")
		return "probably an empty line!"

	def login(self, username,password, local_ip='*', cpu=0):
		password = b64encode(md5(password).digest()).decode('utf8')
		command = 'LOGIN %s %s %i %s' % (username, password, cpu, local_ip)
		self.network.send(command)



	def openBattle(self, battle_type, nat_type, password, port, max_players, mod_hash, rank, map_hash, engine_name, engine_version, map_name, title, game_name):
		command = 'OPENBATTLE %i %i %s %i %i %i %i %i %s\t%s\t%s\t%s\t%s' % (battle_type, nat_type, password, port, max_players, mod_hash, rank, map_hash, engine_name, engine_version, map_name, title, game_name)
		self.network.send(command)


	def startBattle(self):
		time.sleep(2)
		command = 'MYSTATUS 1'
		self.network.send(command)


	def keepalive(self,username):
		
		command = 'PING'
		self.network.send(command)
		

		while (True):
			self.network.send(command)
			print(colored('[INET]', 'grey'), colored(username+': keeping alive', 'white'))
			time.sleep(5)
			
	def ping(self,username):
		
		command = 'PING'
		self.network.send(command)
	
	
	def joinChat(self, channel):
		print('joining')
		command = 'JOIN '+channel
		self.network.send(command)
		


	def clearBuffer(self, username):
		self.network.receive()

		
		while(self.network.hasCmd()):
			#self.network.nextCmd()
			print(colored('[INET]', 'grey'), colored(username+': '+self.network.nextCmd(), 'white'))

