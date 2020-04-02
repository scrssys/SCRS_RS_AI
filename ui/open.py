import matplotlib,gdal,os,sys
import numpy as np
gdal.UseExceptions()
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import QFileInfo,QEventLoop
from PyQt5.QtWidgets import QFileDialog,QMessageBox
class matplot_Figure(FigureCanvas):
    """
    use matplotlib for add figure convas to qtwidget
    """

    def __init__(self, dpi=100,file="e"):
        self.fig = Figure(dpi=dpi)
        super(matplot_Figure,self).__init__(self.fig)
        self.file = file
        self.axes = self.fig.add_subplot(111)
    def plotdesrt(self):
        # file, _ = QFileDialog.getOpenFileName(self, 'Select image', '../../data/', self.tr("Image(*.png *.jpg *.tif)"))
        if not 1:#os.path.isfile(file):
            QMessageBox.warning(self, "Warning", 'Please select a raster image file!')
            # sys.exit(-1)
        else:
            dataset = gdal.Open(self.file)
            if dataset == None:
                QMessageBox.warning(self, "Warning", 'Open file failed!')
                sys.exit(-2)
        try:
            dataset = gdal.Open(self.file)
        except:
            print("can not open file\n")
            return -1
        im_band = dataset.RasterCount
        height = dataset.RasterYSize
        width = dataset.RasterXSize
        data = dataset.ReadAsArray(0,0,width,height)
        data = np.array(data)
        data = data.transpose((1, 2, 0))
        if im_band == 1:
            QMessageBox.warning(self, "Warning", 'only one band')
            self.axes.imshow(data,"gray")
        elif im_band == 3:
            # data = data.transpose((0, 1, 2))
            self.axes.imshow(data)
        elif im_band > 3:
            # data = data.transpose((0, 1, 2))
            img = data[:, :, :3]
            self.axes.imshow(img)
        else:
            # data = data.transpose((1, 2, 0))
            img = data[:, :, :0]
            self.axes.imshow(data)
        return 0

import platform
sysinfo = platform.system()
if sysinfo == 'Linux':
    from qgis.gui import QgsMapCanvas
    from qgis.core import QgsMapLayer, QgsRasterLayer, QgsProject, QgsDataSourceUri, QgsApplication


def canvas():
    pass
def qgis_plot(canvas,file):
    """
    use qgis map canvas to plot raster or vector
    :param canvas: qt canvas
    :param file: image file
    :return:
    """
    if os.path.isfile(file):
        QgsApplication.setPrefixPath('/usr/local/', True)
        qgs = QgsApplication([], True)
        qgs.initQgis()
        reg = QgsProject.instance()

        fileInfo = QFileInfo(file)
        baseName = fileInfo.baseName()
        rlayer = QgsRasterLayer(file, baseName)
        print("Raster:" + file)
        if not rlayer.isValid():
            print("图层加载失败！")
            # current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            # self.OutputWritten(current_time + "Fialed on Opened: " + file + "\n")
        else:
            # current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            # self.OutputWritten(current_time + " Opened: " + file + "\n")
            reg.addMapLayer(rlayer)
            # set extent to the extent of our layer
            canvas.setExtent(rlayer.extent())
            # set the map canvas layer set
            canvas.setLayers([rlayer])
            canvas.show()
        mloop = QEventLoop()
        canvas.extentsChanged.connect(mloop.exec())