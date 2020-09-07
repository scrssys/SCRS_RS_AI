import tkinter
import  argparse
import json, time,gdal,osgeo,osr,numpy
raster = gdal.Open(r"D:\data\00000000\2019-12-27_18-16-01\T47RQN_20180120T035049.tif")

print("sre")
parser=argparse.ArgumentParser(description='RS classification train')
parser.add_argument('--gpu', dest='gpu_id', help='GPU device id to use [0]',
                        default=5, type=int)
parser.add_argument('--config', dest='config_file', help='json file to config',
                         default='config_multiclass_global.json')
args=parser.parse_args()
gpu_id=args.gpu_id
print("gpu_id:{}".format(gpu_id))

# win = tkinter.Tk()
# win.title("yudanqu")
# win.geometry("400x400+200+50")
# label1 = tkinter.Label(win, text="good", bg="blue")
# label2 = tkinter.Label(win, text="nice", bg="red")
# label3 = tkinter.Label(win, text="cool", bg="green")
# label4 = tkinter.Label(win, text="handsome", bg="yellow")
# label1.grid(row=0,column=0)
# label2.grid(row=0,column=1)
# label3.grid(row=1,column=0)
# label4.grid(row=1,column=1)
# win.mainloop()

def select_Out_Path():
    import tkinter.filedialog
    path_o = tkinter.filedialog.askdirectory()
    path_out.set(path_o.replace("/","\\"))
def select_In_Path():
    import tkinter.filedialog
    path_i = tkinter.filedialog.askdirectory()
    path_in.set(path_i.replace("/","\\"))
def  processCallback():
    pass

window = tkinter.Tk()
window.geometry('300x100')
path_out = tkinter.Variable()
path_in = tkinter.Variable()
lable_in = tkinter.Label(window,text = "输入路径")
lable_in.grid(row=1, column=0)

lable_out = tkinter.Label(window,text = "输出路径")
lable_out.grid(row=2, column=0)

e1 = tkinter.Entry(window, textvariable = path_in)
e1.grid(row=1, column = 1)
e2 = tkinter.Entry(window, textvariable = path_out)
e2.grid(row=2, column = 1)
b1 = tkinter.Button(window, text = "打开",command = select_In_Path)
b1.grid(row = 1, column=3,)
b2 = tkinter.Button(window, text = "打开",command = select_Out_Path)
b2.grid(row=2, column=3)
b_process = tkinter.Button(window, text="开始处理",command = processCallback)
b_process.grid(row=3, column=3)
# tkinter.messagebox.showinfo(title='Hi', message='开始处理')
window.mainloop()


