"""
ui/main_panel.py  –  DataForge · Professional Main Panel
Framework : Streamlit
Theme     : Light Professional
"""

import streamlit as st
import pandas as pd
import numpy as np
import io

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from modules.data_cleaning import DataCleaner
from modules.visualization import DataVisualizer

# ─────────────────────────────────────────────────────────────────────────────
#  GLOBAL STYLES
# ─────────────────────────────────────────────────────────────────────────────

def _inject_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&family=Fraunces:ital,opsz,wght@0,9..144,300;1,9..144,400&display=swap');

    :root {
        --brand-50:  #eff6ff;
        --brand-100: #dbeafe;
        --brand-200: #bfdbfe;
        --brand-400: #60a5fa;
        --brand-500: #3b82f6;
        --brand-600: #2563eb;
        --brand-700: #1d4ed8;
        --n50:  #f8fafc; --n100: #f1f5f9; --n200: #e2e8f0;
        --n300: #cbd5e1; --n400: #94a3b8; --n500: #64748b;
        --n600: #475569; --n700: #334155; --n800: #1e293b; --n900: #0f172a;
        --success: #10b981; --warning: #f59e0b; --danger: #ef4444;
        --radius: 12px; --radius-sm: 8px;
        --shadow: 0 1px 3px rgba(15,23,42,.07),0 1px 2px rgba(15,23,42,.04);
        --shadow-md: 0 4px 16px rgba(15,23,42,.08),0 2px 4px rgba(15,23,42,.04);
    }

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif !important; }

    /* ── Hide default Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 1.75rem 2.25rem 3rem !important; max-width: 1380px !important; }

    /* ── Page header ── */
    .df-header {
        display: flex; align-items: center; gap: 1rem;
        padding: 1.5rem 1.75rem;
        background: linear-gradient(120deg, #ffffff 60%, var(--brand-50) 100%);
        border: 1px solid var(--brand-100);
        border-radius: var(--radius);
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow);
    }
    .df-header .icon {
        width: 46px; height: 46px; flex-shrink: 0;
        background: linear-gradient(135deg, var(--brand-500), var(--brand-700));
        border-radius: 11px; display: flex; align-items: center;
        justify-content: center; font-size: 1.35rem;
        box-shadow: 0 4px 12px rgba(37,99,235,.28);
    }
    .df-header h1 {
        font-family: 'Fraunces', serif !important; font-weight: 300 !important;
        font-size: 1.6rem !important; color: var(--n900) !important;
        margin: 0 !important; padding: 0 !important; line-height: 1.2 !important;
        letter-spacing: -.02em;
    }
    .df-header p { font-size: .8rem; color: var(--n400); margin: 0 !important; }
    .df-header .pill {
        margin-left: auto; font-family: 'DM Mono', monospace;
        font-size: .68rem; font-weight: 500; padding: .25rem .7rem;
        background: var(--brand-100); color: var(--brand-700);
        border-radius: 20px; border: 1px solid var(--brand-200); white-space: nowrap;
    }

    /* ── Stat cards ── */
    .stats-row { display: flex; gap: .875rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
    .stat-card {
        flex: 1; min-width: 130px; background: #fff;
        border: 1px solid var(--n200); border-radius: var(--radius);
        padding: 1.1rem 1.25rem; box-shadow: var(--shadow);
        position: relative; overflow: hidden;
        transition: box-shadow .18s, transform .18s;
    }
    .stat-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
    .stat-card::after {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
        border-radius: 3px 3px 0 0;
    }
    .stat-card.c-blue::after  { background: linear-gradient(90deg,var(--brand-400),var(--brand-600)); }
    .stat-card.c-green::after { background: linear-gradient(90deg,#34d399,#059669); }
    .stat-card.c-amber::after { background: linear-gradient(90deg,#fbbf24,#d97706); }
    .stat-card.c-rose::after  { background: linear-gradient(90deg,#fb7185,#e11d48); }
    .stat-card .s-label {
        font-size: .68rem; font-weight: 600; letter-spacing: .07em;
        text-transform: uppercase; color: var(--n400); margin-bottom: .35rem;
    }
    .stat-card .s-value {
        font-family: 'DM Mono', monospace; font-size: 1.55rem;
        font-weight: 500; color: var(--n800); line-height: 1;
    }
    .stat-card .s-sub { font-size: .7rem; color: var(--n400); margin-top: .3rem; }

    /* ── Section card ── */
    .sec-card {
        background: #fff; border: 1px solid var(--n200);
        border-radius: var(--radius); padding: 1.4rem 1.5rem;
        box-shadow: var(--shadow); margin-bottom: 1.25rem;
    }
    .sec-title {
        font-family: 'Fraunces', serif !important;
        font-size: 1rem !important; font-weight: 300 !important;
        color: var(--n800) !important; margin: 0 0 1rem !important;
        padding: 0 0 .65rem !important; letter-spacing: -.01em;
        border-bottom: 1px solid var(--n100) !important;
        display: flex; align-items: center; gap: .45rem;
    }

    /* ── Tab overrides ── */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--n50); border-radius: var(--radius-sm);
        padding: 4px; gap: 2px; border: 1px solid var(--n200);
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent; border-radius: 6px;
        font-size: .8rem; font-weight: 500; color: var(--n500);
        padding: .4rem .9rem; transition: all .15s;
    }
    .stTabs [aria-selected="true"] {
        background: #fff !important; color: var(--brand-600) !important;
        box-shadow: var(--shadow) !important;
    }
    .stTabs [data-baseweb="tab-panel"] { padding-top: 1rem !important; }

    /* ── Buttons ── */
    .stButton > button {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important; font-size: .83rem !important;
        border-radius: var(--radius-sm) !important;
        transition: all .15s !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--brand-500), var(--brand-700)) !important;
        border: none !important; box-shadow: 0 2px 8px rgba(37,99,235,.3) !important;
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 4px 16px rgba(37,99,235,.4) !important;
        transform: translateY(-1px) !important;
    }

    /* ── Selectbox / inputs ── */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        border-radius: var(--radius-sm) !important;
        border-color: var(--n200) !important;
        font-size: .84rem !important;
    }

    /* ── Alerts ── */
    .stInfo, .stSuccess, .stWarning, .stError {
        border-radius: var(--radius-sm) !important;
        font-size: .83rem !important;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        font-size: .84rem !important; font-weight: 600 !important;
        color: var(--n700) !important;
    }

    /* ── Quality badge ── */
    .quality-badge {
        display: inline-flex; align-items: center; gap: .35rem;
        padding: .3rem .75rem; border-radius: 20px;
        font-size: .76rem; font-weight: 600; letter-spacing: .03em;
    }
    .quality-badge.excellent { background:#d1fae5; color:#065f46; border:1px solid #a7f3d0; }
    .quality-badge.good      { background:#dbeafe; color:#1e40af; border:1px solid #bfdbfe; }
    .quality-badge.fair      { background:#fef3c7; color:#92400e; border:1px solid #fde68a; }
    .quality-badge.poor      { background:#fee2e2; color:#991b1b; border:1px solid #fecaca; }

    /* ── Recommendation item ── */
    .rec-item {
        display: flex; align-items: flex-start; gap: .65rem;
        padding: .7rem .9rem; border-radius: var(--radius-sm);
        background: var(--n50); border: 1px solid var(--n200);
        margin-bottom: .5rem; font-size: .83rem; color: var(--n700);
        line-height: 1.5;
    }
    .rec-item .rec-icon { font-size: 1rem; flex-shrink: 0; margin-top: .05rem; }

    /* ── Divider ── */
    .df-divider { border: none; border-top: 1px solid var(--n100); margin: 1.25rem 0; }
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  HELPER WIDGETS
# ─────────────────────────────────────────────────────────────────────────────

def _stat_card(label: str, value, sub: str, color: str):
    return f"""
    <div class="stat-card c-{color}">
        <div class="s-label">{label}</div>
        <div class="s-value">{value}</div>
        <div class="s-sub">{sub}</div>
    </div>"""


def _section_header(icon: str, title: str):
    st.markdown(f'<p class="sec-title">{icon}&nbsp; {title}</p>', unsafe_allow_html=True)


def _quality_score(df: pd.DataFrame) -> tuple[float, str]:
    total_cells   = df.shape[0] * df.shape[1]
    missing_pct   = (df.isnull().sum().sum() / max(total_cells, 1)) * 100
    duplicate_pct = (df.duplicated().sum() / max(len(df), 1)) * 100
    score = max(0, 100 - missing_pct * 1.5 - duplicate_pct * 2)
    if score >= 90:   label = "excellent"
    elif score >= 70: label = "good"
    elif score >= 50: label = "fair"
    else:             label = "poor"
    return round(score, 1), label


def _memory_str(df: pd.DataFrame) -> str:
    mem = df.memory_usage(deep=True).sum()
    if mem < 1024:            return f"{mem} B"
    elif mem < 1024 ** 2:     return f"{mem/1024:.1f} KB"
    else:                     return f"{mem/1024**2:.1f} MB"


# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 1 – STATS OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────

def _render_stats(df: pd.DataFrame):
    score, badge = _quality_score(df)
    missing      = int(df.isnull().sum().sum())
    duplicates   = int(df.duplicated().sum())

    missing_sub   = f"{missing / max(df.shape[0]*df.shape[1],1)*100:.1f}% of cells"
    duplicate_sub = f"{duplicate_pct:.1f}% of rows" if (duplicate_pct := duplicates/max(len(df),1)*100) > 0 else "no duplicates"

    cards_html = "".join([
        _stat_card("Rows",          f"{df.shape[0]:,}",  f"{df.shape[1]} columns",   "blue"),
        _stat_card("Columns",       f"{df.shape[1]}",    f"{df.dtypes.nunique()} dtypes", "green"),
        _stat_card("Missing Values",f"{missing:,}",      missing_sub,                 "amber"),
        _stat_card("Duplicates",    f"{duplicates:,}",   duplicate_sub,               "rose"),
        _stat_card("Memory",        _memory_str(df),     "in-memory footprint",       "blue"),
        _stat_card("Quality Score", f"{score}",          f'<span class="quality-badge {badge}">{badge.upper()}</span>', "green"),
    ])

    st.markdown(f'<div class="stats-row">{cards_html}</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 2 – DATA PREVIEW
# ─────────────────────────────────────────────────────────────────────────────

def _render_data_preview(df: pd.DataFrame):
    with st.container():
        st.markdown('<div class="sec-card">', unsafe_allow_html=True)
        _section_header("🔍", "Data Preview")

        tab_sample, tab_info, tab_stats = st.tabs(["📄 Sample Data", "🗂 Column Info", "📐 Statistics"])

        with tab_sample:
            n_rows = st.slider("Rows to display", 5, min(100, len(df)), 10, key="preview_rows")
            st.dataframe(
                df.head(n_rows),
                use_container_width=True,
                height=min(400, n_rows * 38 + 40),
            )

        with tab_info:
            info_df = pd.DataFrame({
                "Column":        df.columns.tolist(),
                "Dtype":         df.dtypes.astype(str).tolist(),
                "Non-Null":      df.count().tolist(),
                "Missing":       df.isnull().sum().tolist(),
                "Missing %":     (df.isnull().mean() * 100).round(2).tolist(),
                "Unique Values": df.nunique().tolist(),
                "Sample":        [str(df[c].dropna().iloc[0]) if df[c].dropna().shape[0] > 0 else "—" for c in df.columns],
            })
            st.dataframe(info_df, use_container_width=True, hide_index=True)

        with tab_stats:
            numeric_cols = df.select_dtypes(include="number").columns
            cat_cols     = df.select_dtypes(include=["object", "category"]).columns

            if not numeric_cols.empty:
                st.caption("**Numeric columns**")
                st.dataframe(df[numeric_cols].describe().T.round(3), use_container_width=True)
            if not cat_cols.empty:
                st.caption("**Categorical columns**")
                cat_stats = pd.DataFrame({
                    "Unique": df[cat_cols].nunique(),
                    "Top Value": [df[c].mode()[0] if not df[c].mode().empty else "—" for c in cat_cols],
                    "Top Freq":  [df[c].value_counts().iloc[0] if not df[c].value_counts().empty else 0 for c in cat_cols],
                })
                st.dataframe(cat_stats, use_container_width=True)
            if numeric_cols.empty and cat_cols.empty:
                st.info("No analysable columns found.")

        st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 3 – DATA CLEANING CONTROLS
# ─────────────────────────────────────────────────────────────────────────────

def _render_cleaning_controls(df: pd.DataFrame):
    with st.container():
        st.markdown('<div class="sec-card">', unsafe_allow_html=True)
        _section_header("🧹", "Data Cleaning Controls")

        left, right = st.columns([1, 1], gap="large")

        with left:
            st.markdown("##### Missing Value Treatment")
            missing_cols = df.columns[df.isnull().any()].tolist()

            if missing_cols:
                target_cols = st.multiselect(
                    "Columns to treat", missing_cols, default=missing_cols[:3],
                    key="clean_cols",
                )
                strategy = st.selectbox(
                    "Strategy",
                    ["Drop rows", "Fill – mean", "Fill – median", "Fill – mode", "Fill – constant"],
                    key="clean_strategy",
                )
                fill_value = None
                if strategy == "Fill – constant":
                    fill_value = st.text_input("Constant value", "0", key="fill_const")

                if st.button("▶ Apply Missing Treatment", type="primary", key="btn_missing"):
                    # Simple debug version
                    try:
                        with st.spinner("Applying treatment..."):
                            df_work = st.session_state["data"].copy()
                            
                            # Simple direct mapping
                            if strategy == "Drop rows":
                                df_work = df_work.dropna(subset=target_cols)
                            elif strategy == "Fill – mean":
                                for col in target_cols:
                                    if pd.api.types.is_numeric_dtype(df_work[col]):
                                        df_work[col] = df_work[col].fillna(df_work[col].mean())
                            elif strategy == "Fill – median":
                                for col in target_cols:
                                    if pd.api.types.is_numeric_dtype(df_work[col]):
                                        df_work[col] = df_work[col].fillna(df_work[col].median())
                            elif strategy == "Fill – mode":
                                for col in target_cols:
                                    mode_val = df_work[col].mode()
                                    if not mode_val.empty:
                                        df_work[col] = df_work[col].fillna(mode_val[0])
                            elif strategy == "Fill – constant":
                                df_work[target_cols] = df_work[target_cols].fillna(fill_value)
                            
                            st.session_state["data"] = df_work
                            st.success(f"✅ Applied '{strategy}' to {len(target_cols)} column(s). "
                                       f"Remaining missing: {df_work.isnull().sum().sum()}")
                            st.rerun()
                            
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        st.write(f"Debug info: strategy={strategy}, cols={target_cols}, fill={fill_value}")
            else:
                st.success("✅ No missing values — nothing to treat!")

        with right:
            st.markdown("##### Duplicate & Type Operations")

            dup_count = df.duplicated().sum()
            st.info(f"**{dup_count:,}** duplicate rows detected.")

            if dup_count > 0 and st.button("🗑 Remove Duplicates", key="btn_dup"):
                df_cleaned = DataCleaner.remove_duplicates(st.session_state["data"])
                st.session_state["data"] = df_cleaned.reset_index(drop=True)
                st.success(f"✅ Removed {dup_count} duplicate rows.")
                st.rerun()

            st.markdown("<hr class='df-divider'>", unsafe_allow_html=True)
            st.markdown("**Convert Column Dtype**")
            col_to_convert = st.selectbox("Column", df.columns.tolist(), key="dtype_col")
            new_dtype = st.selectbox("Target dtype", ["int64", "float64", "str", "datetime", "category"], key="dtype_target")

            if st.button("▶ Convert", key="btn_dtype"):
                try:
                    df_work = st.session_state["data"].copy()
                    if new_dtype == "datetime":
                        df_work[col_to_convert] = pd.to_datetime(df_work[col_to_convert], errors="coerce")
                    elif new_dtype == "str":
                        df_work[col_to_convert] = df_work[col_to_convert].astype(str)
                    else:
                        df_work[col_to_convert] = df_work[col_to_convert].astype(new_dtype)
                    st.session_state["data"] = df_work
                    st.success(f"✅ '{col_to_convert}' → {new_dtype}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Conversion failed: {e}")

        st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 4 – VISUALIZATIONS
# ─────────────────────────────────────────────────────────────────────────────

_CHART_PALETTE = ["#3b82f6","#10b981","#f59e0b","#ef4444","#8b5cf6","#06b6d4","#f97316","#ec4899"]

def _plotly_layout(fig, title=""):
    fig.update_layout(
        title=dict(text=title, font=dict(family="Fraunces, serif", size=15, color="#1e293b"), x=0.02),
        font=dict(family="DM Sans, sans-serif", size=12, color="#475569"),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=20, t=50 if title else 20, b=40),
        legend=dict(bgcolor="rgba(255,255,255,.85)", bordercolor="#e2e8f0", borderwidth=1),
        colorway=_CHART_PALETTE,
        xaxis=dict(gridcolor="#f1f5f9", linecolor="#e2e8f0", zerolinecolor="#e2e8f0"),
        yaxis=dict(gridcolor="#f1f5f9", linecolor="#e2e8f0", zerolinecolor="#e2e8f0"),
    )
    return fig


def _render_visualizations(df: pd.DataFrame):
    with st.container():
        st.markdown('<div class="sec-card">', unsafe_allow_html=True)
        _section_header("📈", "Data Visualization")

        viz_tabs = st.tabs([
            "🗺 Overview Dashboard",
            "📊 Distributions",
            "🔗 Correlation Matrix",
            "❓ Missing Values",
            "✏️ Custom Chart",
        ])

        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        cat_cols     = df.select_dtypes(include=["object", "category"]).columns.tolist()

        # ── Tab 0: Overview Dashboard ────────────────────────────────────────
        with viz_tabs[0]:
            if len(numeric_cols) >= 1:
                try:
                    fig = DataVisualizer.plot_data_overview(df)
                    _plotly_layout(fig)
                    st.plotly_chart(fig, use_container_width=True)
                except Exception:
                    # Fallback overview
                    cols_to_plot = numeric_cols[:4]
                    rows = (len(cols_to_plot) + 1) // 2
                    fig = make_subplots(rows=rows, cols=2,
                                        subplot_titles=[f"Distribution: {c}" for c in cols_to_plot])
                    for i, col in enumerate(cols_to_plot):
                        r, c = divmod(i, 2)
                        fig.add_trace(go.Histogram(x=df[col], name=col,
                                                   marker_color=_CHART_PALETTE[i % len(_CHART_PALETTE)],
                                                   opacity=.8), row=r+1, col=c+1)
                    _plotly_layout(fig, "Data Overview")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No numeric columns available for overview dashboard.")

        # ── Tab 1: Distributions ─────────────────────────────────────────────
        with viz_tabs[1]:
            if numeric_cols:
                c1, c2, c3 = st.columns([2, 2, 1])
                with c1:
                    sel_col  = st.selectbox("Column", numeric_cols, key="dist_col")
                with c2:
                    plot_type = st.selectbox("Chart type", ["Histogram", "Box", "Violin", "ECDF"], key="dist_type")
                with c3:
                    color_col = st.selectbox("Group by", ["—"] + cat_cols, key="dist_color")

                color = color_col if color_col != "—" else None

                try:
                    if plot_type == "Histogram":
                        fig = px.histogram(df, x=sel_col, color=color, nbins=40,
                                           color_discrete_sequence=_CHART_PALETTE, opacity=.85,
                                           marginal="rug")
                    elif plot_type == "Box":
                        fig = px.box(df, y=sel_col, x=color, color=color,
                                     color_discrete_sequence=_CHART_PALETTE, points="outliers")
                    elif plot_type == "Violin":
                        fig = px.violin(df, y=sel_col, x=color, color=color, box=True,
                                        color_discrete_sequence=_CHART_PALETTE)
                    else:
                        fig = px.ecdf(df, x=sel_col, color=color,
                                      color_discrete_sequence=_CHART_PALETTE)
                    _plotly_layout(fig, f"{plot_type} · {sel_col}")
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Could not render chart: {e}")
            else:
                st.info("No numeric columns for distribution plots.")

        # ── Tab 2: Correlation Matrix ─────────────────────────────────────────
        with viz_tabs[2]:
            if len(numeric_cols) > 1:
                method = st.radio("Method", ["pearson", "spearman", "kendall"],
                                  horizontal=True, key="corr_method")
                corr = df[numeric_cols].corr(method=method).round(3)
                mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
                corr_display = corr.where(~mask)

                fig = px.imshow(
                    corr_display, text_auto=True, aspect="auto",
                    color_continuous_scale=[[0,"#ef4444"],[.5,"#f8fafc"],[1,"#3b82f6"]],
                    zmin=-1, zmax=1,
                )
                fig.update_traces(textfont_size=10)
                _plotly_layout(fig, f"{method.capitalize()} Correlation Matrix")
                st.plotly_chart(fig, use_container_width=True)

                # Strongest correlations table
                with st.expander("🔗 Strongest Correlations"):
                    pairs = (corr.where(np.tril(np.ones(corr.shape), k=-1).astype(bool))
                               .stack().reset_index())
                    pairs.columns = ["Feature A", "Feature B", "Correlation"]
                    pairs["Abs"] = pairs["Correlation"].abs()
                    st.dataframe(
                        pairs.sort_values("Abs", ascending=False)
                             .drop("Abs", axis=1).head(15)
                             .style.background_gradient(subset=["Correlation"],
                                                        cmap="RdBu_r", vmin=-1, vmax=1),
                        use_container_width=True, hide_index=True
                    )
            else:
                st.info("Need at least 2 numeric columns for a correlation matrix.")

        # ── Tab 3: Missing Values ─────────────────────────────────────────────
        with viz_tabs[3]:
            missing = df.isnull().sum()
            missing = missing[missing > 0].sort_values(ascending=False)

            if not missing.empty:
                miss_pct = (missing / len(df) * 100).round(2)
                miss_df  = pd.DataFrame({"Missing Count": missing, "Missing %": miss_pct})

                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=missing.index, y=miss_pct,
                    marker_color=[_CHART_PALETTE[0] if v < 5
                                  else (_CHART_PALETTE[2] if v < 20 else _CHART_PALETTE[3])
                                  for v in miss_pct],
                    text=[f"{v:.1f}%" for v in miss_pct],
                    textposition="outside",
                ))
                fig.add_hline(y=5,  line_dash="dot", line_color="#f59e0b",
                              annotation_text="5% threshold")
                fig.add_hline(y=20, line_dash="dot", line_color="#ef4444",
                              annotation_text="20% threshold")
                _plotly_layout(fig, "Missing Values by Column (%)")
                fig.update_layout(yaxis_title="Missing %", xaxis_title="")
                st.plotly_chart(fig, use_container_width=True)
                st.dataframe(miss_df.style.background_gradient(subset=["Missing %"],
                             cmap="YlOrRd"), use_container_width=True)
            else:
                st.success("✅ No missing values — data is complete!")

        # ── Tab 4: Custom Chart ───────────────────────────────────────────────
        with viz_tabs[4]:
            if len(numeric_cols) >= 2:
                c1, c2, c3, c4 = st.columns(4)
                with c1: x_col  = st.selectbox("X-axis",   numeric_cols, key="cx")
                with c2: y_col  = st.selectbox("Y-axis",   numeric_cols, index=1, key="cy")
                with c3: c_col  = st.selectbox("Color by", ["—"] + cat_cols, key="cc")
                with c4: s_col  = st.selectbox("Size by",  ["—"] + numeric_cols, key="cs")

                chart_kind = st.radio("Chart type", ["Scatter", "Line", "Bar", "Area"],
                                      horizontal=True, key="custom_kind")

                color = c_col if c_col != "—" else None
                size  = s_col if s_col != "—" else None

                try:
                    if chart_kind == "Scatter":
                        fig = px.scatter(df, x=x_col, y=y_col, color=color, size=size,
                                         color_discrete_sequence=_CHART_PALETTE,
                                         trendline="ols", opacity=.75)
                    elif chart_kind == "Line":
                        fig = px.line(df.sort_values(x_col), x=x_col, y=y_col, color=color,
                                      color_discrete_sequence=_CHART_PALETTE)
                    elif chart_kind == "Bar":
                        fig = px.bar(df, x=x_col, y=y_col, color=color,
                                     color_discrete_sequence=_CHART_PALETTE, opacity=.85)
                    else:
                        fig = px.area(df.sort_values(x_col), x=x_col, y=y_col, color=color,
                                      color_discrete_sequence=_CHART_PALETTE)
                    _plotly_layout(fig, f"{chart_kind}: {y_col} vs {x_col}")
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Could not render chart: {e}")
            else:
                st.info("Need at least 2 numeric columns for custom charts.")

        st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 5 – QUALITY REPORT
# ─────────────────────────────────────────────────────────────────────────────

def _render_quality_report(df: pd.DataFrame):
    with st.container():
        st.markdown('<div class="sec-card">', unsafe_allow_html=True)
        _section_header("📋", "Data Quality Report")

        score, badge_cls = _quality_score(df)
        badge_labels = {"excellent": "⭐ Excellent", "good": "✅ Good",
                        "fair": "⚠️ Fair", "poor": "🔴 Poor"}

        st.markdown(
            f'Overall Quality:&nbsp; <span class="quality-badge {badge_cls}">'
            f'{badge_labels[badge_cls]} · {score}/100</span>',
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)

        col_miss, col_dup, col_out = st.columns(3)

        # ── Missing ──────────────────────────────────────────────────────────
        with col_miss:
            st.markdown("**Missing Values**")
            missing = df.isnull().sum()
            missing = missing[missing > 0].sort_values(ascending=False)
            if not missing.empty:
                pct = (missing / len(df) * 100).round(2)
                st.dataframe(pd.DataFrame({"Count": missing, "%": pct}),
                             use_container_width=True, height=220)
            else:
                st.success("None found")

        # ── Duplicates ───────────────────────────────────────────────────────
        with col_dup:
            st.markdown("**Duplicate Rows**")
            dup = df.duplicated().sum()
            st.metric("Duplicate count", f"{dup:,}",
                      delta=f"−{dup/max(len(df),1)*100:.1f}% rows" if dup else None,
                      delta_color="inverse")
            if dup > 0:
                st.warning(f"{dup} rows are exact duplicates.")
            else:
                st.success("No duplicates found")

        # ── Outliers ─────────────────────────────────────────────────────────
        with col_out:
            st.markdown("**Outliers (IQR)**")
            try:
                outliers = DataCleaner.detect_outliers(df, method="iqr")
                if outliers:
                    out_df = pd.DataFrame(
                        [(k, len(v)) for k, v in outliers.items()],
                        columns=["Column", "Outlier Count"]
                    )
                    st.dataframe(out_df, use_container_width=True,
                                 hide_index=True, height=220)
                else:
                    st.success("No outliers detected")
            except Exception:
                st.info("Install scipy for outlier detection.")

        # ── Recommendations ──────────────────────────────────────────────────
        st.markdown("<hr class='df-divider'>", unsafe_allow_html=True)
        st.markdown("**Recommendations**")

        recs = []
        missing_all = df.isnull().sum()
        high_missing = missing_all[missing_all / len(df) > 0.20].index.tolist()
        low_missing  = missing_all[(missing_all > 0) & (missing_all / len(df) <= 0.20)].index.tolist()
        dup_count = df.duplicated().sum()
        cat_cols  = df.select_dtypes(include=["object", "category"]).columns.tolist()
        num_cols  = df.select_dtypes(include="number").columns.tolist()

        if high_missing:
            recs.append(("🗑", f"<b>Drop or carefully evaluate</b> columns with >20% missing: "
                               f"<code>{', '.join(high_missing[:5])}</code>"))
        if low_missing:
            recs.append(("💉", f"<b>Impute</b> missing values in: "
                               f"<code>{', '.join(low_missing[:5])}</code> (mean / median / mode)"))
        if dup_count > 0:
            recs.append(("🔁", f"<b>Remove {dup_count:,} duplicate rows</b> to prevent skewed analysis"))
        if cat_cols:
            recs.append(("🏷", f"<b>Encode categorical columns</b> before ML: "
                               f"<code>{', '.join(cat_cols[:4])}</code>"))
        if len(num_cols) > 1:
            recs.append(("📐", "<b>Check correlations</b> — highly correlated features may need dimensionality reduction"))
        if not recs:
            recs.append(("✅", "<b>No major issues detected.</b> Data appears clean and ready for analysis."))

        for icon, text in recs:
            st.markdown(
                f'<div class="rec-item"><span class="rec-icon">{icon}</span>{text}</div>',
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  SECTION 6 – EXPORT
# ─────────────────────────────────────────────────────────────────────────────

def _render_export(df: pd.DataFrame):
    with st.container():
        st.markdown('<div class="sec-card">', unsafe_allow_html=True)
        _section_header("📤", "Export Cleaned Data")

        c1, c2, c3 = st.columns([2, 2, 3])

        with c1:
            fmt = st.selectbox("Format", ["CSV", "Excel (.xlsx)", "JSON", "Parquet"], key="export_fmt")

        with c2:
            filename = st.text_input("Filename (no extension)", "cleaned_data", key="export_name")

        with c3:
            st.markdown("<br>", unsafe_allow_html=True)
            if fmt == "CSV":
                data  = df.to_csv(index=False).encode("utf-8")
                mime  = "text/csv"
                fname = f"{filename}.csv"
            elif fmt == "Excel (.xlsx)":
                buf = io.BytesIO()
                with pd.ExcelWriter(buf, engine="openpyxl") as w:
                    df.to_excel(w, index=False)
                data  = buf.getvalue()
                mime  = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                fname = f"{filename}.xlsx"
            elif fmt == "JSON":
                data  = df.to_json(orient="records", indent=2).encode("utf-8")
                mime  = "application/json"
                fname = f"{filename}.json"
            else:
                buf  = io.BytesIO(); df.to_parquet(buf, index=False)
                data = buf.getvalue()
                mime = "application/octet-stream"
                fname = f"{filename}.parquet"

            st.download_button(
                label=f"⬇ Download {fmt}",
                data=data, file_name=fname, mime=mime,
                type="primary", use_container_width=True,
            )

        st.caption(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns · {_memory_str(df)}")
        st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  EMPTY STATE
# ─────────────────────────────────────────────────────────────────────────────

def _render_empty_state():
    st.markdown("""
    <div style="
        display:flex; flex-direction:column; align-items:center;
        justify-content:center; padding:4rem 2rem; text-align:center;
        background:#fff; border:1.5px dashed #cbd5e1; border-radius:16px;
        margin-top:1rem;
    ">
        <div style="font-size:3rem; margin-bottom:1rem;">📂</div>
        <h2 style="font-family:'Fraunces',serif; font-weight:300; font-size:1.5rem;
                   color:#1e293b; margin:0 0 .5rem; letter-spacing:-.02em;">
            No dataset loaded
        </h2>
        <p style="color:#94a3b8; font-size:.9rem; max-width:340px; line-height:1.6; margin:0 0 1.5rem;">
            Upload a CSV, Excel, or JSON file from the <strong>sidebar</strong>
            to start cleaning and visualising your data.
        </p>
        <div style="
            display:flex; gap:.75rem; flex-wrap:wrap; justify-content:center;
            font-size:.78rem; color:#64748b;
        ">
            <span style="background:#f1f5f9;border:1px solid #e2e8f0;
                         border-radius:6px;padding:.3rem .7rem;">📄 CSV</span>
            <span style="background:#f1f5f9;border:1px solid #e2e8f0;
                         border-radius:6px;padding:.3rem .7rem;">📊 Excel</span>
            <span style="background:#f1f5f9;border:1px solid #e2e8f0;
                         border-radius:6px;padding:.3rem .7rem;">🗃 JSON</span>
            <span style="background:#f1f5f9;border:1px solid #e2e8f0;
                         border-radius:6px;padding:.3rem .7rem;">🗜 Parquet</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def render_main_panel():
    """Render the full professional DataForge main panel."""
    _inject_styles()

    # ── Page header ──────────────────────────────────────────────────────────
    df_rows = st.session_state.get("data", pd.DataFrame()).shape[0]
    badge_text = f"{df_rows:,} rows loaded" if df_rows else "no data"

    st.markdown(f"""
    <div class="df-header">
        <div class="icon">🔬</div>
        <div>
            <h1>DataForge</h1>
            <p>Data Cleaning &amp; Visualization Toolkit</p>
        </div>
        <div class="pill">{badge_text}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Guard: no data ────────────────────────────────────────────────────────
    if "data" not in st.session_state or st.session_state["data"].empty:
        _render_empty_state()
        return

    df = st.session_state["data"]

    # ── Sections ─────────────────────────────────────────────────────────────
    _render_stats(df)
    _render_data_preview(df)
    _render_cleaning_controls(df)
    _render_visualizations(df)
    _render_quality_report(df)
    _render_export(df)