import os, sys,subprocess, fire
import numpy as np
from tqdm import tqdm
from ulitities.base_functions import get_file,echoRuntime,send_message_callback,geotrans_match
import gdal
gdal.UseExceptions()
gdal.SetCacheMax(1000000000000)

@echoRuntime
def convert_to_8Bit_percentclip(inputRaster, outputRaster,
                    outputDataType='Byte',
                    outputFormat='GTiff',
                    stretch_type='rescale',
                     nodata=65535,
                    percentiles=[0.5, 99.75]):
    '''
    Convert 16bit image to 8bit
    rescale_type = [clip, rescale]
        if clip, scaling is done strictly between 0 65535
        if rescale, each band is rescaled to a min and max
        set by percentiles
    '''
    # from osgeo import gdal
    try:
        srcRaster = gdal.Open(inputRaster)
    except:
        print("Opening file failed:{}".format(inputRaster))
        return
    # iterate through bands
    height = srcRaster.RasterYSize
    width = srcRaster.RasterXSize
    im_bands = srcRaster.RasterCount

    geotransform = srcRaster.GetGeoTransform()
    projinf = srcRaster.GetProjectionRef()
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
            new_data = np.asarray(band_arr_tmp, dtype=np.float32)
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
        temp=np.asarray(temp,np.uint8)
        result.append(temp)
        # plt.imshow(temp, cmap='gray')
        # plt.show()

    driver = gdal.GetDriverByName("GTiff")
    outdataset = driver.Create(outputRaster, width, height, im_bands, gdal.GDT_Byte)
    outdataset.SetGeoTransform(geotransform)
    outdataset.SetProjection(projinf)
    for i in range(im_bands):
        outdataset.GetRasterBand(i + 1).WriteArray(result[i])

    del outdataset

def convert_8bit_minMaxium(inputRaster, outputRaster, nodata=65535):
    # from osgeo import gdal
    try:
        srcRaster = gdal.Open(inputRaster)
    except:
        print("Opening file failed:{}".format(inputRaster))
        return -1
    # iterate through bands
    height = srcRaster.RasterYSize
    width = srcRaster.RasterXSize
    im_bands = srcRaster.RasterCount
    geotransform = srcRaster.GetGeoTransform()
    projinf = srcRaster.GetProjectionRef()
    result = []
    for bandId in range(srcRaster.RasterCount):
        bandId = bandId + 1
        band = srcRaster.GetRasterBand(bandId)
        # band.SetNoDataValue ( -333 )
        band.SetNoDataValue(nodata)
        bmin = band.GetMinimum()
        bmax = band.GetMaximum()
        # if not exist minimum and maximum values
        if bmin is None or bmax is None:
            (bmin, bmax) = band.ComputeRasterMinMax(1)
        band_arr_tmp = band.ReadAsArray()
        if band_arr_tmp is None:
            band_arr_tmp = srcRaster.ReadRaster1(0, 0, width, height)
            print("load image failed")
            return -2

        index = np.where(band_arr_tmp == nodata)
        new_data = np.asarray(band_arr_tmp, dtype=np.float32)
        if len(index)<2:
            print("no nodata")
            bmin = new_data.min()
            bmax=new_data.max()
            # continue
        else:
            # mmmm =np.min(new_data)
            new_data[index] = np.nan
            t_min = np.nanargmin(new_data)
            t_max=np.nanargmax(new_data)
            bmin= (new_data.flatten())[t_min]
            bmax=(new_data.flatten())[t_max]

        temp = 254.0 * (new_data - bmin) / (bmax - bmin + 0.000001)
        temp[temp < 0.00001] = 0
        temp[temp > 253.99999] = 254
        # temp[index] = 255
        temp = np.asarray(temp, np.uint8)
        temp[index] = 255
        result.append(temp)
        # plt.imshow(temp, cmap='gray')
        # plt.show()

    driver = gdal.GetDriverByName("GTiff")
    outdataset = driver.Create(outputRaster, width, height, im_bands, gdal.GDT_Byte)
    outdataset.SetGeoTransform(geotransform)
    outdataset.SetProjection(projinf)
    for i in range(im_bands):
        outdataset.GetRasterBand(i + 1).WriteArray(result[i])
    del outdataset

####分块转换
def convert_8bit_minMaxium_blocks(inputRaster, outputRaster, nodata=65535,block_h=10000):
    # from osgeo import gdal
    try:
        srcRaster = gdal.Open(inputRaster)
    except:
        print("Opening file failed:{}".format(inputRaster))
        return -1
    # iterate through bands
    height = srcRaster.RasterYSize
    if block_h > height:
        print("Warnin:block height is gt image height")
        bk_h=height
        # return -2
    width = srcRaster.RasterXSize
    im_bands = srcRaster.RasterCount
    geotransform = srcRaster.GetGeoTransform()
    projinf = srcRaster.GetProjectionRef()
    # result = []
    all_mins=np.zeros(im_bands,np.float32)
    all_maxs = np.zeros(im_bands, np.float32)
    ###创建输出数据
    try:
        driver = gdal.GetDriverByName("GTiff")
        outdataset = driver.Create(outputRaster, width, height, im_bands, gdal.GDT_Byte)
    except:
        print("Error: output raster is existed or can not be opened:\n {}".format(outputRaster))
        return -3
    outdataset.SetGeoTransform(geotransform)
    outdataset.SetProjection(projinf)

    for i in range(im_bands):
        bandId = i + 1
        band = srcRaster.GetRasterBand(bandId)
        bmin = band.GetMinimum()
        bmax = band.GetMaximum()
        # if not exist minimum and maximum values
        if bmin is None or bmax is None:
            (bmin, bmax) = band.ComputeRasterMinMax(1)
        all_mins[i] = bmin
        all_maxs[i] = bmax
    n_blocks = 1
    if height % bk_h == 0:
        n_blocks = int(height / bk_h)
    else:
        n_blocks = int(height / bk_h) + 1

    # real_b = min(im_bands, bands)
    for index_block in range(n_blocks):
        start_y = index_block * bk_h
        y_block_height = bk_h
        if index_block == n_blocks - 1:
            y_block_height = height - start_y
        img = srcRaster.ReadAsArray(0, start_y, width, y_block_height)
        img = np.transpose(img, (1, 2, 0))

        # for index_band in range(im_bands):

        for i in range(im_bands):
            index = np.where(img[:,:,i] == nodata)
            t_img = np.asarray(img[:,:,i], dtype=np.float32)
            temp = np.zeros(t_img.shape, np.float32)
            temp[:,:] = 254.0 * (t_img[:,:] - all_mins[i]) / (all_maxs[i] - all_mins[i] + 0.000001)
            temp[temp < 0.00001] = 0
            temp[temp > 253.99999] = 254
            temp[index] = 255
            temp = np.asarray(temp, np.uint8)
            outdataset.GetRasterBand(i + 1).WriteArray(temp,xoff=0,yoff=start_y)

    del srcRaster
    del outdataset




def convert_8bit_standdeivtion():
    pass
def convert_8bit_histspecification():
    pass


def batch_convert_8bit(send_massage_callback=send_message_callback,inputdir="",outputdir="", nodata=65535):
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
        if os.path.isfile(outputfile):
            print("This image has been converted:{}".format(outputfile))
            continue
        convert_to_8Bit_percentclip(file,outputfile, nodata)
        # convert_to_8Bit_percentclip(file, outputfile,
        #                  outputDataType='Byte',
        #                  stretch_type='rescale',
        #                  nodata=65535,
        #                  percentiles=[1, 99.8])
def batch_convert_8bit_minmax(send_massage_callback=send_message_callback,inputdir="",outputdir="",nd =65535,bk_h=10000):
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
        if os.path.isfile(outputfile):
            print("This image has been converted:{}".format(outputfile))
            continue
        convert_8bit_minMaxium_blocks(file,outputfile,nd,block_h=bk_h)

if __name__=='__main__':
    # convert_8bit_minMaxium(r"D:\\222222\\GF1102160794620200630F.pix",
    #                        r"D:\\222222\\GF1F.pix",0)
    # convert_8bit_minMaxium_blocks(r"D:\data\original\16\16b.tif",
    # r"D:\data\original\4\16b4.tif", block_h=20000)
    # convert_8bit_minMaxium(r"D:\data\original\16\16b.tif",
    #                               r"D:\data\original\4\16b5.tif")
    fire.Fire()