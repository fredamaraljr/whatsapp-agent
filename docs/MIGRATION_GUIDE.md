# Guia de Migração para Sistema Multi-Tenant

## 📋 Checklist de Migração

### Antes de Começar

- [ ] Backup completo do banco de dados atual
- [ ] Backup dos arquivos de configuração (.env)
- [ ] Backup do código anterior
- [ ] Documentar usuários ativos atuais

### 1. Atualização do Código

```bash
# 1. Fazer backup do código atual
cd /app
cp -r . ../backup_$(date +%Y%m%d)

# 2. Pull das novas mudanças
git pull origin main

# 3. Instalar novas dependências (se houver)
pip install -e .
```

### 2. Configurar Variáveis de Ambiente

Adicionar ao arquivo `.env`:

```env
# === NOVO: User Management ===
ADMIN_PHONE_NUMBER=+5511991668852
USER_DB_PATH=/app/data/users.db

# === NOVO: Monitori Integration ===
MITTO_API_KEY=your_mitto_api_key_here
MITTO_DATABASE_URL=your_database_connection_string

# === NOVO: FPS Configuration ===
FPS_CALENDAR_PATH=/app/data/fps_calendar.json
FPS_CLINICAL_CASES_PATH=/app/knowledge/fps_clinical_cases

# === Existentes (manter) ===
GROQ_API_KEY=...
ELEVENLABS_API_KEY=...
# ... resto das configurações
```

### 3. Criar Estrutura de Diretórios

```bash
# Criar diretórios necessários
mkdir -p /app/data
mkdir -p /app/knowledge/fps_clinical_cases

# Definir permissões
chmod 755 /app/data
chmod 755 /app/knowledge/fps_clinical_cases
```

### 4. Migrar Dados Existentes

#### Script de Migração de Usuários

Criar arquivo `scripts/migrate_users.py`:

```python
"""
Script para migrar usuários existentes para o novo sistema multi-tenant.
"""
import sqlite3
from datetime import datetime
from ai_companion.settings import settings
from ai_companion.modules.user_management import UserManager, UserGroup

def migrate_existing_users():
    """Migra usuários do sistema antigo para o novo."""

    # Conectar ao banco antigo
    old_db = sqlite3.connect(settings.SHORT_TERM_MEMORY_DB_PATH)
    old_cursor = old_db.cursor()

    # Inicializar novo user manager
    user_manager = UserManager(settings.USER_DB_PATH)

    # Buscar números de telefone únicos do sistema antigo
    # (adapte a query conforme sua estrutura anterior)
    old_cursor.execute("""
        SELECT DISTINCT thread_id FROM checkpoints
    """)

    phone_numbers = [row[0] for row in old_cursor.fetchall()]

    print(f"Encontrados {len(phone_numbers)} números de telefone")

    # Para cada número, criar registro com grupo FFL (padrão anterior)
    for phone in phone_numbers:
        if phone == settings.ADMIN_PHONE_NUMBER:
            # Admin
            user = user_manager.create_user(phone, settings.ADMIN_PHONE_NUMBER)
            print(f"✓ Migrado admin: {phone}")
        else:
            # Criar como FFL (comportamento padrão anterior)
            user = user_manager.create_user(phone, settings.ADMIN_PHONE_NUMBER)
            user_manager.verify_user(phone, UserGroup.FFL)
            print(f"✓ Migrado usuário FFL: {phone}")

    old_db.close()
    print(f"\n✅ Migração concluída: {len(phone_numbers)} usuários")

if __name__ == "__main__":
    migrate_existing_users()
```

Executar migração:

```bash
python scripts/migrate_users.py
```

### 5. Testar o Sistema

#### Teste 1: Admin

```
Enviar de: +5511991668852
Mensagem: /help

Esperado: Lista de comandos administrativos
```

#### Teste 2: Novo Usuário

```
Enviar de: +5511999999999 (número novo)
Mensagem: Olá

Esperado: Pergunta de identificação de grupo
```

#### Teste 3: Verificação de Grupo

```
Enviar de: mesmo número acima
Mensagem: 4

Esperado: Confirmação como FFL e ativação de features
```

#### Teste 4: Usuário Existente

```
Enviar de: número já migrado
Mensagem: Qualquer mensagem

Esperado: Resposta normal sem pergunta de verificação
```

### 6. Verificar Banco de Dados

```bash
# Acessar banco de dados
sqlite3 /app/data/users.db

# Ver usuários
SELECT * FROM users;

# Ver estatísticas
SELECT user_group, COUNT(*) FROM users GROUP BY user_group;

# Sair
.quit
```

### 7. Monitoramento Pós-Migração

```bash
# Ver logs em tempo real
tail -f /app/logs/app.log

# Filtrar erros
tail -f /app/logs/app.log | grep ERROR

# Ver interações de usuários
sqlite3 /app/data/users.db "SELECT * FROM interaction_log ORDER BY timestamp DESC LIMIT 10;"
```

## 🔄 Rollback (se necessário)

Se algo der errado, reverter:

```bash
# 1. Parar o serviço
docker-compose down

# 2. Restaurar código anterior
cd /app
rm -rf *
cp -r ../backup_YYYYMMDD/* .

# 3. Restaurar .env
cp ../backup_YYYYMMDD/.env .

# 4. Reiniciar
docker-compose up -d
```

## 📊 Validação Final

### Checklist de Validação

- [ ] Admin consegue executar comandos (`/stats`, `/help`)
- [ ] Novos usuários recebem pergunta de verificação
- [ ] Verificação de grupo funciona corretamente
- [ ] Usuários migrados mantêm histórico
- [ ] Prompts específicos são aplicados por grupo
- [ ] Banco de dados está sendo atualizado
- [ ] Logs estão sendo gerados
- [ ] Não há erros críticos nos logs

### Comandos de Validação

```bash
# 1. Verificar estrutura do banco
sqlite3 /app/data/users.db ".schema"

# 2. Contar usuários por grupo
sqlite3 /app/data/users.db "SELECT user_group, COUNT(*) as count FROM users GROUP BY user_group;"

# 3. Ver últimas interações
sqlite3 /app/data/users.db "SELECT phone_number, timestamp, message_type FROM interaction_log ORDER BY timestamp DESC LIMIT 5;"

# 4. Verificar admin
sqlite3 /app/data/users.db "SELECT * FROM users WHERE user_group='admin';"
```

## 🐛 Troubleshooting

### Problema: Usuários não são identificados

**Solução:**

```bash
# Verificar se user_phone está sendo passado
tail -f logs/app.log | grep "user_phone"

# Verificar webhook
tail -f logs/app.log | grep "whatsapp_handler"
```

### Problema: Banco de dados não é criado

**Solução:**

```bash
# Verificar permissões
ls -la /app/data/

# Criar manualmente se necessário
touch /app/data/users.db
chmod 666 /app/data/users.db

# Reiniciar aplicação
docker-compose restart
```

### Problema: Prompts não mudam por grupo

**Solução:**

```python
# Testar chains.py
python -c "
from ai_companion.graph.utils.chains import get_prompt_for_group
print(get_prompt_for_group('admin'))
print(get_prompt_for_group('monitori'))
"
```

### Problema: Admin não consegue executar comandos

**Solução:**

```bash
# Verificar ADMIN_PHONE_NUMBER no .env
grep ADMIN_PHONE_NUMBER .env

# Verificar no banco
sqlite3 /app/data/users.db "SELECT * FROM users WHERE phone_number='${ADMIN_PHONE_NUMBER}';"

# Forçar criação do admin
python -c "
from ai_companion.modules.user_management import UserManager
from ai_companion.settings import settings
um = UserManager(settings.USER_DB_PATH)
um.create_user(settings.ADMIN_PHONE_NUMBER, settings.ADMIN_PHONE_NUMBER)
"
```

## 📝 Notas Importantes

1. **Backup Regular**: Configurar backup automático do banco de dados

   ```bash
   # Adicionar ao crontab
   0 */6 * * * cp /app/data/users.db /app/backups/users_$(date +\%Y\%m\%d_\%H\%M).db
   ```

2. **Monitoramento**: Configurar alertas para erros

   ```bash
   # Exemplo com script de monitoramento
   watch -n 60 'tail -100 /app/logs/app.log | grep -c ERROR'
   ```

3. **Documentação**: Manter documentação atualizada
   - Atualizar README.md principal
   - Documentar customizações específicas
   - Manter changelog

## ✅ Pós-Migração

### Próximos Passos

1. **Comunicar Mudanças**

   - Informar usuários existentes sobre novo sistema
   - Enviar instruções de uso para cada grupo

2. **Treinar Admin**

   - Demonstrar comandos administrativos
   - Explicar como customizar prompts
   - Mostrar como visualizar estatísticas

3. **Monitorar por 1 Semana**

   - Verificar logs diariamente
   - Responder rapidamente a problemas
   - Coletar feedback dos usuários

4. **Otimizar**
   - Ajustar prompts baseado em feedback
   - Melhorar mensagens de verificação
   - Adicionar features específicas solicitadas

## 🆘 Suporte

Em caso de problemas durante a migração:

1. **Documentar o erro**: Copiar mensagem de erro completa
2. **Verificar logs**: `tail -100 /app/logs/app.log`
3. **Consultar troubleshooting** acima
4. **Contatar suporte**: Incluir erro e logs na mensagem

---

**Data de Criação:** Outubro 2025
**Versão:** 1.0
**Autor:** Fred Amaral Jr
