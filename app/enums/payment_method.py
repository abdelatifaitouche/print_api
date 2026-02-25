from enum import StrEnum


class PaymentMethod(StrEnum):
    CCP = "CCP"
    CASH = "CASH"
    CHEQUE = "CHEQUE"
