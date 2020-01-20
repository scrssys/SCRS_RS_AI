
import os, sys
import gdal
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from ulitities.base_functions import get_file

class_types = [[255, 255, 255], [0, 0, 255], [0, 255, 255], [0, 255, 0], [255, 255, 0], [255, 0, 0]]

input_dir='/home/omnisky/PycharmProjects/data/samples/isprs/test/pred/2020-01-18_17-49-46'
output_dir='/home/omnisky/PycharmProjects/data/samples/isprs/test/results'

if __name__=='__main__':
    print("Info: starting to get final mask...")

    files,_=get_file(input_dir)
    for file in tqdm(files):
        file_name = os.path.split(file)[1]
        img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        a,b = img.shape
        mask = np.zeros((img.shape[0],img.shape[1],3),np.uint8)
        for i in range(len(class_types)):
            index = np.where(img==i)
            mask[index[0],index[1],0]=class_types[i][2]
            mask[index[0], index[1], 1] = class_types[i][1]
            mask[index[0], index[1], 2] = class_types[i][0]

        # plt.imshow(mask)
        # plt.show()

        output_file = os.path.join(output_dir, file_name)
        cv2.imwrite(output_file, mask)






