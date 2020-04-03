import os, sys,subprocess, fire
import numpy as np
from tqdm import tqdm
from ulitities.base_functions import get_file,echoRuntime,send_message_callback


@echoRuntime
def convert_to_8Bit_percentclip(inputRaster, outputRaster,
                    outputDataType='Byte',
                    outputFormat='GTiff',
                    stretch_type='rescale',
                     nodata=65535,
                    percentiles=[1, 99]):
    '''
    Convert 16bit image to 8bit
    rescale_type = [clip, rescale]
        if clip, scaling is done strictly between 0 65535
        if rescale, each band is rescaled to a min and max
        set by percentiles
    '''
    from osgeo import gdal
    srcRaster = gdal.Open(inputRaster)
    # iterate through bands
    height = srcRaster.RasterYSize
    width = srcRaster.RasterXSize
    im_bands = srcRaster.RasterCount

    geotransform = srcRaster.GetGeoTransform()
    # del srcRaster
    result = []
    for bandId in range(srcRaster.RasterCount):
        bandId = bandId + 1
        band = srcRaster.GetRasterBand(bandId)
        # band.SetNoDataValue ( -333 )
        if stretch_type == 'rescale':
            band.SetNoDataValue(nodata)

            bmin = band.GetMinimum()
            bmax = band.GetMaximum()
            # if not exist minimum and maximum values
            if bmin is None or bmax is None:
                (bmin, bmax) = band.ComputeRasterMinMax(1)
            band_arr_tmp = band.ReadAsArray()

            index = np.where(band_arr_tmp==nodata)
            new_data = np.asarray(band_arr_tmp, dtype=np.float)
            new_data[index]=np.nan
            bmin = np.nanpercentile(new_data.flatten(),
                                 percentiles[0])
            bmax = np.nanpercentile(new_data.flatten(),
                                 percentiles[1])
        elif isinstance(stretch_type, dict):
            bmin, bmax = stretch_type[bandId]
        else:
            bmin, bmax = 0, 65535

        temp = 255.0*(new_data-bmin)/(bmax-bmin+0.000001)
        temp[temp<0.00001]=0
        temp[temp>253.99999]=254
        temp[index]=255
        result.append(temp)
        # plt.imshow(temp, cmap='gray')
        # plt.show()

    driver = gdal.GetDriverByName("GTiff")
    outdataset = driver.Create(outputRaster, width, height, im_bands, gdal.GDT_Byte)
    outdataset.SetGeoTransform(geotransform)
    for i in range(im_bands):
        outdataset.GetRasterBand(i + 1).WriteArray(result[i])

    del outdataset

def convert_8bit_minMaxium():
    pass
def convert_8bit_standdeivtion():
    pass
def convert_8bit_histspecification():
    pass


def batch_convert_8bit(send_massage_callback,inputdir,outputdir):
    if not os.path.isdir(inputdir):
        send_massage_callback("Please check input directory:{}".format(inputdir))

    if not os.path.isdir(outputdir):
        send_massage_callback('Warning: output directory is not existed')
        try:
            os.mkdir(outputdir)
        except:
            pass
    files,_=get_file(inputdir)
    # print(files)
    for file in files:#tqdm(files):
        send_massage_callback("Converting : " + file)
        print("\ndealing with : " + file)
        absname = os.path.split(file)[1]
        outputfile = os.path.join(outputdir,absname)
        convert_to_8Bit_percentclip(file,outputfile)
        # convert_to_8Bit_percentclip(file, outputfile,
        #                  outputDataType='Byte',
        #                  stretch_type='rescale',
        #                  nodata=65535,
        #                  percentiles=[1, 99.8])

if __name__=='__main__':
    fire.Fire()



