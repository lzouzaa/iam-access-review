"""
IAM Access Review - Streamlit app.
"""
from datetime import datetime
from io import BytesIO
from pathlib import Path

import pandas as pd
import streamlit as st

from comparator import (
    CLASS_ACESSO_OBSOLETO,
    CLASS_OK,
    CLASS_POSSIVEL_REMOCAO,
    CLASS_REMOVER_PRIORIDADE,
    CLASS_REVISAO_MANUAL,
    compare,
    summary_stats,
)
from i18n import classification_label, t
from ppt_export import build_executive_pptx
from utils import ensure_output_dir, load_file

st.set_page_config(
    page_title="IAM Access Review",
    page_icon="🔐",
    layout="wide",
)

# Language: small buttons at top right
if "lang" not in st.session_state:
    st.session_state.lang = "pt-BR"

_, col_lang = st.columns([5, 1])
with col_lang:
    btn_pt, btn_en = st.columns(2)
    with btn_pt:
        if st.button("PT-BR", key="lang_pt", use_container_width=True):
            st.session_state.lang = "pt-BR"
    with btn_en:
        if st.button("EN-US", key="lang_en", use_container_width=True):
            st.session_state.lang = "en-US"

lang = st.session_state.lang

st.title(f"🔐 {t('page_title', lang)}")
st.caption(t("page_caption", lang))

# Sidebar: template downloads
templates_dir = Path(__file__).parent / "templates"
if templates_dir.exists():
    with st.sidebar.expander(t("header_templates", lang), expanded=False):
        st.caption(t("template_hint", lang))
        try:
            corp_csv = (templates_dir / "modelo_usuarios_corporativo.csv").read_bytes()
            app_csv = (templates_dir / "modelo_ferramenta_aplicacao.csv").read_bytes()
            col_a, col_b = st.columns(2)
            with col_a:
                st.download_button(t("btn_corp_csv", lang), data=corp_csv, file_name="modelo_usuarios_corporativo.csv", mime="text/csv", key="dl_corp_csv")
                st.download_button(t("btn_app_csv", lang), data=app_csv, file_name="modelo_ferramenta_aplicacao.csv", mime="text/csv", key="dl_app_csv")
            with col_b:
                df_corp = pd.read_csv(templates_dir / "modelo_usuarios_corporativo.csv")
                df_app = pd.read_csv(templates_dir / "modelo_ferramenta_aplicacao.csv")
                buf_corp = BytesIO()
                df_corp.to_excel(buf_corp, index=False, engine="openpyxl")
                buf_corp.seek(0)
                buf_app = BytesIO()
                df_app.to_excel(buf_app, index=False, engine="openpyxl")
                buf_app.seek(0)
                st.download_button(t("btn_corp_xlsx", lang), data=buf_corp.getvalue(), file_name="modelo_usuarios_corporativo.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key="dl_corp_xlsx")
                st.download_button(t("btn_app_xlsx", lang), data=buf_app.getvalue(), file_name="modelo_ferramenta_aplicacao.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key="dl_app_xlsx")
        except Exception:
            st.caption("Templates unavailable." if lang == "en-US" else "Modelos não disponíveis.")

# Sidebar: uploads
st.sidebar.header(t("sidebar_upload", lang))

corp_file = st.sidebar.file_uploader(
    t("upload_corporate", lang),
    type=["csv", "xlsx"],
    key="corp",
)
app_files = st.sidebar.file_uploader(
    t("upload_apps", lang),
    type=["csv", "xlsx"],
    key="app",
    accept_multiple_files=True,
)
if app_files:
    st.sidebar.caption(t("upload_apps_hint", lang))

corporate_df = None
app_df = None

if corp_file:
    try:
        corporate_df = load_file(uploaded_file=corp_file)
        st.sidebar.success(t("success_corporate", lang, n=len(corporate_df)))
    except Exception as e:
        st.sidebar.error(t("error_corporate", lang, msg=str(e)))

if app_files:
    loaded = []
    total_rows = 0
    for f in app_files:
        try:
            df = load_file(uploaded_file=f)
            name = Path(f.name).stem
            df["application"] = name
            loaded.append(df)
            total_rows += len(df)
            st.sidebar.caption(t("success_app_file", lang, name=name, n=len(df)))
        except Exception as e:
            st.sidebar.error(t("error_app_file", lang, name=f.name, msg=str(e)))
    if loaded:
        app_df = pd.concat(loaded, ignore_index=True)
        st.sidebar.success(t("success_apps", lang, count=len(loaded), n=total_rows))

# Run comparison (corporate = main base; app_df = all tool files combined)
review_df = None
if corporate_df is not None and app_df is not None and not app_df.empty:
    if st.sidebar.button(t("btn_run", lang)):
        with st.spinner(t("spinner_compare", lang)):
            review_df = compare(corporate_df, app_df)
        st.sidebar.success(t("success_done", lang))
        st.session_state["review_df"] = review_df

if "review_df" in st.session_state:
    review_df = st.session_state["review_df"]

if review_df is not None and not review_df.empty:
    stats = summary_stats(review_df)

    # Metrics (translated labels)
    st.header(t("header_dashboard", lang))
    cols = st.columns(5)
    for i, (cl, count) in enumerate(stats.items()):
        with cols[i]:
            st.metric(label=classification_label(cl, lang), value=int(count))

    # Filter by application
    app_col = "application"
    filter_all_label = t("filter_all", lang)
    if app_col in review_df.columns and review_df[app_col].notna().any():
        app_list = sorted(review_df[app_col].dropna().astype(str).unique().tolist())
        apps = [filter_all_label] + app_list
        selected_app = st.selectbox(t("filter_app", lang), apps)
        if selected_app != filter_all_label:
            table_df = review_df[review_df[app_col].astype(str) == selected_app]
        else:
            table_df = review_df
    else:
        table_df = review_df

    # Classification filter (translated options; internal value for filter)
    internal_to_label = {cl: classification_label(cl, lang) for cl in stats.index}
    label_to_internal = {v: k for k, v in internal_to_label.items()}
    classification_options = [internal_to_label[cl] for cl in stats.index]
    selected_labels = st.multiselect(
        t("filter_classification", lang),
        options=classification_options,
        default=classification_options,
    )
    selected_internal = [label_to_internal[l] for l in selected_labels]
    table_df = table_df[table_df["classification"].isin(selected_internal)]

    # Table: show classification in selected language
    table_display = table_df.copy()
    table_display["classification"] = table_display["classification"].map(
        lambda c: classification_label(c, lang)
    )

    st.subheader(t("table_detail", lang))
    st.dataframe(table_display, use_container_width=True, height=400)

    # Executive summary (in selected language) - build once for text and PPT
    total = len(review_df)
    n_ok = int(stats.get(CLASS_OK, 0))
    n_remove = int(stats.get(CLASS_REMOVER_PRIORIDADE, 0))
    n_possivel = int(stats.get(CLASS_POSSIVEL_REMOCAO, 0))
    n_revisao = int(stats.get(CLASS_REVISAO_MANUAL, 0))
    n_obsoleto = int(stats.get(CLASS_ACESSO_OBSOLETO, 0))

    date_str = datetime.now().strftime("%d/%m/%Y %H:%M") if lang == "pt-BR" else datetime.now().strftime("%m/%d/%Y %H:%M")
    summary_lines = [
        t("summary_title", lang),
        "=" * 50,
        t("summary_date", lang, date=date_str),
        t("summary_total", lang, total=total),
        "",
        t("summary_by_class", lang),
        f"  - {classification_label(CLASS_OK, lang)}: {n_ok}",
        f"  - {classification_label(CLASS_REMOVER_PRIORIDADE, lang)}: {n_remove}",
        f"  - {classification_label(CLASS_POSSIVEL_REMOCAO, lang)}: {n_possivel}",
        f"  - {classification_label(CLASS_REVISAO_MANUAL, lang)}: {n_revisao}",
        f"  - {classification_label(CLASS_ACESSO_OBSOLETO, lang)}: {n_obsoleto}",
        "",
        t("summary_recommendation", lang, n=n_remove),
    ]
    summary_text = "\n".join(summary_lines)

    # Export
    st.header(t("header_export", lang))
    out_dir = ensure_output_dir()
    base_name = f"access_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    col1, col2, col3, col4 = st.columns(4)

    csv_bytes = table_df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8")
    with col1:
        st.download_button(
            t("download_csv", lang),
            data=csv_bytes,
            file_name=f"{base_name}.csv",
            mime="text/csv",
        )

    buf = BytesIO()
    table_df.to_excel(buf, index=False, engine="openpyxl")
    buf.seek(0)
    with col2:
        st.download_button(
            t("download_excel", lang),
            data=buf.getvalue(),
            file_name=f"{base_name}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    with col3:
        st.download_button(
            t("download_summary", lang),
            data=summary_text.encode("utf-8"),
            file_name=f"{base_name}_resumo.txt",
            mime="text/plain; charset=utf-8",
        )

    ppt_bytes = build_executive_pptx(stats, summary_lines, lang, date_str)
    with col4:
        st.download_button(
            t("download_ppt", lang),
            data=ppt_bytes,
            file_name=f"{base_name}_apresentacao.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        )

    st.subheader(t("header_summary", lang))
    st.text(summary_text)

    # Users to remove only (per system) - download below executive summary
    st.subheader(t("header_remove_by_system", lang))
    st.markdown(t("header_remove_by_system_desc", lang))
    remove_df = review_df[review_df["classification"] == CLASS_REMOVER_PRIORIDADE].copy()
    if remove_df.empty:
        st.info(t("empty_remove", lang))
    else:
        # Show table with key columns (application so they know which system to remove from)
        display_remove = remove_df[["name", "email", "login", "application"]].copy()
        display_remove.columns = ["Nome" if lang == "pt-BR" else "Name", "E-mail", "Login", "Sistema" if lang == "pt-BR" else "System"]
        st.dataframe(display_remove, use_container_width=True, height=min(300, 80 + len(remove_df) * 35))
        r_csv = remove_df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8")
        r_buf = BytesIO()
        remove_df.to_excel(r_buf, index=False, engine="openpyxl")
        r_buf.seek(0)
        c1, c2 = st.columns(2)
        with c1:
            st.download_button(
                t("download_remove_csv", lang),
                data=r_csv,
                file_name=f"{base_name}_usuarios_a_remover.csv",
                mime="text/csv",
                key="dl_remove_csv",
            )
        with c2:
            st.download_button(
                t("download_remove_xlsx", lang),
                data=r_buf.getvalue(),
                file_name=f"{base_name}_usuarios_a_remover.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="dl_remove_xlsx",
            )
else:
    st.info(t("info_upload", lang))
