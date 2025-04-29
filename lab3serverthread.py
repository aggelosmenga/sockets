#Import the socket library
import struct
from struct import *
import socket
import binascii
from _thread import *
#import για τις πραξεις
import math 
import statistics
from functools import reduce
"""ΚΩΔΙΚΑΣ ΕΡΓΑΣΤΗΡΙΟΥ"""
"""ο κωδικας για να δεχεται threads ειναι καθαρα αντιγραμμενος απο τον κωδικα του εργασστηριου εκτος απο τις πραξεις που κανει ο server
και το ποσο clients Που μπορει να δεχτει αντι για 5 (δεχεται απεριοριστους) """
def threadedclient(conn,addr):
    #Print info: Connected address, Server IP & Port, Client IP & Port
    print("Thread to handle connection by:", addr)
    print("Server Socket port: ", conn.getsockname())
    print("Client Socket port: ", conn.getpeername())

        #Handle the request
        #Receive the 4st four bytes
    while (1):
        msg = conn.recv(4)
        #Print them just for fun as hex numbers
        print("message without numbers inserted from client:",binascii.hexlify(msg))
        #We know the structure from the header specification. So we need to unpack them. 
        #H stands for short. So, 'HH' are two shorts (two 16-bit unsigned integers)
        """ΤΕΛΟΣ ΚΩΔΙΚΑ ΕΡΓΑΣΤΗΡΙΟΥ"""
        """ο header ειναι σημειωμενος στο PDF"""
        msg_type,msg_length = struct.unpack('!HH', msg) #μετα αφου καναμε Unpack το type και το length πρεπει να κανουμε Unpack τη λιστα των αριθμων
        buffer_size = 4 + (msg_length * 4) + 1 #με τη χρηση του Buffer size μπορουμε να παμε στο μηνυμα και να βρουμε τη λιστα χωρις padding
        msg = conn.recv(buffer_size) #εδω γινεται το unpacking με βαση το ειδος της πραξης που θελει ο client να εφαρμοσει
        #με βαση το msg_type που καναμε Unpack απο το μηνυμα μπορουμε να βρουμε τη πραξη που διαλεξε και ετσι να κανουμε Unpack σωστα τους αριθμους
        #εφοσον δωσαμε περιορισμους απο το σημειο του client
        if msg_type==1:
            msgnums = struct.unpack(f'!{msg_length}b', msg) #στον κωδικα του client αναφερεται ο λογος που διαλεξαμε αυτα τα fomarts
        elif msg_type==2:
            msgnums = struct.unpack(f'!{msg_length}I',msg)
        else:
            msgnums=struct.unpack(f'!{msg_length}I', msg)
        



        #We're done receiving. Now we need to do our processing of the packet.

        #Initial response code is 0. if there is an error, server will send 0
        msg_response_code = 0
        #This is completely optimal
        #κανουμε pack με βαση το server header το μηνυμα,παραλληλα κανουμε και τη πραξη που ζητησε ο client ως ενα int αντι για μια λιστα με Ints
        #οι πραξεις γινονται με τις βιβλιοθηκες που εβαλα
        if msg_type==1:
            msg_response_code = 11
            product=math.prod(msgnums)
            message = pack('!BBi', msg_type, msg_response_code,product)
        elif msg_type==2:
            msg_response_code=22
            mean=statistics.mean(msgnums)
            message=pack('!BBf',msg_type,msg_response_code,mean)
        else:
            msg_response_code=33 #response code ειναι τυχαιο το εβαλα εγω και δεν αλλαζει το προγραμμα με καποιο τροπο
            subtract=reduce(lambda x,y:x-y,msgnums)
            message = pack('!BBi', msg_type, msg_response_code,subtract)


        #Send the message through the same connection
        err = conn.sendall(message)
        #Print any errors if any exist
        print("errors: ",err)
#Αν ολα πηγαν καλα ο server θα προσπαθησει να διαβασει μηνυμα ενω η συνδεση του client εχει κλεισει, αυτο ειναι απολυτα φυσιολογικο

#Host IP to listen to. If '' then all IPs in this interface
serverIP = ''
#Port to listen to
serverPort = 12345
#Flag to close the socket. Normally we don't close the socket. We keep on listening. 
#This flag is used to simply terminate the program and close the socket as we don't need it after
#the message exchange
close = False
#Create the server socker
#socket.AF_INET == IPv4
#socket.SOCK_STREAM == TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
    #Bind the socket
    serverSocket.bind((serverIP, serverPort))
    print ("The server is ready to receive at port", str(serverPort))
    #Listen for connections
    #If we don't specify in the listen a number e.g. serverSocket.listen(5), it goes to the system default
    serverSocket.listen()
    ThreadCount=0
    while not close:
        conn, addr = serverSocket.accept()
        #Listen and wait for connection
        #Once a connection is made it returns two values, the conn will have the connection socket and the addr will have the address
        #These will be passed to the Thread to handle the connection. The main program will go on
        start_new_thread(threadedclient, (conn, addr))
        ThreadCount+=1
        print('Thread Number: ' + str(ThreadCount))

        #Signal (with the flag) to close the socket
        #close=True