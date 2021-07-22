from PyQt5.QtWidgets import QApplication, QFileDialog, QListWidgetItem, QMainWindow, QMessageBox, QAbstractItemView
from PyQt5.QtCore import QModelIndex, QStringListModel, QThread, pyqtSignal
from SND_UI import Ui_MainWindow
from subSND import Ui_Child
from PyQt5.QtCore import Qt
import requests
import base64
import os
import sys
from PyQt5 import QtGui, QtCore, QtGui, QtWidgets
import numpy as np
import cv2

# 服务器地址
url_pull_db = "http://ip/xxx"
url_pull_img = "http://ip/xxx"
url_pull_legaldb = "http://ip/xxx"
url_push_sn = "http://ip/xxx"

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, '..')))

sql = {}
db = []
legal_db = []


class MyGUIDemo(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyGUIDemo, self).__init__()
        self.my_thread = MyThread()
        self.my_thread.start()  # 开启线程
        self.my_subthread = subMyThread()
        self.my_subthread.start()  # 开启线程
        self.child_win = Child()
        self.setupUi(self)
        self.initlegalDatabase(self)
        self.signal(self)
        self.WidgetsUi(self)
        self.m_drag = False
        self.save_result_path = None
        self.list = []
        self.info_dict = {}

    def WidgetsUi(self, MainWindow):
        imgName = './Ship_White.png'
        icon = QtGui.QPixmap(imgName)
        self.label.setPixmap(icon)

    def signal(self, MainWindow):
        """放置信号函数"""
        # Button
        self.pushButton_2.clicked.connect(self.close)
        self.pushButton_6.clicked.connect(self.slot_max_or_recv)
        self.pushButton.clicked.connect(self.showMinimized)
        self.pushButton_5.clicked.connect(self.save_as)
        self.pushButton_3.clicked.connect(self.child_win.OPEN)
        self.listWidget.itemClicked.connect(self.onClickedListWidget)
        self.my_thread.trigger.connect(self.showDatabase)  # 显示数据库

    def showDatabase(self, list):
        """将数据库添加到ListView里面"""
        # print(list)
        # self.list = []  # 清空显示框
        self.info_dict = {} # 清空信息框
        self.db = []
        self.listWidget.clear()
        for data in list:
            flag = False
            img_id = data[0] #在数据库的id号
            file_name = data[1].split('.')[1]  # 分割提取文件名
            info = data[2] #该帧图像的检测目标
            if info[:-1] in legal_db:
                flag = True
            if not flag:
                self.info_dict[img_id] = info #建表
                time = file_name.split('/')[2].split('S')[0]
                filename = str(img_id) + ':    ' + time + '推理到的目标帧'
                item = QListWidgetItem(filename)
                item.setForeground(Qt.red)
                self.listWidget.addItem(item)
                # self.list.append(filename)
            else:
                self.info_dict[img_id] = info
                time = file_name.split('/')[2].split('S')[0]
                filename = str(img_id) + ':    ' + time + '推理到的目标帧'
                self.listWidget.addItem(filename)

    def initlegalDatabase(self, MainWindow):
        """更新合法数据库"""
        # print(list)
        self.data = {'info': "select * from legal_SN"}
        try:
            self.result = requests.request(
                "POST", url_pull_legaldb, json=self.data)
            result = eval(self.result.content)  # 将内容传回显示框
            # print("刷新一次数据库")
        except:
            # print("无法连接数据库")
            return
        for x in result:
            legal_db.append(x[1])
        

    def onClickedListWidget(self, item):
        """数据库列表点击响应，并且拉取响应的帧图片"""
        filename = item.text()
        img_id = filename.split(':')[0]
        # print(self.info_dict)
        info = self.info_dict[int(img_id)]
        info = info[:-1]
        self.label_6.setText(info)
        sql['img_id'] = img_id
        try:
            result = requests.request("POST", url_pull_img, json=sql)
            print("拉取帧成功")
        except:
            print("无法连接数据库")
            return
        result = result.content
        # 以下将图像信息从 base64->Mat->QImage
        try:
            img = base64.b64decode(result)
            nparr = np.fromstring(img, np.uint8)
            self.image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            self.image = QtGui.QImage(
                self.image.data, self.image.shape[1], self.image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
            self.label_5.setPixmap(QtGui.QPixmap.fromImage(self.image).scaled(self.label_5.width(), self.label_5.height()))
        except :
            return

    def save_as(self):
        reSave_path = QFileDialog.getSaveFileName(self,"另存为","","普通图像(*.jpg *.png *.bmp);图像(*.tif)") 
        try:
            if(reSave_path!=None):
                # 获取图片并且保存
                imgptr = self.label_5.pixmap().toImage()
                ptr = imgptr.constBits()
                ptr.setsize(imgptr.byteCount())
                mat = np.array(ptr).reshape(imgptr.height(), imgptr.width(),4)
                mat_img = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)
                mat_img = cv2.cvtColor(mat_img, cv2.COLOR_BGR2RGB)
                cv2.imwrite(reSave_path[0], mat_img)
                QMessageBox.about(self,"检测结果保存","保存成功！");  
            else:
                QMessageBox.critical(self, "检测结果保存","发生错误，未打开任何文件！",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        except:
            return

    def slot_max_or_recv(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    # 重写三个方法使我们的窗口支持拖动，上面参数 window 就是拖动对象
    def mousePressEvent(self, event):  # 鼠标长按事件
        if event.button() == QtCore.Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):  # 鼠标移动事件
        if QtCore.Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):  # 鼠标释放事件
        self.m_drag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

class Child(QMainWindow,Ui_Child):
    """子窗口类"""
    def __init__(self):
        super(Child, self).__init__()
        self.my_thread = subMyThread()
        self.my_thread.start()  # 开启线程
        self.setupUi(self)
        self.signal(self)
        self.listModel = QStringListModel()
        self.list = []

    def signal(self, MainWindow):
        self.pushButton.clicked.connect(self.add_info)
        self.my_thread.trigger.connect(self.showDatabase)  # 显示数据库

    def showDatabase(self, list):
        """将数据库添加到ListView里面"""
        # print(list)
        self.list = []  # 清空显示框
        legal_db = []
        for data in list:
            img_id = data[0] #在数据库的id号
            legal_SN = data[1]  # 船牌信息
            file_info = str(img_id) + ':  ' + legal_SN
            self.list.append(file_info)
            legal_db.append(data[1])
        self.listModel.setStringList(self.list)
        self.listView.setModel(self.listModel)
        self.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def add_info(self):
        s = self.lineEdit.text()
        if s == "":
            return
        try:
            data = {}
            data['info'] = s
            result = requests.request("POST", url_push_sn, json=data)
            print("添加成功")
        except:
            print("数据库连接失败")
        self.lineEdit.clear()
        legal_db.clear()
        self.data = {'info': "select * from legal_SN"}
        try:
            self.result = requests.request(
                "POST", url_pull_legaldb, json=self.data)
            result = eval(self.result.content)  # 将内容传回显示框
            # print("刷新一次数据库")
        except:
            # print("无法连接数据库")
            return
        for x in result:
            legal_db.append(x[1])


    def OPEN(self):
        self.setWindowIcon(QtGui.QIcon(".\Ship_White.png"))
        self.show()


class MyThread(QThread):
    # 自定义信号对象。参数list就代表这个信号可以传一个列表
    trigger = pyqtSignal(list)

    def __init__(self):
        super(MyThread, self).__init__()
        self.data = {'info': "select * from deted_Ship"}

    def run(self):
        while True:
            # 从数据库获取数据
            try:
                self.result = requests.request(
                    "POST", url_pull_db, json=self.data)
                self.trigger.emit(list(eval(self.result.content)))  # 将内容传回显示框
                # print("刷新一次数据库")
            except:
                print("无法连接数据库")
            self.sleep(5)

class subMyThread(QThread):
    # 自定义信号对象。参数list就代表这个信号可以传一个列表
    trigger = pyqtSignal(list)

    def __init__(self):
        super(subMyThread, self).__init__()
        self.data = {'info': "select * from legal_SN"}

    def run(self):
        while True:
            # 从数据库获取数据
            try:
                self.result = requests.request(
                    "POST", url_pull_legaldb, json=self.data)
                self.trigger.emit(list(eval(self.result.content)))  # 将内容传回显示框
                # print("刷新一次数据库")
            except:
                # print("无法连接数据库")
                continue
            self.sleep(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyGUIDemo()
    child_win = Child()
    window.setWindowTitle("智慧渔政")
    window.setWindowIcon(QtGui.QIcon(".\Ship_White.png"))
    window.show()
    sys.exit(app.exec_())
