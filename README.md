# LendShield 🛡️
AI-Powered Loan Risk & Fraud Analyzer

LendShield is a desktop-based AI underwriting tool that helps financial institutions
assess loan risk, detect fraud, and simulate portfolio impact using explainable
machine learning.

## Problem
Loan underwriting is slow, opaque, and vulnerable to fraud.
Banks need faster, more transparent risk assessment tools.

## Solution
LendShield combines machine learning, fraud heuristics, and interactive dashboards
into a secure, offline-first desktop application.

## Key Features
- AI-powered loan risk scoring
- Fraud detection and alerting
- Portfolio risk simulation
- Explainable decision insights
- Desktop-first workflow (Electron)

## Architecture
Electron (React UI)
→ FastAPI (Local AI Engine)
→ ML Models + CSV Data + SQLite

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