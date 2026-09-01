from fastapi import FastAPI, APIRouter, UploadFile, File, Form, HTTPException, Header, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Any
import os, uuid, hashlib, hmac, base64

ROOT = Path(__file__).parent
load_dotenv(ROOT / '.env')
mongo = AsyncIOMotorClient(os.environ['MONGO_URL'])
db = mongo[os.environ['DB_NAME']]
app = FastAPI(title='Dinho Rodas API')
api = APIRouter(prefix='/api')
app.add_middleware(CORSMiddleware, allow_origins=os.environ.get('CORS_ORIGINS','*').split(','), allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

ADMIN_EMAIL = os.environ['ADMIN_EMAIL']
ADMIN_PASSWORD = os.environ['ADMIN_PASSWORD']
TOKEN_SECRET = os.environ['TOKEN_SECRET']
COLLECTIONS = ['services','testimonials','gallery','faqs','leads','quotes']
DEMO = {
 'services': [
  {'title':'Rodas','description':'Encontre opções para diferentes estilos de veículos e projetos.','category':'Rodas','image_url':'https://images.unsplash.com/photo-1611838608826-4c32a6160d90?auto=format&fit=crop&w=900&q=80','active':True,'demo':True},
  {'title':'Pneus','description':'Orientação para escolher a combinação adequada ao seu carro.','category':'Pneus','image_url':'https://images.unsplash.com/photo-1558981806-ec527fa84c39?auto=format&fit=crop&w=900&q=80','active':True,'demo':True},
  {'title':'Serviços automotivos','description':'Atendimento especializado para cuidar do conjunto roda e pneu.','category':'Serviços automotivos','image_url':'https://images.unsplash.com/photo-1486006920555-c77dcf18193c?auto=format&fit=crop&w=900&q=80','active':True,'demo':True},
 ],
 'testimonials': [],
 'gallery': [
  {'title':'Detalhes que fazem diferença','category':'Rodas','description':'Imagem DEMO para apresentação inicial.','image_url':'https://images.unsplash.com/photo-1503736334956-4c8f8e92946d?auto=format&fit=crop&w=900&q=80','active':True,'demo':True},
  {'title':'Cuidado em cada etapa','category':'Serviços','description':'Imagem DEMO para apresentação inicial.','image_url':'https://images.unsplash.com/photo-1487754180451-c456f719a1fc?auto=format&fit=crop&w=900&q=80','active':True,'demo':True},
 ],
 'faqs': [
  {'question':'Como faço um orçamento?','answer':'Preencha o formulário nesta página ou fale diretamente com a equipe pelo WhatsApp.','order':1,'active':True,'demo':True},
  {'question':'Posso enviar uma foto do meu carro?','answer':'Sim. Você pode anexar uma foto no formulário para ajudar na avaliação inicial.','order':2,'active':True,'demo':True},
  {'question':'Vocês atendem sem agendamento?','answer':'Fale com a equipe para confirmar a melhor forma e horário de atendimento.','order':3,'active':True,'demo':True},
 ]
}
SETTINGS = {'company_name':'Dinho Rodas','phone':'(31) 9931-0824','whatsapp':'553199310824','instagram':'instagram.com','address':'Av. Teresa Cristina, 5573 - Gameleira, Belo Horizonte - MG, 30550-390','hours':'Aberto · Fecha às 18:00','maps_url':'https://maps.google.com/?q=Av.+Teresa+Cristina,+5573,+Gameleira,+Belo+Horizonte+-+MG','meta_title':'Dinho Rodas | Rodas em Belo Horizonte','meta_description':'Dinho Rodas: loja e oficina especializada em rodas em Belo Horizonte, no bairro Gameleira. Solicite seu orçamento pelo WhatsApp.'}

def now(): return datetime.now(timezone.utc).isoformat()
def clean(doc):
    if not doc: return None
    doc.pop('_id', None); return doc
def token_for(email):
    raw=f'{email}:{TOKEN_SECRET}'.encode(); return hashlib.sha256(raw).hexdigest()
def require_auth(authorization: Optional[str]):
    if not authorization or not hmac.compare_digest(authorization.replace('Bearer ','').strip(), token_for(ADMIN_EMAIL)): raise HTTPException(401, 'Não autorizado')
async def seed():
    for name, rows in DEMO.items():
        if await db[name].count_documents({}) == 0:
            for row in rows: await db[name].insert_one({**row,'id':str(uuid.uuid4()),'created_at':now()})
    if await db.settings.count_documents({}) == 0: await db.settings.insert_one({**SETTINGS,'id':'main'})
@app.on_event('startup')
async def startup(): await seed()

class Login(BaseModel): email: str; password: str
class Item(BaseModel): model_config={'extra':'allow'}

@api.get('/public')
async def public_data():
    out={}
    for name in ['services','testimonials','gallery','faqs']:
        out[name]=[clean(x) for x in await db[name].find({'active':{'$ne':False}}).sort('order',1).to_list(100)]
    out['settings']=clean(await db.settings.find_one({'id':'main'}))
    return out
@api.get('/health')
async def health():
    await db.command('ping')
    return {'status':'ok','database':'connected'}
@api.post('/auth/login')
async def login(data: Login):
    if not hmac.compare_digest(data.email,ADMIN_EMAIL) or not hmac.compare_digest(data.password,ADMIN_PASSWORD): raise HTTPException(401,'E-mail ou senha inválidos')
    return {'token':token_for(data.email),'email':data.email}
@api.post('/quotes')
async def create_quote(name: str=Form(...), phone: str=Form(...), vehicle: str=Form(''), year: str=Form(''), interest: str=Form(''), message: str=Form(''), origin: str=Form('site-form'), photos: list[UploadFile]=File(default=[])):
    files=[]
    for photo in photos[:5]:
        if not photo.content_type or not photo.content_type.startswith('image/'): continue
        file_id=str(uuid.uuid4()); contents=await photo.read()
        if len(contents)>10*1024*1024: continue
        await db.files.insert_one({'id':file_id,'content':base64.b64encode(contents).decode(),'content_type':photo.content_type,'original_filename':photo.filename,'created_at':now()})
        files.append(f'/api/files/{file_id}')
    lead={'id':str(uuid.uuid4()),'name':name,'phone':phone,'vehicle':vehicle,'year':year,'interest':interest,'message':message,'photos':files,'origin':origin,'status':'Novo','created_at':now()}
    await db.quotes.insert_one(lead); await db.leads.insert_one({**lead,'source':origin})
    return clean(lead)
@api.get('/files/{file_id}')
async def get_file(file_id:str):
    record=await db.files.find_one({'id':file_id})
    if not record: raise HTTPException(404,'Arquivo não encontrado')
    return Response(base64.b64decode(record['content']), media_type=record.get('content_type','image/jpeg'))
@api.post('/leads/click')
async def whatsapp_click(data: Item):
    row={**data.model_dump(),'id':str(uuid.uuid4()),'status':'Novo','created_at':now()}; await db.leads.insert_one(row); return clean(row)
@api.get('/dashboard/metrics')
async def metrics(authorization: Optional[str]=Header(None)):
    require_auth(authorization); return {'total_leads':await db.leads.count_documents({}),'total_quotes':await db.quotes.count_documents({}),'new_quotes':await db.quotes.count_documents({'status':'Novo'}),'converted':await db.leads.count_documents({'status':'Convertido'}),'services_count':await db.services.count_documents({'active':True}),'whatsapp_clicks':await db.leads.count_documents({'source':{'$regex':'WhatsApp'}})}
@api.get('/admin/{collection}')
async def list_items(collection:str, authorization:Optional[str]=Header(None)):
    require_auth(authorization); name='quotes' if collection=='quotes' else collection
    if name not in COLLECTIONS: raise HTTPException(404,'Coleção inválida')
    return [clean(x) for x in await db[name].find({}).sort('created_at',-1).to_list(1000)]
@api.post('/admin/{collection}')
async def add_item(collection:str, data:Item, authorization:Optional[str]=Header(None)):
    require_auth(authorization)
    if collection not in COLLECTIONS: raise HTTPException(404,'Coleção inválida')
    row={**data.model_dump(),'id':str(uuid.uuid4()),'created_at':now()}; await db[collection].insert_one(row); return clean(row)
@api.put('/admin/{collection}/{item_id}')
async def update_item(collection:str,item_id:str,data:Item,authorization:Optional[str]=Header(None)):
    require_auth(authorization); payload=data.model_dump(); payload.pop('id',None); await db[collection].update_one({'id':item_id},{'$set':payload}); return clean(await db[collection].find_one({'id':item_id}))
@api.delete('/admin/{collection}/{item_id}')
async def delete_item(collection:str,item_id:str,authorization:Optional[str]=Header(None)):
    require_auth(authorization); await db[collection].delete_one({'id':item_id}); return {'ok':True}
@api.get('/settings')
async def get_settings(): return clean(await db.settings.find_one({'id':'main'}))
@api.put('/settings')
async def update_settings(data:Item,authorization:Optional[str]=Header(None)):
    require_auth(authorization); payload=data.model_dump(); payload.pop('_id',None); await db.settings.update_one({'id':'main'},{'$set':payload},upsert=True); return clean(await db.settings.find_one({'id':'main'}))
app.include_router(api)
@app.on_event('shutdown')
async def shutdown(): mongo.close()