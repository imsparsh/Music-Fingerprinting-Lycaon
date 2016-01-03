__author__ = 'imsparsh'

# import libraries
import PIL
from PIL import Image
import images_rc
from PyQt4 import QtCore, QtGui

import numpy, scipy, librosa, os, sys, time, gc, multiprocessing as mp
from fingerprint import *

# pymongo driver for MongoDB
from pymongo import *
from bson.objectid import ObjectId
from scipy import *

# metadata for scanning song info
from metadata import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class WindowLayout(QtGui.QWidget):
    def __init__(self):
        '''        initialize Main Window with Widgets        '''
        super(WindowLayout, self).__init__()
        
        # connect to dataBase
        cl = MongoClient('localhost',27017)
        self.dB = cl.lycaon_db
        
        # initialize Vertical Box Layout
        self.fp1 = QtGui.QVBoxLayout()
        self.fp2 = QtGui.QVBoxLayout()
        self.fp3 = QtGui.QVBoxLayout()

        # initialize main Box and add Layouts
        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(self.fp1)
        vbox.addLayout(self.fp2)
        vbox.addLayout(self.fp3)

        # set layout for Main Window
        self.setLayout(vbox)

        # set internal margin and spacing between widgets to zero
        vbox.setSpacing(0)
        vbox.setMargin(0)

        # initialize first Layout Activity
        self.fp_one()

        self.setObjectName(_fromUtf8("Wizard"))
        self.setGeometry(300,100,320,480) # set height, width, position
        self.move(QtGui.QApplication.desktop().screen().rect().center()- self.rect().center()) # reset position to center
        self.resize(320, 480)
        # fix height and width
        self.setMinimumSize(QtCore.QSize(320, 480))
        self.setMaximumSize(QtCore.QSize(320, 480))
        self.setWindowTitle(_translate("Wizard", "Lycaon Fingerprint", None)) # set Window Title

        # add icon to MainWindow | Taskbar Panel
        app_icon = QtGui.QIcon()
        app_icon.addFile('./icons/listen16.png', QtCore.QSize(16,16))
        app_icon.addFile('./icons/listen24.png', QtCore.QSize(24,24))
        app_icon.addFile('./icons/listen32.png', QtCore.QSize(32,32))
        app_icon.addFile('./icons/listen48.png', QtCore.QSize(48,48))
        app_icon.addFile('./icons/listen.png', QtCore.QSize(256,256))
        app_icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icon/images/listen.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(app_icon)

    # terminate all process on Escape keyPress
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            if 'self.proTerminate' in vars(): # check if fingerPrint is initiated
                if not self.proTerminate:
                    self.proTerminate = 1
                    self.pro.terminate() # terminate Child process
            self.close() # close MainWindow

    def fp_one(self):
        '''
        the first Layout
        '''

        WizardPage1 = QtGui.QWizardPage() # initialize Wizard Page as parent
        # set Wizard Properties
        WizardPage1.setObjectName(_fromUtf8("WizardPage1"))
        WizardPage1.setGeometry(0,0,320,480)
        WizardPage1.resize(320, 480)
        WizardPage1.setMinimumSize(QtCore.QSize(320, 480))
        WizardPage1.setMaximumSize(QtCore.QSize(320, 480))
        WizardPage1.setAutoFillBackground(False) # set Background to NULL
        WizardPage1.setStyleSheet(_fromUtf8("QWidget  {background: url(:/bg/images/bg.png); margin: 0;}")) # set custom background
        self.widget1 = QtGui.QWidget(WizardPage1) # initialize Main Widget
        # set Main Widget Occurrence Properties
        self.widget1.setGeometry(QtCore.QRect(0, 0, 320, 480))
        self.widget1.setObjectName(_fromUtf8("widget1"))
        
        # generate child widgets, set Properties
        self.label1 = QtGui.QLabel(self.widget1)
        self.label1.setGeometry(QtCore.QRect(0, 20, 321, 111))
        self.label1.setText(_fromUtf8(""))
        self.label1.setPixmap(QtGui.QPixmap(_fromUtf8(":/icon/images/logo1.png")))
        self.label1.setScaledContents(True)
        self.label1.setObjectName(_fromUtf8("label"))
        self.toolButton1 = QtGui.QToolButton(self.widget1)
        self.toolButton1.setGeometry(QtCore.QRect(0, 120, 321, 51))
        self.toolButton1.setStyleSheet(_fromUtf8("QToolButton { background: rgba(255,255,255,150); font: italic 20pt \"Monotype Corsiva\";}"))
        self.toolButton1.setObjectName(_fromUtf8("toolButton1"))
        self.pushButton1 = QtGui.QPushButton(self.widget1)
        self.pushButton1.setGeometry(QtCore.QRect(50, 390, 221, 61))
        self.pushButton1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton1.setStyleSheet(_fromUtf8("QPushButton {background:rgba(11,11,11,202); font: italic 18pt \"Monotype Corsiva\"; border-radius: 50px 0; color: white; }"))
        self.pushButton1.setObjectName(_fromUtf8("pushButton1"))
        self.plainTextEdit1 = QtGui.QPlainTextEdit(self.widget1)
        self.plainTextEdit1.setEnabled(True)
        self.plainTextEdit1.setGeometry(QtCore.QRect(10, 190, 301, 181))
        self.plainTextEdit1.setMaximumSize(QtCore.QSize(500, 1000))
        self.plainTextEdit1.setStyleSheet(_fromUtf8("QPlainTextEdit {background: rgba(87,74,76,150); border-radius: 10px; color: rgb(222,222,222); padding: 10px; font-size:14px} QScrollBar {background: gray}"))
        self.plainTextEdit1.setObjectName(_fromUtf8("plainTextEdit1"))
        #self.plainTextEdit1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # init Strings
        self.fileString = ''
        self.fullFileNames = ''
        
        # initialize Labels for the widgets
        WizardPage1.setWindowTitle(_translate("WizardPage1", "Lycaon", None))
        self.toolButton1.setText(_translate("WizardPage1", "Select Files", None))
        self.pushButton1.setText(_translate("WizardPage1", "FingerPrint", None))
        self.plainTextEdit1.setPlainText(_translate("WizardPage1", "No Files Selected", None))
        self.plainTextEdit1.setReadOnly(True) # set Editable to False
        QtCore.QMetaObject.connectSlotsByName(WizardPage1)

        self.fp1.addWidget(WizardPage1) # add Wizard Page to Layout

        # initialize Click Events
        self.connect(self.pushButton1, QtCore.SIGNAL("clicked()"), self.makeFingerprinting)
        self.connect(self.toolButton1, QtCore.SIGNAL("clicked()"), self.file_open)

    def file_open(self):
        '''
        open a file chooser and select multiple files
        '''
        filter_mask = "Music files (*.mp3)"
        openPath = 'C:/'
        # get full filenames along with path
        self.fullFileNames = QtGui.QFileDialog.getOpenFileNames(self, 'Select Files', openPath , filter_mask)
        # get individual filename in list
        self.fileNames = [aFile.split('\\')[-1] for aFile in self.fullFileNames]
        for aFile in self.fileNames:
            self.fileString += (aFile + '\n')
        if not self.fileString == '':
            self.plainTextEdit1.clear()
        self.plainTextEdit1.insertPlainText(self.fileString)

    def makeFingerprinting(self):
        '''
        check for selected files and format
        '''
        if not self.fullFileNames == '' and '.mp3' in self.fileNames[0]:
            self.fingerPrintFiles = []
            for aFile in self.fullFileNames:
                self.fingerPrintFiles.append(aFile)
            self.initFingerprint() # initialize fingerPrint
            self.fp_one_two()
        else:
            self.file_open()
        

    def initFingerprint(self):
        '''
        initialize the fingerPrint phase
        '''
        dBproject = self.dB.projections
        projections = dBproject.find() # extract random projections
        for cursor in projections:
            getItem = cursor[unicode('projections')]
        self.projections = array(eval(str(getItem.decode())))

    def fp_one_two(self):
        '''
        change Layout one to two
        '''
        self.remove_fp_one()
        self.fp_two()

    def fp_two(self):
        '''
        the second Layout
        '''

        WizardPage2 = QtGui.QWizardPage() # initialize Wizard Page as parent
        # set Wizard Properties
        WizardPage2.setGeometry(0,0,320,480)
        WizardPage2.setObjectName(_fromUtf8("WizardPage2"))
        WizardPage2.resize(320, 480)
        WizardPage2.setMinimumSize(QtCore.QSize(320, 480))
        WizardPage2.setMaximumSize(QtCore.QSize(320, 480))
        WizardPage2.setAutoFillBackground(False) # set background to NULL
        WizardPage2.setStyleSheet(_fromUtf8("QWidget  {background: url(:/bg/images/bg.png);}")) # set custom background
        self.widget2 = QtGui.QWidget(WizardPage2) # initialize Main Widget
        # set Main Widget Occurrence Properties
        self.widget2.setGeometry(QtCore.QRect(0, 0, 321, 481))
        self.widget2.setObjectName(_fromUtf8("widget2"))
        
        # generate child widgets, set Properties
        self.label2 = QtGui.QLabel(self.widget2)
        self.label2.setGeometry(QtCore.QRect(0, 20, 321, 111))
        self.label2.setPixmap(QtGui.QPixmap(_fromUtf8(":/icon/images/logo1.png")))
        self.label2.setScaledContents(True)
        self.label2.setObjectName(_fromUtf8("label2"))
        self.pushButton2 = QtGui.QPushButton(self.widget2)
        self.pushButton2.setGeometry(QtCore.QRect(80, 430, 151, 41))
        self.pushButton2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton2.setStyleSheet(_fromUtf8("QPushButton {background:rgba(11,11,11,142); font: italic 14pt \"Monotype Corsiva\"; border-radius: 50px 0; color: white; }"))
        self.pushButton2.setObjectName(_fromUtf8("pushButton2"))
        self.plainTextEdit2 = QtGui.QPlainTextEdit(self.widget2)
        self.plainTextEdit2.setEnabled(True)
        self.plainTextEdit2.setGeometry(QtCore.QRect(10, 230, 301, 181))
        self.plainTextEdit2.setMaximumSize(QtCore.QSize(500, 1000))
        self.plainTextEdit2.setStyleSheet(_fromUtf8("QPlainTextEdit {background: rgba(87,74,76,150); border-radius: 10px; color: rgb(222,222,222); padding: 10px; font-size:14px} QScrollBar {background: gray}"))
        self.plainTextEdit2.setPlainText(_fromUtf8(""))
        self.plainTextEdit2.setObjectName(_fromUtf8("plainTextEdit2"))
        self.songname = QtGui.QLabel(self.widget2)
        self.songname.setGeometry(QtCore.QRect(20, 120, 281, 21))
        self.songname.setStyleSheet(_fromUtf8("#songname {color: white; font: italic 15pt \"Monotype Corsiva\"; border-radius: 5px; padding: 0 5px; background: transparent}"))
        self.songname.setObjectName(_fromUtf8("songname"))
        self.progressBar = QtGui.QProgressBar(self.widget2)
        self.progressBar.setGeometry(QtCore.QRect(20, 150, 281, 23))
        self.progressBar.setStyleSheet(_fromUtf8("#progressBar {color: white}"))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.remainingSongs = QtGui.QLabel(self.widget2)
        self.remainingSongs.setGeometry(QtCore.QRect(20, 200, 281, 21))
        self.remainingSongs.setStyleSheet(_fromUtf8("#remainingSongs {color: white; padding: 0 5px; border-radius: 5px}"))
        self.remainingSongs.setObjectName(_fromUtf8("remainingSongs"))

        # initialize Labels for the widgets
        WizardPage2.setWindowTitle(_translate("WizardPage2", "Lycaon", None))
        self.pushButton2.setText(_translate("WizardPage2", "Cancel", None))
        self.remainingSongs.setText(_translate("WizardPage2", "Remaining Songs to be FingerPrinted..", None))
        self.plainTextEdit2.setReadOnly(True) # set Editable to False
        QtCore.QMetaObject.connectSlotsByName(WizardPage2)

        self.fp2.addWidget(WizardPage2) # add Wizard Page to Layout

        # initialize Click Events
        self.connect(self.pushButton2, QtCore.SIGNAL("clicked()"), self.fp_two_one)

        # initialize variables
        self.fileNames = [aFile.split('\\')[-1] for aFile in self.fingerPrintFiles]
        self.completedFiles = ''
        self.alreadyCompletedFiles = ''
        self.fileList = []
        for aFile in self.fileNames:
            self.fileList.append(aFile)

        self.proTerminate = 0
        start = time.time() #  timer start for fingerPrint
        for filepath in self.fingerPrintFiles:
            # if process termination is set
            if self.proTerminate:
                pass
            else:
                fpath = str(filepath.split('\\')[-1]) # get song name
                if not self.fileList == []: # check if at least one is selected
                    self.plainTextEdit2.clear()
                    del self.fileList[0]
                    for aStr in self.fileList:
                        self.plainTextEdit2.insertPlainText(aStr+'\n') # build the display String
                gc.collect() # garbage Collection

                # extract song metadata
                info = getSongInfo(str(filepath))
                songTitle = info['title']
                tempImage = ''
                if 'image' in info: # check if albumart exists
                    tempImage = info['image']
                    del info['image']
                checkSong = []

                # check if song already exists in dataBase
                getSong = self.dB.songInfo.find({'title':unicode(info['title'])},{'title':1,'_id':0})
                gc.collect()
                for cursor in getSong:
                    checkSong.append(cursor)
                # add the new song only if it does not exist previously
                if checkSong == []:
                    self.progressBar.setRange(0, 0) # initialize ProgressBar
                    self.completedFiles += (fpath + '\n')
                    self.songname.setText(QtCore.QString(songTitle))
                    self.songname.repaint() # refresh the view
                    
                    # insert song metadata
                    dbSong = self.dB.songInfo
                    songId = str(dbSong.insert(info))

                    if not os.path.isdir('albumart'): # check if albumart directory exist
                        os.mkdir('albumart')
                    self.imgName = './albumart/'+songId+'.jpg' # image name = ObjectId()
                    if not tempImage == '':
                        with open(self.imgName, 'wb') as img:
                            img.write(tempImage) # write artwork to new image 

                    del tempImage

                    # reduce the size of album art image to display properly..
                    basewidth = 400
                    img = Image.open(self.imgName)
                    wpercent = (basewidth/float(img.size[0]))
                    hsize = int((float(img.size[1])*float(wpercent)))
                    img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS) # resize all to same size
                    img.save(self.imgName) # write image
                    
                    '''
                    fingerprint(filepath, songId, self.projections)
                    multiprocessing module initiated for fingerPrinting
                    '''
                    self.pro = mp.Process(target=fingerprint, args=(str(filepath), songId, self.projections))
                    self.pro.start() # start the process
                    while self.pro.is_alive(): # refresh View
                        time.sleep(0.05)
                        QtGui.QApplication.processEvents()
                    if not self.proTerminate:
                        self.pro.join() # join the process to queue
                        self.progressBar.setRange(0, 1) # update ProgressBar
                    else:
                        # remove song metadata from dataBase if cancelled
                        dbSong.remove({'_id': ObjectId(songId)})
                        os.remove(self.imgName) # delete albumart
                else:
                    # if present, attach the name to String
                    self.alreadyCompletedFiles += (fpath + '\n')
                
                gc.collect() # flush memory
        
        stop = time.time() # timer stop for fingerPrint
        self.timeTaken = stop - start # total time spent to fingerPrint
        if not self.proTerminate:
            self.fp_two_three() # change Layout to three if all gets well

    def fp_two_one(self):
        '''
        change Layout two to one
        '''
        if not self.proTerminate:
            self.proTerminate = 1
            self.pro.terminate() # terminate process if cancelled
        self.remove_fp_two()
        self.fp_one()

    def fp_two_three(self):
        '''
        change Layout two to three
        '''
        self.remove_fp_two()
        self.fp_three()

    def fp_three(self):
        '''
        the third Layout
        '''

        WizardPage3 = QtGui.QWizardPage() # initialize Wizard Page as parent
        # set Wizard Properties
        WizardPage3.setGeometry(0,0,320,480)
        WizardPage3.setObjectName(_fromUtf8("WizardPage3"))
        WizardPage3.resize(320, 480)
        WizardPage3.setMinimumSize(QtCore.QSize(320, 480))
        WizardPage3.setMaximumSize(QtCore.QSize(320, 480))
        WizardPage3.setAutoFillBackground(False) # set Background to NULL
        WizardPage3.setStyleSheet(_fromUtf8("QWidget  {background: url(:/bg/images/bg.png);}")) # set custom background
        self.widget3 = QtGui.QWidget(WizardPage3) # initialize Main Widget
        # set Main Widget Occurrence Properties
        self.widget3.setGeometry(QtCore.QRect(0, 0, 321, 481))
        self.widget3.setObjectName(_fromUtf8("widget"))
        
        # generate child widgets, set Properties
        self.label3 = QtGui.QLabel(self.widget3)
        self.label3.setGeometry(QtCore.QRect(0, 20, 321, 111))
        self.label3.setText(_fromUtf8(""))
        self.label3.setPixmap(QtGui.QPixmap(_fromUtf8(":/icon/images/logo1.png")))
        self.label3.setScaledContents(True)
        self.label3.setObjectName(_fromUtf8("label"))
        self.pushButton3 = QtGui.QPushButton(self.widget3)
        self.pushButton3.setGeometry(QtCore.QRect(80, 430, 151, 41))
        self.pushButton3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton3.setStyleSheet(_fromUtf8("QPushButton {background:rgba(11,11,11,142); font: italic 14pt \"Monotype Corsiva\"; border-radius: 50px 0; color: white; }"))
        self.pushButton3.setObjectName(_fromUtf8("pushButton3"))
        self.plainTextEdit3 = QtGui.QPlainTextEdit(self.widget3)
        self.plainTextEdit3.setEnabled(True)
        self.plainTextEdit3.setGeometry(QtCore.QRect(10, 170, 301, 181))
        self.plainTextEdit3.setMaximumSize(QtCore.QSize(500, 1000))
        self.plainTextEdit3.setStyleSheet(_fromUtf8("QPlainTextEdit {background: rgba(87,74,76,150); border-radius: 10px; color: rgb(222,222,222); padding: 10px; font-size:14px} QScrollBar {background: gray}"))
        self.plainTextEdit3.setPlainText(_fromUtf8(""))
        self.plainTextEdit3.setObjectName(_fromUtf8("plainTextEdit3"))
        self.songname = QtGui.QLabel(self.widget3)
        self.songname.setGeometry(QtCore.QRect(20, 120, 281, 41))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Euphemia"))
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.songname.setFont(font)
        self.songname.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.songname.setStyleSheet(_fromUtf8("#songname {color: white; border-radius: 5px; padding: 0 5px; background: transparent;}"))
        self.songname.setObjectName(_fromUtf8("songname"))
        self.remainingSongs = QtGui.QLabel(self.widget3)
        self.remainingSongs.setGeometry(QtCore.QRect(20, 370, 281, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Reference Sans Serif"))
        font.setPointSize(10)
        self.remainingSongs.setFont(font)
        self.remainingSongs.setStyleSheet(_fromUtf8("#remainingSongs {color: white; padding: 0 5px; border-radius: 5px}"))
        self.remainingSongs.setObjectName(_fromUtf8("remainingSongs"))

        self.plainTextEdit3.clear()

        if not self.completedFiles == '':
            self.plainTextEdit3.insertPlainText(self.completedFiles)
        if not self.alreadyCompletedFiles == '':
            self.plainTextEdit3.insertPlainText('\n Already fingerprinted: \n\n')
            self.plainTextEdit3.insertPlainText(self.alreadyCompletedFiles)
        
        # initialize Labels for the widgets
        WizardPage3.setWindowTitle(_translate("WizardPage3", "Lycaon", None))
        self.pushButton3.setText(_translate("WizardPage3", "Done", None))
        self.songname.setText(_translate("WizardPage3", "FingerPrinting Completed", None))
        self.remainingSongs.setText(_translate("WizardPage3", "Took "+str(self.timeTaken)+" seconds", None))
        self.plainTextEdit3.setReadOnly(True)
        QtCore.QMetaObject.connectSlotsByName(WizardPage3)

        self.fp3.addWidget(WizardPage3) # add Wizard Page to Layout

        # initialize Click Events
        self.connect(self.pushButton3, QtCore.SIGNAL("clicked()"), self.fp_close)

    def fp_close(self):
        '''
        close Main Layout
        '''
        sys.exit()

    def remove_fp_one(self):
        '''
        remove nested widgets from Layout one
        '''
        for cnt in reversed(range(self.fp1.count())):
            # takeAt does both the jobs of itemAt and removeWidget
            # namely it removes an item and returns it
            widget = self.fp1.takeAt(cnt).widget()

            if widget is not None: 
                # widget will be None if the item is a layout
                widget.deleteLater()

    def remove_fp_two(self):
        '''
        remove nested widgets from Layout two
        '''
        for cnt in reversed(range(self.fp2.count())):
            # takeAt does both the jobs of itemAt and removeWidget
            # namely it removes an item and returns it
            widget = self.fp2.takeAt(cnt).widget()

            if widget is not None: 
                # widget will be None if the item is a layout
                widget.deleteLater()

def run():
    mp.freeze_support()
    app = QtGui.QApplication(sys.argv) # initialize QApplication
    app.setStyle(QtGui.QStyleFactory.create("Plastique")) # set theme
    app.setStyleSheet(_fromUtf8("QApplication {background:rgba(11,11,11,142)}"))
    ex = WindowLayout() # make object: Main Window

    # set Window Icon
    app_icon = QtGui.QIcon()
    app_icon.addFile('./icons/listen16.png', QtCore.QSize(16,16))
    app_icon.addFile('./icons/listen24.png', QtCore.QSize(24,24))
    app_icon.addFile('./icons/listen32.png', QtCore.QSize(32,32))
    app_icon.addFile('./icons/listen48.png', QtCore.QSize(48,48))
    app_icon.addFile('./icons/listen.png', QtCore.QSize(256,256))
    app_icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icon/images/listen.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    ex.setWindowIcon(app_icon)

    ex.show() # run the application
    sys.exit(app.exec_()) # terminate when all parsed

if __name__ == "__main__":
    '''
    main function
    '''
    run()
