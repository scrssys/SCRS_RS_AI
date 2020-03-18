import fire,os,sys,numpy
from tqdm import tqdm
from skimage import io,morphology
from ulitities.base_functions import get_file,load_img_by_gdal
def remove_small_obj(inf,outf,minsize):
    pass
    # img = load_img_by_gdal()
    import cv2
    img = cv2.imread(inf)
    kernel = numpy.ones((5,5),numpy.uint8)
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    cv2.imwrite(outf,closing)
    img = io.imread(inf)
    cv2.imwrite(outf, img)
    # img_ = morphology.remove_small_holes(img,800)
def batch_rmovesmallobj(inputdir,outputdir,minsize=5):
    if not os.path.isdir(inputdir):
        print("Please check input directory:{}".format(inputdir))
        sys.exit(-1)
    if not os.path.isdir(outputdir):
        print('Warning: output directory is not existed')
        os.mkdir(outputdir)
    files,_=get_file(inputdir)
    for file in tqdm(files):
        absname = os.path.split(file)[1]
        outputfile = os.path.join(outputdir, absname)
        remove_small_obj(file, outputfile,minsize)
if __name__ == "__main__":
    # batch_rmovesmallobj(r"C:\Users\SCRS\Pictures\111",r"C:\Users\SCRS\Pictures\222")
    fire.Fire()