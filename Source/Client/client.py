import json
import socket
import tkinter as tk
from tkinter import *
HEADER = 2048
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#create new socket and connect to server
address_wd = Tk()
address_wd.title('Address')
entry = Entry(address_wd, width=37)
entry.pack(side=LEFT, padx=15)

def Click():
    global SERVER
    SERVER=entry.get()
    ADDR = (SERVER,PORT)
    client.connect(ADDR)
    address_wd.destroy()
    
address_button = Button(address_wd, text='OK', command=Click,width=10)
address_button.pack(side=RIGHT,padx=15)
address_wd.geometry('450x100')
address_wd.mainloop()


#print(client.recv(2048).decode(FORMAT))
def send(msg):
    client.send(msg.encode(FORMAT))

def receive():
    res = client.recv(HEADER).decode(FORMAT)
    return res
    
def receiveFile (fileAddr):
    file = open(fileAddr, 'w', encoding=FORMAT)
    file_data = receive()
    file.write(file_data)
    file.close()
    print("File has been received successfully.")
    file.close()   

def receiveList():
    res=[]
    data=""
    while (data!="endData"):
        data=receive()
        if data=="endData":
            break;
        data=json.loads(data)
        res.append(data)
        buy=data["buy"]
        sell=data["sell"]
        company=data["company"]
        brand=data["brand"]
        brand1=data["brand1"]
        id=data["id"]
        print ("gia ban"+str(sell)+"gia mua"+str(buy))
        print("\n")
        return res
        