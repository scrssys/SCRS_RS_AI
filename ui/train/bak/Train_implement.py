from ui.train.Dialog_train import Ui_Dialog_train
from os import system
from subprocess import call
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox

class child_train(QDialog,Ui_Dialog_train):
    def __init__(self):
        super(child_train,self).__init__()
        self.setWindowTitle("train")
        self.setupUi(self)
    def slot_open_sample(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_sample.setText(dir_tmp)
    def slot_open_config(self):
        str, _ = QFileDialog.getOpenFileName(self, "Select road mask", '../../data/', self.tr("masks(*)"))
        self.lineEdit_config.setText(str)
    def slot_open_modelpath(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_modelpath.setText(dir_tmp)
    def slot_process(self):
        sample = self.lineEdit_sample.text()
        config = self.lineEdit_config.text()
        model = self.lineEdit_modelpath.text()
        QMessageBox.information(self, '提示',
        "sample:{}\n config :{}\n model :{}".format(sample,config,model)
        ,QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
        print( call(["python3","../test.py"]))
        print( QMessageBox.information(self, '提示', self.lineEdit_config.text(), QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes))
        # dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        # self.lineEdit_sample.setText(dir_tmp)
        # QDir.setCurrent(dir_tmp)