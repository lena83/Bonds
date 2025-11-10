from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any


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





