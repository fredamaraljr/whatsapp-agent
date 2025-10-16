# 🚀 AI Companion - Sistema Multi-Tenant v2.0

> Agente de IA inteligente com suporte a múltiplos grupos de usuários via WhatsApp

## ✨ Novidades da Versão 2.0

### 🎯 Sistema Multi-Tenant

Agora o AI Companion suporta **5 grupos distintos de usuários**, cada um com funcionalidades específicas:

- 👨‍💼 **Admin** - Gestão total do sistema
- 📊 **Monitori** - Análise de dados e BI
- 🏥 **FPS** - Educação médica
- 💼 **Ávila Digital** - Demonstrações de IA
- ✈️ **FFL** - Aviação técnica (A320)

### 🔥 Features Principais

- ✅ **Identificação Automática**: Usuários identificados pelo número de telefone
- ✅ **Verificação Inteligente**: Pergunta de grupo na primeira interação
- ✅ **Prompts Especializados**: Contexto específico para cada grupo
- ✅ **Comandos Admin**: Gestão via WhatsApp (`/stats`, `/setprompt`, etc)
- ✅ **Customização Dinâmica**: Admin pode modificar prompts sem redeploy
- ✅ **Logging Completo**: Tracking de todas as interações
- ✅ **Estatísticas**: Métricas por grupo e usuário

## 📋 Documentação

### Guias Disponíveis

1. **[Sistema Multi-Tenant](docs/MULTI_TENANT_SYSTEM.md)** - Documentação completa
2. **[Arquitetura](docs/ARCHITECTURE_DIAGRAM.md)** - Diagramas e fluxos
3. **[Migração](docs/MIGRATION_GUIDE.md)** - Guia passo a passo
4. **[Exemplos](docs/USAGE_EXAMPLES.md)** - Casos de uso práticos
5. **[Resumo](docs/IMPLEMENTATION_SUMMARY.md)** - Implementação completa

## 🚀 Quick Start

### 1. Configuração

```bash
# Clone o repositório
git clone https://github.com/fredamaraljr/whatsapp-agent.git
cd whatsapp-agent/ava-whatsapp-agent-course

# Configure variáveis de ambiente
cp .env.example .env
nano .env  # Adicionar configurações
```

### 2. Variáveis de Ambiente Essenciais

```env
# Admin Configuration
ADMIN_PHONE_NUMBER=+5511991668852

# Database Paths
USER_DB_PATH=/app/data/users.db
SHORT_TERM_MEMORY_DB_PATH=/app/data/memory.db

# LLM APIs
GROQ_API_KEY=your_groq_key
TOGETHER_API_KEY=your_together_key

# Voice
ELEVENLABS_API_KEY=your_elevenlabs_key
ELEVENLABS_VOICE_ID=your_voice_id

# Vector Store
QDRANT_URL=http://localhost
QDRANT_PORT=6333
```

### 3. Executar

```bash
# Com Docker Compose
docker-compose up -d

# Ou localmente
pip install -e .
uvicorn ai_companion.interfaces.whatsapp.webhook_endpoint:app --reload
```

### 4. Testar

Envie uma mensagem WhatsApp para o número configurado:

```
👤: Olá

🤖: Olá! Seja bem-vindo(a)! 👋

Você é:
1️⃣ Cliente da Monitori
2️⃣ Estudante da FPS
3️⃣ Colaborador da Ávila Digital
4️⃣ Piloto ou interessado em aviação

Por favor, responda com o número...
```

## 👥 Grupos de Usuários

### 👨‍💼 Admin (Fred)

**Número:** +5511991668852  
**Acesso:** Total ao sistema

**Comandos:**

```bash
/stats              # Estatísticas do sistema
/users              # Lista de usuários
/setprompt GRUPO    # Customizar prompt
/getprompt GRUPO    # Ver prompt atual
/config KEY=VALUE   # Configurar sistema
/help               # Ajuda
```

### 📊 Monitori (Análise de Dados)

**Features:**

- Análise de dados via Mitto
- Insights e dashboards
- Métricas de negócio
- Relatórios customizados

**Verificação:** Confirmar que é cliente Monitori

### 🏥 FPS (Faculdade Pernambucana de Saúde)

**Features:**

- Calendário de provas
- Casos clínicos
- Discussão de conteúdo médico
- Orientação educacional

**Verificação:** Confirmar que estuda na FPS

### 💼 Ávila Digital (Demonstrações)

**Features:**

- Apresentação de capacidades
- Modo simulação de outros grupos
- Demonstrações interativas
- Casos de uso de IA

**Verificação:** Confirmar que trabalha na Ávila

### ✈️ FFL (Flight Fans & Learners)

**Features:**

- Manuais técnicos A320 (FCOM, FCTM, MEL, CDL)
- Explicações de procedimentos
- Discussões operacionais
- Conhecimento especializado

**Verificação:** Confirmar interesse em aviação

## 🏗️ Arquitetura

```
WhatsApp Message
       ↓
webhook_endpoint.py
       ↓
user_identification_node
       ↓
   ┌───┴────┐
   │        │
Admin?   Verified?
   │        │
   ↓        ↓
Commands  Conversation
   │        │
   └────┬───┘
        ↓
    Response
```

### Componentes Principais

- **User Manager**: Identificação e gerenciamento de usuários
- **Admin Commands**: Sistema de comandos administrativos
- **Group Prompts**: Prompts especializados por grupo
- **LangGraph Flow**: Roteamento condicional baseado em grupo
- **Vector Store**: Base de conhecimento (Qdrant)
- **Memory System**: Memória de curto e longo prazo

## 📊 Banco de Dados

### Estrutura

```sql
-- Usuários
CREATE TABLE users (
    phone_number TEXT PRIMARY KEY,
    user_group TEXT NOT NULL,
    verified INTEGER NOT NULL,
    first_interaction TEXT,
    last_interaction TEXT,
    message_count INTEGER,
    metadata TEXT
);

-- Log de Interações
CREATE TABLE interaction_log (
    id INTEGER PRIMARY KEY,
    phone_number TEXT,
    timestamp TEXT,
    message_type TEXT
);
```

## 🔧 Desenvolvimento

### Estrutura de Pastas

```
src/ai_companion/
├── core/
│   └── prompts.py              # Prompts por grupo
├── graph/
│   ├── state.py               # Estado com campos de usuário
│   ├── nodes.py               # Nós de identificação/verificação
│   ├── edges.py               # Roteamento condicional
│   └── graph.py               # Grafo principal
├── modules/
│   ├── user_management/       # Sistema de usuários
│   │   └── user_manager.py
│   ├── admin/                 # Comandos admin
│   │   └── admin_commands.py
│   ├── memory/
│   ├── speech/
│   └── image/
└── interfaces/
    └── whatsapp/
        └── whatsapp_response.py
```

### Adicionar Novo Grupo

1. Adicionar enum em `user_manager.py`:

```python
class UserGroup(Enum):
    ...
    NOVO_GRUPO = "novo_grupo"
```

2. Criar prompt em `prompts.py`:

```python
NOVO_GRUPO_PROMPT = """
[Prompt específico do grupo]
"""
```

3. Adicionar à seleção em `chains.py`:

```python
group_prompts = {
    ...
    "novo_grupo": NOVO_GRUPO_PROMPT,
}
```

4. Atualizar pergunta de verificação

## 📈 Monitoramento

### Ver Logs

```bash
tail -f /app/logs/app.log
```

### Estatísticas

```bash
sqlite3 /app/data/users.db "
SELECT user_group, COUNT(*)
FROM users
GROUP BY user_group;
"
```

### Backup

```bash
# Backup automático (crontab)
0 */6 * * * cp /app/data/users.db /backups/users_$(date +\%Y\%m\%d).db
```

## 🧪 Testes

### Teste Completo

```bash
# 1. Admin
curl -X POST localhost:8000/whatsapp_response \
  -H "Content-Type: application/json" \
  -d '{"entry":[{"changes":[{"value":{"messages":[{"from":"+5511991668852","text":{"body":"/stats"}}]}}]}]}'

# 2. Novo usuário
# Enviar mensagem de número desconhecido
# Verificar pergunta de verificação

# 3. Verificação
# Responder com número 1-4
# Verificar confirmação

# 4. Uso normal
# Enviar mensagem do mesmo número
# Verificar resposta contextualizada
```

## 🚨 Troubleshooting

### Problema: Usuário não identificado

```bash
# Verificar logs
tail -f /app/logs/app.log | grep "user_phone"

# Verificar banco
sqlite3 /app/data/users.db "SELECT * FROM users;"
```

### Problema: Comandos admin não funcionam

```bash
# Verificar .env
grep ADMIN_PHONE_NUMBER .env

# Verificar banco
sqlite3 /app/data/users.db "SELECT * FROM users WHERE user_group='admin';"
```

### Problema: Prompts não mudam

```bash
# Testar seleção de prompts
python -c "
from ai_companion.graph.utils.chains import get_prompt_for_group
print(get_prompt_for_group('monitori'))
"
```

## 📞 Suporte

- **Documentação**: Ver `/docs`
- **Issues**: GitHub Issues
- **Admin**: WhatsApp +5511991668852

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Ver arquivo `LICENSE` para mais detalhes.

## 👏 Créditos

- **Desenvolvido por:** Fred Amaral Jr
- **Tecnologias:** LangChain, LangGraph, Groq, Qdrant, ElevenLabs
- **Versão:** 2.0 - Multi-Tenant
- **Data:** Outubro 2025

## 🗺️ Roadmap

### Próximas Features

- [ ] Integração Mitto para Monitori
- [ ] Sistema de calendário FPS
- [ ] Upload de casos clínicos FPS
- [ ] Modo demo interativo Ávila
- [ ] Dashboard web para admin
- [ ] API REST para gestão
- [ ] Notificações automáticas
- [ ] Análise de sentimento
- [ ] Recomendações ML
- [ ] Integração com outras plataformas

---

**⭐ Se este projeto foi útil, considere dar uma estrela!**

[GitHub](https://github.com/fredamaraljr/whatsapp-agent) | [Documentação](docs/) | [Issues](https://github.com/fredamaraljr/whatsapp-agent/issues)
