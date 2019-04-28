
#	CS3031 A Web Proxy Server
#	Name: David scolard
#	Student Number: 16322277


#import modules
import socket, sys, zlib

from thread import *

max_conn = 20	 # Max number of connections to proxy server
buffer_size = 8192 	# Max socket buffer size
cache = {}


# Management Console
def main():
	while 1:
		try:
			# Get user input.
			user_input = raw_input("\n-- Main Menu --\n[1] Start proxy server\n[2] Add URL to blacklist\n[3] Remove URL from blacklist\n[Ctrl+C] To exit.\n\nEnter Number: ")
			
			# If they wish to start the proxy server then get port number and run the server
			if(user_input == '1'):
				runServer() # Call runServer

			# If user chooses to add url to blacklist then execute this.
			elif(user_input == '2'):
				blacklistURL()

			# If they wish to remove URL from blacklist execute this. 
			elif(user_input == '3'):
				removeFromBlacklist()

			else:
				print "Invalid entry.\n"

		except KeyboardInterrupt: 	# Ctrl+C to exit
			print "\n-->  User requested an interrupt"
			print "-->  Application Exiting..."
			sys.exit()


def runServer():
	try:
		listening_port = int(raw_input("-->  Enter listening port number: ")) #Get port number to run server on
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 	#Initiate socket
		s.bind(('', listening_port)) 	#Bind socket to listening port
		s.listen(max_conn) 	#Start listening for incoming connections
		print "-->  Initialising sockets ... Done"
		print "-->  Sockets binded successfully ..."
		print ( "-->  Server started successfully [%d]\n" % (listening_port))
	except Exception, e:
		#Execute this if anything fails
		print "-->  Unable to initalise socket"
		sys.exit(2)

	while 1:
		try:
			conn, addr = s.accept() 	# Accept connection
			data = conn.recv(buffer_size) 	# Receive data
			start_new_thread(conn_string, (conn,data,addr)) 	#Start a thread for client
		except KeyboardInterrupt:
			#Execute this block if client socket failed
			s.close()
			print "\n-->  Proxy Server Shutting Down..."
			sys.exit(1)
	s.close()


def conn_string(conn, data, addr):
	#Client browser request 
	try:
		first_line = data.split('\n')[0]
		url = first_line.split(' ')[1]
		http_pos = url.find("://")

		if(http_pos == -1):
			temp = url
		else:
			temp = url[(http_pos+3):]	 #Get rest of the url

		blacklist = False 	#Boolean to check if url is blacklisted
		searchfile = open("blacklist.txt", "r") 	#Read blacklist.txt

		for line in searchfile:
		    if url in line: 
		    	print url + " -->  Website is not permitted on this server."
		    	blacklist = True 	#Mark blacklist as true if url is found in blacklist.txt    
		searchfile.close()

		if blacklist == False:		#Access webpage if not blacklisted
			print url + " -->  Accessing WebPage." 
			port_pos = temp.find(":") 	# Find position of the port
			webserver_pos = temp.find("/") 	# Find end of the webserver
			if webserver_pos == -1:
				webserver_pos = len(temp)
			webserver = ""
			port = -1
			if(port_pos==-1 or webserver_pos < port_pos):
				port = 80  # Default port
				webserver = temp[:webserver_pos]
			else:
				#Specific port
				port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
				webserver = temp[:port_pos]

			proxy_server(webserver, port, conn, data)	 #Call proxy
	except Exception, e:
		pass


def proxy_server(webserver, port, conn, data):
	try:
		# Sends request to the webserver
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 	#Initiate socket
		s.connect((webserver,port))	 # Connect to webserver
		s.sendall(data) 	

		while 1:
			reply = s.recv(buffer_size) 
			if(len(reply) > 0):
				conn.send(reply)	 #Send reply to browser
			else:
				break

		s.close()	#Close server sockets
		conn.close()	#Close client socket
	except socket.error, (value, message):
		s.close()
		conn.close()
		sys.exit(1)


def blacklistURL():
	urlToBlacklist = raw_input("-->  Enter url to add to blacklist: ")	 # Ask for url to be blacklisted
	f = open('blacklist.txt', 'a') 	# Open blacklist file
	f.write(urlToBlacklist+"\n")	 # Add url to blacklist
	f.close() 	# Close file
	print "-->  " + urlToBlacklist + " has been added to the blacklist.\n"
	main()
  

def removeFromBlacklist():
	urlToDelete = raw_input("-->  Enter URL to remove from blacklist: ")
	f = open("blacklist.txt","r") 	#Open File
	lines = f.readlines() 	#Get lines from file
	f.close()	#Close file
	f = open("blacklist.txt", "w") 	#Reopen in write mode
	for line in lines: 	# Scan blacklist.txt line by line
		if line!=urlToDelete+"\n": 	#Rewrite all lines except the url chosen to delete
			f.write(line)
	f.close()
	print "-->  "+urlToDelete + " has been removed from the blacklist.\n"
	main()



if __name__ == '__main__':
	main()






