# pyuic4 markupform.ui >> ui_markupform.py

import sys
from PyQt4 import QtGui
from ui_markupform import Ui_MarkupForm


class Window(QtGui.QWidget, Ui_MarkupForm):

    def __init__(self):
        super(Window, self).__init__()
        Ui_MarkupForm.__init__(self)
        self.setupUi(self)
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("Markup")


def main():
    app = QtGui.QApplication(sys.argv)
    gui = Window()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

