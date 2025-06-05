from tkinter import *
from tkinter import messagebox

class RootGUI:
    def __init__(self):
        '''Initalizes the root window for the GUI and communications of the program'''
        self.root = Tk()
        self.root.title("Serial Communication")
        self.root.geometry("360x120")
        self.root.config(bg="white")

class ComGUI():
    def __init__(self, root, serial):
        '''     Initalizes the connection to the GUI and main widgets   '''
        # Frame
        self.root=root
        self.serial=serial
        self.frame=LabelFrame(root, text="Com Manager", padx=5, pady=5,bg="white")
        self.label_com = Label(
            self.frame, text="Available Port(s): ", bg="white", width=15, anchor="w"
        )
        self.label_bd = Label(
            self.frame, text="Baude Rate: ", bg="white", width=15, anchor="w"
        )
        self.ComOptionMenu()
        self.BaudOptionMenu()

        self.btn_refresh = Button(self.frame, text="Refresh", width=10,command=self.com_refresh)
        self.btn_connect = Button(self.frame, text="Connect", width=10, state="disabled", command=self.serial_connect)

        self.padx=20
        self.pady=5
        self.publish()

    def ComOptionMenu(self):
        self.serial.getCOMList()                    # With the getCOMList() function we no longer need the hard coded values of different ports
        self.click_com=StringVar()                  # StringVar() is used to edit a widget's text
        self.click_com.set(self.serial.com_list[0]) # Instead of reference the previous (com[0]) we can reference the self variable which has com_list as a child
        self.drop_com = OptionMenu(
            self.frame, self.click_com, *self.serial.com_list, command=self.connect_ctrl
        )
        self.drop_com.config(width=10)
    
    def BaudOptionMenu(self):
        bauds = ["-","300","600","1200","2400","4800","9600","14400","19200","28800","38400","56000","57600","115200","128000","256000"]
        self.click_baud=StringVar()  #  StringVar() is used to edit a widget's text
        self.click_baud.set(bauds[0])
        self.drop_baud = OptionMenu(
            self.frame, self.click_baud, *bauds, command=self.connect_ctrl
        )
        self.drop_baud.config(width=10)
        
    def publish(self):
        self.frame.grid(row=0,column=0,rowspan=3,columnspan=3,padx=5,pady=5)
        self.label_com.grid(column=1,row=2)
        self.drop_com.grid(column=2,row=2,padx=self.padx,pady=self.pady)
        self.label_bd.grid(column=1,row=3)
        self.drop_baud.grid(column=2,row=3)
        self.btn_refresh.grid(column=3,row=2)
        self.btn_connect.grid(column=3,row=3)

    def connect_ctrl(self, widget):
        print("Connect ctrl")
        if "-" in self.click_baud.get() or "-" in self.click_com.get():
            self.btn_connect["state"] = "disable"
        else: 
            self.btn_connect["state"] = "active"

    def com_refresh(self):
        self.drop_com.destroy()

        self.ComOptionMenu()
        self.drop_com.grid(column=2,row=2,padx=self.padx,pady=self.pady)
        
        logic=[]
        self.connect_ctrl(logic)
        print("Refresh")

    def serial_connect(self):
        if self.btn_connect["text"] in "Connect":
            # start the connection
            self.serial.SerialOpen(self)
            # if there is a conncetion established
            if self.serial.ser.status:
                # Updates the COM manager
                self.btn_connect["text"] = "Disconnect"
                self.btn_refresh["state"] = "disable"
                self.drop_baud["state"] = "disable"
                self.drop_com["state"] = "disable"
                InfoMsg=f"Successful UART connection using {self.click_com.get()}"
                messagebox.showinfo("showinfo",InfoMsg)
            else:
                ErrorMsg=f"Failure to estabish UART connection using {self.click_com.get()} "
                messagebox.showerror("showerror", ErrorMsg)
        else:
            # close the connection
            self.serial.SerialClose(self)

            InfoMsg = f"UART connection using {self.click_com.get()} is now closed"
            messagebox.showwarning("showinfo", InfoMsg)
            self.btn_connect["text"] = "Connect"
            self.btn_refresh["state"] = "active"
            self.drop_baud["state"] = "active"
            self.drop_com["state"] = "active"

if __name__ == "main":
    RootGUI()
    ComGUI()