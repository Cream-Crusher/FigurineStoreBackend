import pyotp


class PYOTP:

    @staticmethod
    async def generate_random_secrets():
        return pyotp.random_base32()

    @staticmethod
    async def create_one_time_password(secret: str, interval: int = 300) -> str:
        code_otp = pyotp.TOTP(secret, interval=interval).now()

        return code_otp

    @staticmethod
    async def verify_one_time_password(secret: str, code_otp: str, interval: int = 300) -> bool:
        totp = pyotp.TOTP(secret, interval=interval)
        return totp.verify(code_otp)


OTP = PYOTP()
