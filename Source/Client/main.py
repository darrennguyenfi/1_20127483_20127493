from client import *
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import json
from fuctionlabe import*


def handleAccountClosing(root):
    if messagebox.askokcancel("Quit", "Do you want to disconnect?"):
        send(DISCONNECT_MESSAGE)
        data = receive()
        print(data)
            
        try:
            time.sleep(5)
        except data!="":
            exit
        root.destroy()
        exit()


def inputData(username, password, choice):
    if(choice == "login"):
        send("log in")
        data = receive()
    elif(choice == "signUp"):
        send("sign up")
        data = receive()
    send(username)
    data = receive()
    send(password)
    data = receive()

    result = receive()

    print(result)
    if result == "LOG IN SUCCEED":
        messagebox.showinfo("Notification", "Log in Successful")
        OMG()
    elif result == "LOG IN FAILED":
        messagebox.showinfo(
            "Notification", "Username or Password is incorrect, try again")
    elif result == "SIGN UP SUCCEED":
        messagebox.showinfo("Notification", "Sign up Successful")
        OMG()
    elif result == "SIGN UP FAILED":
        messagebox.showinfo("Notification", "Username is used, try again")

def themes():
    root = Tk()
    root.title('GoldPrice')
    root.geometry("1090x613")

    bg = PhotoImage(file="GoldPrice.png")
    # Create a label
    my_label = Label(root, image=bg)
    my_label.place(x=0, y=0, relwidth=1, relheight=1)
    # Add something to the left
    frame1 = Frame(root, width=100, bg="white")
    frame1.grid(row=0, column=0, padx=120, pady=300, ipadx=0, ipady=0)

    usernamel1 = Label(frame1, text="Username:", font=(16), bg="white")
    usernamel1.grid(row=0, column=0, ipadx=1, ipady=1)
    username = Entry(frame1, font=(5), bg="white")
    username.grid(row=0, column=1)

    passwordl1 = Label(frame1, text="Password:", font=(16), bg="white")
    passwordl1.grid(row=1, column=0, ipadx=1, ipady=1)
    password = Entry(frame1, font=(5), bg="white", show='*')
    password.grid(row=1, column=1)

    close = Button(frame1, text="close", font=(16), bg="white")
    close.grid(row=3, column=0, ipadx=1, ipady=0)

    nonen = Label(frame1, bg="white")
    nonen.grid(row=2, column=0)

    login = Button(frame1, text="Log In", font=(5), width=10, bg="white",
                   command=lambda: inputData(username.get(), password.get(), "login"))
    login.grid(row=3, column=0)

    signup = Button(frame1, text="Sign Up", font=(5), width=10, bg="white",
                    command=lambda: inputData(username.get(), password.get(), "signUp"))
    signup.grid(row=3, column=1)
    root.protocol("WM_DELETE_WINDOW", lambda: handleAccountClosing(root))
    root.mainloop()


# main
try:
    themes()
except:
    exit()
