import socket 
import threading
import time
import requests
import json
#define
HEADER = 2048
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
HOST = socket.gethostname()

ACTIVE_USERS = []

ACCOUNT = {"admin" : "@@"}
ACCOUNT_PATH = "account.txt"



def send(conn, msg):
    conn.send(msg.encode(FORMAT))

def receive(conn):
    res = conn.recv(HEADER).decode(FORMAT)
    return res

def sendFile(conn, fileAddr):
    file = open(fileAddr, 'r', encoding=FORMAT)
    file_data = file.read()
    send(conn, file_data)
    print ("file send success")
    file.close()

#function to load data from account file to ACCOUNT
def load_ACCOUNT(ACCOUNT):
    with open(ACCOUNT_PATH, "r") as f:        
        while True:
            x = f.readline()
            x = x.replace("\n", "")
            if not x: #reach the end of file
                break
            y = f.readline()
            y = y.replace("\n", "")

            ACCOUNT.update({x : y})

    print(ACCOUNT)


#LOGIN
def check_log_in(conn):
    #nhan username va password tu client
    send(conn, "YOU ARE LOGGING IN")
    
    username = receive(conn)
    print("user: " + username)
    send(conn,"ok")
    password = receive(conn)
    print("pass: " + password)
    send(conn,"ok")
    #kiem tra xem co phai tin nhan dong ket noi khong
    if (username != DISCONNECT_MESSAGE and password != DISCONNECT_MESSAGE):
    #kiem tra xem co trong ACCOUNT hay khong
        if username in ACCOUNT and ACCOUNT[username] == password:
            
            send(conn, "LOG IN SUCCEED")
            return True
        else:
            send(conn, "LOG IN FAILED")
            return False
    else: 
        send(conn, "BYE")
        return False

#SIGNUP
def check_sign_up(conn):
    #nhan username va password tu client
    send(conn, "YOU ARE SIGNING UP")
    
    username = receive(conn)
    print("user: " + username)
    send(conn,"ok")
    password = receive(conn)
    print("pass: " + password)
    send(conn,"ok")

    #kiem tra co phai tin nhan dong ket noi khong
    if (username != DISCONNECT_MESSAGE and password != DISCONNECT_MESSAGE):
    #kiem tra xem co trong ACCOUNT hay khong
        if username in ACCOUNT:
            send(conn, "SIGN UP FAILED")
            return False
        else:
            ACCOUNT.update({username : password})
            #add new account into file
            with open("account.txt", "a") as f: 
                f.writelines("\n" + username + "\n" + password)
            send(conn, "SIGN UP SUCCEED")
            return True
    else: 
        send(conn, "BYE")
        return False


def request(conn,data):
    
    str ="https://tygia.com/json.php?ran=0&rate=0&gold=1&bank=VIETCOM&date=now"
    str=str.replace("now",data)
    print (str)
    req = requests.get(str)
    decoded_data=req.text.encode().decode('utf-8-sig') 
    data = json.loads(decoded_data)

    with open("data.json", "w") as f:
        f.write(json.dumps(data, indent=4))

    with open("data.json","r") as streamIn:
        DataGold = json.loads(streamIn.read())
    
    ListValueGold = DataGold["golds"][0]["value"]

    temp=[]
    for value in ListValueGold:
            temp.append(value)   
    sendList(conn,temp)  

def sendList(conn,msg):
    send(conn,str(len(msg)))
    for num in range(0,len(msg)):
        company=msg[num]["company"]
        sell=msg[num]["sell"]
        buy=msg[num]["buy"]
        brand=msg[num]["brand"]
       
        brand1=msg[num]["brand1"]
        send(conn,company)
        time.sleep(0.05)
        if sell=="":
            send(conn,"NODATA")
        else :
            send(conn,sell)
        time.sleep(0.05)
        if buy=="":
            send(conn,"NODATA")
        else :
            send(conn,buy)
        time.sleep(0.05)
        if brand=="":
            send(conn,"NODATA")
        else :
            send(conn,brand)
        time.sleep(0.05)
        if brand1=="":
            send(conn,"NODATA")
        else :
            send(conn,brand1)
        time.sleep(0.05)



def request1(conn,time,type):
    # URL
    webUrl = "https://tygia.com/json.php?ran=0&rate=0&gold=1&bank=VIETCOM&date=now"
    webUrl = webUrl.replace("now",time)
 
    req = requests.get(webUrl)
    decoded_data=req.text.encode().decode('utf-8-sig') 
    # Dict
    data = json.loads(decoded_data)

    with open("data.json","w") as fi:
        # Dump return str
        fi.write(json.dumps(data,indent=4))
    
    with open("data.json","r") as streamIn:
        DataGold = json.loads(streamIn.read())
    
    ListValueGold = DataGold["golds"][0]["value"]

    temp=[]
    for value in ListValueGold:
        if value["type"] == type:
            temp.append(value)
            
    sendList(conn,temp)  
    




def handle_cmd(conn, cmd,cmd1) :
 
    if cmd == DISCONNECT_MESSAGE:
        return
    elif cmd1=="none" :
        request(conn,cmd)
    
    else :
        request1(conn,cmd,cmd1)
    
