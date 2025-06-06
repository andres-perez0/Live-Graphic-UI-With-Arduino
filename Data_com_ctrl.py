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

    def DecodeMsg(self):
        '''
            Method used to get the message coming from UART and converted to a python string
            it is also used to get defferent type of messages based on the Message protocol
            '''
        temp = self.RowMsg.decode('utf-8', errors='ignore')
        if len(temp) > 0:
            if "#" in temp:
                self.msg = temp.split("#")
                # print(self.msg)
                del self.msg[0]

    def GenChannels(self):
        self.Channels=[f"Ch{ch}" for ch in range(self.SynchChannel)]

    def BuildYData(self):
        for _ in range(self.SynchChannel):
            self.YData.append([])

    def ClearData(self):
        self.RowMsg = ""
        self.msg = []
        self.YData = []

if __name__=="__main__":
    DataMaster()
