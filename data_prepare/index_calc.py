import os,fire
from osgeo import gdal
import numpy as np
from ulitities.base_functions import get_file,geotrans_match
def progress(percent, msg, tag):
    print(percent, msg, tag)
def compress(path, target_path):
    dataset = gdal.Open(path)
    driver = gdal.GetDriverByName('GTiff')
    driver.CreateCopy(target_path, dataset, strict=1, callback=progress, options=["TILED=YES", "COMPRESS=LZW"])
def Calc_grid(width=1011,height=2000,w_size=1000,full=True):
    num_x = int(width/w_size)
    num_y = int(height/w_size)
    x_residue = width - num_x*w_size
    y_residue = height - num_y*w_size

    if num_x > 0 and num_y >0:
        arry_square = []
        arry_full = []
        for i in range(num_x+1):
            for j in range(num_y+1):
                if i == num_x and x_residue > 0:
                    if j == num_y and y_residue > 0:
                        arry_square.append([(i-1) * w_size+x_residue, (j - 1) * w_size + y_residue,w_size,w_size])
                        arry_full.append([i * w_size , j* w_size ,x_residue, y_residue])
                    elif i == num_x and x_residue == 0:
                        pass
                    elif i != num_x and x_residue > 0:
                        arry_square.append([(i-1) * w_size+x_residue, j * w_size,w_size,w_size])
                        arry_full.append([i * w_size , j * w_size,x_residue,w_size])
                else:
                    if j == num_y and y_residue > 0:
                        arry_square.append([i*w_size,(j-1) * w_size+y_residue,w_size,w_size])
                        arry_full.append([i * w_size, j * w_size,w_size,y_residue])
                    else:
                        arry_square.append([i * w_size, j * w_size,w_size,w_size])
                        arry_full.append([i * w_size, j * w_size,w_size,w_size])
        return arry_full,arry_square
    else:
        return [0,0,width,height],[0,0,width,height]
    print()
# print(Calc_grid())
def Calc_grid2(width,height,x_size=1000,y_size=1000):
    num_x = int(width/x_size) + 1
    num_y = int(height/y_size) + 1

    tmp_x=-x_size
    arry_full = []
    for i in range(num_x):
        tmp_x = tmp_x +x_size
        tmp_y = -y_size
        for j in range(num_y):
            tmp_y = tmp_y + y_size
            if (i+1)*y_size > height:
                ofst_ysize = height-i*y_size
            else:
                ofst_ysize =  y_size
            if (j+1)*x_size > width:
                ofst_xsize = width-j*x_size
            else:
                ofst_xsize = x_size
            if tmp_x <= width and tmp_y <= height and ofst_xsize >0 and ofst_ysize >0:
                arry_full.append([tmp_x,tmp_y,ofst_xsize,ofst_ysize])
    return arry_full
# print(Calc_grid2())
def Calc_Normalized_Difference_index_block(imagery):
    pass

    dataset = gdal.Open(imagery)
    X = dataset.RasterXSize
    Y = dataset.RasterYSize
    n_bands = dataset.RasterCount
    metaData = dataset.GetProjection()
    Trans = dataset.GetGeoTransform()
    image_datatype = dataset.GetRasterBand(1).DataType
    block_list=Calc_grid2(X,Y,x_size=10000,y_size=10000)
    image=[]
    driver = gdal.GetDriverByName('GTiff')
    output_filename = "D:\\data_file\\tmp\\tttt.tif"
    output_ds = driver.Create(output_filename, X,
                              Y, n_bands, gdal.GDT_Byte)
    for band in range(n_bands):
        band_p = dataset.GetRasterBand(band+1)
        for block in block_list:
            data = band_p.ReadAsArray(block[0], block[1], block[2], block[3])
            output_ds.GetRasterBand(band + 1).WriteArray(data,block[0],block[1])
    output_ds.FlushCache()

# Calc_Normalized_Difference_index_block('D:\\data_file\\2_8b_ndvi.tif')

def Calc_Normalized_Difference_Index(imagery,output="",index_type = "NDVI" ,nodata=65535,):
    try:
        dataset = gdal.Open(imagery)
    except:
        print("Open file failed")
        return -1
    X = dataset.RasterXSize
    Y = dataset.RasterYSize
    n_bands = dataset.RasterCount
    if n_bands != 4:
        print("please use BGRN satellite imagery")
        return -2
    image_datatype = dataset.GetRasterBand(1).DataType

    band_img = []
    for b in range(n_bands):
        band = dataset.GetRasterBand(b + 1)
        band_img.append(np.asarray(band.ReadAsArray(),
                                   dtype=np.float64))
    index = np.where(band_img[0] == nodata)

    if not os.path.isfile(output):
        output_dir = os.path.dirname(imagery)
        basename = os.path.basename(imagery).split(".")[0]
        if output_dir==output or not os.path.isdir(output):
            output_filename = output_dir+'/'+basename+'_'+index_type+'.tif'
        else:
            output_filename = output + '/' + basename +'.tif'
    else:
        if imagery==output:
            print("Error: input image should not be outputfile")
            return -3
        output_filename = output
    # output_basename = os.path.basename(imagery).split(".")[0]


    if index_type == "NDVI":
        # output_filename = output_dir + "\\" + output_basename + "_ndvi.tif"
        tmp = (band_img[3]-band_img[1])/(band_img[3]+band_img[2]+0.00000001)
    elif index_type == "NDWI":
        # output_filename = output_dir + "\\" + output_basename + "_ndwi.tif"
        tmp = (band_img[1]-band_img[3])/(band_img[1]+band_img[3]+0.00000001)
    else:
        print("Error: please check index type")
        return -4
    del band_img,band
    result = np.zeros((Y,X),np.uint8)
    result[:,:]= (tmp[:,:]+1.0)*255.0/2.0

    result[index] = 255
    driver = gdal.GetDriverByName('GTiff')
    output_ds = driver.Create(output_filename, X,
                              Y, 1, gdal.GDT_Byte)

    output_ds.GetRasterBand(1).WriteArray(result)
    geotrans_match(imagery,output_filename)
    return 0


def index_convert_8bit_minMaxium(inputRaster, outputRaster,nodata=65535):
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
        # if bmin is None or bmax is None:
        #     (bmin, bmax) = band.ComputeRasterMinMax(1)
        band_arr_tmp = band.ReadAsArray()
        index = np.where(band_arr_tmp == nodata)
        new_data = np.asarray(band_arr_tmp, dtype=np.float64)
        # mmmm =np.min(new_data)
        new_data[index] = np.nan
        # t_min = np.nanargmin(new_data)
        # t_max=np.nanargmax(new_data)
        # bmin= (new_data.flatten())[t_min]
        # bmax=(new_data.flatten())[t_max]
        bmin = -1
        bmax = 1
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
# ndvi = "D:\\data_file\\Land_ndwi.tif"
# out = "D:\\data_file\\2_8b_ndvi.tif"
# Calc_Normalized_Difference_Index("C:\\data\\8bits\\GF2331678620180712F_45985.img")
# convert_8bit_minMaxium("C:\\data\\8bits\\GF2331678620180712F_45985_ndvi.tif",out,255)
def batch_calc_index(indir,outdir="",keyword="NDWI",nulldata=65535):
    filelist=[]
    if os.path.isdir(indir):
        filelist,nb=get_file(indir)
        if nb ==0:
            print("Error: no file in input dir")
            return -1
    elif os.path.isfile(indir):
        filelist.append(indir)
    else:
        print("input is not dir or file")
        return -2

    # list = os.listdir(indir)
    if not os.path.isdir(outdir):
        os.mkdir(outdir)
    for file in filelist:
        # absname = os.path.split(file)[1]
        # outfile = os.path.join(outdir,absname)
        res=0
        if keyword == "NDWI":
            # Calc_Normalized_Difference_Index(imagery, output="", index_type="NDVI", nodata=255, ):
            print("Calculating Normalized Difference Water Index : " + file)
            res=Calc_Normalized_Difference_Index(file, output=outdir, index_type="NDWI", nodata=nulldata)
        elif keyword == "NDVI":
            print("Calculating Normalized Difference Vegetation Index : " + file)
            res=Calc_Normalized_Difference_Index(file, output=outdir, index_type="NDVI", nodata=nulldata)
        else:
            print("Error:please check index type")
            return -2
        if res !=0:
           print("Error: calculating index failed")
           return -3


    return 0
if __name__ == "__main__":
    fire.Fire()