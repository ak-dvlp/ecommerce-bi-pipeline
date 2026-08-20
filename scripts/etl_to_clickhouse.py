import pandas as pd
from sqlalchemy import create_engine
import clickhouse_connect

# Настройки подключений
PG_URL = "postgresql://bi_user:bi_password@localhost:5433/ecommerce_db"
pg_engine = create_engine(PG_URL)

print("⏳ Чтение данных из PostgreSQL...")
df_orders = pd.read_sql("SELECT * FROM orders", pg_engine)
df_order_items = pd.read_sql("SELECT * FROM order_items", pg_engine)
df_clients= pd.read_sql("SELECT * FROM clients", pg_engine)
df_products = pd.read_sql("SELECT * FROM products", pg_engine)

print("⏳ Денормализация данных (сборка плоской витрины)...")
# Сборка всех 4 таблиц в один большой датафрейм через JOIN (merge)
df_flat = df_order_items.merge(df_orders, on="order_id", how="inner")
df_flat = df_flat.merge(df_clients, on="client_id", how="inner")
df_flat = df_flat.merge(df_products, on="product_id", how="inner")

# Подсчёт финансовых показателей непосредственно в Pandas для удобства BI
df_flat["revenue"] = df_flat["quantity"] * df_flat["sale_price"]
df_flat["cost"] = df_flat["quantity"] * df_flat["cost_price"]
df_flat["profit"] = df_flat["revenue"] - df_flat["cost"]

# Отбираем и упорядочиваем только нужные для дашборда колонки
final_columns = [
    "row_id", "order_id", "date_time", "client_id", "client_name", 
    "city", "country", "device", "status", "promocode", 
    "product_id", "product_name", "category", "quantity", 
    "sale_price", "cost_price", "revenue", "cost", "profit"
]
df_flat = df_flat[final_columns]

print("⏳ Подключение к ClickHouse и создание таблицы...")
# Настройки берутся из нашего docker-compose.yml (порт 8123 для HTTP)
ch_client = clickhouse_connect.get_client(
    host='localhost',
    port=8123,
    username='bi_user',
    password='bi_password',
    database='ecommerce_olap'
)

# Создаем таблицу в ClickHouse. Используем движок MergeTree с сортировкой по дате и заказу
ch_client.command("""
CREATE TABLE IF NOT EXISTS f_sales (
    row_id Int32,
    order_id Int32,
    date_time DateTime,
    client_id Int32,
    client_name String,
    city String,
    country String,
    device String,
    status String,
    promocode String,
    product_id Int32,
    product_name String,
    category String,
    quantity Int32,
    sale_price Decimal(10, 2),
    cost_price Decimal(10, 2),
    revenue Decimal(10, 2),
    cost Decimal(10, 2),
    profit Decimal(10, 2)
) ENGINE = MergeTree()
PRIMARY KEY (order_id)
ORDER BY (order_id, date_time);
""")

print("⏳ Запись плоской витрины в ClickHouse...")
# clickhouse-connect умеет эффективно паковать датафреймы Pandas напрямую
ch_client.insert_df(table='f_sales', df=df_flat)

print(f"🚀 Успех! В ClickHouse перенесено {len(df_flat)} строк в плоском виде.")
