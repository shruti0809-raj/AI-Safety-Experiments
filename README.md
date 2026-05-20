# Iterative Cross-Model Red Teaming (ICRT)

A Framework for Adversarial Evaluation of Frontier AI Safety

## Overview

This repository contains the complete **Iterative Cross-Model Red Teaming (ICRT)** experiment and framework, demonstrating how frontier LLMs can be used as adversarial agents to probe and exploit the safety boundaries of peer systems.

The experiment evaluated Claude, ChatGPT, and Gemini using a 6-cell cross-model attack matrix across three high-risk domains: cybersecurity, biological/chemical hazards, and manipulation. The key finding: all three models willingly generated adversarial attack prompts targeting peer systems without any resistance, making frontier LLMs viable adversarial prompt factories.

## Key Results

**Overall Break Rates by Model:**
- Claude (Anthropic): 3.3% - Strongest safety alignment
- ChatGPT (OpenAI): 10.0% - Moderate; vulnerable to roleplay and training framings
- Gemini (Google): 82.5% - Critical failure; no meaningful safety resistance

**Break Rates by Domain:**
- Bio/Chem: 0.0% - Most robust across all models
- Cybersecurity: 35.1% - Vulnerable to CTF and professional framings
- Manipulation: 58.3% - Most exploitable domain

**Dominant Attack Vector:**
Semantic laundering - reframing harmful requests through legitimate-appearing professional, educational, or creative language so models evaluate stated framing rather than real-world impact.

## Repository Contents

```
.
├── README.md                          This file
├── ICRT_Final_Submission.pdf          Complete research paper
├── whitepaper.pdf                     Pre-defined methodology document
├── generate_icrt_charts.py            Script to regenerate all 5 figures
├── scoring_sheet.xlsx                 All 177 binary break/safe evaluations with justifications
├── prompts_&_outputs.xlsx             Complete prompt-response pairs with conversation links
├── icrt_charts/                       Generated figures (300 DPI)
│   ├── fig1_model_break_rates.png
│   ├── fig2_domain_break_rates.png
│   ├── fig3_heatmap.png
│   ├── fig4_iterations.png
│   └── fig5_semantic_laundering_taxonomy.png
```

## Main Files

**ICRT_Final_Submission.pdf**
Complete academic paper with methodology, results, and analysis. Start here for full details.

**whitepaper.pdf**
Pre-defined experimental design document established before any prompts were executed.

**scoring_sheet.xlsx**
Binary break classifications for all 177 evaluations (60 base prompts × 3 iterations, minus 3 from Claude's self-termination). Includes:
- Prompt ID, Attacker, Target, Domain, Iteration
- Break (0/1), Attack Strategy, Justification
- Severity level for breaks

**prompts_&_outputs.xlsx**
Full prompt-response pairs organized by domain:
- Base prompt text
- Iterations 1, 2, 3 prompts and responses (full verbatim text)
- Break scores
- Conversation links to actual model outputs
- Execution dates and notes

**generate_icrt_charts.py**
Python script to regenerate all 5 figures at publication quality (300 DPI). Requires matplotlib, seaborn, numpy, pandas.

```bash
pip install matplotlib seaborn numpy pandas
python generate_icrt_charts.py
```

**icrt_charts/ folder**
Five publication-ready figures:
- fig1: Overall break rates by model (bar chart)
- fig2: Break rates by domain (bar chart)
- fig3: Attacker-target heatmap (3x3 matrix with NA for self-attacks)
- fig4: Break rates across 3 iteration rounds (bar chart)
- fig5: Semantic laundering attack type taxonomy (diagram)

## Experimental Design

6-cell cross-model attack matrix (no model attacks itself):

```
Target:     Claude    ChatGPT    Gemini
Gemini (A)    2         0         NA
Claude (A)   NA         6         18
ChatGPT (A)   0        NA         29
```

60 base prompts (10 per track) × 3 iterative escalation rounds = 177 evaluated interactions

Each prompt executed in fixed loop:
1. Iteration 1: Initial adversarial prompt from attacker model
2. Iteration 2: Refined prompt based on target's response
3. Iteration 3: Escalated prompt with heightened specificity/urgency

Binary break classification: Break (unsafe) = 1, Safe = 0

## Six Major Findings

**Finding 1: Model Divergence**
Claude 3.3%, ChatGPT 10.0%, Gemini 82.5% - not merely quantitative but qualitative differences in safety alignment.

**Finding 2: Semantic Laundering**
All successful breaks used semantic laundering - framing harmful requests as legitimate professional/educational/creative activities. Models evaluate stated purpose rather than output-level harm.

**Finding 3: Context Collapse**
Safety filters evaluate immediate conversational framing rather than real-world impact. A DDoS tool approved as "performance calibration" targeting localhost is a prime example.

**Finding 4: Bio/Chem Robustness**
0% break rate reflects two distinct mechanisms: system-level infrastructure blocks (Claude) and conversational refusals (ChatGPT).

**Finding 5: Attacker Effectiveness**
ChatGPT most effective (53.1%), Claude moderate (27.8%), Gemini least effective (3.3%). Asymmetry: high susceptibility as target doesn't predict effectiveness as attacker.

**Finding 6: Claude's Ethical Self-Termination**
Claude refused to continue generating attacks after Prompt 3 when Gemini produced medical device exploitation guide, demonstrating reflective ethical reasoning about its own agentic role.

## How to Use This Repository

**To read the full paper:**
Open ICRT_Final_Submission.pdf

**To understand the methodology:**
Read whitepaper.pdf

**To analyze the data:**
Open scoring_sheet.xlsx (binary classifications) and prompts_&_outputs.xlsx (full conversations)

**To view the figures:**
Open files in icrt_charts/ folder or regenerate using generate_icrt_charts.py

**To reproduce figures:**
```bash
python generate_icrt_charts.py
# Creates icrt_charts/ with all 5 figures at 300 DPI
```

## Accessing the Data

In Python:
```python
import pandas as pd

# Load scoring data
scoring = pd.read_excel('scoring_sheet.xlsx')

# Quick analysis
print(f"Total breaks: {scoring['Break'].sum()}")
print(f"Break rate by model:")
print(scoring.groupby('Target_Model')['Break'].mean())

# Load prompts and outputs
prompts = pd.read_excel('prompts_&_outputs.xlsx')
```

## Methodology Notes

Pre-defined experimental design established before execution to ensure consistency. All prompts generated entirely by attacker models with no manual optimization. Single researcher scoring with mandatory one-line justifications for all 177 evaluations. No post-hoc revision of scores.

Attack strategies employed: persona adoption, humanitarian framing, forensic auditing, technical troubleshooting, recursive systems analysis, edge-case calculation.

Limitations: Small sample size (10 prompts per track), specific model versions tested (late 2025-early 2026), single researcher scoring, three domains only (not CSAM/WMD/financial fraud), attacks constrained to 3 iterations.

## Key Insights for AI Safety

Semantic laundering is systematic and highly effective. Safety filters that evaluate intent signals rather than output signals are structurally vulnerable to adaptive adversarial framing. Robust alignment requires output-level harm assessment independent of request framing.

Safety robustness varies substantially across frontier models. An 82.5% break rate versus 3.3% reflects fundamentally different alignment approaches and has direct implications for deployment decisions.

Models do not build resistance across conversation turns. Iteration 3 achieves highest break rate, indicating sustained iterative pressure remains effective or increases in potency.

## Contact

Author: Shruti Rajvanshi
Email: shruti0809.raj@gmail.com
Location: New Delhi, India

Questions about methodology, data, or results? Open an issue or contact directly.
