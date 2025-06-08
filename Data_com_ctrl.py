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
        temp = self.RowMsg.decode('utf-8', errors='ignore')
        if len(temp) > 0:
            if "#" in temp:
                # checks if valid seperator is present in the RowMsg
                self.msg = temp.split("#")
                # As the initial list will look similar to "#CH1#CH2#" -> ['', 'CH1', 'CH2', '']; 
                # deleting the first index would make it more workable ['CH1', 'CH2', '']  
                del self.msg[0]

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

if __name__=="__main__":
    DataMaster()
