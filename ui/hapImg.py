
from qgis.gui import *
from qgis.core import *

class HapImg(QgsMapCanvas):
    def __init__(self, canvas):
        # super(HapImg,self).__init__(self)
        self.canvas=canvas
        # pass

    def load(self,file):
            QgsApplication.setPrefixPath('/usr/local/', True)
            qgs = QgsApplication([], True)
            qgs.initQgis()
            reg = QgsProject.instance()
            # fileInfo = QFileInfo(file)
            # baseName = fileInfo.baseName()
            # canvas=QgsMapCanvas()
            rlayer = QgsRasterLayer(file, 'test')
            print(file)
            if not rlayer.isValid():
                print("图层加载失败！")
            else:
                print("in hapimg")
                reg.addMapLayer(rlayer)

                # set extent to the extent of our layer
                self.canvas.setExtent(rlayer.extent())

                # set the map canvas layer set
                self.canvas.setLayers([rlayer])

                # self.canvas.refreshAllLayers()
                # self.canvas.setCurrentLayer(QgsMapLayer[rlayer])
                self.canvas.show()
                # return 0

                # self.canvas.exec()
            qgs.exec_()
            # qgs.quit()
            # qgs.exitQgis()