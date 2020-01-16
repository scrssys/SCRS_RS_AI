#coding:utf-8

import os,sys
try:
    from osgeo import ogr, osr, gdal
    gdal.UseExceptions()
except:
    sys.exit('ERROR: cannot find GDAL/OGR modules')

import numpy as np

variable_str='3_13'

input_files =['/home/omnisky/PycharmProjects/data/samples/isprs/4_Ortho_RGBIR/top_potsdam_{}_RGBIR.tif'.format(variable_str),
              '/home/omnisky/PycharmProjects/data/samples/isprs/1_DSM_normalisation/1_DSM_normalisation/dsm_potsdam_0{}_normalized_lastools.jpg'.format(variable_str)]
output_file = '/home/omnisky/PycharmProjects/data/samples/isprs/train/src/top_potsdam_{}.tif'.format(variable_str)

if __name__=="__main__":
    if not os.path.isfile(input_files[0]):
        print("File does not exist:{}".format(input_files[0]))
        sys.exit(-1)

    try:
        dataset=gdal.Open(input_files[0])
    except RuntimeError:
        print("Could not open file:{}".format(input_files[0]))
    finally:
        print("Input file could be opened!")

    x=dataset.RasterXSize
    y=dataset.RasterYSize
    d_type = dataset.GetRasterBand(1).DataType
    # print(dataset.GetMetadata())
    dataset = None
    # del dataset

    """
    Extract data from each images, and combine to output file
    """
    out_data=[]
    for file in input_files:
        if not os.path.isfile(file):
            print("file does not exist:{}".format(file))
            sys.exit(-2)
        print("Extract data from :{}".format(file))

        try:
            dataset = gdal.Open(file)
        except RuntimeError:
            print("Could not open file:{}".format(file))
        finally:
            print("Input file could be opened!")

        width = dataset.RasterXSize
        height=dataset.RasterYSize
        if x!=width or y!=height:
            print("Error: input files have different width and height\n")
            sys.exit(-4)
        im_band = dataset.RasterCount
        im_type = dataset.GetRasterBand(1).DataType
        if d_type != im_type:
            print("Error: data types are not the same!\n")
            sys.exit(-5)
        for index in range(im_band):
            # banddatarater=dataset.GetRasterBand(index)
            tmp=dataset.GetRasterBand(index+1).ReadAsArray(0,0,width,height)
            out_data.append(tmp)

        dataset=None
        # del dataset

    out_data = np.array(out_data)
    res_band,_,_ = out_data.shape
    if (res_band<2):
        print("The number of input-image bands is less than 2! ")
        sys.exit(-3)
    out_driver=gdal.GetDriverByName("GTiff")
    out_dataset=out_driver.Create(output_file, x, y, res_band, d_type)
    for i in range(res_band):
        out_dataset.GetRasterBand(i+1).WriteArray(out_data[i])

    print("Saved to: {}".format(output_file))

    del out_dataset




