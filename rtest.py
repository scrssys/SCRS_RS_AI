import os

# import gdal

# from qgis.core import *
# from qgis.core import QgsProject
# project = QgsProject.instance()
# 打印当前项目的文件名（可能为空，因为没有项目加载）
# print(project.fileName())
'/home/user/projects/my_qgis_project.qgs'
# 加载另一个项目
# project.read('/home/user/projects/my_other_qgis_project.qgs')
# print(project.fileName())
import os
import sys
from qgis.core import (
QgsVectorLayer,
QgsRasterLayer,
)

from qgis.gui import (
QgsMapCanvas
)

canvas = QgsMapCanvas()
canvas.show()
sys.exit(-2)
# 如果你不在QGIS控制台内运行，首先需要导入qgis和PyQt类，如下所示：
from qgis.core import QgsProject
# 获取项目实例
project = QgsProject.instance()
# 打印当前项目的文件名（可能为空，因为没有项目加载）
print(project.fileName())
print(QgsProject.instance().homePath())

project.read('/home/omnisky/Desktop/test.qgs')
print(project.fileName())
print(QgsProject.instance().homePath())
# sys.exit(-1)
# 获取shapefile的路径，例如：/home/project/data/ports.shp
path_to_ports_layer = os.path.join(QgsProject.instance().homePath(), "data", "ports.shp")
# 格式为：
# vlayer = QgsVectorLayer(data_source, layer_name, provider_name)
vlayer = QgsVectorLayer(path_to_ports_layer, "Ports layer", "ogr")
if not vlayer.isValid():
    print("图层加载失败！")

# 获取tif文件的路径，例如：/home/project/data/srtm.tif
path_to_tif = os.path.join(QgsProject.instance().homePath(), "data", "zy304016420151108.tif")
if os.path.isfile(path_to_tif):
    rlayer = QgsRasterLayer(path_to_tif, "SRTM layer name")
    if not rlayer.isValid():
        print("图层加载失败！")
# path_to_ports_layer='/home/omnisky/PycharmProjects/data/test/paper/2019-06-14_16-28-01/cuiping_4bands1024.shp'
# vlayer = QgsVectorLayer(path_to_ports_layer, "Ports layer", "ogr")
# if not vlayer.isValid():
#     print("loading layers failed\n")
#
# print("test fork")
