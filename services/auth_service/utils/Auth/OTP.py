import time
import base64
import pyotp


class PYOTP:

    @staticmethod
    async def create_one_time_password(secret: str) -> str:
        code_otp = pyotp.TOTP(secret).now()

        return code_otp

    @staticmethod
    async def verify_one_time_password(secret: str, code_otp: str) -> bool:
        totp = pyotp.TOTP(secret)
        return totp.verify(code_otp)


OTP = PYOTP()
