import phonenumbers

from fastapi import HTTPException


async def check_phone(number: str) -> phonenumbers:
    try:
        number = phonenumbers.parse(number)
    except Exception:
        raise HTTPException(400, 'phone not valid')

    if phonenumbers.is_valid_number(number):
        return phonenumbers.format_number(numobj=number, num_format=1)
    else:
        raise HTTPException(400, 'phone not valid')
