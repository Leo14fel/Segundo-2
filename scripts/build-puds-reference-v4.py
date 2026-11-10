from pathlib import Path
import xml.etree.ElementTree as E,copy,json,html,csv
R=Path(__file__).resolve().parents[1]
src=R/'scripts/build-puds-drawio-v2.py';code=src.read_text(encoding='utf8').split("master=ET.Element('mxfile'")[0]
# Execute the model definitions only; isolate output path from every prior deliverable.
code=code.replace("OUT=ROOT/'docs/formal/diagramas-drawio-v2'","OUT=ROOT/'docs/formal/diagramas-revision-referencias-v4'")
c={'__file__':str(src),'__name__':'reference_revision'};exec(compile(code,str(src),'exec'),c)
pages=c['pages'];Page=c['Page'];S=c['SPECS'];out=c['OUT'];academic=c['academic']
# References use folder packages, cube nodes and compartmental analysis classes.
# Keep detailed V2 realizations instead of the rejected compact V3 summaries.
selected=[p for p in pages if p.n in list(range(4,26)) or p.n>=200]
# Rebuild communications with separate context, message, access and delivery responsibilities.
for p in list(selected):
 if 7<=p.n<=13:selected.remove(p)
for i,s in enumerate(S):
 p=Page(i+7,'Comunicación detallada · '+s['code'],'Objetos de análisis; mensajes numerados y responsabilidades separadas.',1450,1030)
 actor=p.actor(45,440,'Integrante móvil' if i==5 else 'Integrante')
 ui=c['bce'](p,300,435,'boundary',c['COMM'][i][0])
 ctrl=c['bce'](p,710,435,'control',c['COMM'][i][1])
 access=c['bce'](p,1080,155,'control','Acceso al proyecto')
 ent=c['bce'](p,1080,435,'entity',c['COMM'][i][2])
 ext=p.box(1020,740,250,65,'«external»\n'+c['COMM'][i][3],'fillColor=#FFFFFF;')
 other=c['bce'](p,380,745,'boundary','Service worker' if i==6 else 'Clientes del proyecto')
 link=c['message_link'];data=c['COMM'][i]
 link(p,actor,ui,data[4],85,345,210,85)
 link(p,ui,ctrl,data[5],370,325,310,100)
 link(p,ctrl,access,['1.1.1 VerificarIdentidad() →','1.1.2 ComprobarMembresía() →','← 1.1.3 AccesoAutorizado()'],760,180,290,110)
 link(p,ctrl,ent,data[6],805,345,255,85)
 link(p,ctrl,ext,data[7],825,640,290,95)
 link(p,ext if i==6 else ctrl,other,data[8],475,655,330,80)
 p.text(45,935,1350,55,'Alternativa: '+s['alt'][0]+'. '+s['foot'],13)
 selected.append(p)
selected.sort(key=lambda p:p.n)
master=E.Element('mxfile',host='Electron',type='device');manifest=[]
for p in selected:
 academic(p)
 code=f'D{p.n:02}' if p.n<200 else f'AC-SP-{p.n-200:02}'
 p.diagram.set('id',code);p.diagram.set('name',code+' · '+p.diagram.get('name').split(' · ',1)[-1])
 # Adopt the package-folder convention of the supplied package reference.
 if p.n in [4,5,6]:
  for cell in p.root.findall('mxCell'):
   st=cell.get('style','')
   if 'swimlane;' in st:cell.set('style',st+'shape=folder;tabWidth=65;tabHeight=20;tabPosition=left;')
 ids={x.get('id') for x in p.root.findall('mxCell')}
 for x in p.root.findall('mxCell'):
  for k in ['source','target','parent']:assert x.get(k) is None or x.get(k) in ids
 single=E.Element('mxfile',host='Electron');single.append(copy.deepcopy(p.diagram));E.indent(single)
 E.ElementTree(single).write(out/(code+'.xml'),encoding='utf8',xml_declaration=True)
 master.append(copy.deepcopy(p.diagram));manifest.append({'codigo':code,'archivo':code+'.xml','estado':'Borrador detallado para revisión conjunta'})
E.indent(master);E.ElementTree(master).write(out/'SinapUML-Revision-Referencias-V4.drawio',encoding='utf8',xml_declaration=True)
(out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
(out/'README.md').write_text('''# Revisión con referencias editables V4

Abrir SinapUML-Revision-Referencias-V4.drawio. Borradores para revisión conjunta; no insertados en Word.

Se usan como referencia los cuatro archivos aportados el 10 de noviembre: paquetes con responsabilidades, comunicación con objetos y mensajes, despliegue con nodos y análisis con tres compartimentos. No se trasladan actores, entidades comerciales o infraestructura del otro proyecto.

Esta revisión recupera el detalle de las realizaciones académicas V2 frente a los resúmenes compactos V3. Reconstruye las siete comunicaciones incorporando acceso al proyecto como responsabilidad explícita. Los controles son abstracciones de análisis: no representan clases adicionales implementadas. Las comunicaciones incluyen mensajes de respuesta y condiciones alternativas. AC-SP contiene atributos y operaciones; D14 es el dominio, no el esquema físico. D19–D25 conservan secuencias detalladas con activaciones y alternativas.

Revisar primero D07 y AC-SP-01 para acordar el nivel de detalle. Después continuar D08–D13, dominio y secuencias. La revisión de notación y distribución visual sigue pendiente; no se declara este paquete aprobado. V8 y los casos de uso aprobados permanecen intactos.

Para Word: no reducir una vista extensa completa hasta volver ilegible el texto. Dividirla por escenario, repetir participantes y usar figuras proporcionales de hasta 16 × 11.3 cm en A4. Las vistas de este archivo son lienzos de trabajo, no exportaciones finales para insertar.

Nube propuesta, IA real y recepción push siguen pendientes de aceptación. No se introduce un rol VIEWER ni integración Gemini ficticia.
''',encoding='utf8')
print(json.dumps({'vistas':len(manifest),'maestro':str(out/'SinapUML-Revision-Referencias-V4.drawio')},ensure_ascii=False))
