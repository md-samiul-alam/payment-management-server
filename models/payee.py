from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class PayeeInfo(BaseModel):
    id: Optional[str] = None
    payee_first_name: str
    payee_last_name: str
    payee_added_date_utc: datetime = Field(default_factory=datetime.utcnow)
    payee_address_line_1: str
    payee_address_line_2: Optional[str] = None
    payee_city: str
    payee_country: str
    payee_province_or_state: Optional[str] = None
    payee_postal_code: str
    payee_phone_number: str
    payee_email: EmailStr 