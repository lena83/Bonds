from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Dict, Any
import bisect


BOND_DTYPES: Dict[str, Any] = {
    "Isin": "string",
    "Nominal": "float64",
    "Coupon": "float64",
    "Frequency": "int64",
    "YTD": "float64",
}
BOND_PARSE_DATES = ["IssueDate", "Maturity"]

@dataclass
class Bond:
    isin: str
    nominal: int
    frequency: int
    coupon: float
    maturity: datetime
    issue_date: datetime
    ytd: float

    @classmethod
    def from_row(cls, row: dict) -> Bond:   # no quotes needed
        def to_date(v):
            if hasattr(v, "date"):  # pd.Timestamp or datetime
                return v.date()
            return datetime.fromisoformat(str(v)).date()

        return cls(
            isin=str(row["Isin"]),
            nominal=int(row["Nominal"]),
            coupon=float(row["Coupon"]),
            frequency=int(row["Frequency"]),
            issue_date=to_date(row["IssueDate"]),
            maturity=to_date(row["Maturity"]),
            ytd=float(row["YTD"]),
        )

    def accrued_interest(self, payments_schedule: List[datetime], settlement_date: date) -> float:
        days_since_last_index = bisect.bisect_left(payments_schedule, settlement_date) - 1
        days_since_last_payment = (settlement_date -  payments_schedule[days_since_last_index]).days
        coupon_per_period = self.nominal*self.coupon/self.frequency
        days_in_period = 365 / self.frequency
        accrued_interest = coupon_per_period * days_since_last_payment / days_in_period
        return accrued_interest

    def dirty_price(self, payments_schedule: List[datetime], settlement_date: date) -> float:
        """

        :type settlement_date: date
        """
        dates_after_settlement = bisect.bisect_left(payments_schedule, settlement_date)
        future_payments = payments_schedule[dates_after_settlement:]
        coupon_cash_per_period = self.nominal * self.coupon / self.frequency
        price =0.0
        for payment in future_payments:
            time_to_next_payment = (payment - settlement_date).days/ 365
            discount_factor = (1 + self.ytd/self.frequency)** (-self.frequency*time_to_next_payment)
            if payment == self.maturity:
                coupon_cash_per_period = self.nominal + coupon_cash_per_period
            p_i = coupon_cash_per_period * discount_factor
            price += p_i

        return price

    def clean_price(self, dirty: float,accrued: float) -> float:
        return dirty - accrued




