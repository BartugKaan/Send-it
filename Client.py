import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog, messagebox, LEFT
import time


hostInput = simpledialog.askstring("IP : ","Please write host IP", show='*')
currentTime = time.strftime("%H:%M:%S")



HOST = hostInput
PORT = 59429

class Client:

    #constructor
    def __init__(self,host,port):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((host,port))

        #Frame
        msg = tkinter.Tk()
        msg.title("Send It")
        msg.withdraw()

        self.nickname = simpledialog.askstring("Nickname : ","Please chose a nickname", parent=msg)
        while self.nickname == "":
            messagebox.showerror("Warning!", "Blank Not Allowed!")
            self.nickname = simpledialog.askstring("Nickname : ", "Please chose a nickname", parent=msg)
        messagebox.showinfo("Welcome", f" Greetings, {self.nickname}")


        #Boolean controller for gui
        self.gui_done = False
        #Boolean controller for program
        self.running = True

        #Threads
        gui_thread = threading.Thread(target=self.gui_loop)
        recv_thread = threading.Thread(target=self.receive)
        gui_thread.start()
        recv_thread.start()

    #Builds to all Gui
    def gui_loop(self):
        # Builds Guı Front-End
        self.win = tkinter.Tk("Send It")
        self.win.title("Send It")
        self.win.configure(bg="navajowhite")
        self.logoLabel = tkinter.Label(self.win, text="Send it", bg="navajowhite", fg="white", font=("Cooper Black", 34)).place(x=0, y=30)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win, bg="white", height=40, width=55)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state="disabled")

        self.msg_label = tkinter.Label(self.win, text="your message:", bg="navajowhite", fg="white",
                                       font=("Cooper Black", 22))

        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(side=LEFT, padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="send it", bg="navajowhite", fg="white",
                                          font=("Cooper Black", 22), command=self.write)
        self.send_button.pack(side=LEFT, padx=15, pady=20)
        self.win.bind('<Return>', lambda event: self.write())


        self.gui_done = True
        self.win.protocol("WM_DELETE_WİNDOW", self.stop)
        self.win.mainloop()

    #Get text form input_area then send to the server after that deletes from input_area
    def write(self):
        message = f"[{currentTime}] {self.nickname}: {self.input_area.get('1.0','end')}" # '1.0','end' means get the whole text
        striped_message = message.strip() + "\n"
        self.sock.send(striped_message.encode("utf-8"))
        self.input_area.delete('1.0', "end")


    #Close and exit from program
    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    #Its like handle function from Server gets new messages
    def receive(self):
        while self.running:
            try:
                # gets messages from the server
                message = self.sock.recv(1024).decode("utf-8")
                if message == "NICK": #If server asks for nickname clients send the nickname
                    self.sock.send(self.nickname.encode("utf-8"))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal') # now we can change the text_area
                        self.text_area.insert('end', message) #insert the messages to the end
                        self.text_area.yview('end') # always scrol to down
                        self.text_area.config(state='disabled') # now we can not change the text_area
            except ConnectionAbortedError:
                break
            except:
                break

Client = Client(HOST,PORT)