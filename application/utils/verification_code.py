import asyncio

from typing import Dict

# Хранилище для временных кодов подтверждения
verification_codes: Dict[str, int] = {}


async def remove_code_after_delay(email: str, delay: int = 300):
    """
    Асинхронная функция для удаления кода подтверждения по истечению времени.

    Аргументы:
    email (str): Адрес электронной почты пользователя, для которого был отправлен код подтверждения.
    delay (int): Время задержки в секундах перед удалением кода. По умолчанию 300 секунд (5 минут).

    Действия:
    - Ждет указанное количество времени.
    - По истечению времени удаляет код подтверждения из хранилища verification_codes.
    - Выводит сообщение в консоль о том, что код был удален.
    """
    # Ожидание указанного времени (в секундах)
    await asyncio.sleep(delay)

    # Удаление кода из хранилища после истечения времени
    if email in verification_codes:
        del verification_codes[email]
        print(f"Verification code for {email} has expired and been removed.")
