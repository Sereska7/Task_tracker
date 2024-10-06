from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy.orm import Mapped, mapped_column


# Базовый класс для всех моделей базы данных, наследуется от SQLAlchemy DeclarativeBase.
class Base(DeclarativeBase):
    __abstract__ = True  # Указывает, что класс является абстрактным и не будет создана таблица для него.

    # Метод для динамического определения имени таблицы на основе имени класса.
    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Данный метод автоматически генерирует имя таблицы для класса модели.
        Имя таблицы будет соответствовать имени класса в нижнем регистре и с суффиксом 's'.

        Например, для класса `User` имя таблицы будет `users`.
        """
        return f"{cls.__name__.lower()}s"

    # Основное поле `id`, которое является первичным ключом во всех моделях, наследуемых от Base.
    id: Mapped[int] = mapped_column(primary_key=True)
