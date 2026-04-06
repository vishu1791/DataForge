"""
ui/sidebar.py  –  DataForge · Professional Sidebar
Framework : Streamlit
Theme     : Light Professional  (matches main_panel.py)
"""

import streamlit as st
import pandas as pd
import os
import io

from modules.data_loader import DataLoader
from modules.data_cleaning import DataCleaner
from modules.data_transform import DataTransformer


# ─────────────────────────────────────────────────────────────────────────────
#  SIDEBAR STYLES
# ─────────────────────────────────────────────────────────────────────────────

def _inject_sidebar_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&family=Fraunces:ital,opsz,wght@0,9..144,300;1,9..144,400&display=swap');

    /* ── Sidebar shell ── */
    [data-testid="stSidebar"] {
        background: #f8fafc !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        padding: 1.25rem 1rem 2rem !important;
    }

    /* ── Sidebar brand header ── */
    .sb-brand {
        display: flex; align-items: center; gap: .75rem;
        padding: .9rem 1rem;
        background: linear-gradient(120deg, #ffffff 60%, #eff6ff 100%);
        border: 1px solid #dbeafe; border-radius: 12px;
        margin-bottom: 1.25rem;
        box-shadow: 0 1px 3px rgba(15,23,42,.07);
    }
    .sb-brand .sb-icon {
        width: 36px; height: 36px; flex-shrink: 0;
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        border-radius: 9px; display: flex; align-items: center;
        justify-content: center; font-size: 1.05rem;
        box-shadow: 0 4px 10px rgba(37,99,235,.28);
    }
    .sb-brand h2 {
        font-family: 'Fraunces', serif !important; font-weight: 300 !important;
        font-size: 1.05rem !important; color: #0f172a !important;
        margin: 0 !important; padding: 0 !important; letter-spacing: -.02em;
    }
    .sb-brand span {
        font-size: .67rem; color: #94a3b8;
        font-family: 'DM Sans', sans-serif;
    }

    /* ── Section divider label ── */
    .sb-section {
        display: flex; align-items: center; gap: .5rem;
        font-family: 'DM Sans', sans-serif;
        font-size: .68rem; font-weight: 700; letter-spacing: .08em;
        text-transform: uppercase; color: #94a3b8;
        margin: 1.1rem 0 .6rem; padding: 0 .1rem;
    }
    .sb-section::after {
        content: ''; flex: 1; height: 1px; background: #e2e8f0;
    }

    /* ── Info card (file loaded state) ── */
    .sb-file-card {
        background: #fff; border: 1px solid #e2e8f0;
        border-radius: 10px; padding: .8rem 1rem;
        margin-bottom: .75rem;
        box-shadow: 0 1px 3px rgba(15,23,42,.05);
    }
    .sb-file-card .sf-name {
        font-family: 'DM Mono', monospace; font-size: .75rem;
        font-weight: 500; color: #1e293b;
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
        margin-bottom: .35rem;
    }
    .sb-file-card .sf-meta {
        display: flex; gap: .5rem; flex-wrap: wrap;
    }
    .sf-pill {
        font-size: .65rem; font-weight: 600; padding: .18rem .55rem;
        border-radius: 20px; border: 1px solid;
    }
    .sf-pill.blue  { background: #dbeafe; color: #1e40af; border-color: #bfdbfe; }
    .sf-pill.green { background: #d1fae5; color: #065f46; border-color: #a7f3d0; }
    .sf-pill.amber { background: #fef3c7; color: #92400e; border-color: #fde68a; }

    /* ── Sub-headers inside sidebar ── */
    .sb-sub {
        font-family: 'DM Sans', sans-serif !important;
        font-size: .78rem !important; font-weight: 600 !important;
        color: #334155 !important; margin: .75rem 0 .35rem !important;
        display: flex; align-items: center; gap: .35rem;
    }

    /* ── Compact status messages ── */
    .sb-success {
        background: #d1fae5; border: 1px solid #a7f3d0;
        border-radius: 8px; padding: .5rem .75rem;
        font-size: .78rem; color: #065f46; font-weight: 500;
        margin: .5rem 0;
    }
    .sb-error {
        background: #fee2e2; border: 1px solid #fecaca;
        border-radius: 8px; padding: .5rem .75rem;
        font-size: .78rem; color: #991b1b; font-weight: 500;
        margin: .5rem 0;
    }
    .sb-info {
        background: #eff6ff; border: 1px solid #bfdbfe;
        border-radius: 8px; padding: .5rem .75rem;
        font-size: .78rem; color: #1e40af; font-weight: 500;
        margin: .5rem 0;
    }

    /* ── Upload drop zone ── */
    [data-testid="stSidebar"] [data-testid="stFileUploader"] > div {
        border-radius: 10px !important;
        border: 1.5px dashed #cbd5e1 !important;
        background: #fff !important;
        transition: border-color .2s, background .2s;
    }
    [data-testid="stSidebar"] [data-testid="stFileUploader"] > div:hover {
        border-color: #60a5fa !important;
        background: #eff6ff !important;
    }

    /* ── Sidebar selectbox / multiselect ── */
    [data-testid="stSidebar"] .stSelectbox > div > div,
    [data-testid="stSidebar"] .stMultiSelect > div > div {
        border-radius: 8px !important;
        border-color: #e2e8f0 !important;
        background: #fff !important;
        font-size: .82rem !important;
    }

    /* ── Sidebar sliders ── */
    [data-testid="stSidebar"] [data-testid="stSlider"] > div {
        padding-top: .1rem !important;
    }

    /* ── Sidebar buttons ── */
    [data-testid="stSidebar"] .stButton > button {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important; font-size: .82rem !important;
        border-radius: 8px !important;
        transition: all .15s !important;
    }
    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
        border: none !important;
        box-shadow: 0 2px 8px rgba(37,99,235,.3) !important;
    }
    [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
        box-shadow: 0 4px 14px rgba(37,99,235,.4) !important;
        transform: translateY(-1px) !important;
    }
    [data-testid="stSidebar"] .stButton > button[kind="secondary"] {
        background: #fff !important;
        border: 1px solid #e2e8f0 !important;
        color: #475569 !important;
    }
    [data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
        border-color: #60a5fa !important; color: #2563eb !important;
    }

    /* ── Expander in sidebar ── */
    [data-testid="stSidebar"] .streamlit-expanderHeader {
        font-size: .8rem !important; font-weight: 600 !important;
        color: #475569 !important; border-radius: 8px !important;
        background: #fff !important; border: 1px solid #e2e8f0 !important;
    }
    [data-testid="stSidebar"] .streamlit-expanderContent {
        border: 1px solid #e2e8f0 !important; border-top: none !important;
        border-radius: 0 0 8px 8px !important;
        background: #f8fafc !important; padding: .75rem !important;
    }

    /* ── Checkbox ── */
    [data-testid="stSidebar"] .stCheckbox label {
        font-size: .82rem !important; color: #334155 !important;
    }

    /* ── Reset link button ── */
    .sb-reset {
        display: block; text-align: center;
        font-size: .73rem; color: #94a3b8; cursor: pointer;
        margin-top: .5rem; text-decoration: underline;
        background: none; border: none; width: 100%;
    }
    .sb-reset:hover { color: #ef4444; }

    /* ── Progress ring placeholder ── */
    .sb-step {
        display: flex; align-items: center; gap: .6rem;
        padding: .45rem .6rem; border-radius: 7px;
        font-size: .78rem; color: #475569; font-weight: 500;
        margin-bottom: .3rem;
        background: #fff; border: 1px solid #e2e8f0;
    }
    .sb-step .step-dot {
        width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0;
    }
    .sb-step .step-dot.done  { background: #10b981; }
    .sb-step .step-dot.active { background: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59,130,246,.2); }
    .sb-step .step-dot.idle  { background: #cbd5e1; }

    /* ── Footer ── */
    .sb-footer {
        margin-top: 1.5rem; padding-top: .75rem;
        border-top: 1px solid #e2e8f0;
        text-align: center; font-size: .67rem; color: #cbd5e1;
        font-family: 'DM Mono', monospace;
    }
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  HELPER WIDGETS
# ─────────────────────────────────────────────────────────────────────────────

def _sb_section(icon: str, label: str):
    st.markdown(
        f'<div class="sb-section">{icon}&nbsp;{label}</div>',
        unsafe_allow_html=True,
    )


def _sb_sub(icon: str, label: str):
    st.markdown(
        f'<p class="sb-sub">{icon}&nbsp;{label}</p>',
        unsafe_allow_html=True,
    )


def _workflow_steps(has_data: bool, cleaned: bool, exported: bool):
    """Mini progress tracker showing pipeline stage."""
    steps = [
        ("Upload data",    has_data,          has_data),
        ("Clean & transform", cleaned,        cleaned and has_data),
        ("Export results", exported,          exported and cleaned),
    ]
    html = ""
    for label, done, active in steps:
        if done:
            cls = "done"
        elif active:
            cls = "active"
        else:
            cls = "idle"
        html += f'<div class="sb-step"><div class="step-dot {cls}"></div>{label}</div>'
    st.markdown(html, unsafe_allow_html=True)


def _memory_str(df: pd.DataFrame) -> str:
    mem = df.memory_usage(deep=True).sum()
    if mem < 1024:        return f"{mem} B"
    elif mem < 1024**2:   return f"{mem/1024:.1f} KB"
    else:                 return f"{mem/1024**2:.1f} MB"


# ─────────────────────────────────────────────────────────────────────────────
#  UPLOAD SECTION
# ─────────────────────────────────────────────────────────────────────────────

def _render_upload():
    _sb_section("📁", "Data Source")

    uploaded_file = st.file_uploader(
        "Drop a file or click to browse",
        type=["csv", "xlsx", "xls", "json", "parquet"],
        help="Supported formats: CSV, Excel (.xlsx/.xls), JSON, Parquet",
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        try:
            # Load data directly from uploaded file to handle encoding better
            df = DataLoader.load_uploaded_file(uploaded_file)
            
            # Also save the file for backup/export purposes
            os.makedirs("data/raw", exist_ok=True)
            file_path = os.path.join("data/raw", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.session_state["data"]          = df
            st.session_state["original_data"] = df.copy()
            st.session_state["file_name"]     = uploaded_file.name
            st.session_state["cleaned"]       = False
            st.session_state["exported"]      = False

            # File info card
            missing_count = int(df.isnull().sum().sum())
            ext = uploaded_file.name.rsplit(".", 1)[-1].upper()
            st.markdown(f"""
            <div class="sb-file-card">
                <div class="sf-name">📄 {uploaded_file.name}</div>
                <div class="sf-meta">
                    <span class="sf-pill blue">{ext}</span>
                    <span class="sf-pill green">{df.shape[0]:,} rows</span>
                    <span class="sf-pill green">{df.shape[1]} cols</span>
                    <span class="sf-pill amber">{missing_count:,} missing</span>
                    <span class="sf-pill blue">{_memory_str(df)}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.markdown(
                f'<div class="sb-error">❌ Failed to load file:<br>{e}</div>',
                unsafe_allow_html=True,
            )

    elif "data" in st.session_state and "file_name" in st.session_state:
        # Already loaded — show persistent card
        df   = st.session_state["data"]
        name = st.session_state.get("file_name", "dataset")
        ext  = name.rsplit(".", 1)[-1].upper() if "." in name else "FILE"
        missing_count = int(df.isnull().sum().sum())
        st.markdown(f"""
        <div class="sb-file-card">
            <div class="sf-name">📄 {name}</div>
            <div class="sf-meta">
                <span class="sf-pill blue">{ext}</span>
                <span class="sf-pill green">{df.shape[0]:,} rows</span>
                <span class="sf-pill green">{df.shape[1]} cols</span>
                <span class="sf-pill amber">{missing_count:,} missing</span>
                <span class="sf-pill blue">{_memory_str(df)}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("↺ Load a different file", key="btn_reset_file",
                     use_container_width=True):
            for k in ["data", "original_data", "file_name", "cleaned", "exported"]:
                st.session_state.pop(k, None)
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
#  CLEANING SECTION
# ─────────────────────────────────────────────────────────────────────────────

def _render_cleaning(df: pd.DataFrame):
    _sb_section("🧹", "Data Cleaning")

    # ── Missing Values ────────────────────────────────────────────────────────
    with st.expander("💉 Missing Values", expanded=True):
        missing_cols = df.columns[df.isnull().any()].tolist()
        if missing_cols:
            missing_count = df.isnull().sum().sum()
            st.markdown(
                f'<div class="sb-info">⚠️ {missing_count:,} missing cells across '
                f'{len(missing_cols)} column(s)</div>',
                unsafe_allow_html=True,
            )
            
            # Add column selection
            target_missing_cols = st.multiselect(
                "Columns to treat",
                missing_cols,
                default=missing_cols,
                key="sb_missing_cols",
                placeholder="Select columns with missing values…",
            )
        else:
            st.markdown(
                '<div class="sb-success">✅ No missing values found</div>',
                unsafe_allow_html=True,
            )
            target_missing_cols = []

        missing_strategy = st.selectbox(
            "Strategy",
            ["none", "drop", "fill_mean", "fill_median", "fill_mode", "fill_value"],
            format_func=lambda x: {
                "none":       "— No action",
                "drop":       "Drop rows with NaN",
                "fill_mean":  "Fill with Mean",
                "fill_median":"Fill with Median",
                "fill_mode":  "Fill with Mode",
                "fill_value": "Fill with Constant",
            }.get(x, x),
            key="sb_missing_strategy",
        )
        fill_value = None
        if missing_strategy == "fill_value":
            fill_value = st.text_input("Constant fill value", "0", key="sb_fill_val")

    # ── Duplicates ────────────────────────────────────────────────────────────
    with st.expander("🔁 Duplicate Rows"):
        dup_count = df.duplicated().sum()
        if dup_count > 0:
            st.markdown(
                f'<div class="sb-info">⚠️ {dup_count:,} duplicate rows detected</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="sb-success">✅ No duplicates found</div>',
                unsafe_allow_html=True,
            )
        remove_duplicates = st.checkbox("Remove duplicate rows", key="sb_rm_dup")

    # ── Outliers ──────────────────────────────────────────────────────────────
    with st.expander("📡 Outlier Detection"):
        detect_outliers = st.checkbox("Enable outlier detection", key="sb_detect_out")
        outlier_method    = "iqr"
        outlier_threshold = 1.5
        outlier_action    = "none"

        if detect_outliers:
            outlier_method = st.selectbox(
                "Detection method",
                ["iqr", "zscore"],
                format_func=lambda x: "IQR (robust)" if x == "iqr" else "Z-Score (normal dist.)",
                key="sb_out_method",
            )
            outlier_threshold = st.slider(
                "Threshold", 1.0, 3.0, 1.5, 0.1,
                key="sb_out_thresh",
                help="IQR multiplier or Z-score cutoff",
            )
            outlier_action = st.selectbox(
                "Action on outliers",
                ["none", "remove", "cap"],
                format_func=lambda x: {
                    "none":   "— Flag only",
                    "remove": "Remove outlier rows",
                    "cap":    "Cap to boundary",
                }.get(x, x),
                key="sb_out_action",
            )

    return missing_strategy, fill_value, target_missing_cols, remove_duplicates, detect_outliers, \
           outlier_method, outlier_threshold, outlier_action


# ─────────────────────────────────────────────────────────────────────────────
#  TRANSFORMATION SECTION
# ─────────────────────────────────────────────────────────────────────────────

def _render_transformation(df: pd.DataFrame):
    _sb_section("🔄", "Transformation")

    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    num_cols = df.select_dtypes(include="number").columns.tolist()

    categorical_columns = []
    encoding_method     = "none"
    numeric_columns     = []
    scaling_method      = "none"
    feature_operations  = {}

    # ── Encoding ──────────────────────────────────────────────────────────────
    with st.expander("🏷 Categorical Encoding"):
        if cat_cols:
            categorical_columns = st.multiselect(
                "Columns to encode",
                cat_cols,
                key="sb_cat_cols",
                placeholder="Select columns…",
            )
            if categorical_columns:
                encoding_method = st.selectbox(
                    "Method",
                    ["none", "onehot", "label"],
                    format_func=lambda x: {
                        "none":   "— No encoding",
                        "onehot": "One-Hot Encoding",
                        "label":  "Label Encoding",
                    }.get(x, x),
                    key="sb_enc_method",
                )
        else:
            st.caption("No categorical columns detected.")

    # ── Scaling ───────────────────────────────────────────────────────────────
    with st.expander("📐 Feature Scaling"):
        if num_cols:
            numeric_columns = st.multiselect(
                "Columns to scale",
                num_cols,
                key="sb_num_cols",
                placeholder="Select columns…",
            )
            if numeric_columns:
                scaling_method = st.selectbox(
                    "Method",
                    ["none", "standard", "minmax"],
                    format_func=lambda x: {
                        "none":     "— No scaling",
                        "standard": "Standard Scaler (z-score)",
                        "minmax":   "Min-Max Scaler [0, 1]",
                    }.get(x, x),
                    key="sb_scale_method",
                )
        else:
            st.caption("No numeric columns detected.")

    # ── Feature Engineering ───────────────────────────────────────────────────
    with st.expander("⚗️ Feature Engineering"):
        if num_cols:
            if st.checkbox("Log transform columns", key="sb_log_check"):
                log_cols = st.multiselect(
                    "Columns for log(x+1)",
                    num_cols, key="sb_log_cols",
                    placeholder="Select columns…",
                )
                if log_cols:
                    feature_operations["log"] = log_cols

            if st.checkbox("Polynomial features (degree 2)", key="sb_poly_check"):
                poly_cols = st.multiselect(
                    "Columns for x²",
                    num_cols, key="sb_poly_cols",
                    placeholder="Select columns…",
                )
                if poly_cols:
                    feature_operations["poly"] = poly_cols
        else:
            st.caption("No numeric columns available.")

    return (categorical_columns, encoding_method,
            numeric_columns, scaling_method, feature_operations)


# ─────────────────────────────────────────────────────────────────────────────
#  EXPORT SECTION
# ─────────────────────────────────────────────────────────────────────────────

def _render_export(df: pd.DataFrame):
    _sb_section("📤", "Export")

    c1, c2 = st.columns([3, 2])
    with c1:
        export_format = st.selectbox(
            "Format",
            ["csv", "xlsx", "json", "parquet"],
            format_func=lambda x: {
                "csv":     "📄 CSV",
                "xlsx":    "📊 Excel (.xlsx)",
                "json":    "🗃 JSON",
                "parquet": "🗜 Parquet",
            }.get(x, x),
            key="sb_export_fmt",
            label_visibility="collapsed",
        )
    with c2:
        filename = st.text_input(
            "Filename",
            "cleaned_data",
            key="sb_export_name",
            label_visibility="collapsed",
            placeholder="filename…",
        )

    # Build download buffer
    fname_map = {"csv": f"{filename}.csv", "xlsx": f"{filename}.xlsx",
                 "json": f"{filename}.json", "parquet": f"{filename}.parquet"}
    mime_map  = {
        "csv":     "text/csv",
        "xlsx":    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "json":    "application/json",
        "parquet": "application/octet-stream",
    }

    try:
        if export_format == "csv":
            data = df.to_csv(index=False).encode("utf-8")
        elif export_format == "xlsx":
            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine="openpyxl") as w:
                df.to_excel(w, index=False)
            data = buf.getvalue()
        elif export_format == "json":
            data = df.to_json(orient="records", indent=2).encode("utf-8")
        else:
            buf = io.BytesIO(); df.to_parquet(buf, index=False)
            data = buf.getvalue()

        st.download_button(
            label=f"⬇ Download {fname_map[export_format]}",
            data=data,
            file_name=fname_map[export_format],
            mime=mime_map[export_format],
            type="primary",
            use_container_width=True,
            key="sb_download_btn",
            on_click=lambda: st.session_state.update({"exported": True}),
        )
    except Exception as e:
        st.markdown(
            f'<div class="sb-error">Export error: {e}</div>',
            unsafe_allow_html=True,
        )

    st.caption(
        f"{df.shape[0]:,} rows × {df.shape[1]} cols · {_memory_str(df)}"
    )


# ─────────────────────────────────────────────────────────────────────────────
#  APPLY OPERATIONS
# ─────────────────────────────────────────────────────────────────────────────

def _apply_all(
    missing_strategy, fill_value, target_missing_cols, remove_duplicates,
    detect_outliers, outlier_method, outlier_threshold, outlier_action,
    categorical_columns, encoding_method,
    numeric_columns, scaling_method, feature_operations,
):
    """Apply all selected cleaning and transformation operations."""
    df = st.session_state["original_data"].copy()
    ops = []

    try:
        # Missing values
        if missing_strategy != "none" and target_missing_cols:
            if missing_strategy == "drop":
                df = DataCleaner.handle_missing_values(df, "drop", None, target_missing_cols)
                ops.append("missing values (dropped rows)")
            else:
                # Convert fill_value to appropriate type if needed
                if missing_strategy == "fill_value" and fill_value:
                    try:
                        # Try to convert to number if possible
                        fill_value = float(fill_value) if '.' in fill_value else int(fill_value)
                    except ValueError:
                        # Keep as string if not a number
                        pass
                
                df = DataCleaner.handle_missing_values(df, missing_strategy, fill_value, target_missing_cols)
                ops.append("missing values")

        # Duplicates
        if remove_duplicates:
            before = len(df)
            df = DataCleaner.remove_duplicates(df)
            ops.append(f"duplicates ({before - len(df)} removed)")

        # Outliers
        if detect_outliers and outlier_action != "none":
            outliers = DataCleaner.detect_outliers(df, outlier_method, outlier_threshold)
            df = DataCleaner.remove_outliers(df, outliers, outlier_action)
            ops.append(f"outliers ({outlier_action})")

        # Encoding
        if categorical_columns and encoding_method != "none":
            df = DataTransformer.encode_categorical(df, categorical_columns, encoding_method)
            ops.append(f"{encoding_method} encoding")

        # Scaling
        if numeric_columns and scaling_method != "none":
            df, _ = DataTransformer.scale_features(df, numeric_columns, scaling_method)
            ops.append(f"{scaling_method} scaling")

        # Feature engineering
        if feature_operations:
            df = DataTransformer.create_features(df, feature_operations)
            ops.append("feature engineering")

        st.session_state["data"]    = df
        st.session_state["cleaned"] = True

        summary = ", ".join(ops) if ops else "no operations selected"
        st.markdown(
            f'<div class="sb-success">✅ Applied: {summary}<br>'
            f'New shape: {df.shape[0]:,} rows × {df.shape[1]} cols</div>',
            unsafe_allow_html=True,
        )
        st.rerun()

    except Exception as e:
        st.markdown(
            f'<div class="sb-error">❌ Operation failed: {e}</div>',
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def render_sidebar():
    """Render the full professional DataForge sidebar."""
    _inject_sidebar_styles()

    with st.sidebar:

        # ── Brand header ─────────────────────────────────────────────────────
        st.markdown("""
        <div class="sb-brand">
            <div class="sb-icon">🔬</div>
            <div>
                <h2>DataForge</h2>
                <span>Cleaning &amp; Visualization</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Workflow progress ─────────────────────────────────────────────────
        has_data = "data" in st.session_state and not st.session_state["data"].empty
        cleaned  = st.session_state.get("cleaned", False)
        exported = st.session_state.get("exported", False)
        _workflow_steps(has_data, cleaned, exported)

        # ── Upload ────────────────────────────────────────────────────────────
        _render_upload()

        # ── Cleaning + Transformation (only when data is loaded) ──────────────
        if has_data:
            df = st.session_state["data"]

            (missing_strategy, fill_value, target_missing_cols, remove_duplicates,
             detect_outliers, outlier_method, outlier_threshold,
             outlier_action) = _render_cleaning(df)

            (categorical_columns, encoding_method,
             numeric_columns, scaling_method,
             feature_operations) = _render_transformation(df)

            # ── Apply button ─────────────────────────────────────────────────
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚀 Apply All Changes", type="primary",
                         use_container_width=True, key="sb_apply_btn"):
                _apply_all(
                    missing_strategy, fill_value, target_missing_cols, remove_duplicates,
                    detect_outliers, outlier_method, outlier_threshold, outlier_action,
                    categorical_columns, encoding_method,
                    numeric_columns, scaling_method, feature_operations,
                )

            if cleaned:
                if st.button("↺ Reset to Original Data", key="sb_reset_btn",
                             use_container_width=True):
                    st.session_state["data"]    = st.session_state["original_data"].copy()
                    st.session_state["cleaned"] = False
                    st.session_state["exported"] = False
                    st.rerun()

            # ── Export ───────────────────────────────────────────────────────
            _render_export(df)

        # ── Footer ────────────────────────────────────────────────────────────
        st.markdown(
            '<div class="sb-footer">DataForge · v1.0 · Powered by Streamlit</div>',
            unsafe_allow_html=True,
        )