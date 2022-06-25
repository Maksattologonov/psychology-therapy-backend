from fastapi import status
from starlette.responses import JSONResponse
from fastapi import HTTPException

register_response = JSONResponse(
    status_code=status.HTTP_200_OK,
    content="The account has been successfully registered, to use please go through verification"
)

duplicate_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='duplicate key value violates unique constraint',
)

permission_exception = HTTPException(detail="You don't have any permissions",
                                     status_code=status.HTTP_406_NOT_ACCEPTABLE)

not_validate = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='could not  validate credentials',
    headers={
        'WWW-Authenticate': 'Bearer'
    })
bad_credentials = HTTPException(detail="Bad credentials", status_code=status.HTTP_400_BAD_REQUEST)

empty_exception = HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Parameters cannot be empty")


def already_exist_exception(text: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"{text} already exists")


def not_found_exception(text: str) -> HTTPException:
    raise HTTPException(detail=f"{text} not found",
                        status_code=status.HTTP_404_NOT_FOUND)
