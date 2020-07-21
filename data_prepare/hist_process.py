

import os, sys,gc
import numpy as np
import gdal
import fire

import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt


from ulitities.base_functions import get_file, load_img_by_gdal,load_img_by_gdal_geo,load_img_by_gdal_info
min_delta=0.0000001


Flag_Hist_match=2 #0:直方图统计，1:save hitmap; 2:直方图匹配

input_dir ='F:\\11'
B=4
S=256
result_bits = 'int8'
blockHeight=20000
dest_file = 'F:\\11\\2_hist1.csv'
# dest_file ='/home/omnisky/PycharmProjects/data/tree/ori-global/global_src_hist1.csv'
src_file='/home/omnisky/PycharmProjects/data/tree/ori-global/global_src_hist1.csv'
histmap_file ='F:\\11\\histmap.csv'
# test_file = '/home/omnisky/PycharmProjects/data/test/global/test_csv/histMap.csv'

output_dir = 'D:\\data\\test'

def get_hist(files, bands=4, scale=256, block_h=20000):
    print("[Info] Statisify histogram from images...")
    # print("bands={}, scale={}".format(bands,scale))
    hist = np.zeros((scale,bands),np.uint64)
    in_files =[]
    if isinstance(files,str):
        in_files.append(files)
    elif isinstance(files,list):
        in_files=files
    # in_files=list(in_files)


    for file in in_files:
        print("\n\t[info]deal:{}".format(file))
        if bands==1:
            img = load_img_by_gdal(file,grayscale=True)
            # c=1
            h, bin_edges = np.histogram(img[:, :], bins=range(scale + 1))
            h = np.array(h, np.uint64)
            hist[:, 0] += h[:scale]
        else:
            try:
                dataset=gdal.Open(file)
            except:
                print("Error:Opening img failed {}".format(file))
                return -1
            y_height = dataset.RasterYSize
            x_width = dataset.RasterXSize
            img_bands = dataset.RasterCount
            n_blocks=1
            if y_height % block_h ==0:
                n_blocks=int(y_height/block_h)
            else:
                n_blocks= int(y_height/block_h) +1
            real_b=min(img_bands,bands)
            for index_block in range(n_blocks):
                start_y = index_block * block_h
                y_block_height = block_h
                if index_block ==n_blocks-1:
                    y_block_height = y_height-start_y
                img = dataset.ReadAsArray(0, start_y, x_width, y_block_height)
                img=np.transpose(img,(1,2,0))
                for index_band in range(real_b):
                    h, bin_edges = np.histogram(img[:, :, index_band], bins=range(scale + 1))
                    h = np.asarray(h, np.uint32)
                    hist[:, index_band] += h[:scale]
            del dataset
            # img = load_img_by_gdal(file)
            # a,b,c = img.shape
            # if bands>c:
            #     print("Warning: image bands is gt B")
            # real_b = min(c, bands)
            # for i in range(real_b):
            #     h, bin_edges = np.histogram(img[:, :, i], bins=range(scale + 1))
            #     h = np.array(h, np.uint64)
            #     hist[:, i] += h[:scale]

    return hist


def save_hist_to_csv(in_dir,csv_file,bands=4,scale=256):
    print(in_dir, csv_file, bands,scale)
    # sys.exit(-1)
    input_files, _ = get_file(in_dir)
    if len(input_files)==0:
        print("Error: there is no file in input dir：{}".format(in_dir))
        return -1

    Hist = get_hist(input_files, bands, scale,blockHeight)

    # Data = {'band_1':Hist[:,0], 'band_2':Hist[:,1],'band_3':Hist[:,2],'band_4':Hist[:,3]}

    df = pd.DataFrame(Hist)
    df.to_csv(csv_file)
    return 0


def calc_cum_hist(hist):
    read_scale = len(hist)
    cum_hist = np.zeros((read_scale, 1), np.float64)

    for i in range(read_scale):
        for j in range(i):
            cum_hist[i] += hist[j]
    total_pixel = np.zeros(1,np.uint64)
    total_pixel = np.sum(hist)
    f_cum_hist = np.zeros((read_scale,1), np.float32)
    f_cum_hist = cum_hist/(total_pixel+min_delta)

    return f_cum_hist

def HistMappingGML(scr, dest, scale):

    diff = np.zeros((scale,scale), np.float)

    histMap = np.zeros(scale,np.uint16)
    # for j in range(scale):
    #     histMap[j]=scale-1

    # minValue = 0.0
    startX = 0
    # lastStartY = 0
    lastEndY = 0
    startY = 0
    endY = 0
    i = 0
    x = 0
    y = 0
    # a = 1
    # b = 0

    for y in range(scale):
        for x in range(scale):
            diff[x,y] = abs(dest[x]-scr[y])

    for x in range(scale):
        minValue=diff[x,0]
        for y in range(scale):
            if minValue>diff[x,y]:
                endY=y
                minValue=diff[x,y]
        if endY !=lastEndY:
            for i in range(startY,endY+1):
                if endY==startY:
                    temp=int((startX+x)/2+0.5)
                    if temp<0:
                        temp=0
                    histMap[i]=temp
                elif startX==x:
                    histMap[i]=x
                else:
                    a = (endY-startY)/(x-startX+min_delta)
                    b = endY-a*x
                    temp = int((i-b)/(a+min_delta) +0.5)
                    histMap[i]=temp

            lastStartY=startY
            lastEndY=endY
            startY=lastEndY+1
            startX=x+1

    for i in range(endY+1,scale):
        histMap[i]=scale-1

    for i in range(scale):
        # if histMap[i]<histMap[i-1]:
        #     histMap[i]=histMap[i-1]
        if histMap[i]>=scale:
            histMap[i]=scale-1



    return histMap


def HistMappingSML(scr, dest, scale):

    diff = np.zeros((scale,scale), np.float)

    histMap = np.zeros(scale,np.uint16)
    for j in range(scale):
        histMap[j]=scale-1

    endY = 0


    for y in range(scale):
        for x in range(scale):
            diff[x,y] = abs(dest[x]-scr[y])

    for x in range(scale):
        minValue=diff[x,0]
        for y in range(scale):
            if minValue>diff[x,y]:
                endY=y
                minValue=diff[x,y]
            histMap[x] = endY

    return histMap


def save_histMap(src_file, dest_file, histmap_file, bands=4,scale=256):
    all_dest = np.array(pd.read_csv(dest_file))
    all_src = np.array(pd.read_csv(src_file))
    if all_dest.shape[-1] != all_src.shape[-1]:
        print("Error: bands of dest and src are not equal!")
        return -1
    C=min(bands, all_dest.shape[-1])
    all_histMap=[]
    for t in range(C):
        print("[Info]\t\tband:{}".format(t + 1))
        # tmp = np.zeros((H, W), np.uint16)
        dest = all_dest[:, t + 1]
        dest[0,t+1] = 1  # 防止背景“0”的值过大，降低了整体的值
        src = all_src[:, t+1]
        src[0, t + 1] = 1  # 防止背景“0”的值过大，降低了整体的值
        if len(dest) != len(src) or len(dest) != scale:
            print("Error: length  of dest, src and scale are not equal")
            return -2
        # assert (len(dest) == len(src))
        # assert (len(dest) == scale)

        cum_dest = calc_cum_hist(dest)
        for i in range(scale):
            if i == scale - 1:
                cum_dest[i] *= scale
            else:
                cum_dest[i] *= scale - 1

        cum_src = calc_cum_hist(src)
        for i in range(scale):
            if i == scale - 1:
                cum_src[i] *= scale
            else:
                cum_src[i] *= scale - 1

        histM = HistMappingGML(cum_src, cum_dest, scale)
        all_histMap.append(histM)
    all_histMap = np.asarray(all_histMap, np.uint16)
    all_histMap = np.transpose(all_histMap,(1,0))
    df = pd.DataFrame(all_histMap)
    df.to_csv(histmap_file)

    return 0

def histmap_img(in_dir, out_dir, histmap_file, bands=4, scale=256, block_h=20000):
    histMaps = np.array(pd.read_csv(histmap_file))
    if not os.path.isdir(in_dir):
        print("Error: input dir is not existed")
        return -1

    files, _ = get_file(in_dir)
    if len(files)==0:
        print("Warnin:There is no file in input dir")
        return -1
    if not os.path.isdir(out_dir):
        print(("Warning: output dir is not existed, it will be created automatically"))
        os.mkdir(out_dir)

    for file in tqdm(files):
        absname = os.path.split(file)[1]
        print('\n\t[Info] images:{}'.format(absname))
        absname = absname.split('.')[0]
        absname = ''.join([absname, '.tif'])

        try:
            dataset = gdal.Open(file)
        except:
            print("Error:Opening img failed {}".format(file))
            return -1
        y_height = dataset.RasterYSize
        x_width = dataset.RasterXSize
        img_bands = dataset.RasterCount
        result = np.zeros((y_height,x_width,img_bands), np.uint16)
        geoinf = dataset.GetGeoTransform()
        projinf= dataset.GetProjectionRef()
        if img_bands != bands:
            print("Error: B is not equal image bands")
            return -1
        n_blocks = 1
        if y_height % block_h == 0:
            n_blocks = int(y_height / block_h)
        else:
            n_blocks = int(y_height / block_h) + 1
        real_b = min(img_bands, bands)
        for index_block in range(n_blocks):
            start_y = index_block * block_h
            y_block_height = block_h
            if index_block == n_blocks - 1:
                y_block_height = y_height - start_y
            img = dataset.ReadAsArray(0, start_y, x_width, y_block_height)
            img = np.transpose(img, (1, 2, 0))

            for index_band in range(real_b):
                tmp = np.zeros((y_block_height, x_width), np.uint16)
                tmp[:,:]=img[:,:,index_band]
                for i in range(scale):
                    if i != histMaps[i,index_band+1]:
                        index = np.where(img[:,:,index_band] == i)
                        tmp[index] = histMaps[i,index_band+1]
                result[start_y:start_y+y_block_height , :, index_band] = tmp[:,:]
                    # tmp[index] = hist_one[i]
                # for i in range(y_block_height):
                #     for j in range(x_width):
                #         result[index_block*block_h+i,j,index_band]=histMaps[img[i,j,index_band],index_band+1]
                # index = np.where(img[:,:,index_band]==)

        # img, geoinfo = load_img_by_gdal_geo(file)
        # H, W, C, geoinf, projinf = load_img_by_gdal_info(file)
        # H, W, C = img.shape
        # if C != bands:
        #     print("Error: B is not equal image bands")
        #     return -1
        # assert (C == bands)
        # all_src = get_hist(file, bands, scale)
        # result = []
        del dataset
        if not os.path.isdir(out_dir):
            print("Warning: output directory does not exist")
            os.mkdir(out_dir)

        # for t in range(bands):
        #     print("[Info]\t\tband:{}".format(t + 1))
        #     tmp = np.zeros((H, W), np.uint16)
        #     tmp[:,:] = img[:,:,t]
        #     hist_one = histMaps[:,t+1]
        #
        #     for i in range(scale):
        #         if i !=hist_one[i]:
        #             index = np.where(img[:,:,t] == i)
        #             # tmp[index] = histMaps[i,t+1]
        #             tmp[index] = hist_one[i]
        #
        #     # plt.imshow(tmp)
        #     # plt.show()
        #     result.append(tmp)

        outputfile = os.path.join(out_dir, absname)
        driver = gdal.GetDriverByName("GTiff")
        outdataset = driver.Create(outputfile, x_width, y_height, real_b, gdal.GDT_UInt16)

        outdataset.SetGeoTransform(geoinf)
        outdataset.SetProjection(projinf)
        for i in range(real_b):
            outdataset.GetRasterBand(i + 1).WriteArray(result[:,:,i])

        del outdataset
        print("Result saved to:{}".format(outputfile))
        gc.collect()


    return 0


if __name__=='__main__':
    fire.Fire()

    """用于测试"""
    # ret=0
    # if Flag_Hist_match==0:
    #     ret=save_hist_to_csv(input_dir,dest_file,bands=B,scale=S)
    # elif Flag_Hist_match==1:
    #     ret=save_histMap(src_file,dest_file,histmap_file, scale=S)
    # elif Flag_Hist_match==2:
    #     ret=histmap_img(input_dir, output_dir,histmap_file,  bands=B, scale=S)
    # else:
    #     print("Error: please check the value Flag_Hist_match which should be in [0,1,2]")
    #
    # if ret!=0:
    #     print("Error: wrong")
    # else:
    #     print("Successfully!")



