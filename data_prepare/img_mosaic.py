
import os, sys
import matplotlib.pyplot as plt
import numpy as np

import gdal
gdal.UseExceptions()

from ulitities.base_functions import get_file, load_img_by_gdal_info

input_dir = '/media/omnisky/e0331d4a-a3ea-4c31-90ab-41f5b0ee2663/traindata/scrs_building/test/8bits/'
img_list=['cuiping.png','jiangyou.png','tongchuan.png','jian.png','shuangliu.png','yujiang.png']
output_file='/media/omnisky/e0331d4a-a3ea-4c31-90ab-41f5b0ee2663/traindata/scrs_building/test/whole_img.tif'

if __name__=="__main__":

    # file_list,_ = get_file(input_dir)
    # if len(file_list)==0:
    #     print("Error: no image files ")
    #     sys.exit(-1)
    W=0
    H=0
    B=0
    T=1
    # H,W,B,_,_=load_img_by_gdal_info(file_list[0])
    try:
        dataset = gdal.Open(input_dir+img_list[0])
    except:
        print("Warning: can not open file {}".format(input_dir+img_list[0]))
        sys.exit(-2)
    else:
        print("Opening file: {}".format(input_dir+img_list[0]))

    W = dataset.RasterXSize
    H = dataset.RasterYSize
    B = dataset.RasterCount
    T = dataset.GetRasterBand(1).DataType
    del dataset

    for file in img_list[1:]:
        try:
            dataset = gdal.Open(input_dir+file)
        except:
            print("Warning: can not open file {}".format(input_dir+file))
            continue
        else:
            print("Opening file: {}".format(input_dir+file))

        x_width = dataset.RasterXSize
        W += x_width
        y_height = dataset.RasterYSize
        if y_height> H:
            H=y_height
        im_bands = dataset.RasterCount
        if im_bands != B:
            print("Error: img file has different bands in {}".format(input_dir+file))
            sys.exit(-3)
        data_type = dataset.GetRasterBand(1).DataType
        if T != data_type:
            print("Error: img file has different data tpye in {}".format(input_dir+file))
            sys.exit(-4)
        del dataset

    print("W:{},H:{},B:{},T:{}".format(W,H,B,T))


    out_img = np.zeros((H,W,B), np.uint16)
    x_off=0
    for file in img_list:
        try:
            dataset = gdal.Open(input_dir+file)
        except:
            print("Warning: can not open file {}".format(input_dir+file))
            sys.exit(-2)
        else:
            print("Opening file: {}".format(input_dir+file))

        x_width = dataset.RasterXSize

        y_height = dataset.RasterYSize

        img = dataset.ReadAsArray(0,0,x_width, y_height)

        img = np.transpose(img, (1,2,0))

        del dataset
        if B==1:
            out_img[0:y_height, x_off:x_off + x_width, 0] = img[0:y_height, 0:x_width]
        else:
            for i in range(B):
                out_img[0:y_height, x_off:x_off+x_width, i] = img[0:y_height, 0:x_width, i]

        x_off += x_width
        print("dsfds")
    plt.imshow(out_img[:,:,0])
    plt.show()

    driver = gdal.GetDriverByName("GTiff")
    outdataset = driver.Create(output_file, W, H, B, T)

    for i in range(B):
        outdataset.GetRasterBand(i + 1).WriteArray(out_img[:,:,i])

    del outdataset









