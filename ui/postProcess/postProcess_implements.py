
import os ,sys,subprocess
from tqdm import tqdm
from PyQt5.QtCore import QFileInfo, QDir, QCoreApplication, Qt
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox

from ui.postProcess.CombineMulticlassFromSingleModelResults import Ui_Dialog_combine_multiclas_fromsinglemodel
from ui.postProcess.VoteMultimodleResults import Ui_Dialog_vote_multimodels
from ui.postProcess.AccuracyEvaluate import Ui_Dialog_accuracy_evaluate
from ui.postProcess.Binarization import Ui_Dialog_binarization
from ui.postProcess.PostPrecessBackend import combine_masks, vote_masks, accuracy_evalute,binarize_mask,batchbinarize_masks
from ui.postProcess.RasterToPolygon import Ui_Dialog_raster_to_polygon
from ui.postProcess.removeSmallPolygon import  Ui_Dialog_removeSmallPolygon
from ui.postProcess.crfui import Ui_Dialog_crf
from ulitities.base_functions import get_file, polygonize,base_message
from mask_process.remove_small_object import batch_rmovesmallobj
from mask_process.crf_postpro import  CRFs
combinefile_dict = {'road_mask':'', 'building_mask':'', 'save_mask':'', 'foreground':127}
vote_dict = {'input_files':'', 'save_mask':'', 'target_values':[]}

accEvaluate_dict = {'gt_file':'', 'mask_file':'', 'valid_values':[], 'check_rate':0.5}

binarization_dict = {'grayscale_mask':'', 'binary_mask':'', 'threshold':127}
binarybatch_dict = {'inputdir':'', 'outputdir':'', 'threshold':127}


class child_crf(QDialog, Ui_Dialog_crf,base_message):
    def __init__(self):
        super(child_crf,self).__init__()
        self.setupUi(self)
        self.new_translate()
    def new_translate(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", " CRF后处理"))
        self.groupBox.setTitle(_translate("Unary potential", "一元势"))
        self.groupBox_2.setTitle(_translate("Pairwise potentials", "二元势"))

    def slot_input_img(self):
        str,_=QFileDialog.getOpenFileName(self, "select a image", "../../", self.tr("img(*.png *.*)"))
        self.lineEdit_input_img.setText(str)
        tp_dir = QFileInfo(str).path()
        QDir.setCurrent(tp_dir)

    def slot_input_mask(self):
        str, _ = QFileDialog.getOpenFileName(self, "select a classified mask", "../../", self.tr("img(*.png *.*)"))
        self.lineEdit_input_mask.setText(str)
        tp_dir = QFileInfo(str).path()
        QDir.setCurrent(tp_dir)
    def slot_result_save(self):
        str, _ = QFileDialog.getSaveFileName(self, "Save file", '../../data/', self.tr("mask(*.png *.*)"))
        self.lineEdit_result.setText(str)
        tp_dir = QFileInfo(str).path()
        QDir.setCurrent(tp_dir)

    def slot_ok(self):
        self.setWindowModality(Qt.ApplicationModal)
        self.buttonBox.setEnabled(False)
        input_img = self.lineEdit_input_img.text()
        input_mask = self.lineEdit_input_mask.text()
        save_path = self.lineEdit_result.text()
        gtProb=self.doubleSpinBox_gtprob.value()
        gauss_sxy = self.spinBox_gauss_sxy.value()
        gauss_compat = self.spinBox_gauss_compat.value()
        bilateral_sxy=self.spinBox_bilateral_sxy.value()
        bilateral_srgb=self.spinBox_bilateral_srgb.value()
        bilateral_compat = self.spinBox_bilateral_compat.value()

        try:
            CRFs(input_img,input_mask,save_path,prob=gtProb,gauss_sxy=gauss_sxy,gauss_compat=gauss_compat,
         bilateral_sxy=bilateral_sxy,bilateral_srgb=bilateral_sxy,bilateral_compat=bilateral_sxy)
            QMessageBox.information(self, '提示', "Finished")
        except:
            QMessageBox.information(self, '提示', "Error occurred")
        finally:
            self.buttonBox.setEnabled(True)



class child_raster_to_polygon(QDialog, Ui_Dialog_raster_to_polygon,base_message):
    def __init__(self):
        super(child_raster_to_polygon,self).__init__()
        self.setupUi(self)

    def slot_open_inputdir(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_input.setText(dir_tmp)
        # QDir.setCurrent(dir_tmp)

        # pass

    def slot_open_outputdir(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_output.setText(dir_tmp)
        # QDir.setCurrent(dir_tmp)

    def slot_ok(self):
        self.send("begin : ")
        self.pushButton_ok.setEnabled(False)
        self.setWindowModality(Qt.ApplicationModal)
        input_dir = self.lineEdit_input.text()
        if not os.path.isdir(input_dir):
            QMessageBox.warning(self, "Prompt", self.tr("Please check input directory!"))
            sys.exit(-1)
        output_dir = self.lineEdit_output.text()
        if not os.path.isdir(output_dir):
            QMessageBox.warning(self, "Prompt", self.tr("Output directory is not existed!"))
            os.mkdir(output_dir)

        try:
            files,nb=get_file(input_dir)
            if nb ==0:
                QMessageBox.warning(self, "Prompt", self.tr("No image found!"))
                sys.exit(-2)
            print(files)
            for file in files:#tqdm(files):
                self.send("Polygonize : " +file)
                abs_filename = os.path.split(file)[1]
                abs_filename= abs_filename.split('.')[0]
                shp_file = ''.join([output_dir, '/', abs_filename, '.shp'])
                polygonize(file, shp_file)
        except:
            self.pushButton_ok.setEnabled(True)
            QMessageBox.warning(self, "Prompt", self.tr("Failed!"))
        else:
            QMessageBox.information(self, "Prompt", self.tr("successfully!"))

        self.pushButton_ok.setEnabled(True)
        self.setWindowModality(Qt.NonModal)




class child_Binarization(QDialog, Ui_Dialog_binarization,base_message):

    def __init__(self):
        super(child_Binarization, self).__init__()
        self.setupUi(self)

    def slot_get_grayscale_mask(self):
        # str, _ = QFileDialog.getOpenFileName(self, "Select grayscale mask", '../../data/', self.tr("masks(*.png *jpg)"))
        # self.lineEdit_grayscale_mask.setText(str)
        # tp_dir = QFileInfo(str).path()
        # QDir.setCurrent(tp_dir)
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_grayscale_mask.setText(dir_tmp)
        # QDir.setCurrent(dir_tmp)


    def slot_get_saving_binary_mask_path(self):
        # str, _ = QFileDialog.getSaveFileName(self, "Save file to ...", '../../data/', self.tr("mask(*.png)"))
        # self.lineEdit_binary_mask.setText(str)
        # tp_dir = QFileInfo(str).path()
        # QDir.setCurrent(tp_dir)
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_binary_mask.setText(dir_tmp)
        # QDir.setCurrent(dir_tmp)


    def slot_ok(self):
        # self.setWindowModality(Qt.ApplicationModal)
        # input_dict = binarization_dict
        # input_dict['grayscale_mask'] = self.lineEdit_grayscale_mask.text()
        # input_dict['binary_mask'] = self.lineEdit_binary_mask.text()
        # input_dict['threshold'] = self.spinBox_forground.value()
        #
        # ret = -1
        # ret = binarize_mask(input_dict)
        #
        #
        # if ret ==0:
        #     QMessageBox.information(self,"Prompt", self.tr("successfully!"))
        # else:
        #     QMessageBox.warning(self, "Prompt", self.tr("Failed!"))
        #
        # self.setWindowModality(Qt.NonModal)

        self.setWindowModality(Qt.ApplicationModal)
        self.buttonBox.setEnabled(False )
        input_dict = binarybatch_dict
        input_dict['inputdir'] = self.lineEdit_grayscale_mask.text()
        input_dict['outputdir'] = self.lineEdit_binary_mask.text()
        input_dict['threshold'] = self.spinBox_forground.value()

        ret = -1
        ret = batchbinarize_masks(self.send,input_dict)
        if ret == 0:
            QMessageBox.information(self, "Prompt", self.tr("successfully!"))
        else:
            QMessageBox.warning(self, "Prompt", self.tr("Failed!"))
        self.buttonBox.setEnabled(True)
        self.setWindowModality(Qt.NonModal)



class child_CombineMulticlassFromSingleModelResults(QDialog, Ui_Dialog_combine_multiclas_fromsinglemodel,base_message):
    def __init__(self):
        super(child_CombineMulticlassFromSingleModelResults, self).__init__()
        self.setupUi(self)

    def slot_select_road_mask(self):
        str, _ = QFileDialog.getOpenFileName(self, "Select road mask", '../../data/', self.tr("masks(*.png *jpg)"))
        self.lineEdit_road_mask.setText(str)
        tp_dir = QFileInfo(str).path()
        # QDir.setCurrent(tp_dir)

    def slot_select_building_mask(self):
        str, _ = QFileDialog.getOpenFileName(self, "Select building mask", '../../data/', self.tr("masks(*.png *jpg)"))
        self.lineEdit_building_mask.setText(str)
        tp_dir = QFileInfo(str).path()
        # QDir.setCurrent(tp_dir)

    def slot_get_save_mask(self):
        str, _ = QFileDialog.getSaveFileName(self, "Save file", '../../data/', self.tr("mask(*.png)"))
        self.lineEdit_mask.setText(str)
        tp_dir = QFileInfo(str).path()
        # QDir.setCurrent(tp_dir)

    def slot_ok(self):
        self.setWindowModality(Qt.ApplicationModal)
        input_dict = combinefile_dict
        input_dict['road_mask'] = self.lineEdit_road_mask.text()
        input_dict['building_mask'] = self.lineEdit_building_mask.text()
        input_dict['save_mask'] = self.lineEdit_mask.text()
        if not '.png' in input_dict['save_mask']:
            input_dict['save_mask'] =''.join([input_dict['save_mask'], '.png'])
        input_dict['foreground'] = self.spinBox_forground.value()
        self.send("Begin")
        ret =-1

        ret = combine_masks(self.send,input_dict)

        if ret ==0:
            QMessageBox.information(self,"Prompt", self.tr("successfully!"))

        self.setWindowModality(Qt.NonModal)


class child_VoteMultimodleResults(QDialog, Ui_Dialog_vote_multimodels,base_message):
    def __init__(self):
        super(child_VoteMultimodleResults, self).__init__()
        self.setupUi(self)

    def slot_select_input_files(self):
        filelist, s = QFileDialog.getOpenFileNames(self, "Select files", '../../data/', self.tr("masks(*.png *jpg)"))
        filenum = len(filelist)
        str = self.lineEdit_inputs.text()
        if str != '':
            str += ';'
        for index, file in enumerate(filelist):
            if index ==filenum -1:
                str += file
            else:
                str +=file
                str +=';'
        self.lineEdit_inputs.setText(str)
        tp_dir = QFileInfo(filelist[0]).path()
        # QDir.setCurrent(tp_dir)


    def slot_get_save_mask(self):
        str, _ = QFileDialog.getSaveFileName(self, "Save file", '../../data/', self.tr("mask(*.png)"))
        self.lineEdit_mask.setText(str)
        tp_dir = QFileInfo(str).path()
        # QDir.setCurrent(tp_dir)


    def slot_ok(self):
        self.buttonBox.setEnabled(False)
        self.setWindowModality(Qt.ApplicationModal)
        input_dict = vote_dict
        input_dict['input_files'] = self.lineEdit_inputs.text()
        input_dict['save_mask'] = self.lineEdit_mask.text()
        if not '.png' in input_dict['save_mask']:
            input_dict['save_mask'] =''.join([input_dict['save_mask'], '.png'])

        min = self.spinBox_min.value()
        max = self.spinBox_max.value()
        input_dict['target_values'] = list(range(min, max+1))

        ret =-1
        ret = vote_masks(self.send,input_dict)

        if ret ==0:
            QMessageBox.information(self, "Prompt", self.tr("successfully!"))
        self.buttonBox.setEnabled(True)
        self.setWindowModality(Qt.NonModal)


class child_AccuacyEvaluate(QDialog, Ui_Dialog_accuracy_evaluate,base_message):
    def __init__(self):
        super(child_AccuacyEvaluate, self).__init__()
        self.setupUi(self)

    def slot_select_gt_file(self):
        str, _ = QFileDialog.getOpenFileName(self, "Select ground-truth file", '../../data/', self.tr("mask(*.png *.tif)"))
        self.lineEdit_gt.setText(str)
        dir = QFileInfo(str).path()
        # QDir.setCurrent(dir)


    def slot_select_mask_file(self):
        str, _ = QFileDialog.getOpenFileName(self, "Select mask file", '../../data/', self.tr("mask(*.png *.tif)"))
        self.lineEdit_mask.setText(str)
        tp_dir = QFileInfo(str).path()
        # QDir.setCurrent(tp_dir)


    def slot_ok(self):
        self.setWindowModality(Qt.ApplicationModal)
        # self.send("Begin")
        self.buttonBox.setEnabled(False)
        input_dict = accEvaluate_dict
        input_dict['gt_file'] = self.lineEdit_gt.text()
        input_dict['mask_file'] = self.lineEdit_mask.text()
        min = self.spinBox_min.value()
        max = self.spinBox_max.value()
        input_dict['valid_values'] = list(range(min, max+1))
        input_dict['check_rate'] = self.doubleSpinBox_rate.value()
        # input_dict['GPUID'] = self.comboBox_gupid.currentText()
        ret =-1
        ret = accuracy_evalute(self.send,input_dict)

        if ret == 0:
            QMessageBox.information(self, "Prompt", self.tr("successfully!"))
        self.buttonBox.setEnabled(True)
        self.setWindowModality(Qt.NonModal)

class child_removesmallobject(QDialog, Ui_Dialog_removeSmallPolygon,base_message):
    def __init__(self):
        super(child_removesmallobject, self).__init__()
        self.setupUi(self)
        self.new_translate()

    def new_translate(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("removeSmallArea", " 去除与填补小面"))
        self.label.setText(_translate("input_dir", "输入路径"))
        self.label_3.setText(_translate("output_dir", "输出路径"))
        self.label_4.setText(_translate("method", "方法"))
        self.label_2.setText(_translate("minsize", "去除小面尺寸"))
        self.label_5.setText(_translate("threshold", "填补小面阈值"))


    def slot_select_inputdir(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_inputdir.setText(dir_tmp)
    def slot_select_outputdir(self):
        dir_tmp = QFileDialog.getExistingDirectory(self, "select a existing directory", '../../data/')
        self.lineEdit_outputdir.setText(dir_tmp)
    def slot_ok(self):
        in_dir = self.lineEdit_inputdir.text()
        ou_dir = self.lineEdit_outputdir.text()
        flag=False
        if self.checkBox_flag.isChecked():
            flag=True
        min_size = self.spinBox_ms.value()
        threshold=self.spinBox_thd.value()
        self.buttonBox.setEnabled(False)
        try:
            batch_rmovesmallobj(self.send,in_dir,ou_dir,flag_cv=flag,msize=min_size, thd=threshold)
            QMessageBox.information(self, '提示', "Finished")
        except:
            QMessageBox.information(self, '提示', "Error occurred")
        finally:
            self.buttonBox.setEnabled(True)
        # print(in_dir + "\n" +ou_dir + "\n"+ scale_factor)
