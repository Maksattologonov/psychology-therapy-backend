from fastapi import HTTPException, status


def get_instance_slice(page: int, count: int) -> slice:
    instance_slice = slice(page * count, page * count + count)
    return instance_slice


bad_exception = HTTPException(detail="Пользователь заблокирован", status_code=status.HTTP_401_UNAUTHORIZED)
