# LendShield 🛡️
AI-Powered Loan Risk & Fraud Analyzer

LendShield is a desktop-based AI underwriting tool that helps financial institutions
assess loan risk, detect fraud, and simulate portfolio impact using explainable
machine learning.

## Problem
Loan underwriting is slow, opaque, and vulnerable to fraud.
Banks need faster, more transparent risk assessment tools.

## Solution
LendShield is a **hybrid AI platform** that runs as a **secure Web Dashboard** or an **offline-first Desktop Application**. It combines machine learning, fraud heuristics, and interactive dashboards to modernize underwriting.

## Key Features
- **AI Risk Engine**: Instant credit scoring and default prediction.
- **Fraud Guard**: Automatic detection of anomalies and ID mismatches.
- **Web & Desktop**: Deploys as a cloud web app or a secure local executable.
- **Explainable Decisions**: Plain-English reasons for every AI approval/rejection.

## Architecture
React (Web/Desktop UI) ↔ FastAPI (AI Engine) ↔ SQLite + Scikit-Learn

## Tech Stack
Frontend: React, Electron, Recharts  
Backend: Python, FastAPI, Scikit-learn, Pandas  
Storage: SQLite, CSV

## Getting Started
See `/backend/README.md` and `/frontend/README.md`

## Demo
📹 Demo video link (to be added)

## Hackathon
Built for **LMA EDGE Hackathon 2026**