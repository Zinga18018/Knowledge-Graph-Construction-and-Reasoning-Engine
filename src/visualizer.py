"""
Graph Visualization Utilities
==============================
Functions for rendering knowledge graphs as interactive HTML (PyVis)
and statistical charts (Plotly).
"""

from typing import Dict, Any
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from src.graph_builder import KnowledgeGraph, ENTITY_COLORS


# ------------------------------------------------------------------
# PyVis interactive graph
# ------------------------------------------------------------------

def create_pyvis_graph(kg: KnowledgeGraph, height: str = "650px") -> str:
    """
    Render *kg* as an interactive PyVis graph and return raw HTML.

    The HTML string can be embedded directly with
    ``streamlit.components.v1.html()``.
    """
    net = kg.to_pyvis(height=height)

    # Generate HTML string (PyVis >= 0.3 supports generate_html)
    try:
        html = net.generate_html()
    except AttributeError:
        # Fallback for older pyvis
        import tempfile, os
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8")
        net.save_graph(tmp.name)
        tmp.close()
        with open(tmp.name, "r", encoding="utf-8") as f:
            html = f.read()
        os.unlink(tmp.name)

    return html


# ------------------------------------------------------------------
# Plotly statistical charts
# ------------------------------------------------------------------

_CHART_LAYOUT = dict(
    paper_bgcolor="#0a0a0a",
    plot_bgcolor="#111111",
    font_color="white",
    font_size=13,
    margin=dict(l=40, r=40, t=50, b=40),
)


def graph_stats_chart(stats: Dict[str, Any]) -> go.Figure:
    """
    Create a combined Plotly figure with:
      - Entity type distribution (bar)
      - Relationship type distribution (bar)
    """
    entity_counts = stats.get("entity_type_counts", {})
    relation_counts = stats.get("relation_type_counts", {})

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=("Entity Types", "Relationship Types"),
        horizontal_spacing=0.15,
    )

    # --- Entity type bar chart ---
    if entity_counts:
        types = list(entity_counts.keys())
        counts = list(entity_counts.values())
        colors = [ENTITY_COLORS.get(t, "#888888") for t in types]

        fig.add_trace(
            go.Bar(
                x=types,
                y=counts,
                marker_color=colors,
                text=counts,
                textposition="outside",
                name="Entity Types",
                showlegend=False,
            ),
            row=1,
            col=1,
        )

    # --- Relationship type bar chart ---
    if relation_counts:
        rels = list(relation_counts.keys())
        rcounts = list(relation_counts.values())

        fig.add_trace(
            go.Bar(
                x=rels,
                y=rcounts,
                marker_color="#00d4ff",
                text=rcounts,
                textposition="outside",
                name="Relationships",
                showlegend=False,
            ),
            row=1,
            col=2,
        )

    fig.update_layout(
        height=370,
        **_CHART_LAYOUT,
    )
    fig.update_xaxes(tickangle=-40)

    return fig


def centrality_chart(top_nodes: list) -> go.Figure:
    """
    Horizontal bar chart of the top-N most central nodes.
    """
    if not top_nodes:
        fig = go.Figure()
        fig.update_layout(
            title="No nodes to display",
            **_CHART_LAYOUT,
            height=300,
        )
        return fig

    names = [n[0] for n in reversed(top_nodes)]
    values = [round(n[1], 4) for n in reversed(top_nodes)]

    fig = go.Figure(
        go.Bar(
            x=values,
            y=names,
            orientation="h",
            marker=dict(
                color=values,
                colorscale=[[0, "#0a0a0a"], [0.5, "#00d4ff"], [1, "#00ff88"]],
            ),
            text=[f"{v:.3f}" for v in values],
            textposition="outside",
        )
    )

    fig.update_layout(
        title="Top Nodes by Degree Centrality",
        xaxis_title="Centrality Score",
        height=max(300, len(top_nodes) * 35 + 100),
        **_CHART_LAYOUT,
    )

    return fig


def community_chart(communities: list) -> go.Figure:
    """Pie chart showing community sizes."""
    if not communities:
        fig = go.Figure()
        fig.update_layout(title="No communities detected", **_CHART_LAYOUT, height=300)
        return fig

    labels = [f"Community {i+1}" for i in range(len(communities))]
    sizes = [len(c) for c in communities]

    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=sizes,
            hole=0.45,
            marker=dict(
                colors=["#00ff88", "#00d4ff", "#a855f7", "#f59e0b", "#ec4899",
                         "#6366f1", "#14b8a6", "#f43f5e", "#84cc16", "#06b6d4"],
            ),
            textinfo="label+percent",
            textfont_size=12,
        )
    )

    fig.update_layout(
        title="Community Distribution",
        height=370,
        **_CHART_LAYOUT,
    )

    return fig
