import os, sys
import cv2
import operator
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
from ulitities.base_functions import get_file

class_types = [[255, 0, 0],[255, 255, 255], [0, 0, 255], [0, 255, 255], [0, 255, 0], [255, 255, 0]]

input_dir = '/home/omnisky/PycharmProjects/data/samples/isprs/original/5_Labels_all'
output_dir = '/home/omnisky/PycharmProjects/data/samples/isprs/original/5_labels_gray'
if __name__ == '__main__':

    try:
        print("Info: transform label to grey image")
        # print(len(class_types))
        # print(class_types[0])
        files, _ = get_file(input_dir)

        for file in tqdm(files):
            file_name = os.path.split(file)[1]

            img = cv2.imread(file)
            # plt.imshow(img)
            # plt.show()
            # img = np.array(img)
            # img = np.transpose(img, (2,0,1))
            # rgb_img=img
            rgb_img = np.zeros(img.shape, np.uint8)
            rgb_img[:, :, 0] = img[:, :, 2]
            rgb_img[:, :, 1] = img[:, :, 1]
            rgb_img[:, :, 2] = img[:, :, 0]

            # plt.figure(2)
            # plt.imshow(rgb_img)
            # plt.show()

            a, b, c = rgb_img.shape
            tgt = np.zeros((rgb_img.shape[0], rgb_img.shape[1]), np.uint8)
            for i in range(len(class_types)):
                for j in range(a):
                    for k in range(b):
                        tmp = [rgb_img[j, k, 0], rgb_img[j, k, 1], rgb_img[j, k, 2]]
                        if operator.eq(tmp, class_types[i]):
                            tgt[j, k] = i

            output_file = os.path.join(output_dir, file_name)
            cv2.imwrite(output_file, tgt)

    finally:
        # print("Press keyboard of Enter to exit")
        input("Press keyboard of Enter to exit")
