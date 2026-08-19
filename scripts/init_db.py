import sys
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://bi_user:bi_password@localhost:5432/ecommerce_db"
engine = create_engine(DATABASE_URL)

DROP_DDL = """
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS products;
"""

CREATE_DDL = """
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(100),
    cost_price NUMERIC(10, 2),
    sale_price NUMERIC(10, 2)
);

CREATE TABLE users (
    user_id INT PRIMARY KEY,
    name VARCHAR(255),
    registration_date TIMESTAMP,
    city VARCHAR(100),
    country VARCHAR(100),
    device VARCHAR(50)
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    date_time TIMESTAMP,
    status VARCHAR(50),
    promocode VARCHAR(50)
);

CREATE TABLE order_items (
    row_id INT PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(product_id),
    quantity INT,
    sale_price NUMERIC(10, 2)
);
"""

def init_database():
    response = input("Вы хотите полностью пересоздать схему БД? (Все данные будут удалены!) [y/N]: ")
    if response.lower() not in ['y', 'yes']:
        print("❌ Инициализация отменена пользователем.")
        sys.exit()

    print("⏳ Удаление старых таблиц...")
    with engine.begin() as conn:
        conn.execute(text(DROP_DDL))
    
    print("⏳ Создание новых таблиц (DDL)...")
    with engine.begin() as conn:
        conn.execute(text(CREATE_DDL))
        
    print("✅ Схема данных PostgreSQL успешно инициализирована.")

if __name__ == "__main__":
    init_database()
