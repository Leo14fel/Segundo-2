"""Diagrams authored as native editable mxGraph cells; no rasterized diagram content.
Run from any directory: python scripts/build-puds-drawio.py
"""
from pathlib import Path
import csv, copy, html, json, heapq, re, xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/formal/diagramas-drawio'
OUT.mkdir(parents=True, exist_ok=True)
INK='#243746'; TEAL='#147D78'; BLUE='#EAF1F7'; MINT='#EDF7F4'; GRAY='#F4F5F6'; AMBER='#FFF5DE'
BASE=f'html=1;whiteSpace=wrap;fontFamily=Arial;fontSize=14;fontColor={INK};strokeColor=#657581;strokeWidth=1.3;'
PAGES=[]
META=list(csv.DictReader((ROOT/'docs/formal/diagramas-xml-planificados.csv').open(encoding='utf-8-sig')))

def label(text):
    return html.escape(text).replace('\n','<br>')

class Page:
    def __init__(self, n, title, subtitle, w=1200, h=800):
        self.n=n; self.code=f'D{n:02}'; self.w=w; self.h=h; self.i=0
        self.diagram=ET.Element('diagram',id=self.code,name=f'{self.code} · {title}')
        self.model=ET.SubElement(self.diagram,'mxGraphModel',dx=str(w),dy=str(h),grid='1',gridSize='10',guides='1',tooltips='1',connect='1',arrows='1',fold='1',page='1',pageScale='1',pageWidth=str(w),pageHeight=str(h),math='0',shadow='0')
        self.root=ET.SubElement(self.model,'root');ET.SubElement(self.root,'mxCell',id='0');ET.SubElement(self.root,'mxCell',id='1',parent='0')
        self.text(30,20,w-60,35,f'{self.code}  /  {title}',24,True)
        self.text(30,62,w-60,35,subtitle,13,color='#526570')
        self.text(30,h-40,w-60,25,'SinapUML  ·  PUDS  ·  9 de noviembre de 2026  |  Modelo documental basado en la implementación local',11,color='#6A7881')
        PAGES.append(self)
    def id(self):self.i+=1;return f'{self.code}-{self.i}'
    def box(self,x,y,w,h,text='',style='',parent='1'):
        ident=self.id();c=ET.SubElement(self.root,'mxCell',id=ident,value=label(text),style=BASE+'fillColor=#FFFFFF;'+style,vertex='1',parent=parent)
        ET.SubElement(c,'mxGeometry',{'x':str(x),'y':str(y),'width':str(w),'height':str(h),'as':'geometry'})
        return ident
    def text(self,x,y,w,h,text,size=14,bold=False,color=INK,parent='1'):
        return self.box(x,y,w,h,text,f'text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacing=0;fontSize={size};fontStyle={1 if bold else 0};fontColor={color};',parent)
    def node(self,x,y,w,h,text,fill=BLUE,style=''):
        return self.box(x,y,w,h,text,f'rounded=0;fillColor={fill};spacing=8;'+style)
    def note(self,x,y,w,h,text):return self.box(x,y,w,h,text,'shape=note;size=16;fillColor='+AMBER+';spacing=10;align=left;fontSize=13;')
    def actor(self,x,y,text,above=False):return self.box(x,y,48,72,text,'shape=umlActor;labelWidth=160;verticalLabelPosition='+('top;verticalAlign=bottom;' if above else 'bottom;verticalAlign=top;')+'fillColor=#FFFFFF;fontSize=13;')
    def uc(self,x,y,w,text):return self.box(x,y,w,60,text,'ellipse;fillColor=#FFFFFF;spacing=8;fontSize=13;')
    def pkg(self,x,y,w,h,text):return self.box(x,y,w,h,text,'shape=folder;tabWidth=90;tabHeight=20;fillColor='+BLUE+';align=left;verticalAlign=top;spacingTop=28;spacingLeft=15;spacingRight=12;')
    def edge(self,a,b,text='',style='',pts=None,ends=None):
        ident=self.id();attrs={'id':ident,'value':label(text),'style':BASE+'whiteSpace=nowrap;edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=open;endFill=0;labelBackgroundColor=#FFFFFF;fontSize=12;'+style,'edge':'1','parent':'1'}
        if a:attrs['source']=a
        if b:attrs['target']=b
        c=ET.SubElement(self.root,'mxCell',attrs);g=ET.SubElement(c,'mxGeometry',{'relative':'1','as':'geometry'})
        if pts:
            ar=ET.SubElement(g,'Array',{'as':'points'})
            for x,y in pts:ET.SubElement(ar,'mxPoint',x=str(x),y=str(y))
        if ends:
            for key,(x,y) in zip(['sourcePoint','targetPoint'],ends):ET.SubElement(g,'mxPoint',{'x':str(x),'y':str(y),'as':key})
        return ident
    def line(self,x1,y1,x2,y2,text='',style=''):
        return self.edge(None,None,text,'edgeStyle=none;'+style,ends=[(x1,y1),(x2,y2)])
    def klass(self,x,y,w,name,attrs,h=None,fill=BLUE):
        hh=h or (52+23*len(attrs));ident=self.box(x,y,w,hh,name,f'swimlane;startSize=36;horizontal=1;fillColor={fill};swimlaneFillColor=#FFFFFF;align=center;fontStyle=1;')
        self.text(10,42,w-20,hh-48,'\n'.join(attrs),13,parent=ident)
        return ident
    def assoc(self,a,b,text='',composition=False,style=''):
        mult=re.match(r'^([0-9.*]+).* / ([0-9.*]+)',text)
        edge=self.edge(a,b,'' if mult else text,'endArrow=none;'+('startArrow=diamond;startFill=1;' if composition else '')+style)
        if mult:
            for x,value in [(-.78,mult.group(1)),(.78,mult.group(2))]:
                cell=ET.SubElement(self.root,'mxCell',id=self.id(),value=value,style='edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;fontFamily=Arial;fontSize=12;fontColor='+INK+';labelBackgroundColor=#FFFFFF;',vertex='1',connectable='0',parent=edge)
                g=ET.SubElement(cell,'mxGeometry',{'x':str(x),'y':'-1','relative':'1','as':'geometry'})
                ET.SubElement(g,'mxPoint',{'x':'0','y':'-10','as':'offset'})
        return edge

# D01: activity, explicit merge and guarded alternatives.
p=Page(1,'Actividad del modelado colaborativo','Vista de negocio · decisiones con guardas y nodos de fusión para caminos alternativos.',1120,1270)
start=p.box(538,110,24,24,'','ellipse;fillColor='+INK+';strokeColor='+INK+';')
a=p.node(380,165,340,55,'Abrir proyecto y recuperar el trabajo')
m1=p.box(535,255,30,30,'','rhombus;fillColor=#FFFFFF;')
b=p.node(380,325,340,55,'Modelar o plantear una consulta al equipo')
d=p.box(480,430,140,80,'¿Pedir ayuda\na la IA?','rhombus;fillColor='+MINT+';')
q=p.node(65,440,285,65,'Solicitar consulta, revisión, resumen\no propuesta de cambio',MINT)
q2=p.node(65,555,285,65,'Compartir respuesta o propuesta\ncon el equipo',MINT)
de=p.box(130,680,155,80,'¿Aplicar una\npropuesta?','rhombus;fillColor='+MINT+';')
mv=p.box(535,680,30,30,'','rhombus;fillColor=#FFFFFF;')
v=p.node(390,780,320,65,'Confirmar y validar permiso,\nrevisión vigente y reglas UML')
val=p.box(820,775,140,80,'¿Válido?','rhombus;fillColor='+BLUE+';')
save=p.node(390,930,320,65,'Persistir cambio y actividad;\ncompartir estado confirmado')
me=p.box(535,1040,30,30,'','rhombus;fillColor=#FFFFFF;')
endchoice=p.box(480,1120,140,80,'¿Continuar?','rhombus;fillColor='+MINT+';')
final=p.box(870,1145,28,28,'','ellipse;shape=doubleEllipse;fillColor='+INK+';')
vertical='exitX=.5;exitY=1;entryX=.5;entryY=0;'
for x,y in [(start,a),(a,m1),(m1,b),(b,d),(q,q2),(q2,de),(mv,v),(save,me),(me,endchoice)]:p.edge(x,y,'',vertical)
p.edge(d,q,'[sí]','exitX=0;exitY=.5;entryX=1;entryY=.5;')
p.edge(d,mv,'[no: edición manual]',vertical)
p.edge(de,mv,'[sí]','exitX=1;exitY=.5;entryX=0;entryY=.5;')
p.edge(de,me,'[no: conservar modelo]','edgeStyle=none;exitX=.5;exitY=1;entryX=0;entryY=.5;',pts=[(207.5,1055)])
p.edge(v,val,'','exitX=1;exitY=.5;entryX=0;entryY=.5;')
p.edge(val,save,'[sí]','edgeStyle=none;exitX=.5;exitY=1;entryX=1;entryY=.5;',pts=[(890,962.5)])
p.edge(val,m1,'[no: corregir / resincronizar]','edgeStyle=none;exitX=1;exitY=.5;entryX=1;entryY=.5;',pts=[(1020,815),(1020,270)])
p.edge(endchoice,m1,'[sí]','edgeStyle=none;exitX=0;exitY=.5;entryX=0;entryY=.5;',pts=[(30,1160),(30,270)])
p.edge(endchoice,final,'[no: pausar]','exitX=1;exitY=.5;entryX=0;entryY=.5;')
p.note(65,130,250,105,'Participantes: propietario, colaboradores y móvil. La IA no actúa sin una solicitud. El móvil observa.')

# D02: actors with deliberate role specializations.
p=Page(2,'Actores de SinapUML','Generalización UML: el triángulo apunta al actor general. Los servicios externos no son usuarios.',1150,750)
vis=p.actor(100,180,'Visitante')
member=p.actor(465,180,'Integrante\nautorizado',above=True)
owner=p.actor(285,390,'Propietario')
editor=p.actor(475,390,'Colaborador\nEDITOR')
mobile=p.actor(665,390,'Integrante en\nmodo móvil')
for n in [owner,editor,mobile]:p.edge(n,member,'','endArrow=block;endFill=0;strokeWidth=1.5;exitX=.5;exitY=0;entryX=.5;entryY=1;',pts=[(489,340)])
p.note(65,320,170,160,'Visitante: registrarse e iniciar sesión. La autenticación habilita el acceso; no es una generalización de roles.')
for y,name,desc in [(155,'Proveedor de IA','Responde y propone; no escribe el UML.'),(310,'Transcripción de voz','Transforma audio en texto.'),(465,'Proveedor push','Entrega eventos al navegador.')]:
    p.node(850,y,240,105,'«actor externo»\n'+name+'\n'+desc,MINT)
p.note(270,555,500,100,'Propietario y EDITOR expresan permisos persistidos. El modo móvil es una experiencia de interfaz; no crea un rol VIEWER ni revoca por sí solo el permiso de edición.')

# D03: readable use-case boundary, no invented include/extend.
p=Page(3,'Modelo general de casos de uso','Vista de alcance · asociaciones de participación; sin flechas que confundan orden temporal con inclusión.',1450,1080)
p.box(245,115,930,850,'SinapUML','fillColor=none;strokeWidth=2;verticalAlign=top;align=left;spacing=15;fontStyle=1;fontSize=18;')
v=p.actor(75,170,'Visitante');m=p.actor(75,465,'Integrante\nautorizado');o=p.actor(75,810,'Propietario')
ai=p.actor(1290,460,'Proveedor IA');st=p.actor(1290,690,'Transcripción');push=p.actor(1290,870,'Proveedor push')
m2=p.actor(1290,165,'Integrante\nautorizado')
items=[(310,175,'Registrarse e iniciar sesión\nCU-28 / CU-29'),(310,300,'Administrar proyectos y acceso\nCU-01 / CU-30 / CU-31'),(310,425,'Modelar, guardar y validar UML\nCU-02 a CU-04'),(310,550,'Deshacer/rehacer, colaborar\ny ver presencia · CU-05 a CU-07'),(310,675,'Importar/exportar y generar\nCapacidades heredadas'),(310,800,'CU-SP-05\nRetomar sesión registrada'),(790,175,'CU-SP-01\nConsultar a la IA grupal'),(790,285,'CU-SP-02\nSolicitar revisión del diagrama'),(790,395,'CU-SP-03\nResumir lo avanzado'),(790,535,'CU-SP-04\nSolicitar y confirmar edición por voz'),(790,675,'CU-SP-06\nObservar desde el móvil'),(790,815,'CU-SP-07\nActivar y recibir avisos push')]
ucs=[p.uc(x,y,305,t) for x,y,t in items]
p.assoc(v,ucs[0]);p.assoc(o,ucs[1],'',style='exitX=1;exitY=.5;entryX=0;entryY=.5;')
for idx in [1,2,3,4,5]:p.assoc(m,ucs[idx],'',style='exitX=1;exitY=.5;entryX=0;entryY=.5;')
for idx in [6,7,8,9,10,11]:p.edge(m2,ucs[idx],'','endArrow=none;exitX=0;exitY=.5;entryX=1;entryY=.5;',pts=[(1215,200),(1215,items[idx][1]+30)])
for idx in [6,7,8,9]:p.assoc(ai,ucs[idx],'',style='exitX=0;exitY=.5;entryX=1;entryY=.5;')
p.assoc(st,ucs[9]);p.assoc(push,ucs[11])
p.text(285,975,1090,55,'El actor Integrante autorizado se repite por legibilidad: representa al mismo actor. El modo móvil participa en CU-SP-05/06/07. Los CU heredados se agrupan; su recertificación sigue pendiente.',13)

# D04-D06 packages and dependencies.
PACKS=[('Identidad y acceso','Autenticación JWT; permisos por proyecto.'),('Proyecto y validación','Documento UML; reglas; control de revisión.'),('Colaboración','Presencia; operaciones confirmadas STOMP.'),('Asistente','Contexto; consulta; revisión; propuesta de edición.'),('Actividad y sesiones','Hechos, sesiones, visitas y avisos internos.'),('Interoperabilidad y generación','XMI y generación de aplicaciones.'),('Push','Suscripciones; cola; envío y reintentos.')]
p=Page(4,'Paquetes de análisis','Agrupación lógica de responsabilidades · no representa servidores ni una colección por paquete.',1200,850)
for i,(name,desc) in enumerate(PACKS):
    col=i%3;row=i//3;p.pkg(45+col*390,130+row*210,350,155,name+'\n\n'+desc)
p.note(445,570,700,140,'Separación de responsabilidades: las interfaces solicitan acciones; el backend valida el acceso y el modelo. Los proveedores de IA y voz son externos al dominio. Las propuestas de IA requieren confirmación humana.')
p=Page(5,'Dependencias entre paquetes','La flecha discontinua va del paquete que usa al paquete utilizado. Se omiten dependencias transversales repetidas.',1250,880)
ids={}
for key,x,y,w in [('Identidad y acceso',470,135,310),('Asistente',45,340,310),('Colaboración',470,340,310),('Interoperabilidad y generación',885,340,320),('Proyecto y validación',470,560,310),('Actividad y sesiones',45,695,310),('Push',885,695,320)]:ids[key]=p.pkg(x,y,w,100,key)
for a,b in [('Asistente','Proyecto y validación'),('Colaboración','Proyecto y validación'),('Interoperabilidad y generación','Proyecto y validación'),('Asistente','Identidad y acceso'),('Colaboración','Identidad y acceso'),('Proyecto y validación','Actividad y sesiones'),('Actividad y sesiones','Push')]:
    p.edge(ids[a],ids[b],'«use»','dashed=1;')
p.note(870,135,330,125,'Identidad y acceso es transversal. El asistente devuelve propuestas; solo el flujo autorizado de aplicación modifica el proyecto.')
p=Page(6,'Casos de uso y responsabilidades','Encapsulamiento de análisis · un caso puede colaborar con varios paquetes; no duplica el caso de uso.',1250,900)
groups=[('Asistente',[('CU-SP-01','Consultar IA grupal'),('CU-SP-02','Revisar diagrama'),('CU-SP-03','Resumir avances'),('CU-SP-04','Proponer edición por voz')]),('Actividad y sesiones',[('CU-SP-05','Retomar sesión registrada')]),('Colaboración',[('CU-SP-06','Observar desde móvil'),('CU-SP-04','Confirmar edición propuesta')]),('Push',[('CU-SP-07','Activar y recibir avisos')])]
for i,(name,cases) in enumerate(groups):
    x=50+(i%2)*610;y=130+(i//2)*330;p.pkg(x,y,560,285,name)
    for j,(code,title) in enumerate(cases):p.box(x+35,y+55+j*52,490,46,code+'  ·  '+title,'ellipse;fillColor=#FFFFFF;fontSize=13;spacing=6;')
p.note(50,810,1150,45,'Identidad y Proyecto/validación son transversales. XMI y generación conservan los casos heredados; se documentan sin cambiar sus identificadores.')

# Detailed interaction catalog shared by communication and sequence views.
SPECS=[
dict(code='CU-SP-01',title='Consultar a la IA grupal',roles=['Integrante','Chat común Vue','Asistente grupal','MongoDB','Proveedor IA','Otros clientes'],
msgs=[(0,1,'Escribir pregunta'),(1,2,'ASK + requestId + JWT'),(2,3,'Comprobar acceso; claim de solicitud'),(2,5,'Publicar mensaje de usuario'),(2,3,'Leer UML, miembros y contexto reciente'),(2,4,'Consultar contexto autorizado'),(4,2,'Respuesta del modelo',True),(2,3,'Completar respuesta sin duplicarla'),(2,5,'Publicar respuesta compartida'),(2,1,'Devolver intercambio',True)],
foot='El UML no cambia. Contexto acotado: hasta 20 mensajes y 50 actividades. El proveedor real todavía requiere aceptación.',
alt=('fallo del proveedor',[(2,3,'Marcar generación fallida'),(2,1,'Informar error; permitir reintento',True)])),
dict(code='CU-SP-02',title='Revisar el diagrama',roles=['Integrante','Chat común Vue','Asistente grupal','MongoDB','Proveedor IA','Otros clientes'],
msgs=[(0,1,'Solicitar revisión'),(1,2,'REVIEW + requestId + JWT'),(2,3,'Acceso y snapshot de revisión r'),(2,4,'Enviar modelo y contexto'),(4,2,'Texto y hallazgos',True),(2,2,'Filtrar referencias, severidad y límites'),(2,3,'Guardar revisión vinculada a r'),(2,5,'Publicar revisión compartida'),(2,1,'Mostrar observaciones',True)],
foot='Revisar no incrementa la revisión del documento. Se descartan referencias inventadas; el texto puede mostrarse sin hallazgos estructurados.',
alt=('proveedor no disponible',[(2,3,'Marcar generación fallida'),(2,1,'Error sin modificar el modelo',True)])),
dict(code='CU-SP-03',title='Resumir lo avanzado',roles=['Integrante tardío','Chat común Vue','Asistente grupal','MongoDB','Proveedor IA','Otros clientes'],
msgs=[(0,1,'Pedir resumen del proyecto'),(1,2,'SUMMARY_CURRENT + requestId'),(2,3,'Autorizar y recuperar snapshot'),(2,3,'Leer miembros, mensajes y actividad reciente'),(2,4,'Contexto disponible y petición'),(4,2,'Resumen con límites de contexto',True),(2,3,'Persistir respuesta y autoría'),(2,5,'Publicar resumen para el grupo'),(2,1,'Mostrar resumen',True)],
foot='No se modifica el diagrama. El resumen se contrasta con actividad registrada; no se presenta el contexto acotado como historia completa.',
alt=('sin actividad previa',[(2,4,'Indicar ausencia de hechos registrados'),(4,2,'Explicar el estado disponible',True),(2,3,'Persistir el resumen del estado disponible'),(2,5,'Publicar resumen para el grupo'),(2,1,'Mostrar resumen sin inventar avances',True)])),
dict(code='CU-SP-04',title='Solicitar y confirmar edición por voz',roles=['Integrante','Herramientas Vue','Voz y planner','STT / IA','API / Colaboración','MongoDB','Otros clientes'],
msgs=[(0,1,'Grabar orden con permiso'),(1,2,'POST audio WAV autenticado'),(2,3,'Transcribir audio con Whisper'),(3,2,'Texto transcrito',True),(2,3,'Planificar sobre el documento actual'),(3,2,'Acciones candidatas',True),(2,2,'Resolver IDs y validar intención / UML'),(2,1,'Propuesta + baseRevision',True),(0,1,'Revisar y confirmar Aplicar'),(1,4,'Comando STOMP + baseRevision'),(4,4,'Comprobar permiso y revisión vigente'),(4,5,'Transacción: modelo, actividad y avisos'),(5,4,'Commit; nueva revisión',True),(4,6,'Publicar operación confirmada'),(4,1,'Operación aplicada',True),(1,4,'Recuperar documento autoritativo vía REST')],
foot='La propuesta de voz se devuelve a quien solicita; la edición confirmada se propaga al grupo. Compartir toda la propuesta de voz sigue por verificar.',
alt=('audio inválido o revisión obsoleta',[(2,1,'Error de audio / planificación',True),(4,1,'Rechazo de conflicto; resincronizar',True)])),
dict(code='CU-SP-05',title='Retomar una sesión registrada',roles=['Integrante','Interfaz Vue','API de proyecto','Continuidad','MongoDB','Asistente grupal'],
msgs=[(0,1,'Abrir proyecto existente'),(1,2,'GET proyecto + JWT'),(2,4,'Autorizar y leer documento actual'),(2,1,'Documento y revisión',True),(1,3,'Consultar desde última visita y sesiones'),(3,4,'Leer visita, actividad y sesión'),(3,1,'Novedades y sesión actual / última',True),(1,3,'Registrar revisión observada'),(3,4,'Guardar visita por usuario y proyecto')],
foot='Retomar usa el documento vigente; no reproduce un Undo/Redo persistente. La recuperación entre dispositivos con MongoDB remoto sigue pendiente.',
alt=('opcional: pedir resumen',[(1,5,'SUMMARY_CURRENT en conversación común'),(5,1,'Resumen compartido',True)])),
dict(code='CU-SP-06',title='Observar el proyecto desde un móvil',roles=['Integrante móvil','Modo observador','API / STOMP','MongoDB','Otro integrante'],
msgs=[(0,1,'Abrir proyecto en modo informativo'),(1,2,'Leer proyecto y conectar presencia'),(2,3,'Validar acceso y leer estado'),(2,1,'Documento actual',True),(4,2,'Confirmar cambio autorizado'),(2,3,'Guardar cambio con revisión'),(2,1,'Evento de operación / presencia'),(1,2,'Reconciliar documento cada 2,5 s'),(2,3,'Leer versión autoritativa'),(2,1,'Actualizar representación',True)],
foot='El móvil no ofrece edición en esta experiencia. No existe rol VIEWER persistido; la autorización real corresponde al backend.',
alt=('desconexión y retorno',[(1,1,'Mostrar desconexión; evitar afirmar sincronía'),(1,2,'Reconectar y recuperar estado actual'),(2,1,'Documento autoritativo',True)])),
dict(code='CU-SP-07',title='Activar y recibir avisos push',roles=['Integrante','Vue / worker SW','API Spring','MongoDB','Worker push','Proveedor push'],
msgs=[(0,1,'Activar y conceder permiso'),(1,1,'Suscribir PushManager y vincular cuenta'),(1,2,'Registrar endpoint y claves + JWT'),(2,3,'Guardar suscripción del usuario'),(2,3,'Ante cambio ajeno: aviso + trabajo en transacción'),(4,3,'Reclamar trabajo con lease'),(3,4,'Trabajo pendiente',True),(4,5,'Enviar cifrado AES128GCM + VAPID'),(5,4,'Aceptación 2xx',True),(4,3,'Marcar SENT'),(5,1,'Entregar evento push'),(1,1,'Comprobar cuenta y mostrar aviso genérico'),(0,1,'Pulsar notificación'),(1,2,'Abrir proyecto y revalidar acceso')],
foot='Push está desactivado por defecto. HTTPS, VAPID y teléfono real pendientes. SENT significa aceptación del proveedor, no visualización física.',
alt=('resultado de entrega alternativo',[(5,4,'404/410 o fallo temporal',True),(4,3,'Eliminar vencida o reintentar hasta 8 veces')]))
]

def communication(n,s):
    p=Page(n,'Comunicación · '+s['code'],s['title']+' · objetos de análisis y mensajes numerados.',1350,950)
    coords=[(60,165),(350,165),(770,165),(770,445),(350,445),(1060,445),(1060,165)]
    roles=[r.replace('MongoDB','Proyecto y registros') for r in s['roles']];ids=[]
    for i,role in enumerate(roles):
        x,y=coords[i]
        if i==0 or role=='Otro integrante':ids.append(p.actor(x+60,y+5,role))
        else:
            stereo='«boundary»' if i==1 or role=='Otros clientes' else ('«entity»' if 'registros' in role else ('«external»' if 'Proveedor' in role or 'STT' in role else '«control»'))
            ids.append(p.node(x,y,205,88,stereo+'\n:'+role,BLUE if i<3 else MINT))
    pairs={}
    allmessages=[(str(i+1),m) for i,m in enumerate(s['msgs'])]+[(f'A{i+1}',m) for i,m in enumerate(s['alt'][1])]
    for number,msg in allmessages:
        a,b,t,*rest=msg;pairs.setdefault(tuple(sorted((a,b))),[]).append(f'{number}: {t}')
    # Communication links carry numbered groups in separately editable label cells.
    # Route links outside objects; use a message ledger to avoid dense labels.
    for (a,b),lines in pairs.items():
        nums=', '.join(t.split(':',1)[0] for t in lines)
        p.edge(ids[a],ids[b],nums,'fontSize=12;endArrow=none;')
    ledger=[]
    for i,m in allmessages:
        a,b,t,*_=m;ledger.append(f'{i}. {roles[a]} → {roles[b]}: {t}')
    mid=(len(ledger)+1)//2
    for col,lines in enumerate([ledger[:mid],ledger[mid:]]):
        p.text(45+col*655,585,620,265,'\n'.join(lines),13)
    p.note(45,845,1260,57,'Excepción / límite: '+s['alt'][0]+'. '+s['foot'])
    return p

for i,s in enumerate(SPECS,7):communication(i,s)

# D14: domain class diagram. Composition and multiplicities are visible on connectors.
p=Page(14,'Modelo de dominio','Vista conceptual · composición UML; las clases del modelo no equivalen a colecciones MongoDB.',1500,1120)
user=p.klass(35,130,250,'Usuario',['id: UUID','nombre: String','email: String'])
proj=p.klass(380,130,280,'Proyecto',['id: UUID','nombre: String','revision: long','ownerId: UUID'])
member=p.klass(35,390,250,'Membresía',['projectId: UUID','userId: UUID','rol: EDITOR'])
msg=p.klass(830,130,300,'MensajeIA',['id, projectId, requestId: UUID','authorUserId: UUID [0..1]','rol: USER | ASSISTANT','tipo: ASK | REVIEW | EDIT','      | SUMMARY_CURRENT','contenido: String','sequence: long'])
doc=p.klass(380,420,280,'DocumentoProyecto',['schemaVersion: String'])
model=p.klass(380,635,280,'ModeloUML',['classes: ClaseUML[*]','relationships: RelaciónUML[*]'])
layout=p.klass(35,650,250,'DistribuciónDiagrama',['posiciones y dimensiones','referencias por identificador'])
cl=p.klass(820,445,280,'ClaseUML',['id: UUID','nombre: String'])
attr=p.klass(1190,445,270,'AtributoUML',['id, nombre','tipo, visibilidad','nullable, identifier'])
op=p.klass(820,700,280,'OperaciónUML',['id, nombre','visibilidad','returnType: String [0..1]'])
param=p.klass(1190,710,270,'ParámetroUML',['id, nombre','tipo: String'])
rel=p.klass(380,870,300,'RelaciónUML',['id, tipo','sourceClassId, targetClassId','multiplicidadOrigen / Destino'])
p.assoc(user,proj,'1 propietario / 0..* proyectos')
p.assoc(proj,member,'1 / 0..*')
p.assoc(member,user,'0..* / 1')
p.assoc(proj,msg,'1 proyecto / 0..* mensajes')
p.assoc(proj,doc,'1 / 1',True)
p.assoc(doc,model,'1 / 1',True)
p.assoc(doc,layout,'1 / 1',True)
p.assoc(model,cl,'1 / 0..*',True)
p.assoc(model,rel,'1 / 0..*',True)
p.assoc(cl,attr,'1 / 0..*',True)
p.assoc(cl,op,'1 / 0..*',True)
p.assoc(op,param,'1 / 0..*',True)
p.edge(rel,cl,'origen / destino','exitX=1;exitY=.5;entryX=0;entryY=.5;',pts=[(740,960),(740,510)])
p.note(820,940,630,95,'La autoría del mensaje de usuario se identifica por authorUserId; la respuesta IA no inventa un usuario humano. returnType ausente representa void. Las relaciones referencian clases del mismo modelo.')

# D15 logical architecture: restrained number of crossings, external calls isolated.
p=Page(15,'Arquitectura lógica','Componentes de implementación · REST y STOMP tienen funciones distintas.',1450,990)
p.box(35,125,610,485,'«frontend»  Vue 3 + TypeScript','fillColor='+GRAY+';verticalAlign=top;spacing=12;fontStyle=1;')
p.box(730,125,680,485,'«backend»  Spring Boot · autoridad del proyecto','fillColor='+GRAY+';verticalAlign=top;spacing=12;fontStyle=1;')
front=p.node(75,200,240,90,'Pizarra Vue Flow\nPinia + adaptador UML')
chat=p.node(365,200,240,90,'Chat común\nHerramientas de voz')
history=p.node(75,390,240,90,'Actividad y sesiones\nModo móvil / PushPanel')
sync=p.node(365,390,240,90,'Cliente REST / STOMP\nReconciliación cada 2,5 s')
auth=p.node(770,200,250,90,'JWT + permisos\nOWNER / EDITOR')
project=p.node(1115,200,250,90,'Proyecto + validación\nRevisión y comandos UML')
assistant=p.node(770,390,250,90,'Asistente + contexto\nVoz y planner')
activity=p.node(1115,390,250,90,'Actividad / sesiones\nAvisos y cola push')
db=p.box(1090,710,290,110,'MongoDB replica set\nDocumento + registros','shape=cylinder3;size=15;fillColor='+MINT+';')
llm=p.node(415,715,260,100,'«externo» Proveedor IA\nllama.cpp / Bedrock',MINT)
stt=p.node(80,715,260,100,'«externo» Whisper\nTranscripción de voz',MINT)
worker=p.node(755,715,260,100,'Worker push\nLease, VAPID y reintentos',MINT)
for a,b in [(front,sync),(chat,sync),(history,sync)]:p.edge(a,b)
p.edge(sync,auth,'REST /api · JWT');p.edge(sync,project,'STOMP /ws · operaciones',pts=[(670,445),(670,330),(1240,330)])
p.edge(auth,project,'autorización');p.edge(auth,assistant);p.edge(project,activity,'cambio confirmado')
p.edge(assistant,llm,'inferencia');p.edge(assistant,stt,'audio → texto',pts=[(700,550),(210,550)])
p.edge(project,db,'persistir');p.edge(activity,db,'misma transacción');p.edge(worker,db,'reclamar y actualizar')
p.note(45,855,1335,70,'Las propuestas no escriben el canvas. Una confirmación explícita pasa por validación autoritativa. XMI/generación usa el servicio de proyecto. El proveedor push entrega al service worker del navegador; se detalla en D25.')

# D16 deployment: separate local reality from proposed cloud.
p=Page(16,'Arquitectura física y despliegue','Izquierda: entorno local documentado. Derecha: objetivo de nube todavía no desplegado ni aceptado.',1450,970)
p.box(35,125,650,690,'ENTORNO LOCAL','fillColor='+GRAY+';verticalAlign=top;spacing=15;fontStyle=1;fontSize=18;')
p.box(755,125,650,690,'«propuesto» NUBE + HTTPS','fillColor='+AMBER+';dashed=1;verticalAlign=top;spacing=15;fontStyle=1;fontSize=18;')
browser=p.node(80,205,250,110,'«device» Navegador\nEscritorio / móvil')
vite=p.node(390,205,250,110,'«executionEnvironment»\nVite · puerto 4200')
spring=p.node(235,420,320,110,'«executionEnvironment»\nJVM 21 · Spring Boot :8082')
mongo=p.box(80,650,250,100,'«executionEnvironment»\nMongoDB replica set :27017','shape=cylinder3;size=15;fillColor='+MINT+';')
runtime=p.node(390,650,250,100,'Runtimes opcionales\nWhisper / llama.cpp',MINT)
p.edge(browser,vite,'HTTP');p.edge(vite,spring,'proxy /api y /ws');p.edge(spring,mongo,'driver MongoDB');p.edge(spring,runtime,'HTTP local')
c1=p.node(810,205,540,110,'«device» Navegadores remotos\nDesarrolladores y observador móvil',AMBER)
c2=p.node(810,420,245,110,'«propuesto» Hosting\nFrontend + HTTPS',AMBER)
c3=p.node(1105,420,245,110,'«propuesto» API\nSpring Boot + WSS',AMBER)
c4=p.box(810,650,245,100,'«propuesto» MongoDB\nReplica set administrado','shape=cylinder3;size=15;fillColor='+AMBER+';')
c5=p.node(1105,650,245,100,'«externo» IA y push\nProveedor por configurar',AMBER)
p.edge(c1,c2,'HTTPS',style='dashed=1;');p.edge(c2,c3,'HTTPS / WSS',style='dashed=1;');p.edge(c3,c4,'TLS',style='dashed=1;');p.edge(c3,c5,'HTTPS',style='dashed=1;')
p.note(45,850,1350,65,'No hay cuenta de nube configurada ni recepción push real verificada. Esta topología de nube es una propuesta sin proveedor elegido. Docker local se usa para MongoDB; no demuestra despliegue en nube.')

# D17 document aggregates, distinct from conceptual UML and physical collection listing.
p=Page(17,'Modelo lógico documental','Agregados y referencias por identificador · composición = embebido; flecha discontinua = referencia.',1450,960)
project=p.klass(520,150,360,'Proyecto · agregado raíz',['id, ownerId, nombre, revision','document: DocumentoProyecto'],fill=MINT)
document=p.klass(520,410,360,'DocumentoProyecto · embebido',['schemaVersion','umlModel: clases y relaciones','layout: posiciones por ID'])
user=p.klass(45,150,340,'Identidad y acceso',['Usuario: id, email, passwordHash','Membresía: projectId, userId, rol','Invitación: projectId, destinatario'])
conversation=p.klass(1045,150,360,'Conversación compartida',['Mensaje: projectId, requestId, sequence','autor, tipo, contenido, projectRevision','review / plan opcionales'])
continuity=p.klass(45,440,340,'Continuidad de trabajo',['Actividad: projectId, sessionId, revisión','Sesión: inicio, fin, estado','Visita: projectId, userId, revisión vista'])
notification=p.klass(1045,440,360,'Avisos y entrega',['Aviso: destinatario, projectId, dedupKey','Suscripción: userId, endpoint, claves','Trabajo: notificationId, subscriptionId'])
p.assoc(project,document,'1 / 1',True)
for a in [user,conversation,continuity,notification]:p.edge(a,project,'ownerId / projectId' if a==user else 'projectId','dashed=1;')
p.note(45,730,1350,115,'NoSQL no significa una colección por clase del diagrama diseñado. ClaseUML, AtributoUML, OperaciónUML, ParámetroUML y RelaciónUML están dentro de document.umlModel. La actividad y las conversaciones son registros separados. Las escrituras relacionadas usan transacciones MongoDB.')

# D18 actual schema and index definitions from MongoPersistenceConfiguration.
p=Page(18,'Persistencia física MongoDB','Colecciones e índices relevantes del código · UQ = único; IDX = consulta; referencias sin claves foráneas SQL.',1650,1300)
collections=[
('app_users',['_id: UUID; email; passwordHash','UQ email (collation strength 2)']),
('projects',['_id, ownerId, name, revision','document: BSON embebido','IDX (ownerId, updatedAt)']),
('project_memberships',['_id, projectId, userId, role','UQ (projectId, userId)','IDX userId']),
('project_invitations',['_id, projectId, invitedEmail, status','IDX (invitedEmail, status, createdAt)','IDX (projectId, status)']),
('project_ai_messages',['_id, projectId, requestId, role, sequence','UQ (projectId, requestId, role)','UQ sequence; IDX (projectId, sequence)']),
('project_activities',['_id, projectId, operationId, revisionAfter','UQ (projectId, operationId)','UQ (projectId, revisionAfter)','IDX (projectId, createdAt)']),
('project_sessions',['_id, projectId, status, startRevision','UQ projectId parcial: status=OPEN','IDX (status, lastActivityAt)']),
('project_session_participants',['_id, sessionId, userId','UQ (sessionId, userId)']),
('project_user_visits',['_id, projectId, userId, lastSeenRevision','UQ (projectId, userId)']),
('project_notifications',['_id, projectId, recipientUserId, read','UQ dedupKey','IDX (recipientUserId, read, createdAt)']),
('push_subscriptions',['_id: hash de endpoint; userId','endpoint, p256dh, auth','IDX userId']),
('push_deliveries',['_id, notificationId, subscriptionId','status, attempts, nextAttemptAt, leaseUntil','IDX (status, nextAttemptAt, leaseUntil)','TTL expiresAt: BSON Date']),
]
for i,(name,attrs) in enumerate(collections):
    x=40+(i%3)*540;y=135+(i//3)*245;p.klass(x,y,500,name,attrs,h=190)
p.note(45,1135,1560,100,'Colecciones técnicas adicionales: _sequences (contador global de mensajes) y legacy_migrations. Los Instant usan conversión UTC a String; expiresAt de push_deliveries usa BSON Date para TTL. Se requiere replica set y transacciones. Campos e índices mostrados son una selección, no un diccionario exhaustivo.')

def sequence(n,s):
    count=len(s['roles']);step=205;w=max(1200,count*step+100)
    main=s['msgs'];alt=s['alt'];row=58;start=245;end=start+(len(main)+len(alt[1])+2)*row
    h=end+190
    p=Page(n,'Secuencia · '+s['code'],s['title']+' · flujo principal y escenario alternativo identificado.',w,h)
    centers=[]
    for i,r in enumerate(s['roles']):
        x=50+i*step;centers.append(x+82)
        p.node(x,135,165,68,r,BLUE if i<3 else MINT)
        p.line(x+82,203,x+82,end+20,'','dashed=1;endArrow=none;strokeColor=#AAB5BC;')
    def message(m,y,num):
        a,b,t,*ret=m;xa,xb=centers[a],centers[b]
        sty='dashed=1;endArrow=open;' if ret and ret[0] else 'endArrow=block;endFill=1;'
        if a==b:
            p.edge(None,None,'',sty+'edgeStyle=none;',pts=[(xa+65,y),(xa+65,y+22)],ends=[(xa,y),(xa,y+22)])
            p.text(xa+10,y-35,step-25,33,f'{num}. {t}',12)
        else:
            p.line(xa,y,xb,y,'',sty)
            p.text(min(xa,xb)+7,y-35,abs(xb-xa)-14,33,f'{num}. {t}',12)
    optional=alt[0].startswith('opcional')
    if not optional:
        common={'CU-SP-01':3,'CU-SP-02':3,'CU-SP-03':3,'CU-SP-04':2,'CU-SP-06':4,'CU-SP-07':8}.get(s['code'],2)
        fy=start+row*common-38
        p.box(25,fy,w-50,end-fy+10,'','fillColor=none;strokeColor=#657581;')
        p.text(38,fy+4,w-75,28,'alt  [flujo principal: solicitud procesable]',13,True)
    for i,m in enumerate(main):message(m,start+i*row,i+1)
    frame_y=start+len(main)*row+12
    if optional:p.box(32,frame_y,w-64,(len(alt[1])+1)*row+12,'','fillColor=none;strokeColor=#657581;')
    else:p.line(25,frame_y,w-25,frame_y,'','dashed=1;endArrow=none;strokeColor=#A2854E;')
    voice=s['code']=='CU-SP-04'
    p.text(45,frame_y+7,w-90,30,('opt  ' if optional else '')+'['+('audio inválido / planificación rechazada' if voice else alt[0])+']',13,True)
    for j,m in enumerate(alt[1]):
        if voice and j==1:
            split=frame_y+row+30
            p.line(25,split,w-25,split,'','dashed=1;endArrow=none;strokeColor=#A2854E;')
            p.text(45,split+3,w-90,28,'[revisión obsoleta al confirmar]',13,True)
        message(m,frame_y+row+j*row+(28 if voice and j>0 else 0),f'A{j+1}')
    p.note(40,end+55,w-80,70,s['foot'])
    return p

for i,s in enumerate(SPECS,19):sequence(i,s)

def avoid_shapes(p):
    """Route orthogonal connectors through free channels, not through other objects.
    Uses coordinate visibility grid and Dijkstra with a bend penalty.
    Sequence messages keep their explicit chronological geometry.
    """
    cells={c.get('id'):c for c in p.root.findall('mxCell')}
    rects={}
    for ident,c in cells.items():
        if c.get('vertex')!='1' or c.get('parent')!='1':continue
        st=c.get('style','');g=c.find('mxGeometry')
        if 'text;' in st or 'fillColor=none;' in st:continue
        x,y,w,h=[float(g.get(k,'0')) for k in ['x','y','width','height']]
        rects[ident]=(x,y,x+w,y+h)
    # Large visual containers (frontend, system boundary) must not block routes.
    for ident,r in list(rects.items()):
        if any(ident!=j and r[0]<v[0] and r[1]<v[1] and r[2]>v[2] and r[3]>v[3] for j,v in rects.items()):
            del rects[ident]
    def inside(pt,r):return r[0]<pt[0]<r[2] and r[1]<pt[1]<r[3]
    def clear(a,b,rs):
        for x1,y1,x2,y2 in rs:
            if a[0]==b[0] and x1<a[0]<x2 and max(min(a[1],b[1]),y1)<min(max(a[1],b[1]),y2):return False
            if a[1]==b[1] and y1<a[1]<y2 and max(min(a[0],b[0]),x1)<min(max(a[0],b[0]),x2):return False
        return True
    for c in cells.values():
        st=c.get('style','');a=c.get('source');b=c.get('target')
        if c.get('edge')!='1' or 'edgeStyle=none;' in st or a not in rects or b not in rects or a==b:continue
        ra,rb=rects[a],rects[b]
        def ports(r,which):
            x1,y1,x2,y2=r;cx=(x1+x2)/2;cy=(y1+y2)/2
            pp=[('left',(x1-18,cy),0,.5),('right',(x2+18,cy),1,.5),('top',(cx,y1-18),.5,0),('bottom',(cx,y2+18),.5,1)]
            xx=re.findall(which+'X=([.0-9]+)',st);yy=re.findall(which+'Y=([.0-9]+)',st)
            if xx and yy:
                ax,ay=float(xx[-1]),float(yy[-1]);selected=[v for v in pp if v[2]==ax and v[3]==ay]
                if selected:return selected
            return pp
        starts=ports(ra,'exit');goals=ports(rb,'entry')
        obstacles=[(x1-6,y1-6,x2+6,y2+6) for x1,y1,x2,y2 in rects.values()]
        xs={20.,p.w-20.};ys={110.,p.h-65.}
        for x1,y1,x2,y2 in rects.values():xs.update([x1-18,x2+18]);ys.update([y1-18,y2+18])
        for _,pt,_,_ in starts+goals:xs.add(pt[0]);ys.add(pt[1])
        xs=sorted(v for v in xs if 10<=v<=p.w-10);ys=sorted(v for v in ys if 105<=v<=p.h-55)
        points={(ix,iy):(x,y) for ix,x in enumerate(xs) for iy,y in enumerate(ys) if not any(inside((x,y),r) for r in obstacles)}
        lookup={v:k for k,v in points.items()};heap=[];dist={};prev={};origin={}
        for port in starts:
            if port[1] not in lookup:continue
            xy=lookup[port[1]];state=(xy[0],xy[1],-1);dist[state]=0;origin[state]=port;heapq.heappush(heap,(0,state))
        targets={lookup[port[1]]:port for port in goals if port[1] in lookup}
        winner=None
        while heap:
            cost,state=heapq.heappop(heap)
            if cost!=dist.get(state):continue
            ix,iy,direction=state
            if (ix,iy) in targets:winner=state;break
            here=points[(ix,iy)]
            for dx,dy,newdir in [(1,0,0),(-1,0,0),(0,1,1),(0,-1,1)]:
                nxt=(ix+dx,iy+dy)
                if nxt not in points or not clear(here,points[nxt],obstacles):continue
                there=points[nxt];nstate=(nxt[0],nxt[1],newdir)
                nc=cost+abs(here[0]-there[0])+abs(here[1]-there[1])+(35 if direction not in [-1,newdir] else 0)
                if nc<dist.get(nstate,float('inf')):
                    dist[nstate]=nc;prev[nstate]=state;origin[nstate]=origin[state];heapq.heappush(heap,(nc,nstate))
        if winner is None:continue
        path=[];cur=winner
        while True:
            path.append(points[(cur[0],cur[1])])
            if cur not in prev:break
            cur=prev[cur]
        path.reverse();simple=[]
        for pt in path:
            if len(simple)>=2 and (simple[-2][0]==simple[-1][0]==pt[0] or simple[-2][1]==simple[-1][1]==pt[1]):simple[-1]=pt
            else:simple.append(pt)
        sp=origin[winner];tp=targets[(winner[0],winner[1])]
        c.set('style',st+f'edgeStyle=none;exitX={sp[2]};exitY={sp[3]};entryX={tp[2]};entryY={tp[3]};')
        g=c.find('mxGeometry')
        for ar in list(g):g.remove(ar)
        ar=ET.SubElement(g,'Array',{'as':'points'})
        for x,y in simple:ET.SubElement(ar,'mxPoint',x=str(x),y=str(y))

for p in PAGES:avoid_shapes(p)

master=ET.Element('mxfile',host='Electron',agent='SinapUML documentation',version='24.7.17',type='device')
for p in PAGES:
    master.append(copy.deepcopy(p.diagram))
    single=ET.Element('mxfile',host='Electron',type='device');single.append(copy.deepcopy(p.diagram))
    name=META[p.n-1]['archivo_xml_previsto']
    ET.indent(single)
    ET.ElementTree(single).write(OUT/name,encoding='utf-8',xml_declaration=True)
ET.indent(master);ET.ElementTree(master).write(OUT/'SinapUML-PUDS.drawio',encoding='utf-8',xml_declaration=True)
manifest=[]
for p in PAGES:
    ids={c.get('id') for c in p.root.findall('mxCell')}
    assert len(ids)==len(p.root.findall('mxCell'))
    for c in p.root.findall('mxCell'):
        for key in ['source','target','parent']:
            assert c.get(key) is None or c.get(key) in ids,(p.code,c.get('id'),key)
        g=c.find('mxGeometry')
        if c.get('vertex')=='1' and c.get('parent')=='1':
            assert float(g.get('x'))>=0 and float(g.get('y'))>=0
            assert float(g.get('x'))+float(g.get('width'))<=p.w+1
            assert float(g.get('y'))+float(g.get('height'))<=p.h+1
    manifest.append({'codigo':p.code,'titulo':p.diagram.get('name'),'archivo':META[p.n-1]['archivo_xml_previsto'],'width':p.w,'height':p.h,'cells':len(ids)})
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
readme='''# SinapUML · Diagramas PUDS

Versión documental del 9 de noviembre de 2026. Los 25 diagramas corresponden a las reservas D01–D25 del Word V4. Son una base revisada contra el código, pendiente de validación académica del docente.

## Abrir y editar

1. Extraer el ZIP completo antes de abrir sus archivos.
2. En draw.io Desktop: Archivo → Abrir y elegir `SinapUML-PUDS.drawio`.
3. Cambiar de diagrama con las 25 pestañas inferiores. Textos, formas, conectores y posiciones son editables.
4. Para trabajar por separado, abrir cualquiera de los archivos `Dxx-*.xml` con draw.io.
5. Guardar una copia antes de cambiar el modelo; los XML individuales y el archivo maestro son instantáneas, sin sincronización automática entre ellos.

## Imágenes para la documentación

- `png/`: imágenes con fondo blanco, exportadas por draw.io; útiles para revisar e insertar en Word.
- `svg/`: imágenes vectoriales para ampliar sin pixelación. Si Word admite SVG, preferir este formato.
- `index.html`: galería local con enlaces a cada imagen y XML; funciona sin subir archivos a un servicio.
- `manifest.json`: inventario de archivos y dimensiones de los lienzos.

Insertar cada imagen en la reserva del mismo código del Word y conservar su pie de figura. Diagramas extensos, especialmente D14, D18, D22 y D25, necesitan una página completa o una sección horizontal; no reducirlos a un recuadro de tres pulgadas si el texto pierde legibilidad. Actualizar los índices después de insertarlos. El Word V4 se conserva sin modificar.

## Convenciones y alcance

Los casos CU-SP-01 a CU-SP-07 conservan la numeración de la documentación. Los casos heredados del primer parcial se agrupan en D03 por legibilidad; esta vista no sustituye su catálogo ni acredita su recertificación.

En D07–D13 los enlaces muestran números de mensaje. La lista inferior especifica orden, emisor, receptor y acción, incluidos los mensajes al propio objeto; no se usa la posición espacial para representar el tiempo. Proyecto y registros es una abstracción de análisis, mientras las secuencias de diseño sí identifican MongoDB.

En D14 el rombo lleno indica composición, y las multiplicidades aparecen cerca de los extremos. D17 representa agregados documentales; D18 muestra colecciones e índices seleccionados, sin sugerir una colección por clase UML ni claves foráneas SQL.

En secuencias, línea discontinua representa una respuesta; las líneas de vida son verticales. Los fragmentos alt muestran un escenario principal y una alternativa; opt identifica el resumen opcional de CU-SP-05. Los participantes de backend agrupan servicios y controles de acceso; las flechas hacia MongoDB se ejecutan desde el servidor.

La nube de D16 es una propuesta: no hay proveedor ni cuenta configurados. El móvil es un modo informativo de interfaz, no un rol VIEWER persistido. Push está desactivado por defecto; SENT acredita aceptación del proveedor, no recepción física. No se afirma Gemini integrado ni aceptación de IA/voz reales.

La ruta de voz devuelve la propuesta al solicitante y comparte la operación confirmada. La difusión grupal completa de la propuesta de voz está pendiente de verificar/completar. D10 y D22 lo señalan; no se inventó un chat de voz grupal que el código actual no demuestra.

## Fuentes y mantenimiento

Se contrastó el documento PUDS V4 y el código de ProjectAssistantService, ProjectAssistantContextService, AssistantVoiceService, AssistantPlanService, editor-sync.ts, ProjectTools.vue, continuidad/sesiones, PushDeliveryService y MongoPersistenceConfiguration. Estas vistas no ejecutan pruebas de aceptación ni cambian código de la aplicación.

Constructor reproducible: `scripts/build-puds-drawio.py`. Exportador local: `scripts/export-puds-drawio.ps1` (requiere draw.io Desktop). Si se regenera el XML, volver a exportar y revisar las imágenes; el constructor puede reemplazar las ediciones manuales hechas en sus archivos de salida.

## Correspondencia con el documento

| Código | Vista | Sección PUDS |
| --- | --- | --- |
'''
sections=['3.2 Modelo de negocio','4.1 Actores','4.4 Casos de uso','5.1.1 Paquetes','5.1.2 Dependencias','5.2 Paquetes y casos']+['5.3.'+str(i)+' Comunicación' for i in range(1,8)]+['5.4 Dominio','6.1.1 Arquitectura lógica','6.1.2 Arquitectura física','6.2.1 Datos lógicos','6.2.2 Datos físicos']+['6.3.'+str(i)+' Secuencia' for i in range(1,8)]
for item,section in zip(manifest,sections):readme+=f"| {item['codigo']} | {item['titulo'].split(' · ',1)[-1]} | {section} |\n"
(OUT/'README.md').write_text(readme,encoding='utf-8')
cards=[]
for item in manifest:
    stem=Path(item['archivo']).stem;title=html.escape(item['titulo'])
    cards.append(f'<article><h2>{title}</h2><a href="svg/{stem}.svg"><img loading="lazy" src="png/{stem}.png" alt="{title}"></a><p><a href="{stem}.xml" download>XML editable</a> · <a href="svg/{stem}.svg">SVG vectorial</a> · <a href="png/{stem}.png">PNG</a></p></article>')
(OUT/'index.html').write_text('''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SinapUML · Diagramas PUDS</title><style>body{font:16px/1.55 Arial,sans-serif;color:#243746;background:#f4f6f8;margin:0}header,main{max-width:1280px;margin:auto;padding:30px}h1{font-size:32px}h2{font-size:19px}a{color:#147d78}article{background:white;border:1px solid #dbe1e5;border-radius:8px;padding:22px;margin-bottom:24px}img{display:block;width:100%;max-height:780px;object-fit:contain;object-position:top}header p{max-width:900px}</style><header><h1>SinapUML · Diagramas PUDS</h1><p>25 diagramas editables, organizados por los códigos del documento. Abrí el archivo maestro en draw.io para editar; usá esta galería para revisar y ampliar las imágenes.</p><p><a href="SinapUML-PUDS.drawio" download>Archivo maestro draw.io</a> · <a href="README.md">Guía y alcance</a></p></header><main>'''+''.join(cards)+'</main></html>',encoding='utf-8')
print(json.dumps({'diagrams':len(PAGES),'output':str(OUT),'master':'SinapUML-PUDS.drawio'},ensure_ascii=False))
