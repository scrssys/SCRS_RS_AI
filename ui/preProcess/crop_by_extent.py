# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'crop_by_extent.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_crop_by_extent(object):
    def setupUi(self, Dialog_crop_by_extent):
        Dialog_crop_by_extent.setObjectName("Dialog_crop_by_extent")
        Dialog_crop_by_extent.resize(500, 263)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_crop_by_extent)
        self.buttonBox.setGeometry(QtCore.QRect(100, 190, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QtWidgets.QWidget(Dialog_crop_by_extent)
        self.widget.setGeometry(QtCore.QRect(30, 20, 411, 151))
        self.widget.setObjectName("widget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        self.lineEdit_imgpath = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_imgpath.setObjectName("lineEdit_imgpath")
        self.horizontalLayout_6.addWidget(self.lineEdit_imgpath)
        self.pushButton_imagepath = QtWidgets.QPushButton(self.widget)
        self.pushButton_imagepath.setObjectName("pushButton_imagepath")
        self.horizontalLayout_6.addWidget(self.pushButton_imagepath)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_11 = QtWidgets.QLabel(self.widget)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_13.addWidget(self.label_11)
        self.lineEdit_shpfilepath = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_shpfilepath.setObjectName("lineEdit_shpfilepath")
        self.horizontalLayout_13.addWidget(self.lineEdit_shpfilepath)
        self.pushButton_shpfilepath = QtWidgets.QPushButton(self.widget)
        self.pushButton_shpfilepath.setObjectName("pushButton_shpfilepath")
        self.horizontalLayout_13.addWidget(self.pushButton_shpfilepath)
        self.verticalLayout_5.addLayout(self.horizontalLayout_13)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_7.addWidget(self.label_6)
        self.lineEdit_outputpath = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_outputpath.setObjectName("lineEdit_outputpath")
        self.horizontalLayout_7.addWidget(self.lineEdit_outputpath)
        self.pushButton_outputpath = QtWidgets.QPushButton(self.widget)
        self.pushButton_outputpath.setObjectName("pushButton_outputpath")
        self.horizontalLayout_7.addWidget(self.pushButton_outputpath)
        self.verticalLayout_5.addLayout(self.horizontalLayout_7)

        self.retranslateUi(Dialog_crop_by_extent)
        self.buttonBox.accepted.connect(Dialog_crop_by_extent.slot_ok)
        self.buttonBox.rejected.connect(Dialog_crop_by_extent.reject)
        self.pushButton_imagepath.clicked.connect(Dialog_crop_by_extent.slot_select_imgfile)
        self.pushButton_shpfilepath.clicked.connect(Dialog_crop_by_extent.slot_select_shpfile)
        self.pushButton_outputpath.clicked.connect(Dialog_crop_by_extent.slot_select_outputpath)
        QtCore.QMetaObject.connectSlotsByName(Dialog_crop_by_extent)

    def retranslateUi(self, Dialog_crop_by_extent):
        _translate = QtCore.QCoreApplication.translate
        Dialog_crop_by_extent.setWindowTitle(_translate("Dialog_crop_by_extent", "Dialog"))
        self.label_5.setText(_translate("Dialog_crop_by_extent", "imageFile"))
        self.pushButton_imagepath.setText(_translate("Dialog_crop_by_extent", "open"))
        self.label_11.setText(_translate("Dialog_crop_by_extent", "shpFile"))
        self.pushButton_shpfilepath.setText(_translate("Dialog_crop_by_extent", "open"))
        self.label_6.setText(_translate("Dialog_crop_by_extent", "outputFile"))
        self.pushButton_outputpath.setText(_translate("Dialog_crop_by_extent", "open"))
