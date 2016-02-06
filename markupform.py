# pyuic4 -x markupform.ui -o ui_markupform.py

import sys
from PyQt4 import QtGui
from ui_markupform import Ui_MarkupForm
import make_poems_model as mpm


class Window(QtGui.QWidget, Ui_MarkupForm):

    def __init__(self):
        self.pmodel = {}
        self.curr_idx = 0

        super(Window, self).__init__()
        Ui_MarkupForm.__init__(self)
        self.setupUi(self)
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("Markup")

        self.modelFileNameLabel.setText("...")
        self.poemLabel.setText("...")
        self.nextPoemBtn.setEnabled(False)
        self.prevPoemBtn.setEnabled(False)
        self.poemNumSpin.setEnabled(False)
        self.rateSlider.setEnabled(False)
        self.saveModelBtn.setEnabled(False)

        self.loadModelBtn.clicked.connect(self.loadModel)
        self.saveModelBtn.clicked.connect(self.saveModel)
        self.poemNumSpin.valueChanged[str].connect(self.poemSpinValueChanged)
        self.nextPoemBtn.clicked.connect(self.nextPoem)
        self.prevPoemBtn.clicked.connect(self.prevPoem)
        self.rateSlider.valueChanged[int].connect(self.rateSliderChanged)

    def poemCount(self):
        return len(self.pmodel['poems'])

    def poemByIdx(self, idx):
        return self.pmodel['poems'][idx]

    def rateByIdx(self, idx):
        return self.pmodel['rates'][idx]

    def setPoemByIdx(self, idx):
        self.poemLabel.setText(self.poemByIdx(idx))

    def loadModel(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open Model', '')
        self.modelFileNameLabel.setText(fname)
        self.pmodel = mpm.read_data_model(fname)
        if not ('rates' in self.pmodel.keys()):
            self.pmodel['rates'] = [0.0 for _ in range(self.poemCount())]
        self.curr_idx = 0
        self.poemNumSpin.setMinimum(1)
        self.poemNumSpin.setMaximum(self.poemCount())
        self.poemNumSpin.setValue(1)

        self.nextPoemBtn.setEnabled(True)
        self.prevPoemBtn.setEnabled(True)
        self.poemNumSpin.setEnabled(True)
        self.rateSlider.setEnabled(True)
        self.saveModelBtn.setEnabled(True)


    def saveModel(self):
        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save Model', '')
        mpm.write_data_model(fname, self.pmodel)
        self.modelFileNameLabel.setText(fname)
        return

    def poemSpinValueChanged(self, val):
        self.pmodel['rates'][self.curr_idx] = self.rateSlider.value() / self.rateSlider.maximum()
        self.curr_idx = self.poemNumSpin.value() - 1
        self.setPoemByIdx(self.curr_idx)
        self.rateSlider.setValue(self.rateByIdx(self.curr_idx) * self.rateSlider.maximum())

    def nextPoem(self):
        self.poemNumSpin.stepUp()

    def prevPoem(self):
        self.poemNumSpin.stepDown()

    def rateSliderChanged(self, val):
        self.rateLabel.setText(str(val) + '%')


def main():
    app = QtGui.QApplication(sys.argv)
    gui = Window()
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

