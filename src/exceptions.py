class HotelsException(Exception):
    details_error = "Base error."

    def __init__(self, *args: object) -> None:
        super().__init__(self.details_error, *args)


class ObjectNotFoundException(HotelsException):
    details_error = "Object wasn't found."


class ItemAlreadyExistsException(HotelsException):
    details_error = "Item already exists."
