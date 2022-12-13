from typing import Optional

from pydantic import BaseModel


class WePayClearNotificationUpdateRequest(BaseModel):
    payments_enabled: Optional[bool] = None
    email_is_verified: Optional[bool] = None
    legal_entity_verified: Optional[bool] = None
    controller_verified: Optional[bool] = None
    payouts_enabled: Optional[bool] = None
