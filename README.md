# 🧠 GraphMind — Knowledge Graph Construction & Reasoning Engine

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![spaCy](https://img.shields.io/badge/spaCy-3.7%2B-09A3D5?logo=spacy&logoColor=white)](https://spacy.io)
[![NetworkX](https://img.shields.io/badge/NetworkX-3.2%2B-4C9A2A?logo=python&logoColor=white)](https://networkx.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-00ff88.svg)](LICENSE)

> **Transform unstructured text into interactive knowledge graphs** using rule-based NER,
> graph reasoning, and community detection — all in a sleek Streamlit interface.

---

## 📐 Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          GraphMind Pipeline                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌──────────┐    ┌──────────────┐    ┌───────────────┐            │
│   │          │    │   Entity     │    │   Knowledge   │            │
│   │  Text    │───▶│  Extractor   │───▶│   Graph       │            │
│   │  Input   │    │  (NER)       │    │   Builder     │            │
│   │          │    │              │    │  (NetworkX)   │            │
│   └──────────┘    └──────┬───────┘    └───────┬───────┘            │
│                          │                    │                     │
│                          ▼                    ▼                     │
│                  ┌───────────────┐    ┌───────────────┐            │
│                  │  Relationship │    │  Community    │            │
│                  │  Inference    │    │  Detection    │            │
│                  │  (Co-occur.)  │    │  (Modularity) │            │
│                  └───────┬───────┘    └───────┬───────┘            │
│                          │                    │                     │
│                          ▼                    ▼                     │
│                  ┌─────────────────────────────────────┐           │
│                  │          Visualizer                  │           │
│                  │   ┌─────────┐   ┌──────────────┐   │           │
│                  │   │  PyVis  │   │   Plotly      │   │           │
│                  │   │  Graph  │   │   Charts      │   │           │
│                  │   └─────────┘   └──────────────┘   │           │
│                  └─────────────────────────────────────┘           │
│                                    │                               │
│                                    ▼                               │
│                           ┌────────────────┐                       │
│                           │   Streamlit    │                       │
│                           │   Dashboard    │                       │
│                           └────────────────┘                       │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

| Feature | Description |
|---|---|
| **Rule-Based NER** | Regex-powered entity extraction — no large model downloads required |
| **5 Entity Types** | `PERSON` · `ORG` · `LOCATION` · `DATE` · `TECHNOLOGY` |
| **Relationship Inference** | Sentence co-occurrence + keyword heuristics for edge labelling |
| **Interactive Graph** | Drag, zoom, hover — powered by PyVis with dark theme |
| **Community Detection** | Greedy modularity clustering via NetworkX |
| **Analytics Dashboard** | Plotly charts for entity distributions, centrality, communities |
| **Demo Texts** | 3 curated multi-paragraph texts for instant exploration |
| **Custom Input** | Paste any text and build a graph on the fly |
| **Configurable** | Filter entity types, set minimum mention thresholds |

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/yogeshkuchimanchi/Knowledge-Graph-Construction-and-Reasoning-Engine.git
cd Knowledge-Graph-Construction-and-Reasoning-Engine
```

### 2. Create a virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

The app will open at **http://localhost:8501**.

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | Streamlit | Interactive web dashboard |
| **NER Engine** | Regex + Rule-based | Named entity recognition |
| **Graph Engine** | NetworkX | Graph construction & algorithms |
| **Visualisation** | PyVis | Interactive HTML graph rendering |
| **Charts** | Plotly | Statistical visualisations |
| **Data** | Pandas | Tabular entity / relationship display |

---

## 📁 Project Structure

```
Knowledge-Graph-Construction-and-Reasoning-Engine/
├── app.py                  # Streamlit entry point
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── extractor.py        # Rule-based NER engine
│   ├── graph_builder.py    # NetworkX knowledge graph wrapper
│   ├── visualizer.py       # PyVis + Plotly rendering
│   └── sample_texts.py     # Curated demo texts
├── data/                   # (reserved for exported graphs)
└── assets/                 # (reserved for static assets)
```

---

## 🎨 Entity Color Palette

| Entity Type | Colour | Hex |
|---|---|---|
| PERSON | 🟢 Green | `#00ff88` |
| ORG | 🔵 Cyan | `#00d4ff` |
| LOCATION | 🟣 Purple | `#a855f7` |
| TECHNOLOGY | 🟡 Amber | `#f59e0b` |
| DATE | 🩷 Pink | `#ec4899` |

---

## 📜 License

MIT License — **Yogesh Kuchimanchi**

```
MIT License

Copyright (c) 2026 Yogesh Kuchimanchi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
