import os
from osgeo import gdal
import numpy as np
import fire
def progress(percent, msg, tag):
    """杩涘害鍥炶皟鍑芥暟"""
    print(percent, msg, tag)
def compress(path, target_path):
    """浣跨敤gdal杩涜鏂囦欢鍘嬬缉"""
    dataset = gdal.Open(path)
    driver = gdal.GetDriverByName('GTiff')
    driver.CreateCopy(target_path, dataset, strict=1, callback=progress, options=["TILED=YES", "COMPRESS=LZW"])


def Calc_Normalized_Difference_Index(imagery,output="",index_type = "NDVI" ,nodata=255,):
    try:
        dataset = gdal.Open(imagery)
    except:
        print("Open file failed")
        return False
    X = dataset.RasterXSize
    Y = dataset.RasterYSize
    n_bands = dataset.RasterCount
    if n_bands != 4:
        print("please use BGRN satellite imagery")
        return False
    Prj = dataset.GetProjection()
    Trans = dataset.GetGeoTransform()
    image_datatype = dataset.GetRasterBand(1).DataType

    band_img = []
    for b in range(n_bands):
        band = dataset.GetRasterBand(b + 1)
        band_img.append(np.asarray(band.ReadAsArray(),
                                   dtype=np.float64))
    index = np.where(band_img[0] == nodata)

    if output == "":
        output_dir = os.path.dirname(imagery)
    else:
        output_dir = output
    output_basename = os.path.basename(imagery).split(".")[0]


    if index_type == "NDVI":
        output_filename = output_dir + "\\" + output_basename + "_ndvi.tif"
        result = (band_img[1]-band_img[3])/(band_img[1]+band_img[3]+0.00000001)
    else:
        output_filename = output_dir + "\\" + output_basename + "_ndwi.tif"
        result = (band_img[3]-band_img[2])/(band_img[3]+band_img[2]+0.00000001)
    del band_img,band

    result[index] = nodata
    driver = gdal.GetDriverByName('GTiff')
    output_ds = driver.Create(output_filename, X,
                              Y, 1, gdal.GDT_Float64)
    output_ds.SetGeoTransform(Trans)
    output_ds.SetProjection(Prj)
    output_ds.GetRasterBand(1).WriteArray(result)


def convert_8bit_minMaxium(inputRaster, outputRaster,nodata=65535):
    from osgeo import gdal
    srcRaster = gdal.Open(inputRaster)
    # iterate through bands
    height = srcRaster.RasterYSize
    width = srcRaster.RasterXSize
    im_bands = srcRaster.RasterCount

    geotransform = srcRaster.GetGeoTransform()
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
        index = np.where(band_arr_tmp == nodata)
        new_data = np.asarray(band_arr_tmp, dtype=np.float64)
        # mmmm =np.min(new_data)
        new_data[index] = np.nan
        # t_min = np.nanargmin(new_data)
        # t_max=np.nanargmax(new_data)
        # bmin= (new_data.flatten())[t_min]
        # bmax=(new_data.flatten())[t_max]

        temp = 255.0 * (new_data - bmin) / (bmax - bmin + 0.000001)
        temp[temp < 0.00001] = 0
        temp[temp > 253.99999] = 254
        temp[index] = 255
        temp=np.asarray(temp, np.uint8)

        result.append(temp)
        # plt.imshow(temp, cmap='gray')
        # plt.show()

    driver = gdal.GetDriverByName("GTiff")
    outdataset = driver.Create(outputRaster, width, height, im_bands, gdal.GDT_Byte)
    outdataset.SetGeoTransform(geotransform)
    for i in range(im_bands):
        outdataset.GetRasterBand(i + 1).WriteArray(result[i])
    del outdataset
if __name__=="__main__":
    fire.Fire()
    # ndvi = "D:\\data_file\\Land_ndwi.tif"
    # out = "D:\\data_file\\2_8b_ndvi.tif"
    # Calc_Normalized_Difference_Index("C:\\data\\8bits\\GF2331678620180712F_45985.img")
    # convert_8bit_minMaxium("C:\\data\\8bits\\GF2331678620180712F_45985_ndvi.tif",out,255)