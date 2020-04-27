

import h5py
import os,sys
from ulitities.base_functions import load_label, load_src, find_file
import fire
import numpy as np


def create_h5_from_samples(sampleDir, h5SavingPath, val_rate=0.25, mode=0):
    # Create a new file
    # f = h5py.File(h5SavingPath, 'w')
    file_type = ['.jpg', '.png', '.tif', '.img']
    sample_url = []
    train_url = []
    train_set = []
    val_set = []
    for pic in os.listdir(sampleDir + '/label'):
        if not (str.lower(os.path.splitext(pic)[1]) in file_type):
            print("d")
        src=find_file(sampleDir + '/label',pic)
        if len(src)==0:
            continue
        filename = os.path.split(src)[1]
        sample_url.append(filename)
    total_num = len(sample_url)
    val_num = int(val_rate * total_num + 0.5)
    if val_num < 1:
        val_num = 1
    for i in range(len(sample_url)):
        if i < val_num:
            val_set.append(sample_url[i])
        else:
            train_set.append(sample_url[i])
    X=[]
    Y=[]
    W=[]
    V=[]
    tmp = load_label(sampleDir + '/label/'+sample_url[0])
    a,b=tmp.shape
    ts=load_label(sampleDir + '/label/'+sample_url[1])
    c,d=ts.shape

    """选更大的图像作为样本的参考尺寸"""
    if c>a and d>b:
        tmp=ts
    for url in train_set:
        label_data = load_label(sampleDir + '/label/'+url)
        if isinstance(label_data,int):
            continue
        if tmp.shape!=label_data.shape:
            print("Warining:data dimension is not equal:{}".format(url))
            continue
        src_data = load_src(sampleDir + '/src/'+url, mode=mode)
        if isinstance(src_data,int):
            continue
        else:
            print("loading:{}".format(url))
        X.append(src_data)
        Y.append(label_data)

    for url in val_set:
        label_val = load_label(sampleDir + '/label/' + url)
        if isinstance(label_val, int):
            continue
        if tmp.shape!=label_val.shape:
            print("Warining:data dimension is not equal:{}".format(url))
            continue
        src_val = load_src(sampleDir + '/src/' + url, mode=mode)
        if isinstance(src_val, int):
            continue
        else:
            print("loading:{}".format(url))
        W.append(src_val)
        V.append(label_val)
    # X = np.array(X)
    # Y=np.array(Y)
    # W=np.array(W)
    # V=np.array(V)
    with h5py.File(h5SavingPath,'r') as f:
        f = h5py.File(h5SavingPath, 'w')
        f.create_dataset('X_train', data=X)
        f.create_dataset('Y_train', data=Y)
        f.create_dataset('X_val', data=W)
        f.create_dataset('Y_val', data=V)
    # f.close()
    return 0

if __name__=='__main__':
    # create_h5_from_samples(r'H:\20200423\train', r'D:\data\samples\tuitiantu\tainval.h5', mode=0)

    fire.Fire()


