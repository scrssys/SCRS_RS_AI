from PyQt5.QtCore import QThread
from ui.tmp.hapImg import HapImg

class myThread(QThread):
    def __init__(self,file,canvas):
        super(myThread,self).__init__()
        # m_viwer=None
        self.fileName=file
        self.canvas=canvas

    def run(self):
        print('check in myThread\n')
        # bAns =False
        imgt=HapImg(self.canvas)
        imgt.load(self.fileName)