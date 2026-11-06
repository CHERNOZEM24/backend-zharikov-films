from rest_framework.exceptions import ParseError, ValidationError
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None  

    if isinstance(exc, ParseError):
        response.data = {"error": "Некорректный JSON", "field": "body"}
    elif isinstance(exc, ValidationError):
        data = response.data
        if isinstance(data, dict) and data:
            field, errors = next(iter(data.items()))
            message = errors[0] if isinstance(errors, list) and errors else errors
            response.data = {"error": str(message), "field": field}
        else:
            response.data = {"error": "Некорректные данные", "field": "body"}
    else:
        response.data = {"error": str(exc.detail), "field": None}
    return response