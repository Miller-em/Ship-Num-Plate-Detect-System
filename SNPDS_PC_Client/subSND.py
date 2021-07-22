# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\subSND.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Child(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(506, 402)
        MainWindow.setFixedSize(506, 402)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 0, 481, 81))
        self.widget.setStyleSheet('''
                            QPushButton{
                                border:1px solid gray;
                                width:300px;
                                border-radius:10px;
                                padding:2px 4px;}
                            QPushButton#pushButton_x:hover{
                                border:5px gray;
                                font-weight:700;
                            }
        ''')
        self.widget.setObjectName("widget")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 50, 381, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText("在此处输入合法船牌")
        self.lineEdit.setStyleSheet('''QLineEdit{
                                                border:1px solid gray;
                                                width:300px;
                                                border-radius:10px;
                                                padding:2px 4px;
                                    }''')
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(400, 50, 81, 20))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(10, 10, 131, 31))
        self.label.setObjectName("label")
        self.label.setStyleSheet('''QLabel#label{
                                            border:none;
                                            font-size:25px;
                                            font-weight:700;
                                            font-family: "宋体";
                                        }''')
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(10, 80, 481, 291))
        self.widget_2.setObjectName("widget_2")
        self.widget_2.setStyleSheet('''
                                        QListView{
                                            color:#232C51;
                                            background:white;
                                            border-top:1px solid darkGray;
                                            border-bottom:1px solid darkGray;
                                            border-right:1px solid darkGray;
                                            border-left:1px solid darkGray;
                                            border-top-right-radius:10px;
                                            border-bottom-right-radius:10px; 
                                            border-top-left-radius:10px;
                                            border-bottom-left-radius:10px; 
                                        }
                                        ''')
        self.listView = QtWidgets.QListView(self.widget_2)
        self.listView.setGeometry(QtCore.QRect(10, 0, 471, 281))
        self.listView.setObjectName("listView")
        self.lineEdit.setStyleSheet('''QLineEdit{
                                                border:1px solid gray;
                                                width:300px;
                                                border-radius:10px;
                                                padding:2px 4px;
                                    }''')
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 506, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "合法船牌信息"))
        self.pushButton.setText(_translate("MainWindow", "添加"))
        self.label.setText(_translate("MainWindow", "添加合法船牌："))
