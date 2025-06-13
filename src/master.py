from GUI_Master import RootGUI, ComGUI
from Serial_com_ctrl import SerialCtrl
from Data_com_ctrl import DataMaster

# Initiate the root class that will manage the other class
MySerial = SerialCtrl()
MyData = DataMaster()
RootMaster = RootGUI(MySerial, MyData)
# Overall Master Class
ComMaster = ComGUI(RootMaster.root, MySerial, MyData)

RootMaster.root.mainloop()