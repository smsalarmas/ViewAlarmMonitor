# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainAlertGenerator.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setMaximumSize(QtCore.QSize(16777215, 52))
        self.frame.setStyleSheet(_fromUtf8("background-color: #38648B;\n"
"font: BOLD 10pt \"Calibri\";\n"
"color: rgb(255, 255, 255);"))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_5 = QtGui.QGridLayout(self.frame)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setStyleSheet(_fromUtf8("font: bold 10pt \"Calibri\";"))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_5.addWidget(self.label, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 3)
        self.tableWidget_Log = QtGui.QTableWidget(self.centralwidget)
        self.tableWidget_Log.setObjectName(_fromUtf8("tableWidget_Log"))
        self.tableWidget_Log.setColumnCount(6)
        self.tableWidget_Log.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tableWidget_Log.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tableWidget_Log.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tableWidget_Log.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tableWidget_Log.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tableWidget_Log.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tableWidget_Log.setHorizontalHeaderItem(5, item)
        self.gridLayout.addWidget(self.tableWidget_Log, 1, 0, 1, 3)
        self.frame_2 = QtGui.QFrame(self.centralwidget)
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 52))
        self.frame_2.setStyleSheet(_fromUtf8("background-color: #38648B;\n"
"font: BOLD 10pt \"Calibri\";\n"
"color: rgb(255, 255, 255);"))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout_6 = QtGui.QGridLayout(self.frame_2)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.label_ColaMensajes = QtGui.QLabel(self.frame_2)
        self.label_ColaMensajes.setStyleSheet(_fromUtf8("font: bold 10pt \"Calibri\";"))
        self.label_ColaMensajes.setObjectName(_fromUtf8("label_ColaMensajes"))
        self.gridLayout_6.addWidget(self.label_ColaMensajes, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.frame_2)
        self.label_3.setStyleSheet(_fromUtf8("font: bold 10pt \"Calibri\";"))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_6.addWidget(self.label_3, 0, 2, 1, 1)
        self.label_MensajesRecibidos = QtGui.QLabel(self.frame_2)
        self.label_MensajesRecibidos.setStyleSheet(_fromUtf8("font: bold 10pt \"Calibri\";"))
        self.label_MensajesRecibidos.setObjectName(_fromUtf8("label_MensajesRecibidos"))
        self.gridLayout_6.addWidget(self.label_MensajesRecibidos, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.frame_2, 2, 0, 1, 3)
        self.tableWidget_Cola = QtGui.QTableWidget(self.centralwidget)
        self.tableWidget_Cola.setObjectName(_fromUtf8("tableWidget_Cola"))
        self.tableWidget_Cola.setColumnCount(4)
        self.tableWidget_Cola.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tableWidget_Cola.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tableWidget_Cola.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tableWidget_Cola.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tableWidget_Cola.setHorizontalHeaderItem(3, item)
        self.gridLayout.addWidget(self.tableWidget_Cola, 3, 0, 1, 1)
        self.tableWidget_Enviados = QtGui.QTableWidget(self.centralwidget)
        self.tableWidget_Enviados.setObjectName(_fromUtf8("tableWidget_Enviados"))
        self.tableWidget_Enviados.setColumnCount(4)
        self.tableWidget_Enviados.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tableWidget_Enviados.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tableWidget_Enviados.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tableWidget_Enviados.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tableWidget_Enviados.setHorizontalHeaderItem(3, item)
        self.gridLayout.addWidget(self.tableWidget_Enviados, 3, 1, 1, 1)
        self.tableWidget_Recibidos = QtGui.QTableWidget(self.centralwidget)
        self.tableWidget_Recibidos.setObjectName(_fromUtf8("tableWidget_Recibidos"))
        self.tableWidget_Recibidos.setColumnCount(3)
        self.tableWidget_Recibidos.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tableWidget_Recibidos.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tableWidget_Recibidos.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tableWidget_Recibidos.setHorizontalHeaderItem(2, item)
        self.gridLayout.addWidget(self.tableWidget_Recibidos, 3, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "AlertGenerator", None))
        self.label.setText(_translate("MainWindow", "Log de Señales Recibidas (Ultimas 100)", None))
        item = self.tableWidget_Log.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Protocolo", None))
        item = self.tableWidget_Log.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Cliente", None))
        item = self.tableWidget_Log.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Evento", None))
        item = self.tableWidget_Log.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Zona/Usuario", None))
        item = self.tableWidget_Log.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Linea", None))
        item = self.tableWidget_Log.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Hora", None))
        self.label_ColaMensajes.setText(_translate("MainWindow", "Cola de Mensajes", None))
        self.label_3.setText(_translate("MainWindow", "Mensajes Enviados (Ultimos 100)", None))
        self.label_MensajesRecibidos.setText(_translate("MainWindow", "Mensajes Recibidos", None))
        item = self.tableWidget_Cola.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Cliente", None))
        item = self.tableWidget_Cola.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Destino", None))
        item = self.tableWidget_Cola.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Mensaje", None))
        item = self.tableWidget_Cola.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Fecha", None))
        item = self.tableWidget_Enviados.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Cliente", None))
        item = self.tableWidget_Enviados.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Destino", None))
        item = self.tableWidget_Enviados.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Mensaje", None))
        item = self.tableWidget_Enviados.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Fecha", None))
        item = self.tableWidget_Recibidos.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Desde", None))
        item = self.tableWidget_Recibidos.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Mensaje", None))
        item = self.tableWidget_Recibidos.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Fecha", None))

