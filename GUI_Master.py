from tkinter import *

class RootGUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("Serial Communication")
        self.root.geometry("360x120")
        self.root.config(bg="white")

class ComGUI():
    def __init__(self, root,serial):
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
        coms=["-", "COM3", "COM4", "COM5"]
        self.click_com=StringVar()  #  StringVar() is used to edit a widget's text
        self.click_com.set(coms[0])
        self.drop_com = OptionMenu(
            self.frame, self.click_com, *coms, command=self.connect_ctrl
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
        print("Refresh")

    def serial_connect(self):
        print("Connect")

if __name__ == "main":
    RootGUI()
    ComGUI()