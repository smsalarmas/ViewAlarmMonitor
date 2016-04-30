# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
from MainAlertGenerator import Ui_MainWindow
import globalvars
import time
globalvars.initvars()

class VentanaMain(QtGui.QMainWindow):
	def __init__(self):
		super(VentanaMain, self).__init__()
		self.SubVentanaMonitorAlertas = Ui_MainWindow()
		self.SubVentanaMonitorAlertas.setupUi(self)

		self.SubVentanaMonitorAlertas.tableWidget_Log.verticalHeader().setVisible(False)
		self.SubVentanaMonitorAlertas.tableWidget_Log.setShowGrid(False)
		self.SubVentanaMonitorAlertas.tableWidget_Log.setAlternatingRowColors(True)
		self.SubVentanaMonitorAlertas.tableWidget_Log.verticalHeader().setDefaultSectionSize(20)
		self.SubVentanaMonitorAlertas.tableWidget_Log.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
		self.SubVentanaMonitorAlertas.tableWidget_Log.setSortingEnabled(False)
		self.SubVentanaMonitorAlertas.tableWidget_Log.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

		self.SubVentanaMonitorAlertas.tableWidget_Cola.verticalHeader().setVisible(False)
		self.SubVentanaMonitorAlertas.tableWidget_Cola.setShowGrid(False)
		self.SubVentanaMonitorAlertas.tableWidget_Cola.setAlternatingRowColors(True)
		self.SubVentanaMonitorAlertas.tableWidget_Cola.verticalHeader().setDefaultSectionSize(20)
		self.SubVentanaMonitorAlertas.tableWidget_Cola.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
		self.SubVentanaMonitorAlertas.tableWidget_Cola.setSortingEnabled(False)
		self.SubVentanaMonitorAlertas.tableWidget_Cola.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

		self.SubVentanaMonitorAlertas.tableWidget_Enviados.verticalHeader().setVisible(False)
		self.SubVentanaMonitorAlertas.tableWidget_Enviados.setShowGrid(False)
		self.SubVentanaMonitorAlertas.tableWidget_Enviados.setAlternatingRowColors(True)
		self.SubVentanaMonitorAlertas.tableWidget_Enviados.verticalHeader().setDefaultSectionSize(20)
		self.SubVentanaMonitorAlertas.tableWidget_Enviados.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
		self.SubVentanaMonitorAlertas.tableWidget_Enviados.setSortingEnabled(False)
		self.SubVentanaMonitorAlertas.tableWidget_Enviados.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

		self.SubVentanaMonitorAlertas.tableWidget_Recibidos.verticalHeader().setVisible(False)
		self.SubVentanaMonitorAlertas.tableWidget_Recibidos.setShowGrid(False)
		self.SubVentanaMonitorAlertas.tableWidget_Recibidos.setAlternatingRowColors(True)
		self.SubVentanaMonitorAlertas.tableWidget_Recibidos.verticalHeader().setDefaultSectionSize(20)
		self.SubVentanaMonitorAlertas.tableWidget_Recibidos.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
		self.SubVentanaMonitorAlertas.tableWidget_Recibidos.setSortingEnabled(False)
		self.SubVentanaMonitorAlertas.tableWidget_Recibidos.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

		#Invento mio para solucionar el Bug con que si esta activado el rezize de las tablas\
		#Con el resize de la ventana no se le puede colocar un tamano por defec
		self.Resize1 =  False
		self.Resize = False
		self.installEventFilter(self)
		self.Inicio()

	def eventFilter(self, source, event):
		if event.type() == QtCore.QEvent.WindowStateChange:
			self.ArreglarTamanoTablas()
		return QtGui.QWidget.eventFilter(self, source, event)

	def resizeEvent(self,resizeEvent):
		if self.Resize1 == True:
			self.ArreglarTamanoTablas()
		self.Resize1 = True
		pass

	def ArreglarTamanoTablas(self):

		if self.Resize == True:
			print 'Aqui Adentro'
			self.SubVentanaMonitorAlertas.tableWidget_Log.setColumnWidth(0,self.SubVentanaMonitorAlertas.tableWidget_Log.width()/10)
			self.SubVentanaMonitorAlertas.tableWidget_Log.setColumnWidth(1,self.SubVentanaMonitorAlertas.tableWidget_Log.width()/3.3)
			self.SubVentanaMonitorAlertas.tableWidget_Log.setColumnWidth(2,self.SubVentanaMonitorAlertas.tableWidget_Log.width()/3.3)
			self.SubVentanaMonitorAlertas.tableWidget_Log.setColumnWidth(3,self.SubVentanaMonitorAlertas.tableWidget_Log.width()/10)
			self.SubVentanaMonitorAlertas.tableWidget_Log.setColumnWidth(4,self.SubVentanaMonitorAlertas.tableWidget_Log.width()/20)
			self.SubVentanaMonitorAlertas.tableWidget_Log.setColumnWidth(5,self.SubVentanaMonitorAlertas.tableWidget_Log.width()/7)
			
			self.SubVentanaMonitorAlertas.tableWidget_Cola.setColumnWidth(0,self.SubVentanaMonitorAlertas.tableWidget_Cola.width()/3.3)
			self.SubVentanaMonitorAlertas.tableWidget_Cola.setColumnWidth(1,self.SubVentanaMonitorAlertas.tableWidget_Cola.width()/5)
			self.SubVentanaMonitorAlertas.tableWidget_Cola.setColumnWidth(2,self.SubVentanaMonitorAlertas.tableWidget_Cola.width()/5)
			self.SubVentanaMonitorAlertas.tableWidget_Cola.setColumnWidth(3,self.SubVentanaMonitorAlertas.tableWidget_Cola.width()/3.3)

			self.SubVentanaMonitorAlertas.tableWidget_Enviados.setColumnWidth(0,self.SubVentanaMonitorAlertas.tableWidget_Enviados.width()/3.3)
			self.SubVentanaMonitorAlertas.tableWidget_Enviados.setColumnWidth(1,self.SubVentanaMonitorAlertas.tableWidget_Enviados.width()/5)
			self.SubVentanaMonitorAlertas.tableWidget_Enviados.setColumnWidth(2,self.SubVentanaMonitorAlertas.tableWidget_Enviados.width()/5)
			self.SubVentanaMonitorAlertas.tableWidget_Enviados.setColumnWidth(3,self.SubVentanaMonitorAlertas.tableWidget_Enviados.width()/3.3)


			self.SubVentanaMonitorAlertas.tableWidget_Recibidos.setColumnWidth(0,self.SubVentanaMonitorAlertas.tableWidget_Recibidos.width()/3.3)
			self.SubVentanaMonitorAlertas.tableWidget_Recibidos.setColumnWidth(1,self.SubVentanaMonitorAlertas.tableWidget_Recibidos.width()/3.3)
			self.SubVentanaMonitorAlertas.tableWidget_Recibidos.setColumnWidth(2,self.SubVentanaMonitorAlertas.tableWidget_Recibidos.width()/3.3)

		self.Resize = True			

	def Inicio(self):
		self.HiloMoniAlert = HiloMonitoreoAlertas(self,self.SubVentanaMonitorAlertas.tableWidget_Log,self.SubVentanaMonitorAlertas.tableWidget_Cola,self.SubVentanaMonitorAlertas.tableWidget_Enviados,self.SubVentanaMonitorAlertas.tableWidget_Recibidos,self.SubVentanaMonitorAlertas.label_ColaMensajes)
		self.HiloMoniAlert.start()

	def closeEvent(self,event):
		self.HiloMoniAlert.terminate()
		del self.HiloMoniAlert
		event.accept()

	


class HiloMonitoreoAlertas(QtCore.QThread):
	def __init__(self,parent,tablalog,tablacola,tablaenviados,tablarecibidos,labelcola):
		QtCore.QThread.__init__(self)
		self.parent = parent
		self.tablalog = tablalog
		self.tablacola = tablacola
		self.tablaenviados = tablaenviados
		self.tablarecibidos = tablarecibidos
		self.labelcola = labelcola

	def CargarLogSenales(self):
		ResultadoLogSenales =	globalvars.BD.Querys('LogSenalesMonitoreoAlertas')


		print 'Buscando Log Senales'
		#Buscar las senales por procesar por primera vez
		rows = len(ResultadoLogSenales)
		self.tablalog.setRowCount(rows)
		fila = 0
		columna = 0
		for signalpp in ResultadoLogSenales:
			columna = 0
			for signal in signalpp:
				#print signal
				#print type(signal)
				if columna <= 5:
					if signal == None:
						signal = ''
					else:
						if columna > 0 and columna < 5:
							signal = signal
						if columna == 5:
							signal = signal.strftime("%A, %d %b %Y %H:%M:%S")
						if type(signal) == int:
							signal = str(signal)
					texto = QtGui.QTableWidgetItem(signal)
					self.tablalog.setItem(fila,columna,texto)
				elif columna == 6:
					colorfila = QtGui.QColor(str(signal))
					for columnacolor in range(5):
						self.tablalog.item(fila,columnacolor).setTextColor(colorfila)
				else:
					break
				columna = columna + 1
			fila = fila + 1


	def CargarMensajesRecibidos(self):
		ResultadoRecibidos =	globalvars.BD.Querys('SeleccionarMensajesRecibidos')

		print 'Buscando Recibidos'
		#Buscar las senales por procesar por primera vez
		rows = len(ResultadoRecibidos)
		self.tablarecibidos.setRowCount(rows)
		fila = 0
		columna = 0
		for mensajes in ResultadoRecibidos:
			columna = 0
			for signal in mensajes:
				if columna <= 2:
					if signal == None:
						signal = ''
					else:
						if columna > 0 and columna < 2:
							signal = signal
						if columna == 2:
							signal = signal.strftime("%A, %d %b %Y %H:%M:%S")
						if type(signal) == int:
							signal = str(signal)
					texto = QtGui.QTableWidgetItem(signal)
					self.tablarecibidos.setItem(fila,columna,texto)
				else:
					break
				columna = columna + 1
			fila = fila + 1

	
	def CargarMensajesEnviados(self):
		ResultadoEnviados =	globalvars.BD.Querys('SeleccionarMensajesEnviado')

		print 'Buscando Enviados'
		#Buscar las senales por procesar por primera vez
		rows = len(ResultadoEnviados)
		self.tablaenviados.setRowCount(rows)
		fila = 0
		columna = 0
		for mensajes in ResultadoEnviados:
			columna = 0
			for signal in mensajes:
				if columna <= 3:
					if signal == None:
						signal = ''
					else:
						if columna > 0 and columna < 3:
							signal = signal
						if columna == 3:
							signal = signal.strftime("%A, %d %b %Y %H:%M:%S")
						if type(signal) == int:
							signal = str(signal)
					texto = QtGui.QTableWidgetItem(signal)
					self.tablaenviados.setItem(fila,columna,texto)
				else:
					break
				columna = columna + 1
			fila = fila + 1

	def CargarMensajesCola(self):
		ResultadoCola =	globalvars.BD.Querys('SeleccionarMensajesCola')

		print 'Buscando Cola'
		#Buscar las senales por procesar por primera vez
		rows = len(ResultadoCola)
		self.tablacola.setRowCount(rows)
		fila = 0
		columna = 0
		for mensajes in ResultadoCola:
			columna = 0
			for signal in mensajes:
				if columna <= 3:
					if signal == None:
						signal = ''
					else:
						if columna > 0 and columna < 3:
							signal = signal
						if columna == 3:
							signal = signal.strftime("%A, %d %b %Y %H:%M:%S")
						if type(signal) == int:
							signal = str(signal)
					texto = QtGui.QTableWidgetItem(signal)
					self.tablacola.setItem(fila,columna,texto)
				else:
					break
				columna = columna + 1
			fila = fila + 1
		


	def run(self):
		self.Iniciar()

	def Iniciar(self):
		while True:
			self.CargarLogSenales()
			self.CargarMensajesCola()
			self.CargarMensajesEnviados()
			self.CargarMensajesRecibidos()
			time.sleep(1)

if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	#app.setStyle(QtGui.QStyleFactory.create("sgi"))
	window = VentanaMain()
	#qss_file = open('style_file.qss').read()
	#window.setStyleSheet(qss_file)
	window.showMaximized()
	app.exec_()
