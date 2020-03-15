import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import upbit_Auto 


# =============================================================================
# form_class = uic.loadUiType("pytrader.ui")[0]
# 
# class MyWindow(QMainWindow, form_class):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)
# 
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     myWindow = MyWindow()
#     myWindow.show()
#     app.exec_()
# 
# 
# =============================================================================

for i in range(1):

    upbit_Auto.Upbit()
    #upbit_Auto.Buying.buy_run()
    #upbit_Auto.selling.sell_run()
    
    #upbit_Auto.Upbit.account_clear()
    #%%