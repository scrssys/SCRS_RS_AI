# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'band_combine.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_band_combine(object):
    def setupUi(self, Dialog_band_combine):
        Dialog_band_combine.setObjectName("Dialog_band_combine")
        Dialog_band_combine.resize(502, 263)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_band_combine)
        self.buttonBox.setGeometry(QtCore.QRect(321, 200, 156, 31))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.layoutWidget = QtWidgets.QWidget(Dialog_band_combine)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 30, 461, 151))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
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
        self.horizontalLayout_5.addLayout(self.horizontalLayout_3)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.spinBox = QtWidgets.QSpinBox(self.layoutWidget)
        self.spinBox.setMinimumSize(QtCore.QSize(0, 22))
        self.spinBox.setMaximum(1000000000)
        self.spinBox.setProperty("value", 65535)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_4.addWidget(self.spinBox)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.retranslateUi(Dialog_band_combine)
        self.buttonBox.accepted.connect(Dialog_band_combine.slot_ok)
        self.buttonBox.rejected.connect(Dialog_band_combine.reject)
        self.pushButton_imagepath.clicked.connect(Dialog_band_combine.slot_select_inputpath)
        self.pushButton_outputpath.clicked.connect(Dialog_band_combine.slot_select_outputpath)
        QtCore.QMetaObject.connectSlotsByName(Dialog_band_combine)

    def retranslateUi(self, Dialog_band_combine):
        _translate = QtCore.QCoreApplication.translate
        Dialog_band_combine.setWindowTitle(_translate("Dialog_band_combine", "Dialog"))
        self.label.setText(_translate("Dialog_band_combine", "inputpath"))
        self.pushButton_imagepath.setText(_translate("Dialog_band_combine", "open"))
        self.label_2.setText(_translate("Dialog_band_combine", "outputpath"))
        self.pushButton_outputpath.setText(_translate("Dialog_band_combine", "open"))
        self.label_4.setText(_translate("Dialog_band_combine", "Nodata"))
