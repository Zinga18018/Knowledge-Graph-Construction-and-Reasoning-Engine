"""
GraphMind — Knowledge Graph Construction & Reasoning Engine
============================================================
Main Streamlit application.
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

from src.extractor import EntityExtractor
from src.graph_builder import KnowledgeGraph, ENTITY_COLORS
from src.visualizer import (
    create_pyvis_graph,
    graph_stats_chart,
    centrality_chart,
    community_chart,
)
from src.sample_texts import SAMPLE_TEXTS

# ======================================================================
# Page configuration
# ======================================================================

st.set_page_config(
    page_title="GraphMind | Knowledge Graph",
    page_icon="G",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ======================================================================
# Custom CSS — dark theme with accent colours
# ======================================================================

st.markdown(
    """
    <style>
    /* ---- Global ---- */
    .stApp {
        background-color: #0a0a0a;
        color: #e0e0e0;
    }

    /* ---- Sidebar ---- */
    section[data-testid="stSidebar"] {
        background-color: #111111;
        border-right: 1px solid #1e1e1e;
    }

    /* ---- Headers ---- */
    h1, h2, h3, h4 {
        color: #ffffff !important;
    }

    /* ---- Metric cards ---- */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #111111 0%, #1a1a2e 100%);
        border: 1px solid #1e1e1e;
        border-radius: 12px;
        padding: 16px 20px;
    }
    div[data-testid="stMetric"] label {
        color: #888888 !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #00ff88 !important;
        font-weight: 700;
    }

    /* ---- Buttons ---- */
    .stButton > button {
        background: linear-gradient(135deg, #00ff88 0%, #00d4ff 100%);
        color: #0a0a0a;
        border: none;
        border-radius: 8px;
        font-weight: 700;
        padding: 0.5rem 1.5rem;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,255,136,0.3);
    }

    /* ---- Tabs ---- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1a1a;
        border-radius: 8px 8px 0 0;
        color: #888888;
        padding: 8px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1e1e2e;
        color: #00ff88 !important;
    }

    /* ---- DataFrame ---- */
    .stDataFrame {
        border: 1px solid #1e1e1e;
        border-radius: 8px;
    }

    /* ---- Expanders ---- */
    .streamlit-expanderHeader {
        background-color: #111111;
        border-radius: 8px;
    }

    /* ---- Success / info banners ---- */
    .stAlert {
        background-color: #111111;
        border: 1px solid #1e1e1e;
        border-radius: 8px;
    }

    /* ---- Accent text helpers ---- */
    .accent-green { color: #00ff88; font-weight: 700; }
    .accent-blue  { color: #00d4ff; font-weight: 700; }

    /* ---- Legend colour pills ---- */
    .legend-pill {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 20px;
        margin: 2px 4px;
        font-size: 0.82rem;
        font-weight: 600;
        color: #0a0a0a;
    }

    /* ---- Divider ---- */
    hr {
        border-color: #1e1e1e;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ======================================================================
# Sidebar
# ======================================================================

with st.sidebar:
    st.markdown("## GraphMind")
    st.markdown(
        "<span class='accent-green'>Knowledge Graph</span> "
        "<span class='accent-blue'>Construction & Reasoning</span>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # --- Input source ---
    st.markdown("### Text Source")
    input_mode = st.radio(
        "Choose input method",
        ["Demo Texts", "Paste Your Own"],
        label_visibility="collapsed",
    )

    text_to_process = ""

    if input_mode == "Demo Texts":
        selected_demo = st.selectbox(
            "Select a demo text",
            list(SAMPLE_TEXTS.keys()),
        )
        text_to_process = SAMPLE_TEXTS[selected_demo]
        with st.expander("Preview text", expanded=False):
            st.caption(text_to_process[:500] + "…")
    else:
        text_to_process = st.text_area(
            "Paste your text below",
            height=250,
            placeholder="Enter text containing named entities…",
        )

    st.markdown("---")

    # --- Extraction settings ---
    st.markdown("### Extraction Settings")
    entity_types = st.multiselect(
        "Entity types to extract",
        ["PERSON", "ORG", "LOCATION", "DATE", "TECHNOLOGY"],
        default=["PERSON", "ORG", "LOCATION", "DATE", "TECHNOLOGY"],
    )

    min_mentions = st.slider(
        "Minimum mentions for nodes",
        min_value=1,
        max_value=5,
        value=1,
        help="Only show entities mentioned at least this many times.",
    )

    st.markdown("---")

    # --- Build button ---
    build_clicked = st.button(" Build Knowledge Graph", use_container_width=True)

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center;color:#555;font-size:0.75rem;'>"
        "Built by <b>Yogesh Kuchimanchi</b><br>MIT License</div>",
        unsafe_allow_html=True,
    )


# ======================================================================
# Main area — Header
# ======================================================================

st.markdown(
    "<h1 style='text-align:center;'>"
    " Graph<span class='accent-green'>Mind</span></h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center;color:#888;margin-top:-10px;'>"
    "Construct knowledge graphs from unstructured text using rule-based NER "
    "and graph reasoning.</p>",
    unsafe_allow_html=True,
)

# Colour legend
legend_html = " ".join(
    f"<span class='legend-pill' style='background:{color};'>{label}</span>"
    for label, color in ENTITY_COLORS.items()
)
st.markdown(
    f"<div style='text-align:center;margin-bottom:20px;'>{legend_html}</div>",
    unsafe_allow_html=True,
)


# ======================================================================
# Processing pipeline
# ======================================================================

@st.cache_data(show_spinner=False)
def run_pipeline(text: str, types: tuple):
    """Run NER + graph construction and cache results."""
    extractor = EntityExtractor()
    entities = extractor.extract(text)

    # Filter entity types
    entities = [e for e in entities if e["label"] in types]

    relationships = extractor.extract_relationships(text, entities)

    kg = KnowledgeGraph()
    kg.add_entities(entities)
    kg.add_relationships(relationships)

    stats = kg.get_stats()
    graph_html = create_pyvis_graph(kg)

    return entities, relationships, kg, stats, graph_html


# ======================================================================
# Run on button click OR first load with demo text
# ======================================================================

if "has_run" not in st.session_state:
    st.session_state.has_run = False

if build_clicked and text_to_process.strip():
    st.session_state.has_run = True
    st.session_state.text = text_to_process
    st.session_state.types = tuple(entity_types)

# Auto-run on first visit with demo text
if not st.session_state.has_run and input_mode == "Demo Texts":
    st.session_state.has_run = True
    st.session_state.text = text_to_process
    st.session_state.types = tuple(entity_types)

if st.session_state.has_run:
    with st.spinner("Extracting entities and building graph…"):
        entities, relationships, kg, stats, graph_html = run_pipeline(
            st.session_state.text, st.session_state.types
        )

    # ==================================================================
    # Metrics row
    # ==================================================================
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Nodes", stats["total_nodes"])
    m2.metric("Total Edges", stats["total_edges"])
    m3.metric("Communities", stats["num_communities"])
    m4.metric("Entity Types", len(stats["entity_type_counts"]))

    st.markdown("---")

    # ==================================================================
    # Tabs
    # ==================================================================
    tab_graph, tab_entities, tab_relations, tab_stats = st.tabs(
        [" Interactive Graph", " Entities", " Relationships", " Statistics"]
    )

    # --- Interactive Graph ---
    with tab_graph:
        st.markdown("#### Interactive Knowledge Graph")
        st.caption("Drag, zoom, and hover nodes for details.")
        components.html(graph_html, height=680, scrolling=False)

    # --- Entities table ---
    with tab_entities:
        st.markdown("#### Extracted Entities")
        if entities:
            df_ent = pd.DataFrame(entities)
            df_ent = df_ent[["text", "label", "start", "end"]]
            df_ent.columns = ["Entity", "Type", "Start", "End"]

            # Colour-coded type column
            st.dataframe(
                df_ent.style.apply(
                    lambda row: [
                        "",
                        f"color: {ENTITY_COLORS.get(row['Type'], '#888')}",
                        "",
                        "",
                    ],
                    axis=1,
                ),
                use_container_width=True,
                height=450,
            )
            st.caption(f"Total: **{len(entities)}** entities extracted.")
        else:
            st.info("No entities found. Try different text or settings.")

    # --- Relationships table ---
    with tab_relations:
        st.markdown("#### Extracted Relationships")
        if relationships:
            df_rel = pd.DataFrame(relationships)
            df_rel = df_rel[["source", "relation", "target", "source_label", "target_label"]]
            df_rel.columns = ["Source", "Relation", "Target", "Src Type", "Tgt Type"]
            st.dataframe(df_rel, use_container_width=True, height=450)
            st.caption(f"Total: **{len(relationships)}** relationships inferred.")
        else:
            st.info("No relationships found.")

    # --- Statistics ---
    with tab_stats:
        st.markdown("#### Graph Analytics")

        col_left, col_right = st.columns(2)

        with col_left:
            fig_dist = graph_stats_chart(stats)
            st.plotly_chart(fig_dist, use_container_width=True)

        with col_right:
            fig_community = community_chart(stats["communities"])
            st.plotly_chart(fig_community, use_container_width=True)

        st.markdown("---")
        fig_central = centrality_chart(stats["top_central_nodes"])
        st.plotly_chart(fig_central, use_container_width=True)

        with st.expander("Community Details"):
            for i, comm in enumerate(stats["communities"]):
                st.markdown(
                    f"**Community {i+1}** ({len(comm)} members): "
                    + ", ".join(comm)
                )

        with st.expander("Raw Statistics"):
            st.json(
                {
                    "density": round(stats["density"], 6),
                    "total_nodes": stats["total_nodes"],
                    "total_edges": stats["total_edges"],
                    "entity_type_counts": stats["entity_type_counts"],
                    "relation_type_counts": stats["relation_type_counts"],
                    "num_communities": stats["num_communities"],
                }
            )

else:
    # Placeholder when nothing has been processed yet
    st.markdown(
        "<div style='text-align:center;padding:80px 20px;color:#555;'>"
        "<h3>Paste text or select a demo, then click "
        "<span class='accent-green'>Build Knowledge Graph</span></h3>"
        "<p>The engine will extract entities, infer relationships, "
        "and visualise an interactive knowledge graph.</p>"
        "</div>",
        unsafe_allow_html=True,
    )
