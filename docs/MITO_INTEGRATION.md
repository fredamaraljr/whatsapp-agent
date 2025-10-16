# Integração Mito - Análise de Dados para Monitori

## Visão Geral

O módulo de integração Mito permite que usuários do grupo **Monitori** façam análises de dados poderosas através de conversação natural com a IA.

## Características

### 🎯 Capacidades

1. **Análise Exploratória**

   - Carregar dados de CSV, Excel, JSON
   - Visualizar estrutura e estatísticas
   - Identificar valores ausentes

2. **Transformações de Dados**

   - Filtros e seleções
   - Agregações e agrupamentos
   - Pivot tables e reshaping

3. **Visualizações**

   - Gráficos interativos
   - Charts customizáveis
   - Dashboards

4. **Geração de Código**
   - Código pandas automático
   - Exportável e reutilizável
   - Reproduzível

## Como Usar

### 1. Via WhatsApp/Chainlit (Grupo Monitori)

```
Usuário: Preciso analisar os dados de vendas
IA: Entendi! Posso ajudar com análise de dados.
    Por favor, envie o arquivo CSV ou Excel com os dados de vendas.
```

### 2. Tipos de Análise Reconhecidas

- **Visualização**: "mostre um gráfico", "crie uma visualização"
- **Filtragem**: "filtre os dados", "mostre apenas"
- **Agregação**: "agrupe por", "calcule a média"
- **Limpeza**: "remova valores nulos", "preencha dados faltantes"
- **Merge**: "combine as tabelas", "faça um join"

### 3. Exemplo de Fluxo Completo

```
Usuário: Quero analisar dados de vendas por região

IA: Perfeito! Para análise de vendas por região, preciso do arquivo de dados.
    Formatos aceitos: CSV, Excel (.xlsx), JSON

[Usuário envia arquivo vendas.csv]

IA: Dados carregados com sucesso!
    - 1.250 registros
    - 8 colunas: data, produto, região, valor, quantidade, vendedor, categoria, status
    - 3 regiões identificadas: Sul, Sudeste, Nordeste

    Análises sugeridas:
    1. Total de vendas por região
    2. Produto mais vendido em cada região
    3. Evolução de vendas ao longo do tempo

    Qual análise você gostaria de ver primeiro?

Usuário: Total de vendas por região

IA: Análise concluída! Aqui está o resumo:

    Sul:      R$ 2.450.000 (35%)
    Sudeste:  R$ 3.120.000 (45%)
    Nordeste: R$ 1.390.000 (20%)

    Gerei também um código Python que você pode usar:
    [código pandas gerado]

    Deseja que eu crie um gráfico desta análise?
```

## Estrutura de Arquivos

```
data/
  mito_workspace/
    analysis_001.csv      # Resultado de análises
    analysis_001.xlsx     # Exportações
    generated_code.py     # Código Python gerado
```

## Código Python Gerado

O Mito gera automaticamente código pandas para todas as operações. Exemplo:

```python
import pandas as pd
from mitosheet.public.v3 import *

# Carregar dados
df = pd.read_csv('vendas.csv')

# Agrupar por região e somar valores
df_grouped = df.groupby('região')['valor'].sum()

# Criar visualização
df_grouped.plot(kind='bar', title='Vendas por Região')
```

## Usando Mito Interativamente

Para análises mais complexas, o usuário pode usar Mito no Jupyter:

```python
import mitosheet
mitosheet.sheet()
```

Isso abre uma interface tipo Excel onde:

- Todas as operações são visuais (drag & drop)
- O código Python é gerado automaticamente
- Fácil de compartilhar e reproduzir análises

## Configuração

No `.env`, adicione:

```env
# Mito Configuration
MITO_WORKSPACE_PATH=/app/data/mito_workspace
MITTO_API_KEY=your_mitto_api_key_here
```

## Dependências

Adicionadas ao `pyproject.toml`:

- `mitosheet>=0.1.0`
- `pandas>=2.0.0`
- `openpyxl>=3.1.0`

## Exemplos de Uso

### Análise de Vendas

```python
from ai_companion.modules.mito_integration import MitoHandler

mito = MitoHandler()

# Analisar requisição do usuário
result = await mito.analyze_data_request(
    user_message="Mostre vendas por produto",
    context={"file_path": "vendas.csv"}
)

# Gerar código
operations = [
    {"type": "load", "file_path": "vendas.csv"},
    {"type": "group_by", "group_column": "produto",
     "agg_column": "valor", "aggregation": "sum"}
]
code = await mito.generate_mito_code(operations)
```

## Limitações e Próximos Passos

### Limitações Atuais

- Arquivos devem ser enviados pelo usuário
- Análises síncronas (não streaming)
- Visualizações estáticas (não interativas no chat)

### Roadmap

- [ ] Upload de arquivos via WhatsApp
- [ ] Integração com Google Sheets
- [ ] Dashboards interativos
- [ ] Agendamento de análises recorrentes
- [ ] Alertas baseados em dados
- [ ] ML/AI insights automáticos

## Suporte

Para mais informações sobre Mito:

- [Documentação Oficial](https://docs.trymito.io/)
- [GitHub](https://github.com/mito-ds/mito)
- [Exemplos](https://docs.trymito.io/how-to)
