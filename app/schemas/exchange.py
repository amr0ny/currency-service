from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, field_validator


class ExchangeRequest(BaseModel):
    from_currency: Annotated[str, Field(min_length=3, max_length=3)]
    to_currency: Annotated[str, Field(min_length=3, max_length=3)]
    value: Annotated[float, Field(gt=0)]

    @field_validator('from_currency', 'to_currency')
    @classmethod
    def validate_currency_code(cls, v: str) -> str:
        if not v.isalpha() or not v.isupper():
            raise ValueError('Currency code must be 3 uppercase letters')
        return v

    @field_validator('value')
    @classmethod
    def validate_value(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('Value must be greater than 0')
        return v

class ExchangeResponse(BaseModel):
    from_currency: str
    to_currency: str
    exchange_rate: Decimal
    amount: Decimal
    converted_amount: Decimal