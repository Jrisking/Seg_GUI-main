import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import DeepLearn
import os


# 语义分割类功能函数
class FileFunction(object):
    def openfile(self):
        # dialog = QFileDialog()
        # # dialog.setFileMode(QFileDialog.AnyFile)
        # # dialog.setFilter(QDir.Files)
        #
        # directory1 = dialog.getExistingDirectory()
        # self.lineEd
        pass

class AspectRatioGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setSceneRect(0, 0, 0, 0)
    def resizeEvent(self, event):
        if self.scene() is None:
            return
        # get the current viewport size
        size = event.size()
        if size.width() <= 0 or size.height() <= 0:
            return
        # get the current scene size
        sceneSize = self.sceneRect().size()
        # calculate the scaling factor
        scaleX = size.width() / sceneSize.width()
        scaleY = size.height() / sceneSize.height()
        scale = min(scaleX, scaleY)
        # set the new scale
        self.setTransform(QTransform().scale(scale, scale))


class CustomGraphicsView(QGraphicsView):
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.scene():
            rect = QRectF(self.sceneRect().x(), self.sceneRect().y(), self.viewport().width(), self.viewport().height())
            self.fitInView(rect, Qt.KeepAspectRatio)
            self.setSceneRect(0, 0, rect.width(), rect.height())


class MyMainForm(QMainWindow, DeepLearn.Ui_MainWindow):#因为界面py文件和逻辑控制py文件分开的，所以在引用的时候要加上文件名再点出对象
    def __init__(self):
        super(MyMainForm, self).__init__()
        self.setupUi(self)   #setupUi是Ui_FilterDesigner类里面的一个方法，这里的self是两个父类的子类的一个实例
        self.fileprocess = FileFunction()

        # 把lineEdit设置成不可编辑状态
        self.lineEdit_5.setEnabled(False)
        self.lineEdit_2.setEnabled(False)
        self.lineEdit_3.setEnabled(False)
        self.lineEdit_4.setEnabled(False)

        # 打开文件
        self.pushButton_2.clicked.connect(lambda: self.openfile(self.pushButton_2.objectName()))
        self.pushButton.clicked.connect(lambda: self.openfile(self.pushButton.objectName()))
        self.pushButton_3.clicked.connect(lambda: self.openfile(self.pushButton_3.objectName()))
        self.pushButton_4.clicked.connect(lambda: self.openfile(self.pushButton_4.objectName()))
        self.comboBox.addItems(['Fig1', 'Fig2', 'Fig3', 'Fig4'])
        self.comboBox.setCurrentIndex(0)
        self.pushButton_5.clicked.connect(lambda: self.select2Show(self.comboBox.currentIndex()))
        self.listWidget.itemClicked.connect(self.show_figure)

        # 筛选条件
        # self.lineEdit.se
        self.lineEdit.setPlaceholderText(".tif/.jpeg/.jpg")
        # self.lineEdit.setChanged.connect(self.update_filelist)


        # 展示图片
        # self.pixmapItem = QGraphicsPixmapItem()



    def openfile(self, push):
        dialog = QFileDialog()
        self.directory1 = dialog.getExistingDirectory()
        if push == 'pushButton_2':
            self.lineEdit_5.setText(self.directory1)

        elif push == 'pushButton_3':
            self.lineEdit_2.setText(self.directory1)

        elif push == 'pushButton':
            self.lineEdit_4.setText(self.directory1)

        elif push == 'pushButton_4':
            self.lineEdit_3.setText(self.directory1)


    def select2Show(self, index):
        # 判断是哪个框输入的
        if index == 0:
            path = str(self.lineEdit_5.text())
        elif index == 1:
            path = str(self.lineEdit_2.text())
        elif index == 2:
            path = str(self.lineEdit_4.text())
        elif index == 3:
            path = str(self.lineEdit_3.text())

        # 设置根路径为文件夹路径
        self.path = path + '/'
        print(self.path)
        self.listWidget.clear()
        all_files = os.listdir(path)

        # 筛选指定文件
        search_text = self.lineEdit.text().strip()

        if search_text:
            # 按文件格式过滤
            filtered_files = [f for f in all_files if os.path.splitext(f.lower())[1] == '.' + search_text.lower()]
        else:
            # 不过滤
            filtered_files = all_files

        # 添加文件名列在QListWidget中
        # for file in filtered_files:
        #     self.listWidget.addItem(file)

        self.rows = 25
        self.total_pages = -(-len(filtered_files) // self.rows)  # 向上取整计算总页数
        self.current_page = 1    # 每次点击下一页，该值将会变化

        # 创建QListWidget并设置最大高度
        # self.list_widget = QListWidget()
        self.listWidget.setMaximumHeight(self.rows * 25)
        # 添加items
        for file in filtered_files:
            self.listWidget.addItem(file)

        # # 创建分页栏
        # self.prev_button = QPushButton("Prev")
        # self.page_label = QLabel(f"Page {self.current_page}/{self.total_pages}")
        # self.next_button = QPushButton("Next")
        # self.prev_button.clicked.connect(self.previous_page)
        # self.next_button.clicked.connect(self.next_page)




    def show_figure(self):
        # 获取选中的文件名
        filename = self.listWidget.currentItem().text()
        self.click_picture = self.path + filename
        print(self.click_picture)

        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.graphicsView.setFixedSize(515, 365)
        self.graphicsView.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap(self.click_picture)
        item = self.scene.addPixmap(pixmap)
        self.graphicsView.setSceneRect(QRectF())
        self.graphicsView.fitInView(item, Qt.KeepAspectRatio)



    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            start_index = (self.current_page - 1) * self.rows
            end_index = self.current_page * self.rows
            self.list_widget.clear()
            for item in self.items[start_index:end_index]:
                self.list_widget.addItem(item)
            self.page_label.setText(f"Page {self.current_page}/{self.total_pages}")

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            start_index = (self.current_page - 1) * self.rows
            end_index = self.current_page * self.rows
            self.list_widget.clear()
            for item in self.items[start_index:end_index]:
                self.list_widget.addItem(item)
            self.page_label.setText(f"Page {self.current_page}/{self.total_pages}")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())