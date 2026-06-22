from typing import AsyncGenerator
from quart_db import Connection


import pytest
from quart import Quart

from backend.run import app, quart_db


@pytest.fixture(name="app", scope="function")
async def _app() -> AsyncGenerator[Quart, None]:
    async with app.test_app():
        yield app


@pytest.fixture(name="connection", scope="function")
async def _connection(app: Quart) -> AsyncGenerator[Connection, None]:
    async with quart_db.connection() as connection:
        async with connection.transaction():
            yield connection
