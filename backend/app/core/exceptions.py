from fastapi import HTTPException, status


class AppError(Exception):
    """Base application error for domain-level failures."""


class ValidationError(AppError):
    pass


def raise_http_error(status_code: int, message: str, details: dict | None = None) -> None:
    raise HTTPException(
        status_code=status_code,
        detail={
            "message": message,
            "details": details or {},
        },
    )
