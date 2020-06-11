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

from ulitities.base_functions import UINT16, UINT8, UINT10

seed = 4
np.random.seed(seed)
from data_prepare.data_generater import train_data_generator,val_data_generator,train_data_generator_files,val_data_generator_files
from config import Config

from palaeoild_models.classical_models import classical_unet, classical_fcnnet,classical_segnet

parser=argparse.ArgumentParser(description='RS classification train')
parser.add_argument('--gpu', dest='gpu_id', help='GPU device id to use [0]', nargs='+',
                        default=4, type=int)
# parser.add_argument('--config', dest='config_file', help='json file to config',
#                          default='config_binary_whu_buildings.json')
parser.add_argument('--config', dest='config_file', help='json file to config',
                         default='')
args=parser.parse_args()
gpu_id=args.gpu_id
print("gpu_id:{}".format(gpu_id))
if isinstance(gpu_id,int):
    os.environ["CUDA_VISIBLE_DEVICES"]=str(gpu_id)
elif isinstance(gpu_id,list):
    tp_str =[]
    for i in gpu_id:
        tp_str.append(str(i))
    ns = ",".join(tp_str)
    os.environ["CUDA_VISIBLE_DEVICES"] = ns
else:
    pass


with open(args.config_file, 'r') as f:
    cfg = json.load(f)

config = Config(**cfg)
print("config file: {}".format(args.config_file))
print(config)


# loss = sm.losses.dice_loss(class_weights=np.array(config.class_weights))
# print(loss)


FLAG_MAKE_TEST=True
im_type=UINT8
if '10' in config.im_type:
    im_type=UINT10
elif '16' in config.im_type:
    im_type=UINT16
else:
    pass

date_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
print("date and time: {}".format(date_time))
print("traindata from: {}".format(config.train_data_path))
band_name=''
if len(config.band_list)==0:
    band_name='fullbands'
else:
    for i in range(len(config.band_list)):
         band_name +=str(config.band_list[i])
    band_name+="bands"
print("band_name:{}".format(band_name))
if not os.path.isdir(config.model_dir):
    print("Warning: model saveing directory is empty!")
    os.mkdir(config.model_dir)
model_save_path = ''.join([config.model_dir,'/',config.target_name, '_', config.network, '_',config.BACKBONE,'_',config.loss,'_',config.optimizer,'_',str(config.img_w), '_',band_name,'_', date_time, 'best.h5'])
print("model save as to: {}".format(model_save_path))
last_model = ''.join([config.model_dir,'/',config.target_name, '_', config.network, '_',config.BACKBONE,'_',config.loss,'_',config.optimizer,'_',str(config.img_w), '_',band_name,'_', date_time, 'last.h5'])

"""get the train file name and divide to train and val parts"""
def get_train_val(val_rate=config.val_rate):
    file_type = ['.png', '.PNG', '.tif', '.img', '.IMG']
    train_url = []
    train_set = []
    val_set = []
    for pic in os.listdir(config.train_data_path + '/label'):
        if (os.path.splitext(pic)[1] in file_type):
            train_url.append(pic)
    random.shuffle(train_url)
    total_num = len(train_url)
    val_num = int(val_rate * total_num+0.5)
    if val_num<1:
        val_num=1
    for i in range(len(train_url)):
        if i < val_num:
            val_set.append(train_url[i])
        else:
            train_set.append(train_url[i])
    return train_set, val_set



"""Train model ............................................."""
def train(model):

    if os.path.isfile(config.base_model):
        try:
            model.load_weights(config.base_model)
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
        patience=config.patience+10,
        verbose=0,
        mode=config.mode
    )

    # """自动调整学习率"""
    model_reduceLR=ReduceLROnPlateau(
        monitor=config.monitor,
        factor=config.factor,
        patience=config.patience,
        verbose=0,
        mode=config.mode,
        epsilon=config.epsilon,
        cooldown=config.cooldown,
        min_lr=config.min_lr
    )

    model_history = History()

    logdir = os.path.split(args.config_file)[0] + '/log/'
    if not os.path.isdir(logdir):
        print("warning: log dir is not exit")
        os.mkdir(logdir)
    logdir = ''.join([config.log_dir,'/log',config.target_name,"_", config.network,"_",config.BACKBONE,"_", config.loss, date_time])
    if not os.path.isdir(logdir):
        print("Warning: ")
        os.mkdir(logdir)

    tb_log = TensorBoard(log_dir=logdir)
    callable = [model_checkpoint,model_earlystop, model_reduceLR, model_history, tb_log]

    train_set, val_set = get_train_val()
    train_numb = len(train_set)*config.sample_per_img
    valid_numb = len(val_set)*config.sample_per_img
    print ("the number of train data is", train_numb)
    print ("the number of val data is", valid_numb)

    if isinstance(gpu_id,int):
        print("using single gpu {}".format(gpu_id))
        pass
    elif isinstance(gpu_id,list):
        print("using multi gpu {}".format(gpu_id))
        if len(gpu_id)>1:
            model = multi_gpu_model(model, gpus=len(gpu_id))

    self_optimizer = SGD(lr=config.lr, decay=1e-6, momentum=0.9, nesterov=True)
    if 'adagrad' in config.optimizer:
        self_optimizer = Adagrad(lr=config.lr, decay=1e-6)
    elif 'adam' in config.optimizer:
        self_optimizer = Adam(lr=config.lr, decay=1e-6, beta_1=0.9, beta_2=0.999, epsilon=1e-8)
    else:
        pass

    try:
        my_loss = config.loss
        # my_metrics = eval(config.metrics)
        model.compile(self_optimizer, loss=my_loss, metrics=['accuracy'])
    except:
        print("model compile error")
        exit(-5)
    finally:
        print("Compile model successfully!")

    H = model.fit_generator(generator=train_data_generator_files(config, config.train_data_path, train_set),
                            steps_per_epoch=train_numb // config.batch_size,
                            epochs=config.epochs,
                            verbose=1,
                            validation_data=val_data_generator_files(config, config.train_data_path, val_set),
                            validation_steps=valid_numb // config.batch_size,
                            callbacks=callable,
                            max_q_size=1,
                            class_weight='auto')

    model.save(last_model)

if __name__ == '__main__':

    if not os.path.isdir(config.train_data_path):
        print ("train data does not exist in the path:\n {}".format(config.train_data_path))
        sys.exit(-1)

    if len(config.band_list)==0:
        print("Error: band_list should not be empty!")
        sys.exit(-2)
    input_layer = (config.img_w,config.img_h, len(config.band_list))
    input_bands=len(config.band_list)

    #test classical_unet
    if "unet" in config.network:
        model = classical_unet(config.img_w,config.img_h,input_bands,config.nb_classes)
    elif "fcns" in config.network:
        model = classical_fcnnet(config.img_w,config.img_h,input_bands,config.nb_classes)
    elif "segnet" in config.network:
        model = classical_segnet(config.img_w, config.img_h, input_bands, config.nb_classes)
    else:
        print("Error: network is wrong!")
        sys.exit(-6)


    print(model.summary())
    print("Train by : {}".format(config.network))
    #
    # model=add_new_model(model, config)
    # print(model.summary())

    """ Training model........"""
    train(model)

    print("[Info]:test model...")
    # model_save_path = '/media/omnisky/b1aca4b8-81b8-4751-8dee-24f70574dae9/bieshu/models/20190731/bieshu_pspnet_inceptionresnetv2_binary_crossentropy_adam_480_012bands_2019-08-01_11-24-18best.h5'
    # test(model_save_path,config)








