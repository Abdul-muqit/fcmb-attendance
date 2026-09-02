from pydantic import BaseModel, EmailStr


class StaffCreate(BaseModel):
    staff_id: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    department: str
    role: str


class StaffResponse(BaseModel):
    id: int
    staff_id: str
    first_name: str
    last_name: str
    email: EmailStr
    department_id: int
    role_id: int

    model_config = {
        "from_attributes": True
    }