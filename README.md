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
- **Exportação**: CSV, Excel e resumo executivo (texto)
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
