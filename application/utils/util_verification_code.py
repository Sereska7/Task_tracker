import asyncio

from typing import Dict

# Хранилище для временных кодов подтверждения
verification_codes: Dict[str, int] = {}


async def remove_code_after_delay(email: str, delay: int = 300):
    # Ожидание указанного времени (в секундах)
    await asyncio.sleep(delay)
    # Удаление кода из хранилища после истечения времени
    if email in verification_codes:
        del verification_codes[email]
        print(f"Verification code for {email} has expired and been removed.")
