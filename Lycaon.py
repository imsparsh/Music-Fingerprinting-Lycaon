__author__ = 'imsparsh'

# initialize Libraries
import sys
import images_rc
from PyQt4 import QtCore, QtGui
import numpy, scipy, librosa, os, sys, time, multiprocessing as mp, record as rc

# pymongo driver for MongoDB
from pymongo import *
from bson.objectid import ObjectId
from scipy import *

# locality sensitive hashing function
def hash_func(vecs, projections):
    # dot vector co-variance of the feature vector with randomly generated vector.
    bools = dot(vecs, projections.T) > 0
    # return a boolean co-variance vector
    return [bool2int(bool_vec) for bool_vec in bools]

#generates the hash for the given boolean co-variance vector
def bool2int(x):
    y = 0
    for i,j in enumerate(x):
        if j: y += 1<<i
    return y

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
    def __init__(self, q):
        '''        initialize Main Window with Widgets        '''
        super(WindowLayout, self).__init__()
        self.queue = q
        
        # connect to dataBase
        cl = MongoClient('localhost',27017)
        self.dB = cl.lycaon_db
        self.result = {}
        
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
        self.setWindowTitle(_translate("Wizard", "Lycaon", None)) # set Window Title
        
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
            self.close()
    

    def fp_one(self):
        '''
        the first Layout
        '''

        WizardPage1 = QtGui.QWizardPage()
        WizardPage1.setGeometry(0,0,320,480)
        WizardPage1.setObjectName(_fromUtf8("WizardPage1"))
        WizardPage1.resize(320, 480)
        WizardPage1.setMinimumSize(QtCore.QSize(320, 480))
        WizardPage1.setMaximumSize(QtCore.QSize(320, 480))
        WizardPage1.setAutoFillBackground(False)
        WizardPage1.setStyleSheet(_fromUtf8("QWidget  {background: url(:/bg/images/bg.png);}"))
        self.widget1 = QtGui.QWidget(WizardPage1)
        self.widget1.setGeometry(QtCore.QRect(0, 0, 321, 481))
        self.widget1.setObjectName(_fromUtf8("widget1"))
        
        # generate child widgets, set Properties
        self.label1 = QtGui.QLabel(self.widget1)
        self.label1.setGeometry(QtCore.QRect(0, 20, 321, 111))
        self.label1.setText(_fromUtf8(""))
        self.label1.setPixmap(QtGui.QPixmap(_fromUtf8(":/icon/images/logo1.png")))
        self.label1.setScaledContents(True)
        self.label1.setObjectName(_fromUtf8("label1"))
        self.pushButton1 = QtGui.QPushButton(self.widget1)
        self.pushButton1.setGeometry(QtCore.QRect(90, 320, 151, 41))
        self.pushButton1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton1.setStyleSheet(_fromUtf8("QPushButton {background:rgba(11,11,11,142); font: italic 14pt \"Monotype Corsiva\"; border-radius: 50px 0; color: white; }"))
        self.pushButton1.setObjectName(_fromUtf8("pushButton1"))
        self.remainingSongs = QtGui.QLabel(self.widget1)
        self.remainingSongs.setGeometry(QtCore.QRect(30, 400, 271, 51))
        font1 = QtGui.QFont()
        font1.setFamily(_fromUtf8("MS Reference Sans Serif"))
        font1.setPointSize(10)
        self.remainingSongs.setFont(font1)
        self.remainingSongs.setStyleSheet(_fromUtf8("#remainingSongs {color: white; padding: 0 auto; border-radius: 5px; background: rgba(55,55,55,100)}"))
        self.remainingSongs.setObjectName(_fromUtf8("remainingSongs"))
        self.listen = QtGui.QToolButton(self.widget1)
        self.listen.setGeometry(QtCore.QRect(80, 130, 161, 161))
        self.listen.setAutoFillBackground(False)
        self.listen.setStyleSheet(_fromUtf8("#listen {background: transparent url(:/icon/images/listen.png) no-repeat center center;}"))
        self.listen.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.listen.setText(_fromUtf8(""))
        self.listen.setObjectName(_fromUtf8("listen"))
        self.remainingSongs.hide()

        # initialize Labels for the widgets
        WizardPage1.setWindowTitle(_translate("WizardPage1", "Lycaon", None))
        self.pushButton1.setDisabled(False)
        self.pushButton1.setText(_translate("WizardPage1", "Browse", None))
        self.remainingSongs.setText(_translate("WizardPage1", "Recognizing . . ", None))
        QtCore.QMetaObject.connectSlotsByName(WizardPage1)

        self.fp1.addWidget(WizardPage1) # add Wizard Page to Layout

        # initialize Click Events
        self.connect(self.pushButton1, QtCore.SIGNAL("clicked()"), self.file_open)
        self.connect(self.listen, QtCore.SIGNAL("clicked()"), self.file_record)

    def file_record(self):
        '''
        record in live environment
        '''
        self.remainingSongs.hide()
        self.remainingSongs.setText("Recording . .")
        self.found = 0
        self.rpath = os.path.join(os.path.abspath('.'),'sample')
        if not os.path.isdir(self.rpath): # check if the directory exists
            os.mkdir(self.rpath)
        self.rfpath = os.path.join(self.rpath,'sample.wav')
        # initialize Queues
        self.rqueue = mp.Queue()
        self.tqueue = mp.Queue()

        '''
        record_to_file(self.rfpath, self.rqueue, self.tqueue)
        multiprocessing module initiated for recording a sample to match with
        '''
        self.rpro = mp.Process(target=rc.record_to_file, args=(self.rfpath, self.rqueue, self.tqueue, ))
        self.rpro.start() # start the process
        #while self.rpro.is_alive():
        while self.tqueue.empty(): # refresh View
            self.remainingSongs.show()
            if not self.rqueue.empty():
                self.rqval = self.rqueue.get()
            else:
                self.rqval = -9999999999
            time.sleep(0.1)
            if not self.rqval == -9999999999:
                # translate icon when chunks received
                self.listen.setGeometry(QtCore.QRect(80, 125, 161, 161))
                #self.listen.hide()
                QtGui.QApplication.processEvents() # refresh View
            time.sleep(0.1)
            self.listen.setGeometry(QtCore.QRect(80, 130, 161, 161))
            self.listen.show()
            QtGui.QApplication.processEvents()
        self.rpro.terminate() # terminate the process
        self.rpro.join() # join to the queue
        # close all queues
        self.tqueue.close()
        self.rqueue.close()
        self.remainingSongs.hide()
        self.listen.show()
        # get full filenames along with path
        self.fullFileName = self.rfpath
        # get individual filename in list
        self.fileName = os.path.join('sample',self.fullFileName.split('\\')[-1])
        #self.remainingSongs.setText(self.fileName)
        
        if not self.fullFileName == '': # check if the file is received
            self.makeFingerprinting() # start fingerPrinting

    def file_open(self):
        '''
        select the file to match
        '''
        self.remainingSongs.hide()
        self.found = 0
        filter_mask = "Music files (*.mp3 *.wav)"
        openPath = 'C:/'
        # get full filenames along with path
        self.fullFileName = QtGui.QFileDialog.getOpenFileName(self, 'Select Files', openPath , filter_mask)
        # get individual filename in list
        self.fileName = self.fullFileName.split('\\')[-1]
        #self.remainingSongs.setText(self.fileName)
        
        if not self.fullFileName == '': # check if the file is received
            self.makeFingerprinting() # start fingerPrinting

    def makeFingerprinting(self):
        '''
        initialize fingerPrinting
        '''
        self.remainingSongs.hide()
        self.remainingSongs.setText("Recognizing . .")
        # check if the files are selected or not
        if '.mp3' in self.fileName or '.wav' in self.fileName:
            self.pushButton1.setDisabled(True)
            self.pushButton1.setStyleSheet(_fromUtf8("QPushButton {background:rgba(111,111,111,142); font: italic 14pt \"Monotype Corsiva\"; border-radius: 50px 0; color: white; }"))
            #print "Recognition started.."

            '''
            initFingerprint(filepath, self.queue)
            multiprocessing module initiated for fingerPrinting
            '''
            self.pro = mp.Process(target=initFingerprint, args=(self.fileName, self.queue, ))
            self.pro.start() # start the process
            while self.pro.is_alive(): # refresh View
                time.sleep(1)
                self.remainingSongs.hide()
                QtGui.QApplication.processEvents()
                time.sleep(0.5)
                self.remainingSongs.show()
                QtGui.QApplication.processEvents()
            self.pro.join() # join the process to queue
            #print "Recognition completed", remove recorded song directory if exists.
            '''if os.path.isdir(self.rpath):
                os.chmod(self.rpath,777)
                os.remove(self.rpath)'''

            # check for result
            if self.queue.get():
                self.found = 1
                self.result = self.queue.get()
                self.dBSong = self.dB.songInfo
                self.matchInfo = 0

                # check for audio correlation
                for r in sorted(self.result, key=self.result.get, reverse=True):
                    if self.result[r] > 5: # THRESHOLD for Accuracy = 5
                        self.matchInfo = self.result[r] # change if Accuracy > THRESHOLD
                        break

                self.similarSongInfo = ''
                # check for the THRESHOLD Breakage
                if not self.matchInfo == 0:
                    self.songMatchInfo = self.dBSong.find({'_id':ObjectId(r)})
                    self.foundSong = dict()
                    # scan metadata for found song
                    for cursor in self.songMatchInfo:
                        self.foundSong['key'] = str(cursor['_id'])
                        self.foundSong['title'] = str(cursor['title'])
                        self.foundSong['album'] = str(cursor['album'])
                        self.foundSong['artist'] = str(cursor['artist'])
                        self.foundSong['dur'] = str(cursor['length'])
                        if 'genre' in cursor:
                            self.foundSong['genre'] = str(cursor['genre'])
                        if 'publisher' in cursor:
                            self.foundSong['publisher'] = str(cursor['publisher'])
                        if 'year' in cursor:
                            self.foundSong['year'] = str(cursor['year'])
                    self.fp_one_two() # change Layout to two
                else:
                    aDigit = 1
                    # scan metadata for all 5 songs
                    for r in sorted(self.result, key=self.result.get, reverse=True):
                        self.partInfo = self.dBSong.find({'_id':ObjectId(r)},{'_id':0})
                        for cursor in self.partInfo:
                            self.similarSongInfo += (str(aDigit)+". "+str(cursor['title']) + " | " + str(round(self.result[r],2)) + "<br />")
                        aDigit += 1
                    #print self.similarSongInfo
                    self.found = 1 # matches found
                    self.fp_one_three() # change Layout
            else:
                self.found = 0 # no match found
                self.fp_one_three() # change Layout
        else:
            self.remainingSongs.show()
            self.remainingSongs.setText("Please try again.. ")
    
    def fp_one_two(self):
        '''
        change Layout one to two
        '''
        self.remove_fp_one()
        self.fp_two()

    def fp_one_three(self):
        '''
        change Layout one to three
        '''
        self.remove_fp_one()
        self.fp_three()

    def fp_two(self):
        '''
        the second Layout
        '''
                
        WizardPage2 = QtGui.QWizardPage()
        WizardPage2.setObjectName(_fromUtf8("WizardPage2"))
        WizardPage2.resize(320, 480)
        WizardPage2.setMinimumSize(QtCore.QSize(320, 480))
        WizardPage2.setMaximumSize(QtCore.QSize(320, 480))
        WizardPage2.setAutoFillBackground(False)
        WizardPage2.setStyleSheet(_fromUtf8("QWidget  {background: url(:/bg/images/bg.png);}"))
        self.widget2 = QtGui.QWidget(WizardPage2)
        self.widget2.setGeometry(QtCore.QRect(0, 0, 321, 481))
        self.widget2.setObjectName(_fromUtf8("widget2"))
        
        # generate child widgets, set Properties
        self.label2 = QtGui.QLabel(self.widget2)
        self.label2.setGeometry(QtCore.QRect(0, 20, 321, 111))
        self.label2.setText(_fromUtf8(""))
        self.label2.setPixmap(QtGui.QPixmap(_fromUtf8(":/icon/images/logo1.png")))
        self.label2.setScaledContents(True)
        self.label2.setObjectName(_fromUtf8("label2"))
        self.songInfo = QtGui.QWidget(self.widget2)
        self.songInfo.setGeometry(QtCore.QRect(0, 100, 320, 320))
        #self.songInfo.setStyleSheet(_fromUtf8("#songInfo {background: url(:/bg/images/songBg.png) center center; }"))
        self.songInfo.setObjectName(_fromUtf8("songInfo"))
        self.songframe = QtGui.QFrame(self.songInfo)
        self.songframe.setGeometry(QtCore.QRect(10, 10, 301, 301))
        self.songframe.setStyleSheet(_fromUtf8("#songframe {background: rgba(222,222,222,70);} #songframe QLabel {border-radius: 5px;padding: 5px 10px ;background: rgba(222,222,222,0); color: white; font: 12pt \"Leelawadee\"; text-align: center}"))
        self.songframe.setFrameShape(QtGui.QFrame.StyledPanel)
        self.songframe.setFrameShadow(QtGui.QFrame.Raised)
        self.songframe.setObjectName(_fromUtf8("songframe"))
        self.infoName = QtGui.QLabel(self.songframe)
        self.infoName.setGeometry(QtCore.QRect(20, 20, 261, 31))
        self.infoName.setObjectName(_fromUtf8("infoName"))
        self.infoArtist = QtGui.QLabel(self.songframe)
        self.infoArtist.setGeometry(QtCore.QRect(20, 60, 261, 31))
        self.infoArtist.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.infoArtist.setObjectName(_fromUtf8("infoArtist"))
        self.infoPub = QtGui.QLabel(self.songframe)
        self.infoPub.setGeometry(QtCore.QRect(20, 260, 121, 31))
        self.infoPub.setObjectName(_fromUtf8("infoPub"))
        self.infoGenre = QtGui.QLabel(self.songframe)
        self.infoGenre.setGeometry(QtCore.QRect(160, 140, 121, 31))
        self.infoGenre.setObjectName(_fromUtf8("infoGenre"))
        self.infoAlbum = QtGui.QLabel(self.songframe)
        self.infoAlbum.setGeometry(QtCore.QRect(20, 190, 261, 51))
        self.infoAlbum.setObjectName(_fromUtf8("infoAlbum"))
        self.infoDate = QtGui.QLabel(self.songframe)
        self.infoDate.setGeometry(QtCore.QRect(160, 260, 121, 31))
        self.infoDate.setObjectName(_fromUtf8("infoDate"))
        self.infoDur = QtGui.QLabel(self.songframe)
        self.infoDur.setGeometry(QtCore.QRect(20, 110, 121, 31))
        self.infoDur.setObjectName(_fromUtf8("infoDur"))
        self.lookAnother = QtGui.QLabel(self.widget2)
        self.lookAnother.setGeometry(QtCore.QRect(20, 440, 141, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Reference Sans Serif"))
        font.setPointSize(10)
        self.lookAnother.setFont(font)
        self.lookAnother.setStyleSheet(_fromUtf8("#lookAnother {color: white; border-radius: 5px;  background: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 189), stop:1 rgba(255, 255, 255, 50)); padding: 0 5px;}"))
        self.lookAnother.setObjectName(_fromUtf8("lookAnother"))
        self.exit = QtGui.QLabel(self.widget2)
        self.exit.setGeometry(QtCore.QRect(170, 440, 141, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Reference Sans Serif"))
        font.setPointSize(10)
        self.exit.setFont(font)
        self.exit.setStyleSheet(_fromUtf8("#exit {color: white; padding: 0 50%; border-radius: 5px; background: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 239), stop:1 rgba(255, 255, 255, 120))}"))
        self.exit.setObjectName(_fromUtf8("exit"))

        # initialize Labels for the widgets
        WizardPage2.setWindowTitle(_translate("WizardPage2", "Lycaon", None))
        self.songInfo.setStyleSheet(_fromUtf8("#songInfo {background: url('./albumart/"+self.foundSong['key']+".jpg') center center; }"))
        self.infoName.setText(_translate("WizardPage", self.foundSong['title'], None))
        self.infoArtist.setText(_translate("WizardPage", self.foundSong['artist'], None))
        self.infoAlbum.setText(_translate("WizardPage", self.foundSong['album'], None))
        self.infoDur.setText(_translate("WizardPage", self.foundSong['dur'], None))
        if 'publisher' in self.foundSong:
            self.infoPub.setText(_translate("WizardPage", self.foundSong['publisher'], None))
        else:
            self.infoPub.hide()
        if 'genre' in self.foundSong:
            self.infoGenre.setText(_translate("WizardPage", self.foundSong['genre'], None))
        else:
            self.infoGenre.hide()
        if 'year' in self.foundSong:
            self.infoDate.setText(_translate("WizardPage", self.foundSong['year'], None))
        else:
            self.infoDate.hide()
        self.lookAnother.setText(_translate("WizardPage2", "Look for another", None))
        self.exit.setText(_translate("WizardPage2", "Exit", None))
        QtCore.QMetaObject.connectSlotsByName(WizardPage2)

        self.fp2.addWidget(WizardPage2) # add Wizard Page to Layout

        # initialize Click Events
        self.lookAnother.mousePressEvent = self.fp_two_one
        self.exit.mousePressEvent = self.fp_close

    def fp_two_one(self, event):
        '''
        change Layout two to one
        '''
        if event.button() == QtCore.Qt.LeftButton:
            self.remove_fp_two()
            self.fp_one()

    def fp_three(self):
        '''
        the third Layout
        '''

        WizardPage3 = QtGui.QWizardPage()
        WizardPage3.setGeometry(0,0,320,480)
        WizardPage3.setObjectName(_fromUtf8("WizardPage3"))
        WizardPage3.resize(320, 480)
        WizardPage3.setMinimumSize(QtCore.QSize(320, 480))
        WizardPage3.setMaximumSize(QtCore.QSize(320, 480))
        WizardPage3.setAutoFillBackground(False)
        WizardPage3.setStyleSheet(_fromUtf8("QWidget  {background: url(:/bg/images/bg.png);}"))
        self.widget3 = QtGui.QWidget(WizardPage3)
        self.widget3.setGeometry(QtCore.QRect(0, 0, 321, 481))
        self.widget3.setObjectName(_fromUtf8("widget3"))
        
        # generate child widgets, set Properties
        self.label3 = QtGui.QLabel(self.widget3)
        self.label3.setGeometry(QtCore.QRect(0, 20, 321, 111))
        self.label3.setText(_fromUtf8(""))
        self.label3.setPixmap(QtGui.QPixmap(_fromUtf8(":/icon/images/logo1.png")))
        self.label3.setScaledContents(True)
        self.label3.setObjectName(_fromUtf8("label3"))
        self.songError = QtGui.QWidget(self.widget3)
        self.songError.setGeometry(QtCore.QRect(0, 100, 320, 320))
        self.songError.setStyleSheet(_fromUtf8("#songError {background: rgba(0,0,0,0); }"))
        self.songError.setObjectName(_fromUtf8("songError"))
        self.notFound = QtGui.QLabel(self.songError)
        self.notFound.setGeometry(QtCore.QRect(110, 20, 91, 71))
        self.notFound.setStyleSheet(_fromUtf8("#notFound {background: transparent;}"))
        self.notFound.setText(_fromUtf8(""))
        self.notFound.setPixmap(QtGui.QPixmap(_fromUtf8(":/icon/images/error.png")))
        self.notFound.setScaledContents(True)
        self.notFound.setObjectName(_fromUtf8("notFound"))
        self.notFoundLabel = QtGui.QLabel(self.songError)
        self.notFoundLabel.setGeometry(QtCore.QRect(30, 110, 271, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Reference Sans Serif"))
        font.setPointSize(10)
        self.notFoundLabel.setFont(font)
        self.notFoundLabel.setStyleSheet(_fromUtf8("#notFoundLabel {color: white; padding: 0 auto; border-radius: 5px; background: rgba(0,0,0,40)}"))
        self.notFoundLabel.setObjectName(_fromUtf8("notFoundLabel"))
        self.similarSongs = QtGui.QTextEdit(self.songError)
        self.similarSongs.setGeometry(QtCore.QRect(30, 160, 261, 151))
        self.similarSongs.setStyleSheet(_fromUtf8("#similarSongs {background: rgba(0,0,0,50); border-radius: 10px; padding: 15px; color: white; } QScrollBar {background: gray}"))
        self.similarSongs.setObjectName(_fromUtf8("similarSongs"))
        self.similarSongs.setReadOnly(True)
        self.lookAnother2 = QtGui.QLabel(self.widget3)
        self.lookAnother2.setGeometry(QtCore.QRect(20, 440, 141, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Reference Sans Serif"))
        font.setPointSize(10)
        self.lookAnother2.setFont(font)
        self.lookAnother2.setStyleSheet(_fromUtf8("#lookAnother {color: white; border-radius: 5px;  background: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 189), stop:1 rgba(255, 255, 255, 50)); padding: 0 5px;}"))
        self.lookAnother2.setObjectName(_fromUtf8("lookAnother"))
        self.exit = QtGui.QLabel(self.widget3)
        self.exit.setGeometry(QtCore.QRect(170, 440, 141, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Reference Sans Serif"))
        font.setPointSize(10)
        self.exit.setFont(font)
        self.exit.setStyleSheet(_fromUtf8("#exit {color: white; padding: 0 50%; border-radius: 5px; background: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 0, 239), stop:1 rgba(255, 255, 255, 120))}"))
        self.exit.setObjectName(_fromUtf8("exit"))

        # initialize Labels for the widgets
        WizardPage3.setWindowTitle(_translate("WizardPage3", "Lycaon", None))
        self.notFoundLabel.setText(_translate("WizardPage3", "Couldn\'t Find . .", None))

        # check if match found
        if self.found:
            #print self.similarSongInfo
            self.similarSongs.setHtml(_translate("WizardPage3", "<!DOCTYPE HTML><html><head><style type=\"text/css\">p, li { white-space: pre-wrap; }</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\"><p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">But some similar ones are:</span></p><br />"+self.similarSongInfo+"</p></body></html>", None))
        else:
            self.similarSongs.setHtml(_translate("WizardPage3", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\"><html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">p, li { white-space: pre-wrap; }</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\"><p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">But Similar Songs are:</span></p>\n\n\n"
            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\">Database empty..</p></body></html>", None))
        self.lookAnother2.setText(_translate("WizardPage3", "Look for another", None))
        self.exit.setText(_translate("WizardPage3", "Exit", None))
        QtCore.QMetaObject.connectSlotsByName(WizardPage3)

        self.fp3.addWidget(WizardPage3) # add Wizard Page to Layout

        # initialize Click Events
        self.lookAnother2.mousePressEvent = self.fp_three_one
        self.exit.mousePressEvent = self.fp_close

    def fp_three_one(self, event):
        '''
        change Layout three to one
        '''
        if event.button() == QtCore.Qt.LeftButton:
            self.remove_fp_three()
            self.fp_one()

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

    def remove_fp_three(self):
        '''
        remove nested widgets from Layout three
        '''
        for cnt in reversed(range(self.fp3.count())):
            # takeAt does both the jobs of itemAt and removeWidget
            # namely it removes an item and returns it
            widget = self.fp3.takeAt(cnt).widget()

            if widget is not None: 
                # widget will be None if the item is a layout
                widget.deleteLater()

    def fp_close(self, event):
        '''
        close Main Layout
        '''
        if event.button() == QtCore.Qt.LeftButton:
            sys.exit()

def initFingerprint(filepath, queue):
    #initializing environment variables
    framesize = 4096
    hopsize = 4000

    # connecting to dataBase
    cl = MongoClient('localhost',27017)
    dB = cl.lycaon_db
    
    # extract randomly generated projections
    dBproject = dB.projections
    projections = dBproject.find()
    for cursor in projections:
        getItem = cursor[unicode('projections')]
    projections = array(eval(str(getItem.decode())))

    # scanning downsampled data in mono (data, sampling rate = 22050)
    x, fs = librosa.load(filepath)
    # retrieving chroma features from audio
    features = librosa.feature.chromagram(x, fs, n_fft=framesize, hop_length=hopsize).T
    # converting the feature vector to normalized hash vector
    features = hash_func(features, projections)

    uniq_features = set(features) # get distinct features

    dBhash = dB.hashes
    initDict = dict()
    results = dict()
    # for each key in distinct hashes
    for key in uniq_features:
        occurence = features.count(key)
        # check for existence of the hash key in hash collection
        diction = dBhash.find({str(key):{'$exists':1}},{'_id':0})
        for cursor in diction:
            for ind in cursor.keys():
                for indHash in cursor[ind].keys():
                    if indHash in initDict.keys():
                        initDict[indHash] += cursor[ind][indHash]*occurence
                    else:
                        initDict[indHash] = cursor[ind][indHash]*occurence

    # if any of the feature exist, we perform the match
    if not initDict == {}:
        k = 0
        for ind in sorted(initDict, key=initDict.get, reverse=True):
            k += 1
            results[ind] = initDict[ind]
            if k >= 5:
                break

        # extract all feature count for selected songs
        features_all = dict()
        dBfeat = dB.features
        for ind in results.keys():
            features = dBfeat.find({str(ind):{'$exists':1}},{'_id' : 0})
            for cursor in features:
                features_all[str(cursor.keys()[0])] = cursor.values()[0]
    
        # manipulate results for relation
        for k in results:
            results[k] = float(results[k]*4)/features_all[k]
    if not results == {}:
        queue.put(True)
        queue.put(results) # send found results
    else:
        queue.put(False)
        queue.put({}) # send NULL
    return
    
def run():
    queue = mp.Queue() # initialize a Queue
    app = QtGui.QApplication(sys.argv) # initialize QApplication
    app.setStyle(QtGui.QStyleFactory.create("Plastique")) # set theme
    ex = WindowLayout(queue) # make object: Main Window

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
