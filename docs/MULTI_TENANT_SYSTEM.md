# Sistema Multi-Tenant - AI Companion

## 📋 Visão Geral

O AI Companion foi transformado em um **sistema multi-tenant** que suporta diferentes grupos de usuários, cada um com funcionalidades específicas e contextos personalizados.

## 👥 Grupos de Usuários

### 1. **Admin** (Fred - +5511991668852)
**Acesso total ao sistema**

O administrador pode:
- Ver estatísticas do sistema (usuários, mensagens, interações)
- Listar todos os usuários cadastrados
- Modificar prompts de grupos via WhatsApp
- Configurar o sistema dinamicamente
- Acessar logs e informações técnicas

**Comandos disponíveis:**
```
/stats                    # Estatísticas do sistema
/users                    # Lista de usuários
/setprompt GRUPO         # Definir prompt customizado
  [texto do prompt]
/getprompt GRUPO         # Ver prompt atual
/config CHAVE=VALOR      # Configurar sistema
/getconfig CHAVE         # Ver configuração
/help                    # Ajuda com comandos
```

**Exemplo:**
```
/setprompt monitori
Você é um especialista em análise de dados...
```

### 2. **Monitori**
**Clientes de análise de dados**

Funcionalidades:
- Análises de dados via Mitto
- Insights e relatórios
- Dashboards e métricas
- Business intelligence

**Verificação:**
Usuário deve confirmar que é cliente Monitori na primeira interação.

### 3. **FPS (Faculdade Pernambucana de Saúde)**
**Estudantes de medicina**

Funcionalidades:
- Calendário de provas
- Casos clínicos da base de conhecimento
- Discussão de conteúdo médico
- Orientação sobre procedimentos

**Verificação:**
Usuário deve confirmar que é estudante da FPS.

### 4. **Ávila Digital**
**Colaboradores e prospects**

Funcionalidades:
- Demonstração de capacidades de IA
- Simulações de diferentes grupos
- Apresentação de funcionalidades
- Modo demo interativo

**Verificação:**
Usuário deve confirmar que trabalha na Ávila Digital.

**Modo Demonstração:**
```
"Simule o grupo Monitori"
"Mostre como funciona para FPS"
```

### 5. **FFL (Flight Fans & Learners)**
**Pilotos e entusiastas de aviação**

Funcionalidades:
- Manuais técnicos do Airbus A320 (FCOM, FCTM, MEL, CDL)
- Explicações de procedimentos
- Discussões operacionais
- Conhecimento técnico especializado

**Verificação:**
Usuário deve confirmar que pilota ou tem interesse em aviação.

## 🔄 Fluxo de Verificação

### Primeira Interação

1. **Identificação:** Sistema identifica o número de telefone
2. **Pergunta de Verificação:** Agente pergunta a qual grupo o usuário pertence
3. **Resposta do Usuário:** Usuário escolhe opção (1, 2, 3 ou 4)
4. **Confirmação:** Sistema confirma e ativa funcionalidades do grupo
5. **Memória:** Sistema lembra do grupo nas próximas interações

### Mensagem de Boas-Vindas

```
Olá! Seja bem-vindo(a)! 👋

Para que eu possa oferecer o melhor atendimento, preciso saber um pouco mais sobre você.

Você é:
1️⃣ Cliente da Monitori
2️⃣ Estudante da FPS (Faculdade Pernambucana de Saúde)
3️⃣ Colaborador da Ávila Digital
4️⃣ Piloto ou interessado em aviação

Por favor, responda com o número da opção que melhor se aplica a você.
```

## 🗄️ Estrutura de Dados

### Banco de Dados de Usuários

**Localização:** `/app/data/users.db`

**Tabelas:**
- `users`: Informações dos usuários
  - phone_number (PK)
  - user_group
  - verified
  - first_interaction
  - last_interaction
  - message_count
  - metadata

- `interaction_log`: Log de interações
  - id (PK)
  - phone_number (FK)
  - timestamp
  - message_type

## 🔧 Configurações

### Arquivo `.env`

Adicionar as seguintes variáveis:

```env
# Admin
ADMIN_PHONE_NUMBER=+5511991668852

# Monitori
MITTO_API_KEY=your_mitto_api_key
MITTO_DATABASE_URL=your_database_url

# FPS
FPS_CALENDAR_PATH=/app/data/fps_calendar.json
FPS_CLINICAL_CASES_PATH=/app/knowledge/fps_clinical_cases

# Database
USER_DB_PATH=/app/data/users.db
```

## 📁 Arquivos Modificados

### Novos Arquivos
- `src/ai_companion/modules/user_management/user_manager.py` - Gerenciamento de usuários
- `src/ai_companion/modules/user_management/__init__.py`
- `src/ai_companion/modules/admin/admin_commands.py` - Comandos administrativos
- `src/ai_companion/modules/admin/__init__.py`

### Arquivos Modificados
- `src/ai_companion/graph/state.py` - Adicionado campos de usuário ao estado
- `src/ai_companion/graph/nodes.py` - Adicionado nós de identificação e verificação
- `src/ai_companion/graph/edges.py` - Adicionado edges de roteamento
- `src/ai_companion/graph/graph.py` - Atualizado fluxo do grafo
- `src/ai_companion/graph/utils/chains.py` - Adicionado seleção de prompts por grupo
- `src/ai_companion/core/prompts.py` - Adicionado prompts específicos por grupo
- `src/ai_companion/settings.py` - Adicionado configurações de grupos
- `src/ai_companion/interfaces/whatsapp/whatsapp_response.py` - Passar número de telefone

## 🚀 Como Usar

### 1. Configuração Inicial

```bash
# Instalar dependências (se necessário)
pip install -e .

# Criar diretórios de dados
mkdir -p /app/data
mkdir -p /app/knowledge/fps_clinical_cases
```

### 2. Configurar Variáveis de Ambiente

Editar `.env` com as configurações necessárias.

### 3. Executar o Sistema

```bash
# Via Docker Compose
docker-compose up

# Ou localmente
uvicorn ai_companion.interfaces.whatsapp.webhook_endpoint:app --reload
```

### 4. Testar

1. Enviar mensagem de um novo número
2. Responder à pergunta de verificação
3. Testar funcionalidades específicas do grupo

## 📊 Estatísticas (Admin)

O admin pode visualizar estatísticas enviando `/stats`:

```
📊 Estatísticas do Sistema

👥 Total de usuários: 15
💬 Total de mensagens: 234
🕐 Interações (24h): 45

Usuários por grupo:
  • admin: 1
  • monitori: 3
  • fps: 5
  • avila: 2
  • ffl: 4
```

## 🔐 Segurança

- Apenas o número cadastrado como ADMIN_PHONE_NUMBER tem acesso total
- Usuários são isolados por grupo
- Verificação obrigatória na primeira interação
- Logs de todas as interações

## 🛠️ Próximos Passos

1. **Implementar ferramentas específicas:**
   - [ ] Integração Mitto para Monitori
   - [ ] Sistema de calendário para FPS
   - [ ] Upload de casos clínicos para FPS
   - [ ] Modo demo completo para Ávila

2. **Melhorias:**
   - [ ] Dashboard web para admin
   - [ ] Exportação de relatórios
   - [ ] Notificações automáticas
   - [ ] Sistema de backup

## 📞 Suporte

Para questões técnicas, contate o administrador pelo WhatsApp: +5511991668852

---

**Desenvolvido por:** Fred Amaral Jr
**Data:** Outubro 2025
**Versão:** 2.0 - Multi-Tenant
