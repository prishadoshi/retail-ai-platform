from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import Column, Integer, String, Date, Boolean, Numeric
import pandas as pd
import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

# df = pd.read_csv("data/retail_store_inventory_data.csv")

# print(df.head())
# print(df.dtypes)

# df["Date"] = pd.to_datetime(df["Date"])

# # -----------------------------
# # Convert Holiday to Boolean
# # -----------------------------
# df["Holiday/Promotion"] = df["Holiday/Promotion"].astype(bool)

# -----------------------------
# Import
# -----------------------------


# df.to_sql(
#     "retail_inventory",
#     engine,
#     if_exists="replace",
#     index=False,
#     dtype={
#         "Date": Date(),

#         "Store ID": String(10),

#         "Product ID": String(20),

#         "Category": String(50),

#         "Region": String(50),

#         "Inventory Level": Integer(),

#         "Units Sold": Integer(),

#         "Units Ordered": Integer(),

#         "Demand Forecast": Numeric(10,2),

#         "Price": Numeric(10,2),

#         "Discount": Integer(),

#         "Weather Condition": String(20),

#         "Holiday/Promotion": Boolean(),

#         "Competitor Pricing": Numeric(10,2),

#         "Seasonality": String(20)
#     }
# )



SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()