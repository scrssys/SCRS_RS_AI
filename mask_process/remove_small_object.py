import fire,os,sys
import numpy as np
from tqdm import tqdm
from skimage import io,morphology
from keras.utils import to_categorical
import cv2
from ulitities.base_functions import get_file,send_message_callback,load_label
def post_process_segment(inf,outf,Flag_cv=True, minsize=10, area_threshold=1000):
    # pass
    # import cv2
    img = load_label(inf)
    print(np.unique(img))
    NB = len(np.unique(img))-1
    if Flag_cv:
        kernel = np.ones((minsize,minsize),np.uint8)
        opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
        cv2.imwrite(outf,closing)
    else:
        # NB=1
        if NB >1:
            NB+=1
            try:
                # label= to_categorical(img,num_classes=NB,dtype='uint8')
                label = to_categorical(img)
            except:
                print("Failed when to transform one hot")
                return -1
            result_list = []
            for i in range(NB):
                t = remove_small_objects_and_holes(label[:, :, i], minsize*10, area_threshold, True)
                result_list.append(t[:,:,None])

            label = np.concatenate(result_list, axis=2)
            label = np.argmax(label, axis=2).astype(np.uint8)
        else:
            label =img
            label= remove_small_objects_and_holes(label, minsize*10, area_threshold, True)
            label = np.asarray(label,np.uint8)
        cv2.imwrite(outf, label)

def remove_small_objects_and_holes(label,min_size, area_threshold, in_place=True):
    label=morphology.remove_small_objects(label==1,min_size=min_size, connectivity=1,in_place=in_place)
    label=morphology.remove_small_holes(label==1,area_threshold=area_threshold,connectivity=1,in_place=in_place)
    return label



def batch_rmovesmallobj(send_message_callback,inputdir,outputdir,flag_cv=True,msize=5, thd=1000):
    if not os.path.isdir(inputdir):
        send_message_callback("Please check input directory:{}".format(inputdir))
        sys.exit(-1)
    if not os.path.isdir(outputdir):
        send_message_callback('Warning: output directory is not existed')
        os.mkdir(outputdir)
    files,_=get_file(inputdir)
    for file in files:#tqdm(files):
        send_message_callback("Dealing with : "+file)
        absname = os.path.split(file)[1]
        outputfile = os.path.join(outputdir, absname)
        post_process_segment(file, outputfile,Flag_cv=flag_cv, minsize=msize, area_threshold=thd)
if __name__ == "__main__":
    # batch_rmovesmallobj(r"C:\Users\SCRS\Pictures\111",r"C:\Users\SCRS\Pictures\222")
    # inputfile='/home/omnisky/PycharmProjects/data/samples/isprs/train_ori/label_all/top_potsdam_7_13.tif'
    # outputfile='/media/omnisky/e0331d4a-a3ea-4c31-90ab-41f5b0ee2663/traindata/scrs_building/test/crfss/whole48-tt.tif'
    # post_process_segment(inputfile,outputfile, Flag_cv=False, minsize=10)

    fire.Fire()