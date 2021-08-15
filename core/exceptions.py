from inventory.exceptions import CommonException


class UserExistsException(CommonException):
    pass


class UserNotFoundException(CommonException):
    pass


class UserAlreadyActiveException(CommonException):
    pass
