import pytest

from asyncpg.exceptions import UniqueViolationError
from quart_db import Connection


from backend.models.member import insert_member, select_member_by_email


async def test_insert_member(connection: Connection) -> None:
    await insert_member(connection, "clearlybestemran@gmail.com", "")
    with pytest.raises(UniqueViolationError):
        await insert_member(connection, "Clearlybestemran@gmail.com", "")


async def test_select_memeber_by_email(connection: Connection) -> None:
    await insert_member(connection, "clearlybestemran@gmail.com", "")
    member = await select_member_by_email(connection, "Clearlybestemran@gmail.com")
    assert member is not None
