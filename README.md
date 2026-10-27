# GraphMind — Rule-based entity graphs

A Streamlit app that turns text into a heuristic entity graph. Regex patterns and seed-name lists identify PERSON, ORG, LOCATION, DATE and TECHNOLOGY entities. Entities found in the same sentence are connected, with edge labels chosen from keyword and entity-type rules.

The graph is useful for exploring what those rules extract; it is not a verified knowledge base or a formal reasoning system.

## Run locally

Use Python 3.10+:

```bash
git clone https://github.com/Zinga18018/Knowledge-Graph-Construction-and-Reasoning-Engine.git
cd Knowledge-Graph-Construction-and-Reasoning-Engine
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

On Windows PowerShell, replace the activation line with `.\.venv\Scripts\Activate.ps1`. Open the local URL printed by Streamlit, normally `http://localhost:8501`.

Choose a bundled demo or paste text, select entity types and build the graph. The current extractor does not load a spaCy model; spaCy is listed in [requirements.txt](requirements.txt), but the implemented extraction is rule-based. No model download, API key or GPU is needed for the extraction algorithm. Package installation still requires its dependencies.

## What the app shows

- A draggable PyVis graph, with entity labels and relationship tooltips.
- Entity and relationship tables.
- Plotly summaries of entity types, degree centrality and communities.
- NetworkX graph statistics and greedy-modularity communities on an undirected projection.

[app.py](app.py) connects the interface to [src/extractor.py](src/extractor.py), [src/graph_builder.py](src/graph_builder.py) and [src/visualizer.py](src/visualizer.py). Bundled examples are in [src/sample_texts.py](src/sample_texts.py).

## Interpretation and current limits

Co-occurrence does not prove a relationship. Edge direction and labels come from heuristics, not fact checking; negation, ambiguous names and coreference can produce misleading results. Community membership and centrality describe this constructed graph, not real-world importance. The bundled prose is demonstration input, not verified evidence.

The “minimum mentions” slider is currently not passed into the extraction/filtering pipeline, so changing it does not implement the advertised filter. This is a known code limitation, not fixed by the README.

No labeled extraction evaluation, reasoning benchmark or automated test suite is committed. Dependencies have minimum versions rather than a reproducible lockfile.

Setup and browser flows were not rerun for this documentation update.

## License

MIT License -- Yogesh Kuchimanchi

The attribution and license statement above are retained from the existing README. The repository currently has no `LICENSE` file; no license text or new grant is supplied by this documentation.

