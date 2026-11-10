import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
const {Client}=createRequire(import.meta.url)('../frontend/node_modules/@stomp/stompjs');

const base=process.env.SINAPUML_TEST_BASE_URL??'http://127.0.0.1:4200';
const email=process.env.SINAPUML_TEST_EMAIL,password=process.env.SINAPUML_TEST_PASSWORD;
if(!email||!password)throw new Error('Define SINAPUML_TEST_EMAIL y SINAPUML_TEST_PASSWORD para la cuenta QA local.');
let token;
async function request(path,body){const response=await fetch(base+'/api'+path,{method:body?'POST':'GET',headers:{...(token?{Authorization:`Bearer ${token}`}:{}) ,...(body?{'Content-Type':'application/json'}:{})},...(body?{body:JSON.stringify(body)}:{})});if(!response.ok)throw new Error(`HTTP ${response.status}: ${await response.text()}`);return response.json();}
token=(await request('/auth/login',{email,password})).accessToken;
const projects=await request('/projects');
const fixture=projects.find(p=>p.name==='QA - Metodos UML');
if(!fixture)throw new Error('La prueba requiere el proyecto aislado QA - Metodos UML.');
const initial=await request(`/projects/${fixture.id}`),owner=initial.document.umlModel.classes[0];
if(!owner)throw new Error('El proyecto QA necesita una clase.');
const clientId=crypto.randomUUID(),pending=new Map();
const socketUrl=new URL('/ws',base);socketUrl.protocol=socketUrl.protocol==='https:'?'wss:':'ws:';
const client=new Client({webSocketFactory:()=>new WebSocket(socketUrl),connectHeaders:{Authorization:`Bearer ${token}`},reconnectDelay:0,connectionTimeout:10000,heartbeatIncoming:10000,heartbeatOutgoing:10000});
function onEvent(message){const event=JSON.parse(message.body);const callback=pending.get(event.operationId);if(callback){pending.delete(event.operationId);callback(event);}}
async function setMethods(project,methods){
 const operationId=crypto.randomUUID();
 const command={commandId:crypto.randomUUID(),issuedAt:new Date().toISOString(),type:'SET_CLASS_OPERATIONS',classId:owner.id,umlClass:{id:owner.id,name:'IGNORED_NAME',attributes:[],operations:methods}};
 const result=new Promise((resolve,reject)=>{const timer=setTimeout(()=>{pending.delete(operationId);reject(new Error('No se recibió confirmación STOMP. No reintentes sin consultar el documento.'));},12000);pending.set(operationId,event=>{clearTimeout(timer);event.type==='OPERATION_APPLIED'?resolve(event):reject(new Error(event.message));});});
 client.publish({destination:`/app/projects/${fixture.id}/operations`,body:JSON.stringify({operationId,projectId:fixture.id,clientId,baseRevision:project.revision,command})});
 await result;return request(`/projects/${fixture.id}`);
}
try{
 await new Promise((resolve,reject)=>{const timer=setTimeout(()=>reject(new Error('STOMP no conectó.')),12000);client.onStompError=f=>{clearTimeout(timer);reject(new Error(f.headers.message));};client.onConnect=()=>{clearTimeout(timer);client.subscribe(`/topic/projects/${fixture.id}/operations`,onEvent);client.subscribe(`/user/queue/projects/${fixture.id}/operations`,onEvent);setTimeout(resolve,150);};client.activate();});
 const old=owner.operations??[],method={id:crypto.randomUUID(),name:'qaProbe'+Date.now(),visibility:'PUBLIC',returnType:null,parameters:[]};
 let project=await setMethods(initial,[...old,method]);
 assert.equal(project.document.umlModel.classes[0].name,owner.name);
 assert.deepEqual(project.document.umlModel.classes[0].attributes,owner.attributes);
 assert.ok(project.document.umlModel.classes[0].operations.some(op=>op.id===method.id));
 project=await setMethods(project,[...old,{...method,name:method.name+'Updated'}]);
 assert.equal(project.document.umlModel.classes[0].operations.find(op=>op.id===method.id).name,method.name+'Updated');
 project=await setMethods(project,old);
 assert.deepEqual(project.document.umlModel.classes[0].operations,old);
 const activity=await request(`/projects/${fixture.id}/activities?size=3`);
 assert.ok(activity.items.some(item=>item.description.includes('método')));
 console.log('STOMP real: crear, actualizar y eliminar método confirmado; atributos y nombre conservados; actividad registrada.');
}finally{await client.deactivate();}
