import struct
from struct import *
import socket 
import binascii
import ctypes
import time
"""ΚΩΔΙΚΑΣ ΕΡΓΑΣΤΗΡΙΟΥ"""
#Host IP to send to.
serverIP = '127.0.0.1'
#Port to send to
serverPort = 12345

#Create the client socker
#socket.AF_INET == IPv4
#socket.SOCK_STREAM == TCP
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Connect. The server socket should be listening.
clientSocket.connect((serverIP, serverPort))
"""ΤΕΛΟΣ ΚΩΔΙΚΑ ΕΡΓΑΣΤΗΡΙΟΥ"""
"""ο header ειναι σημειωμενος στο PDF"""
#αρχικα ζηταμε απο τον client να διαλεξει τη πραξη που θελει να κανει (τιμη type του header)
print("choose desired operation (1 for product, 2 for mean, 3 for subtraction): ")
msgtype=int(input())
msgvalues=[] #οριζουμε τη λιστα msgvalues οπου εδω θα βαλουμε τους αριθμους για τη πραξη που θα διαλεξει ο χρηστης (τιμη Values του Header)
while msgtype not in range(1,4): #ελεγχος εγκυροτητας τιμων για να σιγουρευτουμε οτι βαζει σωστη τιμη
    print("try again: ")
    msgtype=int(input())

if msgtype==1: #για τον πολλαπλασιασμο του ζηταμε να βαλει το συνολο των αριθμων (τιμη length του header )
    msglength=int(input("operation 1: product. Insert amount of numbers you want to add (must be between 2 and 10): "))
    while msglength not in range(2,11):
        msglength=int(input("Try again. insert a value between 2 and 10: ")) #ελεγχος εγκυροτητας για να ειναι στο πεδιου ορισμου η τιμη που οριζει
    for i in range(0,msglength):
        num=int(input("insert number in domain [-5,5]: ")) #ελεγχος εκγυροτητας για τους αριθμους που εισαγει
        while num not in range(-5,6):
            num=int(input("Number inserted must be at between -5 and 5: "))
        msgvalues.append(num) #μετα αφου εισαγουμε ολες τις τιμες στη λιστα κανουμε Pack τους αριθμους
    numspacked=struct.pack(f'!{msglength}b',*msgvalues) #ο server στη πραξη 1 δεχεται τιμες απο -5 εως 5
    #επομενως μπορουμε να αναπαραστησουμε το συνολο τιμων αυτο με το format b το οποιο ειναι μεγεθους n=1 byte και signed char (δεχεται αρνητικες τιμες)
    #επομενως το ευρος τιμων που μπορει να δεχτει ειναι
    #-2^(n*8)/2 εως (2^(n*8)/2) - 1 = -128 εως 127

elif msgtype==2: #υπολογισμος μεσου ορου, κανουμε την ιδια διαδικασια οπως και πανω μεχρι το formatting.Η μονη διαφορα ειναι το ευρος τιμων που μπορει να εισαγει
    msglength=int(input("operation 2: Mean of n integers. Insert amount of numbers you want to add (must be between 2 and 20): "))
    while msglength not in range(2,21):
        msglength=int(input("insert value between 0 and 20: ")) #0 εως 20 αντι για 0 εως 10, βεβαια δε μας απασχολει αυτο εφοσον η λιστα ειναι δυναμικη δομη δεδομενων
    for i in range(0,msglength):
        num=int(input("insert number in domain [0,200]"))
        while num not in range(0,201):
            num=int(input("Number inserted must be at between 0 and 200: "))
        msgvalues.append(num) 
    numspacked=struct.pack(f'!{msglength}I',*msgvalues) #στη πραξη 2 ο server δεχεται τιμες απο 0 εως 200 επομενως 1 byte δεν μας αρκει για το packing.
    #επομενως θα χρησιμοποιησουμε το format I που ειναι 4 Bytes unsigned αριθμος οπου δεχεται τιμες απο 0 εως 4294967295 
    # (η χρηση του H που ειναι 2 bytes μου εβγαζε σφαλμα, μαλλον επειδη θελει τουλαχιστον 2 bytes)


else:
    msglength=int(input("operation 3: subtraction. Insert amount of numbers you want to add (must be between 2 and 10): "))
    while msglength not in range(2,11):
        msglength=int(input("insert value between 0 and 10: "))
    for i in range(0,msglength):
        num=int(input("insert number in domain [0,60000]: ")) #στην αφαιρεση ο server δεχεται τιμες απο 0 εως 60000
        while num not in range(0,60001):
            num=int(input("Number inserted must be at between 0 and 60000: "))
        msgvalues.append(num) 
    numspacked=struct.pack(f'!{msglength}I',*msgvalues) #ομοιως με την αφαιρεση θα χρησιμοποιησουμε το format I εφοσον ο αριθμος 60000 θελει τουλαχιστον 2bytes για την αναπαρασταση του
#εδω κανουμε ολο το header σε ενα μηνυμα σειριακα (βασισμενο στον κωδικα του εργαστηριου)
message = struct.pack('!H', msgtype)
message = message + struct.pack('!H', msglength)
message = message + numspacked

#και εδω αρχικα κανουμε πριντ οτ μηνυμα σε hex και μετα το στελνουμε
print('Message in hex to send to server')
print(binascii.hexlify(message))
clientSocket.sendall(message)

#ΑΠΑΝΤΗΣΗ ΤΟΥ SERVER
modifiedMessage = clientSocket.recv(6) #δεχομαστε 6 bytes το πολυ (type = 1 byte , length = 1 byte , values = 4 bytes το πολυ)
if msgtype==1:
    servertype,msg_responsecode,msganswer  = unpack('!BBi', modifiedMessage) #αν η πραξη ειναι πολλαπλασιασμος κανουμε Unpack signed int 
    print("operation :",servertype,"Product. ""server response code: ",msg_responsecode," server answer: ",msganswer)
elif msgtype==2:
    servertype,msg_responsecode,msganswer  = unpack('!BBf', modifiedMessage) #αν η πραξη ειναι μεσος ορος τοτε κανουμε unpack signed float (λογω της διαιρεσης)
    print("operation :",servertype,"Mean. ""server response code: ",msg_responsecode," server answer: ",msganswer)
else:
   servertype,msg_responsecode,msganswer  = unpack('!BBi', modifiedMessage) #αν η πραξη ειναι αφαιρεση τοτε κανουμε unpack signed int (μπορει να ειναι αρνητικη η τιμη)
   print("operation :",servertype,"Subtraction. ""server response code: ",msg_responsecode," server answer: ",msganswer)

time.sleep(5)
#τα prints ειναι μηνυματα απαντησης με τον κωδικο και την λυση που εδωσε ο server

    
        
