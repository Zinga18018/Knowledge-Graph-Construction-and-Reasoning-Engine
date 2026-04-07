# GraphMind -- Knowledge Graph Construction and Reasoning Engine

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31%2B-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![spaCy](https://img.shields.io/badge/spaCy-3.7%2B-09A3D5?style=flat-square&logo=spacy&logoColor=white)](https://spacy.io)
[![NetworkX](https://img.shields.io/badge/NetworkX-3.2%2B-4C9A2A?style=flat-square)](https://networkx.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-00ff88?style=flat-square)](LICENSE)

Transform unstructured text into interactive knowledge graphs using rule-based NER, graph reasoning, and community detection -- all in a Streamlit interface.

---

## Features

| Feature | Description |
|---|---|
| **Rule-Based NER** | Regex-powered entity extraction -- no large model downloads required |
| **5 Entity Types** | PERSON, ORG, LOCATION, DATE, TECHNOLOGY |
| **Relationship Inference** | Sentence co-occurrence + keyword heuristics for edge labelling |
| **Interactive Graph** | Drag, zoom, hover -- powered by PyVis with dark theme |
| **Community Detection** | Greedy modularity clustering via NetworkX |
| **Analytics Dashboard** | Plotly charts for entity distributions, centrality, communities |
| **Demo Texts** | 3 curated multi-paragraph texts for instant exploration |
| **Custom Input** | Paste any text and build a graph on the fly |

---

## Quick Start

```bash
git clone https://github.com/Zinga18018/Knowledge-Graph-Construction-and-Reasoning-Engine.git
cd Knowledge-Graph-Construction-and-Reasoning-Engine
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # macOS / Linux
pip install -r requirements.txt
streamlit run app.py
```

The app will open at **http://localhost:8501**.

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | Streamlit | Interactive web dashboard |
| **NER Engine** | Regex + Rule-based | Named entity recognition |
| **Graph Engine** | NetworkX | Graph construction and algorithms |
| **Visualisation** | PyVis | Interactive HTML graph rendering |
| **Charts** | Plotly | Statistical visualisations |
| **Data** | Pandas | Tabular entity / relationship display |

---

## Project Structure

```
Knowledge-Graph-Construction-and-Reasoning-Engine/
|-- app.py                  # Streamlit entry point
|-- requirements.txt        # Python dependencies
|-- README.md
|-- .gitignore
|-- src/
|   |-- __init__.py
|   |-- extractor.py        # Rule-based NER engine
|   |-- graph_builder.py    # NetworkX knowledge graph wrapper
|   |-- visualizer.py       # PyVis + Plotly rendering
|   +-- sample_texts.py     # Curated demo texts
```

---

## Entity Color Palette

| Entity Type | Color | Hex |
|---|---|---|
| PERSON | Green | `#00ff88` |
| ORG | Cyan | `#00d4ff` |
| LOCATION | Purple | `#a855f7` |
| TECHNOLOGY | Amber | `#f59e0b` |
| DATE | Pink | `#ec4899` |

---

## License

MIT License -- Yogesh Kuchimanchi
