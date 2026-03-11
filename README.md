# IAM Access Review – Ferramenta de Revisão de Acessos

Ferramenta interna para comparar usuários do diretório corporativo com listas de acesso em aplicações e identificar acessos indevidos, obsoletos ou sem correspondência.

## Funcionalidades

- **Upload**: CSV e Excel (usuários corporativos + usuários por ferramenta/aplicação)
- **Padronização**: Mapeamento automático de colunas (nome, e-mail, login)
- **Comparação**: Por nome, e-mail e login
- **Classificação**:
  - OK
  - Remover com prioridade
  - Possível remoção
  - Revisão manual
  - Acesso obsoleto
- **Dashboard**: Métricas e filtros por aplicação
- **Exportação**: CSV, Excel, resumo executivo (texto) e **apresentação em PowerPoint (PPTX)**
- **Modelos de planilha**: Download de modelos (CSV/Excel) para preencher corretamente a base corporativa e as ferramentas
- **Idiomas**: Interface em Português (Brasil) e English (US)

## Configuração

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Executar

```bash
streamlit run app.py
```

Ou com Make: `make run` (após `make install`).

Abra o endereço exibido no terminal (padrão: http://localhost:8501).

## Estrutura do projeto

```
iam-access-review/
├── app.py           # Interface Streamlit
├── comparator.py    # Lógica de comparação e classificação
├── utils.py         # Leitura de arquivos e normalização de colunas
├── i18n.py          # Textos em PT-BR e EN-US
├── ppt_export.py    # Geração da apresentação executiva (PPTX)
├── templates/       # Modelos de planilha para download (corporativo e ferramenta)
├── sample_data/     # Arquivos de exemplo para teste
├── outputs/         # Relatórios exportados (ignorado pelo git)
├── requirements.txt
├── Makefile
└── README.md
```

## Dados de exemplo

Use ou coloque arquivos em `sample_data/`:

1. **Usuários corporativos**: Um arquivo com usuários ativos do AD/diretório corporativo (colunas: nome, e-mail, login ou equivalentes).
2. **Ferramentas/aplicações**: Um ou mais arquivos — cada arquivo = uma ferramenta. O nome do arquivo identifica a fonte (ex.: `Sistema_RH.csv`, `Portal_Financeiro.xlsx`).

Os nomes de coluna são normalizados automaticamente (ex.: "e-mail", "email", "usuário" → email).  
**Acentuação:** o app tenta várias codificações ao ler CSV (UTF-8, CP1252, Latin-1). Prefira salvar planilhas em **UTF-8** (no Excel: "CSV UTF-8" ou .xlsx) para que nomes e e-mails com acento (ã, é, ç, etc.) apareçam corretamente. As saídas (CSV, Excel, TXT, PPT) são geradas em UTF-8.

## Modelos de planilha

Na barra lateral do app, use o expander **Modelos de planilha** para baixar:

- **Corporativo (CSV/Excel)**: modelo com colunas `nome`, `email`, `login` para a base principal de usuários ativos.
- **Ferramenta (CSV/Excel)**: modelo para cada planilha de ferramenta/aplicação (mesmas colunas; o nome do arquivo no upload identifica a fonte).

Preencha os modelos com seus dados e faça o upload no app.

## Apresentação executiva (PPTX)

Após rodar a comparação, na área **Exportar** é possível baixar uma apresentação em PowerPoint com:

- Slide de título (Revisão de Acessos IAM + data)
- Slide de métricas por classificação
- Slide de resumo executivo e recomendações

O idioma da apresentação segue o idioma selecionado na interface.

## Subir para o seu Git (GitHub, GitLab, etc.)

1. **Crie um repositório novo** no GitHub/GitLab (vazio, sem README).

2. **Inicialize e envie da sua máquina:**

```bash
cd iam-access-review
git init
git add .
git commit -m "Initial commit: IAM Access Review tool"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/iam-access-review.git
git push -u origin main
```

Substitua `SEU_USUARIO/iam-access-review` pelo seu **usuário/nome-do-repo**.  
Se usar SSH: `git remote add origin git@github.com:SEU_USUARIO/iam-access-review.git`

## Licença

Uso interno.
