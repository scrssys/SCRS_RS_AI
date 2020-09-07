


import os, sys

import cv2

import numpy as np
import matplotlib.pyplot as plt


# base_file = '/home/omnisky/PycharmProjects/data/samples/global/test/result-pspnet/binary/bce-dice-loss/2020-02-26_15-18-28-road-bce-dice/zy304016420151108.tif'
# CHANGE_BASE=True
# base_value = 4

insert_file ='/home/omnisky/PycharmProjects/data/samples/global/test/result-pspnet/binary/dice/2020-02-28_10-12-17-road-dice/zy304016420151108.tif'
insert_value =4

combine_file = '/home/omnisky/PycharmProjects/data/samples/global/test/result-pspnet/binary/dice/combine-yes.tif'

if __name__=="__main__":
    if not os.path.isfile(insert_file):
        print("One or Two of input files do not exist")
        sys.exit(-1)
    insert_data = cv2.imread(insert_file, cv2.IMREAD_GRAYSCALE)
    insert_data = np.array(insert_data, np.uint8)

    if os.path.isfile(combine_file):
        try:
            base_data = cv2.imread(combine_file, cv2.IMREAD_GRAYSCALE)
            base_data = np.array(base_data, np.uint8)
        except:
            print("combine file open failed:{}".format(combine_file))
            sys.exit(-2)
    else:
        base_data=np.zeros(insert_data.shape, np.uint8)

    if base_data.shape[0]!=insert_data.shape[0] or base_data.shape[1]!=insert_data.shape[1]:
        print("The dimensions of input images are not equal")
        sys.exit(-3)
    # out_data = np.zeros(base_data.shape,np.uint8)

    # "change the target class value in base image"
    # if CHANGE_BASE:
    #     index = np.where(base_data==1)
    #     base_data = np.zeros(base_data.shape, np.uint8)
    #     base_data[index] = base_value
    print("unique values in base image: {}".format(np.unique(base_data)))

    tmp = np.unique(insert_data)
    print("unique values in insert image: {}".format(np.unique(insert_data)))

    if len(tmp)>2:
        print("insert image has more than 3 classes")
        sys.exit(-3)
    else:
        if not 1 in tmp:
            print("no target whose value = 2 in insert image")
            sys.exit(-3)
    index_add = np.where(insert_data==1)
    base_data[index_add]=insert_value
    print("valid value in result:{}".format(np.unique(base_data)))

    plt.figure()
    plt.imshow(base_data)
    plt.show()
    cv2.imwrite(combine_file,base_data)



