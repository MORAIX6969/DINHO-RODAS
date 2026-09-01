import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__, static_folder='static')
CORS(app)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# In-memory storage with seed demo data
SERVICES_DB = [
    {
        "id": 1,
        "title": "Reforma e Pintura de Rodas",
        "description": "Restauração completa de rodas de liga leve, remoção de amassados, solda de trincas e pintura eletrostática de alta resistência.",
        "price": "A partir de R$ 150/roda",
        "icon": "Wrench",
        "popular": True
    },
    {
        "id": 2,
        "title": "Alinhamento 3D & Balanceamento",
        "description": "Tecnologia laser de última geração para máxima precisão na geometria da suspensão e estabilidade do veículo.",
        "price": "R$ 120",
        "icon": "Target",
        "popular": True
    },
    {
        "id": 3,
        "title": "Diamantação de Rodas",
        "description": "Acabamento diamantado em CNC computadorizado com verniz protetores especiais para o brilho original de fábrica.",
        "price": "A partir de R$ 220/roda",
        "icon": "Sparkles",
        "popular": False
    },
    {
        "id": 4,
        "title": "Venda de Rodas & Pneus",
        "description": "Amplo estoque multimarca de rodas esportivas e originais, além de pneus novos e seminovos com garantia.",
        "price": "Sob consulta",
        "icon": "Disc",
        "popular": False
    },
    {
        "id": 5,
        "title": "Cambagem & Castor",
        "description": "Correção técnica de cambagem e castor para evitar desgaste irregular de pneus e puxadas na direção.",
        "price": "R$ 100",
        "icon": "Sliders",
        "popular": False
    },
    {
        "id": 6,
        "title": "Manutenção de Suspensão & Freios",
        "description": "Revisão completa de amortecedores, molas, pastilhas e discos de freio para sua total segurança.",
        "price": "Orçamento gratuito",
        "icon": "ShieldCheck",
        "popular": False
    }
]

TESTIMONIALS_DB = [
    {
        "id": 1,
        "title": "Excelente atendimento e rapidez!",
        "content": "Minhas rodas esportivas estavam raladas e amassadas após um buraco. A equipe da Dinho Rodas deixou zeradas, parece que saíram da concessionária! Recomendo demais.",
        "author": "Carlos Eduardo M.",
        "rating": 5,
        "vehicle": "VW Golf GTI",
        "date": "15 dias atrás"
    },
    {
        "id": 2,
        "title": "Melhor oficina de BH para rodas",
        "content": "Serviço de diamantação impecável. Atendimento nota 10 pelo WhatsApp e cumpriram o prazo combinado. Preço justo pela altíssima qualidade.",
        "author": "Mariana Silveira",
        "rating": 5,
        "vehicle": "BMW Série 3",
        "date": "1 mês atrás"
    },
    {
        "id": 3,
        "title": "Profissionais de confiança",
        "content": "Fiz alinhamento 3D e troca de pneus. O carro ficou perfeitamente alinhado. Local limpo, organizado e com ótima localização na Av. Teresa Cristina.",
        "author": "Roberto S. Alves",
        "rating": 5,
        "vehicle": "Toyota Hilux",
        "date": "2 meses atrás"
    }
]

GALLERY_DB = [
    {
        "id": 1,
        "title": "Diamantação CNC em Roda Aro 20",
        "category": "Diamantação",
        "image_url": "https://images.unsplash.com/photo-1611838608826-4c32a6160d90?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1NzB8MHwxfHNlYXJjaHw0fHxsdXh1cnklMjBjYXIlMjB3aGVlbHMlMjByaW0lMjByZXBhaXJ8ZW58MHx8fHwxNzg4MjkwNTg1fDA&ixlib=rb-4.1.0&q=85"
    },
    {
        "id": 2,
        "title": "Oficina & Estoque Organizado",
        "category": "Oficina",
        "image_url": "https://images.unsplash.com/photo-1786489623872-2ebdfe51297c?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2OTF8MHwxfHNlYXJjaHwyfHxjYXIlMjBhbGxveSUyMHdoZWVscyUyMGdhcmFnZSUyMHdvcmtzaG9wfGVufDB8fHx8MTc4ODI5MDU4MXww&ixlib=rb-4.1.0&q=85"
    },
    {
        "id": 3,
        "title": "Pintura Eletrostática Preto Fosco",
        "category": "Pintura",
        "image_url": "https://images.unsplash.com/photo-1611633235555-45e252fe48c8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1NzB8MHwxfHNlYXJjaHwyfHxsdXh1cnklMjBjYXIlMjB3aGVlbHMlMjByaW0lMjByZXBhaXJ8ZW58MHx8fHwxNzg4MjkwNTg1fDA&ixlib=rb-4.1.0&q=85"
    },
    {
        "id": 4,
        "title": "Alinhamento Esportivo 3D",
        "category": "Alinhamento",
        "image_url": "https://images.unsplash.com/photo-1515871401659-95f03af5fb36?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1NzB8MHwxfHNlYXJjaHwzfHxsdXh1cnklMjBjYXIlMjB3aGVlbHMlMjByaW0lMjByZXBhaXJ8ZW58MHx8fHwxNzg4MjkwNTg1fDA&ixlib=rb-4.1.0&q=85"
    }
]

FAQS_DB = [
    {
        "id": 1,
        "question": "Quanto tempo demora a reforma ou diamantação das rodas?",
        "answer": "Normalmente o serviço leva de 24 a 48 horas, dependendo do estado da roda e do tipo de acabamento solicitado. Oferecemos agilidade para você ficar o mínimo tempo possível sem o veículo."
    },
    {
        "id": 2,
        "question": "Rodas trincadas ou amassadas têm conserto seguro?",
        "answer": "Sim! Realizamos solda TIG especializada e desamassamento hidráulico com rigorosos testes de qualidade e balanceamento, garantindo total segurança para uso urbano e rodoviário."
    },
    {
        "id": 3,
        "question": "Preciso agendar horário ou posso ir direto à oficina?",
        "answer": "Recomendamos o agendamento prévio (via WhatsApp ou formulário no site) para garantir atendimento imediato e prioridade na execução dos serviços."
    },
    {
        "id": 4,
        "question": "Quais são as formas de pagamento aceitas?",
        "answer": "Aceitamos dinheiro, PIX (com desconto especial), cartões de crédito em até 10x sem juros e faturamento para frotistas cadastrados."
    },
    {
        "id": 5,
        "question": "Onde a Dinho Rodas está localizada em Belo Horizonte?",
        "answer": "Estamos na Av. Teresa Cristina, 5573 - Gameleira, Belo Horizonte - MG (CEP 30550-390), com fácil acesso pela Via Expressa e Anel Rodoviário."
    }
]

QUOTES_DB = [
    {
        "id": 1,
        "name": "Marcos Vinicius",
        "phone": "(31) 98765-4321",
        "vehicle": "Honda Civic 2021",
        "service": "Reforma e Pintura de Rodas",
        "message": "Minhas 4 rodas aro 17 estão raladas na borda. Quero pintar em grafite fosco.",
        "image_url": "",
        "status": "Novo",
        "created_at": "2026-06-01 10:30"
    },
    {
        "id": 2,
        "name": "Juliana Paiva",
        "phone": "(31) 97123-4567",
        "vehicle": "Jeep Compass",
        "service": "Alinhamento 3D & Balanceamento",
        "message": "Carro puxando para a direita e volante vibrando acima de 90km/h.",
        "image_url": "",
        "status": "Em Contato",
        "created_at": "2026-06-02 14:15"
    }
]

LEADS_DB = [
    {
        "id": 1,
        "name": "Alexandre Souza",
        "phone": "(31) 99888-7766",
        "interest": "Orçamento Rodas Aro 18",
        "source": "WhatsApp Floating Button",
        "status": "Convertido",
        "created_at": "2026-06-02 09:12"
    }
]

SETTINGS_DB = {
    "company_name": "Dinho Rodas",
    "address": "Av. Teresa Cristina, 5573 - Gameleira, Belo Horizonte - MG, 30550-390",
    "phone": "(31) 9931-0824",
    "instagram": "https://instagram.com/dinhorodas",
    "google_rating": "4,8",
    "google_reviews_count": 64,
    "opening_hours": "Segunda a Sexta: 08:00 às 18:00 | Sábado: 08:00 às 13:00",
    "analytics_code": "G-DINHODAS2026",
    "whatsapp_message": "Olá! Vim pelo site da Dinho Rodas e gostaria de tirar uma dúvida ou solicitar orçamento."
}

# --- API ROUTES ---

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})

@app.route('/api/settings', methods=['GET'])
def get_settings():
    return jsonify(SETTINGS_DB)

@app.route('/api/settings', methods=['PUT'])
def update_settings():
    data = request.json
    SETTINGS_DB.update(data)
    return jsonify({"status": "success", "settings": SETTINGS_DB})

@app.route('/api/services', methods=['GET'])
def get_services():
    return jsonify(SERVICES_DB)

@app.route('/api/services', methods=['POST'])
def add_service():
    data = request.json
    new_id = max([s['id'] for s in SERVICES_DB], default=0) + 1
    new_service = {
        "id": new_id,
        "title": data.get("title"),
        "description": data.get("description"),
        "price": data.get("price", "Sob consulta"),
        "icon": data.get("icon", "Wrench"),
        "popular": data.get("popular", False)
    }
    SERVICES_DB.append(new_service)
    return jsonify(new_service), 201

@app.route('/api/services/<int:service_id>', methods=['PUT'])
def update_service(service_id):
    data = request.json
    for s in SERVICES_DB:
        if s['id'] == service_id:
            s.update(data)
            return jsonify(s)
    return jsonify({"error": "Service not found"}), 404

@app.route('/api/services/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    global SERVICES_DB
    SERVICES_DB = [s for s in SERVICES_DB if s['id'] != service_id]
    return jsonify({"status": "success"})

@app.route('/api/testimonials', methods=['GET'])
def get_testimonials():
    return jsonify(TESTIMONIALS_DB)

@app.route('/api/testimonials', methods=['POST'])
def add_testimonial():
    data = request.json
    new_id = max([t['id'] for t in TESTIMONIALS_DB], default=0) + 1
    new_item = {
        "id": new_id,
        "title": data.get("title"),
        "content": data.get("content"),
        "author": data.get("author"),
        "rating": int(data.get("rating", 5)),
        "vehicle": data.get("vehicle", "Cliente Dinho Rodas"),
        "date": "Hoje"
    }
    TESTIMONIALS_DB.append(new_item)
    return jsonify(new_item), 201

@app.route('/api/testimonials/<int:item_id>', methods=['DELETE'])
def delete_testimonial(item_id):
    global TESTIMONIALS_DB
    TESTIMONIALS_DB = [t for t in TESTIMONIALS_DB if t['id'] != item_id]
    return jsonify({"status": "success"})

@app.route('/api/gallery', methods=['GET'])
def get_gallery():
    return jsonify(GALLERY_DB)

@app.route('/api/gallery', methods=['POST'])
def add_gallery():
    data = request.json
    new_id = max([g['id'] for g in GALLERY_DB], default=0) + 1
    new_item = {
        "id": new_id,
        "title": data.get("title", "Trabalho Dinho Rodas"),
        "category": data.get("category", "Geral"),
        "image_url": data.get("image_url", "https://images.unsplash.com/photo-1611838608826-4c32a6160d90?q=80&w=800&auto=format&fit=crop")
    }
    GALLERY_DB.append(new_item)
    return jsonify(new_item), 201

@app.route('/api/gallery/<int:item_id>', methods=['DELETE'])
def delete_gallery(item_id):
    global GALLERY_DB
    GALLERY_DB = [g for g in GALLERY_DB if g['id'] != item_id]
    return jsonify({"status": "success"})

@app.route('/api/faqs', methods=['GET'])
def get_faqs():
    return jsonify(FAQS_DB)

@app.route('/api/faqs', methods=['POST'])
def add_faq():
    data = request.json
    new_id = max([f['id'] for f in FAQS_DB], default=0) + 1
    new_item = {
        "id": new_id,
        "question": data.get("question"),
        "answer": data.get("answer")
    }
    FAQS_DB.append(new_item)
    return jsonify(new_item), 201

@app.route('/api/faqs/<int:item_id>', methods=['DELETE'])
def delete_faq(item_id):
    global FAQS_DB
    FAQS_DB = [f for f in FAQS_DB if f['id'] != item_id]
    return jsonify({"status": "success"})

@app.route('/api/quotes', methods=['GET'])
def get_quotes():
    return jsonify(QUOTES_DB)

@app.route('/api/quotes', methods=['POST'])
def create_quote():
    data = request.form
    image_url = ""
    
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename:
            filename = secure_filename(file.filename)
            unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            image_url = f"/static/uploads/{unique_filename}"
    
    new_id = max([q['id'] for q in QUOTES_DB], default=0) + 1
    new_quote = {
        "id": new_id,
        "name": data.get("name"),
        "phone": data.get("phone"),
        "vehicle": data.get("vehicle", "Não informado"),
        "service": data.get("service", "Geral"),
        "message": data.get("message", ""),
        "image_url": image_url or data.get("image_url", ""),
        "status": "Novo",
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    QUOTES_DB.append(new_quote)
    
    # Also create a corresponding lead
    LEADS_DB.append({
        "id": len(LEADS_DB) + 1,
        "name": data.get("name"),
        "phone": data.get("phone"),
        "interest": f"Orçamento: {data.get('service')}",
        "source": "Formulário Web",
        "status": "Novo",
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M')
    })
    
    return jsonify({"status": "success", "quote": new_quote}), 201

@app.route('/api/quotes/<int:quote_id>', methods=['PUT'])
def update_quote_status(quote_id):
    data = request.json
    for q in QUOTES_DB:
        if q['id'] == quote_id:
            if 'status' in data:
                q['status'] = data['status']
            return jsonify(q)
    return jsonify({"error": "Quote not found"}), 404

@app.route('/api/leads', methods=['GET'])
def get_leads():
    return jsonify(LEADS_DB)

@app.route('/api/leads', methods=['POST'])
def create_lead():
    data = request.json
    new_id = max([l['id'] for l in LEADS_DB], default=0) + 1
    new_lead = {
        "id": new_id,
        "name": data.get("name", "Contato WhatsApp"),
        "phone": data.get("phone", "(31) 9xxxx-xxxx"),
        "interest": data.get("interest", "Contato Direto"),
        "source": data.get("source", "WhatsApp Widget"),
        "status": "Novo",
        "created_at": datetime.now().strftime('%Y-%m-%d %H:%M')
    }
    LEADS_DB.append(new_lead)
    return jsonify(new_lead), 201

@app.route('/api/leads/<int:lead_id>', methods=['PUT'])
def update_lead_status(lead_id):
    data = request.json
    for l in LEADS_DB:
        if l['id'] == lead_id:
            if 'status' in data:
                l['status'] = data['status']
            return jsonify(l)
    return jsonify({"error": "Lead not found"}), 404

@app.route('/api/dashboard/metrics', methods=['GET'])
def get_dashboard_metrics():
    return jsonify({
        "total_leads": len(LEADS_DB),
        "total_quotes": len(QUOTES_DB),
        "new_quotes": sum(1 for q in QUOTES_DB if q['status'] == 'Novo'),
        "services_count": len(SERVICES_DB),
        "google_rating": "4.8 / 64 avaliações"
    })

# Auth login
@app.route('/api/auth/login', methods=['POST'])
def admin_login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    if email == "admin@dinhorodas.com" and password == "Dinho#2026":
        return jsonify({
            "status": "success",
            "token": "dinho_token_secure_2026_xyz",
            "user": {"email": email, "name": "Dinho Administrador"}
        })
    return jsonify({"error": "Credenciais inválidas. Use admin@dinhorodas.com / Dinho#2026"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
