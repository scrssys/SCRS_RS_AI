# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'samplecrop.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_samplecrop(object):
    def setupUi(self, Dialog_samplecrop):
        Dialog_samplecrop.setObjectName("Dialog_samplecrop")
        Dialog_samplecrop.resize(557, 225)
        self.widget = QtWidgets.QWidget(Dialog_samplecrop)
        self.widget.setGeometry(QtCore.QRect(42, 22, 471, 171))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_inputdir = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_inputdir.setObjectName("lineEdit_inputdir")
        self.horizontalLayout.addWidget(self.lineEdit_inputdir)
        self.select_inputdir = QtWidgets.QPushButton(self.widget)
        self.select_inputdir.setObjectName("select_inputdir")
        self.horizontalLayout.addWidget(self.select_inputdir)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.lineEdit_outputdir = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_outputdir.setObjectName("lineEdit_outputdir")
        self.horizontalLayout_4.addWidget(self.lineEdit_outputdir)
        self.select_outputdir = QtWidgets.QPushButton(self.widget)
        self.select_outputdir.setObjectName("select_outputdir")
        self.horizontalLayout_4.addWidget(self.select_outputdir)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(190, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_cropsize = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_cropsize.setMaximumSize(QtCore.QSize(8000, 16777215))
        self.lineEdit_cropsize.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit_cropsize.setMaxLength(6)
        self.lineEdit_cropsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_cropsize.setObjectName("lineEdit_cropsize")



        self.horizontalLayout_2.addWidget(self.lineEdit_cropsize)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.pushButton_process = QtWidgets.QPushButton(self.widget)
        self.pushButton_process.setObjectName("pushButton_process")
        self.horizontalLayout_3.addWidget(self.pushButton_process)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog_samplecrop)
        self.select_inputdir.clicked.connect(Dialog_samplecrop.slot_select_inputdir)
        self.pushButton_process.clicked.connect(Dialog_samplecrop.slot_ok)
        self.select_outputdir.clicked.connect(Dialog_samplecrop.slot_select_outputdir)
        QtCore.QMetaObject.connectSlotsByName(Dialog_samplecrop)

    def retranslateUi(self, Dialog_samplecrop):
        _translate = QtCore.QCoreApplication.translate
        Dialog_samplecrop.setWindowTitle(_translate("Dialog_samplecrop", "samplecrop"))
        self.label.setText(_translate("Dialog_samplecrop", "Sampledir"))
        self.select_inputdir.setText(_translate("Dialog_samplecrop", "open"))
        self.label_3.setText(_translate("Dialog_samplecrop", "Outputdir"))
        self.select_outputdir.setText(_translate("Dialog_samplecrop", "open"))
        self.label_2.setText(_translate("Dialog_samplecrop", "CropSize:"))
        self.lineEdit_cropsize.setText(_translate("Dialog_samplecrop", "2000"))
        self.pushButton_process.setText(_translate("Dialog_samplecrop", "process"))
