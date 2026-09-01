# Dinho Rodas — PRD

## Objetivo
Site profissional focado em conversão (WhatsApp + orçamento) para a loja/oficina Dinho Rodas em Belo Horizonte, com painel admin para gerenciar todo o conteúdo.

## Stack
- React (CRA + CRACO) — mobile first
- FastAPI + MongoDB
- Auth admin por token derivado de TOKEN_SECRET (env)

## Personas
- Cliente final buscando rodas/pneus em BH (mobile, alta intenção)
- Admin Dinho Rodas gerenciando leads e conteúdo pelo painel

## Implementado
- 2026-08: Site público completo (Hero, Benefícios, Serviços, Orçamento, Foto-WhatsApp, Galeria, FAQ, Localização, CTA final, footer, floating WhatsApp, barra mobile fixa)
- 2026-08: Formulário de orçamento com upload de imagens (armazenadas no MongoDB) + confirmação
- 2026-08: Admin em /admin — login, dashboard com métricas, CRUD para services/testimonials/gallery/faqs/leads/quotes/settings
- 2026-08: Tracking de cliques no WhatsApp como leads
- 2026-09-01: Deployment readiness — removidas credenciais default do formulário de login (não vazam mais no bundle); app.py legado removido; deployment_agent status **pass**
- 2026-09-01: Regressão testada (backend 100%, frontend 100%)

## Backlog priorizado
- P1: Refino do painel — pipeline kanban de leads (Novo → Em atendimento → Enviado → Convertido → Perdido) + busca/filtros
- P1: Página de Configurações editável (telefone, endereço, textos, links, IDs GA/Pixel)
- P1: SEO — meta tags dinâmicas, Open Graph, Schema.org LocalBusiness, sitemap, robots
- P2: Notificação de novo lead (Resend e-mail ou Twilio WhatsApp)
- P2: Migrar uploads de MongoDB para Object Storage
- P3: Refatorar App.js em pages/components separados
- P3: `required`/`type=email` no login + limpar erro em nova tentativa

## Credenciais admin
Ver /app/memory/test_credentials.md
