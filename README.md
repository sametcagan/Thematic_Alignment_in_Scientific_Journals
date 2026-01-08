# AI USAGE DISCLAIMER
Parts of this project have been developed with the assistance of OpenAI’s ChatGPT (GPT-5). The AI was used to support the development of project ideas, the structuring of methodological workflows, the drafting of descriptive texts, and the identification of relevant datasets (arXiv scraping code and query). Figures and graphs developed with AI assistance have been carefully reviewed, edited, and validated by me. I take full responsibility for the final content and its accuracy, relevance, and academic integrity.

# Project Specification (P7): Analyzing Thematic Alignment in Scientific Journals

## Objective
The core objective of this project is to quantitatively assess whether the articles published in a target venue align with its stated **Aims & Scope**. The analysis should enable detection of:
- **Thematic drift** over time, and
- **Outlier papers** that are unusually misaligned with the venue’s declared mission.

## Reference Concept (“Ground Truth”)
The venue’s **Aims & Scope** text (sourced from an authoritative venue description) serves as the fixed thematic reference representing intended editorial focus.

## Core Pipeline
The required analytical pipeline consists of:

1. **Collect a corpus** of articles (at minimum, abstracts) from the target venue.
2. **Model the content** by converting both article text and the Aims & Scope text into machine-readable semantic representations (e.g., embeddings or topic distributions).
3. **Compute alignment** by generating a quantitative **alignment score** for each paper based on similarity to the Aims & Scope reference.
4. **Analyze and report findings** by examining alignment score distributions to identify drift and outliers, supported by qualitative inspection of extreme cases.

## Implementation in This Study
In this work, the venue specification is instantiated using a longitudinal corpus of Medical AI-related publications and a fixed scope reference statement embedded in the same semantic space. Alignment is operationalized through cosine similarity, and topic structure is recovered via unsupervised clustering to contextualize drift in terms of shifting research pillars.

