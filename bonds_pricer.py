import datetime
from dataclasses import dataclass, field
from typing import List

import QuantLib as ql
from dateutil.relativedelta import relativedelta


@dataclass
class BondSchedule:
    frequency: int
    maturity: datetime.date
    issue_date: datetime.date

    def CreateSchedule(self) -> List[datetime.date]:
        schedule = []
        coupon_payment = self.issue_date
        offset = int(12/self.frequency)
        while coupon_payment < self.maturity:
            coupon_payment = coupon_payment + relativedelta(months=offset)
            schedule.append(coupon_payment)

        return schedule



class FixedRateBondHelper:
    def __init__(self,
                 issue_date,
                 maturity_date,
                 face_value,
                 coupon_rate,
                 discount_rate=None,
                 evaluation_date=None,
                 calendar=None,
                 day_count=None,

                 ):
        self.calendar = calendar or ql.UnitedKingdom()

        self.settlement_days = 1

        self.face_value = face_value
        self.coupon_rate = coupon_rate
        self.issue_date = issue_date
        self.maturity_date = maturity_date
        self.day_count = day_count or ql.Actual365Fixed()
        self.discount_rate = discount_rate

        if evaluation_date:
            ql.Settings.instance().evaluationDate = evaluation_date

        self.schedule = ql.Schedule(
            self.issue_date,
            self.maturity_date,
            ql.Period(ql.Semiannual),
            self.calendar,
            ql.ModifiedFollowing,
            ql.ModifiedFollowing,
            ql.DateGeneration.Backward,
            False
        )

        self.bond = ql.FixedRateBond(
            self.settlement_days,
            self.face_value,
            self.schedule,
            [self.coupon_rate],
            self.day_count
        )

        if discount_rate is not None:
            flat_ts = ql.YieldTermStructureHandle(
                ql.FlatForward(ql.Settings.instance().evaluationDate, discount_rate, self.day_count)
            )
            self.bond_engine = ql.DiscountingBondEngine(flat_ts)
            self.bond.setPricingEngine(self.bond_engine)

    def get_schedule(self):
        return self.schedule

    def get_clean_price(self):
        return self.bond.cleanPrice()

    def get_accrued_amount(self):
        return self.bond.accruedAmount()

    def get_dirty_price(self):
        return self.bond.dirtyPrice()
