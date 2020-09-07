# coding=utf-8

from keras.utils.np_utils import to_categorical
from keras.preprocessing.image import img_to_array
from keras.callbacks import ModelCheckpoint, EarlyStopping, History,ReduceLROnPlateau
import matplotlib.pyplot as plt
import cv2, argparse
import os, sys, json, random, time
from keras.models import *
from keras.layers import *
from keras.optimizers import *
from keras.models import load_model

from keras import backend as K

K.set_image_dim_ordering('tf')
from keras.callbacks import TensorBoard
from keras.utils import multi_gpu_model

from ulitities.base_functions import echoRuntime,send_message_callback,UINT16, UINT8, UINT10

seed = 4
np.random.seed(seed)
import segmentation_models as sm

from deeplab.model import Deeplabv3
from data_prepare.data_generater import train_data_generator,val_data_generator, train_data_generator_files,val_data_generator_files,\
    train_data_generator_h5,val_data_generator_h5
from config import Config
import h5py


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
        try:
            cfgl = json.load(f)
            config = Config(**cfgl)
        except:
            print("parsing config file failed")
            return -5
    print(type(config))
    if os.path.isdir(dict_para["sampleDir"]) or os.path.isfile(dict_para["sampleDir"]):
        ult_input=dict_para["sampleDir"]
    elif os.path.isdir(config.train_data_path)or os.path.isfile(config.train_data_pat):
        print("Default input in config file will be used")
        ult_input = config.train_data_path
    else:
        print("Error: para input is not a file or directory\n")
        return -2

    if os.path.isdir(dict_para["outDir"]):
        output_dir=dict_para["outDir"]
    elif os.path.isdir(config.model_dir):
        output_dir=config.model_dir
    else:
        print("warning: para model output is not a directory\n")
        return -3
    t = config.model_path
    if os.path.isfile(dict_para["baseModel"]) and ('.h5' in dict_para["baseModel"]):
        base_model=dict_para["baseModel"]
    elif os.path.isfile(config.base_model):
        base_model=config.base_model
    else:
        print("warning: para base model is not a h5 file")
        base_model=''
    print("Following parameters will be used:")
    print("gpu: {}".format(gpu_id))
    print("input: {}".format(ult_input))
    print("output: {}".format(output_dir))
    print("baseModel: {}\n".format(base_model))
    out = {"configs": config_file, "gpu":gpu_id, "sampleDir":ult_input,
           "outDir":output_dir, "baseModel":base_model}
    return out


"""get the train file name and divide to train and val parts"""
def get_train_val(sample_path, val_rate):
    file_type = ['.jpg','.png', '.tif', '.img']
    train_url = []
    train_set = []
    val_set = []
    for pic in os.listdir(sample_path + '/label'):
        if (str.lower(os.path.splitext(pic)[1]) in file_type):
            train_url.append(pic)
    random.shuffle(train_url)
    total_num = len(train_url)
    val_num = int(val_rate * total_num + 0.5)
    if val_num < 1:
        val_num = 1
    for i in range(len(train_url)):
        if i < val_num:
            val_set.append(train_url[i])
        else:
            train_set.append(train_url[i])
    return train_set, val_set


def train(configs=None,gpu=0, samples='',outdir='',baseModel='',send_massage_callback=send_message_callback):

    send_massage_callback("training >>>")
    # return 0
    dict_in = {"configs": configs, "gpu":gpu, "sampleDir":samples,"outDir":outdir, "baseModel":baseModel}
    try:
        out=check_predict_input(dict_in)
    except:
        out=-999
    if isinstance(out, int):
        send_massage_callback("Fault! check input parameter:{} ".format(out))
        return out

    os.environ["CUDA_VISIBLE_DEVICES"] = str(out["gpu"])
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
    if target_class>1:   # multiclass, target class = total class -1
        if target_class==2:
            print("Warning: target classes should not be 2, this must be binary classification!")
            target_class =1
        else:
            target_class -=1

    date_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    print("date and time: {}".format(date_time))
    # print("traindata from: {}".format(config.train_data_path))
    band_name = ''
    if len(config.band_list) == 0:
        band_name = 'fullbands'
    else:
        for i in range(len(config.band_list)):
            band_name += str(config.band_list[i])
        band_name += "bands"
    print("band_name:{}".format(band_name))
    if not os.path.isdir(out["outDir"]):
        print("Warning: model saveing directory is empty!")
        os.mkdir(config.model_dir)
    model_save_path = ''.join(
        [out["outDir"], '/', config.target_name, '_', config.network, '_', config.BACKBONE, '_', config.loss, '_',
         config.optimizer, '_', str(config.img_w), '_', band_name, '_', date_time, 'best.h5'])
    print("model save as to: {}".format(model_save_path))
    last_model = ''.join(
        [out["outDir"], '/', config.target_name, '_', config.network, '_', config.BACKBONE, '_', config.loss, '_',
         config.optimizer, '_', str(config.img_w), '_', band_name, '_', date_time, 'last.h5'])

    input_layer = (config.img_w, config.img_h, len(config.band_list))

    if 'unet' in config.network:
        model = sm.Unet(backbone_name=config.BACKBONE, input_shape=input_layer,
                        classes=config.nb_classes, activation=config.activation,
                        encoder_weights=config.encoder_weights)
    elif 'pspnet' in config.network:
        model = sm.PSPNet(backbone_name=config.BACKBONE, input_shape=input_layer,
                          classes=config.nb_classes, activation=config.activation,
                          encoder_weights=config.encoder_weights, psp_dropout=config.dropout)
    elif 'fpn' in config.network:
        model = sm.FPN(backbone_name=config.BACKBONE, input_shape=input_layer,
                       classes=config.nb_classes, activation=config.activation,
                       encoder_weights=config.encoder_weights, pyramid_dropout=config.dropout)
    elif 'linknet' in config.network:
        model = sm.Linknet(backbone_name=config.BACKBONE, input_shape=input_layer,
                           classes=config.nb_classes, activation=config.activation,
                           encoder_weights=config.encoder_weights)
    elif 'deeplabv3plus' in config.network:
        model = Deeplabv3(weights=config.encoder_weights, input_shape=input_layer,
                          classes=config.nb_classes, backbone=config.BACKBONE, activation=config.activation)

    else:
        print("Error:")

    print(model.summary())
    # from keras.utils import plot_model
    # plot_model(model, to_file='model_fpn.png')
    # sys.exit(-99)
    """\n**************************************"""
    print("Train by : {}_{}".format(config.network, config.BACKBONE))
    """\n**************************************\n"""
    if os.path.isfile(out['baseModel']):
        try:
            model.load_weights(out["baseModel"])
        except ValueError:
            print("Can not load weights from base model: {}".format(config.base_model))
        else:
            print("loaded weights from base model:{}".format(config.base_model))
    model_checkpoint = ModelCheckpoint(
        model_save_path,
        monitor=config.monitor,
        save_best_only=config.save_best_only,
        mode=config.mode
    )

    model_earlystop = EarlyStopping(
        monitor=config.monitor,
        patience=config.patience + 10,
        verbose=0,
        mode=config.mode
    )

    # """自动调整学习率"""
    model_reduceLR = ReduceLROnPlateau(
        monitor=config.monitor,
        factor=config.factor,
        patience=config.patience,
        verbose=0,
        mode=config.mode,
        min_delta=config.epsilon,
        cooldown=config.cooldown,
        min_lr=config.min_lr
    )

    model_history = History()
    logdir = os.path.split(out["configs"])[0]+'/log/'
    if not os.path.isdir(logdir):
        print("warning: log dir is not exit")
        os.mkdir(logdir)
    #     return -6
    # else:
    #     if not os.path.isdir(os.path.split(out["configs"])[0], '/log/')
    #     os.mkdir((os.path.split(out["configs"])[0], '/log/'))
    logpath = ''.join(
        [logdir, config.target_name, "_", config.network, "_", config.BACKBONE, "_", config.loss, date_time])
    
    tb_log = TensorBoard(log_dir=logpath)
    callable = [model_checkpoint, model_earlystop, model_reduceLR, model_history, tb_log]

    train_set, val_set = get_train_val(out["sampleDir"],config.val_rate)
    train_numb = len(train_set) * config.sample_per_img
    valid_numb = len(val_set) * config.sample_per_img
    print("the number of train data is", train_numb)
    print("the number of val data is", valid_numb)

    # if isinstance(gpu_id, int):
    #     print("using single gpu {}".format(gpu_id))
    #     pass
    # elif isinstance(gpu_id, list):
    #     print("using multi gpu {}".format(gpu_id))
    #     if len(gpu_id) > 1:
    #         model = multi_gpu_model(model, gpus=len(gpu_id))

    self_optimizer = SGD(lr=config.lr, decay=1e-6, momentum=0.9, nesterov=True)
    if 'adagrad' in config.optimizer:
        self_optimizer = Adagrad(lr=config.lr, decay=1e-6)
    elif 'adam' in config.optimizer:
        self_optimizer = Adam(lr=config.lr, decay=1e-6, beta_1=0.9, beta_2=0.999, epsilon=1e-8)
    else:
        pass

    try:
        my_loss = eval("sm.losses." + config.loss)
        my_metrics = eval("sm.metrics." + config.metrics)
        model.compile(self_optimizer, loss=my_loss, metrics=['accuracy', my_metrics])
    except:
        print("model compile error")
        exit(-5)
    finally:
        print("Compile model successfully!")

    H = model.fit_generator(generator=train_data_generator_files(config, out["sampleDir"], train_set),
                            steps_per_epoch=train_numb // config.batch_size,
                            epochs=config.epochs,
                            verbose=1,
                            validation_data=val_data_generator_files(config, out["sampleDir"], val_set),
                            validation_steps=valid_numb // config.batch_size,
                            callbacks=callable,
                            max_q_size=1,
                            class_weight='auto')

    model.save(last_model)
    print("Training finished!")


def train_h5(send_massage_callback=send_message_callback, configs=None, gpu=0, samples='', outdir='', baseModel=''):
    send_massage_callback("training >>>")
    # return 0
    dict_in = {"configs": configs, "gpu": gpu, "sampleDir": samples, "outDir": outdir, "baseModel": baseModel}
    try:
        out = check_predict_input(dict_in)
    except:
        out = -999
    if isinstance(out, int):
        send_massage_callback("Fault! check input parameter:{} ".format(out))
        return out

    os.environ["CUDA_VISIBLE_DEVICES"] = str(out["gpu"])
    with open(configs, 'r') as f:
        cfgl = json.load(f)
    config = Config(**cfgl)

    im_type = UINT8
    if "10" in config.im_type:
        im_type = UINT10
    elif "16" in config.im_type:
        im_type = UINT16
    else:
        pass

    target_class = config.nb_classes
    if target_class > 1:  # multiclass, target class = total class -1
        if target_class == 2:
            print("Warning: target classes should not be 2, this must be binary classification!")
            target_class = 1
        else:
            target_class -= 1

    date_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    print("date and time: {}".format(date_time))
    # print("traindata from: {}".format(config.train_data_path))
    band_name = ''
    if len(config.band_list) == 0:
        band_name = 'fullbands'
    else:
        for i in range(len(config.band_list)):
            band_name += str(config.band_list[i])
        band_name += "bands"
    print("band_name:{}".format(band_name))
    if not os.path.isdir(out["outDir"]):
        print("Warning: model saveing directory is empty!")
        os.mkdir(config.model_dir)
    model_save_path = ''.join(
        [out["outDir"], '/', config.target_name, '_', config.network, '_', config.BACKBONE, '_', config.loss, '_',
         config.optimizer, '_', str(config.img_w), '_', band_name, '_', date_time, 'best.h5'])
    print("model save as to: {}".format(model_save_path))
    last_model = ''.join(
        [out["outDir"], '/', config.target_name, '_', config.network, '_', config.BACKBONE, '_', config.loss, '_',
         config.optimizer, '_', str(config.img_w), '_', band_name, '_', date_time, 'last.h5'])

    input_layer = (config.img_w, config.img_h, len(config.band_list))

    if 'unet' in config.network:
        model = sm.Unet(backbone_name=config.BACKBONE, input_shape=input_layer,
                        classes=config.nb_classes, activation=config.activation,
                        encoder_weights=config.encoder_weights)
    elif 'pspnet' in config.network:
        model = sm.PSPNet(backbone_name=config.BACKBONE, input_shape=input_layer,
                          classes=config.nb_classes, activation=config.activation,
                          encoder_weights=config.encoder_weights, psp_dropout=config.dropout)
    elif 'fpn' in config.network:
        model = sm.FPN(backbone_name=config.BACKBONE, input_shape=input_layer,
                       classes=config.nb_classes, activation=config.activation,
                       encoder_weights=config.encoder_weights, pyramid_dropout=config.dropout)
    elif 'linknet' in config.network:
        model = sm.Linknet(backbone_name=config.BACKBONE, input_shape=input_layer,
                           classes=config.nb_classes, activation=config.activation,
                           encoder_weights=config.encoder_weights)
    elif 'deeplabv3plus' in config.network:
        model = Deeplabv3(weights=config.encoder_weights, input_shape=input_layer,
                          classes=config.nb_classes, backbone=config.BACKBONE, activation=config.activation)

    else:
        print("Error:")

    print(model.summary())
    # from keras.utils import plot_model
    # plot_model(model, to_file='model_fpn.png')
    # sys.exit(-99)
    """\n**************************************"""
    print("Train by : {}_{}".format(config.network, config.BACKBONE))
    """\n**************************************\n"""
    if os.path.isfile(out['baseModel']):
        try:
            model.load_weights(out["baseModel"])
        except ValueError:
            print("Can not load weights from base model: {}".format(config.base_model))
        else:
            print("loaded weights from base model:{}".format(config.base_model))
    model_checkpoint = ModelCheckpoint(
        model_save_path,
        monitor=config.monitor,
        save_best_only=config.save_best_only,
        mode=config.mode
    )

    model_earlystop = EarlyStopping(
        monitor=config.monitor,
        patience=config.patience + 10,
        verbose=0,
        mode=config.mode
    )

    # """自动调整学习率"""
    model_reduceLR = ReduceLROnPlateau(
        monitor=config.monitor,
        factor=config.factor,
        patience=config.patience,
        verbose=0,
        mode=config.mode,
        min_delta=config.epsilon,
        cooldown=config.cooldown,
        min_lr=config.min_lr
    )

    model_history = History()
    logdir = os.path.split(out["configs"])[0] + '/log/'
    if not os.path.isdir(logdir):
        print("warning: log dir is not exit")
        os.mkdir(logdir)
    #     return -6
    # else:
    #     if not os.path.isdir(os.path.split(out["configs"])[0], '/log/')
    #     os.mkdir((os.path.split(out["configs"])[0], '/log/'))
    logpath = ''.join(
        [logdir, config.target_name, "_", config.network, "_", config.BACKBONE, "_", config.loss, date_time])

    tb_log = TensorBoard(log_dir=logpath)
    callable = [model_checkpoint, model_earlystop, model_reduceLR, model_history, tb_log]

    # train_set, val_set = get_train_val(out["sampleDir"], config.val_rate)
    # train_numb = len(train_set) * config.sample_per_img
    # valid_numb = len(val_set) * config.sample_per_img
    # print("the number of train data is", train_numb)
    # print("the number of val data is", valid_numb)

    # if isinstance(gpu_id, int):
    #     print("using single gpu {}".format(gpu_id))
    #     pass
    # elif isinstance(gpu_id, list):
    #     print("using multi gpu {}".format(gpu_id))
    #     if len(gpu_id) > 1:
    #         model = multi_gpu_model(model, gpus=len(gpu_id))

    self_optimizer = SGD(lr=config.lr, decay=1e-6, momentum=0.9, nesterov=True)
    if 'adagrad' in config.optimizer:
        self_optimizer = Adagrad(lr=config.lr, decay=1e-6)
    elif 'adam' in config.optimizer:
        self_optimizer = Adam(lr=config.lr, decay=1e-6, beta_1=0.9, beta_2=0.999, epsilon=1e-8)
    else:
        pass

    try:
        my_loss = eval("sm.losses." + config.loss)
        my_metrics = eval("sm.metrics." + config.metrics)
        model.compile(self_optimizer, loss=my_loss, metrics=['accuracy', my_metrics])
    except:
        print("model compile error")
        exit(-5)
    finally:
        print("Compile model successfully!")

    train_h5_file = out["sampleDir"]
    try:
        with h5py.File(train_h5_file, 'r') as f:
            print("trainVal file:{}".format(train_h5_file))
            Y = f['Y_train']
            V=f['Y_val']
            train_numb = len(Y)*config.sample_per_img
            valid_numb = len(V)*config.sample_per_img
            H = model.fit_generator(generator=train_data_generator_h5(config, f),
                                    steps_per_epoch=train_numb // config.batch_size,
                                    epochs=config.epochs,
                                    verbose=1,
                                    validation_data=val_data_generator_h5(config, f),
                                    validation_steps=valid_numb // config.batch_size,
                                    callbacks=callable,
                                    max_q_size=1,
                                    class_weight='auto')
            model.save(last_model)
            print("Training finished!")
    except:
        print("opening {} failed or train error".format(train_h5_file))
        return -4

import fire
if __name__ == '__main__':

    # train(
    #     send_massage_callback=send_message_callback,
    #     configs='/media/omnisky/e0331d4a-a3ea-4c31-90ab-41f5b0ee2663/traindata/scrs_building/config_binary_buiding_fpn_2.json',
    #     gpu=1,
    #     samples='',
    #     outdir='',
    #     baseModel=''
    # )

    fire.Fire()








