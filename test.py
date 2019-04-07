from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import MainWindow

app = QApplication(sys.argv)
main1 = QMainWindow()
ui = MainWindow.Ui_MainWindow()
ui.setupUi(main1)
main1.show()
sys.exit(app.exec_())