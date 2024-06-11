
class CustomException(Exception):
    ...


class InvalidNameError(CustomException):
    pass


class InvalidDeadlineError(CustomException):
    pass


class ActivityError(CustomException):
    pass
