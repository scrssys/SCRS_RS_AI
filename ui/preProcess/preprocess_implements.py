#coding:utf-8
import os
import sys
import gdal
import cv2
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from PyQt5 import QtCore
# from PyQt5.QtCore import QFileInfo, QDir, QCoreApplication, Qt
# from PyQt5.QtGui import QIntValidator
# from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox
from ui.preProcess.ImageStretch import Ui_Dialog_image_stretch
from ui.preProcess.label_check import Ui_Dialog_label_check
from ui.preProcess.ImageClip import Ui_Dialog_image_clip
from ui.preProcess.convert_8bit import Ui_Dialog_convert8bit
from ui.preProcess.samplecrop import Ui_Dialog_samplecrop
from ui.preProcess.index_calc import Ui_Dialog_index_calc
from ui.preProcess.band_combine import Ui_Dialog_band_combine
from ui.preProcess.crop_by_extent import Ui_Dialog_crop_by_extent
from ui.preProcess.rasterizeLayer import Ui_Dialog_rasterizeLayer
from ulitities.xml_prec import generate_xml_from_dict, parse_xml_to_dict
from ulitities.base_functions import get_file, load_img_by_gdal,base_message
from .preprocess_backend import image_normalize, image_clip
from data_prepare.convert_to_8bits import batch_convert_8bit,batch_convert_8bit_minmax
from data_prepare.crop_samples import Simple_Crop
from data_prepare.index_calc import batch_calc_index
from data_prepare.band_combine import batch_band_combine
from data_prepare.rasterizeLayer import crop_by_extent,rasterize_layer

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from  PyQt5.QtGui import *
# QTranslator()

imgStretch_dict = {'input_dir': '', 'output_dir': '', 'NoData': '65535', 'OutBits': '16bits',
                       'StretchRange': '1024','CutValue': '100'}
imgClip_dict = {'input_file':'', 'output_file':'', 'x':'0', 'y':'0', 'row':'1', 'column':'1'}
class child_rasterizeLayer(QDialog,Ui_Dialog_rasterizeLayer,base_message):
    def __init__(self):
        super(child_rasterizeLayer, self).__init__()
        self.setupUi(self)
        self.new_translate()
    def new_translate(self):
        pass
    def slot_select_imgpath(self):
        dir_tmp ,_= QFileDialog.getOpenFileName(self, "select a existing directory", '../../data/')
        self.lineEdit_imgpath.setText(dir_tmp)
    def slot_select_shpfilepath(self):
        dir_tmp ,_= QFileDialog.getOpenFileName(self, "select a existing directory", '../../data/')
        self.lineEdit_shpfilepath.setText(dir_tmp)
    def slot_select_outputpath(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_outputpath.setText(dir_tmp)
    def slot_ok(self):
        imgfile = self.lineEdit_imgpath.text()
        shpfile = self.lineEdit_shpfilepath.text()
        outputpath = self.lineEdit_outputpath.text()
        attributeFiled = self.lineEdit_attributeFiledName.text()
        self.buttonBox.setEnabled(False)
        ret = 0
        try:
            rasterize_layer(imgfile,shpfile,outputpath,attributeFiled)
        except:
            QMessageBox.information(self, '提示', "Error occurred")
        if ret != 0:
            QMessageBox.information(self, '提示', "Error occurred")
        else:
            QMessageBox.information(self, '提示', "此操作成功")
        self.buttonBox.setEnabled(True)
        pass
class child_crop_by_extent(QDialog,Ui_Dialog_crop_by_extent,base_message):
    def __init__(self):
        super(child_crop_by_extent,self).__init__()
        self.setupUi(self)
        self.new_translate()
    def new_translate(self):
        pass
    def slot_select_imgfile(self):
        dir_tmp ,_= QFileDialog.getOpenFileName(self, "select a existing directory", '../../data/')
        self.lineEdit_imgpath.setText(dir_tmp)
    def slot_select_shpfile(self):
        dir_tmp ,_= QFileDialog.getOpenFileName(self, "select a existing directory", '../../data/')
        self.lineEdit_shpfilepath.setText(dir_tmp)
    def slot_select_outputpath(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_outputpath.setText(dir_tmp)
    def slot_ok(self):
        imgfile = self.lineEdit_imgpath.text()
        shpfile = self.lineEdit_shpfilepath.text()
        outputpath = self.lineEdit_outputpath.text()
        self.buttonBox.setEnabled(False)
        ret = 0
        ret = crop_by_extent(imgfile, shpfile, outputpath)
        if ret != 0:
            QMessageBox.information(self, '提示', "Error occurred")
        else:
            QMessageBox.information(self, '提示', "此操作成功")
        self.buttonBox.setEnabled(True)



class child_band_combine(QDialog,Ui_Dialog_band_combine,base_message):
    def __init__(self):
        super(child_band_combine,self).__init__()
        self.setupUi(self)
        self.new_translate()

    def new_translate(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog_band_combine", "影像波段合成"))
        self.label.setText(_translate("inputpath", "输入路径"))
        self.label_2.setText(_translate("outputpath", "输出路径"))

    def slot_select_inputpath(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_imagpath.setText(dir_tmp)
    def slot_select_outputpath(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_outputpath.setText(dir_tmp)
    def slot_ok(self):
        dir_input = self.lineEdit_imagpath.text()
        dir_output = self.lineEdit_outputpath.text()
        nodata = self.spinBox.value()
        self.buttonBox.setEnabled(False)
        ret =0
        ret = batch_band_combine(dir_input,dir_output,nodata=nodata)
        if ret !=0:
            QMessageBox.information(self, '提示', "Error occurred")
        else:
            QMessageBox.information(self, '提示', "波段合成成功")
        self.buttonBox.setEnabled(True)


class child_index_calc(QDialog,Ui_Dialog_index_calc,base_message):
    def __init__(self):
        super(child_index_calc,self).__init__()
        self.setupUi(self)
        self.new_translate()

    def new_translate(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog_index", "指数计算"))
        self.label.setText(_translate("imagepath", "输入路径"))
        self.label_2.setText(_translate("outputpath", "输出路径"))
        self.label_3.setText(_translate("Index", "指数类型"))
    def slot_select_inputpath(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_imagpath.setText(dir_tmp)
    def slot_select_outputpath(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_outputpath.setText(dir_tmp)
    def slot_ok(self):
        dir_input = self.lineEdit_imagpath.text()
        dir_output = self.lineEdit_outputpath.text()
        nodata = self.spinBox.value()
        index_tpye = self.comboBox.currentText()
        self.buttonBox.setEnabled(False)
        ret =0
        ret = batch_calc_index(dir_input,dir_output,keyword=index_tpye,nulldata=nodata)
        if ret !=0:
            QMessageBox.information(self, '提示', "Error occurred")
        else:
            QMessageBox.information(self, '提示', "计算成功")
        self.buttonBox.setEnabled(True)

# HAS_INVALID_VALUE = False
class child_convert_8bit(QDialog,Ui_Dialog_convert8bit,base_message):
    def __init__(self):
        super(child_convert_8bit,self).__init__()
        self.setWindowTitle("convert 8bit")
        self.setupUi(self)
        self.new_translate()

    def new_translate(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("conver8bits", "图像转8bits"))
        self.label.setText(_translate("imagepath", "输入路径"))
        self.label_2.setText(_translate("outputpath", "输出路径"))
        self.label_3.setText(_translate("Strench type", "拉伸方式"))
    def slot_select_samplepath(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_imagpath.setText(dir_tmp)
    def slot_select_outputpath(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_outputpath.setText(dir_tmp)
    def slot_ok(self):
        dir_input = self.lineEdit_imagpath.text()
        dir_output = self.lineEdit_outputpath.text()
        nodata = self.spinBox.value()

        # QMessageBox.information(self, '提示',
        #                         "input:{}\n output :{}".format(dir_sample, dir_output)
        #                         , QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        #excute pragram
        # cmd = ['python', '../data_prepare/convert_to_8bits.py',"batch_convert_8bit" ,dir_sample,dir_output]
        # try:
        #     subprocess.call(cmd)
        # except:
        #     QMessageBox.information(self, '提示', "Error occurred")
        # QMessageBox.information(self, '提示', "Finished")
        # print("dir_input is " + dir_output+ "\n")
        convert_func = self.comboBox_scale.currentText()
        self.buttonBox.setEnabled(False)
        try:
            if convert_func in "Percent clip":
                self.send("Using Percent Clip Streth")
                batch_convert_8bit(self.send,dir_input, dir_output, nodata)
            else:
                self.send("Using Max Min Streth")
                batch_convert_8bit_minmax(self.send, dir_input, dir_output, nodata)

            QMessageBox.information(self, '提示', "Finished")
        except:
            QMessageBox.information(self, '提示', "Error occurred")
        finally:
            self.buttonBox.setEnabled(True)


class child_samplecrop(QDialog,Ui_Dialog_samplecrop,base_message):
    def __init__(self):
        super(child_samplecrop,self).__init__()
        # self.lineEdit_cropsize.setPlaceholderText()

        self.setWindowTitle("samplecrop")
        self.setupUi(self)
        self.new_translate()

    def new_translate(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("samplecrop", "样本裁剪"))
        self.label.setText(_translate("Sampledir", "输入路径"))
        self.label_3.setText(_translate("Outputdir", "输出路径"))
        self.label_2.setText(_translate("CropSize:", "尺寸"))
        pIntvalidator=QIntValidator(self)
        pIntvalidator.setRange(1,9999)
        self.lineEdit_cropsize.setValidator(pIntvalidator)
    def slot_select_inputdir(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_inputdir.setText(dir_tmp)
        # QDir.setCurrent(dir_tmp)
    def slot_select_outputdir(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_outputdir.setText(dir_tmp)
    def slot_ok(self):
        self.setWindowModality(Qt.ApplicationModal)
        cropsize = self.lineEdit_cropsize.text()
        sample_dir = self.lineEdit_inputdir.text()
        output_dir = self.lineEdit_outputdir.text()

        #excute program

        # cmd =['python',r'C:\Users\SCRS\PycharmProjects\SCRS_RS_AI-developer\data_prepare\crop_samples.py',
        #       "Simple_Crop",sample_dir,output_dir,cropsize]
        # # cmd =['python',r'..\data_prepare\crop_samples.py',
        # #       "Simple_Crop",sample_dir,output_dir,cropsize]
        # try:
        #     subprocess.call(cmd)
        # except:
        #     QMessageBox.information(self, '错误', "Error occurred")
        # QMessageBox.information(self, '提示', "Finished")

        try:
            self.pushButton_process.setEnabled(False)
            Simple_Crop(self.send, sample_dir, output_dir, cropsize)
            QMessageBox.information(self, '提示', "Finished")
        except:
            QMessageBox.information(self, '错误', "Error occurred")
        finally:
            self.pushButton_process.setEnabled(True)
        self.setWindowModality(Qt.NonModal)


class child_image_stretch(QDialog, Ui_Dialog_image_stretch,base_message):
    def __init__(self):
        super(child_image_stretch,self).__init__()

        self.setWindowTitle("Image stretch")
        self.setupUi(self)


    def slot_select_input_dir(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_input.setText(dir_tmp)
        # QDir.setCurrent(dir_tmp)

    def slot_select_output_dir(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_output.setText(dir_tmp)
        # QDir.setCurrent(dir_tmp)

    def slot_ok(self):
        self.setWindowModality(Qt.ApplicationModal)
        self.buttonBox.setEnabled(False)
        imgStretch_dict['input_dir'] = self.lineEdit_input.text()
        imgStretch_dict['output_dir'] = self.lineEdit_output.text()
        # nodata = self.spinBox_nodata.value()
        imgStretch_dict['NoData'] = self.spinBox_nodata.value()
        imgStretch_dict['OutBits'] = self.comboBox_outbits.currentText()
        imgStretch_dict['StretchRange']=self.spinBox_range.value()
        imgStretch_dict['CutValue']=self.spinBox_cutvalue.value()

        # ss = QCoreApplication.applicationDirPath()
        # QDir.setCurrent(QCoreApplication.applicationDirPath()) # change current dir to "venv/bin/"
        ''' save parameters into xml '''

        ret =0
        ret = image_normalize(self.send,imgStretch_dict)
        if ret !=0:
            self.send("Error: failed to normalize images")
            print("Error: failed to normalize images")
        else:
            QMessageBox.information(self, 'Prompt', self.tr("Images stretched !"))
        self.buttonBox.setEnabled(True)
        # self.setWindowModality(Qt.NonModal)

        # xmlfile = '../../metadata/image_stretch_inputs.xml'
        # generate_xml_from_dict(imgStretch_dict, xmlfile)
        #
        # QMessageBox.information(self, 'Prompt', self.tr("Have saved the xml file !"))
        # # one_stretch = ImageStretch(imgStretch_dict)
        # # one_stretch.stretch_all_image_from_dict()
        # one_stretch = ImageStretch(inputXml=xmlfile)
        # one_stretch.stretch_all_image_from_xml()
        # QMessageBox.information(self, 'Prompt', self.tr("Images stretched !"))
        self.setWindowModality(Qt.NonModal)



class ImageStretch():
    def __init__(self, inputDict={}, inputXml=''):
        self.in_dict = inputDict
        self.xmlfile = inputXml

    def stretch_all_image_from_dict(self):
        if None == self.in_dict:
            QMessageBox.warning(self, "Warning", self.tr("input dict errors!"))
            sys.exit(-1)
        src_files, tt = get_file(self.in_dict['input_dir'])
        assert (tt != 0)
        NoData = int(self.in_dict['NoData'])
        valid_range = float(self.in_dict['StretchRange'])
        print(valid_range)
        cut_value = float(self.in_dict['CutValue'])
        if '8' in self.in_dict['OutBits']:
            assert(valid_range < 256)
        elif '16' in self.in_dict['OutBits']:
            assert (valid_range < 65536)


        for file in tqdm(src_files):

            absname = os.path.split(file)[1]
            absname = absname.split('.')[0]
            # absname = 'shuidao.png'
            absname = ''.join([absname, '.png'])
            print(absname)
            if not os.path.isfile(file):
                print("input file dose not exist:{}\n".format(file))
                # sys.exit(-1)
                continue

            dataset = gdal.Open(file)
            if dataset == None:
                print("Open file failed: {}".format(file))
                continue

            height = dataset.RasterYSize
            width = dataset.RasterXSize
            im_bands = dataset.RasterCount
            im_type = dataset.GetRasterBand(1).DataType
            img = dataset.ReadAsArray(0, 0, width, height)
            del dataset
            # img = np.array(img, np.uint16)
            img = np.array(img, np.float32)
            result = []
            for i in range(im_bands):
                data = np.array(img[i])
                maxium = data.max()
                minm = data.min()
                mean = data.mean()
                std = data.std()
                print(maxium, minm, mean, std)
                data = data.reshape(height * width)
                ind = np.where((data > 0) & (data < NoData))
                ind = np.array(ind)

                a, b = ind.shape
                print("valid value number: {}\n".format(b))
                # tmp = np.zeros(b, np.uint16)
                tmp = np.zeros(b, np.float32)
                for j in range(b):
                    tmp[j] = data[ind[0, j]]
                tmaxium = tmp.max()
                tminm = tmp.min()
                tmean = tmp.mean()
                tstd = tmp.std()
                print(tmaxium, tminm, tmean, tstd)
                tt = (data - tmean) / tstd  # first Z-score normalization
                tt = (tt + 4) * valid_range / 8.0 - cut_value
                tind = np.where(data == 0)

                tt = np.array(tt)
                # tt = tt.astype(np.uint8)
                tt = tt.astype(np.uint16)
                tt[tind] = 0

                smaxium = tt.max()
                sminm = tt.min()
                smean = tt.mean()
                sstd = tt.std()
                print(smaxium, sminm, smean, sstd)

                out = tt.reshape((height, width))
                result.append(out)

            outputfile = os.path.join(self.in_dict['output_dir'], absname)
            driver = gdal.GetDriverByName("GTiff")

            if '8' in self.in_dict['OutBits']:
                outdataset = driver.Create(outputfile, width, height, im_bands, gdal.GDT_Byte)
            elif '16' in self.in_dict['OutBits']:
                outdataset = driver.Create(outputfile, width, height, im_bands, gdal.GDT_UInt16)
            # outdataset = driver.Create(outputfile, width, height, im_bands, gdal.GDT_UInt16)

            for i in range(im_bands):
                outdataset.GetRasterBand(i + 1).WriteArray(result[i])

            del outdataset

    def stretch_all_image_from_xml(self):
        if not os.path.isfile(self.xmlfile):
            QMessageBox.warning(self, "Warning", self.tr("input xml not exist!"))
            sys.exit(-1)
        new_dict = parse_xml_to_dict(self.xmlfile)
        self.in_dict = new_dict[0]
        src_files, tt = get_file(self.in_dict['input_dir'])
        assert (tt != 0)
        NoData = int(self.in_dict['NoData'])
        valid_range = float(self.in_dict['StretchRange'])
        print(valid_range)
        cut_value = float(self.in_dict['CutValue'])
        if '8' in self.in_dict['OutBits']:
            assert(valid_range < 256)
        elif '16' in self.in_dict['OutBits']:
            assert (valid_range < 65536)


        for file in tqdm(src_files):

            absname = os.path.split(file)[1]
            absname = absname.split('.')[0]
            # absname = 'shuidao.png'
            absname = ''.join([absname, '.png'])
            print(absname)
            if not os.path.isfile(file):
                print("input file dose not exist:{}\n".format(file))
                # sys.exit(-1)
                continue

            dataset = gdal.Open(file)
            if dataset == None:
                print("Open file failed: {}".format(file))
                continue

            height = dataset.RasterYSize
            width = dataset.RasterXSize
            im_bands = dataset.RasterCount
            im_type = dataset.GetRasterBand(1).DataType
            img = dataset.ReadAsArray(0, 0, width, height)
            del dataset
            # img = np.array(img, np.uint16)
            img = np.array(img, np.float32)
            result = []
            for i in range(im_bands):
                data = np.array(img[i])
                maxium = data.max()
                minm = data.min()
                mean = data.mean()
                std = data.std()
                print(maxium, minm, mean, std)
                data = data.reshape(height * width)
                ind = np.where((data > 0) & (data < NoData))
                ind = np.array(ind)

                a, b = ind.shape
                print("valid value number: {}\n".format(b))
                # tmp = np.zeros(b, np.uint16)
                tmp = np.zeros(b, np.float32)
                for j in range(b):
                    tmp[j] = data[ind[0, j]]
                tmaxium = tmp.max()
                tminm = tmp.min()
                tmean = tmp.mean()
                tstd = tmp.std()
                print(tmaxium, tminm, tmean, tstd)
                tt = (data - tmean) / tstd  # first Z-score normalization
                tt = (tt + 4) * valid_range / 8.0 - cut_value
                tind = np.where(data == 0)

                tt = np.array(tt)
                # tt = tt.astype(np.uint8)
                tt = tt.astype(np.uint16)
                tt[tind] = 0

                smaxium = tt.max()
                sminm = tt.min()
                smean = tt.mean()
                sstd = tt.std()
                print(smaxium, sminm, smean, sstd)

                out = tt.reshape((height, width))
                result.append(out)

            outputfile = os.path.join(self.in_dict['output_dir'], absname)
            driver = gdal.GetDriverByName("GTiff")

            if '8' in self.in_dict['OutBits']:
                outdataset = driver.Create(outputfile, width, height, im_bands, gdal.GDT_Byte)
            elif '16' in self.in_dict['OutBits']:
                outdataset = driver.Create(outputfile, width, height, im_bands, gdal.GDT_UInt16)
            # outdataset = driver.Create(outputfile, width, height, im_bands, gdal.GDT_UInt16)

            for i in range(im_bands):
                outdataset.GetRasterBand(i + 1).WriteArray(result[i])

            del outdataset


"""
for ui label_check
"""
class child_label(QDialog, Ui_Dialog_label_check,base_message):
    def __init__(self):
        super(child_label, self).__init__()
        self.setupUi(self)

    def slot_select_input_path(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_input.setText(dir_tmp)
        # QDir.setCurrent(dir_tmp)

    def slot_ok(self):
        self.buttonBox.setEnabled(False)
        self.setWindowModality(Qt.ApplicationModal)
        # QDir.setCurrent(QCoreApplication.applicationDirPath())  # change current dir to "venv/bin/"
        min =self.spinBox_min.value()
        max=self.spinBox_max.value()
        assert (min<=max)
        valid_labels=list(range(min,max+1))
        input_path = self.lineEdit_input.text()
        if not os.path.isdir(input_path):
            QMessageBox.warning(self, "Warning", self.tr("input path is not exist!"))
        self.send("checking......")
        instance = DataCheck_and_modify(valid_labels)
        instance.select_invalid_values(input_path)
        self.send("Checked ")
        QMessageBox.information(self, 'Prompt', self.tr("Check completely !"))
        self.buttonBox.setEnabled(True)
        self.setWindowModality(Qt.NonModal)

class DataCheck_and_modify():
    def __init__(self,valid_values=[0]):
        self.valid_values = valid_values
        self.HAS_INVALID_VALUE = False

    def make_invalid_to_zeros(self, img, false_values):
        height, width = img.shape

        tp_img = img.reshape((height * width))
        for inv_lab in false_values:
            index = np.where(tp_img == inv_lab)
            tp_img[index] = 0
        tp_img = tp_img.reshape((height, width))

        return tp_img

    def select_invalid_values(self, filepath):
        files, num = get_file(filepath)
        assert (num != 0)

        for label_file in tqdm(files):
            # label_file = input_label_path + os.path.split(src_file)[1]
            #
            # ret,src_img = load_img(src_file)
            # assert(ret==0)

            label_img = load_img_by_gdal(label_file, grayscale=True)
            label_img = np.array(label_img)

            local_labels = np.unique(label_img)
            invalid_labels = []

            self.HAS_INVALID_VALUE = False

            for tmp in local_labels:
                if tmp not in self.valid_values:
                    invalid_labels.append(tmp)
                    print("\nWarning: some label is not valid value")
                    print("\nFile: {}".format(label_file))
                    self.HAS_INVALID_VALUE = True

            if self.HAS_INVALID_VALUE == True:
                new_label_img = self.make_invalid_to_zeros(label_img, invalid_labels)
                new_label_file = os.path.split(label_file)[0] + '/new_' + os.path.split(label_file)[1]
                cv2.imwrite(new_label_file, new_label_img)
                self.HAS_INVALID_VALUE = False
                label_img = new_label_img

            plt.imshow(label_img, cmap='gray')
            plt.show()

        print("Check completely!\n")



"""
for ui image_clip
"""
class child_ImageClip(QDialog, Ui_Dialog_image_clip,base_message):
    def __init__(self):
        super(child_ImageClip, self).__init__()
        self.setupUi(self)

    def slot_input(self):
        dir_tmp, _ = QFileDialog.getOpenFileName(self, "Open image", '../../data/', self.tr("Images(*.png *.jpg *.tif)"))
        self.lineEdit_input.setText(dir_tmp)
        tp = QFileInfo(dir_tmp).path()
        # QDir.setCurrent(tp)

    def slot_output(self):
        # dir_tmp = QFileDialog.getOpenFileName(self, "Open image", '../../data/')
        dir_tmp, _ = QFileDialog.getSaveFileName(self, "Open image", '../../data/',
                                                 self.tr("Images(*.png *.jpg *.tif)"))
        self.lineEdit_output.setText(dir_tmp)
        # QDir.setCurrent(dir_tmp)

    def slot_ok(self):
        self.setWindowModality(Qt.ApplicationModal)
        self.buttonBox.setEnabled(False)
        inputDict = imgClip_dict
        inputDict['input_file']=self.lineEdit_input.text()
        inputDict['output_file']=self.lineEdit_output.text()
        inputDict['x']=self.spinBox_x.value()
        inputDict['y']=self.spinBox_y.value()
        inputDict['row']=self.spinBox_row.value()
        inputDict['column']=self.spinBox_column.value()

        # QDir.setCurrent(QCoreApplication.applicationDirPath())  # change current dir to "venv/bin/"

        ret =0
        self.send("Dealing : " + inputDict['input_file'])
        ret = image_clip(self.send,inputDict)
        if ret !=0:
            self.send("Error: failed to clip images")
        else:
            QMessageBox.information(self, 'Prompt', self.tr("Images cliped !"))
        self.buttonBox.setEnabled(True)
        self.setWindowModality(Qt.NonModal)

        # xmlFileName = '../../metadata/image_clip_inputs.xml'
        # generate_xml_from_dict(inputDict, xmlFileName)
        #
        # QMessageBox.information(self, 'Prompt', self.tr("Have saved the xml file !"))
        # instance = ImageClip(inputDict)
        # instance.image_clip_from_dict()
        # QMessageBox.information(self, 'Prompt', self.tr("Images clipped !"))
        # self.setWindowModality(Qt.NonModal)

class ImageClip():
    def __init__(self,input_dict={}, xmlfile=''):
        self.input_dict = input_dict
        self.xmlfile= xmlfile

    def image_clip_from_dict(self):
        input_src_file = self.input_dict['input_file']
        if not os.path.isfile(input_src_file):
            print("input file is not existing!")
            sys.exit(-1)

        dataset = gdal.Open(input_src_file)
        if dataset == None:
            print("Open file failed:{}".format(input_src_file))
            sys.exit(-1)

        Yheight = dataset.RasterYSize
        Xwidth = dataset.RasterXSize
        im_bands = dataset.RasterCount
        d_type = dataset.GetRasterBand(1).DataType
        img = dataset.ReadAsArray(0, 0, Xwidth, Yheight)
        del dataset

        x = int(self.input_dict['x'])
        y = int(self.input_dict['y'])
        height = int(self.input_dict['row'])
        width = int(self.input_dict['column'])
        assert(width<=Xwidth and height<=Yheight)
        output_file = self.input_dict['output_file']

        if im_bands == 1:
            output_img = img[y:y + height, x:x + width]
            output_img = np.array(output_img, np.uint16)
            output_img = np.array(output_img, np.uint8)
            plt.imshow(output_img)
            plt.show()
            cv2.imwrite(output_file, output_img)  # for label clip
        else:
            output_img = img[:, y:y + height, x:x + width]
            plt.imshow(output_img[0])
            plt.show()
            driver = gdal.GetDriverByName("GTiff")
            # outdataset = driver.Create(clip_src_file, window_size, window_size, im_bands, d_type)
            outdataset = driver.Create(output_file,  width, height, im_bands, d_type)
            if outdataset == None:
                print("create dataset failed!\n")
                sys.exit(-2)
            if im_bands == 1:
                outdataset.GetRasterBand(1).WriteArray(output_img)
            else:
                for i in range(im_bands):
                    outdataset.GetRasterBand(i + 1).WriteArray(output_img[i])
            del outdataset
