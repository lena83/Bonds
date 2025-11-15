from __future__ import annotations

from pathlib import Path
from typing import Optional, Dict, Any, List
import pandera as pa
from pandera import Column, Check
import logging
import pandas as pd

from data import BOND_DTYPES, BOND_PARSE_DATES, Bond

BondsSchema = pa.DataFrameSchema(
    {
        "Isin":      Column(pa.String, nullable=False),
        "Nominal":   Column(pa.Float64, Check.gt(0), nullable=False),
        "Coupon":    Column(pa.Float64, Check.ge(0), nullable=False),
        "Frequency": Column(pa.Int64, Check.isin({1, 2, 4, 12}), nullable=False),  # annual, semi, quarterly, monthly
        "IssueDate": Column(pa.Date, nullable=False),
        "Maturity":  Column(pa.Date, nullable=False),
        "YTD":       Column(pa.Float64, nullable=False),
    },

    checks=[
        Check(lambda df: (df["Maturity"] > df["IssueDate"]).all(), error="Maturity must be after IssueDate"),
    ],
    coerce=True,   # try to coerce types to the ones above
    strict=True    # fail if extra/unexpected columns appear
)



class CSVLoader:
    def __init__(
        self,
        path: str | Path,
        dtypes: Optional[Dict[str, Any]] = None,
        parse_dates: Optional[list[str]] = None,


    ):
        self.path = Path(path)
        self.dtypes = dtypes
        self.parse_dates = parse_dates
        self._df: Optional[pd.DataFrame] = None

    def load(self) -> pd.DataFrame:
        if not self.path.exists():
            raise FileNotFoundError(f"CSV not found: {self.path}")

        if self._df is None:
            self._df = pd.read_csv(
                self.path,
                dtype=self.dtypes,
                parse_dates=self.parse_dates
            )
        return self._df

def load_bonds_df(path: str) -> pd.DataFrame:
    loader = CSVLoader(path, dtypes=BOND_DTYPES, parse_dates=BOND_PARSE_DATES)
    df = loader.load()
    df.dropna(inplace=True)

    try:
        df = BondsSchema.validate(df, lazy=True)
    except pa.errors.SchemaErrors as err:
        # Inspect what failed
        print("Validation errors:\n", err.failure_cases.head(20))
        raise

    return df

def load_bonds(path: str) -> List[Bond]:
    df = load_bonds_df(path)
    records = df.to_dict(orient="records")
    bonds = []

    for i, rec in enumerate(records):
        try:
            bond = Bond.from_row(rec)
            bonds.append(bond)
        except Exception as e:
            logging.exception("Failed to convert row %d: %s", i, rec)

    return bonds
