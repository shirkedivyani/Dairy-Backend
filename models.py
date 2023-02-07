import datetime as _dt

import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import passlib.hash as _hash

import database as _database


class User(_database.Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password = _sql.Column(_sql.String)

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)


class Customer(_database.Base):
    __tablename__ = "customer"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    name = _sql.Column(_sql.String, index=True)
    mobile = _sql.Column(_sql.String)
    email = _sql.Column(_sql.String)
    pan = _sql.Column(_sql.String)
    address = _sql.Column(_sql.String)
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    date_last_updated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    milks = _orm.relationship("Milk", back_populates="cust")


class Milk(_database.Base):
    __tablename__ = "milk"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    customer_id = _sql.Column(_sql.Integer, _sql.ForeignKey("customer.id"))
    customer_name = _sql.Column(_sql.String)
    milk_type = _sql.Column(_sql.String)
    lit = _sql.Column(_sql.String)
    fat = _sql.Column(_sql.String, default="")
    snf = _sql.Column(_sql.String, default="")
    amount = _sql.Column(_sql.String)
    is_paid = _sql.Column(_sql.String, default="No")
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    date_last_updated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    cust = _orm.relationship("Customer", back_populates="milks")

#--------------------sales-----------------------
class Sale(_database.Base):
    __tablename__ = "sale"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    customername = _sql.Column(_sql.String, index=True)
    milk_type = _sql.Column(_sql.String)
    lit = _sql.Column(_sql.String)
    amount = _sql.Column(_sql.String)
    is_paid = _sql.Column(_sql.String, default="No")
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    date_last_updated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

#--------------------------------------Purchase--------------------------
class Purchase(_database.Base):
    __tablename__ = "purchase"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    customername = _sql.Column(_sql.String, index=True)
    milk_type = _sql.Column(_sql.String)
    lit = _sql.Column(_sql.String)
    amount = _sql.Column(_sql.String)
    is_paid = _sql.Column(_sql.String, default="No")
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    date_last_updated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    #----------------------------Expenses------------------------------
class Expense(_database.Base):
    __tablename__ = "expense"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    remark = _sql.Column(_sql.String, index=True)
    amount = _sql.Column(_sql.String)
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    date_last_updated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

