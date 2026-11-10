"""Academic UML revision based on the student's seven visual references.
Reuses the verified project facts from V1, without overwriting its deliverables.
"""
from pathlib import Path
import copy, csv, html, json, re, xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
source=ROOT/'scripts/build-puds-drawio.py'
ctx={'__file__':str(source),'__name__':'reference_model'}
exec(compile(source.read_text(encoding='utf-8').split("master=ET.Element")[0],str(source),'exec'),ctx)
Page=ctx['Page'];SPECS=ctx['SPECS'];pages=ctx['PAGES'];route=ctx['avoid_shapes']
OUT=ROOT/'docs/formal/diagramas-drawio-v2';OUT.mkdir(parents=True,exist_ok=True)
old=list(pages);pages.clear()
byid={p.n:p for p in old}

def frame(p,x,y,w,h,title):
    p.box(x,y,w,h,'','fillColor=none;strokeColor=#333333;strokeWidth=1;')
    width=min(w-20,max(160,len(title)*8))
    p.text(x+10,y+2,width-15,24,title,13,True)
    p.line(x,y+28,x+width-12,y+28,'','endArrow=none;strokeColor=#333333;')
    p.line(x+width-12,y+28,x+width,y+16,'','endArrow=none;strokeColor=#333333;')
    p.line(x+width,y+16,x+width,y,'','endArrow=none;strokeColor=#333333;')

def bce(p,x,y,kind,name):
    c=p.box(x,y,56,56,'','ellipse;fillColor=#FFFFFF;strokeColor=#222222;strokeWidth=1.4;')
    if kind=='boundary':
        p.line(x-16,y-2,x-16,y+58,'','endArrow=none;')
        p.line(x-16,y+28,x,y+28,'','endArrow=none;')
    elif kind=='control':
        p.line(x+8,y-8,x+35,y-8,'','endArrow=open;strokeWidth=1.3;')
        p.line(x+8,y-8,x+8,y+4,'','endArrow=none;')
    else:p.line(x-2,y+66,x+58,y+66,'','endArrow=none;')
    p.box(x-115,y+78,290,50,'«'+kind+'»\n'+name,'text;fillColor=none;strokeColor=none;align=center;fontSize=14;')
    return c

def comp(p,x,y,w,h,name):
    c=p.box(x,y,w,h,name,'fillColor=#FFFFFF;spacingLeft=20;strokeColor=#333333;')
    for dy in [15,35]:p.box(x-6,y+dy,15,10,'','fillColor=#FFFFFF;strokeColor=#333333;')
    return c

def cube(p,x,y,w,h,name,artifacts):
    c=p.box(x,y,w,h,'','shape=cube;size=15;fillColor=#FFFFFF;strokeColor=#333333;')
    p.text(x+24,y+22,w-55,40,name,15,True)
    for i,t in enumerate(artifacts):comp(p,x+40,y+80+i*68,w-80,48,t)
    return c

def class3(p,x,y,w,name,attrs,ops):
    titleh=48;ah=max(60,26*len(attrs)+16);oh=max(60,26*len(ops)+16)
    c=p.box(x,y,w,titleh+ah+oh,'','fillColor=#FFFFFF;')
    p.box(x+10,y+4,w-20,titleh-8,name,'text;fillColor=none;strokeColor=none;align=center;fontSize=14;fontStyle=1;')
    p.line(x,y+titleh,x+w,y+titleh,'','endArrow=none;')
    p.text(x+12,y+titleh+7,w-24,ah-14,'\n'.join(attrs),13)
    p.line(x,y+titleh+ah,x+w,y+titleh+ah,'','endArrow=none;')
    p.text(x+12,y+titleh+ah+7,w-24,oh-14,'\n'.join(ops) or ' ',13)
    return c

def message_link(p,a,b,labels,x,y,w=280,h=85,style=''):
    p.edge(a,b,'','edgeStyle=none;endArrow=none;'+style)
    p.text(x,y,w,h,'\n'.join(labels),13)

# Keep the inventory and domain views, preserving their factual content.
for n in [1,2,3,4,5,6,14,17,18]:pages.append(byid[n])

# Communication uses the BCE symbols and messages beside their links.
COMM=[
('VistaChat','ControlConsultaIA','Proyecto / MensajesIA','Proveedor IA',
 ['1. Consultar(pregunta) →'],['1.1 EnviarSolicitud() →','← 1.7 MostrarRespuesta()'],
 ['1.2 RecuperarContexto() →','1.5 RegistrarIntercambio() →'],['1.3 ConsultarIA() →','← 1.4 Responder()'],['1.6 DifundirRespuesta() →']),
('VistaChat','ControlRevision','Documento / RevisionIA','Proveedor IA',
 ['1. SolicitarRevision() →'],['1.1 EnviarRevision() →','← 1.7 MostrarHallazgos()'],
 ['1.2 ObtenerSnapshot() →','1.5 RegistrarRevision() →'],['1.3 RevisarModelo() →','← 1.4 DevolverHallazgos()'],['1.6 CompartirRevision() →']),
('VistaChat','ControlResumen','Proyecto / Actividad','Proveedor IA',
 ['1. PedirResumen() →'],['1.1 SolicitarResumen() →','← 1.7 MostrarResumen()'],
 ['1.2 RecuperarContexto() →','1.5 RegistrarRespuesta() →'],['1.3 ResumirContexto() →','← 1.4 EntregarResumen()'],['1.6 CompartirResumen() →']),
('HerramientasVoz','ControlEdicionVoz','Documento / Actividad','Whisper + proveedor IA',
 ['1. GrabarOrden() →','2. ConfirmarPropuesta() →'],['1.1 EnviarAudio() →','← 1.4 MostrarPropuesta()','2.1 Aplicar(baseRevision) →'],
 ['1.2 LeerDocumento() →','2.2 ValidarYGuardar() →'],['1.3 TranscribirYPlanificar() →'],['2.3 CompartirCambioConfirmado() →']),
('VistaProyecto','ControlContinuidad','Documento / Visita / Sesion','Asistente grupal',
 ['1. AbrirProyecto() →'],['1.1 SolicitarEstado() →','← 1.4 MostrarNovedades()'],
 ['1.2 RecuperarUltimaVisita() →','1.3 RegistrarVisita() →'],['[pide resumen] 2. Resumir() →'],['Estado vigente y actividad\ndisponibles para el integrante.']),
('VistaMovil','ControlObservacion','Documento / Presencia','Otro integrante',
 ['1. ObservarProyecto() →'],['1.1 ConectarYLeer() →','← 1.4 MostrarEstado()','1.5 Reconciliar(2,5 s) →'],
 ['1.2 LeerEstadoActual() →'],['2. ConfirmarCambio() ←'],['1.3 CompartirOperacion() →']),
('VistaPush / SW','ControlAvisosPush','Suscripcion / Aviso / Trabajo','Proveedor push',
 ['1. ActivarAvisos() →','3. AbrirNotificacion() →'],['1.1 RegistrarSuscripcion() →','← 3.1 RevalidarAcceso()'],
 ['1.2 GuardarSuscripcion() →','2.1 ReclamarTrabajo() →','2.4 RegistrarResultado() →'],['2.2 EnviarCifrado() →','← 2.3 AceptarORechazar()'],['[cuenta vinculada]\nMostrar aviso genérico.'])
]
for i,data in enumerate(COMM):
    s=SPECS[i];ui,control,entity,external,ua,uc,ce,cx,co=data
    p=Page(i+7,'Comunicación · '+s['code'],s['title']+' · realización de análisis con objetos BCE.',1570,900)
    frame(p,25,120,1520,660,s['code'])
    actor=p.actor(75,360,'Integrante' if i!=5 else 'Integrante móvil')
    u=bce(p,360,365,'boundary',ui);c=bce(p,780,365,'control',control)
    e=bce(p,1245,205,'entity',entity)
    x=p.actor(1265,580,external) if i==5 else p.box(1190,580,210,80,'«external»\n'+external,'fillColor=#FFFFFF;')
    other=bce(p,720,655,'boundary','ServiceWorker' if i==6 else 'Otros clientes') if i!=4 else None
    message_link(p,actor,u,ua,145,290,210,65)
    message_link(p,u,c,uc,440,265,310,105)
    message_link(p,c,e,ce,925,190,300,120)
    message_link(p,c,x,cx,915,490,285,85)
    if other:message_link(p,x if i==6 else c,other,['2.5 EntregarPush() ←' if i==6 else t.replace('→','↙') for t in co],815,615,355,85)
    p.text(40,800,1490,48,'Alternativa / límite: '+s['alt'][0]+'. '+s['foot'],12)

# D15: explicit layers with a small, deliberate dependency set.
p=Page(15,'Diseño lógico · arquitectura por capas','Dependencias dirigidas hacia los servicios y contratos utilizados. Adaptada a Vue, Spring Boot y MongoDB.',1660,1120)
layer_titles=['PRESENTACIÓN','APLICACIÓN','DOMINIO Y ADAPTADORES','INFRAESTRUCTURA']
for row,title in enumerate(layer_titles):
    y=135+row*220;p.box(25,y,1610,200,'','fillColor=none;strokeColor=#333333;')
    p.text(40,y+65,175,65,title,13,True)
top=[comp(p,245+j*275,180,240,75,t) for j,t in enumerate(['Pizarra UML','Chat grupal / Voz','Actividad y sesiones','Vista móvil / Push'])]
app=[comp(p,245+j*230,400,200,75,t) for j,t in enumerate(['Proyecto','Asistente','Colaboración','Continuidad','Avisos / Push','XMI / Generación'])]
domain=[comp(p,245+j*325,620,280,75,t) for j,t in enumerate(['ProjectDocument + reglas UML','Permisos y revisión','Repositorios MongoDB','Puertos IA / Voz / Push'])]
infra=[comp(p,245+j*325,840,280,75,t) for j,t in enumerate(['Vue / Vite','Java 21 / Spring Boot','MongoDB replica set','Runtimes / proveedores'])]
for a,b in [(top[0],app[0]),(top[1],app[1]),(top[1],app[2]),(top[2],app[3]),(top[3],app[4]),(app[0],domain[0]),(app[2],domain[1]),(app[3],domain[2]),(app[4],domain[3]),(app[1],domain[3]),(domain[0],infra[1]),(domain[1],infra[1]),(domain[2],infra[2]),(domain[3],infra[3])]:p.edge(a,b,'','dashed=1;')
p.text(40,1040,1560,40,'El frontend consume REST/STOMP; no accede a MongoDB directamente. La nube y los proveedores reales siguen pendientes de configuración y aceptación.',12)

# D16: UML deployment nodes with contained executable artifacts.
p=Page(16,'Diseño físico · diagrama de despliegue','Nodos de ejecución y artefactos. El objetivo de nube se distingue del entorno local comprobado.',1700,1150)
frame(p,25,120,795,900,'ENTORNO LOCAL')
frame(p,855,120,820,900,'«propuesto» NUBE / HTTPS')
desktop=cube(p,65,200,305,260,'«device» Computador',['Sistema operativo','Navegador web'])
mobile=cube(p,450,200,305,260,'«device» Móvil',['Sistema operativo','Navegador · observador'])
web=cube(p,65,575,305,325,'«executionEnvironment»\nServidor de aplicación',['Vite :4200','JVM / Spring Boot :8082','Whisper / IA opcionales'])
db=cube(p,450,625,305,235,'«executionEnvironment»\nServidor de datos',['MongoDB replica set',':27017 · Docker local'])
p.line(217.5,460,217.5,575,'HTTP / REST / STOMP','endArrow=none;')
p.edge(None,None,'HTTP / REST / STOMP','edgeStyle=none;endArrow=none;',pts=[(602.5,520),(300,520)],ends=[(602.5,460),(300,575)])
p.line(370,755,450,755,'MongoDB','endArrow=none;fontSize=11;')
clients=cube(p,900,200,320,260,'«device» Clientes remotos',['Navegador escritorio','Navegador móvil'])
api=cube(p,900,575,320,325,'«propuesto» Servidor web',['Frontend HTTPS','API Spring / WSS','Worker push'])
cloud_db=cube(p,1290,575,330,240,'«propuesto» Datos',['MongoDB remoto','Replica set / TLS'])
providers=cube(p,1290,200,330,260,'«external» Proveedores',['IA / transcripción','Push del navegador'])
p.line(1060,460,1060,575,'HTTPS / WSS','dashed=1;endArrow=none;')
p.line(1220,695,1290,695,'TLS','dashed=1;endArrow=none;')
p.edge(None,None,'HTTPS','edgeStyle=none;dashed=1;endArrow=none;',pts=[(1250,775),(1250,500),(1455,500)],ends=[(1220,775),(1455,460)])
p.text(40,1055,1590,45,'No se asignan Railway, Vercel, Aiven ni otro servicio de las referencias: todavía no hay una cuenta de nube configurada. IA y recepción push reales requieren pruebas.',12)

# Sequence diagrams: retain the verified messages; add execution specifications.
for n in range(19,26):
    p=byid[n];pages.append(p);s=SPECS[n-19]
    centers=[132+205*i for i in range(len(s['roles']))]
    intervals={i:[] for i in range(1,len(centers))}
    for i,m in enumerate(s['msgs']):
        a,b,*rest=m
        if b==0 or (len(m)>3 and m[3]) or a==b:continue
        start=245+i*58;stop=start+24
        for j in range(i+1,len(s['msgs'])):
            nxt=s['msgs'][j]
            if nxt[0]==b and nxt[1]==a and len(nxt)>3 and nxt[3]:stop=245+j*58;break
        intervals[b].append((start,stop))
    # UI execution spans the interaction it presents to the initiating actor.
    intervals[1]=[(245,245+(len(s['msgs'])-1)*58+22)]
    for role in range(2,len(centers)):
        if not intervals[role]:
            outgoing=[j for j,m in enumerate(s['msgs']) if m[0]==role]
            if outgoing:intervals[role]=[(245+min(outgoing)*58,245+max(outgoing)*58+22)]
    firstmsg=next(c for c in p.root if c.get('edge')=='1' and c.find("mxGeometry/mxPoint[@as='sourcePoint']") is not None and float(c.find("mxGeometry/mxPoint[@as='sourcePoint']").get('y'))>=240)
    insertion=list(p.root).index(firstmsg)
    for role,spans in intervals.items():
        merged=[]
        for a,b in sorted(spans):
            if merged and a<=merged[-1][1]:merged[-1]=(merged[-1][0],max(merged[-1][1],b))
            else:merged.append((a,b))
        for a,b in merged:
            ident=p.box(centers[role]-6,a,12,max(20,b-a),'','fillColor=#67A6A4;strokeColor=#222222;')
            cell=next(c for c in p.root if c.get('id')==ident);p.root.remove(cell);p.root.insert(insertion,cell);insertion+=1
    frame(p,20,106,p.w-40,p.h-245,'sd '+s['code'])

# Detailed use-case views: inclusion = mandatory reuse, extension = guarded behavior.
details=[
(['Verificar acceso al proyecto','Construir contexto compartido','Registrar intercambio grupal'],None),
(['Verificar acceso al proyecto','Obtener snapshot del modelo','Registrar revisión compartida'],None),
(['Verificar acceso al proyecto','Recuperar contexto disponible','Compartir resumen'],None),
(['Verificar permiso de edición','Transcribir orden de voz','Preparar y validar propuesta'],('Aplicar cambio confirmado','confirma y revisión vigente')),
(['Verificar acceso al proyecto','Recuperar documento vigente','Consultar novedades de sesión'],('Solicitar resumen a la IA','el integrante pide resumen')),
(['Verificar acceso al proyecto','Recuperar estado autoritativo','Actualizar vista informativa'],None),
(['Validar sesión de usuario','Registrar suscripción push'],('Mostrar aviso de actualización','llega push de la cuenta vinculada')),
]
analysis=[
('VistaChat',['contenido: String','modo: ASK','requestId: UUID'],['+consultar()','+mostrarRespuesta()'],'ControlConsultaIA',['+autorizar()','+construirContexto()','+registrarIntercambio()'],[('Proyecto',['id, revision','documento UML']),('MensajeIA',['projectId, requestId','autor, contenido, sequence'])]),
('VistaChat',['modo: REVIEW','revision: long','hallazgos: Lista'],['+solicitarRevision()','+mostrarHallazgos()'],'ControlRevision',['+obtenerSnapshot()','+filtrarHallazgos()','+compartirRevision()'],[('DocumentoProyecto',['schemaVersion','umlModel, layout']),('RevisionIA',['projectId, revision','hallazgos, solicitante'])]),
('VistaChat',['modo: SUMMARY_CURRENT','contenido: String'],['+pedirResumen()','+mostrarResumen()'],'ControlResumen',['+recuperarContexto()','+consultarProveedor()','+registrarRespuesta()'],[('ActividadProyecto',['projectId, actorUserId','revisionAfter, createdAt']),('MensajeIA',['projectId, sequence','tipo, contenido'])]),
('HerramientasVoz',['audio: WAV','propuesta: Comando','baseRevision: long'],['+grabarOrden()','+previsualizar()','+confirmarAplicacion()'],'ControlEdicionVoz',['+transcribirYPlanificar()','+validarPropuesta()','+aplicarSiRevisionVigente()'],[('DocumentoProyecto',['umlModel, layout','revision del agregado']),('ActividadProyecto',['operationId, actorUserId','revisionAfter, sessionId'])]),
('VistaProyecto',['projectId: UUID','revisionVista: long','novedades: Lista'],['+abrirProyecto()','+mostrarNovedades()','+registrarVisita()'],'ControlContinuidad',['+recuperarEstado()','+consultarDesdeUltimaVisita()','+actualizarVisita()'],[('VisitaProyecto',['projectId, userId','lastSeenAt, lastSeenRevision']),('SesionProyecto',['projectId, status','startRevision, endRevision'])]),
('VistaMovil',['observer: true','revision: long','estadoConexion'],['+observar()','+reconciliar()','+mostrarEstado()'],'ControlObservacion',['+autorizarLectura()','+recuperarDocumento()','+publicarOperacionConfirmada()'],[('DocumentoProyecto',['umlModel, layout','revision del agregado']),('Presencia',['projectId, userId','conexion en tiempo real'])]),
('VistaPush',['permiso: Estado','endpoint: URL','cuentaVinculada: UUID'],['+activarAvisos()','+mostrarAvisoGenerico()','+abrirProyecto()'],'ControlAvisosPush',['+registrarSuscripcion()','+encolarAviso()','+entregarConReintentos()'],[('SuscripcionPush',['userId, endpoint','p256dh, auth']),('TrabajoPush',['notificationId, subscriptionId','status, attempts, leaseUntil'])])
]
for i,s in enumerate(SPECS):
    p=Page(101+i,'Detalle · '+s['code'],s['title']+' · relaciones de inclusión y extensión justificadas.',1380,830)
    p.diagram.set('id','UC'+str(i+1));p.diagram.set('name',s['code']+' · Detalle del caso de uso')
    frame(p,25,120,1330,560,s['code']+' · SinapUML')
    actor=p.actor(110,335,'Integrante autorizado' if i!=5 else 'Integrante móvil')
    main=p.uc(425,330,340,s['code']+'\n'+s['title'])
    p.assoc(actor,main,'',style='edgeStyle=none;')
    inc,ext=details[i]
    for j,t in enumerate(inc):
        target=p.uc(975,170+j*145,310,t)
        p.edge(main,target,'«include»','dashed=1;edgeStyle=none;exitX=1;exitY=.5;entryX=0;entryY=.5;')
    if ext:
        child=p.uc(425,540,340,ext[0]);p.edge(child,main,'«extend»','dashed=1;edgeStyle=none;exitX=.5;exitY=0;entryX=.5;entryY=1;')
        p.text(55,710,1250,40,'Punto de extensión: '+ext[1]+'. La flecha extend apunta al caso base.',13)
    else:p.text(55,710,1250,40,'Precondición: sesión iniciada y proyecto accesible. Iniciar sesión no se repite como include en cada caso.',13)
    p.text(55,755,1250,35,s['foot'],12)
    ui,attrs,ops,ctrl,cops,entities=analysis[i]
    p=Page(201+i,'Análisis · '+s['code'],s['title']+' · realización de análisis: interfaz, control y entidades.',1500,1000)
    p.diagram.set('id','AC'+str(i+1));p.diagram.set('name',s['code']+' · Realización de análisis')
    frame(p,25,120,1450,730,s['code'])
    a=p.actor(80,390,'Integrante autorizado' if i!=5 else 'Integrante móvil')
    u=class3(p,270,260,290,'«boundary»\n'+ui,attrs,ops)
    c=class3(p,685,310,310,'«control»\n'+ctrl,['projectId: UUID','solicitante: UUID'],cops)
    primary=('Proyecto',['documento: DocumentoProyecto','revision: long']) if i in [3,5] else entities[0]
    e1=class3(p,1130,195,280,'«entity»\n'+primary[0],primary[1],[])
    e2=class3(p,1130,560,280,'«entity»\n'+entities[1][0],entities[1][1],[])
    p.assoc(a,u,'',style='edgeStyle=none;');p.assoc(u,c,'solicita',style='edgeStyle=none;')
    p.edge(c,e1,'consulta / valida','edgeStyle=none;');p.edge(c,e2,'consulta / registra','edgeStyle=none;')
    p.text(45,880,1400,65,'Clases y operaciones conceptuales de análisis, derivadas del flujo. Su correspondencia con los servicios del código está en la guía; no constituyen nuevas clases implementadas.',12)

# Order core views, detailed use cases, and analysis realizations.
pages.sort(key=lambda p:p.n)
def academic(p):
    for c in p.root.findall('mxCell'):
        st=c.get('style')
        if not st:continue
        st=re.sub(r'fontColor=#[0-9A-Fa-f]{6};','fontColor=#111111;',st)
        st=re.sub(r'strokeColor=#[0-9A-Fa-f]{6};','strokeColor=#333333;',st)
        if 'fillColor=#67A6A4;' not in st:
            # Preserve filled activity start/end markers and composition diamonds.
            st=re.sub(r'fillColor=#[0-9A-Fa-f]{6};','fillColor=#FFFFFF;',st)
            if 'ellipse;' in st and not c.get('value') and p.n==1:st+='fillColor=#333333;'
        if p.n==1 and 'shape=doubleEllipse;' in st:
            st+='fillColor=#FFFFFF;'
            g=c.find('mxGeometry')
            p.box(float(g.get('x'))+7,float(g.get('y'))+7,14,14,'','ellipse;fillColor=#333333;strokeColor=#333333;')
        if c.get('id') in [p.code+'-1',p.code+'-2',p.code+'-3']:
            st=st.replace('fontSize=24;','fontSize=20;')
        if c.get('id')==p.code+'-1' and p.n>100:
            c.set('value',c.get('value').replace(p.code,('AC-SP-' if p.n>200 else 'CU-SP-')+f'{p.n%100:02}',1))
        g=c.find('mxGeometry')
        if 19<=p.n<=25 and c.get('vertex')=='1' and g is not None and g.get('y')=='135':
            st+='fillColor=#B8DAD6;fontStyle=1;'
            if c.get('value') in ['Integrante','Integrante tardío','Integrante móvil','Otro integrante']:
                g.set('x',str(float(g.get('x'))+62));g.set('y','158');g.set('width','40');g.set('height','45')
                st+='shape=umlActor;fillColor=none;labelWidth=175;verticalLabelPosition=top;verticalAlign=bottom;fontStyle=0;'
            else:
                c.set('value',':'+c.get('value'))
        c.set('style',st)
    # Keep editable BCE and sequence frames; avoid re-routing deliberately straight views.
    if p.n in [15,16]:route(p)

meta=list(csv.DictReader((ROOT/'docs/formal/diagramas-xml-planificados.csv').open(encoding='utf-8-sig')))
master=ET.Element('mxfile',host='Electron',type='device');manifest=[]
for p in pages:
    academic(p)
    if p.n<=25:name=meta[p.n-1]['archivo_xml_previsto'];code=f'D{p.n:02}'
    elif p.n<200:code=f'CU-SP-{p.n-100:02}';name=code+'-detalle.xml'
    else:code=f'AC-SP-{p.n-200:02}';name=code+'-realizacion.xml'
    master.append(copy.deepcopy(p.diagram))
    single=ET.Element('mxfile',host='Electron',type='device');single.append(copy.deepcopy(p.diagram));ET.indent(single)
    ET.ElementTree(single).write(OUT/name,encoding='utf-8',xml_declaration=True)
    ids={c.get('id') for c in p.root.findall('mxCell')}
    assert len(ids)==len(p.root.findall('mxCell'))
    for c in p.root.findall('mxCell'):
        for key in ['source','target','parent']:assert c.get(key) is None or c.get(key) in ids
    manifest.append({'codigo':code,'titulo':p.diagram.get('name'),'archivo':name,'width':p.w,'height':p.h})
ET.indent(master);ET.ElementTree(master).write(OUT/'SinapUML-PUDS-Academico-V2.drawio',encoding='utf-8',xml_declaration=True)
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
mapping=['ProjectAssistantService.send(ASK), ProjectAssistantContextService, ProjectAssistantMessageStore','ProjectAssistantService.send(REVIEW), validFindings, AssistantReview','ProjectAssistantService.send(SUMMARY_CURRENT), ProjectAssistantContextService','ProjectTools.vue, AssistantVoiceService.plan, AssistantPlanService.planVoice, colaboración','ProjectContinuityService, ProjectSessionService, ProjectService','editor-sync.ts, API de proyecto, presencia STOMP, modo observer','PushSubscriptionService, PushDeliveryService, service worker']
readme='''# SinapUML · Diagramas académicos V2

Nueva versión basada en las siete capturas proporcionadas por el estudiante. Conserva la versión anterior y el Word V4. Fecha: 9 de noviembre de 2026.

## Uso

Abrir `SinapUML-PUDS-Academico-V2.drawio` en draw.io Desktop mediante Archivo → Abrir. Contiene 39 pestañas: 25 vistas D01–D25, siete detalles CU-SP y siete realizaciones de análisis AC-SP. También hay XML individuales y exportaciones PNG/SVG. `index.html` es una galería local.

Los códigos D01–D25 mantienen su correspondencia con las reservas del Word. Los detalles CU-SP corresponden a las fichas de 4.3; AC-SP amplía las realizaciones del capítulo de análisis. Para incorporar estas vistas adicionales hay que añadir sus figuras e índice en una siguiente versión del Word.

## Criterios aplicados de las referencias

- Presentación académica sobria, fondo blanco y marcos identificados por caso de uso.
- Casos de uso con actores, include y extend únicamente cuando la semántica del flujo lo justifica. La autenticación existente se trata como precondición; no se inventan roles de administrador, vendedor o cliente.
- Comunicación con símbolos boundary, control y entity, mensajes próximos a sus enlaces y dirección indicada en el texto. Las operaciones son abstracciones de análisis, no nombres nuevos de endpoints.
- Realizaciones de análisis en tres compartimentos, separando datos y operaciones de interfaz/control. No se atribuyen métodos CRUD ficticios a las entidades.
- Arquitectura lógica en capas; despliegue con nodos tridimensionales y artefactos contenidos.
- Secuencias con líneas de vida, mensajes, retornos, fragmentos alternativos y barras de activación. Las barras indican ejecución conceptual; no representan hilos medidos en runtime.

La tecnología sigue siendo Vue, Java/Spring Boot y MongoDB. No se copian PostgreSQL, Prisma, Node backend, Railway, Aiven ni Vercel de las capturas. La nube es propuesta; Gemini no está integrado; voz/IA reales y recepción push física siguen pendientes. El modo móvil no es un rol VIEWER persistido. Las propuestas de voz se devuelven al solicitante; se comparte el cambio confirmado, y la difusión completa de la propuesta de voz necesita verificación.

## Correspondencia del análisis con la implementación

Los controles de AC-SP son abstracciones para la documentación PUDS y no clases adicionales implementadas. Su responsabilidad se distribuye en:

'''
for i,text in enumerate(mapping,1):readme+=f'- AC-SP-{i:02}: {text}.\n'
readme+='''
## Edición y mantenimiento

Los XML individuales y el maestro son copias independientes, sin sincronización automática. Guardar una copia antes de modificar. El constructor `scripts/build-puds-drawio-v2.py` regenera su carpeta y puede reemplazar ediciones manuales. Exportar con `scripts/export-puds-drawio.ps1 -DiagramDirectory docs/formal/diagramas-drawio-v2`. Los diagramas extensos requieren página completa o sección horizontal en Word; no reducirlos a un espacio donde sus textos queden ilegibles.

Las referencias orientan notación y estructura. No acreditan que el docente haya validado estos nuevos modelos ni sustituyen pruebas reales de la aplicación.
'''
(OUT/'README.md').write_text(readme,encoding='utf-8')
cards=[]
for item in manifest:
    stem=Path(item['archivo']).stem;t=html.escape(item['titulo'])
    cards.append(f'<article><h2>{t}</h2><a href="svg/{stem}.svg"><img loading="lazy" src="png/{stem}.png" alt="{t}"></a><p><a href="{stem}.xml" download>XML editable</a> · <a href="svg/{stem}.svg">SVG</a> · <a href="png/{stem}.png">PNG</a></p></article>')
(OUT/'index.html').write_text('''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SinapUML · PUDS académico V2</title><style>body{font:16px/1.5 Arial,sans-serif;color:#111;background:#f2f2f2;margin:0}header,main{max-width:1400px;margin:auto;padding:28px}article{background:white;border:1px solid #ccc;padding:20px;margin:0 0 25px}h1{font-size:30px}h2{font-size:19px}img{display:block;width:100%;max-height:950px;object-fit:contain;object-position:top}a{color:#245382}</style><header><h1>SinapUML · Diagramas PUDS académicos V2</h1><p>39 vistas editables: 25 diagramas principales, siete detalles de caso de uso y siete realizaciones de análisis.</p><p><a href="SinapUML-PUDS-Academico-V2.drawio" download>Maestro draw.io</a> · <a href="README.md">Guía y alcance</a></p></header><main>'''+''.join(cards)+'</main></html>',encoding='utf-8')
print(json.dumps({'pages':len(pages),'output':str(OUT)},ensure_ascii=False))
