from PyQt5.Qt import (QThread)
from PyQt5.QtCore import QTimer,QEventLoop,pyqtSignal
from PyQt5.QtWidgets import QApplication
from ulitities.base_functions import echoRuntime
from predict import predict
from ui.main_gui import mywindow,Signal
import logging,time

class main_thread(QThread):
    main_signal = pyqtSignal()
    add_massage = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.s=Signal()

    @echoRuntime
    def run_predict(self,config,*args):
        print("predict is runing")
        print(config)
        print(args[2])
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s [%(levelname)s] at %(filename)s,%(lineno)d: %(message)s',
                            datefmt='%Y-%m-%d(%a)%H:%M:%S',
                            filename='out.txt',
                            filemode='w')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('[%(levelname)-8s] %(message)s')  # 屏显实时查看，无需时间
        console.setFormatter(formatter)
        logging.getLogger().addHandler(console)
        while 1:
        #     loop = QEventLoop()
        #     QTimer.singleShot(1000, loop.quit)
        #     loop.exec_()
        #     logging.debug('gubed');
        #     logging.info('ofni');
        #     logging.critical('lacitirc')
        # QApplication.processEvents()

        # predict(configs='/home/omnisky/PycharmProjects/data/rice/samples_uav1_crop_fpn/config_binary_global.json',
        #         gpu=2,
        #         input="/home/omnisky/PycharmProjects/data/rice/test/all0.1/image",
        #         output = "/home/omnisky/PycharmProjects/data/rice/test/pred/fpn",
        #         model = "/home/omnisky/PycharmProjects/data/rice/models/fpn/rice_uav1_null_fpn_seresnet34_binary_crossentropy_adam_480_012bands_2020-03-25_15-49-16best.h5")

        # predict(config,args[0],args[1],args[2],args[3])
        #     self.add_massage(time.time())
            time.sleep(1)
            print("begin")
            self.s.add_message.emit("myhhhyuu")
        self.main_signal.emit()
class write_test(mywindow):
    def OutputWritten(self):
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText("\n,smsmh\n")
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()
