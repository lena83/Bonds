from __future__ import annotations

import datetime

from bonds_pricer import FixedRateBondHelper, BondSchedule
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
    eval_date = datetime.date(2025, 2, 20)
    for bond_data in bonds:
        schedule = BondSchedule(frequency=bond_data.frequency,
                                issue_date=bond_data.issue_date,
                                maturity=bond_data.maturity)
        payments_schedule = schedule.CreateSchedule()
        accrued_interest = bond_data.accrued_interest(payments_schedule, eval_date)
        dirty_price = bond_data.dirty_price(payments_schedule, eval_date)
        clean_price = dirty_price -accrued_interest
        helper = FixedRateBondHelper(
            issue_date=to_ql_date(bond_data.issue_date),
            maturity_date=to_ql_date(bond_data.maturity),
            face_value=bond_data.nominal,
            coupon_rate=bond_data.coupon,
            discount_rate=bond_data.ytd,
            evaluation_date=ql.Date(eval_date.day, eval_date.month, eval_date.year)
        )
        print(f"  Clean Price from Quantlib: {helper.get_clean_price():.2f}")
        print(f"  Clean Price: {clean_price:.2f}")
        print(f"  Accrued Amount from Quantlib: {helper.get_accrued_amount():.2f}")
        print(f"  Accrued Amount : {accrued_interest:.2f}")
        print(f"  Dirty Price from Quantlib: {helper.get_dirty_price():.2f}")
        print(f"  Dirty Price : {dirty_price:.2f}")




