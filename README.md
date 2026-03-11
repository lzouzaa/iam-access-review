# IAM Access Review Tool

Internal tool for comparing corporate directory users with application access lists to identify improper, obsolete, or unmatched access.

## Features

- **Upload**: CSV and Excel (corporate users + application users)
- **Standardization**: Automatic column mapping (name, email, login)
- **Comparison**: By name, email, and login
- **Classification**:
  - OK
  - Remover com prioridade
  - Possível remoção
  - Revisão manual
  - Acesso obsoleto
- **Dashboard**: Metrics and filters by application
- **Export**: CSV, Excel, and executive summary (text)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

Or with Make: `make run` (after `make install`).

Open the URL shown in the terminal (default: http://localhost:8501).

## Project structure

```
iam-access-review/
├── app.py           # Streamlit UI
├── comparator.py    # Comparison and classification logic
├── utils.py         # File load and column normalization
├── sample_data/     # Example files for testing
├── outputs/         # Exported reports (gitignored)
├── requirements.txt
└── README.md
```

## Sample data

Place or use files in `sample_data/`:

1. **Corporate users**: Active users from AD/corporate directory (columns: name, email, login or similar).
2. **Application users**: Active users per application (columns: name, email, login, application or similar).

Column names are normalized automatically (e.g. "e-mail", "email", "usuário" → email).

## Push to your Git (GitHub, GitLab, etc.)

1. **Create a new repository** on GitHub/GitLab (empty, no README).

2. **Initialize and push from your machine:**

```bash
cd iam-access-review
git init
git add .
git commit -m "Initial commit: IAM Access Review tool"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/iam-access-review.git
git push -u origin main
```

Replace `SEU_USUARIO/iam-access-review` with your actual **username/repo-name**.  
If you use SSH: `git remote add origin git@github.com:SEU_USUARIO/iam-access-review.git`

## License

Internal use only.
