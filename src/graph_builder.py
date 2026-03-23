"""
Knowledge Graph Builder
=======================
Wraps a NetworkX DiGraph to construct, query, and export
knowledge graphs from extracted entities and relationships.
"""

from typing import List, Dict, Any, Optional
import networkx as nx
from pyvis.network import Network
import json


# Colour palette for entity types
ENTITY_COLORS = {
    "PERSON": "#00ff88",
    "ORG": "#00d4ff",
    "LOCATION": "#a855f7",
    "TECHNOLOGY": "#f59e0b",
    "DATE": "#ec4899",
}

ENTITY_SHAPES = {
    "PERSON": "dot",
    "ORG": "diamond",
    "LOCATION": "triangle",
    "TECHNOLOGY": "square",
    "DATE": "star",
}


class KnowledgeGraph:
    """
    A directed knowledge graph backed by ``networkx.DiGraph``.
    """

    def __init__(self):
        self.graph = nx.DiGraph()

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def add_entities(self, entities: List[Dict]) -> None:
        """
        Add entity nodes to the graph.

        Parameters
        ----------
        entities : list of dict
            Each dict must contain at least ``text`` and ``label`` keys.
        """
        for ent in entities:
            node_id = ent["text"]
            if self.graph.has_node(node_id):
                # Increment mention count
                self.graph.nodes[node_id]["mentions"] = (
                    self.graph.nodes[node_id].get("mentions", 1) + 1
                )
                continue

            self.graph.add_node(
                node_id,
                label=ent["label"],
                color=ENTITY_COLORS.get(ent["label"], "#888888"),
                shape=ENTITY_SHAPES.get(ent["label"], "dot"),
                mentions=1,
            )

    def add_relationships(self, relationships: List[Dict]) -> None:
        """
        Add directed edges (relationships) to the graph.

        Parameters
        ----------
        relationships : list of dict
            Each dict needs ``source``, ``target``, ``relation`` keys.
        """
        for rel in relationships:
            src, tgt = rel["source"], rel["target"]

            # Ensure nodes exist
            if not self.graph.has_node(src):
                self.graph.add_node(
                    src,
                    label=rel.get("source_label", "UNKNOWN"),
                    color=ENTITY_COLORS.get(rel.get("source_label"), "#888888"),
                    shape=ENTITY_SHAPES.get(rel.get("source_label"), "dot"),
                    mentions=1,
                )
            if not self.graph.has_node(tgt):
                self.graph.add_node(
                    tgt,
                    label=rel.get("target_label", "UNKNOWN"),
                    color=ENTITY_COLORS.get(rel.get("target_label"), "#888888"),
                    shape=ENTITY_SHAPES.get(rel.get("target_label"), "dot"),
                    mentions=1,
                )

            if self.graph.has_edge(src, tgt):
                self.graph.edges[src, tgt]["weight"] = (
                    self.graph.edges[src, tgt].get("weight", 1) + 1
                )
            else:
                self.graph.add_edge(
                    src,
                    tgt,
                    relation=rel["relation"],
                    weight=1,
                    sentence=rel.get("sentence", ""),
                )

    # ------------------------------------------------------------------
    # Queries & Analytics
    # ------------------------------------------------------------------

    def get_stats(self) -> Dict[str, Any]:
        """Return summary statistics of the knowledge graph."""
        G = self.graph

        label_counts: Dict[str, int] = {}
        for _, data in G.nodes(data=True):
            lbl = data.get("label", "UNKNOWN")
            label_counts[lbl] = label_counts.get(lbl, 0) + 1

        relation_counts: Dict[str, int] = {}
        for _, _, data in G.edges(data=True):
            rel = data.get("relation", "UNKNOWN")
            relation_counts[rel] = relation_counts.get(rel, 0) + 1

        communities = self.get_communities()

        # Degree centrality for top nodes
        if G.number_of_nodes() > 0:
            centrality = nx.degree_centrality(G)
            top_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]
        else:
            top_nodes = []

        return {
            "total_nodes": G.number_of_nodes(),
            "total_edges": G.number_of_edges(),
            "entity_type_counts": label_counts,
            "relation_type_counts": relation_counts,
            "num_communities": len(communities),
            "communities": communities,
            "top_central_nodes": top_nodes,
            "density": nx.density(G) if G.number_of_nodes() > 1 else 0,
        }

    def get_communities(self) -> List[List[str]]:
        """
        Detect communities using the greedy modularity algorithm
        on the undirected projection.
        """
        if self.graph.number_of_nodes() == 0:
            return []

        undirected = self.graph.to_undirected()
        try:
            from networkx.algorithms.community import greedy_modularity_communities
            communities = greedy_modularity_communities(undirected)
            return [sorted(list(c)) for c in communities]
        except Exception:
            # Fallback: connected components
            return [sorted(list(c)) for c in nx.connected_components(undirected)]

    def get_node_details(self, node_id: str) -> Optional[Dict]:
        """Return all attributes for a single node."""
        if not self.graph.has_node(node_id):
            return None
        data = dict(self.graph.nodes[node_id])
        data["id"] = node_id
        data["in_degree"] = self.graph.in_degree(node_id)
        data["out_degree"] = self.graph.out_degree(node_id)
        data["neighbors"] = list(self.graph.successors(node_id)) + list(
            self.graph.predecessors(node_id)
        )
        return data

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def to_pyvis(self, height: str = "600px", width: str = "100%") -> Network:
        """
        Convert the graph to a PyVis ``Network`` for interactive
        HTML visualisation.
        """
        net = Network(
            height=height,
            width=width,
            directed=True,
            bgcolor="#0a0a0a",
            font_color="white",
            select_menu=False,
            filter_menu=False,
        )

        net.barnes_hut(
            gravity=-8000,
            central_gravity=0.3,
            spring_length=200,
            spring_strength=0.05,
            damping=0.09,
        )

        for node_id, data in self.graph.nodes(data=True):
            mentions = data.get("mentions", 1)
            size = 15 + mentions * 5
            net.add_node(
                node_id,
                label=node_id,
                color=data.get("color", "#888888"),
                shape=data.get("shape", "dot"),
                size=min(size, 50),
                title=f"{data.get('label', 'UNKNOWN')}\nMentions: {mentions}",
                font={"size": 14, "color": "white"},
            )

        for src, tgt, data in self.graph.edges(data=True):
            relation = data.get("relation", "")
            weight = data.get("weight", 1)
            net.add_edge(
                src,
                tgt,
                title=relation,
                label=relation,
                width=min(weight * 1.5, 6),
                color={"color": "#444444", "highlight": "#00ff88"},
                font={"size": 10, "color": "#888888", "align": "middle"},
                arrows={"to": {"enabled": True, "scaleFactor": 0.5}},
                smooth={"type": "curvedCW", "roundness": 0.2},
            )

        return net

    def to_dict(self) -> Dict:
        """Serialise the graph to a JSON-safe dictionary."""
        return nx.node_link_data(self.graph)

    def from_dict(self, data: Dict) -> None:
        """Load a graph from a dictionary produced by ``to_dict``."""
        self.graph = nx.node_link_graph(data)
