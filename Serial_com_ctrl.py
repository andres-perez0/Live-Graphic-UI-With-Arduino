import serial.tools.list_ports
import time

class SerialCtrl():
    def __init__(self):
        self.sync_cnt=200

    def getCOMList(self):
        ports=serial.tools.list_ports.comports()    # Returns a list with port name, description, and hardware ID.
        self.com_list = [com[0] for com in ports]   # Iterates through ports, with com, and adds the first item in the list , com[0], to com_list 
        self.com_list.insert(0, "-")

    def SerialOpen(self, ComGUI):
        '''
        Tries to access self.ser.is_open, if it fails it initialzes the variable with the 
        GUI information
        '''
        try:
            self.ser.is_open
        except:
            PORT=ComGUI.click_com.get()
            BAUD=ComGUI.click_baud.get()
            self.ser=serial.Serial()
            self.ser.port=PORT  
            self.ser.baudrate=BAUD
            self.ser.timeout=0.1
            self.ser.open()                # Attempts to open the serial point           
            self.ser.status=True

        try:
            # Check if serial object exists and is open
            if self.ser.is_open:
                print("Already Open")
                self.ser.status=True
            else:
                # Re-initialize and open the serial port
                PORT=ComGUI.click_com.get()
                BAUD=ComGUI.click_baud.get()
                self.ser=serial.Serial()
                self.ser.port=PORT  
                self.ser.baudrate=BAUD
                self.ser.timeout=0.1
                self.ser.open()                 
                self.ser.status=True 
        except:
            # Opening failed
            self.ser.status=False

    def SerialClose(self, ComGUI):
        '''
            if the custom attribute(is_open) is true, then closs the serial port
        '''
        try:
            if self.ser.is_open:
                self.ser.close()
            self.ser.status=False
        except:
            self.ser.status=False

    def SerialStop(self, gui):
        self.ser.write(gui.data.StopStream.encode())

    def SerialSync(self, gui):
        self.threading = True
        time.sleep(0.2)
        cnt = 0
        while self.threading:
            try:
                self.ser.write(gui.data.sync.encode())
                gui.conn.sync_status["text"] = "..Sync.."
                gui.conn.sync_status["fg"] = "orange"
                gui.data.RowMsg = self.ser.readline()
                gui.data.DecodeMsg()
                if gui.data.sync_ok in gui.data.msg[0]:
                    if int(gui.data.msg[1]) > 0:
                        gui.conn.btn_start_stream["state"] = "active"
                        gui.conn.btn_add_chart["state"] = "active"
                        gui.conn.btn_kill_chart["state"] = "active"
                        gui.conn.save_check["state"] = "active"
                        gui.conn.sync_status["text"] = "OK"
                        gui.conn.sync_status["fg"] = "green"
                        gui.conn.ch_status["text"] = gui.data.msg[1]
                        gui.conn.ch_status["fg"] = "green"
                        gui.data.SynchChannel = int(gui.data.msg[1])
                        gui.data.GenChannels()
                        gui.data.BuildYData()
                        print(gui.data.Channels, gui.data.YData)
                        self.threading = False
                        break
                if self.threading == False:
                    break
            except Exception as e:
                print(e)
            cnt += 1
            if self.threading == False:
                break
            if cnt > self.sync_cnt:
                cnt = 0
                gui.conn.sync_status["text"] = "failed"
                gui.conn.sync_status["fg"] = "red"
                time.sleep(0.5)

                if self.threading == False:
                    break   

    def SerialDataStream(self, gui):
        self.threading = True
        cnt = 0
        while self.threading:
            try:
                self.ser.write(gui.data.StartStream.encode())
                gui.data.RowMsg = self.ser.readline()
                gui.data.DecodeMsg()
                gui.data.StreamDataCheck()
                if gui.data.StreamData:
                    gui.data.SetRefTime()
                    break
            except Exception as e:
                print(e)
            
        gui.UpdateChart()
        while self.threading:
            try:
                gui.data.RowMsg = self.ser.readline()
                gui.data.DecodeMsg()
                gui.data.StreamDataCheck()
                if gui.data.StreamData:
                    gui.data.UpdataXdata()
                    gui.data.UpdataYdata()
                    # Ysam = [Ys[len(gui.data.XData)-1] for Ys in gui.data.YData]
                    gui.data.AdjustData()
                    # print(
                    #     f"X Len: {len(gui.data.XData)}, Xstart:{gui.data.XData[0]}  Xend : {gui.data.XData[len(gui.data.XData)-1]}, Xrange: {gui.data.XData[len(gui.data.XData)-1] - gui.data.XData[0]} Ydata len: {len(gui.data.YData[0])} Yval: : {Ysam} ")
            except Exception as e:
                print(e)

# Should I add this?
# if __name__ == "__main__":
#     SerialCtrl()