import os
from subprocess import call  # nosec
from urllib.parse import urlparse
from quart import Quart, ResponseReturnValue
from quart_auth import QuartAuth
from quart_rate_limiter import RateLimitExceeded, RateLimiter, rate_exempt, rate_limit
from quart_schema import QuartSchema, RequestSchemaValidationError
from pydantic import ValidationError
from quart_db import QuartDB


from backend.lib.api_error import APIError
from datetime import timedelta

app = Quart(__name__)

app.config["QUART_DB_DATABASE_URL"] = os.environ.get("TOZO_QUART_DB_DATABASE_URL")
quart_db = QuartDB(app)

schema = QuartSchema(app, convert_casing=True)

auth_manager = QuartAuth(app)
rate_limiter = RateLimiter(app)


@app.cli.command("recreate_db")
def recreate_db() -> None:
    db_url = urlparse(os.environ["TOZO_QUART_DB_DATABASE_URL"])

    call(
        [
            "psql",
            "-U",
            "postgres",
            "-c",
            f"DROP DATABASE IF EXISTS {db_url.path.removeprefix('/')}",
        ]
    )

    call(
        [
            "psql",
            "-U",
            "postgres",
            "-c",
            f"DROP USER IF EXISTS {db_url.username}",
        ]
    )

    call(
        [
            "psql",
            "-U",
            "postgres",
            "-c",
            f"CREATE USER {db_url.username} LOGIN PASSWORD '{db_url.password}' CREATEDB",
        ]
    )

    call(
        [
            "psql",
            "-U",
            "postgres",
            "-c",
            f"CREATE DATABASE {db_url.path.removeprefix('/')}",
        ]
    )


@app.errorhandler(RequestSchemaValidationError)  # type: ignore
async def handle_request_validation_error(
    error: RequestSchemaValidationError,
) -> ResponseReturnValue:
    if isinstance(error.validation_error, TypeError):
        return {"errors": str(error.validation_error)}, 400
    elif isinstance(error.validation_error, ValidationError):
        return {"errors": error.validation_error.json()}, 400
    else:
        return {"errors": str(error.validation_error)}, 400


@app.errorhandler(APIError)  # type: ignore
async def handle_api_error(error: APIError) -> ResponseReturnValue:
    return {"code": error.code}, error.status_code


@app.errorhandler(RateLimitExceeded)  # type: ignore
async def handle_rate_limit_exceeded_error(
    error: RateLimitExceeded,
) -> ResponseReturnValue:
    return {}, 429, error.get_headers()


@app.errorhandler(500)
async def handle_generic_error(error: Exception) -> ResponseReturnValue:
    return {"code": "INTERNAL_SERVER_ERROR"}, 500


@app.get("/")
@rate_limit(6, timedelta(minutes=1))
async def hello_handler():
    return {"message": "hello"}


@app.get("/control/ping/")
@rate_exempt
async def handler():
    return {"ping": "pong"}
