"""
Comparison and classification logic for IAM access review.
"""
from typing import List, Tuple

import pandas as pd

CLASS_OK = "OK"
CLASS_REMOVER_PRIORIDADE = "Remover com prioridade"
CLASS_POSSIVEL_REMOCAO = "Possível remoção"
CLASS_REVISAO_MANUAL = "Revisão manual"
CLASS_ACESSO_OBSOLETO = "Acesso obsoleto"

CLASSIFICATION_ORDER = [
    CLASS_OK,
    CLASS_REMOVER_PRIORIDADE,
    CLASS_POSSIVEL_REMOCAO,
    CLASS_REVISAO_MANUAL,
    CLASS_ACESSO_OBSOLETO,
]


def _normalize_value(val: str) -> str:
    """Normalize for comparison: strip, lower, collapse spaces."""
    if pd.isna(val) or val is None:
        return ""
    s = str(val).strip().lower()
    return " ".join(s.split())


def _build_lookup(df: pd.DataFrame) -> dict:
    """Build lookup by login, email, name. Keys are normalized; value is index (first occurrence)."""
    by_login, by_email, by_name = {}, {}, {}
    for idx, row in df.iterrows():
        login = _normalize_value(row.get("login", ""))
        email = _normalize_value(row.get("email", ""))
        name = _normalize_value(row.get("name", ""))
        if login and login not in by_login:
            by_login[login] = idx
        if email and email not in by_email:
            by_email[email] = idx
        if name and name not in by_name:
            by_name[name] = idx
    return {"login": by_login, "email": by_email, "name": by_name}


def _find_corporate_match(
    row: pd.Series, lookup: dict, corporate_df: pd.DataFrame
) -> Tuple[str, str]:
    """
    Find match type: 'login' | 'email' | 'name' | None.
    Returns (match_type, classification hint).
    """
    login = _normalize_value(row.get("login", ""))
    email = _normalize_value(row.get("email", ""))
    name = _normalize_value(row.get("name", ""))

    idx_login = lookup["login"].get(login)
    idx_email = lookup["email"].get(email)
    idx_name = lookup["name"].get(name)

    # Reference rule: if ANY identifier matches corporate base, do not recommend
    # priority removal. Corporate base is the source of truth.
    if idx_login is not None:
        return "login", CLASS_OK
    if idx_email is not None:
        return "email", CLASS_OK
    if idx_name is not None:
        return "name", CLASS_POSSIVEL_REMOCAO

    return "", CLASS_REMOVER_PRIORIDADE


def _is_duplicate_app_access(
    row: pd.Series, app_df: pd.DataFrame, application_col: str
) -> bool:
    """True if same person (login or email) has another row in same application."""
    login = _normalize_value(row.get("login", ""))
    email = _normalize_value(row.get("email", ""))
    app = row.get(application_col, "")
    if not app:
        return False
    for idx, other in app_df.iterrows():
        if other.get(application_col, "") != app:
            continue
        if login and _normalize_value(other.get("login", "")) == login:
            return True
        if email and _normalize_value(other.get("email", "")) == email:
            return True
    return False


def compare(
    corporate_df: pd.DataFrame,
    app_df: pd.DataFrame,
    application_col: str = "application",
) -> pd.DataFrame:
    """
    Compare application users against corporate directory.
    Returns a dataframe with original app columns plus:
    - match_type (login | email | name | '')
    - classification (OK | Remover com prioridade | ...)
    - in_corporate (True/False)
    """
    lookup = _build_lookup(corporate_df)
    rows: List[dict] = []
    for idx, row in app_df.iterrows():
        match_type, classification = _find_corporate_match(
            row, lookup, corporate_df
        )
        in_corporate = classification in (CLASS_OK, CLASS_POSSIVEL_REMOCAO, CLASS_REVISAO_MANUAL)

        # If matched and duplicate app entry for same app, mark as obsolete
        if classification == CLASS_OK and in_corporate:
            if _is_duplicate_app_access(row, app_df.drop(idx), application_col):
                classification = CLASS_ACESSO_OBSOLETO

        out = row.to_dict()
        out["match_type"] = match_type
        out["classification"] = classification
        out["in_corporate"] = in_corporate
        rows.append(out)

    result = pd.DataFrame(rows)
    return result


def summary_stats(review_df: pd.DataFrame) -> pd.DataFrame:
    """Count by classification. Index = classification, column = count."""
    return review_df["classification"].value_counts().reindex(CLASSIFICATION_ORDER).fillna(0).astype(int)
