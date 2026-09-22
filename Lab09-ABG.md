**LAB 09 · ASBURY AUTOMOTIVE GROUP**

# Five years. Three statements. A checked answer.

2026–2030 forecast built from the supplied course assumptions. All amounts are USD millions except value per share. This is a saved model report, not live market data.

| Value per share | Equity value, millions | Value after 2030 |
| :---: | :---: | :---: |
| **$291.75** | **$5,237.34** | **79.76%** |

## Known-answer verification

| Line | FY2026E | FY2030E | Match |
| :--- | ---: | ---: | :---: |
| Revenue | 18,323.0 | 19,678.3 | PASS |
| Operating income | 844.2 | 971.4 | PASS |
| Net income | 413.6 | 527.5 | PASS |
| Free cash flow to equity | 211.4 | 342.3 | PASS |
| Cash, year end | 101.8 | 719.8 | PASS |
| Assets − liabilities − equity | 0.0 | 0.0 | PASS |

## The model refuses the broken balance sheet

In a separate in-memory test, FY2026E cash was replaced with the opening 40.4. Valuation stopped with this error:

```text
FY2026E: assets - liabilities - equity gap -61.4
```

The −61.4 gap means assets are understated by the omitted 61.4 increase in cash. The saved base model retains the correct 101.8 ending cash.

> Four automated tests passed: the supplied known answer; rejection of broken cash; revolver draw, repayment and opening-balance interest; and rejection when the revolver limit cannot fund minimum cash.

## The three judgments

**Revenue growth: 1.8%.** Sets the sales path and inventory requirements. **Gross margin: 17.05%.** Determines how much revenue remains to cover overhead. **SG&A / gross profit: 66.5%, 65.5%, then 64.5%.** Assumes improving operating efficiency. These are the supplied case judgments; defending them for another company requires company evidence.

## Why cash comes last

Profit, noncash expenses, investment, inventory financing, debt repayment and buybacks determine the cash movement. The revolver then funds any shortfall to the 25 minimum, subject to its 850 limit; excess cash first repays an outstanding revolver. Cash follows these flows rather than being forced to make the balance sheet balance.

## Floor-plan financing in this model

Floor plan is borrowing tied to vehicle inventory. The model holds loans / inventory at the exact historical ratio 2,027.0 / 2,135.8. Interest uses the opening loan balance, and an increase in floor-plan loans funds inventory within operating cash flow and FCFE under the lab convention. Omitting that funding makes the company appear to finance more inventory with cash. The video’s approximately −$1.1 billion cash result is not independently reproduced by this report; removing only forecast loan increases is a different change from removing the opening financing as well.

## Valuation

Discount the five annual FCFE at 10%. Terminal value adds back the 2030 debt repayment of 150, grows the result by 2.5%, and capitalizes it at 10% − 2.5%. Discount that terminal value five years and divide total equity value by 17.951349 million shares. Buybacks reduce cash and book equity but are not subtracted again from FCFE for this valuation.

## Full model output

**ABG | LAB 09 | FIVE-YEAR THREE-STATEMENT MODEL**

### Income statement

| USD millions | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Revenue | 18,323.0 | 18,652.8 | 18,988.5 | 19,330.3 | 19,678.3 |
| Cost of sales | 15,198.9 | 15,472.5 | 15,751.0 | 16,034.5 | 16,323.1 |
| Gross profit | 3,124.1 | 3,180.3 | 3,237.5 | 3,295.8 | 3,355.1 |
| SG&A | 2,077.5 | 2,083.1 | 2,088.2 | 2,125.8 | 2,164.1 |
| Depreciation | 82.4 | 86.9 | 91.3 | 95.5 | 99.7 |
| Impairment | 120.0 | 120.0 | 120.0 | 120.0 | 120.0 |
| Operating income | 844.2 | 890.3 | 938.1 | 954.5 | 971.4 |
| Interest | 289.0 | 282.5 | 276.1 | 269.7 | 263.4 |
| Pretax income | 555.2 | 607.8 | 661.9 | 684.8 | 708.0 |
| Tax | 141.6 | 155.0 | 168.8 | 174.6 | 180.5 |
| Net income | 413.6 | 452.8 | 493.1 | 510.1 | 527.5 |

### Balance sheet

| USD millions | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Cash | 101.8 | 206.9 | 356.6 | 527.5 | 719.8 |
| Inventory | 2,174.7 | 2,213.8 | 2,253.7 | 2,294.2 | 2,335.5 |
| PP&E | 3,238.0 | 3,401.1 | 3,559.8 | 3,714.3 | 3,864.6 |
| Other assets | 6,254.2 | 6,136.8 | 6,019.5 | 5,902.3 | 5,785.0 |
| Floor plan | 2,063.9 | 2,101.0 | 2,138.9 | 2,177.4 | 2,216.5 |
| Term debt | 3,422.0 | 3,272.0 | 3,122.0 | 2,972.0 | 2,822.0 |
| Revolver | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Other liabilities | 2,127.5 | 2,127.5 | 2,127.5 | 2,127.5 | 2,127.5 |
| Equity | 4,155.3 | 4,458.1 | 4,801.2 | 5,161.4 | 5,538.9 |

### Cash flow (deductions shown positive)

| USD millions | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Net income | 413.6 | 452.8 | 493.1 | 510.1 | 527.5 |
| Add depreciation | 82.4 | 86.9 | 91.3 | 95.5 | 99.7 |
| Add impairment | 120.0 | 120.0 | 120.0 | 120.0 | 120.0 |
| Less change in inventory | 38.9 | 39.1 | 39.8 | 40.6 | 41.3 |
| Less change in other WC | 2.6 | 2.6 | 2.7 | 2.7 | 2.8 |
| Add change in floor plan | 36.9 | 37.1 | 37.8 | 38.5 | 39.2 |
| Operating cash flow | 611.4 | 655.1 | 699.7 | 720.9 | 742.3 |
| Less capex | 250.0 | 250.0 | 250.0 | 250.0 | 250.0 |
| Less term debt repayment | 150.0 | 150.0 | 150.0 | 150.0 | 150.0 |
| FCFE | 211.4 | 255.1 | 299.7 | 320.9 | 342.3 |
| Less share buyback | 150.0 | 150.0 | 150.0 | 150.0 | 150.0 |
| Revolver draw / (repayment) | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Change in cash | 61.4 | 105.1 | 149.7 | 170.9 | 192.3 |
| Opening cash | 40.4 | 101.8 | 206.9 | 356.6 | 527.5 |
| Ending cash | 101.8 | 206.9 | 356.6 | 527.5 | 719.8 |

```text
CHECKS
FY2026E: assets - liabilities - equity = 0.0; cash >= 25.0: PASS
FY2027E: assets - liabilities - equity = 0.0; cash >= 25.0: PASS
FY2028E: assets - liabilities - equity = 0.0; cash >= 25.0: PASS
FY2029E: assets - liabilities - equity = 0.0; cash >= 25.0: PASS
FY2030E: assets - liabilities - equity = 0.0; cash >= 25.0: PASS
```

```text
Equity value (USD millions): 5,237.34
Share of value after 2030: 79.76%
Value per share: $291.75
```

## Local files

[Python engine](proforma.py) · [Verification tests](test_proforma.py) · [Plain-text output](ABG-Proforma-Output.txt) · [Checkout notes](Lab09-ABG.md)

Run: `python proforma.py`  
Verify: `python -m unittest test_proforma.py`

Week 3 prerequisite: dcf.py now reproduces the saved CROX inputs and $157.74/share result. Its CFO-less-capex proxy and WACC remain provisional.
