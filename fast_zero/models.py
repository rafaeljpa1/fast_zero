from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

'''
Por padrão todos os atributos devem ser especificados. Alguns serão preenchidos
automático pelo banco de dados. Algumas colunas apresentam propriedades específicas;
Para esses casos o SQLAlchemy possui uma função mapped_column no qual definimos
as propriedades.
'''

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )