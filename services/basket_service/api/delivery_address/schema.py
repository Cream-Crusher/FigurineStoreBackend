from typing import List, Optional

from pydantic import BaseModel


class DeliveryAddressBase(BaseModel):
    address_line: Optional[str] = None
    country: Optional[str] = None
    zip_code: Optional[str] = None


class DeliveryAddressRead(DeliveryAddressBase):
    pass


class DeliveryAddressCreate(DeliveryAddressBase):
    user_id: str


class DeliveryAddressUpdate(DeliveryAddressBase):
    user_id: str
