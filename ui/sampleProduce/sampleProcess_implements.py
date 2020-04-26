import os
import sys
import gdal
import numpy as np
import random
import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt

from scipy.signal import medfilt, medfilt2d
from skimage import exposure
import cv2
from tqdm import tqdm
from PyQt5.QtCore import QFileInfo, QDir, QCoreApplication, Qt
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox
from ui.sampleProduce.SampleGenCommon import Ui_Dialog_sampleGenCommon
from ui.sampleProduce.SampleGenSelfAdapt import Ui_Dialog_sampleGenSelfAdapt
from ui.sampleProduce.Sample2H5 import Ui_Dialog_sample2H5

from ulitities.base_functions import get_file, load_img_by_gdal
from ui.sampleProduce.sampleProcess_backend import SampleGenerate,base_message
from data_prepare.create_h5_from_samples import create_h5_from_samples

sampleGen_dict={'input_dir':'', 'output_dir':'', 'window_size':256, 'min':0, 'max':2, 'target_label':1, 'sample_num':5000, 'mode':'augment'}
sampleGenSelfAdapt_dict={'input_dir':'', 'output_dir':'', 'window_size':256, 'min':0, 'max':2, 'target_label':1, 'sample_scaleRate':1.0, 'mode':'augment', 'imgmode':"normalize"}
sample2H5_dict={'input_dir':'', 'output_dir':'', 'mode':0}


class child_sampleGenCommon(QDialog, Ui_Dialog_sampleGenCommon,base_message):
    def __init__(self):
        super(child_sampleGenCommon,self).__init__()
        # self.label_targetLabel.setVisible(self, False)
        # self.spinBox_targetLabel.setVisible(self, False)
        self.Flag_binary=True

        self.setupUi(self)

    def slot_input(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_input.setText(dir_tmp)
        # QDir.setCurrent(dir_tmp)

    def slot_output(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_output.setText(dir_tmp)
        # QDir.setCurrent(dir_tmp)

    def slot_strategy_binary(self):
        self.label_targetLabel.setVisible(True)
        self.spinBox_targetLabel.setVisible(True)

    def slot_strategy_multiclass(self):
        self.label_targetLabel.setVisible(False)
        self.spinBox_targetLabel.setVisible(False)

    def slot_ok(self):
        self.buttonBox.setEnabled(False)
        self.setWindowModality(Qt.ApplicationModal)

        self.Flag_binary = self.radioButton_binary.isChecked()

        input_dict = sampleGen_dict
        input_dict['input_dir'] = self.lineEdit_input.text()
        input_dict['output_dir'] = self.lineEdit_output.text()
        input_dict['window_size']= self.spinBox_windsize.value()
        input_dict['min'] = self.spinBox_min_2.value()
        input_dict['max'] = self.spinBox_max_2.value()
        input_dict['target_label'] = self.spinBox_targetLabel.value()
        assert (self.spinBox_targetLabel.value()<=self.spinBox_max_2.value())
        input_dict['sample_num'] = self.spinBox_sampNum.value()
        st = self.checkBox.isChecked()
        if st ==True:
            input_dict['mode'] = 'augument'
        else:
            input_dict['mode'] = 'original'

        instance = SampleGenerate(input_dict)
        if self.radioButton_binary.isChecked():
            self.send("produce_training_samples_binary")

            instance.produce_training_samples_binary(self.send)
        else:
            self.send("produce_training_samples_multiclass")
            instance.produce_training_samples_multiclass(self.send)

        QMessageBox.information(self, "Prompt", self.tr("Sample produced!"))
        self.buttonBox.setEnabled(True)
        self.setWindowModality(Qt.NonModal)


class child_sampleGenSelfAdapt(QDialog, Ui_Dialog_sampleGenSelfAdapt,base_message):
    def __init__(self):
        super(child_sampleGenSelfAdapt,self).__init__()
        # self.label_targetLabel.setVisible(self, False)
        # self.spinBox_targetLabel.setVisible(self, False)
        self.Flag_binary=True

        self.setupUi(self)

    def slot_input(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_input.setText(dir_tmp)
        # QDir.setCurrent(dir_tmp)

    def slot_output(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_output.setText(dir_tmp)
        # QDir.setCurrent(dir_tmp)

    def slot_strategy_binary(self):
        self.label_targetLabel.setVisible(True)
        self.spinBox_targetLabel.setVisible(True)

    def slot_strategy_multiclass(self):
        self.label_targetLabel.setVisible(False)
        self.spinBox_targetLabel.setVisible(False)

    def slot_ok(self):
        self.setWindowModality(Qt.ApplicationModal)

        self.Flag_binary = self.radioButton_binary.isChecked()

        input_dict = sampleGen_dict
        input_dict['input_dir'] = self.lineEdit_input.text()
        input_dict['output_dir'] = self.lineEdit_output.text()
        input_dict['window_size']= self.spinBox_windsize.value()
        input_dict['min'] = self.spinBox_min.value()
        input_dict['max'] = self.spinBox_max.value()
        input_dict['target_label'] = self.spinBox_targetLabel.value()
        assert (self.spinBox_targetLabel.value()<=self.spinBox_max.value())
        input_dict['sample_scaleRate'] = self.doubleSpinBox_sampleScale.value()
        st = self.checkBox.isChecked()
        if st ==True:
            input_dict['mode'] = 'augument'
        else:
            input_dict['mode'] = 'original'

        sp = self.checkBox_normimg.isChecked()
        if sp == True:
            input_dict['imgmode'] = 'normalize'
        else:
            input_dict['imgmode'] = 'original'

        instance = SampleGenerate(input_dict)
        self.buttonBox.setEnabled(False)
        if self.radioButton_binary.isChecked():
            self.send("Produce_training_samples_binary_selfAdapt")
            instance.produce_training_samples_binary_selfAdapt(self.send)
        else:
            self.send("Produce_training_samples_multiclass_selfAdapt")
            instance.produce_training_samples_multiclass_selfAdapt(self.send)

        QMessageBox.information(self, "Prompt", self.tr("Sample produced!"))

        self.setWindowModality(Qt.NonModal)
        self.buttonBox.setEnabled(True)


class child_sample2H5(QDialog, Ui_Dialog_sample2H5,base_message):
    def __init__(self):
        super(child_sample2H5,self).__init__()
        # self.label_targetLabel.setVisible(self, False)
        # self.spinBox_targetLabel.setVisible(self, False)
        self.Flag_binary=True

        self.setupUi(self)

    def slot_input(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_input.setText(dir_tmp)
        # QDir.setCurrent(dir_tmp)

    def slot_output(self):
        # str, _ = QFileDialog.getOpenFileName(self, "Select h5 file", '../../data/', self.tr("Json(*.h5)"))
        # self.lineEdit_sample.setText(str)
        # dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        str, _ = QFileDialog.getSaveFileName(self, "saving to h5", '../../data/',self.tr("H5(*.h5)"))
        self.lineEdit_output.setText(str)
        # QDir.setCurrent(dir_tmp)


    def slot_ok(self):
        self.buttonBox.setEnabled(False)
        self.setWindowModality(Qt.ApplicationModal)

        self.Flag_binary = self.radioButton_binary.isChecked()

        # input_dict = sample2H5_dict
        input_dir = self.lineEdit_input.text()
        if not os.path.isdir(input_dir):
            print("Error: input dir is not a directory:{}".format(input_dir))
            return -1
        save_file = self.lineEdit_output.text()
        if not os.path.isdir(os.path.split(save_file)[0]):
            print("Error: dir of save_file doese not exist:{}".format(save_file))
            return -2

        # input_dict['window_size']= self.spinBox_windsize.value()
        # input_dict['min'] = self.spinBox_min_2.value()
        # input_dict['max'] = self.spinBox_max_2.value()
        # input_dict['target_label'] = self.spinBox_targetLabel.value()
        # assert (self.spinBox_targetLabel.value()<=self.spinBox_max_2.value())
        # input_dict['sample_num'] = self.spinBox_sampNum.value()
        # st = self.checkBox.isChecked()
        val_rate = self.doubleSpinBox_val_rate.value()

        mode=self.comboBox_mode.currentIndex()
        if not isinstance(mode,int):
            print("mode is not a int:{}".format(mode))
            return -3

        # instance = SampleGenerate(input_dict)
        ret = create_h5_from_samples(input_dir,save_file, val_rate=val_rate, mode=mode)
        if ret !=0:
            QMessageBox.information(self, "Error", self.tr("Converting h5 file failed!"))
        else:
            QMessageBox.information(self, "Prompt", self.tr("Sample produced!"))
        self.buttonBox.setEnabled(True)
        self.setWindowModality(Qt.NonModal)



