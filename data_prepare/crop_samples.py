import os,sys,fire
import numpy as np
import cv2
import gdal
# import gc
gdal.UseExceptions()
from tqdm import tqdm
from ulitities.base_functions import get_file, load_img_by_gdal, find_file,send_message_callback

def Simple_Crop(send_message_callback=send_message_callback,inputdir="",outputdir="",patch_size=3000):
    if not os.path.isdir(inputdir):
        send_message_callback("Error: input directory is not existed")
        sys.exit(-1)
    if not os.path.isdir(outputdir):
        send_message_callback("Warning: output directory is not existed")
        os.mkdir(outputdir)
    out_label_dir=outputdir+'/label/'
    if not os.path.isdir(out_label_dir):
        os.mkdir(out_label_dir)

    out_src_dir = outputdir + '/src/'
    if not os.path.isdir(out_src_dir):
        os.mkdir(out_src_dir)
    label_list, img_list =[], []

    label_files, _=get_file(inputdir+'/label')

    for label_file in tqdm(label_files):
        absname = os.path.split(label_file)[1]
        absname = absname.split('.')[0]
        src_file = find_file(inputdir+'/src', absname)
        if not os.path.isfile(src_file):
            print("src file does not exist:{}".format(os.path.split(label_file)[1]))
            continue
        label_data = load_img_by_gdal(label_file,grayscale=True)
        if len(label_data)==0:
            print("label can not be loaded:{}".format(os.path.split(label_file)[1]))
            continue
        src_data = load_img_by_gdal(src_file)
        if len(label_data) == 0:
            print("src can not be loaded:{}".format(os.path.split(label_file)[1]))
            continue
        try:
            dataset = gdal.Open(src_file)
        except RuntimeError:
            send_message_callback("Warning: open file failed:{}".format(src_file))
            dataset = gdal.Open(src_file)
        else:
            print("Prompt: opened:{}".format(src_file))

        d_type = dataset.GetRasterBand(1).DataType
        del dataset

        send_message_callback("Cropping : " + absname)
        label = np.asarray(label_data, np.uint8)
        img = np.asarray(src_data, np.uint8)
        if label.shape[:2] != img.shape[:2]:
            print("the size of label and src are not equal:{}".format(absname))
            continue
        h, w, c = img.shape
        patch_size = int(patch_size)
        if h // patch_size == 0 or w // patch_size == 0:
            crop_label = label
            crop_img = img

            ret = cv2.imwrite(out_label_dir + absname + '.png', crop_label)
            if ret==None:
                ret = cv2.imencode('.png', crop_label)[1].tofile(out_label_dir + absname + '.png')
            if ret==False:
                print("Warning: saving label failed")
                continue
            driver = gdal.GetDriverByName("GTiff")
            try:
                outdataset = driver.Create(out_src_dir + absname + '.png', w, h, c, d_type)
            except:
                print("create gdal dataset failed for :{}".format(absname))
                continue
            finally:
                print("create gdal dataset successfully for :{}".format(absname))

            if outdataset == None:
                print("create dataset failed!\n")
                sys.exit(-2)
            if c == 1:
                outdataset.GetRasterBand(1).WriteArray(crop_img)
            else:
                for s in range(c):
                    outdataset.GetRasterBand(s + 1).WriteArray(crop_img[:, :, s])
            del outdataset
        else:
            for i in range(h // patch_size):
                for j in range(w // patch_size):
                    if i == h // patch_size:
                        crop_label = label[i * patch_size:h, j * patch_size:(j + 1) * patch_size]
                        crop_img = img[i * patch_size:h, j * patch_size:(j + 1) * patch_size, :]
                    elif j == w // patch_size:
                        crop_label = label[i * patch_size:(i + 1) * patch_size, j * patch_size:w]
                        crop_img = img[i * patch_size:(i + 1) * patch_size, j * patch_size:w, :]
                    else:
                        crop_label = label[i * patch_size:(i + 1) * patch_size, j * patch_size:(j + 1) * patch_size]
                        crop_img = img[i * patch_size:(i + 1) * patch_size, j * patch_size:(j + 1) * patch_size, :]

                    crop_label=np.asarray(crop_label, np.uint8)
                    uniq_value = np.unique(crop_label)
                    if len(uniq_value)< 2 and ((0 in uniq_value) or (255 in uniq_value)):
                        print("Warning: no target in this patch")
                        continue
                    t_h, t_w = crop_label.shape
                    newName = absname + '_' + str(i) + '_' + str(j) + '.png'
                    ret = cv2.imwrite(out_label_dir + newName, crop_label)
                    if ret == None:
                        ret=cv2.imencode('.png',crop_label)[1].tofile(out_label_dir + newName)
                    if ret==False:
                        print("saving label failed")
                        continue
                    driver = gdal.GetDriverByName("GTiff")
                    try:
                        outdataset = driver.Create(out_src_dir + newName, t_w, t_h, c, d_type)
                    except:
                        print("create gdal dataset failed for :{}".format(absname))
                        continue
                    finally:
                        print("create gdal dataset successfully for :{}".format(absname))
                    if outdataset == None:
                        print("create dataset failed!\n")
                        sys.exit(-2)
                    if c == 1:
                        outdataset.GetRasterBand(1).WriteArray(crop_img)
                    else:
                        for s in range(c):
                            outdataset.GetRasterBand(s + 1).WriteArray(crop_img[:, :, s])
                    del outdataset

    # img_files =[]
    # for file in label_files:
    #     absname = os.path.split(file)[1]
    #     absname = absname.split('.')[0]
    #     img_f = find_file(inputdir+'/src',absname)
    #     img_files.append(img_f)
    # # img_files = list()
    # # img_files, _=get_file(inputdir+'/src')
    # assert(len(label_files)==len(img_files))
    # name_list =[]
    # for i,file in enumerate(label_files):
    #     l_img = load_img_by_gdal(file, grayscale=True)
    #     if len(l_img)==0:
    #         continue
    #     # label_list.append(l_img)
    #     absname = os.path.split(file)[1]
    #     only_name = absname.split('.')[0]
    #     name_list.append(only_name)
    #     # src_file = inputdir+'/src/'+absname
    #
    #     s_img = load_img_by_gdal(img_files[i])
    #     if len(s_img)==0:
    #         continue
    #     img_list.append(s_img)
    #     label_list.append(l_img)
    #
    # # assert(len(label_list)==len(img_list))
    # try:
    #     dataset = gdal.Open(img_files[0])
    # except RuntimeError:
    #     send_message_callback("Warning: open file failed:{}".format(img_files[0]))
    #     dataset=gdal.Open(img_files[1])
    # else:
    #     print("Prompt: opened:{}".format(img_files[0]))
    #
    # d_type = dataset.GetRasterBand(1).DataType
    # del dataset
    # # print(img_list)
    # # print(label_list)
    # for i in tqdm(range(len(label_list))):
    #     only_name = name_list[i]
    #     send_message_callback("Cropping : " + only_name)
    #     label=np.asarray(label_list[i], np.uint8)
    #     img=np.asarray(img_list[i], np.uint8)
    #     if label.shape[:2]!=img.shape[:2]:
    #         print("the size of label and src are not equal:{}".format(only_name))
    #
    #         continue
    #     h,w,c = img.shape
    #     patch_size = int(patch_size)
    #     if h//patch_size==0 or w//patch_size==0:
    #         crop_label = label
    #         crop_img = img
    #
    #         cv2.imwrite(out_label_dir+only_name+'.png', crop_label)
    #         driver = gdal.GetDriverByName("GTiff")
    #         outdataset = driver.Create(out_src_dir+only_name+'.png', w, h, c, d_type)
    #         if outdataset == None:
    #             print("create dataset failed!\n")
    #             sys.exit(-2)
    #         if c == 1:
    #             outdataset.GetRasterBand(1).WriteArray(crop_img)
    #         else:
    #             for s in range(c):
    #                 outdataset.GetRasterBand(s + 1).WriteArray(crop_img[:,:,s])
    #         del outdataset
    #     else:
    #         for i in range(h//patch_size):
    #             for j in range(w//patch_size):
    #                 if i==h//patch_size:
    #                     crop_label = label[i * patch_size:h, j * patch_size:(j + 1) * patch_size]
    #                     crop_img = img[i * patch_size:h, j * patch_size:(j + 1) * patch_size, :]
    #                 elif j==w//patch_size:
    #                     crop_label = label[i * patch_size:(i + 1) * patch_size, j * patch_size:w]
    #                     crop_img = img[i * patch_size:(i + 1) * patch_size, j * patch_size:w, :]
    #                 else:
    #                     crop_label = label[i*patch_size:(i+1)*patch_size, j*patch_size:(j+1)*patch_size]
    #                     crop_img = img[i*patch_size:(i+1)*patch_size, j*patch_size:(j+1)*patch_size,:]
    #
    #                 t_h,t_w = crop_label.shape
    #                 cv2.imwrite(out_label_dir + only_name+'_'+str(i)+'_'+str(j) + '.png', crop_label)
    #                 driver = gdal.GetDriverByName("GTiff")
    #                 outdataset = driver.Create(out_src_dir + only_name + '_'+str(i)+'_'+str(j) +'.png', t_w, t_h, c, d_type)
    #                 if outdataset == None:
    #                     print("create dataset failed!\n")
    #                     sys.exit(-2)
    #                 if c == 1:
    #                     outdataset.GetRasterBand(1).WriteArray(crop_img)
    #                 else:
    #                     for s in range(c):
    #                         outdataset.GetRasterBand(s + 1).WriteArray(crop_img[:,:,s])
    #                 del outdataset

if __name__=="__main__":
    fire.Fire()