# Lab 09 ? ABG pro-forma build

Source: the assignment and assumptions supplied in this chat. No current market data substituted.

## Results

- Equity value: $5,237.34 million.
- Value per share: $291.75.
- Share of value after 2030: 79.76%.
- Every supplied FY2026E / FY2030E checkpoint matches to one decimal.
- All five balance sheets balance and meet minimum cash.
- Four automated tests pass, including revolver funding and limit behavior.

## Deliberate break

Set FY2026E cash to 40.4 in a separate copy of the computed records. Valuation refuses:

```text
FY2026E: assets - liabilities - equity gap -61.4
```

The gap is the omitted increase in cash, with its sign flipped. The base model remains intact. This is an automated local test, not a claim that the partner exercise was performed.

## Reflection

The three central operating judgments are revenue growth (1.8%), gross margin (17.05%), and SG&A / gross profit (66.5%, 65.5%, then 64.5%). They drive sales, gross profit and operating efficiency respectively.

Cash is computed last because it is the cumulative result of operations, investment and financing, including buybacks and revolver movements. It is not an arbitrary balance-sheet plug.

Floor-plan loans fund inventory. In this lab they scale with inventory, incur interest on the opening balance, and changes enter FCFE through operating cash flow. Removing funding consumes more cash. The video's approximately -1.1 billion result is not independently reproduced here; removing only annual changes differs from removing opening financing too.

Terminal FCFE adds back the 2030 repayment before applying terminal growth. The high terminal share (79.76%) means most modeled value rests on cash flows beyond the explicit forecast.

## Files and commands

- Open Lab09-ABG.html to view the full report.
- Run `python proforma.py` for the three statements and valuation.
- Run `python -m unittest test_proforma.py` for verification.
- ABG-Proforma-Output.txt contains the saved model output.
- dcf.py restores the saved Week 3 CROX assumptions, producing $157.74/share; its cash-flow proxy and WACC remain provisional.

All files remain local. Nothing submitted to GitHub.
