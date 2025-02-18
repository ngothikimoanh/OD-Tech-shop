from enum import StrEnum

PHONE_NUMBER_REGEX = r"^0\d{9}$"
DEFAULT_FULL_NAME = "Khách hàng"


class Role(StrEnum):
    ADMIN = "admin"
    GUEST = "guest"
    EMPLOYEE = "employee"


ROLE_DISPLAY: dict[str, str] = {
    Role.ADMIN: "Quản trị viên",
    Role.GUEST: "Khách hàng",
}
