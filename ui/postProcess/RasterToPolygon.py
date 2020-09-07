# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RasterToPolygon.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_raster_to_polygon(object):
    def setupUi(self, Dialog_raster_to_polygon):
        Dialog_raster_to_polygon.setObjectName("Dialog_raster_to_polygon")
        Dialog_raster_to_polygon.resize(400, 207)
        self.pushButton_ok = QtWidgets.QPushButton(Dialog_raster_to_polygon)
        self.pushButton_ok.setGeometry(QtCore.QRect(200, 160, 85, 27))
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.pushButton_cancel = QtWidgets.QPushButton(Dialog_raster_to_polygon)
        self.pushButton_cancel.setGeometry(QtCore.QRect(290, 160, 85, 27))
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.widget = QtWidgets.QWidget(Dialog_raster_to_polygon)
        self.widget.setGeometry(QtCore.QRect(10, 20, 371, 121))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_input = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_input.setObjectName("lineEdit_input")
        self.horizontalLayout.addWidget(self.lineEdit_input)
        self.pushButton_input = QtWidgets.QPushButton(self.widget)
        self.pushButton_input.setObjectName("pushButton_input")
        self.horizontalLayout.addWidget(self.pushButton_input)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_output = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_output.setObjectName("lineEdit_output")
        self.horizontalLayout_2.addWidget(self.lineEdit_output)
        self.pushButton_output = QtWidgets.QPushButton(self.widget)
        self.pushButton_output.setObjectName("pushButton_output")
        self.horizontalLayout_2.addWidget(self.pushButton_output)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog_raster_to_polygon)
        self.pushButton_input.clicked.connect(Dialog_raster_to_polygon.slot_open_inputdir)
        self.pushButton_output.clicked.connect(Dialog_raster_to_polygon.slot_open_outputdir)
        self.pushButton_ok.clicked.connect(Dialog_raster_to_polygon.slot_ok)
        self.pushButton_cancel.clicked.connect(Dialog_raster_to_polygon.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_raster_to_polygon)

    def retranslateUi(self, Dialog_raster_to_polygon):
        _translate = QtCore.QCoreApplication.translate
        Dialog_raster_to_polygon.setWindowTitle(_translate("Dialog_raster_to_polygon", "Raster to Polygon"))
        self.pushButton_ok.setText(_translate("Dialog_raster_to_polygon", "OK"))
        self.pushButton_cancel.setText(_translate("Dialog_raster_to_polygon", "Cancel"))
        self.label.setText(_translate("Dialog_raster_to_polygon", "input dir"))
        self.pushButton_input.setText(_translate("Dialog_raster_to_polygon", "open"))
        self.label_2.setText(_translate("Dialog_raster_to_polygon", "output dir"))
        self.pushButton_output.setText(_translate("Dialog_raster_to_polygon", "open"))

