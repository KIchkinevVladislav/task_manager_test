from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


async def handle_api_exceptions(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except HTTPException:
        raise
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )
