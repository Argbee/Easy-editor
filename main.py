from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import os
from PyQt5.QtGui import QPixmap

from PIL import *
from PIL import Image, ImageFilter

#приложение и виджеты
app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Easy Editor')
main_win.resize(700, 400)

donknowwhy_btn = QPushButton("Папка")
list_o_photo = QListWidget()

left_btn = QPushButton('Лево')
right_btn = QPushButton('Право')
mirrow_btn = QPushButton('Зеркало')
sharpness_btn = QPushButton('Резкость')
wb_btn = QPushButton('Ч/Б')

Pictuuure = QLabel('Картинка')


#Лэйауты
main_line = QHBoxLayout()

sec_main_line1 = QVBoxLayout()
sec_main_line2 = QVBoxLayout()

not_main_line = QHBoxLayout()

sec_main_line1.addWidget(donknowwhy_btn)
sec_main_line1.addWidget(list_o_photo)

sec_main_line2.addWidget(Pictuuure)

not_main_line.addWidget(left_btn)
not_main_line.addWidget(right_btn)
not_main_line.addWidget(mirrow_btn)
not_main_line.addWidget(sharpness_btn)
not_main_line.addWidget(wb_btn)


sec_main_line2.addLayout(not_main_line)

main_line.addLayout(sec_main_line1)
main_line.addLayout(sec_main_line2)

main_win.setLayout(main_line)
workdir = ''
def ChooseWorkdir():
 global workdir
 workdir = QFileDialog.getExistingDirectory()

result = ''

def filterr(files, extensions):
 global result
 result = list()
 for filename in files:
  if filename.endswith(str(extensions[0])) or filename.endswith(extensions[1]) or filename.endswith(extensions[2]) or filename.endswith(extensions[3]) or filename.endswith(str(extensions[4])):
   result.append(filename)
 return result

def showFilenamesList():
 global result
 ChooseWorkdir()
 files = os.listdir(workdir)
 extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
 filterr(files, extensions)
 list_o_photo.clear()
 for something in result:
  list_o_photo.addItem(something)


class ImageProcessor():
  def __init__(self):
    self.filename = None
    self.imagee = None
    self.dir = None
    self.savedir = "Modified/"

  def LoadImage(self, filename):
    self.filename = filename
    imagePath = os.path.join(workdir, filename)
    self.imagee = Image.open(imagePath)

  def ShowImagee(self, path):
    Pictuuure.hide()
    pixmapimage = QPixmap(path)
    w, h = Pictuuure.width(), Pictuuure.height() 
    pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
    Pictuuure.setPixmap(pixmapimage)
    Pictuuure.show()
  
  def saveImage(self):
    path = os.path.join(workdir, self.savedir)
    if not(os.path.exists(path) or os.path.isdir(path)):
      os.mkdir(path)
    imagePath = os.path.join(path, self.filename)
    self.imagee.save(imagePath)

  def Black_White(self):
    self.imagee = self.imagee.convert('L')
    self.saveImage()
    imagePath = os.path.join(workdir, self.savedir, self.filename)
    self.ShowImagee(imagePath)

  def left_90(self):
    self.imagee = self.imagee.transpose(Image.ROTATE_90)
    self.saveImage()
    imagePath = os.path.join(workdir, self.savedir, self.filename)
    self.ShowImagee(imagePath)

  def right_90(self):
    self.imagee = self.imagee.transpose(Image.ROTATE_270)
    self.saveImage()
    imagePath = os.path.join(workdir, self.savedir, self.filename)
    self.ShowImagee(imagePath)  

  def flip_img(self):
    self.imagee = self.imagee.transpose(Image.FLIP_LEFT_RIGHT)
    self.saveImage()
    imagePath = os.path.join(workdir, self.savedir, self.filename)
    self.ShowImagee(imagePath)   

  def sharpness(self):
    self.imagee = self.imagee.filter(ImageFilter.SHARPEN)
    self.saveImage()
    imagePath = os.path.join(workdir, self.savedir, self.filename)
    self.ShowImagee(imagePath)        
    
workimage = ImageProcessor()

def showChosenImage():
  if list_o_photo.currentRow() >= 0:
    filename = list_o_photo.currentItem().text()
    workimage.LoadImage(filename)
    image_Path = os.path.join(workdir, workimage.filename)
    workimage.ShowImagee(image_Path)

list_o_photo.currentRowChanged.connect(showChosenImage)
donknowwhy_btn.clicked.connect(showFilenamesList)
left_btn.clicked.connect(workimage.left_90)
right_btn.clicked.connect(workimage.right_90)
mirrow_btn.clicked.connect(workimage.flip_img)
sharpness_btn.clicked.connect(workimage.sharpness)
wb_btn.clicked.connect(workimage.Black_White)


main_win.show()
app.exec_()