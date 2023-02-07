import datetime as _dt

import pydantic as _pydantic


class _UserBase(_pydantic.BaseModel):
    email: str


class UserCreate(_UserBase):
    hashed_password: str

    class Config:
        orm_mode = True


class User(_UserBase):
    id: int

    class Config:
        orm_mode = True


class _CustomerBase(_pydantic.BaseModel):
    name: str
    mobile: str
    email: str
    pan: str
    address: str

class CustomerCreate(_CustomerBase):
    pass


class Customer(_CustomerBase):
    id: int
    date_created: _dt.datetime
    date_last_updated: _dt.datetime

    class Config:
        orm_mode = True


class _MilkBase(_pydantic.BaseModel):
    customer_id: int
    customer_name: str
    milk_type: str
    lit: str
    fat: str
    snf: str
    amount: str
    is_paid: str


class MilkCreate(_MilkBase):
    pass


class Milk(_MilkBase):
    id: int
    date_created: _dt.datetime
    date_last_updated: _dt.datetime

    class Config:
        orm_mode = True
#-------------------------------------------------SALES
class _SaleBase(_pydantic.BaseModel):
    customername: str
    milk_type: str
    lit: str
    amount: str
    is_paid: str


class SaleCreate(_SaleBase):
    pass


class Sale(_SaleBase):
    id: int
    date_created: _dt.datetime
    date_last_updated: _dt.datetime

    class Config:
        orm_mode = True

# #---------------------purchase---------------
class _PurchaseBase(_pydantic.BaseModel):
    customername: str
    milk_type: str
    lit: str
    amount: str
    is_paid: str


class PurchaseCreate(_PurchaseBase):
    pass


class Purchase(_PurchaseBase):
    id: int
    date_created: _dt.datetime
    date_last_updated: _dt.datetime

    class Config:
        orm_mode = True

#-----------------------------Expense--------------------------------
class _ExpenseBase(_pydantic.BaseModel):
    remark: str
    amount: str
    
    


class ExpenseCreate(_ExpenseBase):
    pass


class Expense(_ExpenseBase):
    id: int
    date_created: _dt.datetime
    date_last_updated: _dt.datetime

    class Config:
        orm_mode = True