"""
Entity Extraction Engine
========================
Rule-based NER (Named Entity Recognition) using regex pattern matching.
Extracts PERSON, ORG, LOCATION, DATE, and TECHNOLOGY entities from text,
then infers relationships via sentence-level co-occurrence.
"""

import re
from typing import List, Dict, Tuple


# ---------------------------------------------------------------------------
# Pattern banks – curated regex patterns for each entity type
# ---------------------------------------------------------------------------

PERSON_PATTERNS = [
    # Titles followed by capitalized names
    r"(?:Dr|Prof|Mr|Mrs|Ms|Sir|Lord|President|CEO|CTO|Director)\.\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+",
    # Common well-known names (seed list)
    r"\b(?:Elon Musk|Jeff Bezos|Sam Altman|Demis Hassabis|Yann LeCun|Geoffrey Hinton|"
    r"Fei-Fei Li|Andrew Ng|Ilya Sutskever|Jensen Huang|Satya Nadella|Tim Cook|"
    r"Mark Zuckerberg|Sundar Pichai|Dario Amodei|Andrej Karpathy|"
    r"Alan Turing|Ada Lovelace|John von Neumann|Claude Shannon|"
    r"Albert Einstein|Isaac Newton|Marie Curie|Nikola Tesla|"
    r"Napoleon Bonaparte|Winston Churchill|Abraham Lincoln|Mahatma Gandhi|"
    r"Alexander Hamilton|Thomas Jefferson|Benjamin Franklin|George Washington|"
    r"Leonardo da Vinci|Galileo Galilei|Charles Darwin|Stephen Hawking)\b",
    # Two or three capitalized words that look like person names
    r"\b[A-Z][a-z]{2,15}\s+(?:[A-Z]\.\s+)?[A-Z][a-z]{2,15}\b",
]

ORG_PATTERNS = [
    r"\b(?:Google|Microsoft|Apple|Amazon|Meta|OpenAI|DeepMind|Anthropic|Tesla|"
    r"NVIDIA|IBM|Intel|AMD|Qualcomm|Samsung|TSMC|Oracle|Salesforce|Adobe|"
    r"Netflix|Spotify|Twitter|LinkedIn|GitHub|Stack Overflow|"
    r"MIT|Stanford|Harvard|Oxford|Cambridge|Berkeley|Carnegie Mellon|"
    r"NASA|CERN|WHO|UNESCO|United Nations|European Union|"
    r"IEEE|ACM|NeurIPS|ICML|ICLR|AAAI|CVPR|"
    r"Goldman Sachs|JPMorgan|Morgan Stanley|BlackRock)\b",
    r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Inc|Corp|Ltd|LLC|Group|Foundation|"
    r"Institute|University|Laboratory|Labs|Research|Association|Organization)\b",
    r"\b(?:University|Institute|Academy)\s+of\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b",
]

LOCATION_PATTERNS = [
    r"\b(?:New York|San Francisco|Silicon Valley|Los Angeles|Chicago|Boston|Seattle|"
    r"Washington D\.C\.|London|Paris|Berlin|Tokyo|Beijing|Shanghai|Mumbai|"
    r"Bangalore|Toronto|Montreal|Sydney|Singapore|Hong Kong|Dubai|"
    r"California|Texas|Massachusetts|Virginia|"
    r"United States|United Kingdom|China|India|Japan|Germany|France|Canada|"
    r"Australia|South Korea|Israel|Switzerland|"
    r"Europe|Asia|North America|South America|Africa)\b",
]

DATE_PATTERNS = [
    # Full dates
    r"\b(?:January|February|March|April|May|June|July|August|September|"
    r"October|November|December)\s+\d{1,2},?\s+\d{4}\b",
    # Month Year
    r"\b(?:January|February|March|April|May|June|July|August|September|"
    r"October|November|December)\s+\d{4}\b",
    # Year ranges & standalone years
    r"\b(?:19|20)\d{2}[-–]\d{2,4}\b",
    r"\b(?:19|20)\d{2}s?\b",
    # Relative dates
    r"\b(?:Q[1-4]\s+\d{4})\b",
]

TECHNOLOGY_PATTERNS = [
    r"\b(?:GPT-[0-9]+|GPT|BERT|Transformer|LLM|LLMs|DALL[-·]E|Stable Diffusion|"
    r"ChatGPT|Copilot|AlphaFold|AlphaGo|"
    r"Python|JavaScript|TypeScript|Rust|Go|Java|C\+\+|SQL|"
    r"TensorFlow|PyTorch|Keras|scikit-learn|Hugging Face|LangChain|"
    r"Kubernetes|Docker|AWS|Azure|GCP|"
    r"blockchain|quantum computing|machine learning|deep learning|"
    r"artificial intelligence|natural language processing|NLP|"
    r"computer vision|reinforcement learning|neural network|neural networks|"
    r"convolutional neural network|CNN|RNN|LSTM|GAN|GANs|"
    r"large language model|retrieval-augmented generation|RAG|"
    r"knowledge graph|attention mechanism|self-attention)\b",
]

# Map label -> compiled patterns
ENTITY_PATTERNS: Dict[str, List[re.Pattern]] = {
    "TECHNOLOGY": [re.compile(p, re.IGNORECASE) for p in TECHNOLOGY_PATTERNS],
    "ORG":        [re.compile(p) for p in ORG_PATTERNS],
    "LOCATION":   [re.compile(p) for p in LOCATION_PATTERNS],
    "DATE":       [re.compile(p) for p in DATE_PATTERNS],
    "PERSON":     [re.compile(p) for p in PERSON_PATTERNS],
}

# Words that should never be tagged as PERSON
PERSON_STOPWORDS = {
    "The", "This", "That", "These", "Those", "Here", "There",
    "However", "Moreover", "Furthermore", "Although", "Because",
    "While", "During", "After", "Before", "Since", "Within",
    "Between", "Through", "About", "Their", "Where", "Which",
    "Every", "Other", "Another", "First", "Second", "Third",
    "Many", "Most", "Some", "Such", "Each", "Both", "Several",
    "Recent", "Major", "Large", "Small", "High", "Early", "Late",
    "With", "From", "Into", "Over", "Under", "Also", "Just",
    "More", "Very", "Much", "Well", "Even", "Still", "Already",
    "Knowledge Graph", "Construction", "Reasoning", "Engine",
    "Research", "Development", "Analysis", "Processing", "Learning",
}


class EntityExtractor:
    """
    Rule-based Named Entity Recognition engine.

    Uses curated regex patterns to identify entities in text without
    requiring large spaCy model downloads.
    """

    def __init__(self):
        self.patterns = ENTITY_PATTERNS

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def extract(self, text: str) -> List[Dict]:
        """
        Extract named entities from *text*.

        Returns a list of dicts:
            [{"text": ..., "label": ..., "start": ..., "end": ...}, ...]
        """
        raw_entities: List[Dict] = []

        for label, compiled_patterns in self.patterns.items():
            for pattern in compiled_patterns:
                for match in pattern.finditer(text):
                    entity_text = match.group().strip()

                    # Filter noisy PERSON matches
                    if label == "PERSON" and entity_text in PERSON_STOPWORDS:
                        continue
                    if label == "PERSON" and len(entity_text.split()) < 2:
                        continue

                    raw_entities.append({
                        "text": entity_text,
                        "label": label,
                        "start": match.start(),
                        "end": match.end(),
                    })

        # Deduplicate overlapping spans (prefer longer matches)
        entities = self._resolve_overlaps(raw_entities)
        return entities

    def extract_relationships(
        self, text: str, entities: List[Dict] | None = None
    ) -> List[Dict]:
        """
        Infer relationships between entities via sentence co-occurrence.

        Returns a list of dicts:
            [{"source": ..., "target": ..., "relation": ..., "sentence": ...}, ...]
        """
        if entities is None:
            entities = self.extract(text)

        sentences = self._split_sentences(text)
        relationships: List[Dict] = []
        seen: set = set()

        for sentence in sentences:
            # Find entities present in this sentence
            present = [
                e for e in entities
                if e["text"] in sentence
            ]

            for i, src in enumerate(present):
                for tgt in present[i + 1:]:
                    key = (src["text"], tgt["text"])
                    if key in seen:
                        continue
                    seen.add(key)

                    relation = self._infer_relation(src, tgt, sentence)
                    relationships.append({
                        "source": src["text"],
                        "target": tgt["text"],
                        "source_label": src["label"],
                        "target_label": tgt["label"],
                        "relation": relation,
                        "sentence": sentence.strip(),
                    })

        return relationships

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _resolve_overlaps(entities: List[Dict]) -> List[Dict]:
        """Keep the longest span when two entities overlap."""
        # Sort by start, then by descending length
        entities.sort(key=lambda e: (e["start"], -(e["end"] - e["start"])))
        result: List[Dict] = []
        last_end = -1
        for ent in entities:
            if ent["start"] >= last_end:
                result.append(ent)
                last_end = ent["end"]
        return result

    @staticmethod
    def _split_sentences(text: str) -> List[str]:
        """Naive sentence splitter."""
        return re.split(r"(?<=[.!?])\s+", text)

    @staticmethod
    def _infer_relation(src: Dict, tgt: Dict, sentence: str) -> str:
        """Heuristic relation labelling based on entity types and context."""
        pair = (src["label"], tgt["label"])

        # Keyword-based relation detection
        s_lower = sentence.lower()

        if any(kw in s_lower for kw in ["founded", "co-founded", "started", "created"]):
            if pair in [("PERSON", "ORG"), ("PERSON", "TECHNOLOGY")]:
                return "FOUNDED"
        if any(kw in s_lower for kw in ["acquired", "bought", "purchased", "merged"]):
            return "ACQUIRED"
        if any(kw in s_lower for kw in ["works at", "joined", "hired", "employed"]):
            return "WORKS_AT"
        if any(kw in s_lower for kw in ["located in", "based in", "headquartered"]):
            return "LOCATED_IN"
        if any(kw in s_lower for kw in ["developed", "built", "designed", "invented"]):
            return "DEVELOPED"
        if any(kw in s_lower for kw in ["published", "released", "announced", "launched"]):
            return "RELEASED"
        if any(kw in s_lower for kw in ["uses", "using", "powered by", "built on", "leverages"]):
            return "USES"
        if any(kw in s_lower for kw in ["competed", "versus", "rivaling", "competing"]):
            return "COMPETES_WITH"
        if any(kw in s_lower for kw in ["collaborated", "partnered", "partnership"]):
            return "COLLABORATES_WITH"
        if any(kw in s_lower for kw in ["invested", "funding", "backed"]):
            return "INVESTED_IN"

        # Fallback: type-pair heuristics
        relation_map = {
            ("PERSON", "ORG"): "AFFILIATED_WITH",
            ("PERSON", "TECHNOLOGY"): "WORKS_ON",
            ("PERSON", "LOCATION"): "LOCATED_IN",
            ("ORG", "TECHNOLOGY"): "DEVELOPS",
            ("ORG", "LOCATION"): "LOCATED_IN",
            ("ORG", "ORG"): "RELATED_TO",
            ("TECHNOLOGY", "TECHNOLOGY"): "RELATED_TO",
            ("PERSON", "PERSON"): "ASSOCIATED_WITH",
            ("PERSON", "DATE"): "ACTIVE_IN",
            ("ORG", "DATE"): "ACTIVE_IN",
            ("TECHNOLOGY", "DATE"): "EMERGED_IN",
        }

        return relation_map.get(pair, relation_map.get((tgt["label"], src["label"]), "RELATED_TO"))
