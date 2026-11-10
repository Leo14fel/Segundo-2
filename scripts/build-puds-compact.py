"""Editable A4 review diagrams. Preserves V1/V2; back up manual V3 edits before running."""
from pathlib import Path
import ast,copy,html,json,math,csv,re,xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1];OUT=R/'docs/formal/diagramas-drawio-v3-compactos';OUT.mkdir(exist_ok=True)
def assignment(path,name):
    tree=ast.parse(path.read_text(encoding='utf-8-sig'))
    n=next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets))
    return eval(compile(ast.Expression(n.value),str(path),'eval'),{'dict':dict})
S=assignment(R/'scripts/build-puds-drawio.py','SPECS')
COL=assignment(R/'scripts/build-puds-drawio.py','collections')
AN=assignment(R/'scripts/build-puds-drawio-v2.py','analysis')
DETAIL=assignment(R/'scripts/build-puds-drawio-v2.py','details')
M={v['codigo']:v for v in json.loads((R/'docs/formal/diagramas-drawio-v2/manifest.json').read_text(encoding='utf-8'))}
pages=[]
BASE='html=1;whiteSpace=wrap;fontFamily=Arial;fontSize=14;fontColor=#111111;strokeColor=#333333;strokeWidth=1;fillColor=#FFFFFF;'
class Page:
    def __init__(self,code,title,part=1):
        self.code=code;self.part=part;self.id=code+('-'+str(part) if part>1 else '');self.i=0;self.title=title
        self.d=E.Element('diagram',id=self.id,name=code+' · '+title+(f' · {part}' if part>1 else ''))
        self.g=E.SubElement(self.d,'mxGraphModel',dx='680',dy='480',grid='1',gridSize='10',guides='1',page='1',pageScale='1',pageWidth='680',pageHeight='480',math='0',shadow='0')
        self.root=E.SubElement(self.g,'root');E.SubElement(self.root,'mxCell',id='0');E.SubElement(self.root,'mxCell',id='1',parent='0');pages.append(self)
    def key(self):self.i+=1;return self.id+'-'+str(self.i)
    def box(self,x,y,w,h,t='',style=''):
        id=self.key();c=E.SubElement(self.root,'mxCell',id=id,value=html.escape(t).replace('\n','<br>'),style=BASE+style,vertex='1',parent='1')
        E.SubElement(c,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),**{'as':'geometry'});return id
    def text(self,x,y,w,h,t,bold=False):return self.box(x,y,w,h,t,'text;strokeColor=none;fillColor=#FFFFFF;align=left;spacing=0;'+('fontStyle=1;' if bold else ''))
    def edge(self,a,b,t='',style='',points=None,ends=None):
        multiplicity=t.split(' / ') if re.fullmatch(r'[0-9.*]+ / [0-9.*]+',t) else None
        if multiplicity:t=''
        id=self.key();v=dict(id=id,value=html.escape(t).replace('\n','<br>'),style=BASE+'edgeStyle=orthogonalEdgeStyle;rounded=0;endArrow=open;endFill=0;labelBackgroundColor=#FFFFFF;'+style,edge='1',parent='1')
        if a:v['source']=a
        if b:v['target']=b
        c=E.SubElement(self.root,'mxCell',**v);g=E.SubElement(c,'mxGeometry',relative='1',**{'as':'geometry'})
        if points:
            ar=E.SubElement(g,'Array',**{'as':'points'})
            for x,y in points:E.SubElement(ar,'mxPoint',x=str(x),y=str(y))
        if ends:
            for role,(x,y) in zip(['sourcePoint','targetPoint'],ends):E.SubElement(g,'mxPoint',x=str(x),y=str(y),**{'as':role})
        if multiplicity:
            for x,val in zip([-.65,.65],multiplicity):
                label=E.SubElement(self.root,'mxCell',id=self.key(),value=val,style='edgeLabel;html=1;align=center;fontFamily=Arial;fontSize=14;labelBackgroundColor=#FFFFFF;',vertex='1',connectable='0',parent=id)
                geo=E.SubElement(label,'mxGeometry',x=str(x),y='-1',width='28',height='20',relative='1',**{'as':'geometry'});E.SubElement(geo,'mxPoint',x='0',y='-12',**{'as':'offset'})
        return id
    def line(self,x,y,xx,yy,t='',style=''):return self.edge(None,None,t,'edgeStyle=none;'+style,ends=[(x,y),(xx,yy)])
    def actor(self,x,y,t):return self.box(x,y,36,56,t,'shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;labelWidth=100;')
    def uc(self,x,y,w,t):return self.box(x,y,w,52,t,'ellipse;spacing=3;')
    def klass(self,x,y,w,title,attrs,ops=None):
        h=44+22*len(attrs)+(30+22*len(ops) if ops else 8)
        c=self.box(x,y,w,h,'');self.text(x+4,y+2,w-8,40,title,True);self.line(x,y+44,x+w,y+44,style='endArrow=none;')
        self.text(x+7,y+48,w-14,22*len(attrs),'\n'.join(attrs))
        if ops:
            cut=y+48+22*len(attrs);self.line(x,cut,x+w,cut,style='endArrow=none;');self.text(x+7,cut+5,w-14,22*len(ops),'\n'.join(ops))
        return c
    def bce(self,x,y,kind,name):
        c=self.box(x,y,40,40,'','ellipse;')
        if kind=='boundary':self.line(x-8,y-4,x-8,y+44,style='endArrow=none;');self.line(x-8,y+20,x,y+20,style='endArrow=none;')
        elif kind=='control':self.line(x+4,y-6,x+28,y-6,style='endArrow=open;');self.line(x+4,y-6,x+4,y+4,style='endArrow=none;')
        else:self.line(x-2,y+48,x+42,y+48,style='endArrow=none;')
        self.text(x-60,y-100 if kind=='control' else y-56 if kind=='entity' else y+56,160,46,'«'+kind+'»\n'+name);return c

# Activity: compact decision structure, no large explanatory note inside the figure.
p=Page('D01','Actividad colaborativa');start=p.box(315,10,18,18,'','ellipse;fillColor=#333333;')
a=p.box(220,40,210,40,'Recuperar proyecto');merge=p.box(318,93,16,16,'','rhombus;');b=p.box(220,135,210,40,'Modelar o consultar al equipo')
c=p.box(265,185,120,64,'¿Solicita IA?','rhombus;');q=p.box(30,195,175,54,'Consultar / revisar /\nresumir / proponer')
v=p.box(230,285,190,54,'Validar cambio y revisión\nConfirmar si es propuesta')
save=p.box(230,382,190,50,'Persistir y compartir\ncambio confirmado');end=p.box(554,392,25,25,'','ellipse;');p.box(560,398,13,13,'','ellipse;fillColor=#333333;')
for x,y in [(start,a),(a,merge),(merge,b),(b,c)]:p.edge(x,y)
p.edge(c,q,'[sí]');p.edge(q,v,'[edición confirmada]',points=[(117,312)]);p.edge(c,v,'[no: edición manual]');p.edge(v,save,'[válido]')
p.edge(q,merge,'[solo respuesta]','edgeStyle=none;exitX=.5;exitY=0;entryX=0;entryY=.5;',points=[(117,101)])
p.edge(v,merge,'[conflicto]','edgeStyle=none;exitX=1;exitY=.5;entryX=1;entryY=.5;',points=[(470,312),(470,101)])
p.edge(save,merge,'[continuar]','edgeStyle=none;exitX=1;exitY=.5;entryX=1;entryY=.5;',points=[(510,407),(510,101)]);p.edge(save,end,'[pausar]')

p=Page('D02','Actores');general=p.actor(310,55,'Integrante autorizado')
general_cell=next(c for c in p.root if c.get('id')==general);general_cell.set('style',general_cell.get('style')+'verticalLabelPosition=top;verticalAlign=bottom;')
for x,t in [(120,'Propietario'),(310,'Colaborador EDITOR')]:
    a=p.actor(x,180,t);p.edge(a,general,'','endArrow=block;endFill=0;',points=[(x+18,135),(328,135)])
p.actor(20,30,'Visitante');p.actor(500,180,'Integrante móvil')
p.text(445,270,210,55,'Modo de interfaz; no es\nun permiso VIEWER.')
for i,t in enumerate(['Proveedor IA','Transcripción','Proveedor push']):p.box(30+i*220,370,190,60,'«actor externo»\n'+t)

# General scope separated into inherited and second-partial capabilities.
for part,items in [(1,['Registrarse e iniciar sesión','Gestionar proyectos y acceso','Modelar guardar y validar','Colaborar y ver presencia','Importar exportar y generar']),(2,[s['code']+'\n'+s['title'] for s in S])]:
    p=Page('D03','Casos de uso '+('base' if part==1 else 'segundo parcial'),part)
    p.box(160,15,385,450,'','fillColor=none;');p.text(175,17,340,25,'SinapUML',True)
    a=p.actor(60,210,'Usuario' if part==1 else 'Integrante');ys=[62+j*(72 if part==1 else 57) for j in range(len(items))]
    for i,(t,y) in enumerate(zip(items,ys)):
        u=p.uc(230,y,265,t);p.edge(a,u,'','edgeStyle=none;endArrow=none;exitX=1;exitY=.5;entryX=0;entryY=.5;')
    p.text(550,55,115,370,'Vista de alcance.\n\nLos actores técnicos se detallan por caso.\n\nEl visitante participa en registro e inicio; el propietario administra acceso.' if part==1 else 'IA: SP-01 a 04\n\nVoz: SP-04\n\nMóvil: SP-06\n\nPush: SP-07')

pk=['Identidad y acceso','Proyecto y validación','Colaboración','Asistente','Actividad y sesiones','Interoperabilidad','Push']
p=Page('D04','Paquetes de análisis')
for i,t in enumerate(pk):p.box(30+(i%3)*215,30+(i//3)*140,190,90,t,'shape=folder;tabWidth=65;tabHeight=16;spacingTop=18;')
p=Page('D05','Dependencias de paquetes');nodes={}
coords=[(245,15),(245,175),(245,350),(15,175),(15,350),(465,175),(465,350)]
for t,(x,y) in zip(pk,coords):nodes[t]=p.box(x,y,190,70,t,'shape=folder;tabHeight=15;spacingTop=15;')
for a,b,points,ports in [
    (3,0,[(110,110),(340,110)],'exitX=.5;exitY=0;entryX=.5;entryY=1;'),
    (2,0,[(455,385),(455,50)],'exitX=1;exitY=.5;entryX=1;entryY=.5;'),
    (2,1,None,'exitX=.5;exitY=0;entryX=.5;entryY=1;'),
    (3,1,None,'exitX=1;exitY=.5;entryX=0;entryY=.5;'),
    (5,1,None,'exitX=0;exitY=.5;entryX=1;entryY=.5;'),
    (1,4,[(230,210),(230,385)],'exitX=0;exitY=.5;entryX=1;entryY=.5;'),
    (4,6,[(110,455),(560,455)],'exitX=.5;exitY=1;entryX=.5;entryY=1;')]:p.edge(nodes[pk[a]],nodes[pk[b]],'','edgeStyle=none;dashed=1;'+ports,points=points)
p=Page('D06','Casos de uso por responsabilidad')
for x,y,name,txt in [(20,20,'Asistente','SP-01 Consultar\nSP-02 Revisar\nSP-03 Resumir\nSP-04 Proponer por voz'),(355,20,'Colaboración','SP-04 Confirmar cambio\nSP-06 Observar'),(20,260,'Actividad y sesiones','SP-05 Retomar sesión'),(355,260,'Push','SP-07 Avisar actualización')]:
    p.box(x,y,305,185,'','shape=folder;tabWidth=100;tabHeight=18;');p.text(x+12,y+28,280,28,name,True);p.text(x+12,y+68,280,100,txt)

for i,s in enumerate(S):
    ui,attrs,ops,ctrl,cops,entities=AN[i];c='D'+str(i+7).zfill(2);p=Page(c,s['title'])
    a=p.actor(20,200,'Integrante');u=p.bce(155,207,'boundary',ui);k=p.bce(355,207,'control',ctrl)
    e=p.bce(565,62,'entity',entities[0][0] if i!=6 else 'Suscripción / trabajos')
    other=p.bce(355,325,'boundary','Otros clientes' if i!=6 else 'Service worker') if i!=4 else None
    ext=p.actor(565,315,'Otro integrante') if i==5 else p.box(535,315,125,60,'Proveedor IA' if i in [0,1,2] else ['Voz / IA','Asistente','Otro integrante','Proveedor push'][i-3])
    p.edge(a,u,'','edgeStyle=none;endArrow=none;');p.text(65,155,150,42,'1. Grabar →\n2. Confirmar →' if i==3 else '1. Solicitar →')
    p.edge(u,k,'','edgeStyle=none;endArrow=none;');p.text(208,178,140,44,'1.1 Planificar →\n2.1 Aplicar →' if i==3 else '1.1 Coordinar →')
    p.edge(k,e,'','edgeStyle=none;endArrow=none;',points=[(485,167)]);p.text(445,170,215,44,'1.2 Leer →\n2.2 Persistir →' if i==3 else '1.2 Leer / registrar →')
    p.edge(k,ext,'','edgeStyle=none;endArrow=none;',points=[(490,280)]);p.text(450,250,215,44,'[opcional] Resumen →' if i==4 else '1.3 Transcribir →' if i==3 else '2. Cambio autorizado ←' if i==5 else '1.3 Consultar / enviar →')
    if other:
        p.edge(k,other,'','edgeStyle=none;endArrow=none;');p.text(205,335,140,44,'2.3 Propagar confirmado ↓' if i==3 else '1.4 Compartir ↓')
    # Detail use case: keep only mandatory reused behavior and guarded extensions.
    p=Page(s['code'],s['title']);p.box(135,10,530,460,'','fillColor=none;');p.text(150,14,480,24,'SinapUML',True)
    a=p.actor(35,190,'Integrante');main=p.box(165,180,215,70,s['code']+'\n'+s['title'],'ellipse;spacing=3;');p.edge(a,main,'','endArrow=none;')
    includes,extn=DETAIL[i]
    for j,t in enumerate(includes):
        uc=p.uc(445,65+j*100,200,t);p.edge(main,uc,'«include»','dashed=1;edgeStyle=none;')
    if extn:
        uc=p.uc(165,370,250,extn[0]);p.edge(uc,main,'«extend»','dashed=1;');p.text(440,380,200,55,'Condición: '+extn[1])
    p=Page('AC-SP-'+str(i+1).zfill(2),s['title'])
    a=p.actor(10,82,'Integrante');u=p.klass(90,20,225,'«boundary»\n'+ui,attrs,ops);k=p.klass(390,20,260,'«control»\n'+ctrl,['projectId, solicitante'],cops)
    en=[p.klass(90+j*300,285,225,'«entity»\n'+name,vals[:2]) for j,(name,vals) in enumerate(entities)]
    p.edge(a,u,'','endArrow=none;');p.edge(u,k,'solicita','endArrow=none;');p.edge(k,en[0],'consulta',points=[(345,240),(202,240)]);p.edge(k,en[1],'registra')

# Domain: separate the project aggregate from the UML edited by the user.
p=Page('D14','Dominio del proyecto')
a=p.klass(20,30,185,'Usuario',['id, nombre, email']);b=p.klass(255,30,190,'Proyecto',['id, ownerId, revision']);c=p.klass(255,250,190,'DocumentoProyecto',['schemaVersion','umlModel, layout']);m=p.klass(20,250,185,'Membresía',['projectId, userId','rol: EDITOR']);msg=p.klass(495,30,165,'MensajeIA',['projectId, sequence','rol, contenido'])
p.edge(a,b,'','endArrow=none;');p.edge(a,m,'1 / 0..*','endArrow=none;');p.edge(b,m,'1 / 0..*','edgeStyle=none;endArrow=none;exitX=0;exitY=.9;entryX=1;entryY=.5;',points=[(230,110),(230,290)]);p.edge(b,c,'1 / 1','endArrow=none;startArrow=diamond;startFill=1;');p.edge(b,msg,'1 / 0..*','endArrow=none;')
p=Page('D14','Dominio del modelo UML',2)
a=p.klass(20,25,190,'ModeloUML',['clases, relaciones']);b=p.klass(255,25,190,'ClaseUML',['id, nombre']);c=p.klass(490,25,170,'AtributoUML',['nombre, tipo']);o=p.klass(255,245,190,'OperaciónUML',['nombre, retorno']);param=p.klass(490,245,170,'ParámetroUML',['nombre, tipo']);rel=p.klass(20,245,190,'RelaciónUML',['origenId, destinoId','tipo, multiplicidad'])
for x,y in [(a,b),(b,c),(b,o),(o,param),(a,rel)]:p.edge(x,y,'1 / 0..*','endArrow=none;startArrow=diamond;startFill=1;')
p.edge(rel,b,'extremos','endArrow=none;',points=[(235,375),(465,375),(465,185)])

p=Page('D15','Arquitectura lógica')
for i,(name,content) in enumerate([('Presentación','Pizarra UML   |   Chat y voz   |   Móvil'),('Aplicación','Proyecto   |   Asistente   |   Colaboración'),('Dominio y adaptadores','Reglas UML   |   Repositorios   |   IA y push'),('Infraestructura','Vue   |   Spring Boot   |   MongoDB')]):
    y=20+i*110;p.box(20,y,640,80,'');p.text(32,y+5,600,25,name,True);p.text(32,y+37,600,32,content)
    if i<3:p.line(340,y+80,340,y+110)
for part,cloud in [(1,False),(2,True)]:
    p=Page('D16','Despliegue '+('propuesto en nube' if cloud else 'local'),part)
    web=p.box(205,15,270,90,'«device» Navegador\nEscritorio / móvil','shape=cube;size=10;')
    app=p.box(205,180,270,100,'«executionEnvironment»\n'+('Frontend HTTPS / API WSS' if cloud else 'Vite :4200 / Spring :8082'),'shape=cube;size=10;')
    db=p.box(20,365,260,85,'«executionEnvironment»\nMongoDB replica set'+('\nRemoto por configurar' if cloud else ' :27017'),'shape=cube;size=10;')
    ai=p.box(390,365,270,85,'«external» IA / voz / push\n'+('Proveedor por configurar' if cloud else 'Runtimes opcionales'),'shape=cube;size=10;')
    p.edge(web,app,'HTTPS / WSS' if cloud else 'HTTP / REST / STOMP','dashed=1;' if cloud else '')
    p.edge(app,db,'TLS' if cloud else 'MongoDB');p.edge(app,ai,'HTTPS' if cloud else 'HTTP')
p=Page('D17','Modelo lógico documental')
a=p.klass(245,20,200,'Proyecto',['id, ownerId, revision']);doc=p.klass(245,195,200,'Documento embebido',['umlModel, layout']);p.edge(a,doc,'1 / 1','startArrow=diamond;startFill=1;endArrow=none;')
for x,y,name,t in [(20,20,'Identidad','Usuario, membresía'),(470,20,'Conversación','Mensajes IA'),(20,345,'Continuidad','Actividad, sesión, visita'),(470,345,'Notificaciones','Aviso, suscripción, trabajo')]:
    c=p.klass(x,y,190,name,[t])
    points=([(230,382),(230,57)] if x==20 else [(460,382),(460,57)]) if y>100 else None
    ports=('exitX=1;exitY=.5;entryX=0;entryY=.5;' if x==20 else 'exitX=0;exitY=.5;entryX=1;entryY=.5;')
    p.edge(c,a,'','edgeStyle=none;dashed=1;'+ports,points=points)
p.text(15,135,200,32,'Referencias por projectId')
for part in range(3):
    p=Page('D18','Colecciones MongoDB',part+1)
    for j,(name,attrs) in enumerate(COL[part*4:part*4+4]):p.klass(15+(j%2)*335,20+(j//2)*230,320,name,attrs)

# Sequence labels share the row, never stack multiple messages on one line.
for i,s in enumerate(S):
    guards=['audio inválido / planificación rechazada','revisión obsoleta al confirmar'] if i==3 else [s['alt'][0]]*len(s['alt'][1])
    allrows=[('principal',str(j+1),m) for j,m in enumerate(s['msgs'])]+[(guards[j],'A'+str(j+1),m) for j,m in enumerate(s['alt'][1])]
    chunks=[allrows[j:j+7] for j in range(0,len(allrows),7)]
    for part,chunk in enumerate(chunks,1):
        p=Page('D'+str(19+i).zfill(2),s['code']+' secuencia',part)
        xs=[40+j*600/(len(s['roles'])-1) for j in range(len(s['roles']))]
        rows=[];offset=0;prior=None
        for row,(guard,num,m) in enumerate(chunk):
            base=136+row*45
            changed=guard!=prior and guard!='principal'
            if changed:offset+=24
            rows.append((base+offset,guard,num,m,changed));prior=guard
        line_end=rows[-1][0]+25
        for j,(x,role) in enumerate(zip(xs,s['roles'])):
            if j==0:p.actor(x-18,12,'Móvil' if i==5 else 'Integrante')
            else:p.box(x-40,10,80,63,role,'fillColor=#EAF1F1;spacing=2;')
            p.line(x,91,x,line_end,style='dashed=1;endArrow=none;')
        for y,guard,num,m,changed in rows:
            a,b,t,*ret=m;xa,xb=xs[a],xs[b]
            if changed:p.text(10,y-62,655,22,'['+guard+']',True)
            dashed=bool(ret and ret[0]);style='dashed=1;endArrow=open;' if dashed else 'endArrow=block;endFill=1;'
            if a==b:p.edge(None,None,'',style+'edgeStyle=none;',points=[(xa+25,y),(xa+25,y+15)],ends=[(xa,y),(xa,y+15)])
            else:p.line(xa,y,xb,y,style=style)
            width=min(410,max(220,abs(xb-xa)-10));left=max(5,min(675-width,(xa+xb-width)/2))
            p.text(left,y-38,width,34,num+'. '+t)
            if not dashed and b>0:p.box(xb-3,y,6,14,'','fillColor=#8CBDB8;')

# Sources are independent editable XMLs; the master is a convenience copy.
manifest=[];master=E.Element('mxfile',host='Electron',type='device')
for p in pages:
    name=p.code+('-parte-'+str(p.part) if sum(x.code==p.code for x in pages)>1 else '')+'.xml'
    root=E.Element('mxfile',host='Electron',type='device');root.append(copy.deepcopy(p.d));E.indent(root)
    E.ElementTree(root).write(OUT/name,encoding='utf-8',xml_declaration=True);master.append(copy.deepcopy(p.d))
    manifest.append({'codigo':p.code,'parte':p.part,'titulo':p.title,'archivo':name,'ancho_cm':16,'alto_max_cm':11.3,'ancho_lienzo':680,'alto_lienzo':480,'letra_objetivo_pt':9,'estado':'Pendiente de corrección del estudiante'})
E.indent(master);E.ElementTree(master).write(OUT/'SinapUML-PUDS-Compactos-V3.drawio',encoding='utf-8',xml_declaration=True)
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
with (OUT/'control-revision.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['Código','Parte','Archivo editable','Revisado por estudiante','Cambios solicitados','Listo para insertar'])
    for m in manifest:w.writerow([m['codigo'],m['parte'],m['archivo'],'No','','No'])
notes='\n\n'.join(s['code']+': '+s['foot'] for s in S)
(OUT/'README.md').write_text('''# SinapUML diagramas compactos para corregir

Abrir SinapUML-PUDS-Compactos-V3.drawio. Son borradores de revisión, no modelos aprobados. Las versiones anteriores quedan intactas. Trabajar sobre una copia del maestro y devolver el .drawio corregido; los XML individuales son copias independientes.

Se redibujaron vistas para un ancho máximo de 16 cm y alto aproximado de hasta 11.3 cm. La tipografía base es 14 unidades, equivalente a unos 9 puntos al imprimir el lienzo completo. No reducir más la figura: separar contenido si se agregan elementos. Las secuencias, dominio, alcance, despliegue y colecciones tienen partes independientes para evitar imágenes gigantes. No es necesario insertar todas las vistas: elegir las requeridas por el docente y las fichas.

Los títulos, fuentes y notas largas deben ir como pies y párrafos del documento, fuera de las imágenes. En PNG/SVG exportar solo la página elegida, fondo blanco y recorte al contenido. Conservar proporciones y usar En línea con el texto en Word. No estirar al ancho figuras con pocos elementos.

Completar control-revision.csv. Mantener los códigos para que pueda incorporar tus correcciones en las reservas D01–D25. CU-SP corresponde a las fichas de 4.3; AC-SP a análisis en 5.3. Las continuaciones repiten participantes; la numeración de mensajes continúa entre partes. Las comunicaciones son síntesis de análisis y las secuencias conservan los mensajes detallados. Los diagramas de colecciones seleccionan campos e índices; no son un diccionario exhaustivo.

Corregir primero D03, un CU-SP, su AC-SP, su comunicación y secuencia para acordar la notación. Revisar el texto al tamaño de impresión en la galería index.html. Una imagen pequeña a escala de página debe seguir siendo legible.

La nube se presenta como propuesta, el modo móvil no es un rol VIEWER y las clases de análisis son conceptuales. No se implementaron nuevas capacidades al redibujar. Límites de los casos:

'''+notes,encoding='utf-8')
cards=[]
for m in manifest:
    stem=Path(m['archivo']).stem;title=html.escape(m['codigo']+' · '+m['titulo']+' · parte '+str(m['parte']))
    cards.append(f'<article><h2>{title}</h2><img src="png/{stem}.png" alt="{title}"><p><a href="{m["archivo"]}">XML editable</a> · <a href="svg/{stem}.svg">SVG</a></p></article>')
(OUT/'index.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><title>SinapUML revisión A4</title><style>body{font:15px Arial;background:#eee}main{max-width:900px;margin:auto}article{background:white;padding:20px;margin:20px 0}h2{font-size:17px}img{display:block;width:auto;max-width:16cm;max-height:11.3cm;border:1px solid #ddd}@media print{article{break-inside:avoid;background:white}body{background:white}}</style><main><h1>Diagramas compactos para A4</h1><p>Imprimir al 100 % para comprobar legibilidad. Borradores pendientes de corrección.</p>'+''.join(cards)+'</main></html>',encoding='utf-8')
print(json.dumps({'logical_diagrams':len(set(m['codigo'] for m in manifest)),'sheets':len(manifest),'out':str(OUT)},ensure_ascii=False))
