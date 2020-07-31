import gdal,fire,os
from osgeo import ogr
def rasterize_layer(imgfile,shpfile,output,attributeFiledName="DN"):
    '''
    Make sure the attributeFiledName is correct
    :param imgfile:
    :param shpfile:
    :param output:
    :return:
    '''
    # open origin image
    data = gdal.Open(imgfile, gdal.GA_ReadOnly)
    geo_transform = data.GetGeoTransform()
    x_res = data.RasterXSize
    y_res = data.RasterYSize

    # set out iamge
    img_basename = os.path.basename(imgfile)
    output = output + "\\" + img_basename
    y_ds = gdal.GetDriverByName('GTiff').Create(output, x_res, y_res, 1, gdal.GDT_Byte,
                                                options=['COMPRESS=LZW', 'BIGTIFF=YES'])
    y_ds.SetGeoTransform(geo_transform)
    target_ds = gdal.GetDriverByName('MEM').Create('', x_res, y_res, 1, gdal.GDT_Byte)
    target_ds.SetGeoTransform(geo_transform)
    band = target_ds.GetRasterBand(1)
    band.SetNoDataValue(255)
    band.FlushCache()
    # open vector
    mb_v = ogr.Open(shpfile)
    mb_l = mb_v.GetLayer()
    attr_name = "ATTRIBUTE=" + attributeFiledName
    if len(mb_l) > 0:
        gdal.RasterizeLayer(target_ds, [1], mb_l,options=[attr_name])
    y_buffer = band.ReadAsArray()
    y_ds.WriteRaster(0, 0, x_res, y_res, y_buffer.tostring())
    target_ds = None
    y_ds = None
    return 0
imgfile = "D:\\222222\\ZY306314304112720190606M.IMG"
shpfile = "D:\\222222\\zy.shp"
outimg = "D:\\222222\\out"
result = "D:\\222222\\out\\ZY306314304112720190606M.IMG"
# rasterize_layer(shpfile,imgfile,outimg,"DN")
def crop_by_extent(imgfile,shpfile,output):
    '''
    Make sure the image contain whole vecotor layer
    :param imgfile:
    :param shpfile:
    :param output:
    :return:
    '''
    mb_v = ogr.Open(shpfile)
    mb_l = mb_v.GetLayer()
    extent = mb_l.GetExtent()
    v_start_p =[extent[0],extent[3]]
    v_ofst_dist = [abs(extent[1]-extent[0]),abs(extent[3]-extent[2])]

    d_set = gdal.Open(imgfile)
    r_extent = d_set.GetGeoTransform()
    Prj = d_set.GetProjection()
    r_x_res = d_set.RasterXSize
    r_y_res = d_set.RasterYSize
    n_bands = d_set.RasterCount
    band_1 = d_set.GetRasterBand(1)
    bits_type = band_1.DataType

    x_start_px = int(abs((v_start_p[0]-r_extent[0])/r_extent[1]))
    y_start_px = int(abs((v_start_p[1]-r_extent[3])/r_extent[5]))
    x_ofst_px = int(abs(v_ofst_dist[0] / r_extent[1]))
    y_ofst_px = int(abs(v_ofst_dist[1] / r_extent[5]))
    img_basename = os.path.basename(imgfile)
    output = output + "\\" + img_basename
    driver = gdal.GetDriverByName('GTiff')
    output_ds = driver.Create(output, x_ofst_px,
                              y_ofst_px, n_bands, bits_type)
    out_extent = (extent[0],r_extent[1],r_extent[2],extent[3],r_extent[4],r_extent[5])
    output_ds.SetGeoTransform(out_extent)
    output_ds.SetProjection(Prj)
    if x_start_px + x_ofst_px > r_x_res:
        x_ofst_px= r_x_res - x_start_px
    if y_start_px + y_ofst_px > r_y_res:
        y_ofst_px= r_y_res - y_start_px
    for band in range(n_bands):
        band_p = d_set.GetRasterBand(band+1)
        data = band_p.ReadAsArray(x_start_px, y_start_px, x_ofst_px, y_ofst_px)
        output_ds.GetRasterBand(band + 1).WriteArray(data)
    return 0
# crop_by_extent(imgfile,shpfile,outimg)
# rasterize_layer(result,shpfile,output="D:\\222222\\label",)
if __name__=="__main__":
    fire.Fire()
