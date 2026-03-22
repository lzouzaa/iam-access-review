"""
Translations for PT-BR and EN-US.
Internal classification keys (from comparator) are mapped to display labels per language.
"""

# Internal keys from comparator (do not change)
CLASS_OK = "OK"
CLASS_REMOVER_PRIORIDADE = "Remover com prioridade"
CLASS_POSSIVEL_REMOCAO = "Possível remoção"
CLASS_REVISAO_MANUAL = "Revisão manual"
CLASS_ACESSO_OBSOLETO = "Acesso obsoleto"

CLASSIFICATION_LABELS = {
    "pt-BR": {
        CLASS_OK: "OK",
        CLASS_REMOVER_PRIORIDADE: "Remover com prioridade",
        CLASS_POSSIVEL_REMOCAO: "Possível remoção",
        CLASS_REVISAO_MANUAL: "Revisão manual",
        CLASS_ACESSO_OBSOLETO: "Acesso obsoleto",
    },
    "en-US": {
        CLASS_OK: "OK",
        CLASS_REMOVER_PRIORIDADE: "Remove with priority",
        CLASS_POSSIVEL_REMOCAO: "Possible removal",
        CLASS_REVISAO_MANUAL: "Manual review",
        CLASS_ACESSO_OBSOLETO: "Obsolete access",
    },
}

TEXTS = {
    "pt-BR": {
        "page_title": "Revisão de Acessos IAM",
        "page_caption": "Compare o diretório corporativo com os acessos nas aplicações e classifique os resultados.",
        "sidebar_upload": "Upload",
        "upload_corporate": "Usuários ativos (base principal – 1 arquivo)",
        "upload_apps": "Ferramentas/aplicações (vários arquivos – 1 por ferramenta)",
        "upload_apps_hint": "Selecione um ou mais CSV/Excel. Cada arquivo = uma ferramenta; o nome do arquivo identifica a fonte.",
        "success_corporate": "Corporativo: {n} linhas",
        "success_apps": "{count} arquivo(s), {n} linhas no total",
        "success_app_file": "{name}: {n} linhas",
        "error_corporate": "Erro ao carregar corporativo: {msg}",
        "error_apps": "Erro ao carregar aplicações: {msg}",
        "error_app_file": "Erro em {name}: {msg}",
        "btn_run": "Executar comparação",
        "spinner_compare": "Comparando bases...",
        "success_done": "Concluído.",
        "header_dashboard": "Dashboard",
        "filter_app": "Filtrar por aplicação",
        "filter_all": "Todos",
        "filter_classification": "Filtrar por classificação",
        "table_detail": "Tabela detalhada",
        "header_export": "Exportar",
        "download_csv": "Download CSV",
        "download_excel": "Download Excel",
        "download_summary": "Download resumo (TXT)",
        "header_summary": "Resumo executivo",
        "summary_title": "RESUMO EXECUTIVO - REVISÃO DE ACESSOS IAM",
        "summary_date": "Data: {date}",
        "summary_total": "Total de registros analisados: {total}",
        "summary_by_class": "Distribuição por classificação:",
        "summary_recommendation": "Ações recomendadas: priorizar remoção de {n} acessos sem correspondência no diretório corporativo.",
        "info_upload": "Faça upload da planilha **corporativa** (1 arquivo) e de **uma ou mais** planilhas de ferramentas/aplicações. Cada arquivo de ferramenta será comparado à base principal. Clique em **Executar comparação** na barra lateral.",
        "header_templates": "Modelos de planilha",
        "template_corporate": "Modelo usuários corporativos",
        "template_app": "Modelo ferramenta/aplicação",
        "template_hint": "Baixe o modelo, preencha com seus dados e use no upload.",
        "btn_corp_csv": "Corporativo (CSV)",
        "btn_corp_xlsx": "Corporativo (Excel)",
        "btn_app_csv": "Ferramenta (CSV)",
        "btn_app_xlsx": "Ferramenta (Excel)",
        "download_ppt": "Download apresentação (PPTX)",
        "header_remove_by_system": "Resumo: usuários a remover por sistema",
        "header_remove_by_system_desc": "Apenas usuários classificados como **Remover com prioridade** em cada planilha/sistema enviado. Use o arquivo abaixo para remoção.",
        "download_remove_csv": "Download lista a remover (CSV)",
        "download_remove_xlsx": "Download lista a remover (Excel)",
        "empty_remove": "Nenhum usuário classificado para remoção prioritária.",
        "header_out_of_standard": "Dashboard: usuários fora do padrão por aplicação",
        "header_out_of_standard_desc": "Considera como fora do padrão qualquer classificação diferente de **OK**.",
        "col_application": "Aplicação",
        "col_out_of_standard": "Fora do padrão",
        "empty_out_of_standard": "Sem dados de aplicação para montar o dashboard de fora do padrão.",
    },
    "en-US": {
        "page_title": "IAM Access Review",
        "page_caption": "Compare corporate directory with application access and classify results.",
        "sidebar_upload": "Upload",
        "upload_corporate": "Active users (main base – 1 file)",
        "upload_apps": "Tools/applications (multiple files – 1 per tool)",
        "upload_apps_hint": "Select one or more CSV/Excel files. Each file = one tool; filename identifies the source.",
        "success_corporate": "Corporate: {n} rows",
        "success_apps": "{count} file(s), {n} rows total",
        "success_app_file": "{name}: {n} rows",
        "error_corporate": "Error loading corporate file: {msg}",
        "error_apps": "Error loading applications file: {msg}",
        "error_app_file": "Error in {name}: {msg}",
        "btn_run": "Run comparison",
        "spinner_compare": "Comparing bases...",
        "success_done": "Done.",
        "header_dashboard": "Dashboard",
        "filter_app": "Filter by application",
        "filter_all": "All",
        "filter_classification": "Filter by classification",
        "table_detail": "Detailed table",
        "header_export": "Export",
        "download_csv": "Download CSV",
        "download_excel": "Download Excel",
        "download_summary": "Download summary (TXT)",
        "header_summary": "Executive summary",
        "summary_title": "EXECUTIVE SUMMARY - IAM ACCESS REVIEW",
        "summary_date": "Date: {date}",
        "summary_total": "Total records analyzed: {total}",
        "summary_by_class": "Distribution by classification:",
        "summary_recommendation": "Recommended actions: prioritize removal of {n} accesses with no match in corporate directory.",
        "info_upload": "Upload the **corporate** spreadsheet (1 file) and **one or more** tool/application spreadsheets. Each tool file will be compared against the main base. Click **Run comparison** in the sidebar.",
        "header_templates": "Spreadsheet templates",
        "template_corporate": "Corporate users template",
        "template_app": "Tool/application template",
        "template_hint": "Download the template, fill with your data, then use in the upload.",
        "btn_corp_csv": "Corporate (CSV)",
        "btn_corp_xlsx": "Corporate (Excel)",
        "btn_app_csv": "Tool (CSV)",
        "btn_app_xlsx": "Tool (Excel)",
        "download_ppt": "Download presentation (PPTX)",
        "header_remove_by_system": "Summary: users to remove by system",
        "header_remove_by_system_desc": "Only users classified as **Remove with priority** per spreadsheet/system. Use the file below for removal.",
        "download_remove_csv": "Download list to remove (CSV)",
        "download_remove_xlsx": "Download list to remove (Excel)",
        "empty_remove": "No users classified for priority removal.",
        "header_out_of_standard": "Dashboard: out-of-standard users by application",
        "header_out_of_standard_desc": "Considers out-of-standard any classification different from **OK**.",
        "col_application": "Application",
        "col_out_of_standard": "Out of standard",
        "empty_out_of_standard": "No application data available to build out-of-standard dashboard.",
    },
}


def t(key: str, lang: str, **kwargs) -> str:
    """Get translated string for key. Use {placeholder} in TEXTS and pass kwargs."""
    s = TEXTS.get(lang, TEXTS["en-US"]).get(key, TEXTS["en-US"].get(key, key))
    return s.format(**kwargs) if kwargs else s


def classification_label(internal_key: str, lang: str) -> str:
    """Get display label for classification key."""
    return CLASSIFICATION_LABELS.get(lang, CLASSIFICATION_LABELS["en-US"]).get(
        internal_key, internal_key
    )
