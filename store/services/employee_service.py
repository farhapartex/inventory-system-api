from core.dtos import UserMinimalDTO
from store.dtos import EmployeeDTO, StoreMinimalDTO
from store.exceptions import EmployeeExists
from store.models import Employee


class EmployeeService:
    @classmethod
    def create_employee(cls, *, store, user) -> EmployeeDTO:
        instance = Employee.get_instance({"store": store, "user": user, "is_active": True, "is_deleted": False})
        if instance is not None:
            raise EmployeeExists("Employee exists!")

        employee = Employee.objects.create(store=store, user=user)
        store_dto = StoreMinimalDTO(id=employee.store.id, name=employee.store.name)
        user_dto = UserMinimalDTO(first_name=user.first_name, last_name=user.last_name, email=user.email)
        return EmployeeDTO(id=employee.id, store=store_dto, user=user_dto, is_active=employee.is_active, is_deleted=employee.is_deleted)
