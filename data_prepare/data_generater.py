
import numpy as np
import random
from PIL import Image
from keras.utils.np_utils import to_categorical
from keras.preprocessing.image import img_to_array
from scipy.signal import medfilt, medfilt2d
from skimage import exposure
import matplotlib.pyplot as plt
import cv2
import sys
import h5py

from ulitities.base_functions import load_img_bybandlist, load_img_normalization,UINT8,UINT10,UINT16, load_label,load_src


def random_crop(img1, img2, crop_H, crop_W):

    # assert  img1.size[:2] ==  img2.size[:2]
    # print(img1.shape[:2])
    img1=np.asarray(img1,np.uint16)
    img2 = np.asarray(img2, np.uint16)
    if img1.shape[:2] != img2.shape[:2]:
        print("sizes of img1 and img2 are not equal")
        return -2
    h, w = img1.shape[:2]

    # 裁剪宽度不可超过原图可裁剪宽度
    if crop_W > w:
        crop_W = w
        # print("crop width is lager than img width")
    # 裁剪高度

    if crop_H > h:
        crop_H = h
        # print("crop height is lager than img height")

    # 随机生成左上角的位置
    x0 = random.randrange(0, w - crop_W + 1, 50)
    y0 = random.randrange(0, h - crop_H + 1, 50)

    try:
        crop_1 = img1[y0:y0+crop_H,x0:x0+crop_W, :]
    except:
        print("can not extract data from img")
    try:
        crop_2 = img2[y0:y0+crop_H,x0:x0+crop_W]
    except:
        print("can not extract data from label")

    return crop_1,crop_2

def rotate(xb, yb, angle):
    xb = np.rot90(np.array(xb), k=angle)

    yb = np.rot90(np.array(yb), k=angle)

    return xb, yb

def add_noise( xb, width, height, dtype=1):
    assert(xb.shape[-1]<xb.shape[0])
    if dtype == 1:
        noise_value = 255
    elif dtype == 2:
        noise_value = 1024
    else:
        noise_value = 25535

    tmp = np.random.random() / 20.0  # max = 0.05
    noise_num = int(tmp * width * height)
    for i in range(noise_num):
        temp_x = np.random.randint(0, xb.shape[0])
        temp_y = np.random.randint(0, xb.shape[1])
        xb[temp_x, temp_y,:] = noise_value
        # xb[:, temp_x, temp_y] = noise_value
    return xb


def gamma_tansform(xb, g=2.0):
    tmp = np.random.random() * g
    # print("gamma:{}".format(tmp))
    if tmp < 0.6:
        tmp = 0.6
    if tmp > 1.4:
        tmp = 1.4

    xb = exposure.adjust_gamma(xb, tmp)
    return xb

def med_filtering(xb, w=3):
    xb = np.asarray(xb,np.float32)
    _, _, bands = xb.shape

    for i in range(bands):
        # cv2.imwrite('/home/omnisky/PycharmProjects/data/samples/isprs/test/orig.png',xb[:, :, i])
        try:
            # tmp = medfilt2d(xb[:, :, i], (w, w))
            tmp = cv2.medianBlur(xb[:, :, i],w)
        except:
            print("Waring: med_filter failed")
            return -1
        xb[:, :, i] =tmp
        # cv2.imwrite('/home/omnisky/PycharmProjects/data/samples/isprs/test/omedifid.png',xb[:, :, i])
        # sys.exit(-2)

    xb = np.asarray(xb, np.uint16)
    return xb

def data_augment(xb, yb, w, h, d_type=1):
    if np.random.random() < 0.25:
        assert (yb.shape[0] == yb.shape[1])
        assert (xb.shape[0] == xb.shape[1])
        xb, yb = rotate(xb, yb, 1)

    if np.random.random() < 0.25:
        xb, yb = rotate(xb, yb, 2)

    if np.random.random() < 0.25:
        assert (yb.shape[0] == yb.shape[1])
        assert (xb.shape[0] == xb.shape[1])
        xb, yb = rotate(xb, yb, 3)

    if np.random.random() < 0.25:
        # xb = np.transpose(xb, (1, 2, 0))
        xb = np.fliplr(xb)  # flip an array horizontally
        # xb = np.transpose(xb, (2, 0, 1))
        yb = np.fliplr(yb)

    if np.random.random() < 0.25:
        # xb = np.transpose(xb, (1, 2, 0))
        xb = np.flipud(xb)  # flip an array vertically (up down directory)
        # xb = np.transpose(xb, (2, 0, 1))
        yb = np.flipud(yb)

    if np.random.random() < 0.25:  # gamma adjust
        tmp = np.random.random() * 2
        xb = gamma_tansform(xb,tmp)

    if np.random.random() < 0.25:  # medium filtering
        if np.random.random() < 0.25:
            xb = med_filtering(xb, 5)
        else:
            xb = med_filtering(xb,3)
        if isinstance(xb ,int):
            return -1, -1

    if np.random.random() < 0.2:
        xb = add_noise(xb, w, h, d_type)
    return xb, yb


def resample_data(img, dst_h, dst_w, mode = Image.ANTIALIAS, bits=8):
    if len(img.shape)>2:
        if bits==8:
            n_img = np.zeros((dst_h, dst_w, img.shape[-1]), np.uint8)
            img = np.asarray(img, np.uint8)
            for i in range(img.shape[-1]):
                b_img = img[:, :, i]
                b_img = Image.fromarray(b_img, mode='L')
                b_img = b_img.resize((dst_h, dst_w), mode)
                b_img = np.array(b_img, np.uint8)
                n_img[:, :, i] = b_img[:, :]
            return n_img
        else:
            n_img = np.zeros((dst_h, dst_w, img.shape[-1]), np.uint16)
            img = np.asarray(img, np.uint32)
            for i in range(img.shape[-1]):
                b_img = img[:, :, i]
                # plt.figure()
                # plt.imshow(b_img, cmap='gray')
                # plt.show()
                b_img = Image.fromarray(b_img, mode='I')
                b_img = b_img.resize((dst_h, dst_w), mode)
                b_img = np.array(b_img, np.uint16)
                n_img[:, :, i] = b_img[:, :]
            return n_img
    else:
        img = Image.fromarray(img, mode='L')
        img = img.resize((dst_h, dst_w), mode)
        img = np.array(img, np.uint8)
        return img


# data for training from memory
def train_data_generator(config, sampth, sample_url):
    # print 'generateData...'
    norm_value =255.0
    bits_num=8
    if '10' in config.im_type:
        norm_value = 1024.0
        bits_num = 16
    elif '16' in config.im_type:
        norm_value = 25535.0
        bits_num = 16
    else:
        pass
    label_list,img_list = [], []
    for pic in sample_url:
        _,t_img = load_img_normalization(1,sampth+'/label/'+pic)
        tp = np.unique(t_img)
        if config.label_nodata in tp:
            print("Warning: contain nodata in label of {}".format(pic))
            continue
        # if len(tp) < 2:
        #     print("Only one value {} in {}".format(tp, sampth+'/label/'+pic))
        #     if tp[0] == 0:
        #         print("no target value in {}".format(sampth+'/label/'+pic))
        #         continue

        ret, s_img = load_img_bybandlist((sampth + '/src/' + pic), bandlist=config.band_list)
        if ret!=0:
            continue

        s_img = img_to_array(s_img)
        s_img = np.asarray(s_img, np.uint16)
        # plt.imshow(s_img[:,:,0])
        # plt.show()
        img_list.append(s_img)
        label_list.append(t_img)
    assert len(label_list) == len(img_list)

    train_data = []
    train_label = []
    batch = 0
    while True:
        if batch==0:  # 防止训练集图像数量少于batch_size
            train_data = []
            train_label = []

        for i in np.random.permutation(np.arange(len(img_list))):
            try:
                src_img=img_list[i]
            except:
                print("can not extract data from img")
            try:
                label_img=label_list[i]
            except:
                print("can not extract data from label")
            random_size = random.randrange(config.img_w, config.img_w*2+1, config.img_w)
            # random_size = config.img_w
            img, label = random_crop(src_img, label_img, random_size, random_size)

            if config.label_nodata in np.unique(label):
                continue
            """ignore pure background area"""
            if len(np.unique(label)) < 2:
                if (0 in np.unique(label)) and (np.random.random() < 0.75):
                    continue

            if img.shape[1] != config.img_w or img.shape[0] != config.img_h:
                # print("resize samples")
                img = resample_data(img,config.img_h,config.img_w,mode=Image.BILINEAR, bits=bits_num)
                label=resample_data(label, config.img_h, config.img_w,mode=Image.NEAREST)
                # if (len(np.unique(label))>config.nb_classes):
                index = np.where(label >= config.label_nodata )
                label[index]=0

            if config.augment:
                img, label = data_augment(img,label,config.img_w,config.img_h)
                if isinstance(img, int):
                    print("warning: something wrong in data_augment")
                    continue

            img = np.asarray(img,np.float16)/norm_value
            img = np.clip(img, 0.0, 1.0)

            batch +=1
            img = img_to_array(img)
            label=img_to_array(label)
            train_data.append(img)
            train_label.append(label)
            if batch%config.batch_size==0:
                train_data = np.array(train_data)
                train_label = np.array(train_label)
                # print("img shape:{}".format(train_data.shape))
                # print("label shap:{}".format(train_label.shape))
                if config.nb_classes > 2:
                    train_label = to_categorical(train_label, num_classes=config.nb_classes)
                yield (train_data, train_label)
                train_data = []
                train_label = []
                batch = 0

##new data_generator from files
def train_data_generator_files(config, sampth, sample_url):
    # print 'generateData...'
    norm_value =255.0
    bits_num=8
    if '10' in config.im_type:
        norm_value = 1024.0
        bits_num = 16
    elif '16' in config.im_type:
        norm_value = 25535.0
        bits_num = 16
    else:
        pass
    # random.shuffle(sample_url)
    train_data = []
    train_label = []
    batch = 0

    while True:
        if batch==0:  # 防止训练集图像数量少于batch_size
            train_data = []
            train_label = []
        random.shuffle(sample_url)
        for pic in sample_url:
            label_img = load_label(sampth+'/label/'+pic)
            if isinstance(label_img,int):
                print("load label failed:{}".fomat(pic))
                continue
            tp = np.unique(label_img)
            if config.label_nodata in tp:
                print("Warning: contain nodata in label of {}".format(pic))
                continue
            # if len(tp) < 2:
            #     # print("Only one value {} in {}".format(tp, sampth + '/label/' + pic))
            #     if tp[0]==config.label_nodata:
            #         # print("only nodata value in {}".format(sampth + '/label/' + pic))
            #         continue

            src_img = load_src((sampth + '/src/' + pic), bandlist=config.band_list)
            if isinstance(src_img, int):
                print("load src failed:{}".format(pic))
                continue
            # print("using data from :{}".format(pic))
            random_size = random.randrange(config.img_w, config.img_w*2+1, config.img_w)
            # random_size = config.img_w
            img, label = random_crop(src_img, label_img, random_size, random_size)
            """ignore nodata img"""
            # if config.label_nodata in np.unique(label):
            #     continue
            """ignore pure background area"""
            if len(np.unique(label)) < 2:
                if (0 in np.unique(label)) and (np.random.random() < 0.75):
                    continue

            if img.shape[1] != config.img_w or img.shape[0] != config.img_h:
                # print("resize samples")
                img = resample_data(img,config.img_h,config.img_w,mode=Image.BILINEAR, bits=bits_num)
                label = resample_data(label, config.img_h, config.img_w, mode=Image.NEAREST)
                # if (len(np.unique(label))>config.nb_classes):
                index = np.where(label >= config.label_nodata )
                label[index]=0

            if config.augment:
                img, label = data_augment(img,label,config.img_w,config.img_h)
                if isinstance(img, int):
                    print("warning: something wrong in data_augment")
                    continue

            img = np.asarray(img, np.float16)/norm_value
            img = np.clip(img, 0.0, 1.0)

            batch +=1

            img = img_to_array(img)
            label=img_to_array(label)
            train_data.append(img)
            train_label.append(label)
            if batch%config.batch_size==0:
                train_data = np.array(train_data)
                train_label = np.array(train_label)
                # print("img shape:{}".format(train_data.shape))
                # print("label shap:{}".format(train_label.shape))
                if config.nb_classes > 2:
                    train_label = to_categorical(train_label, num_classes=config.nb_classes)
                yield (train_data, train_label)
                train_data = []
                train_label = []
                batch = 0

# data for training from memory
def train_data_generator_h5(config, f):
    # print 'generateData...'
    norm_value =255.0
    bits_num=8
    if '10' in config.im_type:
        norm_value = 1024.0
        bits_num = 16
    elif '16' in config.im_type:
        norm_value = 25535.0
        bits_num = 16
    else:
        pass

    # try:
    #     f = h5py.File(sampth, 'r')
    # except:
    #     print("opening {} failed".format(sampth))
    # # X = f['X_train']
    Y = f['Y_train']
    # V=f['Y_val']
    num=len(Y)
    # num_val=len(V)

    train_data = []
    train_label = []
    batch = 0
    while True:
        if batch==0:  # 防止训练集图像数量少于batch_size
            train_data = []
            train_label = []

        idx = np.random.randint(num)
        # img_data=[]

        src_img=f['X_train'][idx][:,:,config.band_list]
        # cv2.imencode('.png', src_img)[1].tofile(r'H:\20200423\train\123band.png')  # for test

        label_img=f['Y_train'][idx]

        tp = np.unique(label_img)
        if config.label_nodata in tp:
            print("Warning: contain nodata in label of {}".format(pic))
            continue

        random_size = random.randrange(config.img_w, config.img_w*2+1, config.img_w)
        # random_size = config.img_w
        img, label = random_crop(src_img, label_img, random_size, random_size)

        # if config.label_nodata in np.unique(label):
        #     continue
        """ignore pure background area"""
        if len(np.unique(label)) < 2:
            if (0 in np.unique(label)) and (np.random.random() < 0.75):
                continue

        if img.shape[1] != config.img_w or img.shape[0] != config.img_h:
            # print("resize samples")
            img = resample_data(img,config.img_h,config.img_w,mode=Image.BILINEAR, bits=bits_num)
            label=resample_data(label, config.img_h, config.img_w,mode=Image.NEAREST)
            # if (len(np.unique(label))>config.nb_classes):
            index = np.where(label >= config.label_nodata )
            label[index]=0

        if config.augment:
            img, label = data_augment(img,label,config.img_w,config.img_h)
            if isinstance(img, int):
                print("warning: something wrong in data_augment")
                continue

        img = np.asarray(img, np.float16)/norm_value
        img = np.clip(img, 0.0, 1.0)

        batch +=1
        img = img_to_array(img)
        label=img_to_array(label)
        train_data.append(img)
        train_label.append(label)
        if batch%config.batch_size==0:
            train_data = np.array(train_data)
            train_label = np.array(train_label)
            # print("img shape:{}".format(train_data.shape))
            # print("label shap:{}".format(train_label.shape))
            if config.nb_classes > 2:
                train_label = to_categorical(train_label, num_classes=config.nb_classes)
            yield (train_data, train_label)
            train_data = []
            train_label = []
            batch = 0
            #close h5 file
    # f.close()


def val_data_generator(config,sampth, sample_url):
    # print 'generate validating Data...'
    norm_value = 255.0
    if '10' in config.im_type:
        norm_value = 1024.0
    elif '16' in config.im_type:
        norm_value = 25535.0
    else:
        pass
    w=config.img_w
    h=config.img_h
    label_list, img_list = [],[]
    for pic in sample_url:
        _, t_img = load_img_normalization(1, sampth + '/label/' + pic)
        tp = np.unique(t_img)

        if config.label_nodata in tp:
            print("Warning: contain nodata in label of {}".format(pic))
            continue

        # if len(tp) < 2:
        #     print("Only one value {} in {}".format(tp, sampth + '/label/' + pic))
        #     if tp[0] == 127:
        #         print("Ignore:nodata value in {}".format(sampth + '/label/' + pic))
        #         continue
        ret, s_img = load_img_bybandlist((sampth + '/src/' + pic), bandlist=config.band_list)
        if ret!=0:
            continue
        s_img = img_to_array(s_img)
        img_list.append(s_img)
        label_list.append(t_img)

    assert len(label_list) == len(img_list)

    train_data = []
    train_label = []
    batch = 0
    while True:
        if batch==0:
            train_data = []
            train_label = []
        # batch = 0
        for i in (range(len(img_list))):
            img = img_list[i]
            label = label_list[i]
            img = np.asarray(img, np.float16)/ norm_value
            img = np.clip(img, 0.0, 1.0)

            label = np.asarray(label)
            assert img.shape[0:2] == label.shape[0:2]

            for i in range(img.shape[0] // h):
                for j in range(img.shape[1] // w):
                    x = img[i * h:(i + 1) * h, (j * w):(j + 1) * w, :]
                    y = label[i * h:(i + 1) * h, (j * w):(j + 1) * w]

                    if config.label_nodata in np.unique(y):
                        continue
                    """ignore pure background area"""
                    if len(np.unique(y)) < 2:
                        if (0 in np.unique(y)) and (np.random.random() < 0.75):
                            continue

                    # x = np.asarray(x).astype(np.float32) / norm_value
                    # x = np.clip(x, 0.0, 1.0)

                    x = img_to_array(x)
                    y = img_to_array(y)
                    train_data.append(x)
                    train_label.append(y)

                    batch += 1
                    if batch % config.batch_size == 0:
                        train_data = np.array(train_data)
                        train_label = np.array(train_label)
                        if config.nb_classes > 2:
                            train_label = to_categorical(train_label, num_classes=config.nb_classes)
                        yield (train_data, train_label)
                        train_data = []
                        train_label = []
                        batch = 0

def val_data_generator_files(config,sampth, sample_url):
    # print 'generate validating Data...'
    norm_value = 255.0
    if '10' in config.im_type:
        norm_value = 1024.0
    elif '16' in config.im_type:
        norm_value = 25535.0
    else:
        pass
    w=config.img_w
    h=config.img_h
    label_list, img_list = [],[]
    # for pic in sample_url:
    #     _, t_img = load_img_normalization(1, sampth + '/label/' + pic)
    #     tp = np.unique(t_img)
    #     if len(tp) < 2:
    #         print("Only one value {} in {}".format(tp, sampth + '/label/' + pic))
    #         if tp[0] == 127:
    #             print("Ignore:nodata value in {}".format(sampth + '/label/' + pic))
    #             continue
    #     ret, s_img = load_img_bybandlist((sampth + '/src/' + pic), bandlist=config.band_list)
    #     if ret!=0:
    #         continue
    #     s_img = img_to_array(s_img)
    #     img_list.append(s_img)
    #     label_list.append(t_img)
    #
    # assert len(label_list) == len(img_list)

    train_data = []
    train_label = []
    batch = 0
    while True:
        if batch==0:
            train_data = []
            train_label = []
        # batch = 0

        for pic in sample_url:
            label = load_label(sampth + '/label/' + pic)
            if isinstance(label, int):
                print("load label failed:{}".fomat(pic))
                continue
            tp = np.unique(label)
            if config.label_nodata in tp:
                print("Warning: contain nodata in label of {}".format(pic))
                continue

            # if len(tp) < 2:
            #     # print("Only one value {} in {}".format(tp, sampth + '/label/' + pic))
            #     if tp[0] == config.label_nodata:
            #         # print("only nodata value in {}".format(sampth + '/label/' + pic))
            #         continue

            img = load_src((sampth + '/src/' + pic), bandlist=config.band_list)
            if isinstance(img, int):
                print("load src failed:{}".format(pic))
                continue
            if img.shape[0:2] != label.shape[0:2]:
                print("Warning: dimensions of label and src are not equal:{}".format(pic))
                continue

            img=np.asarray(img, np.float16)/norm_value
            img = np.clip(img, 0.0, 1.0)

            for i in range(img.shape[0] // h):
                for j in range(img.shape[1] // w):
                    x = img[i * h:(i + 1) * h, (j * w):(j + 1) * w, :]
                    y = label[i * h:(i + 1) * h, (j * w):(j + 1) * w]

                    if config.label_nodata in np.unique(y):
                        continue
                    """ignore pure background area"""
                    # if len(np.unique(y)) < 2:
                    #     if (0 in np.unique(y)) and (np.random.random() < 0.75):
                    #         continue
                    x = img_to_array(x)
                    y = img_to_array(y)
                    train_data.append(x)
                    train_label.append(y)

                    batch += 1
                    if batch % config.batch_size == 0:
                        train_data = np.array(train_data)
                        train_label = np.array(train_label)
                        if config.nb_classes > 2:
                            train_label = to_categorical(train_label, num_classes=config.nb_classes)
                        yield (train_data, train_label)
                        train_data = []
                        train_label = []
                        batch = 0



def val_data_generator_h5(config,f):
    # print 'generate validating Data...'
    norm_value = 255.0
    if '10' in config.im_type:
        norm_value = 1024.0
    elif '16' in config.im_type:
        norm_value = 25535.0
    else:
        pass
    w=config.img_w
    h=config.img_h

    # try:
    #     #     f = h5py.File(sampth, 'r')
    #     # except:
    #     #     print("opening {} failed".format(sampth))
    #     #     return -2
    V = f['Y_val']
    # V=f['Y_val']
    num=len(V)

    train_data = []
    train_label = []
    batch = 0
    while True:
        if batch==0:
            train_data = []
            train_label = []
        # batch = 0
        idx = np.random.randint(num)
        # img_data=[]

        try:
            src_img = f['X_val'][idx][:, :, config.band_list]
        except:
            print("no val data in h5 file")

        # cv2.imencode('.png', src_img)[1].tofile(r'H:\20200423\train\123band.png')  # for test

        label_img = f['Y_val'][idx]

        # for i in (range(len(img_list))):
        #     img = img_list[i]
        #     label = label_list[i]
        img = np.asarray(src_img, np.float16) / norm_value
        img = np.clip(img, 0.0, 1.0)

        label = np.asarray(label_img)
        assert img.shape[0:2] == label.shape[0:2]

        for i in range(img.shape[0] // h):
            for j in range(img.shape[1] // w):
                x = img[i * h:(i + 1) * h, (j * w):(j + 1) * w, :]
                y = label[i * h:(i + 1) * h, (j * w):(j + 1) * w]

                if config.label_nodata in np.unique(y):
                    continue
                """ignore pure background area"""
                if len(np.unique(y)) < 2:
                    if (0 in np.unique(y)) and (np.random.random() < 0.75):
                        continue
                x = img_to_array(x)
                y = img_to_array(y)
                train_data.append(x)
                train_label.append(y)

                batch += 1
                if batch % config.batch_size == 0:
                    train_data = np.array(train_data)
                    train_label = np.array(train_label)
                    if config.nb_classes > 2:
                        train_label = to_categorical(train_label, num_classes=config.nb_classes)
                    yield (train_data, train_label)
                    train_data = []
                    train_label = []
                    batch = 0
    # f.close()