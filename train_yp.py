# coding=utf-8
import os, sys, json, random, time, argparse
import segmentation_models as sm
from keras.callbacks import ModelCheckpoint, EarlyStopping, History,ReduceLROnPlateau
from keras.layers import *
from keras.optimizers import *
from keras import backend as K
from keras.callbacks import TensorBoard
from keras.utils import multi_gpu_model
from ulitities.base_functions import UINT16, UINT8, UINT10
from deeplab.model import Deeplabv3
from data_prepare.data_generater import train_data_generator,val_data_generator
from config import Config

K.set_image_dim_ordering('tf')
seed = 4
print(np.random.seed(seed))


parser=argparse.ArgumentParser(description='RS classification train')
parser.add_argument('--sample', dest='sample_dir', help='the path of source and label file',
                         default='')
parser.add_argument('--model', dest='model_dir', help='path to storage model',
                         default='')
parser.add_argument('--gpu', dest='gpu_id', help='GPU device id to use [0]', nargs='+',
                        default="0", type=int)
parser.add_argument('--config', dest='config_file', help='json file to config',
                         default='config_multiclass_global.json')
args=parser.parse_args()
with open(args.config_file, 'r') as f:
    cfg = json.load(f)
config = Config(**cfg)
print(args.sample_dir)

def get_parameters():

    if not os.path.isdir(config.train_data_path):
        print ("train data does not exist in the path:\n {}".format(config.train_data_path))
        sys.exit(-1)

    if len(config.band_list)==0:
        print("Error: band_list should not be empty!")
        sys.exit(-2)

    'get gpuid'
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

    FLAG_MAKE_TEST=True

    "get image type"
    if '10' in config.im_type:
        im_type=UINT10
    elif '16' in config.im_type:
        im_type=UINT16
    else:
        im_type = UINT8

    "get image bands"
    band_name=''
    if len(config.band_list)==0:
        band_name='fullbands'
    else:
        for i in range(len(config.band_list)):
             band_name +=str(config.band_list[i])
        band_name+="bands"
    "config the model dir"
    if not os.path.isdir(config.model_dir):
        os.mkdir(config.model_dir)


    date_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    model_save_path = ''.join([config.model_dir,'/',config.target_name, '_', config.network, '_',config.BACKBONE,'_',
                               config.loss,'_',config.optimizer,'_',str(config.img_w), '_',band_name,'_', date_time, 'best.h5'])
    last_model = ''.join([config.model_dir,'/',config.target_name, '_', config.network, '_',config.BACKBONE,'_',
                          config.loss,'_',config.optimizer,'_',str(config.img_w), '_',band_name,'_', date_time, 'last.h5'])


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
def train(model,gpu_id,model_save_path,last_model):

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
    date_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
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
        my_loss = eval("sm.losses."+config.loss)
        my_metrics = eval("sm.metrics." + config.metrics)
        model.compile(self_optimizer, loss=my_loss, metrics=['accuracy',my_metrics])
    except:
        print("model compile error")
        exit(-5)
    finally:
        print("Compile model successfully!")

    H = model.fit_generator(generator=train_data_generator(config, train_set),
                            steps_per_epoch=train_numb // config.batch_size,
                            epochs=config.epochs,
                            verbose=1,
                            validation_data=val_data_generator(config, val_set),
                            validation_steps=valid_numb // config.batch_size,
                            callbacks=callable,
                            max_q_size=1,
                            class_weight='auto')

    model.save(last_model)

if __name__ == '__main__':

    input_layer = (config.img_w,config.img_h, len(config.band_list))
    if 'unet' in config.network:
        model = sm.Unet(backbone_name=config.BACKBONE, input_shape=input_layer,
                 classes=config.nb_classes, activation=config.activation,
                 encoder_weights=config.encoder_weights)
    elif 'pspnet' in config.network:
        model = sm.PSPNet(backbone_name=config.BACKBONE, input_shape=input_layer,
                     classes=config.nb_classes, activation=config.activation,
                     encoder_weights=config.encoder_weights,psp_dropout=config.dropout)
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
    print("Train by : {}_{}".format(config.network, config.BACKBONE))
    """ Training model........"""
    train(model)
    print("[Info]:test model...")









