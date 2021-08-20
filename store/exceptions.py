from inventory.exceptions import CommonException


class StoreNotFoundException(CommonException):
    pass


class StoreAlreadyExistsException(CommonException):
    pass


class StoreOwnerDoesNotMatch(CommonException):
    pass


class ProductCategoryNotFoundException(CommonException):
    pass