# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dialog_predict.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_predict(object):
    def setupUi(self, Dialog_predict):
        Dialog_predict.setObjectName("Dialog_predict")
        Dialog_predict.resize(492, 352)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_predict)
        self.buttonBox.setGeometry(QtCore.QRect(110, 280, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog_predict)
        self.label.setGeometry(QtCore.QRect(30, 20, 49, 12))
        self.label.setObjectName("label")
        self.lineEdit_input = QtWidgets.QLineEdit(Dialog_predict)
        self.lineEdit_input.setGeometry(QtCore.QRect(110, 10, 221, 21))
        self.lineEdit_input.setObjectName("lineEdit_input")
        self.BT_input = QtWidgets.QPushButton(Dialog_predict)
        self.BT_input.setGeometry(QtCore.QRect(360, 10, 85, 27))
        self.BT_input.setObjectName("BT_input")
        self.BT_output = QtWidgets.QPushButton(Dialog_predict)
        self.BT_output.setGeometry(QtCore.QRect(360, 80, 85, 27))
        self.BT_output.setObjectName("BT_output")
        self.label_2 = QtWidgets.QLabel(Dialog_predict)
        self.label_2.setGeometry(QtCore.QRect(30, 90, 49, 12))
        self.label_2.setObjectName("label_2")
        self.lineEdit_output = QtWidgets.QLineEdit(Dialog_predict)
        self.lineEdit_output.setGeometry(QtCore.QRect(110, 80, 221, 21))
        self.lineEdit_output.setObjectName("lineEdit_output")
        self.BT_config = QtWidgets.QPushButton(Dialog_predict)
        self.BT_config.setGeometry(QtCore.QRect(360, 160, 85, 27))
        self.BT_config.setObjectName("BT_config")
        self.label_3 = QtWidgets.QLabel(Dialog_predict)
        self.label_3.setGeometry(QtCore.QRect(30, 170, 49, 12))
        self.label_3.setObjectName("label_3")
        self.lineEdit_config = QtWidgets.QLineEdit(Dialog_predict)
        self.lineEdit_config.setGeometry(QtCore.QRect(110, 160, 221, 21))
        self.lineEdit_config.setObjectName("lineEdit_config")
        self.comboBox_gpu = QtWidgets.QComboBox(Dialog_predict)
        self.comboBox_gpu.setGeometry(QtCore.QRect(210, 230, 41, 24))
        self.comboBox_gpu.setObjectName("comboBox_gpu")
        self.comboBox_gpu.addItem("")
        self.comboBox_gpu.addItem("")
        self.comboBox_gpu.addItem("")
        self.comboBox_gpu.addItem("")
        self.comboBox_gpu.addItem("")
        self.comboBox_gpu.addItem("")
        self.comboBox_gpu.addItem("")
        self.comboBox_gpu.addItem("")
        self.label_4 = QtWidgets.QLabel(Dialog_predict)
        self.label_4.setGeometry(QtCore.QRect(160, 240, 49, 12))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog_predict)
        self.buttonBox.rejected.connect(Dialog_predict.reject)
        self.BT_input.clicked.connect(Dialog_predict.slot_input)
        self.BT_output.clicked.connect(Dialog_predict.slot_output)
        self.BT_config.clicked.connect(Dialog_predict.slot_config)
        self.buttonBox.accepted.connect(Dialog_predict.slot_done)
        QtCore.QMetaObject.connectSlotsByName(Dialog_predict)

    def retranslateUi(self, Dialog_predict):
        _translate = QtCore.QCoreApplication.translate
        Dialog_predict.setWindowTitle(_translate("Dialog_predict", "Dialog"))
        self.label.setText(_translate("Dialog_predict", "input"))
        self.BT_input.setText(_translate("Dialog_predict", "Open"))
        self.BT_output.setText(_translate("Dialog_predict", "Open"))
        self.label_2.setText(_translate("Dialog_predict", "output"))
        self.BT_config.setText(_translate("Dialog_predict", "Open"))
        self.label_3.setText(_translate("Dialog_predict", "config"))
        self.comboBox_gpu.setItemText(0, _translate("Dialog_predict", "0"))
        self.comboBox_gpu.setItemText(1, _translate("Dialog_predict", "1"))
        self.comboBox_gpu.setItemText(2, _translate("Dialog_predict", "2"))
        self.comboBox_gpu.setItemText(3, _translate("Dialog_predict", "3"))
        self.comboBox_gpu.setItemText(4, _translate("Dialog_predict", "4"))
        self.comboBox_gpu.setItemText(5, _translate("Dialog_predict", "5"))
        self.comboBox_gpu.setItemText(6, _translate("Dialog_predict", "6"))
        self.comboBox_gpu.setItemText(7, _translate("Dialog_predict", "7"))
        self.label_4.setText(_translate("Dialog_predict", "GPU"))

