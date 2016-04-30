#Importamos el Modulo Pyodbc para conexion con la base de datos
import pyodbc
#Importamos el modulo para archivos INI
from ConfigParser import ConfigParser
#Importamos Desencriptador XOR Pycrypto
from Crypto.Cipher import XOR
import base64
import time, datetime

class BasedeDatos(object):
	def __init__(self):
		self.resultado = None
		#Buscando el archivo INI para saber el String de Conexion
		config = ConfigParser()
		config.read("conf/config.ini")
		self.conexioncifrada = config.get('BASE DE DATOS', 'conexion')
		PASSWORD = XOR.new(base64.b64decode('MjAxMDE3MzMtOTYwOTkyNg=='))
		self.conexion = PASSWORD.decrypt(base64.b64decode(str(self.conexioncifrada)))
		self.cantidad = 0
	def Conectar(self):
		self.cnxn = pyodbc.connect(self.conexion)
		self.cursor = self.cnxn.cursor()
	def Querys(self,nombrequery,*datos):
		#time.sleep(0.1)
		self.cantidad = self.cantidad + 1
		print nombrequery + str(self.cantidad)

		if nombrequery == 'LoginPersonal':
			self.cursor.execute('SELECT o.idPersonal, o.nombre, o.id_empresa,o.correo, em.latitud, em.longuitud, e.id_pais, e.nombre AS NameEmpresa, e.web, o.estatus, e.master, e.logo, e.direccion, o.imagen, e.webTheme, o.webTheme AS themePer, e.webThemeSoport, o.WebThemeSoport AS themeSoportPer, o.id_perfil, ce.timeAlertPen, ce.timeHombreM, ce.timeNotifiHombre, ce.correosHombre FROM sSMS_Personal o INNER JOIN sSMS_Empresas e ON o.id_empresa = e.id_empresa INNER JOIN sSMS_Empresas em ON e.id_empresa = em.id_empresa INNER JOIN smsalarmas_ConfigEmpresas ce ON e.id_empresa = ce.id_empresa  WHERE o.usuario = ? AND o.clave = ?  AND o.eliminado=0;',datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'ListarClientesIDNombre':
			self.cursor.execute('SELECT  id_cliente, nombre_cliente FROM sSMS_Clientes')
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'ListarClientesTodos':
			self.cursor.execute('SELECT  id_cliente, nombre_cliente, direccion, email,telf_local FROM sSMS_Clientes')
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'ListarClientesTodosLike':
			self.cursor.execute("SELECT  id_cliente, nombre_cliente, direccion, email,telf_local FROM sSMS_Clientes where nombre_cliente like ? or id_cliente like ?",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'ListarClientesEmpresas':
			self.cursor.execute('SELECT  id_cliente, id_empresa, nombre_cliente, status, status_web, telf_local, ciudad, email FROM sSMS_Clientes WHERE (id_empresa = ?);',datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'DatosPanelCliente':
			self.cursor.execute("SELECT E.latitud as LatiEmpresa, E.longuitud as LongiEmpresa,E.nombre as Empresa, C.id_cliente,C.latitud,C.longitud,C.rif,C.clave,C.fechinicio,sSMS_StatusCliente.Descrip AS StatusC,TC.descrip AS TipoC, P.descrip AS Protocolo, TA.Descrip AS TipoAlarma,  C.nombre_cliente, C.ciudad, C.direccion, C.referencia, C.telf_local,C.imagen as pic, C.telf_fax, C.telf_movil, C.email, C.web_site, CASE WHEN cast(C.fecha_corte AS varchar(20)) IS NULL THEN 'Sin fecha de corte' ELSE cast(C.fecha_corte AS varchar(20)) END AS fecha_corte, C.monto, C.nombre, (select m.manual_file from sSMS_TypeAlarmaManual m where m.id_tipo_manual=1 and m.id_manual=TA.id_manual_help) as manu_help, C.login, C.clave, C.status_web,TC.img as icon, pa.descripcion AS pais, es.descripcion AS estado ,c.clavemaster FROM sSMS_Paises AS pa INNER JOIN  sSMS_PaisEstados AS es ON pa.id_pais = es.id_pais RIGHT OUTER JOIN sSMS_Clientes AS C INNER JOIN sSMS_Protocolos AS P ON C.id_protocolo = P.id_protocolo ON es.id_estado = C.id_estado LEFT OUTER JOIN  sSMS_Empresas AS E ON C.id_empresa = E.id_empresa LEFT OUTER JOIN  sSMS_StatusCliente ON C.id_status = sSMS_StatusCliente.id_Status LEFT OUTER JOIN sSMS_TypeCliente AS TC ON C.id_type_cliente = TC.id_type_empresa LEFT OUTER JOIN  sSMS_TypeAlarma AS TA ON C.alarma = TA.id_Alarma  WHERE C.id_cliente = ?",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'ZonasCliente':
			self.cursor.execute("SELECT  cast(id_zona as int) as id_zona, descrip as str_zona,ubicacion  FROM  sSMS_ClienteZonas where id_cliente = ?",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'UsuariosCliente':
			self.cursor.execute("SELECT id_user,nombre + ' ' + apellido AS nombre , email , movil FROM sSMS_Usuarios WHERE id_cliente = ? AND id_user < 500",datos)
			self.resultado = self.cursor.fetchall()
		
		elif nombrequery == 'DatosUsuarioCliente':
			self.cursor.execute("SELECT * FROM sSMS_Usuarios u WHERE (id_user = ?) AND (id_cliente = ?)",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'ContactosEmergenciaCliente':
			self.cursor.execute("SELECT nombre, numero, descript, observacion, id_numero from sSMS_NumEmergencia  WHERE (id_cliente = ?)",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'ContactoEmergenciaDatos':
			self.cursor.execute("SELECT * FROM sSMS_NumEmergencia  WHERE id_cliente = ? AND numero = ?",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'VerificarContactoEmergencia':
			self.cursor.execute("SELECT descript,nombre,numero FROM sSMS_NumEmergencia where id_cliente = ? and numero = ?",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'DiasSMSCliente':
			self.cursor.execute("SELECT DISTINCT TOP 31 CAST(CAST(send_date AS varchar(11)) AS smalldatetime) AS fech FROM sSMS_MensajesSend WHERE id_cliente = ? ORDER BY fech DESC",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'MensajesEnviandosClienteFecha':
			self.cursor.execute("SELECT  movil, send_date, sms FROM sSMS_MensajesSend WHERE CAST(send_date AS DATE ) = ? AND status = 1 AND id_cliente = ? ORDER BY send_date DESC ",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'DiasSenalesCliente':
			self.cursor.execute("SELECT DISTINCT TOP 20 CAST(LEFT(fecha, 12)  AS SMALLDATETIME) AS fechaSalida FROM sSMS_Tramas WHERE (cliente = ?) ORDER BY fechaSalida DESC",datos)
			self.resultado = self.cursor.fetchall()
		
		elif nombrequery == 'SenalesClienteFecha':
			self.cursor.execute("SELECT descript, UserZona, fecha, Fecha_proc, web_color FROM cSMS_HistorialSenales WHERE cliente = ? AND CAST(fecha AS DATE ) = ? ORDER BY fecha DESC ",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SenalesUltimas100Cliete':
			self.cursor.execute("SELECT TOP 100 descript, UserZona, fecha, Fecha_proc, web_color FROM cSMS_HistorialSenales WHERE (cliente = ?) ORDER BY fecha DESC",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'NotasCliente':
			self.cursor.execute("SELECT top 1 IdNota,NotaFija,NotaTemp, CAST(CONVERT(NVARCHAR, FechaIni, 112) AS DATETIME)  AS FechaIni, CAST(CONVERT(NVARCHAR, FechaFin, 112) AS DATETIME) AS FechaFin FROM sSMS_NotasClientes WHERE (IdCliente = ?) ORDER BY IdNota DESC",datos)
			self.resultado = self.cursor.fetchall()
		
		elif nombrequery == 'HorariosClienteTodos':
			#Ojo la interfaz no concuerda con la base de datos, hice una copia del Web pero en la BD
			#Puede ser distinto el dia de apertura que el de cierre pero aqui no lo permite porque en el web tampoco
			self.cursor.execute("SELECT Id, diaapertura, horaapertura, horacierre FROM sSMS_HorariosOC WHERE (id_cliente = ?) ",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'HorariosClienteDia':
			#Ojo la interfaz no concuerda con la base de datos, hice una copia del Web pero en la BD
			#Puede ser distinto el dia de apertura que el de cierre pero aqui no lo permite porque en el web tampoco
			self.cursor.execute("SELECT Id, diaapertura, horaapertura, horacierre FROM sSMS_HorariosOC WHERE id_cliente = ? AND diaapertura = ? ",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'PlanesProtocoloCliente':
			self.cursor.execute(" SELECT p.* FROM sSMS_Clientes c INNER JOIN sSMS_Planes p ON c.id_protocolo = p.id_protocolo WHERE c.id_cliente = ?",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'EventosDetalleCliente':
			self.cursor.execute(" SELECT EP.cod_evento, E.descript FROM sSMS_Clientes C INNER JOIN sSMS_Planes P ON C.id_protocolo = P.id_protocolo   INNER JOIN sSMS_EventosPlanes EP ON P.id_plan = EP.id_plan AND P.id_protocolo = EP.id_protocolo INNER JOIN sSMS_Eventos E ON EP.cod_evento = E.cod_event AND EP.id_protocolo = E.id_protocolo WHERE (C.id_cliente = ?) AND (P.id_plan = ?)",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'TodosUsuariosEventosCliente':
			self.cursor.execute("SELECT DISTINCT sSMS_Usuarios.nombre + ' ' + sSMS_Usuarios.apellido AS nombrecompleto, sSMS_Usuarios.* FROM  sSMS_Usuarios INNER JOIN sSMS_ClienteEventos ON sSMS_Usuarios.id_cliente =   sSMS_ClienteEventos.id_cliente AND sSMS_Usuarios.id_user = sSMS_ClienteEventos.id_user   WHERE (sSMS_Usuarios.id_cliente = ?) AND (sSMS_Usuarios.id_user < 500) order by sSMS_Usuarios.id_user",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'EventosUsuarioCliente':
			self.cursor.execute("SELECT E.cod_event, E.descript, CE.type FROM sSMS_ClienteEventos CE INNER JOIN sSMS_Eventos E ON CE.cod_evento = E.cod_event INNER JOIN sSMS_Clientes C ON CE.id_cliente = C.id_cliente AND  E.id_protocolo = C.id_protocolo WHERE     (CE.id_user = ?) AND (CE.id_cliente = ?) ORDER BY CE.type DESC",datos)
			self.resultado = self.cursor.fetchall()	

		elif nombrequery == 'PlanesUsuariosCliente':
			self.cursor.execute("SELECT EP.*, E.descript FROM sSMS_Clientes C INNER JOIN sSMS_Planes P ON C.id_protocolo = P.id_protocolo   INNER JOIN sSMS_EventosPlanes EP ON P.id_plan = EP.id_plan AND P.id_protocolo = EP.id_protocolo INNER JOIN sSMS_Eventos E ON EP.cod_evento = E.cod_event AND EP.id_protocolo = E.id_protocolo WHERE (C.id_cliente =?) AND (P.id_plan =?)",datos)
			self.resultado = self.cursor.fetchall()	

		elif nombrequery == 'NombrePlan':
			self.cursor.execute("SELECT descrip FROM sSMS_Planes where id_plan = ?",datos)
			self.resultado = self.cursor.fetchall()	
	
		elif nombrequery == 'DatosReceptores':
			self.cursor.execute("SELECT descrip FROM sSMS_Planes where id_plan = ?",datos)
			self.resultado = self.cursor.fetchall()	

		elif nombrequery == 'DatosAsociados':
			self.cursor.execute("SELECT nombre, email, status, id_asociado, direccion, telef_contacto, id_empresa,usuario, clave  FROM smsalarmas_asociados where id_empresa = ?",datos)
			self.resultado = self.cursor.fetchall()	
		
		elif nombrequery == 'CantidadAsociadosAbonados':
			self.cursor.execute("SELECT COUNT(*) AS Total FROM   smsalarmas_asociados_abonados  WHERE (id_asociado = ?) AND (id_empresa = ?)",datos)
			self.resultado = self.cursor.fetchall()	

		elif nombrequery == 'AbonadosEnGrupo':
			self.cursor.execute("SELECT  sSMS_Clientes.id_cliente, sSMS_Clientes.nombre_cliente  as nombre FROM  smsalarmas_asociados_abonados ASO INNER JOIN  sSMS_Clientes ON ASO.id_cliente = sSMS_Clientes.id_cliente  WHERE  ASO.id_asociado = ?",datos)
			self.resultado = self.cursor.fetchall()	

		elif nombrequery == 'AbonadosSinGrupo':
			self.cursor.execute("SELECT  id_cliente, nombre_cliente FROM sSMS_Clientes WHERE (id_cliente NOT IN (SELECT  id_cliente FROM  smsalarmas_asociados_abonados   WHERE id_asociado =  ?)) order by id_cliente asc",datos)
			self.resultado = self.cursor.fetchall()	
		
		elif nombrequery == 'VerificarUsuarioAsociado':
			self.cursor.execute("SELECT * FROM smsalarmas_asociados WHERE (usuario = ? ) ",datos)
			self.resultado = self.cursor.fetchall()	

		elif nombrequery == 'Paises':
			self.cursor.execute("SELECT * FROM sSMS_Paises  order by descripcion asc")
			self.resultado = self.cursor.fetchall()	

		elif nombrequery == 'EstadosPaises':
			self.cursor.execute(" SELECT * FROM sSMS_PaisEstados where id_pais=? ",datos)
			self.resultado = self.cursor.fetchall()	

		elif nombrequery == 'Protocolos':
			self.cursor.execute("SELECT descrip, id_protocolo FROM sSMS_Protocolos")
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'TiposClientes':
			self.cursor.execute("SELECT id_type_empresa, descrip FROM sSMS_TypeCliente")
			self.resultado = self.cursor.fetchall()	

		elif nombrequery == 'TiposAlarmas':
			self.cursor.execute("SELECT id_Alarma,Descrip FROM sSMS_TypeAlarma order by Descrip")
			self.resultado = self.cursor.fetchall()	

		elif nombrequery == 'Empresas':
			self.cursor.execute("SELECT id_empresa, nombre FROM sSMS_Empresas")
			self.resultado = self.cursor.fetchall()	

		elif nombrequery == 'VerificarAbonado':
			self.cursor.execute("SELECT * FROM sSMS_Clientes WHERE (id_cliente = ? ) ",datos)
			self.resultado = self.cursor.fetchall()	

		elif nombrequery == 'EstatusGenerales':
			self.cursor.execute("SELECT * FROM sSMS_StatusGeneral ")
			self.resultado = self.cursor.fetchall()
		
		elif nombrequery == 'VerificarZona':
			self.cursor.execute("SELECT cast(id_zona as int) as id_zona, descrip  FROM  sSMS_ClienteZonas where (id_zona=?) AND (id_cliente =?)",datos)
			self.resultado = self.cursor.fetchall()	

		elif nombrequery == 'VerificarUsuario':
			self.cursor.execute("SELECT cast(id_user as int) as id_user, nombre + ' ' + apellido AS nombre  FROM  sSMS_Usuarios where (id_user=?) AND (id_cliente =?)",datos)
			self.resultado = self.cursor.fetchall()			

		elif nombrequery == 'TiposUsuarioClientes': 
			self.cursor.execute("SELECT id_type_user, descrip FROM sSMS_TypeUser t order by id_type_user asc")
			self.resultado = self.cursor.fetchall()	

		elif nombrequery == 'FrecuenciaEmail': 
			self.cursor.execute("SELECT id_frecuencia, descripcion FROM sSMS_FrecuenciaEmail order by descripcion")
			self.resultado = self.cursor.fetchall()	

		elif nombrequery == 'SeleccionarUnHorario': 
			self.cursor.execute("SELECT * FROM   sSMS_HorariosOC WHERE  id_cliente = ?  and Id = ?",datos)
			self.resultado = self.cursor.fetchall()		

		elif nombrequery == 'ClientesSinImagen': 
			self.cursor.execute("SELECT id_cliente, nombre_cliente FROM sSMS_Clientes c WHERE (id_cliente > 0) AND  (imagen IS NULL OR imagen = '')")
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'ListaTiposCliente': 
			self.cursor.execute("SELECT id_type_empresa, descrip, img, monto FROM sSMS_TypeCliente")
			self.resultado = self.cursor.fetchall()
		
		elif nombrequery == 'VerificarIDTipoCliente': 
			self.cursor.execute("SELECT  descrip, id_type_empresa FROM sSMS_TypeCliente WHERE  id_type_empresa = ?",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'UnTipoCliente': 
			self.cursor.execute("SELECT TOP 1 id_type_empresa, descrip, img, monto FROM sSMS_TypeCliente WHERE id_type_empresa = ?",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'DepartamentosEmpresa': 
			self.cursor.execute("SELECT idDepartamento, nombre, correo FROM sSMS_DepartamentosEmpresa WHERE idEmpresa = ?",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'UnDepartamentosEmpresa': 
			self.cursor.execute("SELECT idDepartamento, nombre, correo FROM sSMS_DepartamentosEmpresa WHERE idDepartamento = ?",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'GruposdeAlarmas': 
			self.cursor.execute("SELECT * FROM sSMS_GrupoCodigosAlarma",datos)
			self.resultado = self.cursor.fetchall()	

		elif nombrequery == 'SenalesBusquedaAvanzada':
			self.cursor.execute("SELECT descript, UserZona, fecha, Fecha_proc, web_color FROM cSMS_HistorialSenales WHERE cliente = ? AND CAST(fecha AS DATE ) >= ? AND CAST(fecha AS DATE ) <= ? AND idGrupo = ?  ORDER BY fecha DESC ",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'TiposAlarmas':
			self.cursor.execute("SELECT id_Alarma,Descrip FROM sSMS_TypeAlarma order by Descrip")
			self.resultado = self.cursor.fetchall()	

		elif nombrequery == 'UnTipoAlarma':
			self.cursor.execute("SELECT id_Alarma, Descrip, id_manual_help, id_manual_user, id_manual_prog FROM sSMS_TypeAlarma  where id_Alarma = ?",datos)
			self.resultado = self.cursor.fetchall()	

		elif nombrequery == 'StatusPanel':
			self.cursor.execute("SELECT * FROM sSMS_StatusPanelCliente where idCliente = ?",datos)
			self.resultado = self.cursor.fetchall()	

		elif nombrequery == 'DatosClienteParaMapa':
			self.cursor.execute("SELECT [latitud],[longitud] FROM [Soluciones-SMSSecure].[dbo].[sSMS_Clientes] where id_cliente= ?",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'TramasPorProcesarOperador':
			self.cursor.execute('''SELECT     T.cliente AS id_cliente, C.nombre_cliente AS NameCliente, CASE WHEN E.descript IS NULL THEN 'Evento ' + CAST(t .evento AS varchar(10)) 
					  + ' no definido' ELSE E.descript END AS StrEvento, CASE WHEN E.type_evento = 0 THEN CASE WHEN U.nombre IS NULL 
					  THEN 'Usuario ' + CAST(T .user_zone AS varchar(6)) ELSE U.nombre + ' ' + U.apellido END WHEN E.type_evento = 1 THEN CASE WHEN Z.descrip IS NULL 
					  THEN 'Zona ' + CAST(T .user_zone AS varchar(6)) ELSE Z.descrip END WHEN E.type_evento = 2 THEN '' END AS UserZona, T.fecha, E.web_color, T.id_trama, 
					  E.web_colorBg, T.protocolo, T.Linea, T.descrip, E.type_evento, T.evento, T.cliente, T.Variante, E.color, E.colorBg, CASE WHEN t .observacion IS NULL 
					  THEN 'SO' ELSE t .observacion END AS Obser, ca.idGrupo, T.status, C.id_empresa, C.direccion, C.referencia, C.latitud, C.longitud, C.clavemaster, C.id_type_cliente, 
					  ty.img, C.telf_local, C.imagen AS pic, ca.codigo AS codAlrm, ca.descript AS codDesc, stp.cod_alarm AS staPanel, stp.Fecha AS fechaStatusp, 
					  sSMS_Empresas.nombre AS nombreempresa, C.telf_movil AS movil
FROM         sSMS_TypeCliente AS ty INNER JOIN
					  sSMS_Clientes AS C ON ty.id_type_empresa = C.id_type_cliente INNER JOIN
					  sSMS_Empresas ON C.id_empresa = sSMS_Empresas.id_empresa LEFT OUTER JOIN
					  sSMS_StatusPanelCliente AS stp ON C.id_cliente = stp.idCliente RIGHT OUTER JOIN
					  sSMS_Usuarios AS U RIGHT OUTER JOIN
					  sSMS_Eventos AS E INNER JOIN
					  sSMS_TramasPorProcesar AS T ON E.cod_event = T.evento AND E.id_protocolo = T.protocolo LEFT OUTER JOIN
					  sSMS_CodigosAlarma AS ca ON E.cod_alarm = ca.codigo ON U.id_cliente = T.cliente AND U.cod_user = T.user_zone LEFT OUTER JOIN
					  sSMS_ClienteZonas AS Z ON T.cliente = Z.id_cliente AND T.user_zone = Z.id_zona ON C.id_cliente = T.cliente
WHERE     T.status in(0,1) AND (T.IdOperador = ?) order by id_trama desc
''',datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'TramasPendientesOperador':
			self.cursor.execute('''SELECT     T.cliente AS id_cliente, C.nombre_cliente AS NameCliente, CASE WHEN E.descript IS NULL THEN 'Evento ' + CAST(t .evento AS varchar(10)) 
					  + ' no definido' ELSE E.descript END AS StrEvento, CASE WHEN E.type_evento = 0 THEN CASE WHEN U.nombre IS NULL 
					  THEN 'Usuario ' + CAST(T .user_zone AS varchar(6)) ELSE U.nombre + ' ' + U.apellido END WHEN E.type_evento = 1 THEN CASE WHEN Z.descrip IS NULL 
					  THEN 'Zona ' + CAST(T .user_zone AS varchar(6)) ELSE Z.descrip END WHEN E.type_evento = 2 THEN '' END AS UserZona, T.fecha, E.web_color, T.id_trama, 
					  E.web_colorBg, T.protocolo, T.Linea, T.descrip, E.type_evento, T.evento, T.cliente, T.Variante, E.color, E.colorBg, CASE WHEN t .observacion IS NULL 
					  THEN 'SO' ELSE t .observacion END AS Obser, ca.idGrupo, T.status, C.id_empresa, C.direccion, C.referencia, C.latitud, C.longitud, C.clavemaster, C.id_type_cliente, 
					  ty.img, C.telf_local, C.imagen AS pic, ca.codigo AS codAlrm, ca.descript AS codDesc, stp.cod_alarm AS staPanel, stp.Fecha AS fechaStatusp, 
					  sSMS_Empresas.nombre AS nombreempresa, C.telf_movil AS movil
FROM         sSMS_TypeCliente AS ty INNER JOIN
					  sSMS_Clientes AS C ON ty.id_type_empresa = C.id_type_cliente INNER JOIN
					  sSMS_Empresas ON C.id_empresa = sSMS_Empresas.id_empresa LEFT OUTER JOIN
					  sSMS_StatusPanelCliente AS stp ON C.id_cliente = stp.idCliente RIGHT OUTER JOIN
					  sSMS_Usuarios AS U RIGHT OUTER JOIN
					  sSMS_Eventos AS E INNER JOIN
					  sSMS_TramasPorProcesar AS T ON E.cod_event = T.evento AND E.id_protocolo = T.protocolo LEFT OUTER JOIN
					  sSMS_CodigosAlarma AS ca ON E.cod_alarm = ca.codigo ON U.id_cliente = T.cliente AND U.cod_user = T.user_zone LEFT OUTER JOIN
					  sSMS_ClienteZonas AS Z ON T.cliente = Z.id_cliente AND T.user_zone = Z.id_zona ON C.id_cliente = T.cliente WHERE T.status = 4
 AND (T.IdOperador = ?) ORDER BY T.id_trama DESC''',datos)
			self.resultado = self.cursor.fetchall()


		elif nombrequery == 'MonitoreoEstatico':  #Log Senales
			self.cursor.execute('''SELECT TOP (100) T.cliente AS id_cliente, C.nombre_cliente AS NameCliente, E.descript AS StrEvento, CASE WHEN E.type_evento = 0 THEN CASE WHEN U.nombre IS NULL 
						 THEN 'Usuario ' + CAST(T .user_zone AS varchar(3)) ELSE U.nombre + ' ' + U.apellido END WHEN E.type_evento = 1 THEN CASE WHEN Z.descrip IS NULL 
						 THEN 'Zona ' + CAST(T .user_zone AS varchar(3)) ELSE Z.descrip END WHEN E.type_evento = 2 THEN '' END AS UserZona, T.fecha, E.web_color, E.web_colorBg, T.id_trama, 
						 E.cod_event AS codEvento, C.imagen AS pic, T.protocolo AS CodProtocolo
FROM            sSMS_Usuarios AS U RIGHT OUTER JOIN
						 sSMS_Eventos AS E INNER JOIN
						 sSMS_Tramas AS T ON E.cod_event = T.evento AND E.id_protocolo = T.protocolo LEFT OUTER JOIN
						 sSMS_Personal AS p ON T.IdOperador = p.idPersonal ON U.id_cliente = T.cliente AND U.cod_user = T.user_zone LEFT OUTER JOIN
						 sSMS_ClienteZonas AS Z ON T.cliente = Z.id_cliente AND T.user_zone = Z.id_zona LEFT OUTER JOIN
						 sSMS_Clientes AS C ON T.cliente = C.id_cliente
ORDER BY T.id_trama DESC''',datos)
			self.resultado = self.cursor.fetchall()


		elif nombrequery == 'TramasProcesadas':  
			self.cursor.execute('''SELECT TOP (100) T.cliente AS id_cliente, CASE WHEN C.nombre_cliente IS NULL THEN 'Cliente NO Definido' ELSE C.nombre_cliente END AS NameCliente, 
						 E.cod_event + ' - ' + E.descript AS StrEvento,
						 CASE WHEN E.type_evento = 0 THEN CASE WHEN U.nombre IS NULL THEN 'Usuario ' + CAST(T .user_zone AS varchar(3)) 
						 ELSE U.nombre + ' ' + U.apellido END WHEN E.type_evento = 1 THEN CASE WHEN Z.descrip IS NULL THEN 'Zona ' + CAST(T .user_zone AS varchar(3)) 
						 ELSE Z.descrip END WHEN E.type_evento = 2 THEN '' END AS UserZona, CASE WHEN T .observacion IS NULL THEN 'SO' ELSE T .observacion END AS Obser, T.fecha, T.Fecha_proc, E.web_color AS color, E.web_colorBg AS colorBg,  T.id_trama, 
						 C.imagen AS pic, E.type_evento AS TipoEvento, T.protocolo AS CodProtocolo, T.IdOperador, p.nombre AS operador
FROM            sSMS_Usuarios AS U RIGHT OUTER JOIN
						 sSMS_Eventos AS E INNER JOIN
						 sSMS_TramasProcesadas AS T ON E.cod_event = T.evento AND E.id_protocolo = T.protocolo LEFT OUTER JOIN
						 sSMS_Personal AS p ON T.IdOperador = p.idPersonal ON U.id_cliente = T.cliente AND U.cod_user = T.user_zone LEFT OUTER JOIN
						 sSMS_ClienteZonas AS Z ON T.cliente = Z.id_cliente AND T.user_zone = Z.id_zona LEFT OUTER JOIN
						 sSMS_Clientes AS C ON T.cliente = C.id_cliente
WHERE        (T.EmpresaMonitorea = ?)
ORDER BY T.Fecha_proc DESC, T.id_trama DESC''',datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'ComprobarExisteOperadorSession': #Saber si existo en la Tabla de OperadorSession
			self.cursor.execute("SELECT TOP 1 [IdOperador] FROM [Soluciones-SMSSecure].[dbo].[sSMS_OperadorSession] where IdOperador = ?",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'DatosClienteSenalMonitoreo':
			self.cursor.execute("""SELECT        sSMS_Clientes.id_cliente, sSMS_Clientes.nombre_cliente, sSMS_TramasPorProcesar.fecha, sSMS_Clientes.direccion, sSMS_Clientes.referencia, 
						 sSMS_StatusPanelCliente.cod_alarm AS StatusPanel, sSMS_StatusPanelCliente.Fecha AS fechastatuspanel, sSMS_TramasPorProcesar.user_zone, 
						 sSMS_TramasPorProcesar.evento, sSMS_Empresas.nombre AS nameempresa, sSMS_Clientes.telf_local, sSMS_Clientes.telf_movil, sSMS_Clientes.clavemaster, 
						 sSMS_Eventos.descript
FROM            sSMS_Clientes INNER JOIN
						 sSMS_TramasPorProcesar ON sSMS_Clientes.id_cliente = sSMS_TramasPorProcesar.cliente INNER JOIN
						 sSMS_StatusPanelCliente ON sSMS_Clientes.id_cliente = sSMS_StatusPanelCliente.idCliente INNER JOIN
						 sSMS_Empresas ON sSMS_Clientes.id_empresa = sSMS_Empresas.id_empresa INNER JOIN
						 sSMS_Eventos ON sSMS_TramasPorProcesar.evento = sSMS_Eventos.cod_event
WHERE        (sSMS_TramasPorProcesar.id_trama =?)""",datos)
			self.resultado = self.cursor.fetchall()


		elif nombrequery == 'MensajesPredefinidosMonitoreo':
			self.cursor.execute("""SELECT mensaje FROM sSMS_MensajesCierre""")
			self.resultado = self.cursor.fetchall()
	
		elif nombrequery == 'MapaClienteMonitoreo':
			self.cursor.execute("""SELECT     c.nombre_cliente, c.latitud AS latclie, c.longitud AS logclie, em.latitud AS latemp , em.longuitud AS logemp, c.direccion AS dirclie, c.referencia AS refclie, e.nombre AS nomemp, c.id_type_cliente, t.img AS icon FROM sSMS_Clientes c INNER JOIN  sSMS_Empresas em ON c.id_empresa = em.id_empresa INNER JOIN  sSMS_Empresas e ON em.id_empresa = e.id_empresa INNER JOIN sSMS_TypeCliente t ON c.id_type_cliente = t.id_type_empresa WHERE (c.id_cliente = ?)""",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'NumerosEmergenciaMonitoreo':
			self.cursor.execute("""SELECT nombre, numero, descript, observacion FROM sSMS_NumEmergencia WHERE (id_cliente = ?)""",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'UsuariosEmergenciaMonitoreo':
			self.cursor.execute("""SELECT  sSMS_Usuarios.nombre + ' ' + sSMS_Usuarios.apellido + ' (' + sSMS_TypeUser.descrip + ')' AS descript,sSMS_Usuarios.movil AS numero, sSMS_Usuarios.clavevoz FROM sSMS_Usuarios INNER JOIN sSMS_TypeUser ON sSMS_Usuarios.id_type_user = sSMS_TypeUser.id_type_user WHERE (sSMS_Usuarios.id_cliente = ?)  AND (sSMS_Usuarios.id_user < 500) order by sSMS_Usuarios.id_user asc""",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'TimeLineSenal':
			self.cursor.execute("""SELECT sSMS_TramasObservaciones.fecha, sSMS_TramasObservaciones.observacion , (CAST(sSMS_TramasObservaciones.idoperador as varchar(10))COLLATE Modern_Spanish_CI_AS) +' - ' + (sSMS_Personal.nombre COLLATE Modern_Spanish_CI_AS) FROM sSMS_TramasObservaciones INNER JOIN sSMS_Personal ON sSMS_TramasObservaciones.idoperador = sSMS_Personal.idPersonal WHERE (sSMS_TramasObservaciones.idtrama = ?) ORDER BY sSMS_TramasObservaciones.fecha DESC""",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'OperadoresActivosWeb':   #Para verificar los operadores que estan activos en el web por Base de Datos
			self.cursor.execute("SELECT IdOperador, Ip, StatusMonitoreo FROM sSMS_OperadorSession where statuslogin = 1")
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'CierreSenalPorCliente':   #Para verificar los operadores que estan activos en el web por Base de Datos
			self.cursor.execute("""SELECT        sSMS_TramasPorProcesar.cliente, sSMS_Clientes.nombre_cliente
FROM            sSMS_TramasPorProcesar INNER JOIN
						 sSMS_Clientes ON sSMS_TramasPorProcesar.cliente = sSMS_Clientes.id_cliente INNER JOIN
						 sSMS_Eventos ON sSMS_TramasPorProcesar.evento = sSMS_Eventos.cod_event
WHERE        (sSMS_TramasPorProcesar.IdOperador = ?) group by sSMS_TramasPorProcesar.cliente,  sSMS_Clientes.nombre_cliente""",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'MapaMonitoreo':   
			self.cursor.execute("""SELECT c.id_cliente, c.nombre_cliente, c.direccion, c.referencia, c.telf_local, c.latitud, c.longitud, c.imagen AS imagencliente, c.id_type_cliente, t.img AS icono, 
					  sSMS_StatusPanelCliente.cod_alarm AS CodigoEstatusPanel, sSMS_StatusPanelCliente.Fecha AS FechaEstatusPanel, sSMS_Eventos.cod_event, 
					  sSMS_Eventos.descript AS DescripcionEvento, CASE WHEN sSMS_Eventos.type_evento = 0 THEN CASE WHEN sSMS_Usuarios.nombre IS NULL 
					  THEN 'Usuario ' + CAST(sSMS_TramasUltimaSignal.user_zone AS varchar(6)) 
					  ELSE sSMS_Usuarios.nombre + ' ' + sSMS_Usuarios.apellido END WHEN sSMS_Eventos.type_evento = 1 THEN CASE WHEN sSMS_ClienteZonas.descrip IS NULL 
					  THEN 'Zona ' + CAST(sSMS_TramasUltimaSignal.user_zone AS varchar(6)) 
					  ELSE sSMS_ClienteZonas.descrip END WHEN sSMS_Eventos.type_evento = 2 THEN '' END AS UserZona, 
					  sSMS_TramasUltimaSignal.fecha AS FechaUltimaSenal
FROM         sSMS_Usuarios RIGHT OUTER JOIN
					  sSMS_TramasUltimaSignal LEFT OUTER JOIN
					  sSMS_Eventos ON sSMS_TramasUltimaSignal.protocolo = sSMS_Eventos.id_protocolo AND 
					  sSMS_TramasUltimaSignal.evento = sSMS_Eventos.cod_event LEFT OUTER JOIN
					  sSMS_ClienteZonas ON sSMS_TramasUltimaSignal.user_zone = sSMS_ClienteZonas.id_zona AND 
					  sSMS_TramasUltimaSignal.cliente = sSMS_ClienteZonas.id_cliente ON sSMS_Usuarios.id_user = sSMS_TramasUltimaSignal.user_zone AND 
					  sSMS_Usuarios.id_cliente = sSMS_TramasUltimaSignal.cliente RIGHT OUTER JOIN
					  sSMS_Clientes AS c LEFT OUTER JOIN
					  sSMS_TypeCliente AS t ON c.id_type_cliente = t.id_type_empresa ON sSMS_TramasUltimaSignal.cliente = c.id_cliente LEFT OUTER JOIN
					  sSMS_StatusPanelCliente ON c.id_cliente = sSMS_StatusPanelCliente.idCliente
WHERE     (c.latitud <> 0) AND (c.latitud <> 0)""")
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SeleccionarPlanesNotificaciones':
			self.cursor.execute("""SELECT sSMS_Planes.id_plan, sSMS_Planes.descrip, sSMS_Planes.id_protocolo, sSMS_Protocolos.descrip AS nombreprotocolo
FROM  sSMS_Planes INNER JOIN sSMS_Protocolos ON sSMS_Planes.id_protocolo = sSMS_Protocolos.id_protocolo""")
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'EventosPorProtocolo':
			self.cursor.execute("SELECT cod_event, descript, web_color FROM sSMS_Eventos WHERE id_protocolo = ?",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'EventosPorPlan':
			self.cursor.execute("SELECT cod_evento FROM sSMS_EventosPlanes WHERE id_plan = ?",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SeleccionarEventos':
			self.cursor.execute("""SELECT sSMS_Eventos.cod_event, sSMS_Eventos.id_protocolo, sSMS_Eventos.descript, sSMS_Eventos.mensaje, sSMS_Eventos.type_evento, sSMS_Eventos.monitorea, 
 sSMS_Eventos.cod_alarm, sSMS_Eventos.orden, sSMS_Eventos.sonido, sSMS_Eventos.prioridad, sSMS_Eventos.web_color, sSMS_Eventos.web_colorBg, sSMS_Protocolos.descrip AS nombreprotocolo
FROM  sSMS_Eventos INNER JOIN sSMS_Protocolos ON sSMS_Eventos.id_protocolo = sSMS_Protocolos.id_protocolo""")
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'CodigosAlarma':
			self.cursor.execute("""SELECT codigo,descript,web_color,web_colorBg,grupo,idgrupo,prioridad FROM sSMS_CodigosAlarma""")
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SeleccionarVariables':
			self.cursor.execute("""SELECT descrip FROM sSMS_Variables""")
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SeleccionarEvento':
			self.cursor.execute("SELECT cod_event, id_protocolo FROM sSMS_Eventos WHERE cod_event = ? and id_protocolo = ?",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'GruposCodigosAlarma':
			self.cursor.execute("SELECT [idGrupo],[Descript],[webColor] FROM sSMS_GrupoCodigosAlarma")
			self.resultado = self.cursor.fetchall()			

		elif nombrequery == 'SeleccionarCodigoAlarma':
			self.cursor.execute("SELECT codigo  FROM sSMS_CodigosAlarma WHERE codigo = ?",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SeleccionarPermisologias':
			self.cursor.execute(" SELECT p.*, a.idAccion, a.descripcion FROM sSMS_PaginasAdmin p INNER   JOIN sSMS_PaginasAcciones a ON p.idPagina = a.idPagina  ORDER BY p.orden,p.idPagina,a.orden, p.nombre ",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SeleccionarPersonal':
			self.cursor.execute("SELECT p.idPersonal, e.nombre as Empresa, t.color, t.descripcion, p.id_empresa, p.idTipoUsuario,p.imagen,p.id_perfil,p.cedula, p.nombre , p.telefono, p.correo, p.Dirreccion, p.Telf_Habitacion, p.usuario, p.clave,p.estatus FROM sSMS_TiposUsuarios t INNER JOIN  sSMS_Personal p ON t.idtipoUsuario = p.idTipoUsuario INNER JOIN  sSMS_Empresas e ON p.id_empresa = e.id_empresa WHERE (p.eliminado = 0)",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SeleccionarTiposUsuarios':
			self.cursor.execute("SELECT t.*, e.nombre  FROM sSMS_TiposUsuarios t INNER JOIN sSMS_Empresas e ON t.idEmpresa = e.id_empresa  WHERE (t.eliminado = 0) ")
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SeleccionarPermisosUsuario':
			self.cursor.execute("SELECT idPagina,idAccion,idUsuario FROM sSMS_PermisosAdmin where idUsuario = ?",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SeleccionarPersonalUno':
			self.cursor.execute("SELECT  [idPersonal] FROM sSMS_Personal WHERE usuario = ? AND id_empresa = ?",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SeleccionarPerfilesUsuario':
			self.cursor.execute("SELECT * FROM sWEB_UsuariosPerfil where   (id_perfil NOT IN (3, 5))",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SeleccionarPermisosTipoUsuario':
			self.cursor.execute("SELECT * FROM sSMS_PermisosTipoUsuario where (idTipoUsuario=?)",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SeleccionarTipoUsuarioUno':
			self.cursor.execute("SELECT idtipoUsuario FROM sSMS_TiposUsuarios WHERE idEmpresa = ? AND id_perfilUsuario = ? AND color = ? AND descripcion = ? ",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SeleccionarPermisosPorTipoUsuario':
			self.cursor.execute("SELECT [idAccion] FROM sSMS_PermisosTipoUsuario WHERE idTipoUsuario = ?",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SeleccionarEmpresas':
			self.cursor.execute("SELECT * FROM sSMS_Empresas where id_empresa>0",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SeleccionarEmpresaUna':
			self.cursor.execute("SELECT  [id_empresa]  FROM [sSMS_Empresas] WHERE nombre = ?",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SeleccionarParentesco':
			self.cursor.execute("SELECT id_type_user, descrip FROM sSMS_TypeUser t order by id_type_user asc",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SeleccionarParentescoUno':
			self.cursor.execute("SELECT id_type_user, descrip FROM sSMS_TypeUser WHERE descrip = ?",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SeleccionarMensajesPredefinidos':  #Resoluciones
			self.cursor.execute("SELECT * FROM  sSMS_MensajesCierre",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SeleccionarResolucionUna':  #Resoluciones
			self.cursor.execute("SELECT * FROM  sSMS_MensajesCierre WHERE Mensaje = ?",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SeleccionarReceptoresConfigPort':  
			self.cursor.execute("SELECT [PortID],[Descrip],[Config],[type],[Server],[Port],[idReceptor],[Heartbeat],[orden],[Status],[geta],[fechaCreator],[idReceiver],[prefijo] FROM [sSMS_ConfigPortII]",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SeleccionarReceptores':  
			self.cursor.execute("SELECT idReceptor,str_receptor,serial,tcpip FROM sSMS_Receptores",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SeleccionarReceptoresConfigPortUno':  
			self.cursor.execute("SELECT PortID FROM sSMS_ConfigPortII where PortID = ?",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SeleccionarMotivosSoporte':  
			self.cursor.execute("SELECT s.*, d.nombre  FROM sSMS_SoporteMotivos s INNER JOIN sSMS_DepartamentosEmpresa d ON s.idDepartCorreo = d.idDepartamento where s.idEmpresa = ? ",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SeleccionarMotivosSoporteUno':  
			self.cursor.execute("SELECT s.*, d.nombre  FROM sSMS_SoporteMotivos s INNER JOIN sSMS_DepartamentosEmpresa d ON s.idDepartCorreo = d.idDepartamento where s.idEmpresa = ? and s.descripcion = ? ",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'LogSenalesMonitoreoAlertas':  
			self.cursor.execute("""SELECT  TOP (100) sSMS_Protocolos.descrip AS protocolo, CONVERT(varchar(10),T.cliente) +'-'+ C.nombre_cliente AS nombrecliente, E.cod_event +'-'+ E.descript AS StrEvento, CASE WHEN E.type_evento = 0 THEN CASE WHEN U.nombre IS NULL 
                         THEN 'Usuario ' + CAST(T .user_zone AS varchar(3)) ELSE U.nombre + ' ' + U.apellido END WHEN E.type_evento = 1 THEN CASE WHEN Z.descrip IS NULL THEN 'Zona ' + CAST(T .user_zone AS varchar(3)) 
                         ELSE Z.descrip END WHEN E.type_evento = 2 THEN '' END AS UserZona, T.Linea, T.fecha, E.web_color
FROM            sSMS_Personal AS p RIGHT OUTER JOIN
                         sSMS_Eventos AS E INNER JOIN
                         sSMS_Tramas AS T ON E.cod_event = T.evento AND E.id_protocolo = T.protocolo INNER JOIN
                         sSMS_Protocolos ON T.protocolo = sSMS_Protocolos.id_protocolo ON p.idPersonal = T.IdOperador LEFT OUTER JOIN
                         sSMS_Usuarios AS U ON T.cliente = U.id_cliente AND T.user_zone = U.cod_user LEFT OUTER JOIN
                         sSMS_ClienteZonas AS Z ON T.cliente = Z.id_cliente AND T.user_zone = Z.id_zona LEFT OUTER JOIN
                         sSMS_Clientes AS C ON T.cliente = C.id_cliente
ORDER BY T.id_trama DESC """,datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SeleccionarMensajesCola':
			self.cursor.execute("""SELECT TOP 200 CONVERT(varchar(10), sSMS_Clientes.id_cliente)+'-'+ sSMS_Clientes.nombre_cliente AS nombrecliente, sSMS_BsalidaSpeed.movil, sSMS_BsalidaSpeed.sms AS mensaje , sSMS_BsalidaSpeed.fecha_creada AS fecha
FROM sSMS_BsalidaSpeed LEFT OUTER JOIN sSMS_Clientes ON sSMS_BsalidaSpeed.id_cliente = sSMS_Clientes.id_cliente WHERE sSMS_BsalidaSpeed.status = 0 order by sSMS_BsalidaSpeed.id_salida desc""",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SeleccionarMensajesEnviado':
			self.cursor.execute("""SELECT TOP 20 CONVERT(varchar(10), sSMS_Clientes.id_cliente)+'-'+ sSMS_Clientes.nombre_cliente AS nombrecliente, sSMS_BsalidaSpeed.movil, sSMS_BsalidaSpeed.sms AS mensaje , sSMS_BsalidaSpeed.fecha_creada AS fecha
FROM sSMS_BsalidaSpeed LEFT OUTER JOIN sSMS_Clientes ON sSMS_BsalidaSpeed.id_cliente = sSMS_Clientes.id_cliente WHERE sSMS_BsalidaSpeed.status = 0 order by sSMS_BsalidaSpeed.id_salida desc""",datos)
			self.resultado = self.cursor.fetchall()

		elif nombrequery == 'SeleccionarMensajesRecibidos':
			self.cursor.execute("""SELECT TOP 50  movil,sms,fecha  FROM sSMS_Bentrada ORDER BY fecha desc""",datos)
			self.resultado = self.cursor.fetchall()


		######################################## INSERT ###############################################
	
		elif nombrequery == 'InsertarNotaFijaCliente':
			self.cursor.execute("INSERT INTO sSMS_ClienteZonas (id_zona, descrip, ubicacion, id_cliente) VALUES (?,?,?,?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'InsertarNotaFijaCliente':
			self.cursor.execute("INSERT INTO sSMS_NotasClientes (IdCliente, NotaFija)   VALUES(?,?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'InsertarNotaTemporalCliente':
			self.cursor.execute("INSERT INTO sSMS_NotasClientes (IdCliente, NotaTemp, FechaIni, FechaFin)   VALUES(?,?,?,?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'InsertarGrupoClientes': #### INSERTAR ASOCIADO ####
			self.cursor.execute("INSERT INTO smsalarmas_asociados (id_empresa, nombre, direccion, telef_contacto, email, usuario, clave, status) VALUES (?,?,?,?,?,?,?,?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'InsertarAbonadosGrupo':  ##### INSERTAR ABONADOS A ASOCIADOS ####
			self.cursor.execute("INSERT INTO smsalarmas_asociados_abonados (id_asociado, id_empresa, id_cliente) VALUES (?,?,?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'InsertarAbonado':  ##### INSERTAR ABONADOS ####
			self.cursor.execute("INSERT INTO sSMS_Clientes (alarma, nombre_cliente, ciudad, direccion, referencia, telf_local, web_site, email, telf_movil, id_type_cliente, id_status,  monto, status_web, status, id_protocolo, id_empresa,id_cliente, telf_fax,clavemaster,rif,fechinicio,latitud,longitud,id_estado,status_monitoreo,status_mail) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'InsertarUsuario': 
			self.cursor.execute("INSERT INTO sSMS_Usuarios (id_user, id_cliente, cod_user, id_type_user, nombre , apellido, movil, email, FechaAniversario, status, send_mail, frecuencia_mail, bbpin,clavevoz,active_email,id_plan,id_plan_email,maximosms) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'InsertarContactoEmergencia':  
			self.cursor.execute("INSERT INTO sSMS_NumEmergencia (nombre,numero, descript,observacion,id_cliente)   VALUES(?,?,?,?,?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'InsertarEventosUsuario':  
			self.cursor.execute("INSERT INTO sSMS_ClienteEventos (id_cliente, cod_evento, id_user, status, variante, type)   SELECT  id_cliente=?, cod_evento, id_user=?, 1, variante, type=?  FROM sSMS_EventosPlanes where id_plan = ?",datos)
			self.cnxn.commit()
		
		elif nombrequery == 'InsertarHorarioCliente':  
			self.cursor.execute("INSERT INTO sSMS_HorariosOC (id_cliente,diaapertura,horaapertura,toleranciaapertura,diacierre,horacierre,toleranciacierre) VALUES (?,?,?,?,?,?,?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'InsertarTipoCliente':  
			self.cursor.execute("INSERT INTO  sSMS_TypeCliente  (id_type_empresa, descrip,monto,img) VALUES (?,?,CAST(? AS MONEY),?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'InsertarDepartamento':  
			self.cursor.execute("INSERT INTO sSMS_DepartamentosEmpresa (idEmpresa, nombre, correo) VALUES (?,?,?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'InsertarTipoAlarma':  
			self.cursor.execute("INSERT INTO  sSMS_TypeAlarma (Descrip) VALUES (?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'InsertarOperadorSession':  
			self.cursor.execute("INSERT INTO sSMS_OperadorSession (IdSession, IdOperador, FechaPIN, Ip, StatusLogin, StatusMonitoreo, FechaDesocupado) Values (?,?,GETDATE(),?,?,?,GETDATE())",datos)
			self.cnxn.commit()

		elif nombrequery == 'InsertarObservacionTrama':  
			self.cursor.execute("INSERT INTO sSMS_TramasObservaciones (idtrama, fecha, observacion, idoperador) values (?,GETDATE(),?,?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'InsertarTramaProcesada':  
			self.cursor.execute("INSERT INTO sSMS_TramasProcesadas (id_trama,descrip, cliente, status, evento, protocolo, user_zone, fecha, Variante, Linea,observacion,IdOperador,EmpresaMonitorea) SELECT id_trama,descrip, cliente,status, evento,  protocolo, user_zone, fecha, Variante, Linea,?, ?,EmpresaMonitorea FROM sSMS_Tramas WHERE  id_trama = ?",datos)
			self.cnxn.commit()

		elif nombrequery == 'InsertarPlanNotificaciones':  
			self.cursor.execute("INSERT INTO sSMS_Planes (descrip,id_protocolo) VALUES(?, ?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'InsertarEventosPlan':  
			self.cursor.execute("INSERT INTO sSMS_EventosPlanes (cod_evento,id_plan,id_protocolo) VALUES(?,?,?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'InsertarEvento':  
			self.cursor.execute("INSERT INTO sSMS_Eventos (cod_event,id_protocolo,descript,mensaje,type_evento,monitorea,cod_alarm,prioridad,web_color) VALUES(?,?,?,?,?,?,?,?,?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'InsertarCodigoAlarma':  
			self.cursor.execute("INSERT INTO sSMS_CodigosAlarma (codigo,descript,prioridad,grupo,idGrupo,web_color,color) VALUES(?,?,?,?,?,?,'1')",datos)
			self.cnxn.commit()

		elif nombrequery == 'InsertarUsuarioPersonal':  
			self.cursor.execute("INSERT INTO sSMS_Personal (id_empresa, idTipoUsuario, cedula, nombre, telefono, correo, Dirreccion, Telf_Habitacion, usuario, clave,eliminado,estatus,id_perfil) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'InsertarPermisosPersonal':
			parentesis = len(datos)-2 
			Query = "INSERT INTO sSMS_PermisosAdmin SELECT p.idPagina, a.idAccion,?  FROM sSMS_PaginasAdmin p INNER JOIN  sSMS_PaginasAcciones a ON p.idPagina = a.idPagina WHERE  (a.idAccion IN ("
			par = '?'
			for i in range(parentesis):
				par = par + ',?'
			Query = Query + par + '))'
			self.cursor.execute(Query,datos)
			self.cnxn.commit()

		elif nombrequery == 'InsertarPermisosTipoUsuario':
			parentesis = len(datos)-2 
			Query = "INSERT INTO sSMS_PermisosTipoUsuario SELECT p.idPagina, a.idAccion, ?    FROM sSMS_PaginasAdmin p INNER JOIN  sSMS_PaginasAcciones a ON p.idPagina = a.idPagina WHERE   (a.idAccion IN ("
			par = '?'
			for i in range(parentesis):
				par = par + ',?'
			Query = Query + par + '))'
			self.cursor.execute(Query,datos)
			self.cnxn.commit()

		elif nombrequery == 'InsertarTipoUsuario':
			self.cursor.execute("INSERT INTO sSMS_TiposUsuarios (idEmpresa, color, descripcion, eliminado,id_perfilUsuario) VALUES (?,?,?,?,?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'InsertarEmpresa':
			self.cursor.execute("INSERT INTO sSMS_Empresas (id_pais, nombre, direccion, telefonos, email, web, login, clave, status, rif, ip, puerto, master,latitud, longuitud,timeAlertPen, timeHombreM, timeNotifiHombre, correosHombre)VALUES (1,?,?,?,?,?,?,?,?,?,0,0,0,?,?,?,?,?,?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'InsertarParentesco':
			self.cursor.execute("INSERT INTO sSMS_TypeUser (descrip) VALUES (?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'InsertarMensajePredefinido':
			self.cursor.execute("INSERT INTO sSMS_MensajesCierre (Mensaje) VALUES (?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'InsertarReceptorConfigPort':
			self.cursor.execute("INSERT INTO sSMS_ConfigPortII (PortID, Descrip, Config, type, Server, Port, idReceptor, Heartbeat, Status, geta,idReceiver,orden, fechaCreator,prefijo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1,?,1, GETDATE(),?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'InsertarSoporteMotivos':
			self.cursor.execute("INSERT INTO  sSMS_SoporteMotivos ( idEmpresa, descripcion, idDepartCorreo) VALUES (?,?,?)",datos)
			self.cnxn.commit()


		#################################################### UPDATE ############################################################

		elif nombrequery == 'ActualizarNotaFijaCliente':
			self.cursor.execute("UPDATE sSMS_NotasClientes SET NotaFija =? where IdCliente = ?",datos)
			self.cnxn.commit()

		elif nombrequery == 'ActualizarNotaTemporalCliente':
			self.cursor.execute("UPDATE sSMS_NotasClientes SET NotaTemp =?, FechaIni = ?, FechaFin= ? where IdCliente = ?",datos)
			self.cnxn.commit()

		elif nombrequery == 'ActualizarZonaCliente':
			self.cursor.execute("UPDATE sSMS_ClienteZonas SET descrip =? , ubicacion =?, id_zona=? WHERE id_zona =? and id_cliente =? ",datos)
			self.cnxn.commit()
		
		elif nombrequery == 'ActualizarUsuariosCliente':
			self.cursor.execute("UPDATE sSMS_Usuarios SET id_user=?, cod_user=?, id_type_user =?, nombre =?, apellido =?, movil =?, email =?, FechaAniversario =?, status =?, send_mail =?, frecuencia_mail =?, bbpin =?, clavevoz =? , active_email=? ,maximosms= ? WHERE (id_user =?) AND (id_cliente =?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'ActualizarContactoCliente':
			self.cursor.execute("UPDATE sSMS_NumEmergencia SET nombre =?, descript =? ,numero =?, observacion=? where (numero=?) AND (id_cliente =?) ",datos)
			self.cnxn.commit()

		elif nombrequery == 'ActualizarPlanSMS':
			self.cursor.execute("UPDATE sSMS_Usuarios SET id_plan = ?  where id_user=? AND id_cliente=?",datos)
			self.cnxn.commit()

		elif nombrequery == 'ActualizarPlanEmail':
			self.cursor.execute("UPDATE sSMS_Usuarios SET id_plan_email = ?  where id_user=? AND id_cliente=?",datos)
			self.cnxn.commit()

		elif nombrequery == 'ActualizarHorario':
			self.cursor.execute("UPDATE sSMS_HorariosOC SET diaapertura =?, horaapertura =?,toleranciaapertura =?,diacierre =?, horacierre =?, toleranciacierre =? WHERE (Id = ?) ",datos)
			self.cnxn.commit()

		elif nombrequery == 'ActualizarTipoCliente':
			self.cursor.execute("UPDATE  sSMS_TypeCliente SET id_type_empresa = ?,descrip=?,monto=CAST(? AS MONEY) , img=? WHERE id_type_empresa = ?",datos)
			self.cnxn.commit()

		elif nombrequery == 'ActualizarDepartamento':
			self.cursor.execute("UPDATE sSMS_DepartamentosEmpresa SET nombre =?, correo =? WHERE (idDepartamento =?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'ActualizarLatitudLongitud':
			self.cursor.execute("UPDATE sSMS_Clientes SET latitud =?, longitud =? WHERE (id_cliente =?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'ActualizarHeartBeatOperador':
			self.cursor.execute(" UPDATE sSMS_OperadorSession SET FechaPIN=GETDATE(), Ip=?, StatusLogin=1, StatusMonitoreo = ? WHERE IdOperador = ?",datos)
			self.cnxn.commit()

		elif nombrequery == 'ActualizarFechaDesocupado':
			self.cursor.execute(" UPDATE sSMS_OperadorSession SET FechaPIN = GETDATE(), StatusLogin=1, StatusMonitoreo = 1, FechaDesocupado = GETDATE() WHERE IdOperador = ?",datos)
			self.cnxn.commit()

		elif nombrequery == 'ActualizarTramaPendiente':
			self.cursor.execute("UPDATE sSMS_TramasPorProcesar SET status =4 where id_trama = ?",datos)
			self.cnxn.commit()

		elif nombrequery == 'ActualizarPlanNotificaciones':
			self.cursor.execute("UPDATE sSMS_Planes SET descrip =?, id_protocolo =? where id_plan = ?",datos)
			self.cnxn.commit()

		elif nombrequery == 'ActualizarEvento':
			self.cursor.execute("UPDATE sSMS_Eventos SET cod_event =?, id_protocolo =?, descript = ?, mensaje = ?, type_evento = ?, monitorea = ?, cod_alarm = ?, prioridad = ?, web_color = ? where cod_event =? and id_protocolo =?",datos)
			self.cnxn.commit()

		elif nombrequery == 'ActualizarCodigoAlarma':
			self.cursor.execute("UPDATE sSMS_CodigosAlarma SET codigo =?, descript =?, prioridad = ?, grupo = ?, idGrupo = ?, web_color = ? where codigo =?",datos)
			self.cnxn.commit()

		elif nombrequery == 'EliminarUsuarioPersonal':
			self.cursor.execute("UPDATE sSMS_Personal SET eliminado =1 where (idPersonal=?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'ActualizarUsuarioPersonal':
			self.cursor.execute("UPDATE sSMS_Personal SET id_empresa =?,idTipoUsuario =?,cedula =?, nombre =?, telefono =?, correo =?, Dirreccion =?, Telf_Habitacion =? ,id_perfil=? where idPersonal=?",datos)
			self.cnxn.commit()

		elif nombrequery == 'ActualizarClaveUsuarioPersonal':
			self.cursor.execute("UPDATE sSMS_Personal SET clave =? where idPersonal=?",datos)
			self.cnxn.commit()

		elif nombrequery == 'ActualizarTipoUsuario':
			self.cursor.execute("UPDATE sSMS_TiposUsuarios SET color =?, descripcion =?, id_perfilUsuario =?, idEmpresa = ? where idtipoUsuario=?",datos)
			self.cnxn.commit()

		elif nombrequery == 'ActualizarEmpresa':
			self.cursor.execute(" UPDATE sSMS_Empresas SET nombre =?, direccion =?, telefonos =?, email =?, web =?,  rif =? , latitud =?, longuitud =?,timeAlertPen =?, timeHombreM =?, timeNotifiHombre =?, correosHombre =?, monitorea =  ?  WHERE (id_empresa =?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'ActualizarEmpresaEmpresaMonitorea':
			self.cursor.execute(" UPDATE sSMS_Empresas SET monitorea = ?  WHERE (id_empresa =?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'ActualizarClaveEmpresa':
			self.cursor.execute(" UPDATE sSMS_Empresas SET clave = ? WHERE (id_empresa =?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'ActualizarParentesco':
			self.cursor.execute("UPDATE sSMS_TypeUser SET descrip =? WHERE (id_type_user = ?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'ActualizarMensajesPredefinidos': #Resoluciones
			self.cursor.execute("UPDATE  sSMS_MensajesCierre SET Mensaje =? WHERE (id = ?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'ActualizarReceptorConfigPort': 
			self.cursor.execute("UPDATE sSMS_ConfigPortII SET Descrip =?, Config =?, type =?, Server =?, Port =?, idReceptor =?, Heartbeat =?, geta =?, Status =?, idReceiver =?, prefijo = ? WHERE (PortID = ?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'ActualizarMotivoSoporte': 
			self.cursor.execute("UPDATE sSMS_SoporteMotivos SET idEmpresa = ? descripcion = ?, idDepartCorreo= ? WHERE (id_motivo = ?)",datos)
			self.cnxn.commit()			

		################################################### DELETE #########################################################
	
		elif nombrequery == 'BorrarAbonadosGrupo':
			self.cursor.execute("DELETE FROM smsalarmas_asociados_abonados WHERE (id_asociado = ?) AND (id_empresa = ?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'BorrarEventosUsuario':
			self.cursor.execute("DELETE FROM sSMS_ClienteEventos WHERE (id_cliente=?) and (id_user=?) and (type=?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'BorrarZona':
			self.cursor.execute(" DELETE FROM sSMS_ClienteZonas WHERE (id_zona = ?) AND (id_cliente = ?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'BorrarUsuario':
			self.cursor.execute("DELETE FROM sSMS_Usuarios WHERE (id_user = ?) AND (id_cliente = ?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'BorrarHorario':
			self.cursor.execute("DELETE FROM sSMS_HorariosOC WHERE   (Id = ?) ",datos)
			self.cnxn.commit()

		elif nombrequery == 'BorrarContacto':
			self.cursor.execute("DELETE FROM sSMS_NumEmergencia WHERE ( id_numero = ?) AND (id_cliente = ?) ",datos)
			self.cnxn.commit()

		elif nombrequery == 'BorrarPlanNotificaciones':
			self.cursor.execute("DELETE FROM sSMS_Planes WHERE (id_plan = ?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'BorrarEventosPlanesNotificaciones':
			self.cursor.execute("DELETE FROM sSMS_EventosPlanes WHERE (id_plan = ?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'BorrarEvento':
			self.cursor.execute("DELETE FROM sSMS_Eventos WHERE (cod_event = ?) AND (id_protocolo = ?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'BorrarCodigoAlarma':
			self.cursor.execute("DELETE FROM [sSMS_CodigosAlarma] WHERE (codigo = ?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'BorrarPermisosUsuarioPersonal':
			self.cursor.execute("DELETE FROM sSMS_PermisosAdmin WHERE (idUsuario =?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'BorrarTipoUsuario':
			self.cursor.execute("UPDATE sSMS_TiposUsuarios SET eliminado =1 WHERE (idtipoUsuario = ?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'BorrarPermisosTipoUsuario':
			self.cursor.execute(" DELETE FROM sSMS_PermisosTipoUsuario WHERE (idTipoUsuario = ?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'BorrarEmpresa':
			self.cursor.execute("DELETE FROM sSMS_Empresas WHERE (id_empresa = ?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'BorrarParentesco':
			self.cursor.execute("DELETE FROM  sSMS_TypeUser WHERE (id_type_user = ?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'BorrarMensajePredefinido': #Resoluciones
			self.cursor.execute(" DELETE FROM sSMS_MensajesCierre WHERE (id = ?)",datos)
			self.cnxn.commit()

		elif nombrequery == 'BorrarReceptor': 
			self.cursor.execute("DELETE FROM sSMS_ConfigPortII WHERE PortID = ?",datos)
			self.cnxn.commit()

		elif nombrequery == 'BorrarMotivoSoporte': 
			self.cursor.execute("DELETE FROM sSMS_SoporteMotivos WHERE (id_motivo = ?)",datos)
			self.cnxn.commit()


  
	

		print 'Listo'

		return self.resultado
	def Seleccionar(self,query):
		self.cursor.execute(query)
		rows = self.cursor.fetchall()
		self.resultado = rows
		return self.resultado
	def SeleccionarUno(self,query,dato):
		self.cursor.execute(query,dato)
		row = self.cursor.fetchone()
		self.resultado = row
		return self.resultado
	def Insertar(self,query,datos):
		self.cursor.execute(query,datos)
		self.cnxn.commit()
	def Actualizar(self,query,*datos):
		self.cursor.execute(query,datos)
		self.cnxn.commit()
	def Borrar(self,query,dato):
		self.cursor.execute(query,dato)
		self.cnxn.commit()


