"""
Utilities for file loading and column normalization.
"""
import re
from pathlib import Path
from typing import Optional

import pandas as pd

# Standard column names after normalization
STANDARD_COLUMNS = {"name", "email", "login", "application"}

# Aliases for automatic mapping (lowercase, strip)
COLUMN_ALIASES = {
    "name": ["nome", "name", "nome completo", "full name", "usuario", "user", "nome do usuario"],
    "email": ["email", "e-mail", "e_mail", "mail", "correio", "usuário", "usuario"],
    "login": ["login", "username", "user_id", "userid", "uid", "matricula", "cpf", "id"],
    "application": ["aplicacao", "application", "app", "sistema", "sistema aplicacao"],
}


def _normalize_header(col: str) -> str:
    """Normalize column name for matching: lowercase, strip, collapse spaces."""
    if not isinstance(col, str):
        col = str(col)
    s = col.lower().strip()
    s = re.sub(r"\s+", " ", s)
    return s


def map_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Map dataframe columns to standard names (name, email, login, application).
    Original columns are kept; standard columns are added/overwritten.
    """
    result = df.copy()
    result.columns = [str(c) for c in result.columns]
    normalized_headers = {_normalize_header(c): c for c in result.columns}

    for std_col, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in normalized_headers:
                orig = normalized_headers[alias]
                if std_col not in result.columns or result[std_col].equals(result[orig]):
                    result[std_col] = result[orig].astype(str).str.strip()
                break

    # Ensure standard columns exist (fill with empty string if missing)
    for col in STANDARD_COLUMNS:
        if col not in result.columns:
            result[col] = ""

    return result


def load_file(file_path: Optional[Path] = None, uploaded_file=None) -> pd.DataFrame:
    """
    Load CSV or Excel file from path or Streamlit UploadedFile.
    Returns normalized dataframe with standard columns.
    """
    if file_path is not None:
        path = Path(file_path)
        suffix = path.suffix.lower()
        if suffix == ".csv":
            df = pd.read_csv(path, encoding="utf-8", on_bad_lines="skip")
        elif suffix in (".xlsx", ".xls"):
            df = pd.read_excel(path, engine="openpyxl" if suffix == ".xlsx" else None)
        else:
            raise ValueError(f"Unsupported format: {suffix}. Use .csv or .xlsx")
    elif uploaded_file is not None:
        suffix = Path(uploaded_file.name).suffix.lower()
        if suffix == ".csv":
            df = pd.read_csv(uploaded_file, encoding="utf-8", on_bad_lines="skip")
        elif suffix in (".xlsx", ".xls"):
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        else:
            raise ValueError(f"Unsupported format: {suffix}. Use .csv or .xlsx")
    else:
        raise ValueError("Provide file_path or uploaded_file")

    return map_columns(df)


def ensure_output_dir() -> Path:
    """Create outputs directory if it does not exist."""
    out = Path("outputs")
    out.mkdir(exist_ok=True)
    return out
