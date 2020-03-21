import matplotlib,gdal,os,sys
import numpy as np
gdal.UseExceptions()
matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QFileDialog,QMessageBox
class MyFigure(FigureCanvas):
    def __init__(self, dpi=100):
        self.fig = Figure(dpi=dpi)
        super(MyFigure,self).__init__(self.fig)
        self.axes = self.fig.add_subplot(111)
    def plotdesrt(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Select image', '../../data/', self.tr("Image(*.png *.jpg *.tif)"))
        if not os.path.isfile(file):
            QMessageBox.warning(self, "Warning", 'Please select a raster image file!')
            # sys.exit(-1)
        else:
            dataset = gdal.Open(file)
            if dataset == None:
                QMessageBox.warning(self, "Warning", 'Open file failed!')
                sys.exit(-2)
        try:
            dataset = gdal.Open(file)
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