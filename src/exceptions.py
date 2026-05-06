from datetime import date

from fastapi import HTTPException


class HotelsException(Exception):
    details_error = "Base error."

    def __init__(self, *args: object) -> None:
        super().__init__(self.details_error, *args)


class ObjectNotFoundException(HotelsException):
    details_error = "Object wasn't found."


class ItemAlreadyExistsException(HotelsException):
    details_error = "Item already exists."


class ObjectHasDependenciesException(HotelsException):
    details_error = "Object has dependent records."


class EmailNotRegisteredException(HotelsException):
    details_error = "Email is not registered."


class IncorrectPasswordException(HotelsException):
    details_error = "Incorrect password."


def check_date_in_and_date_out(date_from: date, date_to: date):
    if date_from >= date_to:
        raise HTTPException(
            status_code=422,
            detail="Date check in must be earlier than date check out.",
        )


class HotelsHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(HotelsHTTPException):
    status_code = 404
    detail = "Hotel wasn't found."


class RoomNotFoundHTTPException(HotelsHTTPException):
    status_code = 404
    detail = "Room wasn't found."


class RoomAlreadyExistsHTTPException(HotelsHTTPException):
    status_code = 409
    detail = "Room already exists."


class HotelHasRoomsHTTPException(HotelsHTTPException):
    status_code = 409
    detail = "Cannot delete hotel because it still has rooms."


class RoomHasBookingsHTTPException(HotelsHTTPException):
    status_code = 409
    detail = "Cannot delete room because it still has bookings."


class EmailNotRegisteredHTTPException(HotelsHTTPException):
    status_code = 404
    detail = "Email is not registered."


class IncorrectPasswordHTTPException(HotelsHTTPException):
    status_code = 401
    detail = "Incorrect password."
