#!/usr/bin/env python3
"""Generate a simple expenses summary from memory files.

Behavior:
- If memory/expenses.csv exists, read it as CSV with columns: category,amount
- Otherwise, scan MEMORY.md for lines like '- Merchant: amount COP' and sum
- Print a markdown table and total to stdout
"""
import csv
from pathlib import Path

workspace = Path('/home/nicolas-asus-ld/.openclaw/workspace')
mem_expenses = workspace / 'memory' / 'expenses.csv'
mem_file = workspace / 'MEMORY.md'

summary = {}

if mem_expenses.exists():
    with mem_expenses.open() as f:
        reader = csv.reader(f)
        for row in reader:
            if not row: 
                continue
            cat = row[0].strip()
            try:
                amt = float(row[1])
            except:
                continue
            summary[cat] = summary.get(cat, 0) + amt
else:
    if mem_file.exists():
        for line in mem_file.read_text().splitlines():
            line = line.strip()
            # matches lines like '- La Granja: 58000 COP' or '- La Granja: 58,000 COP'
            if ':' in line and 'COP' in line:
                try:
                    left,right = line.split(':',1)
                    amt_text = right.split('COP')[0]
                    amt = float(amt_text.replace(',','').strip())
                    cat = 'Food'
                    summary[cat] = summary.get(cat,0)+amt
                except:
                    pass

# print markdown table
print('Category | Amount (COP)')
print('-------- | -------------')
total = 0
for cat,amt in summary.items():
    print(f'{cat} | {amt:,.2f}')
    total += amt
print('\nTotal | {0:,.2f}'.format(total))
