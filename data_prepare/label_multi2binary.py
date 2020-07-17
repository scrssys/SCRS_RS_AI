import os,sys
import numpy as np
import matplotlib.pyplot as plt
import cv2
from tqdm import tqdm
from ulitities.base_functions import get_file


inputdir = '/home/omnisky/PycharmProjects/data/tree/isprs/label_all'
outputdir = '/home/omnisky/PycharmProjects/data/tree/isprs/label_binary'
target_class=[1,2,3,4,5]

if __name__=='__main__':
    if not os.path.isdir(inputdir):
        print("Error: input directory is not existed")
        sys.exit(-1)
    if not os.path.isdir(outputdir):
        print("Warning: output directory is not existed")
        os.mkdir(outputdir)

    for t in tqdm(target_class):
        files,_ = get_file(inputdir)

        s_dir = os.path.join(outputdir,('t_'+str(t)))
        if not os.path.exists(s_dir):
            os.mkdir(s_dir)

        for file in files:
            label = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
            label = np.array(label,np.uint8)
            # plt.figure("s")
            # plt.imshow(label,cmap="flag")
            # plt.show()
            if not t in np.unique(label):
                print("no label {} in {}".format(t, file))
                continue
            else:
                out_file = os.path.join(s_dir,os.path.split(file)[1])
                data = np.zeros(label.shape,np.uint8)
                index = np.where(label==t)
                data[index]=1
                # plt.figure(2)
                # plt.imshow(data)
                # plt.show()
                # print("sdf")
                cv2.imwrite(out_file,data)

