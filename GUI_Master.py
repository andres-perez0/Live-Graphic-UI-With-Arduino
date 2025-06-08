from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import threading

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

class RootGUI:
    def __init__(self, serial, data):
        '''Initalizes the root window for the GUI and communications of the program'''
        self.root = Tk()
        self.root.title("Serial Communication")
        self.root.geometry("360x120")
        self.root.config(bg="white")
        self.serial=serial
        self.data=data
        # Prevents the user from exiting during processes (threads)
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)   

    def close_window(self):
        print("Closing the window and exit")
        self.root.destroy()
        self.serial.SerialClose(self)
        self.serial.threading=False

class ComGUI():
    def __init__(self, root, serial, data):
        '''=Initalizes the connection to the GUI and main widgets'''
        # Includes the main frame, serial communication information, and data
        self.root=root
        self.serial=serial
        self.data=data

        self.frame = LabelFrame(root, text="Com Manager", padx=5, pady=5,bg="white")
        self.label_com = Label(self.frame, text="Available Port(s): ", bg="white", width=15, anchor="w")
        self.label_bd = Label(self.frame, text="Baude Rate: ", bg="white", width=15, anchor="w")
        
        self.ComOptionMenu()
        self.BaudOptionMenu()

        self.btn_refresh = Button(self.frame, text="Refresh", width=10,command=self.com_refresh)
        self.btn_connect = Button(self.frame, text="Connect", width=10, state="disabled", command=self.serial_connect)

        self.padx=20
        self.pady=5

        self.publish()
    
    def publish(self):
        self.frame.grid(row=0,column=0,rowspan=3,columnspan=3,padx=5,pady=5)
        
        self.label_com.grid(column=1,row=2)
        self.drop_com.grid(column=2,row=2,padx=self.padx,pady=self.pady)
        
        self.label_bd.grid(column=1,row=3)
        self.drop_baud.grid(column=2,row=3)
        
        self.btn_refresh.grid(column=3,row=2)
        self.btn_connect.grid(column=3,row=3)

    def ComOptionMenu(self):
        self.serial.getCOMList()                    # With the getCOMList() function we no longer need the hard coded values of different ports
        self.click_com=StringVar()                  # StringVar() is used to edit a widget's text
        self.click_com.set(self.serial.com_list[0]) # Instead of reference the previous (com[0]) we can reference the self variable which has com_list as a child
        self.drop_com = OptionMenu(self.frame, self.click_com, *self.serial.com_list, command=self.connect_ctrl)
        self.drop_com.config(width=10)
    
    def BaudOptionMenu(self):
        bauds = ["-","300","600","1200","2400","4800","9600","14400","19200","28800","38400","56000","57600","115200","128000","256000"]
        self.click_baud=StringVar()  #  StringVar() is used to edit a widget's text
        self.click_baud.set(bauds[0])
        self.drop_baud = OptionMenu(self.frame, self.click_baud, *bauds, command=self.connect_ctrl)
        self.drop_baud.config(width=10)   

    def connect_ctrl(self, widget):
        # print("Connect ctrl")
        if "-" in self.click_baud.get() or "-" in self.click_com.get():
            self.btn_connect["state"] = "disable"
        else: 
            self.btn_connect["state"] = "active"

    def com_refresh(self):
        # Properly destroyed the previous drop_com to ensure it doesnt stay in memory
        self.drop_com.destroy()
        # Calls to refresh the available COM ports 
        self.ComOptionMenu()
        # Replaces it on the grid
        self.drop_com.grid(column=2,row=2,padx=self.padx,pady=self.pady)
        
        logic=[]
        # Revalutes the state of the "connect" button
        self.connect_ctrl(logic)
        # print("Refresh")

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

                self.conn = ConnGUI(self.root, self.serial, self.data)

                self.serial.t1=threading.Thread(target=self.serial.SerialSync,args=(self,),daemon=True)
                self.serial.t1.start()

            else:
                ErrorMsg=f"Failure to estabish UART connection using {self.click_com.get()} "
                messagebox.showerror("showerror", ErrorMsg)

        else:
            self.serial.threading=False
            # close the connection
            self.serial.SerialClose(self)

            self.conn.ConnGUIClose()
            self.data.ClearData()

            InfoMsg = f"UART connection using {self.click_com.get()} is now closed"
            messagebox.showwarning("showinfo", InfoMsg)
            self.btn_connect["text"] = "Connect"
            self.btn_refresh["state"] = "active"
            self.drop_baud["state"] = "active"
            self.drop_com["state"] = "active"

class ConnGUI():
    def __init__(self, root, serial,data):
        self.root=root
        self.serial=serial
        self.data=data

        self.frame=LabelFrame(self.root,text="Connection",padx=5,pady=5,bg='white',width=60)

        self.sync_label = Label(self.frame, text="Sync Status: ", bg="white", width=15, anchor="w")
        self.sync_status = Label(self.frame, text="..Sync..", bg="white", fg="orange", width=5)

        self.ch_label = Label(self.frame, text="Active channels: ", bg="white", width=15, anchor="w")
        self.ch_status = Label(self.frame, text="...", bg="white", fg="orange", width=5)

        self.btn_start_stream = Button(self.frame, text="Start", state="disabled", width=5, command=self.start_stream)
        self.btn_stop_stream = Button(self.frame, text="Stop", state="disabled", width=5, command=self.stop_stream)
        self.btn_add_chart = Button(self.frame, text="+", state="disabled", width=5, bg="white", fg="#098577", command=self.new_chart)
        self.btn_kill_chart = Button(self.frame, text="-", state="disabled", width=5, bg="white", fg="#CC252C", command=self.kill_chart)

        self.save = False
        self.SaveVar = IntVar()
        self.save_check = Checkbutton(self.frame, text="Save data", variable=self.SaveVar, onvalue=1, offvalue=0, bg="white", state="disabled", command=self.save_data)
        # ttk.Seperator is what seperates the two widgets into two columns
        self.separator = ttk.Separator(self.frame, orient='vertical')

        # Optional Graphic parameters
        self.padx = 20
        self.pady = 15

        # Extending the GUI
        self.ConnGUIOpen()

    def ConnGUIOpen(self):
        self.root.geometry('800x120')
        self.frame.grid(row=0,column=4,rowspan=3,columnspan=5,padx=5,pady=5)

        self.sync_label.grid(column=1, row=1)
        self.sync_status.grid(column=2, row=1)

        self.ch_label.grid(column=1, row=2)
        self.ch_status.grid(column=2, row=2, pady=self.pady)

        self.btn_start_stream.grid(column=3, row=1, padx=self.padx)
        self.btn_stop_stream.grid(column=3, row=2, padx=self.padx)

        self.btn_add_chart.grid(column=4, row=1, padx=self.padx)
        self.btn_kill_chart.grid(column=5, row=1, padx=self.padx)

        self.save_check.grid(column=4, row=2, columnspan=2)
        self.separator.place(relx=0.58, rely=0, relwidth=0.001, relheight=1)

    def ConnGUIClose(self):
        '''
        Method to close the connection GUI and destorys the widgets
        '''
        # Must destroy all the element so they are not kept in Memory
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.frame.destroy()
        self.root.geometry("360x120")

    def start_stream(self):
        pass

    def stop_stream(self):
        pass

    def new_chart(self):
        try:
            self.chartMaster.AddChannelMaster()
        except:
            self.chartMaster=DisGUI(self.root, self.serial, self.data)

    def kill_chart(self):
        try:
            if len(self.chartMaster.frames) > 0:
                totalFrame = len(self.chartMaster.frames)-1
                self.chartMaster.frames[totalFrame].destroy()
                self.chartMaster.frames.pop()
                self.chartMaster.figs.pop()
                self.chartMaster.ControlFrames.pop()
                self.chartMaster.AdjustRootFrame()
        except:
            pass

    def save_data(self):
        pass

class DisGUI():
    def __init__(self, root, serial, data):
        self.root = root
        self.serial = serial
        self.data = data
        # Master Frame controls
        self.frames = []
        self.framesCol = 0
        self.framesRow = 4
        self.totalframes = 0

        self.figs = []

        # The control Frame
        self.ControlFrames = []

    def AddChannelMaster(self):
        self.AddMasterFrame()
        self.AdjustRootFrame()
        self.AddGraph()
        self.AddBtnFrame()

    def AddMasterFrame(self):
        self.frames.append(LabelFrame(self.root, text=f"Display Manager-{len(self.frames)+1}",
                                      pady=5, padx=5, bg="white"))
        self.totalframes = len(self.frames)-1
        # print(f'Total frames:{self.totalframes}')
        if self.totalframes % 2 == 0:
            self.framesCol = 0
        else:
            self.framesCol = 9
        # print(f'Col: {self.framesCol}')
        self.framesRow = 4 + 4 * int(self.totalframes / 2)
        # print(f'Row: {self.framesRow}')
        self.frames[self.totalframes].grid(padx=5,
                                           column=self.framesCol, row=self.framesRow, columnspan=8, sticky=NW)
    def AdjustRootFrame(self):
        '''
        This Method will generate the code related to adjusting
        the main root Gui based on the number of added GUI
        '''
        self.totalframes = len(self.frames)-1
        if self.totalframes > 0:
            RootW = 800*2

        else:
            RootW = 800

        if self.totalframes+1 == 0:
            RootH = 120
        else:
            RootH = 120 + 430 * (int(self.totalframes/2)+1)
        self.root.geometry(f"{RootW}x{RootH}") 
    
    def AddGraph(self):
        # Setting up the plot for the each Frame
        self.figs.append([])
        # Initialize figures
        self.figs[self.totalframes].append(plt.Figure(figsize=(7, 5), dpi=80))
        # Initialize the plot
        self.figs[self.totalframes].append(
            self.figs[self.totalframes][0].add_subplot(111))
        # Initialize the chart
        self.figs[self.totalframes].append(FigureCanvasTkAgg(
            self.figs[self.totalframes][0], master=self.frames[self.totalframes]))

        self.figs[self.totalframes][2].get_tk_widget().grid(
            column=1, row=0, columnspan=4, rowspan=17,  sticky=N)

    def AddBtnFrame(self):
        btnH = 2
        btnW = 4
        self.ControlFrames.append([])
        self.ControlFrames[self.totalframes].append(LabelFrame(self.frames[self.totalframes],
                                                               pady=5, bg="white"))
        self.ControlFrames[self.totalframes][0].grid(
            column=0, row=0, padx=5, pady=5,  sticky=N)

        self.ControlFrames[self.totalframes].append(Button(self.ControlFrames[self.totalframes][0], text="+",
                                                           bg="white", width=btnW, height=btnH))
        self.ControlFrames[self.totalframes][1].grid(
            column=0, row=0, padx=5, pady=5)
        self.ControlFrames[self.totalframes].append(Button(self.ControlFrames[self.totalframes][0], text="-",
                                                           bg="white", width=btnW, height=btnH))
        self.ControlFrames[self.totalframes][2].grid(
            column=1, row=0, padx=5, pady=5)
        
if __name__ == "main":
    RootGUI()
    ComGUI()
    ConnGUI()
    DisGUI()