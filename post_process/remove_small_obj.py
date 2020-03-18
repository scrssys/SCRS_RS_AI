import fire,os,sys,numpy
from tqdm import tqdm
from skimage import io,morphology
from ulitities.base_functions import get_file,load_img_by_gdal
def remove_small_obj(inf,outf,minsize):
    from osgeo import gdal
    srcRaster = gdal.Open(inf)
    # iterate through bands

    im_bands = srcRaster.RasterCount
    if im_bands == 1:
        height = srcRaster.RasterYSize
        width = srcRaster.RasterXSize
        geotransform = srcRaster.GetGeoTransform()
        band = srcRaster.GetRasterBand(1)
        band_arr_tmp = band.ReadAsArray()
        ##use opencv
        import cv2
        kernel = numpy.ones((minsize,minsize),numpy.uint8)
        opening = cv2.morphologyEx(band_arr_tmp, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
        ##use skimge
        # import skimage
        # closing_ = skimage.morphology.remove_small_objects(band_arr_tmp,minsize*10,connectivity=2)
        # closing = skimage.morphology.remove_small_holes(closing_,area_threshold=minsize*10, connectivity=2)

        driver = gdal.GetDriverByName("GTiff")
        outdataset = driver.Create(outf, width, height, im_bands, gdal.GDT_Byte)
        outdataset.SetGeoTransform(geotransform)
        outdataset.GetRasterBand(1).WriteArray(closing)
    del outdataset
    # cv2.imwrite(outf,closing)
    # img = io.imread(inf)
    # cv2.imwrite(outf, img)
    # img_ = morphology.remove_small_holes(img,800)
def batch_rmovesmallobj(inputdir,outputdir,minsize=5):
    if not os.path.isdir(inputdir):
        print("Please check input directory:{}".format(inputdir))
    if not os.path.isdir(outputdir):
        print('Warning: output directory is not existed')
        os.mkdir(outputdir)
    files,_=get_file(inputdir)
    for file in tqdm(files):
        print("Processing : " + file)
        absname = os.path.split(file)[1]
        outputfile = os.path.join(outputdir, absname)
        remove_small_obj(file, outputfile,minsize)
if __name__=="__main__":
    # batch_rmovesmallobj(r"D:\data\bieshu\2019-12-25_16-40-40",r"C:\Users\SCRS\Pictures\22")
    fire.Fire()