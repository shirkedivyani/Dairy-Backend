from typing import List
import fastapi as _fastapi
from fastapi import Depends, FastAPI
import fastapi.security as _security
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy.orm as _orm

import services as _services, schemas as _schemas

app = FastAPI()


origins = [
    "http://localhost:6001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/users")
async def create_user(
    user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    db_user = await _services.get_user_by_email(user.email, db)
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="Email already in use")

    user = await _services.create_user(user, db)

    return await _services.create_token(user)


@app.post("/api/token")
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    user = await _services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")

    return await _services.create_token(user)


@app.get("/api/users/me", response_model=_schemas.User)
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return user


@app.get("/api/customers", response_model=List[_schemas.Customer])
async def get_customers(
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await _services.get_customers(db=db)


@app.post("/api/customers", response_model=_schemas.Customer)
async def create_customer(
    customer: _schemas.CustomerCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await _services.create_customer(db=db, customer=customer)


@app.get("/api/customers/{customer_id}", status_code=200)
async def get_customer(
    customer_id: int,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await _services.get_customer(customer_id, db)


@app.delete("/api/customers/{customer_id}", status_code=200)
async def delete_customer(
    customer_id: int,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    await _services.delete_customer(customer_id, db)
    return {"message", "Successfully Deleted"}


@app.put("/api/customers/{customer_id}", status_code=200)
async def update_customer(
    customer_id: int,
    customer: _schemas.CustomerCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    await _services.update_customer(customer_id, customer, db)
    return {"message", "Successfully Updated"}


@app.post("/api/milks", response_model=_schemas.Milk)
async def create_milk(
    milk: _schemas.MilkCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await _services.create_milk(db=db, milk=milk)


@app.get("/api/milks", response_model=List[_schemas.Milk])
async def get_milks(
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await _services.get_milks(db=db)


@app.get("/api/milks/{milk_id}", status_code=200)
async def get_milk(
    milk_id: int,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await _services.get_milk(milk_id, db)


@app.put("/api/milks/{milk_id}", status_code=200)
async def update_milk(
    milk_id: int,
    milk: _schemas.MilkCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    await _services.update_milk(milk_id, milk, db)
    return {"message", "Successfully Updated"}


@app.delete("/api/milks/{milk_id}", status_code=200)
async def delete_milk(
    milk_id: int,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    await _services.delete_milk(milk_id, db)
    return {"message", "Successfully Deleted"}

#---------------milksales---------------
@app.post("/api/sales", response_model=_schemas.Sale)
async def create_sale(
    sale: _schemas. SaleCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await _services.create_sale(db=db, sale=sale)


@app.get("/api/sales", response_model=List[_schemas.Sale])
async def get_sales(
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await _services.get_sales(db=db)


@app.get("/api/sales/{sale_id}", status_code=200)
async def get_sale(
    sale_id: int,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await _services.get_sale(sale_id, db)


@app.put("/api/sales/{sale_id}", status_code=200)
async def update_sale(
    sale_id: int,
    sale: _schemas.SaleCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    await _services.update_sale(sale_id, sale, db)
    return {"message", "Successfully Updated"}


@app.delete("/api/sales/{sale_id}", status_code=200)
async def delete_sale(
    sale_id: int,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    await _services.delete_sale(sale_id, db)
    return {"message", "Successfully Deleted"}

#-------------------------------------MilkPurchase----------------------
@app.post("/api/purchases", response_model=_schemas.Purchase)
async def create_purchase(
    purchase: _schemas. PurchaseCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await _services.create_purchase(db=db, purchase=purchase)


@app.get("/api/purchases", response_model=List[_schemas.Purchase])
async def get_purchases(
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await _services.get_purchases(db=db)


@app.get("/api/purchases/{purchase_id}", status_code=200)
async def get_purchase(
    purchase_id: int,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await _services.get_purchase(purchase_id, db)


@app.put("/api/purchases/{purchase_id}", status_code=200)
async def update_purchase(
    purchase_id: int,
    purchase: _schemas.PurchaseCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    await _services.update_purchase(purchase_id, purchase, db)
    return {"message", "Successfully Updated"}


@app.delete("/api/purchases/{purchase_id}", status_code=200)
async def delete_purchase(
    purchase_id: int,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    await _services.delete_purchase(purchase_id, db)
    return {"message", "Successfully Deleted"}

#--------------------------------------Expenses----------------------------
@app.post("/api/expenses", response_model=_schemas.Expense)
async def create_expense(
    expense: _schemas. ExpenseCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await _services.create_expense(db=db, expense=expense)


@app.get("/api/expenses", response_model=List[_schemas.Expense])
async def get_expenses(
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await _services.get_expenses(db=db)


@app.get("/api/expenses/{expense_id}", status_code=200)
async def get_expense(
    expense_id: int,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await _services.get_expense(expense_id, db)


@app.put("/api/expenses/{expense_id}", status_code=200)
async def update_expense(
    expense_id: int,
    expense: _schemas.ExpenseCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    await _services.update_expense(expense_id, expense, db)
    return {"message", "Successfully Updated"}


@app.delete("/api/expenses/{expense_id}", status_code=200)
async def delete_expense(
    expense_id: int,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    await _services.delete_expense(expense_id, db)
    return {"message", "Successfully Deleted"}



# --------------------------------------------------------------------
@app.get("/api")
async def root():
    return {"message": "Awesome backend connected"}