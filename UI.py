from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap
from bibleRead import bibleRead
import textwrap

# https://stackoverflow.com/questions/47345776/pyqt5-how-to-add-a-scrollbar-to-a-qmessagebox
class ScrollMessageBox(QMessageBox):
    def __init__(self, l, whichTranslation, whichBook, whichChapter, *args, **kwargs):
        QMessageBox.__init__(self, *args, **kwargs)
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        self.content = QWidget()
        scroll.setWidget(self.content)
        lay = QVBoxLayout(self.content)
        for item in l:
            lay.addWidget(QLabel(textwrap.fill(item, 65), self))
        self.layout().addWidget(scroll, 0, 0, 1, self.layout().columnCount())
        self.setStyleSheet("QScrollArea{min-width:500 px; min-height: 400px}")
        self.setWindowTitle(f'{whichTranslation} {whichBook} Chapter {whichChapter}')

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # form
        self.setWindowTitle('Bible Read')
        self.center() # self.move(500,200)    # 창 위치
        self.resize(700, 600)   # 창 크기

        # creating label
        self.imgLabel = QLabel(self)

        # loading image
        self.pixmap = QPixmap('Bible.jpg')

        # adding image to label
        self.imgLabel.setPixmap(self.pixmap)

        # move
        self.imgLabel.move(0, 0)

        # Optional, resize label to image size
        self.imgLabel.resize(self.pixmap.width(),
                          self.pixmap.height())

        # creative commons label
        self.ccLabel = QLabel(self)
        self.ccLabel.setText('"Bible" by lokarta is licensed with CC BY-NC-ND 2.0.\n'
                             'To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-nd/2.0/')
        self.ccLabel.setFont(QFont("Arial", 10))
        self.ccLabel.move(20, 550)

        # translation label
        self.translationLabel = QLabel(self)
        self.translationLabel.setText('1. translation')
        self.translationLabel.setFont(QFont("Arial", 12))
        self.translationLabel.setStyleSheet("color: white;")
        self.translationLabel.move(20, 20)

        # translation line
        self.translationLine = QLineEdit(self)
        self.translationLine.move(20, 50)
        self.translationLine.resize(120, 30)

        # book label
        self.bookLabel = QLabel(self)
        self.bookLabel.setText('2. book')
        self.bookLabel.setFont(QFont("Arial", 12))
        self.bookLabel.setStyleSheet("color: white;")
        self.bookLabel.move(200, 20)

        # book line
        self.bookLine = QLineEdit(self)
        self.bookLine.move(200, 50)
        self.bookLine.resize(120, 30)

        # chapter label
        self.chapterLabel = QLabel(self)
        self.chapterLabel.setText('3. chapter')
        self.chapterLabel.setFont(QFont("Arial", 12))
        self.chapterLabel.setStyleSheet("color: white;")
        self.chapterLabel.move(380, 20)

        # chapter line
        self.chapterLine = QLineEdit(self)
        self.chapterLine.move(380, 50)
        self.chapterLine.resize(120, 30)

        # btnEnter label
        self.btnEnterLabel = QLabel(self)
        self.btnEnterLabel.setText('4. click enter')
        self.btnEnterLabel.setFont(QFont("Arial", 12))
        self.btnEnterLabel.setStyleSheet("color: white;")
        self.btnEnterLabel.move(560, 20)

        # btnEnter
        self.btnEnter = QPushButton('Enter', self)
        self.btnEnter.clicked.connect(self.bibleReadInit)
        self.btnEnter.resize(100, 30)
        self.btnEnter.move(560, 50)

        # starting phrase label
        self.startPhraseLabel = QLabel(self)
        self.startPhraseLabel.setText('5. from')
        self.startPhraseLabel.setFont(QFont("Arial", 12))
        self.startPhraseLabel.setStyleSheet("color: white;")
        self.startPhraseLabel.move(20, 120)

        # starting phrase line
        self.startPhraseLine = QLineEdit(self)
        self.startPhraseLine.move(20, 150)
        self.startPhraseLine.resize(120, 30)

        # ending phrase label
        self.endPhraseLabel = QLabel(self)
        self.endPhraseLabel.setText('6. to')
        self.endPhraseLabel.setFont(QFont("Arial", 12))
        self.endPhraseLabel.setStyleSheet("color: white;")
        self.endPhraseLabel.move(200, 120)

        # ending phrase line
        self.endPhraseLine = QLineEdit(self)
        self.endPhraseLine.move(200, 150)
        self.endPhraseLine.resize(120, 30)

        # btnRead label
        self.btnReadLabel = QLabel(self)
        self.btnReadLabel.setText('7. click read')
        self.btnReadLabel.setFont(QFont("Arial", 12))
        self.btnReadLabel.setStyleSheet("color: white;")
        self.btnReadLabel.move(380, 120)

        # btnRead
        self.btnRead = QPushButton('Read', self)
        self.btnRead.clicked.connect(self.readPhrases)
        self.btnRead.resize(100, 30)
        self.btnRead.move(380, 150)

    # initialize bibleRead object
    def bibleReadInit(self):
        self.br = bibleRead(self.translationLine.text(), self.bookLine.text(), self.chapterLine.text())
        self.translationBookEntered()

    # enter translation
    def translationBookEntered(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Translation, book, and chapter entered!")
        msg.setWindowTitle("Information")
        msg.exec_()

    def readPhrases(self):
        if self.endPhraseLine.text() == "":
            endPhrase = -1
        else:
            endPhrase = int(self.endPhraseLine.text())
        self.br.whichPhrases(int(self.startPhraseLine.text()), endPhrase)
        result = ScrollMessageBox(self.br.displayPhrases(),
                                  self.translationLine.text(),
                                  self.bookLine.text(), self.chapterLine.text())
        result.exec_()

    # window at the center of my monitor
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
