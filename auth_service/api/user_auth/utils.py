import phonenumbers

from fastapi import HTTPException


def check_phone(number: str) -> phonenumbers:
    try:
        phone_number = phonenumbers.parse(number, 'RU')

        if not phonenumbers.is_valid_number(phone_number):
            phone_number = phonenumbers.parse(number)

        return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)
    except:
        raise HTTPException(400, 'phone not valid')
