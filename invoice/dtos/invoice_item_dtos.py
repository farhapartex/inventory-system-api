from pydantic import BaseModel


class InvoiceItemCreateDTO(BaseModel):
    product_id: int
    quantity: int
    price: float


