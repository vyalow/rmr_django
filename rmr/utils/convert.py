import collections

from rmr.errors import ClientError


def to_int(value, field_name=None, strict=True):
    if field_name:
        error_message = \
            'Type error: integer is expected for {field_name} field'.format(
                field_name=field_name
            )
    else:
        error_message = 'Type error: integer is expected'
    if isinstance(value, collections.Iterable):
        try:
            return list(map(int, value))
        except (ValueError, TypeError):
            raise ClientError(
                code='type_error',
                message=error_message,
            )
    else:
        try:
            if strict:
                return int(value)
            else:
                return int(float(value))
        except (ValueError, TypeError):
            raise ClientError(
                code='type_error',
                message=error_message,
            )
