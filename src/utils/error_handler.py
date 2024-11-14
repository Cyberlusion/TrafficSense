# Centralized Error Handling

# For more complex applications, it’s a good idea to centralize error handling. This can help maintain a consistent error structure throughout the project.

# src/utils/error_handler.py

from fastapi import HTTPException
from fastapi.responses import JSONResponse
from starlette.requests import Request

def handle_http_exception(request: Request, exc: HTTPException):
    """Custom error handler for HTTPExceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "method": request.method, "url": str(request.url)},
    )

def handle_generic_error(request: Request, exc: Exception):
    """Generic error handler for unexpected exceptions."""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "method": request.method, "url": str(request.url)},
    )
