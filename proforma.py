"""Lab 09: ABG three-statement model. USD millions, except per-share value.

Standard library only. Run: python proforma.py
Assumptions and known answers are supplied by the Lab 09 instruction.
"""

YEARS = range(2026, 2031)
OPENING = dict(revenue=17999.0, inventory=2135.8, ppe=3070.4,
               other_assets=6371.6, cash=40.4, floor_plan=2027.0,
               debt=3572.0, other_liabilities=2127.5, equity=3891.7,
               revolver=0.0)
ASSUMPTIONS = dict(
    growth=0.018, gross_margin=0.1705,
    sga_ratios=(0.665, 0.655, 0.645, 0.645, 0.645),
    depreciation_ratio=82.4 / 3070.4, impairment=120.0, capex=250.0,
    tax_rate=0.255, inventory_days=2135.8 / (17999.0 - 3071.7) * 365,
    floor_plan_ratio=2027.0 / 2135.8, other_wc_ratio=0.008,
    minimum_cash=25.0, revolver_limit=850.0, revolver_rate=0.06,
    repayment=150.0, buyback=150.0, floor_plan_rate=0.0467,
    debt_rate=0.0544, cost_of_equity=0.10, terminal_growth=0.025,
    shares=17.951349,
)


def project(opening=None, assumptions=None):
    """Return five annual records; retain full precision until printing."""
    prior = dict(OPENING if opening is None else opening)
    a = ASSUMPTIONS if assumptions is None else assumptions
    records = []
    for year, sga_ratio in zip(YEARS, a['sga_ratios'], strict=True):
        r = dict(year=year)
        r['revenue'] = prior['revenue'] * (1 + a['growth'])
        r['gross_profit'] = r['revenue'] * a['gross_margin']
        r['cost_of_sales'] = r['revenue'] - r['gross_profit']
        r['sga'] = r['gross_profit'] * sga_ratio
        r['depreciation'] = prior['ppe'] * a['depreciation_ratio']
        r['impairment'] = a['impairment']
        r['operating_income'] = (r['gross_profit'] - r['sga']
                                 - r['depreciation'] - r['impairment'])
        r['interest'] = (prior['floor_plan'] * a['floor_plan_rate']
                         + prior['debt'] * a['debt_rate']
                         + prior['revolver'] * a['revolver_rate'])
        r['pretax_income'] = r['operating_income'] - r['interest']
        r['tax'] = max(0.0, r['pretax_income']) * a['tax_rate']
        r['net_income'] = r['pretax_income'] - r['tax']
        r['inventory'] = r['cost_of_sales'] * a['inventory_days'] / 365
        r['floor_plan'] = r['inventory'] * a['floor_plan_ratio']
        r['capex'] = a['capex']
        r['ppe'] = prior['ppe'] + r['capex'] - r['depreciation']
        r['change_other_wc'] = a['other_wc_ratio'] * (r['revenue'] - prior['revenue'])
        r['other_assets'] = prior['other_assets'] + r['change_other_wc'] - r['impairment']
        r['repayment'] = a['repayment']
        r['debt'] = prior['debt'] - r['repayment']
        r['other_liabilities'] = prior['other_liabilities']
        r['buyback'] = a['buyback']
        r['equity'] = prior['equity'] + r['net_income'] - r['buyback']
        r['change_inventory'] = r['inventory'] - prior['inventory']
        r['change_floor_plan'] = r['floor_plan'] - prior['floor_plan']
        r['operating_cash_flow'] = (r['net_income'] + r['depreciation']
                                    + r['impairment'] - r['change_inventory']
                                    - r['change_other_wc'] + r['change_floor_plan'])
        r['fcfe'] = r['operating_cash_flow'] - r['capex'] - r['repayment']
        r['opening_cash'] = prior['cash']
        cash_before_revolver = prior['cash'] + r['fcfe'] - r['buyback']
        if cash_before_revolver < a['minimum_cash']:
            r['revolver_change'] = min(a['minimum_cash'] - cash_before_revolver,
                                       max(0.0, a['revolver_limit'] - prior['revolver']))
        else:
            r['revolver_change'] = -min(prior['revolver'],
                                        cash_before_revolver - a['minimum_cash'])
        r['revolver_change'] = r['revolver_change'] or 0.0
        r['revolver'] = prior['revolver'] + r['revolver_change']
        r['cash'] = cash_before_revolver + r['revolver_change']
        r['change_cash'] = r['cash'] - prior['cash']
        records.append(r)
        prior = r
    return records


def balance_gap(r):
    # Recompute from the actual statement lines so a changed cash cell is caught.
    return (r['cash'] + r['inventory'] + r['ppe'] + r['other_assets']
            - r['floor_plan'] - r['debt'] - r['revolver']
            - r['other_liabilities'] - r['equity'])


def assert_balanced(records, assumptions=None):
    a = ASSUMPTIONS if assumptions is None else assumptions
    for r in records:
        year = f"FY{r['year']}E"
        gap = balance_gap(r)
        if abs(gap) > 1e-6:
            raise AssertionError(f'{year}: assets - liabilities - equity gap {gap:.1f}')
        cash_gap = r['cash'] - a['minimum_cash']
        if cash_gap < -1e-6:
            raise AssertionError(f'{year}: cash below minimum; gap {cash_gap:.1f}')
        if not -1e-6 <= r['revolver'] <= a['revolver_limit'] + 1e-6:
            raise AssertionError(f'{year}: revolver outside 0 to {a["revolver_limit"]:.1f}')


def value_equity(records, assumptions=None):
    a = ASSUMPTIONS if assumptions is None else assumptions
    assert_balanced(records, a)
    rate, growth = a['cost_of_equity'], a['terminal_growth']
    if not -1 < growth < rate or a['shares'] <= 0:
        raise ValueError('Require -100% < terminal growth < cost of equity and positive shares.')
    explicit = sum(r['fcfe'] / (1 + rate) ** t for t, r in enumerate(records, 1))
    last = records[-1]
    terminal = (last['fcfe'] + last['repayment']) * (1 + growth) / (rate - growth)
    pv_terminal = terminal / (1 + rate) ** len(records)
    equity = explicit + pv_terminal
    return equity, pv_terminal / equity, equity / a['shares']


def print_table(title, records, rows):
    print('\n' + title)
    print(f'{"USD millions":<36}' + ''.join(f'{"FY" + str(r["year"]) + "E":>13}' for r in records))
    for label, key in rows:
        print(f'{label:<36}' + ''.join(f'{r[key]:>13,.1f}' for r in records))


def main():
    records = project()
    print('ABG | LAB 09 | FIVE-YEAR THREE-STATEMENT MODEL')
    print_table('INCOME STATEMENT', records, [
        ('Revenue', 'revenue'), ('Cost of sales', 'cost_of_sales'),
        ('Gross profit', 'gross_profit'), ('SG&A', 'sga'),
        ('Depreciation', 'depreciation'), ('Impairment', 'impairment'),
        ('Operating income', 'operating_income'), ('Interest', 'interest'),
        ('Pretax income', 'pretax_income'), ('Tax', 'tax'), ('Net income', 'net_income')])
    print_table('BALANCE SHEET', records, [
        ('Cash', 'cash'), ('Inventory', 'inventory'), ('PP&E', 'ppe'),
        ('Other assets', 'other_assets'), ('Floor plan', 'floor_plan'),
        ('Term debt', 'debt'), ('Revolver', 'revolver'),
        ('Other liabilities', 'other_liabilities'), ('Equity', 'equity')])
    print_table('CASH FLOW (deductions shown positive)', records, [
        ('Net income', 'net_income'), ('Add depreciation', 'depreciation'),
        ('Add impairment', 'impairment'), ('Less change in inventory', 'change_inventory'),
        ('Less change in other WC', 'change_other_wc'),
        ('Add change in floor plan', 'change_floor_plan'),
        ('Operating cash flow', 'operating_cash_flow'), ('Less capex', 'capex'),
        ('Less term debt repayment', 'repayment'), ('FCFE', 'fcfe'),
        ('Less share buyback', 'buyback'), ('Revolver draw / (repayment)', 'revolver_change'),
        ('Change in cash', 'change_cash'), ('Opening cash', 'opening_cash'), ('Ending cash', 'cash')])
    print('\nCHECKS')
    for r in records:
        gap = balance_gap(r)
        shown_gap = 0.0 if abs(gap) < 1e-6 else gap
        print(f"FY{r['year']}E: assets - liabilities - equity = {shown_gap:.1f}; "
              f"cash >= {ASSUMPTIONS['minimum_cash']:.1f}: "
              f"{'PASS' if r['cash'] >= ASSUMPTIONS['minimum_cash'] - 1e-6 else 'FAIL'}")
    assert_balanced(records)
    equity, terminal_share, price = value_equity(records)
    print(f'\nEquity value (USD millions): {equity:,.2f}')
    print(f'Share of value after 2030: {terminal_share:.2%}')
    print(f'Value per share: ${price:.2f}')


if __name__ == '__main__':
    main()
