from pathlib import Path
import xml.etree.ElementTree as E,copy,json,zipfile
R=Path(__file__).resolve().parents[1];out=R/'docs/formal/comunicacion-corregida-v5';out.mkdir(exist_ok=True)
s=R/'scripts/build-puds-drawio.py';ctx={'__file__':str(s)};exec(compile(s.read_text(encoding='utf8').split('master=ET.Element')[0],str(s),'exec'),ctx)
Page=ctx['Page']
DATA=[
('consulta-ia-grupal','Consultar a la IA grupal','Chat del proyecto','Consulta IA','Proyecto y membresía','Conversación IA','Proveedor IA',['1. consultar(pregunta)'],['1.1 enviarConsulta()'],['1.2 verificarAcceso()','1.3 recuperarContexto()'],['1.4 solicitarRespuesta()'],['1.5 devolverRespuesta()'],['1.6 registrarIntercambio()'],['1.7 difundirRespuesta()'], 'La consulta no modifica el UML. Si falla el proveedor, informar el error.'),
('revision-diagrama','Solicitar revisión del diagrama','Chat del proyecto','Revisión UML','Proyecto y documento','Revisión compartida','Proveedor IA',['1. solicitarRevision()'],['1.1 enviarSolicitud()'],['1.2 verificarAcceso()','1.3 obtenerSnapshot()'],['1.4 analizarModelo()'],['1.5 devolverHallazgos()'],['1.6 registrarRevision()'],['1.7 compartirHallazgos()'],'Los hallazgos son recomendaciones; no se aplican cambios automáticamente.'),
('resumen-avances','Resumir los avances','Chat del proyecto','Resumen de avances','Proyecto y actividad','Conversación IA','Proveedor IA',['1. pedirResumen()'],['1.1 solicitarResumen()'],['1.2 verificarAcceso()','1.3 recuperarContexto()'],['1.4 resumirContexto()'],['1.5 devolverResumen()'],['1.6 registrarResumen()'],['1.7 compartirResumen()'],'Resumir solo la información disponible, conservando autoría y límites de contexto.'),
('edicion-por-voz','Solicitar y confirmar edición por voz','Herramientas de voz','Edición por voz','Proyecto y documento','Actividad del proyecto','Whisper e IA',['1. grabarOrden()','2. confirmarPropuesta()'],['1.1 enviarAudio()','2.1 aplicar(baseRevision)'],['1.2 verificarAcceso()','1.3 recuperarDocumento()','2.2 validarRevision()'],['1.4 transcribirYPlanificar()'],['1.5 devolverPropuesta()'],['2.3 guardarCambio()','2.4 registrarActividad()'],['1.6 mostrarPropuesta()','2.5 compartirCambio()'],'Confirmación y revisión vigente obligatorias. Cancelar conserva el documento; propuesta de voz al solicitante.'),
('retomar-sesion','Retomar una sesión registrada','Proyecto','Continuidad de sesión','Proyecto y documento','Visitas y sesiones','Asistente grupal',['1. abrirProyecto()'],['1.1 solicitarEstado()'],['1.2 verificarAcceso()','1.3 recuperarDocumento()'],['2. [pide resumen] resumir()'],['2.1 entregarResumen()'],['1.4 recuperarVisitaAnterior()','1.5 registrarVisita()'],['1.6 mostrarEstadoYNovedades()'],'El resumen es opcional. No confundir el historial persistido con Undo/Redo de sesión.'),
('observacion-movil','Observar el proyecto desde el móvil','Vista móvil','Observación del proyecto','Documento vigente','Presencia y actividad','Colaboración en tiempo real',['1. observarProyecto()'],['1.1 conectarYLeer()','2.1 reconciliarEstado()'],['1.2 verificarAcceso()','1.3 recuperarDocumento()'],['1.4 suscribirCambios()'],['2. recibirCambioConfirmado()'],['1.5 consultarParticipantes()'],['1.6 mostrarEstado()','2.2 actualizarVista()'],'Vista informativa sin edición. Reconectar recupera el estado autoritativo; no es un rol VIEWER persistido.'),
('notificaciones-push','Activar y recibir avisos push','Panel de avisos / SW','Avisos push','Suscripción push','Aviso y trabajo push','Proveedor push',['1. activarAvisos()','3. abrirNotificacion()'],['1.1 registrarSuscripcion()','3.1 revalidarAcceso()'],['1.2 verificarCuenta()','1.3 guardarSuscripcion()'],['2.2 enviarCifrado()'],['2.3 aceptarORechazar()'],['2.1 reclamarTrabajo()','2.4 registrarResultado()'],['1.4 confirmarSuscripcion()','3.2 abrirProyecto()'],'Flujo 2 ejecutado por el trabajador al existir un cambio ajeno. HTTPS, permiso y VAPID requeridos; aceptación del proveedor no prueba recepción visible.')]
master=E.Element('mxfile',host='Electron',type='device');manifest=[]
def bce(p,x,y,kind,name):
 c=p.box(x,y,48,48,'','ellipse;strokeColor=#222222;fillColor=#FFFFFF;')
 if kind=='Vista':
  p.line(x-12,y-3,x-12,y+51,'','endArrow=none;');p.line(x-12,y+24,x,y+24,'','endArrow=none;')
 elif kind=='CTRL':p.line(x+32,y-5,x+8,y-5,'','endArrow=open;')
 else:p.line(x,y+52,x+48,y+52,'','endArrow=none;')
 p.text(x-70,y+63,188,48,kind+'\n'+name,13)
 return c
for i,d in enumerate(DATA):
 slug,title,ui,ctrl,e1,e2,ext,ua,uc,ce,cx,xr,ce2,ret,note=d;code=f'D{i+7:03d}';cu=f'CU-SP-{i+1:02d}'
 p=Page(i+7,title,'',1200,720)
 # Remove inherited titles and footer; keep one clear title above the model.
 for cell in list(p.root):
  if cell.get('vertex')=='1':p.root.remove(cell)
 p.text(30,20,1140,32,code+' · Comunicación · '+title,20,True)
 actor=p.actor(35,355,'Integrante móvil' if i==5 else 'Integrante')
 u=bce(p,250,350,'Vista',ui);c=bce(p,590,350,'CTRL',ctrl)
 a=bce(p,1015,155,'CE',e1);b=bce(p,1015,485,'CE',e2)
 x=p.box(360,105,225,54,'«servicio externo»\n'+ext,'fillColor=#FFFFFF;')
 for source,target in [(actor,u),(u,c),(c,a),(c,b),(c,x)]:p.edge(source,target,'','edgeStyle=none;endArrow=none;strokeColor=#555555;')
 def msg(x1,y1,x2,y2,lines,above=True):
  p.line(x1,y1,x2,y2,'','endArrow=block;endFill=1;strokeColor=#222222;')
  h=18*len(lines)+6;p.text((x1-240 if y2<y1 else x1+15) if x1==x2 else min(x1,x2),y1-h-5 if above else y1+5,max(220,abs(x2-x1)+20),h,'\n'.join(lines),12)
 msg(95,325,230,325,ua)
 msg(330,325,565,325,uc)
 msg(560,470,330,470,ret,False)
 msg(740,185,985,185,ce)
 msg(985,275,755,275,['retorno: datos autorizados'],True)
 msg(720,515,985,515,ce2)
 msg(900,580,720,580,['2.4.1 confirmarRegistro()' if i in [3,6] else '1.6.1 confirmarRegistro()'],False)
 msg(400,205,400,165,cx)
 msg(560,165,560,225,xr,False)
 p.text(35,650,1130,45,cu+' · '+note,12)
 p.diagram.set('id',code);p.diagram.set('name',code+' - '+title)
 name=code+'-comunicacion-'+slug+'.drawio'
 single=E.Element('mxfile',host='Electron',type='device');single.append(copy.deepcopy(p.diagram));E.indent(single);E.ElementTree(single).write(out/name,encoding='utf8',xml_declaration=True)
 master.append(copy.deepcopy(p.diagram));manifest.append({'codigo_archivo':code,'codigo_documento':f'D{i+7:02d}','caso':cu,'archivo':name,'titulo':title})
E.indent(master);E.ElementTree(master).write(out/'00-SinapUML-Comunicacion-D007-D013.drawio',encoding='utf8',xml_declaration=True)
(out/'LEEME.md').write_text('# Comunicación D007–D013\n\nAbrir 00-SinapUML-Comunicacion-D007-D013.drawio para revisar los siete diagramas. Cada archivo individual contiene solo su caso y puede abrirse o importarse en draw.io. Las pestañas llevan código y título. D007 corresponde a D07 del Word, hasta D013/D13.\n\nDistribución: actor → vista → control → entidades. Las líneas sin flecha son enlaces; las flechas separadas representan mensajes numerados. CE significa entidad de análisis y CTRL control conceptual, no necesariamente una clase implementada. Proveedores externos se distinguen de entidades. No se modificó el Word ni las fuentes anteriores. Revisión con el estudiante pendiente.\n',encoding='utf8')
(out/'correspondencia.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
print(out)
