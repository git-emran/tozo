import pytest

from asyncpg.exceptions import UniqueViolationError
from quart_db import Connection


from backend.models.member import insert_member


async def test_insert_member(connection: Connection) -> None:
    await insert_member(connection, "clearlybestemran@gmail.com", "")
    with pytest.raises(UniqueViolationError):
        await insert_member(connection, "Clearlybestemran@gmail.com", "")
