#import RPi.GPIO as GPIO
import time
import sys,cv2,os
from PyQt5.QtWidgets import QApplication, QWidget ,QMainWindow, QSizePolicy, QDesktopWidget, QTableWidgetItem , QMessageBox
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from pyzbar.pyzbar import decode
from datetime import datetime
import csv
import pandas as pd
import numpy as np
#import EasyPySpin as es

# class dialog1(QWidget):
#     def __init__(self):
#         super().__init__()
#         uic.loadUi("MVS/Prototype_2/dia1.ui",self)
#         self.ApplyDia1.clicked.connect(self.getpinnum)
#         self.CancelDia1.clicked.connect(self.close)

#     def getpinnum(self):
#         value=int(self.PinNumDia1.currentText())
#         print(value)
#         print(type(value))

#     def cnc(self):
#         self.close()

# class dialog2(QWidget):
#     def __init__(self):
#         super().__init__()
#         uic.loadUi("MVS/Prototype_2/dia2.ui",self)
#         self.ApplyDia2.clicked.connect(self.getpinnum)
#         self.CancelDia2.clicked.connect(self.close)
    
#     def getpinnum(self):
#         value=int(self.PinNumDia2.currentText())
#         print(value)
#         print(type(value))

#     def cnc(self):
#         self.close()

class Settings(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("MVS/Prototype_2/set.ui",self)
        self.CancelBtn.clicked.connect(self.cancl)
        self.OkBtn.clicked.connect(self.cancl)
        # self.AddBtn.clicked.connect(self.add)
        # self.RemoveBtn.clicked.connect(self.rem)
        
    # def add(self):
    #     dia1.show()

    # def rem(self):
    #     dia2.show()

    def cancl(self):
        self.close()

class Library(QWidget):
    def __init__(self):
        super().__init__()
        self.row=0
        uic.loadUi("MVS/Prototype_2/lib.ui",self)
        self.Header.setColumnWidth(0,30)
        self.Header.setColumnWidth(3,130)
        self.LogFile_Btn.clicked.connect(self.log)
        self.Cancel_Btn.clicked.connect(self.cncl)
        self.Search_Btn.clicked.connect(self.search)  
        self.Clear_Btn.clicked.connect(self.clr)
    
    def log(self):
        os.startfile('MVS\Prototype_2\LogFile.csv')
 
    def search(self):
        self.Data_View.addItem('ASAD')

    def cncl(self):
        self.close()
    
    def clr(self):
        self.Data_View.clear()

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("MVS/Prototype_2/prop_2.ui",self)
        self.listW=''
        self.count=0
        self.flog=False
        self.centre()
        self.Imaging_Btn.clicked.connect(self.imging)
        self.Library_Btn.clicked.connect(self.libr)
        self.Obs_Header.setColumnWidth(0,50)
        self.Obs_Header.setColumnWidth(1,120)
        self.Obs_Header.setColumnWidth(2,120)
        self.Worker1 = Worker1()
        self.Worker1.ImageUpdate.connect(self.ImageUpdateSlot)
        self.Worker1.listUpdate.connect(self.observe)
        self.Enable_Radio.toggled.connect(self.enable)
        self.Disable_Radio.toggled.connect(self.disable)
        self.IDs=self.Worker1.ProdIDs
        # self.Exposure_Edit.valueChanged.connect(lambda:  self.spin_method())
    
    def enable(self):
        # self.count=0  
        self.flog=True 
        self.Worker1.start()
           
    def disable(self):
        #self.count=0
        self.flog=False
        self.Worker1.stop()

    def observe(self,data):
        
        self.count+=1
        self.keyslist=list(self.IDs.keys())
        self.valueslist=list(self.IDs.values())
        self.position1=[self.valueslist.index(i) for i in self.valueslist if i[0]==int(data)]
        self.listW=f'{self.count}: \t PASSED \t      ({data}) : {self.keyslist[self.position1[0]]}       {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        self.listWidget.addItem(self.listW)
        self.asas=[data,self.keyslist[self.position1[0]],datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        self.inv=pd.read_csv("MVS\Prototype_2\Inventory.csv")
        self.inv.loc[(int(data))-1,"Amount"]+=1
        self.inv.loc[(int(data))-1,"Recent_Entry"]=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.inv.to_csv("MVS\Prototype_2\Inventory.csv",index=False)

        with open("MVS\Prototype_2\LogFile.csv",'a',newline='') as f:
            w=csv.writer(f)
            w.writerow(self.asas)
            f.close()
        


    def spin_method(self):
        value = self.Exposure_Edit.value()
        #Worker1.ExpVal=value
    
    def imging(self):
        if not self.flog:
            im.show()
        else:
            msg=QMessageBox.warning(self,'Warning','Disable Live Feed to Proceed')
    
    def libr(self):
        if not self.flog:
            libb.show()
        else:
            msg=QMessageBox.warning(self,'Warning','Disable Live Feed to Proceed')
        
    def centre(self):
        qr=self.frameGeometry()
        cp=QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def ImageUpdateSlot(self, Image):
        self.Camera_Feedlabel.setPixmap(QPixmap.fromImage(Image))

class Worker1(QThread):
    
    '''Class Level Variables and Flags'''
    Detected=[]
    Sens1_Count=-1
    Sens2_Count=-1
    Flag=False
    bbox=None
    ImageUpdate = pyqtSignal(QImage)
    listUpdate = pyqtSignal(str)
    
    '''List of PRODUCTS
       dType--> Dictionary
       Assigning Format--> 'NAME':(AssignedID,AssignedPin)
    '''

    ProdIDs= {
        
            'Article 1':(1,21),
            'Article 2':(2,19),
            'Article 3':(3,26)
        }

    '''*RASPBERRY PI 4 GPIO PIN SETUP*'''
    
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(21,GPIO.OUT)
    # GPIO.output(21,GPIO.LOW)
    # GPIO.setup(19,GPIO.OUT)
    # GPIO.output(19,GPIO.LOW)
    # GPIO.setup(26,GPIO.OUT)
    # GPIO.output(26,GPIO.LOW)

    def run(self):
        self.ThreadActive=True
        SenseFlag= False
        Box_Flag= False

        tracker=cv2.legacy.TrackerCSRT_create()
        arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_1000)
        arucoParams = cv2.aruco.DetectorParameters_create()
        
        self.Capture = cv2.VideoCapture(0)
        self.Capture.set(cv2.CAP_PROP_EXPOSURE,8000)
        self.Capture.set(cv2.CAP_PROP_APERTURE,2)
        self.Capture.set(cv2.CAP_PROP_AUTOFOCUS,100)
        self.Capture.set(cv2.CAP_PROP_AUTO_EXPOSURE,-1)
        self.Capture.set(cv2.CAP_PROP_BACKLIGHT,5000)
        self.Capture.set(cv2.CAP_PROP_BRIGHTNESS,3200)
        self.Capture.set(cv2.CAP_PROP_GAIN,20)
        
        while self.ThreadActive:
            self.Flag = False
            ret, self.frame = self.Capture.read()
            if ret:
                Image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                Pic = ConvertToQtFormat.scaled(640,480, Qt.KeepAspectRatio)
                self.ImageUpdate.emit(Pic)
                
                
                # if GPIO.input() and not SenseFlag:
                #     SenseFlag=True
                #     Sens1_Count+=1
                #     if self.Detected[Sens1_Count]==1:
                #         GPIO.output(self.Detected[Sens1_Count],GPIO.HIGH)
                #         self.Detected.pop(Sens1_Count)
                #     else:
                #         continue
                # if GPIO.input() and not SenseFlag:
                #     continue
                # if GPIO.input() and SenseFlag:
                #     SenseFlag=False
                #     GPIO.output(self.Detected[Sens1_Count],GPIO.HIGH)
                # else:
                #     continue
                
                corners,id,_ = cv2.aruco.detectMarkers(Image,arucoDict,parameters=arucoParams)
                if id is not None and len(id)>0:
                    markercorners = corners[0][0]
                    bbox=cv2.boundingRect(markercorners)
                    tracker.init(Image,bbox)
                    if bbox is not None:
                        success, bbox= tracker.update(Image)
                        if success:
                            bbox = tuple(map(int,bbox))
                            cv2.rectangle(Image, bbox, (0,225,0),2)
                            cv2.putText(Image,'Tracking',(bbox[0],bbox[1]-10),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,225,0),2)
                        else:
                            bbox=None
                #cv2.aruco.drawDetectedMarkers(Image,corners)
                #print(id)
                
                if id is not None and not Box_Flag :
                    Box_Flag=True
                    print(id[0][0])
                    for i in self.ProdIDs.values():
                        if id[0][0] == i[0]:
                            print('Signal Generated')
                            #GPIO.output(i[1],GPIO.HIGH)
                            self.listUpdate.emit(str(i[0]))
                            self.Detected.append(i[0])
                            
                
                elif id is not None and Box_Flag:
                    continue
                
                elif id is None and Box_Flag:
                    Box_Flag=False
                
                else:
                    continue

                # for code in decode(Image):
                #     print(code.data.decode('utf-8'))
        self.Capture.release()

    def close(self):
        cv2.destroyAllWindows()

    def stop(self):
        self.ThreadActive = False

'''-------------------------------------------------------------------------------------------------------------'''

app=QApplication([])
app.setStyle("Fusion")    
obj=Window()
im=Settings() 
libb=Library()
# dia1=dialog1()
# dia2=dialog2()         
print("Done successfully")
obj.show()        
sys.exit(app.exec())