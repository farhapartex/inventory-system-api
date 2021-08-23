from inventory.exceptions import CommonException


class StoreNotFoundException(CommonException):
    pass


class StoreAlreadyExistsException(CommonException):
    pass


class StoreOwnerDoesNotMatch(CommonException):
    pass


class EmployeeExists(CommonException):
    pass


class ProductCategoryNotFoundException(CommonException):
    pass


class ProductNotFoundException(CommonException):
    pass


class ProductOwnerDoesNotMatchException(CommonException):
    pass

