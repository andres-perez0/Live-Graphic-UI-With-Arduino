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
            Attempts to open the serial port using settings from the GUI. If not already open, initializes and opens the port. Sets status accordingly.
        '''
        try: 
            PORT=ComGUI.click_com.get()
            BAUD=ComGUI.click_baud.get()
            self.ser=serial.Serial()
            self.ser.port=PORT  
            self.ser.baudrate=BAUD
            self.ser.timeout=0.1
            self.ser.open()                 
            self.ser.status=True
        except:
            self.ser.status=False

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
        try:
            if self.ser.is_open:
                self.ser.close()
            self.ser.status=False
        except:
            self.ser.status=False

    def SerialSync(self, gui):
        self.threading = True
        cnt = 0
        while self.threading:
            try:
                self.ser.write(gui.data.sync.encode())
                gui.conn.sync_status["text"] = "..Sync.."
                gui.conn.sync_status["fg"] = "orange"
                gui.data.RowMsg = self.ser.readline()
                # print(f"RowMsg: {gui.data.RowMsg}")
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

if __name__=="__main__":
    SerialCtrl()