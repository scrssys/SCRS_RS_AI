import os,sys
import fire
try:
    from osgeo import ogr, osr, gdal
    gdal.UseExceptions()
except:
    sys.exit('ERROR: cannot find GDAL/OGR modules')

import numpy as np
from ulitities.base_functions import get_file
input_dir ='/home/omnisky/PycharmProjects/data/tree/ori-isprs/src_5bands'
output_dir ='/home/omnisky/PycharmProjects/data/tree/ori-isprs/src'
bands=[0,1,2,3]

def band_extract(infile, out, bandlist=[0]):
    if os.path.isfile(infile) or os.path.isdir(infile):
        print("input is correct")
    else:
        print("Error:input is not a file or dir")
        return -1

    if not os.path.isdir(out):
        print("Warning: output dir is not exist,it will be created automatically!")
        os.mkdir(out)

    filelist=[]
    if os.path.isfile(infile):
        filelist.append(infile)

    elif os.path.isdir(infile):
        files,_=get_file(infile)
        for file in files:
            filelist.append(file)

    for file in filelist:
        # file=filelist[s]
        try:
            dataset = gdal.Open(file)
        except:
            print("gdal loading label also failed")
            return -2

        y_height = dataset.RasterYSize
        x_width = dataset.RasterXSize
        im_bands = dataset.RasterCount
        im_type = dataset.GetRasterBand(1).DataType
        img = dataset.ReadAsArray(0, 0, x_width, y_height)
        img = np.transpose(img,(1,2,0))
        del dataset
        if len(bandlist) == 0:
            print("bandlist is empty")
            return -3
        if len(bandlist) > im_bands or max(bandlist) >= im_bands:
            print("input bands should not be bigger than image bands!")
            # sys.exit(-2)
            return -4
        # outimg=np.zeros((y_height,x_width,len(bandlist)),np.uint16)
        # for i in bandlist:
        #     outimg[:,:,i]=img[:,:,bandlist[i]]

        absname = os.path.split(file)[1]
        outputfile = os.path.join(out, absname)
        driver = gdal.GetDriverByName("GTiff")
        outdataset = driver.Create(outputfile, x_width, y_height, len(bandlist), im_type)
        if outdataset == None:
            print("create dataset failed!\n")
            sys.exit(-2)
        if len(bandlist) == 1:
            outdataset.GetRasterBand(1).WriteArray(img[:,:,bandlist[0]])
        else:
            for i in range(len(bandlist)):
                outdataset.GetRasterBand(i + 1).WriteArray(img[:,:,bandlist[i]])
        del outdataset



    return 0

if __name__=="__main__":


    band_extract(input_dir, output_dir, bandlist=bands)

    fire.Fire()

