from dataclasses import dataclass
from datetime import datetime
from quart_db import Connection


from pydantic import constr


@dataclass
class Todo:
    complete: bool
    due: datetime | None
    id: int
    task: constr(strip_whitespace=True, min_length=1)  # type: ignore


async def select_todos(
    connection: Connection, member_id: int, complete: bool | None = None
) -> list[Todo]:
    if complete is None:
        query = (
            """SELECT id, complete, due, task FROM todos WHERE member_id = :member_id"""
        )
        values = {"member_id": member_id}

    else:
        query = """SELECT id, complete, due, task FROM todos AND complete = :complete"""
        values = {"member_id": member_id, "complete": complete}

    return [Todo(**row) async for row in connection.iterate(query, values)]
