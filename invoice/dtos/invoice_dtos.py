from typing import List

from pydantic import BaseModel, validator
from datetime import datetime, date

from invoice.dtos import InvoiceItemCreateDTO


class InvoiceCreateDTO(BaseModel):
    bill_from: str
    bill_to: str
    date: date
    amount: float = None
    is_paid: bool
    paid_on: date = None
    items: List[InvoiceItemCreateDTO]

    @validator("date", pre=True)
    def parse_date(cls, value):
        return datetime.strptime(value, "%d-%m-%Y").date()

    @validator("paid_on", pre=True)
    def parse_paid_on(cls, value):
        return datetime.strptime(value, "%d-%m-%Y").date()

