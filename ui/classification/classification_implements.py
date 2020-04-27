import os, sys

from main_thread import *

from PyQt5.QtCore import QFileInfo,Qt,QCoreApplication
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox
from ui.classification.predict_one import Ui_Dialog_predict_one
from ui.classification.classification_backend import predict_backend
from ui.classification.Dialog_predict import Ui_Dialog_predict
from predict import predict
from ulitities.base_functions import base_message
inputdict = {'input':'','output':'','gpu':'0','config':'','model':''}


class child_predict(QDialog, Ui_Dialog_predict,base_message):
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
    def slot_model(self):
        dir_tmp, _ = QFileDialog.getOpenFileName(self, "Select model", "",
                                                 self.tr("h5(*.h5)"))
        self.lineEdit_model.setText(dir_tmp)
    def slot_done(self):
        input = self.lineEdit_input.text()
        output = self.lineEdit_output.text()
        config=self.lineEdit_config.text()
        gpu_id = self.comboBox_gpu.currentText()
        model = self.lineEdit_model.text()

        # config = '/home/omnisky/PycharmProjects/data/rice/samples_uav1_crop_fpn/config_binary_global.json'
        # gpu_id= 3
        # input="/home/omnisky/PycharmProjects/data/samples/snowlineSamples/croped/960x960/src"
        # output = "/home/omnisky/PycharmProjects/data/rice/test/pred/fpn"
        # model = "/home/omnisky/PycharmProjects/data/rice/models/fpn/rice_uav1_null_fpn_seresnet34_binary_crossentropy_adam_480_012bands_2020-03-25_15-49-16best.h5"
        self.buttonBox.setEnabled(False)
        os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)
        try:
            predict(self.send,config,gpu_id,input,output,model)
            QMessageBox.information(self, 'Prompt', "Finished")
        except:
            QMessageBox.information(self, '错误', "Error occurred")
        finally:
            self.buttonBox.setEnabled(True)
        # self.buttonBox.setEnabled(True)
        # self.predict_thread = main_thread()
        # self.predict_thread.main_signal.connect(self.set_btn)
        # self.predict_thread.add_massage.connect()
        # self.predict_thread.run_predict(config,gpu_id,input,output,model)


        # cmd =['python','../predict.py','--gpu',gpu_id, '--input', input, '--output', output,
        #       '--config', config,"--model",model]
        # try:
        #     subprocess.call(cmd)
        # except:
        #     QMessageBox.information(self, '错误', "Error occurred")


        # cs = '/home/omnisky/PycharmProjects/data/rice/samples_uav1_crop_fpn/config_binary_global.json'
        # gpu_id= 3
        # inpu="/home/omnisky/PycharmProjects/data/rice/test/all0.1/image"
        # outpu = "/home/omnisky/PycharmProjects/data/rice/test/pred/fpn"
        # mode = "/home/omnisky/PycharmProjects/data/rice/models/fpn/rice_uav1_null_fpn_seresnet34_binary_crossentropy_adam_480_012bands_2020-03-25_15-49-16best.h5"
        #
        # ret=predict(cs, gpu_id, inpu, outpu, mode)
        # if ret!=0:
        #     QMessageBox.warning(self,'提示', "Wrong")
        # else:
        #     QMessageBox.information(self, '提示', "Finished")




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