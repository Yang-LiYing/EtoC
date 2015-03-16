from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QDialog,QApplication,QComboBox,QSystemTrayIcon,QAction,QMenu,QWidget)
import re
import systray_rc
from get_translate_text import get_translate_text


class EtoC(QDialog):
    def __init__(self):
        super(EtoC,self).__init__()
        
        self.createIcon()
        self.createMessage()
        
        self.createActions() #create the selection of the toolbar
        self.createTrayIcon()#build the selection of the toolbar
        self.createClipboard()

        self.iconComboBox.currentIndexChanged.connect(self.setIcon)
        #self.trayIcon.messageClicked.connect(self.messageClicked)
        self.trayIcon.activated.connect(self.iconActivated)
        self.sysClipboard.dataChanged.connect(self.dataChanged)

        self.iconComboBox.setCurrentIndex(1)
        self.switch = str(self.iconComboBox.currentText())
        self.trayIcon.show()

        self.createMessage(str(self.sysClipboard.ownsFindBuffer()))
        #self.showMessage()

        #self.hide()
    def setIcon(self,index):
        icon = self.iconComboBox.itemIcon(index)
        self.trayIcon.setIcon(icon)
        self.setWindowIcon(icon)

        self.trayIcon.setToolTip(self.iconComboBox.itemText(index))#look

    def iconActivated(self,reason):
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self.iconComboBox.setCurrentIndex((self.iconComboBox.currentIndex()+1)%self.iconComboBox.count())
            #here must be change the translate state(on or off)
            self.switch = str(self.iconComboBox.currentText())
        elif reason == QSystemTrayIcon.MiddleClick:
            self.showMessage()
        
    def showMessage(self):
        icon = QSystemTrayIcon.MessageIcon(QSystemTrayIcon.NoIcon)
        self.trayIcon.showMessage(self.messageTitle,self.messageBody,icon,15000)
                                  #title            message               second

    #def messageClicked(self):
        #none

    def dataChanged(self): 
        if self.switch == "on":
            text = str(self.sysClipboard.text())
            print("Text is:"+text+":")
            print("Text size:"+str(len(text)))
            if len(text) != 0:
                if text[len(text)-1] == " ":# "words " => "words"
                    text = text[:len(text)-1]
                text = text.lower()
                matchoneword = re.match('[a-z]+',text)
                print("Type:"+str(type(matchoneword)))
                if type(matchoneword) != type(None):
                    print("Search:"+matchoneword.group())
                    self.searchengine = get_translate_text(matchoneword.group())
                    self.formatData(self.searchengine.get_translate())
        else:
            print("Switch is off")

    def formatData(self,data):
        title = data[:data.index(" ")]
        body = data[data.index(" ")+1:]
        self.createMessage(title,body)
        self.showMessage()
    
    def createIcon(self):
        self.iconComboBox = QComboBox()
        self.iconComboBox.addItem(QIcon('./images/translate_off.png'),"off")
        self.iconComboBox.addItem(QIcon('./images/translate_on.png'),"on")

    def createMessage(self,title="Hello",body="I am EtoC!"):
        self.messageTitle = title
        self.messageBody = body
    
    def createActions(self):
        self.quitAction = QAction("&Quit",self,triggered=QApplication.instance().quit)

    def createTrayIcon(self):
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
    
    def createClipboard(self):
        self.sysClipboard = QApplication.clipboard()
        
    
if __name__ == "__main__":

    import sys
    
    #QApplication.addLibraryPath("./")
    app = QApplication(sys.argv)
    app.addLibraryPath("./")
    
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None,"Translate","I couldn't detect any system tray on this system.")
        sys.exit(1)

    QApplication.setQuitOnLastWindowClosed(False)
    
    translate = EtoC()
    #translate.show()
    sys.exit(app.exec_())
