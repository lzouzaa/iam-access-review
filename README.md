# IAM Access Review

Ferramenta para revisar acessos IAM comparando usuários do diretório corporativo com usuários de uma ou mais ferramentas/aplicações.

## O que o app faz

- Faz upload de planilhas CSV/XLSX.
- Normaliza colunas automaticamente (`nome`, `email`, `login`, `application`).
- Compara base corporativa (referência) vs. bases de ferramentas.
- Classifica cada linha em:
  - `OK`
  - `Remover com prioridade`
  - `Possível remoção`
  - `Revisão manual`
  - `Acesso obsoleto`
- Exibe dashboard com métricas e filtros.
- Exibe dashboard de usuários fora do padrão por aplicação.
- Exporta CSV, Excel, resumo TXT e apresentação PPTX.

## Regra de comparação (resumo)

A planilha corporativa é a base de referência.

- Se houver match por `login` ou `email`, o registro é considerado válido (`OK`).
- Se houver match apenas por `nome`, classifica como `Possível remoção`.
- Se não houver match por nenhum identificador, classifica como `Remover com prioridade`.
- Duplicidade dentro da mesma aplicação pode virar `Acesso obsoleto`.

## Requisitos

- Python 3.10+
- `pip`

## Rodar na sua máquina (passo a passo)

No terminal, dentro da pasta do projeto:

```bash
cd /caminho/para/iam-access-review
make install
.venv/bin/streamlit run app.py
```

Se preferir sem `make`:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run app.py
```

Abra no navegador:

- `http://localhost:8501`

Observação: no primeiro uso, o Streamlit pode pedir e-mail no terminal. Pode só apertar `Enter` em branco.

## Como usar no app

1. No sidebar, suba 1 arquivo de **Usuários ativos (base principal)**.
2. Suba 1 ou mais arquivos de **Ferramentas/aplicações**.
3. Clique em **Executar comparação**.
4. Analise:
   - Cards de classificação
   - Dashboard de fora do padrão por aplicação
   - Tabela detalhada e filtros
5. Baixe os relatórios em **Exportar**.

## Teste rápido com dados de exemplo

Você pode testar com os arquivos em `sample_data/`:

- `sample_data/teste_corporativo.csv`
- `sample_data/teste_sistema.csv`

Ou executar um teste rápido no terminal:

```bash
.venv/bin/python - <<'PY'
from utils import load_file
from comparator import compare, summary_stats

corp = load_file(file_path='sample_data/teste_corporativo.csv')
app = load_file(file_path='sample_data/teste_sistema.csv')
app['application'] = 'teste_sistema'
review = compare(corp, app)

print('=== RESUMO ===')
print(summary_stats(review).to_string())
print('\n=== DETALHE ===')
print(review[['name','email','login','match_type','classification']].to_string(index=False))
PY
```

## Estrutura do projeto

```text
iam-access-review/
├── app.py
├── comparator.py
├── utils.py
├── i18n.py
├── ppt_export.py
├── templates/
├── sample_data/
├── requirements.txt
├── Makefile
└── README.md
```

## Exportações

- CSV completo do resultado
- Excel completo do resultado
- TXT com resumo executivo
- PPTX executivo com:
  - métricas por classificação
  - resumo e recomendações
  - ferramentas e quantidade de usuários recomendados para remoção

## Problemas comuns

- `ModuleNotFoundError`:
  - Execute `make install` e rode usando `.venv/bin/streamlit`.
- Porta ocupada:
  - Rode `streamlit run app.py --server.port 8502`.
- Acentuação quebrada:
  - Prefira CSV UTF-8 ou XLSX.

## Subir para o GitHub

```bash
git add .
git commit -m "Update README and IAM access review improvements"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/iam-access-review.git
git push -u origin main
```

Se o `origin` já existir:

```bash
git remote set-url origin https://github.com/SEU_USUARIO/iam-access-review.git
git push -u origin main
```

## Licença

Uso interno.
