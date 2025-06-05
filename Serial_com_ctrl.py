import serial.tools.list_ports

class SerialCtrl():
    def __init__(self):
        self.com_list=[]

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

if __name__=="__main__":
    SerialCtrl()