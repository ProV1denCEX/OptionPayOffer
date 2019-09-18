
from PyQt5.QtWidgets import QApplication
from sys import argv as sys_argv, exit as sys_exit
from gui.main import ApplicationWindow
from qtmodern.styles import dark as qtdark
from qtmodern.windows import ModernWindow

if __name__ == '__main__':
    app = QApplication(sys_argv)
    main = ApplicationWindow()
    qtdark(app)
    window_main = ModernWindow(main)
    window_main.show()
    sys_exit(app.exec_())