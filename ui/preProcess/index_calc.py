# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'index_calc.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_index_calc(object):
    def setupUi(self, Dialog_index_calc):
        Dialog_index_calc.setObjectName("Dialog_index_calc")
        Dialog_index_calc.resize(498, 240)
        self.layoutWidget = QtWidgets.QWidget(Dialog_index_calc)
        self.layoutWidget.setGeometry(QtCore.QRect(9, 20, 461, 151))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_imagpath = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_imagpath.setObjectName("lineEdit_imagpath")
        self.horizontalLayout.addWidget(self.lineEdit_imagpath)
        self.pushButton_imagepath = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_imagepath.setObjectName("pushButton_imagepath")
        self.horizontalLayout.addWidget(self.pushButton_imagepath)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_outputpath = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_outputpath.setObjectName("lineEdit_outputpath")
        self.horizontalLayout_2.addWidget(self.lineEdit_outputpath)
        self.pushButton_outputpath = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_outputpath.setObjectName("pushButton_outputpath")
        self.horizontalLayout_2.addWidget(self.pushButton_outputpath)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.comboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox.setMinimumSize(QtCore.QSize(0, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout_3.addWidget(self.comboBox)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_3)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.spinBox = QtWidgets.QSpinBox(self.layoutWidget)
        self.spinBox.setMinimumSize(QtCore.QSize(0, 22))
        self.spinBox.setMaximum(1000000000)
        self.spinBox.setProperty("value", 65535)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_5.addWidget(self.spinBox)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        self.spinBox_2 = QtWidgets.QSpinBox(self.layoutWidget)
        self.spinBox_2.setMinimumSize(QtCore.QSize(0, 22))
        self.spinBox_2.setMinimum(1000)
        self.spinBox_2.setMaximum(1000000)
        self.spinBox_2.setSingleStep(100)
        self.spinBox_2.setProperty("value", 20000)
        self.spinBox_2.setObjectName("spinBox_2")
        self.horizontalLayout_6.addWidget(self.spinBox_2)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_index_calc)
        self.buttonBox.setGeometry(QtCore.QRect(310, 190, 156, 31))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(Dialog_index_calc)
        self.pushButton_imagepath.clicked.connect(Dialog_index_calc.slot_select_inputpath)
        self.pushButton_outputpath.clicked.connect(Dialog_index_calc.slot_select_outputpath)
        self.buttonBox.accepted.connect(Dialog_index_calc.slot_ok)
        self.buttonBox.rejected.connect(Dialog_index_calc.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_index_calc)

    def retranslateUi(self, Dialog_index_calc):
        _translate = QtCore.QCoreApplication.translate
        Dialog_index_calc.setWindowTitle(_translate("Dialog_index_calc", "Dialog_index"))
        self.label.setText(_translate("Dialog_index_calc", "imagepath"))
        self.pushButton_imagepath.setText(_translate("Dialog_index_calc", "open"))
        self.label_2.setText(_translate("Dialog_index_calc", "outputpath"))
        self.pushButton_outputpath.setText(_translate("Dialog_index_calc", "open"))
        self.label_3.setText(_translate("Dialog_index_calc", "Index"))
        self.comboBox.setCurrentText(_translate("Dialog_index_calc", "NDVI"))
        self.comboBox.setItemText(0, _translate("Dialog_index_calc", "NDVI"))
        self.comboBox.setItemText(1, _translate("Dialog_index_calc", "NDWI"))
        self.comboBox.setItemText(2, _translate("Dialog_index_calc", "NDBI"))
        self.label_4.setText(_translate("Dialog_index_calc", "Nodata"))
        self.label_5.setText(_translate("Dialog_index_calc", "block"))

