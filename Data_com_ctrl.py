import time
import numpy as np

class DataMaster():
    def __init__(self):
        self.sync="#?#\n"           # synchronization request; '\n' often acts as a message to terminate serial communication
        self.sync_ok="!"            # The expected response from the ARduino to acknowledge that it has received the sync request
        self.StartStream = "#A#\n"  # The start(A) and stop(S) request to tell the Arduino
        self.StopStream = "#S#\n"
        self.SynchChannel = 0
        
        self.msg = []

        self.XData = []
        self.YData = []

        self.FunctionMaster = {
            "RowData": self.RowData,
            "VoltageDisplay": self.VoltData
        }

        self.DisplayTimeRange = 5

        self.ChannelNum = {
            'Ch0': 0,
            'Ch1': 1,
            'Ch2': 2,
            'Ch3': 3,
            'Ch4': 4,
            'Ch5': 5,
            'Ch6': 6,
            'Ch7': 7
        }
        self.ChannelColor = {
            'Ch0': 'blue',
            'Ch1': 'green',
            'Ch2': 'red',
            'Ch3': 'cyan',
            'Ch4': 'magenta',
            'Ch5': 'yellow',
            'Ch6': 'black',
            'Ch7': 'white'
        }

    def DecodeMsg(self):
        temp = self.RowMsg.decode('utf-8', errors='ignore')
        if len(temp) > 0:
            if "#" in temp:
                # checks if valid seperator is present in the RowMsg
                self.msg = temp.split("#")
                # As the initial list will look similar to "#CH1#CH2#" -> ['', 'CH1', 'CH2', '']; 
                # deleting the first index would make it more workable ['CH1', 'CH2', '']  
                del self.msg[0]
                if self.msg[0] in "D":
                    self.messageLen = 0
                    self.messageLenCheck = 0
                    del self.msg[0]
                    del self.msg[len(self.msg)-1]
                    self.messageLen = int(self.msg[len(self.msg)-1])
                    del self.msg[len(self.msg)-1]
                    for item in self.msg:
                        self.messageLenCheck += len(item)

    def GenChannels(self):
        ''' Creates a list of channels based on the number of SynchChannel
        ["Ch0","Ch1","Ch2"] up too SynchChannel-1 '''
        self.Channels=[f"Ch{ch}" for ch in range(self.SynchChannel)]

    def BuildYData(self):
        ''' Creates an YData list also based on the number of SynchChannel  '''
        self.YData = [[] for idy in range(self.SynchChannel)]

    def ClearData(self):
        self.RowMsg = ""
        self.msg = []
        self.YData = []
        self.XData = []
    
    def IntMsgFunc(self):
        self.IntMsg=[int(msg) for msg in self.msg]

    def StreamDataCheck(self):
        self.StreamData=False
        if self.SynchChannel == len(self.msg):
            if self.messageLen==self.messageLenCheck:
                self.StreamData=True
                self.IntMsgFunc()

    def SetRefTime(self):
        if len(self.XData) == 0:
            self.RefTime=time.perf_counter()
        else: 
            self.RefTime=time.perf_counter() - self.XData[len(self.XData)-1]

    def UpdataXdata(self):
        if len(self.XData) == 0:
            self.XData.append(0)
        else:
            self.XData.append(time.perf_counter()-self.RefTime)

    def UpdataYdata(self):
        for ChNumber in range(self.SynchChannel):
            self.YData[ChNumber].append(self.IntMsg[ChNumber])

    def AdjustData(self):
        lenXdata = len(self.XData)
        if (self.XData[lenXdata-1] - self.XData[0]) > self.DisplayTimeRange:
            del self.XData[0]
            for ydata in self.YData:
                del ydata[0]

        x = np.array(self.XData)
        self.XDisplay = np.linspace(x.min(), x.max(), len(x), endpoint=0)
        self.YDisplay = np.array(self.YData)

    def RowData(self, gui):
        gui.chart.plot(gui.x, gui.y, color=gui.color, dash_capstyle='projecting', linewidth=1)

    def VoltData(self, gui):
        gui.chart.plot(gui.x, (gui.y/4096)*3.3, color=gui.color, dash_capstyle='projecting', linewidth=1)
        
# if __name__=="__main__":
#     DataMaster()
