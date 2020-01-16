
import os, sys
import subprocess
from PyQt5.QtCore import QFileInfo, QDir, QCoreApplication, Qt
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox, QApplication
from ui.classification.predict_one import Ui_Dialog_predict_one
from ui.classification.classification_backend import predict_backend
from ui.classification.Dialog_predict import Ui_Dialog_predict

inputdict = {'input':'','output':'','gpu':'0','config':'','model':''}


class child_predict(QDialog, Ui_Dialog_predict):
    def __init__(self):
        super(child_predict, self).__init__()
        self.setupUi(self)

    def slot_input(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing dir", '')
        self.lineEdit_input.setText(dir_tmp)

    def slot_output(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing dir", '')
        self.lineEdit_output.setText(dir_tmp)

    def slot_config(self):
        dir_tmp, _ = QFileDialog.getOpenFileName(self, "Select config", "",
                                                 self.tr("Json(*.json)"))
        self.lineEdit_config.setText(dir_tmp)

    def slot_done(self):
        input = self.lineEdit_input.text()
        output = self.lineEdit_output.text()
        config=self.lineEdit_config.text()
        gpu_id = self.comboBox_gpu.currentText()
        print(os.getcwd())
        print(QApplication.applicationDirPath())
        # print(os.path.curdir)

        cmd =['python3','../predict.py','--gpu',gpu_id, '--input', input, '--output', output, '--config', config]
        print("Converting command: ", cmd)

        subprocess.call(cmd)
        # subprocess.call('python')



class child_predict_one(QDialog, Ui_Dialog_predict_one):
    def __init__(self):
        super(child_predict_one,self).__init__()
        self.setupUi(self)

    def slot_input(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_input.setText(dir_tmp)
        # QDir.setCurrent(dir_tmp)

    def slot_config(self):
        dir_tmp, _ = QFileDialog.getOpenFileName(self, "Select config", '../../data/',
                                                 self.tr("Json(*.json)"))
        self.lineEdit_config.setText(dir_tmp)
        tp = QFileInfo(dir_tmp).path()
        # QDir.setCurrent(tp)

    def slot_model(self):
        dir_tmp, _ = QFileDialog.getOpenFileName(self, "Select model", '../../data/',
                                                 self.tr("Model(*.h5)"))
        self.lineEdit_model.setText(dir_tmp)
        tp = QFileInfo(dir_tmp).path()
        # QDir.setCurrent(tp)

    def slot_output(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_output.setText(dir_tmp)
        # QDir.setCurrent(dir_tmp)

    def slot_ok(self):
        self.setWindowModality(Qt.ApplicationModal)
        inputdict['input'] = self.lineEdit_input.text()
        if not os.path.isdir(inputdict['input']):
            QMessageBox.warning(self, "Prompt", self.tr("Please check input directory!"))
            sys.exit(-1)
        inputdict['output'] = self.lineEdit_output.text()
        if not os.path.isdir(inputdict['output']):
            QMessageBox.warning(self, "Prompt", self.tr("Output directory is not existed!"))
            os.mkdir(inputdict['output'])
        inputdict['config'] = self.lineEdit_config.text()
        if not os.path.isfile(inputdict['config']):
            QMessageBox.warning(self, "Prompt", self.tr("Please check config file!"))
            sys.exit(-2)
        inputdict['model'] = self.lineEdit_model.text()
        if not os.path.isfile(inputdict['model']):
            QMessageBox.warning(self, "Prompt", self.tr("Please check model file!"))
            sys.exit(-3)
        inputdict['gpu']=self.comboBox_gpu.currentText()
        ret =-1
        ret = predict_backend(inputdict)
        if ret == 0:
            QMessageBox.information(self, "Prompt", self.tr("successfully!"))
        else:
            QMessageBox.warning(self, "Prompt", self.tr("Failed!"))

        self.setWindowModality(Qt.NonModal)