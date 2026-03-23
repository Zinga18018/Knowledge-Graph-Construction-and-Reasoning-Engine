"""
Sample Texts for Demo
=====================
Curated multi-paragraph texts rich in named entities and inter-entity
relationships, designed to showcase the knowledge graph pipeline.
"""

SAMPLE_TEXTS = {

    # ------------------------------------------------------------------
    "AI Research Paper Abstract": (
        "In recent years, the field of artificial intelligence has undergone a "
        "remarkable transformation driven by large language models. Geoffrey Hinton "
        "and Yann LeCun, both pioneers in deep learning, laid the groundwork that "
        "enabled breakthroughs such as the Transformer architecture. Their research "
        "at the University of Toronto and Meta respectively has shaped the entire "
        "landscape of modern neural networks.\n\n"

        "OpenAI, founded in San Francisco in 2015, developed GPT-4 — a large language "
        "model that demonstrated unprecedented capabilities in natural language processing. "
        "Sam Altman, as CEO of OpenAI, oversaw the release of ChatGPT in November 2022, "
        "which reached 100 million users within two months. Meanwhile, Google DeepMind, "
        "led by Demis Hassabis in London, released AlphaFold, revolutionising protein "
        "structure prediction using deep learning.\n\n"

        "At Stanford University in California, Fei-Fei Li and Andrew Ng pioneered "
        "computer vision and online machine learning education. Their contributions to "
        "TensorFlow and PyTorch ecosystems accelerated the adoption of neural networks "
        "across both academia and industry. The NeurIPS 2024 conference showcased over "
        "3,000 papers on topics ranging from reinforcement learning to retrieval-augmented "
        "generation.\n\n"

        "Anthropic, founded by Dario Amodei in San Francisco, has focused on AI safety "
        "research. Their work on constitutional AI and RLHF (Reinforcement Learning from "
        "Human Feedback) represents a paradigm shift in how large language models are "
        "aligned with human values. The collaboration between Anthropic and Google has "
        "further strengthened the responsible AI movement in Silicon Valley."
    ),

    # ------------------------------------------------------------------
    "Tech Industry News": (
        "NVIDIA, headquartered in Santa Clara, California, reported record revenue "
        "driven by surging demand for its AI accelerator chips. Jensen Huang, CEO of "
        "NVIDIA, announced new partnerships with Microsoft and Amazon to power their "
        "cloud-based machine learning infrastructure on AWS and Azure. The company's "
        "GPU technology has become the backbone of deep learning research worldwide.\n\n"

        "In a landmark deal, Microsoft, led by CEO Satya Nadella, invested $10 billion "
        "in OpenAI in January 2023, securing exclusive rights to integrate GPT-4 into "
        "its products. GitHub Copilot, powered by OpenAI's Codex model, has transformed "
        "software development, with over 1 million developers using the AI-powered "
        "coding assistant built on the Transformer architecture.\n\n"

        "Apple, under Tim Cook, has taken a different approach to artificial intelligence, "
        "focusing on on-device machine learning and privacy-first AI. At their headquarters "
        "in Cupertino, California, Apple's research team has developed advanced natural "
        "language processing models that run entirely on iPhone hardware without cloud "
        "connectivity. Samsung and Qualcomm have pursued similar edge AI strategies.\n\n"

        "The European Union introduced the AI Act in 2024, establishing the world's first "
        "comprehensive regulatory framework for artificial intelligence. The legislation "
        "affects major tech companies operating in Europe, including Google, Meta, and "
        "Amazon. Mark Zuckerberg responded by open-sourcing Meta's LLaMA models, while "
        "Sundar Pichai pledged Google's commitment to responsible AI development in "
        "partnership with UNESCO and the United Nations."
    ),

    # ------------------------------------------------------------------
    "Historical Event": (
        "The development of computing in the 20th century stands as one of humanity's "
        "greatest intellectual achievements. Alan Turing, working at Cambridge University "
        "in the 1930s, formulated the concept of a universal computing machine that could "
        "simulate any algorithmic process. His work at Bletchley Park during World War II "
        "on breaking the Enigma cipher demonstrated the practical power of computation.\n\n"

        "John von Neumann, a mathematician at the Institute for Advanced Study in "
        "Princeton, designed the architecture that bears his name in 1945. The von Neumann "
        "architecture — separating memory, processing, and input/output — remains the "
        "foundation of virtually every modern computer. Claude Shannon, working at Bell "
        "Labs in New Jersey, simultaneously developed information theory, establishing "
        "the mathematical framework for digital communication.\n\n"

        "Ada Lovelace, often regarded as the first computer programmer, wrote algorithms "
        "for Charles Babbage's Analytical Engine in London during the 1840s. Her vision "
        "of machines that could manipulate symbols beyond mere calculation anticipated "
        "modern artificial intelligence by over a century. The United Kingdom has since "
        "honored her legacy with Ada Lovelace Day, celebrated annually in October.\n\n"

        "The founding of the Internet can be traced to ARPANET, developed by the United "
        "States Department of Defense in the 1960s. Tim Berners-Lee, working at CERN in "
        "Switzerland, invented the World Wide Web in 1989. His creation transformed how "
        "humanity shares knowledge. Today, the convergence of quantum computing, "
        "artificial intelligence, and blockchain technology promises yet another "
        "revolution, with IBM, Google, and Microsoft leading the charge in quantum "
        "computing research from laboratories across North America and Europe."
    ),
}
