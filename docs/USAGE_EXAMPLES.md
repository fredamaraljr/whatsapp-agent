# Exemplos Práticos de Uso - Sistema Multi-Tenant

## 📱 Exemplos de Conversas por Grupo

### 1. Admin (Fred)

#### Exemplo 1: Ver Estatísticas

```
👤 Fred: /stats

🤖 Ava: 📊 **Estatísticas do Sistema**

👥 Total de usuários: 15
💬 Total de mensagens: 234
🕐 Interações (24h): 45

**Usuários por grupo:**
  • admin: 1
  • monitori: 3
  • fps: 5
  • avila: 2
  • ffl: 4
```

#### Exemplo 2: Customizar Prompt

```
👤 Fred: /setprompt monitori
Você é um especialista em análise de dados da Monitori.
Sempre use gráficos e números nas suas explicações.
Seja direto e focado em ROI.

🤖 Ava: ✅ Prompt atualizado para o grupo 'monitori'
```

#### Exemplo 3: Ver Configuração

```
👤 Fred: /getprompt ffl

🤖 Ava: 📝 **Prompt do grupo 'ffl':**

Você é Ava, uma ex-pilota de Airbus A320...
[prompt completo]

_Atualizado em: 2025-10-15T14:30:00_
```

### 2. Monitori (Análise de Dados)

#### Primeira Interação

```
👤 Cliente: Olá

🤖 Ava: Olá! Seja bem-vindo(a)! 👋

Para que eu possa oferecer o melhor atendimento, preciso saber
um pouco mais sobre você.

Você é:
1️⃣ Cliente da Monitori
2️⃣ Estudante da FPS
3️⃣ Colaborador da Ávila Digital
4️⃣ Piloto ou interessado em aviação

Por favor, responda com o número da opção que melhor se aplica a você.

👤 Cliente: 1

🤖 Ava: Ótimo! Você foi identificado como cliente Monitori.
Posso ajudá-lo com análises de dados e insights. Como posso ajudar hoje?
```

#### Conversa Normal

```
👤 Cliente: Preciso analisar as vendas do último trimestre

🤖 Ava: Claro! Vou buscar os dados de vendas do Q3 para você.
Para fazer uma análise completa, preciso saber:

1. Qual região você quer analisar?
2. Quer comparar com o trimestre anterior?
3. Há alguma métrica específica de interesse (receita, volume, ticket médio)?
```

### 3. FPS (Estudantes de Medicina)

#### Consulta sobre Provas

```
👤 Estudante: Quando é a próxima prova de cardiologia?

🤖 Ava: Consultando o calendário acadêmico...

📅 Próxima Prova de Cardiologia:
- Data: 28 de Outubro, 2025
- Horário: 14h00
- Local: Auditório Principal
- Conteúdo: Módulos 1-4

Boa sorte nos estudos! Precisa revisar algum caso clínico?
```

#### Discussão de Caso Clínico

```
👤 Estudante: Me explica sobre infarto agudo do miocárdio

🤖 Ava: Vamos revisar IAM!

📚 **Infarto Agudo do Miocárdio (IAM)**

**Definição:** Necrose do músculo cardíaco causada por isquemia prolongada...

**Quadro Clínico:**
- Dor torácica em aperto
- Irradiação para braço esquerdo/mandíbula
- Náuseas, sudorese
- Dispneia

**Diagnóstico:**
- ECG: Supra de ST
- Marcadores: Troponina ↑
- Clínica compatível

Quer discutir o tratamento ou algum caso específico?
```

### 4. Ávila Digital (Demonstração)

#### Modo Apresentação

```
👤 Prospect: O que você pode fazer?

🤖 Ava: Olá! Sou uma demonstração das capacidades de IA da Ávila Digital! 🚀

Posso mostrar como agentes de IA funcionam em diferentes contextos:

🔹 Análise de Dados (como Monitori)
🔹 Educação Médica (como FPS)
🔹 Aviação Técnica (como FFL)

Também posso:
- Responder perguntas em linguagem natural
- Gerar conteúdo contextualizado
- Manter conversas coerentes
- Aprender com interações

Gostaria de ver uma simulação? Diga "simule o grupo [nome]"
```

#### Modo Simulação

```
👤 Colaborador: simule o grupo monitori

🤖 Ava: 🎭 **Modo Demonstração: Monitori**

Agora estou simulando como atenderia um cliente de análise de dados.

Posso ajudá-lo com:
- Dashboard de vendas
- Análise de métricas
- Insights de negócio
- Relatórios customizados

[Esta é uma simulação para demonstração. Em produção, teria
acesso real aos dados via Mito]

O que gostaria de analisar?
```

### 5. FFL (Aviação)

#### Consulta Técnica

```
👤 Piloto: Como funciona o sistema APU do A320?

🤖 Ava: Ótima pergunta! Vou buscar nos manuais...

✈️ **APU (Auxiliary Power Unit) - A320**

Segundo o **FCOM Seção 1.49.10**:

O APU é uma turbina a gás que fornece:
- Pneumático para start dos motores e ar condicionado
- Energia elétrica (115V AC / 400Hz)
- Pode operar até FL 410

**Limitações (MEL 49-10):**
- Start no solo: até ISA +40°C
- Start em voo: até 25,000 ft
- Bleed: até 20,000 ft

**Procedimento de Start:**
1. APU MASTER SW - ON
2. APU START - ON
3. Aguardar APU AVAIL (45-60 seg)

Citando o FCTM PR-AEP-APU: "O APU start normal leva
aproximadamente 50 segundos."

Tem alguma dúvida específica sobre operação ou limitações?
```

#### Discussão de Procedimento

```
👤 Piloto: Explica o procedimento de engine failure após V1

🤖 Ava: Procedimento crítico! Vamos revisar...

🚨 **ENGINE FAILURE AFTER V1**

**Segundo FCTM PR-ABN-ENG:**

**Imediato (PF):**
1. Continue takeoff
2. Rotate at VR (normal rate)
3. Target V2 + 10 to 15 kt
4. Maintain runway heading

**PNF:**
1. "ENGINE FAILURE"
2. Silence warnings

**Após positivo:**
1. "GEAR UP"
2. Retract flaps on schedule
3. Clean up normally

**Importante do FCOM 3.02.21:**
- Não tentar relight até estável acima 400 ft
- Manter V2+10 mínimo até obstáculos clear
- Single engine ceiling: consultar performance

Na sua experiência, qual é a maior preocupação nesse cenário?
```

## 🎯 Casos de Uso Específicos

### Admin: Modificar Comportamento

```
# Admin quer que Monitori seja mais técnico
👤 Fred: /setprompt monitori
Você é um data scientist sênior. Use:
- Terminologia técnica (SQL, Python, ML)
- Métricas estatísticas (p-value, R², etc)
- Recomende análises avançadas
- Seja preciso com números

🤖 Ava: ✅ Prompt atualizado para o grupo 'monitori'

# Agora clientes Monitori terão respostas mais técnicas
```

### FPS: Upload de Novo Material

```
👤 Fred: [enviando PDF de casos clínicos]
Adiciona esses casos clínicos para os alunos da FPS

🤖 Ava: ✅ Casos clínicos recebidos!

Processando PDF...
- Extraindo texto
- Criando embeddings
- Adicionando ao banco de conhecimento

Concluído! Os estudantes da FPS agora têm acesso a:
- 15 novos casos clínicos
- Total de 47 casos no banco

Os casos foram indexados e podem ser consultados normalmente.
```

### Ávila: Demo Personalizada

```
👤 Prospect: Mostre análise de dados

🤖 Ava: 🎭 Demonstração: Análise de Dados

Imagine que você é um gerente de vendas e quer entender
o desempenho da equipe...

👤 Prospect: Quais foram as vendas de ontem?

🤖 Ava: [Simulando busca no Mito]

📊 **Vendas - 14/10/2025**

Total: R$ 45.230,00 (+12% vs. dia anterior)

Por região:
- Sul: R$ 18.500 (41%)
- Sudeste: R$ 15.800 (35%)
- Nordeste: R$ 10.930 (24%)

Top vendedor: João Silva (R$ 8.200)

[DEMO: Em produção real, esses dados viriam do seu banco
via integração Mito]

Legal, né? É assim que funciona para clientes Monitori!
```

## 📊 Comandos Admin em Diferentes Contextos

### Debugging de Usuário Específico

```python
# Admin pode executar queries personalizadas
👤 Fred: /config query=SELECT * FROM users WHERE user_group='fps'

🤖 Ava: ⚙️ Executando query...

Resultado:
+-------------------+-------+----------+----------------+
| phone_number      | group | messages | last_contact   |
+-------------------+-------+----------+----------------+
| +5581988776655    | fps   | 45       | 2h ago        |
| +5581977665544    | fps   | 23       | 5h ago        |
| +5581966554433    | fps   | 67       | 30m ago       |
+-------------------+-------+----------+----------------+

Total: 3 usuários FPS
```

### Monitoramento em Tempo Real

```
👤 Fred: /stats

🤖 Ava: 📊 **Estatísticas do Sistema**

👥 Total de usuários: 23
💬 Total de mensagens: 567
🕐 Interações (24h): 89

**Atividade por hora:**
12h: ████████░░ 34 msgs
13h: ██████████ 45 msgs
14h: ████░░░░░░ 18 msgs (agora)

**Grupos mais ativos:**
1. FPS: 156 msgs (27%)
2. FFL: 134 msgs (24%)
3. Monitori: 89 msgs (16%)
```

## 🔧 Troubleshooting com Admin

### Usuário com Problema

```
👤 Fred: /users +5511999887766

🤖 Ava: 📋 **Detalhes do Usuário**

Phone: +5511999887766
Grupo: monitori
Verificado: ✅ Sim
Primeira interação: 10/10/2025 14:30
Última interação: 15/10/2025 09:15
Total de mensagens: 23

**Últimas 5 interações:**
1. 15/10 09:15 - "Mostre vendas"
2. 15/10 09:12 - "Bom dia"
3. 14/10 16:45 - "Obrigado"
4. 14/10 16:40 - "Explica dashboard"
5. 14/10 11:20 - "Olá"

Tudo normal! Usuário ativo e engajado.
```

## 📱 Fluxos Completos

### Novo Cliente Monitori (Completo)

```
# Dia 1 - Primeira Mensagem
👤 Cliente: Bom dia

🤖 Ava: Olá! Seja bem-vindo(a)! 👋 [pergunta de verificação]

👤 Cliente: 1

🤖 Ava: Ótimo! Você foi identificado como cliente Monitori...

# Dia 2 - Uso Normal
👤 Cliente: Olá

🤖 Ava: Olá! Tudo bem? Como posso ajudar com suas análises hoje?

👤 Cliente: Quero ver o desempenho das vendas

🤖 Ava: Perfeito! [análise de dados]

# Dia 30 - Usuário Frequente
👤 Cliente: Ava, análise rápida

🤖 Ava: Claro! Já sei o que você gosta de ver.
Buscando dados mais recentes...
```

---

**Nota:** Todos esses exemplos são baseados no código implementado e podem ser testados após a migração do sistema!
