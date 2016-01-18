# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'markupform.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MarkupForm(object):
    def setupUi(self, MarkupForm):
        MarkupForm.setObjectName(_fromUtf8("MarkupForm"))
        MarkupForm.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(MarkupForm)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.modelFileNameLabel = QtGui.QLabel(MarkupForm)
        self.modelFileNameLabel.setMinimumSize(QtCore.QSize(0, 20))
        self.modelFileNameLabel.setFrameShape(QtGui.QFrame.Box)
        self.modelFileNameLabel.setFrameShadow(QtGui.QFrame.Plain)
        self.modelFileNameLabel.setObjectName(_fromUtf8("modelFileNameLabel"))
        self.verticalLayout.addWidget(self.modelFileNameLabel)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.loadModelBtn = QtGui.QPushButton(MarkupForm)
        self.loadModelBtn.setObjectName(_fromUtf8("loadModelBtn"))
        self.horizontalLayout.addWidget(self.loadModelBtn)
        self.saveModelBtn = QtGui.QPushButton(MarkupForm)
        self.saveModelBtn.setObjectName(_fromUtf8("saveModelBtn"))
        self.horizontalLayout.addWidget(self.saveModelBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.widget = QtGui.QWidget(MarkupForm)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.poemLabel = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.poemLabel.setFont(font)
        self.poemLabel.setFrameShape(QtGui.QFrame.Box)
        self.poemLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.poemLabel.setObjectName(_fromUtf8("poemLabel"))
        self.horizontalLayout_3.addWidget(self.poemLabel)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(3, -1, 3, 3)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.rateLabel = QtGui.QLabel(self.widget)
        self.rateLabel.setMinimumSize(QtCore.QSize(30, 0))
        self.rateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.rateLabel.setObjectName(_fromUtf8("rateLabel"))
        self.verticalLayout_2.addWidget(self.rateLabel)
        self.rateSlider = QtGui.QSlider(self.widget)
        self.rateSlider.setSizeIncrement(QtCore.QSize(0, 0))
        self.rateSlider.setMaximum(100)
        self.rateSlider.setOrientation(QtCore.Qt.Vertical)
        self.rateSlider.setInvertedAppearance(False)
        self.rateSlider.setTickPosition(QtGui.QSlider.TicksAbove)
        self.rateSlider.setObjectName(_fromUtf8("rateSlider"))
        self.verticalLayout_2.addWidget(self.rateSlider)
        self.verticalLayout_2.setStretch(1, 1)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.horizontalLayout_3.setStretch(0, 1)
        self.verticalLayout.addWidget(self.widget)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.prevPoemBtn = QtGui.QPushButton(MarkupForm)
        self.prevPoemBtn.setObjectName(_fromUtf8("prevPoemBtn"))
        self.horizontalLayout_2.addWidget(self.prevPoemBtn)
        self.poemNumSpin = QtGui.QSpinBox(MarkupForm)
        self.poemNumSpin.setAlignment(QtCore.Qt.AlignCenter)
        self.poemNumSpin.setObjectName(_fromUtf8("poemNumSpin"))
        self.horizontalLayout_2.addWidget(self.poemNumSpin)
        self.nextPoemBtn = QtGui.QPushButton(MarkupForm)
        self.nextPoemBtn.setObjectName(_fromUtf8("nextPoemBtn"))
        self.horizontalLayout_2.addWidget(self.nextPoemBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.setStretch(2, 1)

        self.retranslateUi(MarkupForm)
        QtCore.QMetaObject.connectSlotsByName(MarkupForm)

    def retranslateUi(self, MarkupForm):
        MarkupForm.setWindowTitle(_translate("MarkupForm", "Markup Form", None))
        self.modelFileNameLabel.setText(_translate("MarkupForm", "TextLabel", None))
        self.loadModelBtn.setText(_translate("MarkupForm", "Load Model", None))
        self.saveModelBtn.setText(_translate("MarkupForm", "Save Model", None))
        self.poemLabel.setText(_translate("MarkupForm", "TextLabel", None))
        self.rateLabel.setText(_translate("MarkupForm", "100%", None))
        self.prevPoemBtn.setText(_translate("MarkupForm", "<<", None))
        self.nextPoemBtn.setText(_translate("MarkupForm", ">>", None))

