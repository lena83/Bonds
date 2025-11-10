from __future__ import annotations

from pathlib import Path
from typing import Optional, Dict, Any, List

import pandas as pd

from data import BOND_DTYPES, BOND_PARSE_DATES, Bond


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
    return loader.load()

def load_bonds(path: str) -> List[Bond]:
    df = load_bonds_df(path)
    return [Bond.from_row(rec) for rec in df.to_dict(orient="records")]