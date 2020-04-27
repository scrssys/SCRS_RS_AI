# import subprocess
import os
from ui.train.Dialog_train import Ui_Dialog_train
from ui.train.Dialog_train_h5 import Ui_Dialog_train_h5
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox
from train_fire import train, train_h5
from ulitities.base_functions import base_message
from PyQt5 import QtCore
# QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

class child_train(QDialog,Ui_Dialog_train,base_message):
    def __init__(self):
        super(child_train,self).__init__()
        self.setWindowTitle("train")
        self.setupUi(self)
    def slot_open_sample(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_sample.setText(dir_tmp)
    def slot_open_config(self):
        str, _ = QFileDialog.getOpenFileName(self, "Select config file", '../../data/', self.tr("Json(*.json)"))
        self.lineEdit_config.setText(str)
    def slot_open_modelpath(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_modelpath.setText(dir_tmp)

    def slot_process(self):
        sample = self.lineEdit_sample.text()
        config = self.lineEdit_config.text()
        model = self.lineEdit_modelpath.text()
        gpu_id = self.comboBox_gpuid.currentText()
        # gpu_id = self.comboBox_gpuid.currentIndex()

        QMessageBox.information(self, '提示',
        "sample:{}\n config :{}\n model :{}".format(sample,config,model)
        ,QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)

        # excute program
        os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)
        # cmd =['python','../train_yp.py','--gpu',gpu_id, '--sample', sample,"--model",model, '--config',  config]
        train(self.send, config, gpu_id, sample, model)
        try:
            # train(self.send,config,gpu_id,sample,model)
            pass
            # subprocess.call(cmd)
        except:
            QMessageBox.information(self, '错误', "Error occurred")
        QMessageBox.information(self, '提示', "Finished")
        # QMessageBox.information(self, '提示', gpu_id, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        # dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        # self.lineEdit_sample.setText(dir_tmp)
        # QDir.setCurrent(dir_tmp)


class child_train_h5(QDialog,Ui_Dialog_train_h5,base_message):
    def __init__(self):
        super(child_train_h5,self).__init__()
        self.setWindowTitle("train")
        self.setupUi(self)
    def slot_open_sample(self):
        str, _ = QFileDialog.getOpenFileName(self, "Select h5 file", '../../data/', self.tr("H5(*.h5)"))
        self.lineEdit_sample.setText(str)

    def slot_open_config(self):
        str, _ = QFileDialog.getOpenFileName(self, "Select config file", '../../data/', self.tr("Json(*.json)"))
        self.lineEdit_config.setText(str)
    def slot_open_modelpath(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_modelpath.setText(dir_tmp)

    def slot_process(self):
        sample = self.lineEdit_sample.text()
        config = self.lineEdit_config.text()
        model = self.lineEdit_modelpath.text()
        gpu_id = self.comboBox_gpuid.currentText()
        # gpu_id = self.comboBox_gpuid.currentIndex()

        QMessageBox.information(self, '提示',
        "sample:{}\n config :{}\n model :{}".format(sample,config,model)
        ,QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)

        # excute program
        os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)
        # cmd =['python','../train_yp.py','--gpu',gpu_id, '--sample', sample,"--model",model, '--config',  config]
        train_h5(self.send, config, gpu_id, sample, model)
        try:
            # train(self.send,config,gpu_id,sample,model)
            pass
            # subprocess.call(cmd)
        except:
            QMessageBox.information(self, '错误', "Error occurred")
        QMessageBox.information(self, '提示', "Finished")
        # QMessageBox.information(self, '提示', gpu_id, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        # dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        # self.lineEdit_sample.setText(dir_tmp)
        # QDir.setCurrent(dir_tmp)