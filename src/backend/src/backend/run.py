from quart import Quart, ResponseReturnValue
from quart_auth import QuartAuth
from quart_rate_limiter import RateLimitExceeded, RateLimiter, rate_exempt, rate_limit
from quart_schema import QuartSchema

from backend.lib.api_error import APIError
from datetime import timedelta

app = Quart(__name__)

schema = QuartSchema(app, convert_casing=True)

auth_manager = QuartAuth(app)
rate_limiter = RateLimiter(app)


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
