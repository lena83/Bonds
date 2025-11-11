from __future__ import annotations

import datetime

from bonds_pricer import FixedRateBondHelper
from data_loader import load_bonds
import QuantLib as ql


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def to_ql_date(py_date):
    return ql.Date(py_date.day, py_date.month, py_date.year)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    bonds = load_bonds("bonds.csv")
    eval_date = datetime.date.today()
    for bond_data in bonds:
        helper = FixedRateBondHelper(
            issue_date=to_ql_date(bond_data.issue_date),
            maturity_date=to_ql_date(bond_data.maturity),
            face_value=bond_data.nominal,
            coupon_rate=bond_data.coupon,
            discount_rate=bond_data.ytd,
            evaluation_date=ql.Date(eval_date.day, eval_date.month, eval_date.year)
        )
        print(f"  Clean Price: {helper.get_clean_price():.2f}")
        print(f"  Clean Price: {helper.get_accrued_amount():.2f}")
        print(f"  Dirty Price: {helper.get_dirty_price():.2f}")




