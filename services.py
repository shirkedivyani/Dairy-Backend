import fastapi as _fastapi
import fastapi.security as _security
import jwt as _jwt
import datetime as _dt
import sqlalchemy.orm as _orm
import passlib.hash as _hash

import database as _database, models as _models, schemas as _schemas

oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")

JWT_SECRET = "myjwtsecret"


def create_database():
    return _database.Base.metadata.create_all(bind=_database.engine)


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_user_by_email(email: str, db: _orm.Session):
    return db.query(_models.User).filter(_models.User.email == email).first()


async def create_user(user: _schemas.UserCreate, db: _orm.Session):
    user_obj = _models.User(
        email=user.email, hashed_password=_hash.bcrypt.hash(user.hashed_password)
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def authenticate_user(email: str, password: str, db: _orm.Session):
    user = await get_user_by_email(db=db, email=email)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user


async def create_token(user: _models.User):
    user_obj = _schemas.User.from_orm(user)

    token = _jwt.encode(user_obj.dict(), JWT_SECRET)

    return dict(access_token=token, token_type="bearer")


async def get_current_user(
    db: _orm.Session = _fastapi.Depends(get_db),
    token: str = _fastapi.Depends(oauth2schema),
):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
    except:
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )

    return _schemas.User.from_orm(user)


async def _customer_selector(customer_id: int, db: _orm.Session):
    customer = (
        db.query(_models.Customer)
        .filter(_models.Customer.id == customer_id)
        .first()
    )

    if customer is None:
        raise _fastapi.HTTPException(status_code=404, detail="Customer does not exist")

    return customer


async def get_customers(db: _orm.Session):
    customers = db.query(_models.Customer)

    return list(map(_schemas.Customer.from_orm, customers))


async def create_customer(db: _orm.Session, customer: _schemas.CustomerCreate):
    customer = _models.Customer(**customer.dict())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return _schemas.Customer.from_orm(customer)


async def get_customer(customer_id: int,  db: _orm.Session):
    customer = await _customer_selector(customer_id=customer_id, db=db)

    return _schemas.Customer.from_orm(customer)


async def delete_customer(customer_id: int, db: _orm.Session):
    customer = await _customer_selector(customer_id, db)

    db.delete(customer)
    db.commit()


async def update_customer(customer_id: int, customer: _schemas.CustomerCreate, db: _orm.Session):
    customer_db = await _customer_selector(customer_id, db)

    customer_db.name = customer.name
    customer_db.mobile = customer.mobile
    customer_db.email = customer.email
    customer_db.pan = customer.pan
    customer_db.mobile = customer.address
    customer_db.date_last_updated = _dt.datetime.utcnow()

    db.commit()
    db.refresh(customer_db)

    return _schemas.Customer.from_orm(customer_db)


async def _milk_selector(milk_id: int, db: _orm.Session):
    milk = (
        db.query(_models.Milk)
        .filter(_models.Milk.id == milk_id)
        .first()
    )

    if milk is None:
        raise _fastapi.HTTPException(status_code=404, detail="Milk record does not exist")

    return milk


async def create_milk(db: _orm.Session, milk: _schemas.MilkCreate):
    milk = _models.Milk(**milk.dict())
    db.add(milk)
    db.commit()
    db.refresh(milk)
    return _schemas.Milk.from_orm(milk)


async def get_milks(db: _orm.Session):
    milks = db.query(_models.Milk)

    return list(map(_schemas.Milk.from_orm, milks))


async def get_milk(milk_id: int,  db: _orm.Session):
    milk = await _milk_selector(milk_id=milk_id, db=db)

    return _schemas.Milk.from_orm(milk)


async def update_milk(milk_id: int, milk: _schemas.MilkCreate, db: _orm.Session):
    milk_db = await _milk_selector(milk_id, db)

    milk_db.customer_id = milk.customer_id
    milk_db.customer_name = milk.customer_name
    milk_db.milk_type = milk.milk_type
    milk_db.lit = milk.lit
    milk_db.fat = milk.fat
    milk_db.snf = milk.snf
    milk_db.amount = milk.amount
    milk_db.is_paid = milk.is_paid
    milk_db.date_last_updated = _dt.datetime.utcnow()

    db.commit()
    db.refresh(milk_db)

    return _schemas.Milk.from_orm(milk_db)


async def delete_milk(milk_id: int, db: _orm.Session):
    milk = await _milk_selector(milk_id, db)

    db.delete(milk)
    db.commit()

    #---------------------------------------------------------sales
async def _sale_selector(sale_id: int, db: _orm.Session):
    sale = (
        db.query(_models.Sale)
        .filter(_models.Sale.id == sale_id)
        .first()
    )

    if sale is None:
        raise _fastapi.HTTPException(status_code=404, detail="Sale record does not exist")

    return sale


async def create_sale(db: _orm.Session, sale: _schemas.SaleCreate):
    sale = _models.Sale(**sale.dict())
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return _schemas.Sale.from_orm(sale)

async def get_sales(db: _orm.Session):
    sales = db.query(_models.Sale)

    return list(map(_schemas.Sale.from_orm, sales))


async def get_sale(sale_id: int,  db: _orm.Session):
    sale = await _sale_selector(sale_id=sale_id, db=db)

    return _schemas.Sale.from_orm(sale)


async def update_sale(sale_id: int, sale: _schemas.SaleCreate, db: _orm.Session):
    sale_db = await _sale_selector(sale_id, db)

    sale_db.customer_id = sale.customer_id
    sale_db.customername = sale.customername
    sale_db.milk_type = sale.milk_type
    sale_db.lit = sale.lit
    sale_db.amount = sale.amount
    sale_db.is_paid = sale.is_paid
    db.commit()
    db.refresh(sale_db)

    return _schemas.Sale.from_orm(sale_db)


async def delete_sale(sale_id: int, db: _orm.Session):
    sale = await _sale_selector(sale_id, db)

    db.delete(sale)
    db.commit()
#---------------------------------purchase__________________________________
async def _purchase_selector(purchase_id: int, db: _orm.Session):
    purchase = (
        db.query(_models.Purchase)
        .filter(_models.Purchase.id ==purchase_id)
        .first()
    )

    if purchase is None:
        raise _fastapi.HTTPException(status_code=404, detail="Purchase record does not exist")

    return purchase


async def create_purchase(db: _orm.Session, purchase: _schemas.PurchaseCreate):
    purchase = _models.Purchase(**purchase.dict())
    db.add(purchase)
    db.commit()
    db.refresh(purchase)
    return _schemas.Purchase.from_orm(purchase)

async def get_purchases(db: _orm.Session):
    purchases = db.query(_models.Purchase)

    return list(map(_schemas.Purchase.from_orm, purchases))


async def get_purchase(purchase_id: int,  db: _orm.Session):
    purchase = await _purchase_selector(purchase_id=purchase_id, db=db)

    return _schemas.Purchase.from_orm(purchase)


async def update_purchase(purchase_id: int, purchase: _schemas.PurchaseCreate, db: _orm.Session):
    purchase_db = await _purchase_selector(purchase_id, db)

    purchase_db.customer_id = purchase.customer_id
    purchase_db.customername = purchase.customername
    purchase_db.milk_type = purchase.milk_type
    purchase_db.lit = purchase.lit
    purchase_db.amount = purchase.amount
    purchase_db.is_paid = purchase.is_paid
    db.commit()
    db.refresh(purchase_db)

    return _schemas.Purchase.from_orm(purchase_db)


async def delete_purchase(purchase_id: int, db: _orm.Session):
    purchase = await _purchase_selector(purchase_id, db)

    db.delete(purchase)
    db.commit()

#-----------------------------------------EXPENSES--------------------------------------
async def _expense_selector(expense_id: int, db: _orm.Session):
    expense = (
        db.query(_models.Expense)
        .filter(_models.Expense.id == expense_id)
        .first()
    )

    if expense is None:
        raise _fastapi.HTTPException(status_code=404, detail="Expense record does not exist")

    return expense


async def create_expense(db: _orm.Session, expense: _schemas.ExpenseCreate):
    expense = _models.Expense(**expense.dict())
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return _schemas.Expense.from_orm(expense)

async def get_expenses(db: _orm.Session):
    expenses = db.query(_models.Expense)

    return list(map(_schemas.Expense.from_orm, expenses))


async def get_expense(expense_id: int,  db: _orm.Session):
    expense = await _expense_selector(expense_id=expense_id, db=db)

    return _schemas.Expense.from_orm(expense)


async def update_expense(expense_id: int, expense: _schemas.ExpenseCreate, db: _orm.Session):
    expense_db = await _expense_selector(expense_id, db)

    expense_db.customer_id = expense.customer_id
    expense_db.remark = expense.remark
    expense_db.amount = expense.amount
    db.commit()
    db.refresh(expense_db)

    return _schemas.Expense.from_orm(expense_db)


async def delete_expense(expense_id: int, db: _orm.Session):
    expense = await _expense_selector(expense_id, db)

    db.delete(expense)
    db.commit()