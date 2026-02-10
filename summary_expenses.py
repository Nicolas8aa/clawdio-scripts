#!/usr/bin/env python3
"""Generate a simple expenses summary from memory/expenses.csv.

Behavior:
- Read workspace/memory/expenses.csv with columns: category,amount_cop,date,notes
- Print a markdown table and total to stdout
"""
import csv
from pathlib import Path

workspace = Path('/home/nicolas-asus-ld/.openclaw/workspace')
mem_expenses = workspace / 'memory' / 'expenses.csv'

summary = {}

total = 0.0
if mem_expenses.exists():
    with mem_expenses.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                cat = row.get('category','').strip() or 'Other'
                amt = float(row.get('amount_cop',0) or 0)
            except:
                continue
            summary[cat] = summary.get(cat, 0) + amt
            total += amt
else:
    print('No expenses CSV found at', mem_expenses)

# print markdown table
print('Category | Amount (COP)')
print('-------- | -------------')
for cat,amt in summary.items():
    print(f'{cat} | {amt:,.2f}')
print('\nTotal | {0:,.2f}'.format(total))
