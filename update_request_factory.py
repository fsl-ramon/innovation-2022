from update_notification_request import WePayClearNotificationUpdateRequest


class WePayClearConnectionUpdateRequestFactory:
    @staticmethod
    def from_legal_entity_dict(data: dict) -> WePayClearNotificationUpdateRequest:
        return WePayClearNotificationUpdateRequest(
            email_is_verified=data["controller"]["email_is_verified"] if "controller" in data else None,
        )

    @staticmethod
    def from_legal_entity_verification_dict(data: dict) -> WePayClearNotificationUpdateRequest:
        return WePayClearNotificationUpdateRequest(
            legal_entity_verified=data["entity_verification"]["verified"] if "entity_verification" in data else None,
            controller_verified=data["controller"]["personal_verification"]["verified"]
            if "controller" in data
            else None,
        )

    @staticmethod
    def from_accounts_capabilities_entity_dict(data: dict) -> WePayClearNotificationUpdateRequest:
        return WePayClearNotificationUpdateRequest(
            payments_enabled=data["payments"]["enabled"] if "payments" in data else None,
            payouts_enabled=data["payouts"]["enabled"] if "payouts" in data else None,
        )
