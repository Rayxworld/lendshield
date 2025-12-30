import sqlite3
import json

import sys
import os

if hasattr(sys, '_MEIPASS'):
    # Frozen: Persistence next to the executable
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Dev: Persistence in the backend directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_NAME = os.path.join(BASE_DIR, "loans.db")

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            credit_score INTEGER,
            annual_income REAL,
            loan_amount REAL,
            doc_id_match BOOLEAN,
            score REAL,
            risk_level TEXT,
            reasoning TEXT,
            is_fraud BOOLEAN,
            alerts TEXT,
            status TEXT DEFAULT 'Pending'
        )
    ''')
    
    # Simple migration for existing databases
    try:
        cursor.execute("ALTER TABLE loans ADD COLUMN status TEXT DEFAULT 'Pending'")
    except sqlite3.OperationalError:
        pass # Column likely already exists

    conn.commit()
    conn.close()

def get_all_loans():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # Order by ID descending to show newest first
    cursor.execute("SELECT * FROM loans ORDER BY id DESC")
    rows = cursor.fetchall()
    loans = []
    for row in rows:
        item = dict(row)
        # Convert boolean fields back from 0/1
        item['doc_id_match'] = bool(item['doc_id_match'])
        item['is_fraud'] = bool(item['is_fraud'])
        # Parse alerts JSON
        try:
            item['alerts'] = json.loads(item['alerts'])
        except:
            item['alerts'] = []
        # Ensure status exists for older records if any remain (schema default handles new ones)
        if 'status' not in item or not item['status']:
            item['status'] = 'Pending'
        loans.append(item)
    conn.close()
    return loans

def add_loan(loan_data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    alerts_json = json.dumps(loan_data.get('alerts', []))
    status = loan_data.get('status', 'Pending')
    
    cursor.execute('''
        INSERT INTO loans (name, credit_score, annual_income, loan_amount, doc_id_match, score, risk_level, reasoning, is_fraud, alerts, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        loan_data['name'],
        loan_data['credit_score'],
        loan_data['annual_income'],
        loan_data['loan_amount'],
        loan_data['doc_id_match'],
        loan_data['score'],
        loan_data['risk_level'],
        loan_data['reasoning'],
        loan_data['is_fraud'],
        alerts_json,
        status
    ))
    
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def update_loan_status(loan_id, status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE loans SET status = ? WHERE id = ?", (status, loan_id))
    conn.commit()
    conn.close()
    return True

def clear_all_loans():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM loans")
    conn.commit()
    conn.close()
