#coding:utf8
""""
    This is main procedure for remote sensing image semantic segmentation

"""
import cv2
import numpy as np
import os
import sys
import gc
import gdal
import json,time
import fire
import argparse
from keras.models import load_model
# from sklearn.preprocessing import LabelEncoder
from tqdm import tqdm
import matplotlib.pyplot as plt
from keras.models import Model
from keras.layers import Conv2D, MaxPooling2D, UpSampling2D, BatchNormalization, Reshape, Permute, Activation, Input

from keras import backend as K
K.set_image_dim_ordering('tf')
K.clear_session()

# from base_predict_functions import orignal_predict_notonehot, smooth_predict_for_binary_notonehot
from ulitities.base_functions import echoRuntime,send_message_callback, load_img_by_gdal_blocks, UINT10,UINT8,UINT16, get_file, polygonize,load_img_by_gdal_info
from predict_backbone import predict_img_with_smooth_windowing,core_orignal_predict,core_smooth_predict_multiclass, core_smooth_predict_binary

from config import Config
import pandas as pd
import segmentation_models  # very important!
from deeplab.model import relu6, BilinearUpsampling
# from crfrnn.crfrnn_layer import CrfRnnLayer

NDVI=True
eps=0.00001

def check_predict_input(dict_para):
    print(dict_para)
    if dict_para["gpu"]==None:
        gpu_id=0
    elif isinstance(dict_para["gpu"], int):
        gpu_id=dict_para["gpu"]
        print("gpu_id:{}".format(gpu_id))
    else:
        tmp=int(dict_para["gpu"][0])
        if isinstance(tmp,int):
            gpu_id=tmp
        else:
            print("Error:para gpu is not a number!\n")
            return -1

    if os.path.isfile(dict_para["configs"]) and ('.json' in dict_para["configs"]):
        config_file = dict_para["configs"]
    else:
        print("Error: para configs is not json file")
        return -4

    with open(config_file, 'r') as f:
        cfgl = json.load(f)
    config = Config(**cfgl)
    print(type(config))
    if os.path.isdir(dict_para["input"]) or os.path.isfile(dict_para["input"]):
        ult_input=dict_para["input"]
        if os.path.isfile(ult_input):
            print("para input is a file\n")
        else:
            print("para input is a directory\n")
    elif os.path.isdir(config.img_input) or os.path.isfile(config.img_input):
        print("Default input in config file will be used")
        ult_input = config.img_input
        if os.path.isfile(ult_input):
            print("para input is a file\n")
        else:
            print("para input is a directory\n")
    else:
        print("Error: para input is not a file or directory\n")
        return -2

    if os.path.isdir(dict_para["output"]):
        output_dir=dict_para["output"]
    elif os.path.isdir(config.mask_dir):
        output_dir=config.mask_dir
    else:
        print("Error: para output is not a directory\n")
        return -3

    if os.path.isfile(dict_para["model"]) and ('.h5' in dict_para["model"]):
        curr_model=dict_para["model"]
    elif os.path.isfile(config.model_path):
        curr_model=config.model_path
    else:
        print("Error: para model is not a h5 file")
        return -5
    print("Following parameters will be used:\n")
    print("gpu: {}\n".format(gpu_id))
    print("input: {}\n".format(ult_input))
    print("output: {}\n".format(output_dir))
    print("model: {}\n".format(curr_model))
    out = {"configs": config_file, "gpu":gpu_id, "input":ult_input,
           "output":output_dir, "model":curr_model}
    return out

@echoRuntime
def predict(send_massage_callback=send_message_callback, configs=None,gpu=0, input='',output='',model=''):
    send_massage_callback("predict >>>")
    # return 0
    dict_in = {"configs": configs, "gpu":gpu, "input":input,"output":output, "model":model}
    try:
        # from PyQt5.QtCore import QTimer, QEventLoop
        # while 1:
        #     send_massage_callback("message 1")
        #     loop = QEventLoop()
        #     QTimer.singleShot(1000, loop.quit)
        #     loop.exec_()
        #     send_massage_callback("message 2")
        out=check_predict_input(dict_in)
    except:
        out=-998
    if isinstance(out, int):
        send_massage_callback("Fault! check input parameter ")
        return out


    # os.environ["CUDA_VISIBLE_DEVICES"] = str(out["gpu"])
    with open(configs, 'r') as f:
        cfgl = json.load(f)
    config = Config(**cfgl)

    im_type = UINT8
    if "10" in config.im_type:
        im_type = UINT10
    elif "16" in config.im_type:
        im_type=UINT16
    else:
        pass

    target_class =config.nb_classes
    if target_class == 2:
        print("Warning: target classes should not be 2, this must be binary classification!")
        target_class =1

    FLAG_APPROACH_PREDICT = 0 # 0: original predict, 1: smooth predict
    if "smooth" in config.strategy:
        FLAG_APPROACH_PREDICT =1
    else:
        pass

    date_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    output_dir=os.path.join(out["output"], date_time)
    if not os.path.isdir(output_dir):
       os.mkdir(output_dir)
    # print("Ultimate output dir:{}".format(output_dir))


    block_size = config.block_size
    # nodata = config.nodata

    input_files = []
    if os.path.isfile(out["input"]):
        print("[INFO] input is one file...")
        input_files.append(out["input"])
    elif os.path.isdir(out["input"]):
        print("[INFO] input is a directory...")
        in_files, _ = get_file(out["input"])
        for file in in_files:
            input_files.append(file)
    if len(input_files)==0:
        send_massage_callback("no input images")
        sys.exit(-1)
    send_massage_callback(" {} images will be classified".format(len(input_files)))

    csv_file = os.path.join(output_dir, 'readme.csv')

    df = pd.DataFrame.from_dict(out, orient='index')
    df.to_csv(csv_file)

    # out_bands = target_class

    try:
        send_massage_callback("loading models...")
        if "deeplab" in out["model"]:
            send_massage_callback("For deeplab V3+, load model with parameters of custom_objects\n")
            model = load_model(out["model"],
                               custom_objects={'relu6': relu6, 'BilinearUpsampling': BilinearUpsampling}, compile=False)
        else:
            model = load_model(out["model"], compile=False)
    except Exception:
        send_massage_callback("Error: failed to load model!\n")
        sys.exit(-1)
    finally:
        send_massage_callback("Load model successfully!\n")
    # print(model.summary())

    for img_file in input_files:#tqdm(input_files):
        if not os.path.isfile(img_file):
            print("Warning: file does not exist:{}".format(img_file))
            continue
        send_massage_callback(" Classify : "+img_file)
        # print("\n[INFO] opening image:{}...".format(img_file))
        abs_filename = os.path.split(img_file)[1]
        H, W, C, geoinf,projinf = load_img_by_gdal_info(img_file)
        if H==0:
            print("Open failed:{}".format(abs_filename))
            continue
        gc.collect()

        nb_blocks = int(H*W/block_size)
        if H*W>nb_blocks*block_size:
            nb_blocks +=1
        block_h = int(block_size/W)
        print("single block size :[{},{}]".format(block_h,W))
        result_mask = np.zeros((H, W), np.uint8)
        for i in list(range(nb_blocks)):#tqdm(list(range(nb_blocks))):
            send_massage_callback("[INFO] predict image for {} block".format(i))
            # print("[INFO] predict image for {} block".format(i))
            start =block_h*i
            this_h = block_h
            if (i+1)*block_h>H:
                this_h = H-i*block_h
            end = start+this_h
            # b_img = load_img_by_gdal_blocks(img_file,0,start,W,this_h)
            b_img = load_img_by_gdal_blocks(img_file, 0, start, W, this_h+config.window_size)

            if i ==nb_blocks-1:
                tmp_img = np.zeros((this_h+config.window_size, W, C), np.uint16)
                tmp_img[:this_h,:,:] = b_img
            else:
                tmp_img = b_img
                # exp_img = np.zeros((this_h+config.window_size, W, C), np.uint16)
                # exp_img[:, :, :] = b_img[:,:,:]
            # b_img = whole_img[start:end,:,:]
            # plt.imshow(b_img[:,:,1])
            # plt.show()
            # sys.exit(-3)
            """get data in bands of band_list"""
            band_list = config.band_list
            if len(band_list) == 0:
                band_list = range(C)
            if len(band_list) > C or max(band_list) >= C:
                print("input bands should not be bigger than image bands!")
                sys.exit(-2)

            a, b, c = tmp_img.shape
            if im_type == UINT8:
                # input_img = input_img / 255.0
                TScale=255.0
                input_img = np.zeros((a, b, len(band_list)), np.uint8)
            elif im_type == UINT10:
                # input_img = input_img / 1024.0
                TScale=1024.0
                input_img = np.zeros((a, b, len(band_list)), np.float16)
            elif im_type == UINT16:
                # input_img = input_img / 25535.0
                TScale=65535.0
                input_img = np.zeros((a, b, len(band_list)), np.float16)

            # input_img = np.zeros((a,b,len(band_list)), np.float16)
            for i in range(len(band_list)):
                input_img[:,:,i] = tmp_img[:,:,band_list[i]]
                if i==0:
                    nodata_indx= np.where(input_img[:,:,i]==config.nodata)


            if FLAG_APPROACH_PREDICT == 0:
                print("[INFO] predict image by orignal approach ...")
                # a,b,c=input_img.shape
                num_of_bands = min(input_img.shape)
                result = core_orignal_predict(input_img, num_of_bands, model, config.window_size, config.img_w, mask_bands=config.nb_classes, QuanScale=TScale)
                result[nodata_indx] = 0
                result_mask[start:end,:]=result[:this_h,:]


            elif FLAG_APPROACH_PREDICT == 1:
                print("[INFO] predict image by smooth approach... ")
                output_mask = np.zeros((this_h+config.window_size, W), np.uint8)
                if target_class > 2:
                    result = predict_img_with_smooth_windowing(
                        input_img,
                        model,
                        window_size=config.window_size,
                        subdivisions=config.subdivisions,
                        slices= config.slices,
                        real_classes=target_class,  # output channels = 是真的类别，总类别-背景
                        pred_func=core_smooth_predict_multiclass,
                        PLOT_PROGRESS=False,
                        QuanScale=TScale
                    )
                    # for i in range(target_class):
                    #     indx = np.where(result[:, :, i] >= 127)
                    #     output_mask[indx] = i + 1

                    output_mask = np.argmax(result, axis=-1)
                    del result
                    gc.collect()

                else:
                    result = predict_img_with_smooth_windowing(
                        input_img,
                        model,
                        window_size=config.window_size,
                        subdivisions=config.subdivisions,
                        slices=config.slices,
                        real_classes=target_class,
                        pred_func=core_smooth_predict_binary,
                        PLOT_PROGRESS=False,
                        QuanScale=TScale
                    )
                    indx = np.where(result[:, :, 0] >= 127)
                    output_mask[indx] = 1
                    # del result
                    gc.collect()
                output_mask[nodata_indx]=0
                result_mask[start:end, :] = output_mask[:this_h, :]
                # del output_mask

                gc.collect()

            del b_img
            # del tmp_img
            # del input_img

            gc.collect()

        print("Unique value in result mask: {}".format(np.unique(result_mask)))
        # result_mask[nodata_indx]=255
        # output_file = ''.join([output_dir, '/', abs_filename, config.suffix])
        output_file = ''.join([output_dir, '/', abs_filename])
        driver = gdal.GetDriverByName("GTiff")
        outdataset = driver.Create(output_file, W, H, 1, gdal.GDT_Byte)
        outdataset.SetGeoTransform(geoinf)
        outdataset.SetProjection(projinf)
        if outdataset == None:
            send_massage_callback("create dataset failed!\n")
            sys.exit(-2)
        outdataset.GetRasterBand(1).WriteArray(result_mask)
        del outdataset
        # result_mask[nodata_indx] = 255
        del result_mask
        gc.collect()
        send_massage_callback("Saved to:{}".format(output_file))

        # output vector file from raster file
        if config.tovector:
            shp_file= ''.join([output_dir, '/', abs_filename, '.shp'])
            polygonize(output_file, shp_file)

    return 0

if __name__=="__main__":
    # predict(
    #     configs=r'D:\data\water\config_binary_water4bands.json',
    #     gpu=0,
    #     input=r"F:\问题",
    #     output = r"D:\data\pred",
    #     model = r"D:\data\water\20200429\all\water4_imagenet_unet_vgg16_bce_dice_loss_adam_480_123bands_2020-04-29_00-53-42best.h5")

    fire.Fire()

