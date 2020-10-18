from dataclasses import dataclass


@dataclass
class ExceptionReportsCriteria:
    trade_id: int
    ccy: str
    amount: int
    msg_type: int


@dataclass
class MismatchCriteria:
    msg_type: int
    ssa_ref: str
    mx_amt: int


@dataclass
class UnclassifiedExceptionCriteria:
    trade_id: int
    pay_receive: str
    amount: int
