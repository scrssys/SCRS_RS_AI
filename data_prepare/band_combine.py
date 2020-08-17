#coding:utf-8
import os,sys,fire
from ulitities.base_functions import get_file,find_file,geotrans_match
from tqdm import tqdm
import numpy as np
try:
    from osgeo import ogr, osr, gdal
    gdal.UseExceptions()
except:
    sys.exit('ERROR: cannot find GDAL/OGR modules')
def band_combine(file_list,outputfile):
    result = []
    try:
        dataset_a = gdal.Open(file_list[0])
    except:
        print("Warning: file opening failed :\n {}".format(file_list[0]))
        return -1
    try:
        dataset_b = gdal.Open(file_list[1])
    except:
        print("Warning: file opening failed :\n {}".format(file_list[1]))
        return -2
    # band_n_a = dataset_a.RasterCount
    # band_n_b = dataset_b.RasterCount
    band_n = dataset_a.RasterCount + dataset_b.RasterCount


    # result.append(dataset_a.ReadAsArray())
    # result.append(dataset_b.ReadAsArray())

    X = dataset_a.RasterXSize
    Y = dataset_a.RasterYSize
    if X!=dataset_b.RasterXSize or Y!=dataset_b.RasterYSize:
        print("Warning:input images must have the same width and height \n {}".format(os.path.split(file_list[0])[1]))
        return -3

    result = np.zeros((Y,X,band_n),np.uint16)

    for i in range(dataset_a.RasterCount):
        tmp_band = dataset_a.GetRasterBand(i+1)
        result[:,:,i] = tmp_band.ReadAsArray()

    for i in range(dataset_b.RasterCount):
        tmp_band = dataset_b.GetRasterBand(i + 1)
        result[:, :, dataset_a.RasterCount+i] = tmp_band.ReadAsArray()

    driver = gdal.GetDriverByName('GTiff')

    outdataset = driver.Create(outputfile, X,
                              Y, band_n, gdal.GDT_Byte)
    for i in range(band_n):
        outdataset.GetRasterBand(i+1).WriteArray(result[:,:,i])

    outdataset.FlushCache()
    del dataset_b,dataset_a, outdataset
    geotrans_match(file_list[0],outputfile)
    return 0


def band_combine_blocks(file_list,output,block_h=10000 ):
    result = []
    try:
        dataset_a = gdal.Open(file_list[0])
    except:
        print("Warning: file opening failed :\n {}".format(file_list[0]))
        return -1
    try:
        dataset_b = gdal.Open(file_list[1])
    except:
        print("Warning: file opening failed :\n {}".format(file_list[1]))
        return -2
    band_n_a = dataset_a.RasterCount
    band_n_b = dataset_b.RasterCount
    band_n = band_n_a + band_n_b


    # result.append(dataset_a.ReadAsArray())
    # result.append(dataset_b.ReadAsArray())

    width = dataset_a.RasterXSize
    height = dataset_a.RasterYSize
    if width!=dataset_b.RasterXSize or height!=dataset_b.RasterYSize:
        print("Warning:input images must have the same width and height \n {}".format(os.path.split(file_list[0])[1]))
        return -3


    bk_h = block_h
    if block_h > height:
        print("Warnin:block height is gt image height")
        bk_h = height
        # return -2

    try:
        driver = gdal.GetDriverByName("GTiff")
        outdataset = driver.Create(output, width, height, band_n, gdal.GDT_Byte)
    except:
        print("Error: output raster is existed or can not be opened:\n {}".format(output))
        return -3

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


        for i in range(band_n_a):
            tmp_band = dataset_a.GetRasterBand(i + 1)
            tmp = tmp_band.ReadAsArray(0, start_y, width, y_block_height)
            outdataset.GetRasterBand(i + 1).WriteArray(tmp, xoff=0, yoff=start_y)

        for i in range(band_n_b):
            tmp_band = dataset_b.GetRasterBand(i + 1)
            tmp = tmp_band.ReadAsArray(0, start_y, width, y_block_height)
            outdataset.GetRasterBand(band_n_a+i + 1).WriteArray(tmp, xoff=0, yoff=start_y)


    outdataset.FlushCache()
    del dataset_b,dataset_a, outdataset
    geotrans_match(file_list[0],output)
    return 0


def batch_band_combine(indir,outdir,nodata=65535):
    if not os.path.isdir(indir):
        print("Error:input is not a directory")
        return -1

    if not os.path.isdir(indir+'/a/') or not os.path.isdir(indir+'/b'):
        print("Error: please check dir img and index")
        return -2

    filelist_a, nb = get_file(indir+'/a/')
    if nb ==0:
        print("Error: there is no file in dir a")
        return -3
    if not os.path.isdir(outdir):
        print("Warning: outdir is not exist, it will be created")
        os.mkdir(outdir)
    for fileA in tqdm(filelist_a):
        basename=os.path.basename(fileA).split(".")[0]
        fileB = find_file(indir+'/b/',basename)
        if len(fileB)==0:
            print("Warning: corresponding index file is not exist \n {}".format(os.path.split(fileA)[1]))
            continue
        print(fileB)
        flist=[]
        flist.append(fileA)
        flist.append(fileB)
        outfile = outdir+'/'+basename+'.tif'
        if os.path.isfile(outfile):
            print("Warning:result file is existed:{}\n".format(outfile))
            continue
        ret =0
        ret = band_combine_blocks(flist,outfile)
        if ret!=0:
            print("Error:combinig failed :{}".format(basename))
            continue

    return 0

# batch_band_combine(r"C:\Users\scrs\Desktop\8bit",r"C:\Users\scrs\Desktop\8",255)

# indir = "D:\\water\\src\\8bitOrigin"
# # list = os.listdir(indir)
# # for file in list:
# #     basename = os.path.basename(file).split(".")[0]
# #     try:
# #         print(file)
# #         infile_1= "D:\\water\\src\\8bitOrigin\\" +file
# #         infile_2 =  "D:\\water\\src\\8bitIndex\\" +basename + "_ndwi.tif"
# #         filelist = [infile_1,infile_2]
# #         band_list = [[0,1,2,3],[0]]
# #         band_combine(filelist,[[0,1,2,3],[0]])
# #
# #     except:
# #         print("filed  : "+file)
# variable_str='3_13'
#
# input_files =['/home/omnisky/PycharmProjects/data/samples/isprs/4_Ortho_RGBIR/top_potsdam_{}_RGBIR.tif'.format(variable_str),
#               '/home/omnisky/PycharmProjects/data/samples/isprs/1_DSM_normalisation/1_DSM_normalisation/dsm_potsdam_0{}_normalized_lastools.jpg'.format(variable_str)]
# output_file = '/home/omnisky/PycharmProjects/data/samples/isprs/train/src/top_potsdam_{}.tif'.format(variable_str)

if __name__=="__main__":
    fire.Fire()
    print("")
