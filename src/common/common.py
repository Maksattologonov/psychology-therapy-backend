def get_instance_slice(page: int, count: int) -> slice:
    instance_slice = slice(page * count, page * count + count)
    return instance_slice
