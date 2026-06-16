from quart import Quart, ResponseReturnValue
from quart_auth import QuartAuth
from backend.lib.api_error import APIError

app = Quart(__name__)

auth_manager = QuartAuth(app)


@app.errorhandler(APIError)  # type: ignore
async def handle_api_error(error: APIError) -> ResponseReturnValue:
    return {"code": error.code}, error.status_code


@app.errorhandler(500)
async def handle_generic_error(error: Exception) -> ResponseReturnValue:
    return {"code": "INTERNAL_SERVER_ERROR"}, 500


@app.get("/control/ping/")
async def ping() -> ResponseReturnValue:
    return {"ping": "pong"}
