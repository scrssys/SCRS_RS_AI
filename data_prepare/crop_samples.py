import os,sys,cv2,gdal,fire
import numpy as np
gdal.UseExceptions()
from tqdm import tqdm
from ulitities.base_functions import get_file, load_img_by_gdal, find_file


inputdir = 'D:/data/0918_cloudsaple_zy3/0919cloud'
outputdir = 'D:/data/0918_cloudsaple_zy3/tes'
patch_size=2000
def get_seglist(w,h,p_size):
    '''
    wait for completion
    :param w:
    :param h:
    :param p_size:
    :return:
    '''

    seg_list=[]
    n_x = w//p_size
    n_y = h//p_size
    if n_x==0 and n_y==0:
        seg_list=[[w,h]]
    if n_x==0 and n_y > 0:
        last_h = h-p_size
        seg_list = h
    if n_x > 0 and n_y ==0:
        last_w = w- p_size
    if n_x>0 and n_y >0:
        last_h = h - p_size
        last_w = w - p_size

    return seg_list
def Simple_Crop(inputdir,outputdir,patch_size=2000):
    if not os.path.isdir(inputdir):
        print("Error: input directory is not existed")
        sys.exit(-1)
    if not os.path.isdir(outputdir):
        print("Warning: output directory is not existed")
        os.mkdir(outputdir)
    out_label_dir=outputdir+'/label/'
    out_src_dir = outputdir + '/src/'

    label_list, img_list =[], []

    label_files, _=get_file(inputdir+'/label')
    img_files =[]
    for file in label_files:
        absname = os.path.split(file)[1]
        absname = absname.split('.')[0]
        img_f = find_file(inputdir+'/src',absname)
        img_files.append(img_f)

    assert(len(label_files)==len(img_files))
    name_list =[]
    for i,file in enumerate(label_files):
        l_img = load_img_by_gdal(file, grayscale=True)
        if len(l_img)==0:
            continue
        label_list.append(l_img)
        absname = os.path.split(file)[1]
        only_name = absname.split('.')[0]
        name_list.append(only_name)

        s_img = load_img_by_gdal(img_files[i])
        if len(s_img)==0:
            continue
        img_list.append(s_img)
    try:
        dataset = gdal.Open(img_files[0])
    except RuntimeError:
        print("Warning: open file failed:{}".format(img_files[0]))
        dataset=gdal.Open(img_files[1])
    else:
        print("Prompt: opened:{}".format(img_files[0]))

    d_type = dataset.GetRasterBand(1).DataType
    # del dataset
    # print(img_list)
    # print(label_list)
    for i in tqdm(range(len(label_list))):
        only_name = name_list[i]
        print("deal: {}".format(only_name))
        label=np.asarray(label_list[i], np.uint8)
        img=np.asarray(img_list[i], np.uint8)
        assert(label.shape[:2]==img.shape[:2])
        h,w,c = img.shape
        if h//patch_size==0 or w//patch_size==0:
            crop_label = label
            crop_img = img

            cv2.imwrite(out_label_dir+only_name+'.png', crop_label)
            driver = gdal.GetDriverByName("GTiff")
            outdataset = driver.Create(out_src_dir+only_name+'.png', w, h, c, d_type)
            if outdataset == None:
                print("create dataset failed!\n")
                sys.exit(-2)
            if c == 1:
                outdataset.GetRasterBand(1).WriteArray(crop_img)
            else:
                for s in range(c):
                    outdataset.GetRasterBand(s + 1).WriteArray(crop_img[:,:,s])
            del outdataset
        else:
            for i in range(h//patch_size):
                for j in range(w//patch_size):
                    if i==h//patch_size:
                        crop_label = label[i * patch_size:h, j * patch_size:(j + 1) * patch_size]
                        crop_img = img[i * patch_size:h, j * patch_size:(j + 1) * patch_size, :]
                    elif j==w//patch_size:
                        crop_label = label[i * patch_size:(i + 1) * patch_size, j * patch_size:w]
                        crop_img = img[i * patch_size:(i + 1) * patch_size, j * patch_size:w, :]
                    else:
                        crop_label = label[i*patch_size:(i+1)*patch_size, j*patch_size:(j+1)*patch_size]
                        crop_img = img[i*patch_size:(i+1)*patch_size, j*patch_size:(j+1)*patch_size,:]

                    t_h,t_w = crop_label.shape
                    cv2.imwrite(out_label_dir + only_name+'_'+str(i)+'_'+str(j) + '.png', crop_label)
                    driver = gdal.GetDriverByName("GTiff")
                    outdataset = driver.Create(out_src_dir + only_name + '_'+str(i)+'_'+str(j) +'.png', t_w, t_h, c, d_type)
                    if outdataset == None:
                        print("create dataset failed!\n")
                        sys.exit(-2)
                    if c == 1:
                        outdataset.GetRasterBand(1).WriteArray(crop_img)
                    else:
                        for s in range(c):
                            outdataset.GetRasterBand(s + 1).WriteArray(crop_img[:,:,s])
                    del outdataset
if __name__=='__main__':
    # Simple_Crop(inputdir,outputdir)
    fire.Fire()