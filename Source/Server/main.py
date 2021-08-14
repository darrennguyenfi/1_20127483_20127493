
#Create a label
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import tkinter
from server import*


load_ACCOUNT(ACCOUNT)

 #create new socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn,addr):
    while True:
        msg = receive(conn)
        print(msg)
        check = False #check if Client log in or sign up successful to do the next task

        if msg == "log in":
            check = check_log_in(conn)
            while check:
                cmd = receive(conn)
                send(conn,"ok1")
                cmd1=receive(conn)
                print(cmd)
                print(cmd1)
                #send(conn,"ok3")
               
                handle_cmd(conn, cmd,cmd1)
        elif msg == "sign up":
            check = check_sign_up(conn)
            while check:
                cmd = receive(conn)
                send(conn,"ok1")
                cmd1=receive(conn)
                handle_cmd(conn, cmd,cmd1)
        elif msg == DISCONNECT_MESSAGE:
            print("ok1234")
            send(conn, "BYE")
            ACTIVE_USERS.remove(conn)
            conn.close()
    
    ACTIVE_USERS.remove(conn)
    conn.close()

def center(toplevel):
    toplevel.update_idletasks()

    # Tkinter way to find the screen resolution
    screen_width = toplevel.winfo_screenwidth()
    screen_height = toplevel.winfo_screenheight()

    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = screen_width/2 - size[0]/2
    y = screen_height/2 - size[1]/2

def handleClosing(window):
     if messagebox.askokcancel("Quit", "DO YOU WANT TURN OFF SERVER ?"):
        window.destroy()
        exit   

def handleListenButton(window, n):
    window.destroy()
    notiWindow(n)

def serverWindow():
    window = Tk()
    window.title("Server's window")
    window.geometry("500x613")
    center(window)
    pic = PhotoImage(file="deal.png")
    #Create a label
    my_label= Label(window,image= pic)
    my_label.place(x=0,y=0,relwidth=1,relheight=1)

    nLabel = tkinter.Label(window, text="Enter max number of clients can access: ",padx=50,pady=100 , bg="white")
    nTextBox = Entry(window, width=20)
    listenButton = Button(window, text = "Start listening", command = lambda: handleListenButton(window, int(nTextBox.get())))

    nLabel.pack()
    nTextBox.pack()
    listenButton.pack()

    window.protocol("WM_DELETE_WINDOW", lambda: handleClosing(window))
    window.mainloop()

def notiWindow(n):
    window = Tk()
    window.title("Notification")
    window.geometry("1000x600")
    center(window)

    global noti
    noti = Text(window, height = 150, width = 150)
    noti.pack(fill = BOTH)

    noti.insert(END, f"[LISTENING] Server is listening on {SERVER}\n". format(SERVER = SERVER))
    server.listen()
    thread = threading.Thread(target = handle_connect, args = (noti,))
    thread.start()
    #thread.setDaemon(True)

    window.protocol("WM_DELETE_WINDOW", lambda: handleClosing(window))  
    window.mainloop()

    
    
def handle_connect(noti):
    while True:
        #i += 1
        conn, addr = server.accept()
        noti.insert(END, f"[NEW CONNECTION] {addr} connected.\n")
        ACTIVE_USERS.append(conn)
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()
        #test
        #thread.setDaemon(True)
        noti.insert(END, f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}\n")

#main
serverWindow()
server.close()