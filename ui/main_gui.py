from ui.MainWin import Ui_MainWindow
from ui.sampleProduce.sampleProcess_implements import*
from ui.preProcess.preprocess_implements import *
from ui.postProcess.postProcess_implements import *
from ui.classification.classification_implements import *
from ui.train.Train_implement import *
from ui.about import Ui_Dialog_about
from ui.open import MyFigure

import platform
sysinfo=platform.system()
if sysinfo=='Linux':
    from qgis.gui import QgsMapCanvas
    from qgis.core import QgsMapLayer,QgsRasterLayer,QgsProject,QgsDataSourceUri


class mywindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mywindow,self).__init__()
        self.move(300,300)
        self.setWindowTitle(self.tr('Image'))
        self.setWindowIcon(QIcon('else/scrslogo.png'))
        self.setupUi(self)
        self.new_translate()
        self.setFont(QFont('SansSerif',12))
        self.newlay = QGridLayout(self.centralwidget)
        self.canvas = QgsMapCanvas()
        self.canvas.setCanvasColor(Qt.red)
        # canvas.show()
        # self.newlay.addWidget(self.canvas,0,0)
        self.newlay.addWidget(self.dockWidget_4,0,0)
        self.doc = QGridLayout(self.dockWidgetContents_4)
        self.newlay.addWidget(self.tabWidget, 1, 0)


    def new_translate(self ):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "    自然资源督察要素遥感识别监测系统"))
        self.menuFile.setTitle(_translate("MainWindow", "文件"))
        self.menuPrepocess.setTitle(_translate("MainWindow", "预处理"))
        self.menuTrain.setTitle(_translate("MainWindow", "模型训练"))
        self.menuClassify.setTitle(_translate("MainWindow", "分类识别"))
        self.menuHelp.setTitle(_translate("MainWindow", "帮助"))
        self.menuSampleProduce.setTitle(_translate("MainWindow", "数据集"))
        self.menuPostproc.setTitle(_translate("MainWindow", "后处理"))
        self.actionLabel_check.setText(_translate("MainWindow", "标注检查"))
        self.actionImage_strech.setText(_translate("MainWindow", "图像标准化"))
        self.actionconvert_8bit.setText(_translate("MainWindow", "图像转8位"))
        self.actionlabel_crop.setText(_translate("MainWindow", "样本裁切"))
        self.actionSampleGenCommon.setText(_translate("MainWindow", "样本制作(默认)"))
        self.actionSample_gen_Self_adapt.setText(_translate("MainWindow", "样本制作(自适应)"))
        self.actionSampleGenByCV2.setText(_translate("MainWindow", "SampleGenByCV2"))
        self.actionImage_Clip.setText(_translate("MainWindow", "图像裁剪"))
        self.actionMismatch_Analyze.setText(_translate("MainWindow", "Mismatch Analyze"))
        # self.actionTrain_Binary_Jaccard.setText(_translate("MainWindow", "二分类模型（Jaccard相似度）"))
        # self.actionTrain_Binary_JaccCross.setText(_translate("MainWindow", "二分类模型（相似度&交叉熵）"))
        # self.actionTrain_Binary_Cross_entropy.setText(_translate("MainWindow", "二分类模型（交叉熵）"))
        # self.actionTrain_Multiclass.setText(_translate("MainWindow", "多分类模型"))
        # self.actionTrain_Binary_Onehot_Cross.setText(_translate("MainWindow", "二分类模型（Onehot编码）"))
        # self.actionPredict_Binary_Single.setText(_translate("MainWindow", "二分类预测"))
        # self.actionPredict_Multiclass_Single.setText(_translate("MainWindow", "多分类预测"))
        # self.actionPredict_Binary_Batch.setText(_translate("MainWindow", "二分类批处理"))
        self.actionPredict.setText(_translate("MainWindow", "分类"))
        self.actionAbout.setText(_translate("MainWindow", "关于"))
        self.actionOpen.setText(_translate("MainWindow", "影像打开"))
        self.actionExit.setText(_translate("MainWindow", "退出"))
        self.actionCombineSingleModelReults.setText(_translate("MainWindow", "多类别合成"))
        self.action_VoteMultiModelResults.setText(_translate("MainWindow", "多模型集成"))
        self.actionAccuracyEvaluation.setText(_translate("MainWindow", "精度评估"))
        self.actionBinarization.setText(_translate("MainWindow", "掩膜二值化"))
        self.action_Train.setText(_translate("MainWindow", "训练"))
        self.actionremove_small_object.setText(_translate("MainWindow","消除小面"))
        self.actionRasterToPolygon.setText(_translate("MainWindow","栅格转矢量"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "输出"))
        # self.actionPredictOne.setText(_translate("MainWindow", "分类"))

    if sysinfo=='Linux':
        def slot_open_show_qgis(self):
            file, _ = QFileDialog.getOpenFileName(self, 'Select image', '../../data/', self.tr("Image(*.png *.jpg *.tif)"))
            if not os.path.isfile(file):
                QMessageBox.warning(self, "Warning", 'Please select a raster image file!')
                # sys.exit(-1)
            else:
                # data=cv2.imread(file)
                # pRasterLayer = QgsRasterLayer(file,'raster','true')
                # path_to_tif = os.path.join(zy304016420151108.tif")
                if os.path.isfile(file):
                    reg=QgsProject.instance()
                    file='/home/omnisky/Desktop/data/scale0ingdal23.tif'
                    fileInfo = QFileInfo(file)
                    baseName = fileInfo.baseName()
                    rlayer = QgsRasterLayer(file, baseName)
                    print(file)
                    # rlayer = QgsRasterLayer(file, "chb_gaofen", "gdal")
                    # layer_name = 'modis'
                    # uri = QgsDataSourceUri()
                    # uri.setParam('url', 'http://demo.mapserver.org/cgi-bin/wcs')
                    # uri.setParam("identifier", layer_name)
                    # rlayer = QgsRasterLayer(str(uri.encodedUri()), 'my wcs layer', 'wcs')
                    if not rlayer.isValid():
                        print("图层加载失败！")
                    else:
                        reg.addMapLayer(rlayer)

                        # set extent to the extent of our layer
                        self.canvas.setExtent(rlayer.extent())

                        # set the map canvas layer set
                        self.canvas.setLayerSet([QgsMapLayer(rlayer)])


    def slot_open_show(self):
        self.F = MyFigure( dpi=100)
        self.F.plotdesrt()
        # self.doc = QGridLayout(self.dockWidgetContents_4)
        self.doc.addWidget(self.F, 0, 1)

    def slot_predict_one(self):
        child = child_predict_one()
        child.show()
        child.exec()

    def slot_predict(self):
        child = child_predict()
        child.show()
        child.exec()

    def slot_train(self):
        child = child_train()
        child.show()
        child.exec()


    def slot_action_rasterToPolygon(self):
        child =child_raster_to_polygon()
        child.show()
        child.exec_()


    def slot_action_sampleGenSelfAdapt(self):
        child = child_sampleGenSelfAdapt()
        child.show()
        child.exec_()


    def slot_action_binarization(self):
        child = child_Binarization()
        child.show()
        child.exec_()

    def for_action_label_check(self):
        child = child_label()
        child.show()
        child.exec_()

    def for_action_image_stretch(self):
        child = child_image_stretch()
        child.show()
        child.exec_()

    def slot_actiong_image_clip(self):
        child = child_ImageClip()
        child.show()
        child.exec_()

    def slot_action_convert8bit(self):
        child = child_convert_8bit()
        child.show()
        child.exec_()

    def slot_action_samplecrop(self):
        child = child_samplecrop()
        child.show()
        child.exec_()

    def slot_action_sampleGenCommon(self):
        child = child_sampleGenCommon()
        child.show()
        child.exec_()

    def slot_action_trainBinaryJaccCross(self):
        child = child_trainBinaryJaccardCross()
        child.show()
        child.exec_()

    def slot_action_trainBinaryOnehot(self):
        child = child_trainBinaryOnehot()
        child.show()
        child.exec_()

    def slot_action_trainBinaryJaccard(self):
        child = child_trainBinaryJaccardOnly()
        child.show()
        child.exec_()

    def slot_action_trainBinaryCrossentropy(self):
        child = child_trainBinaryCrossentropy()
        child.show()
        child.exec_()

    def slot_action_trainBinaryNew(self):
        child = child_trainBinaryCommon()
        child.show()
        child.exec_()


    def slot_action_trainMulticlass(self):
        child = child_trainMulticlass()
        child.show()
        child.exec_()

    def slot_action_predictBinarySingleImg(self):
        child = child_predictBinaryForSingleImage()
        child.show()
        child.exec_()

    def slot_action_predictMulticlassSingleImg(self):
        child = child_predictMulticlassForSingleImage()
        child.show()
        child.exec_()

    def slot_action_predictBinaryBatch(self):
        child = child_predictBinaryBatch()
        child.show()
        child.exec_()

    def slot_action_predictMulticlassBatch(self):
        child = child_predictMulticlassBatch()
        child.show()
        child.exec_()

    def slot_action_combineMulticlassFromSingleModel(self):
        child = child_CombineMulticlassFromSingleModelResults()
        child.show()
        child.exec_()

    def slot_action_VoteMultimodleResults(self):
        child = child_VoteMultimodleResults()
        child.show()
        child.exec_()

    def slot_action_accuracyEvaluate(self):
        child = child_AccuacyEvaluate()
        child.show()
        child.exec_()

    def slot_action_removesmallobject(self):
        child = child_removesmallobject()
        child.show()
        child.exec_()

    def slot_action_about(self):
        child = child_abount()
        child.show()
        child.exec_()





class child_abount(QDialog, Ui_Dialog_about):
    def __init__(self):
        super(child_abount, self).__init__()
        self.setupUi(self)


if __name__=='__main__':
    import sys
    app=QApplication(sys.argv)
    widget=mywindow()
    # widget = child_label()
    widget.show()
    sys.exit(app.exec_())
