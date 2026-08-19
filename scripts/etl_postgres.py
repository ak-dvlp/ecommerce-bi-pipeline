import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://bi_user:bi_password@localhost:5432/ecommerce_db"
engine = create_engine(DATABASE_URL)

def run_etl():
    print("⏳ Чтение сырых CSV файлов из папки data/...")
    try:
        df_products = pd.read_csv('data/products.csv')
        df_users = pd.read_csv('data/users.csv')
        df_orders = pd.read_csv('data/orders.csv')
        df_order_items = pd.read_csv('data/order_items.csv')
    except FileNotFoundError as e:
        print(f"❌ Ошибка: Не найден файл данных. {e}")
        print("💡 Убедитесь, что файлы лежат прямо в папке data/ и называются соответствующим образом.")
        return

    print("⏳ Предварительная обработка данных в Pandas...")
    # Приведение типов дат к формату datetime для корректной записи в TIMESTAMP базы
    df_users['registration_date'] = pd.to_datetime(df_users['registration_date'])
    df_orders['date_time'] = pd.to_datetime(df_orders['date_time'])
    
    # Обработка пустых промокодов (замена NaN на понятную строку)
    df_orders['promocode'] = df_orders['promocode'].fillna('БЕЗ_ПРОМО')

    print("⏳ Загрузка данных в PostgreSQL...")
    try:
        # !Порядок загрузки важен из-за связей (сначала справочники, потом транзакции)
        df_products.to_sql('products', con=engine, if_exists='append', index=False)
        df_users.to_sql('users', con=engine, if_exists='append', index=False)
        df_orders.to_sql('orders', con=engine, if_exists='append', index=False)
        df_order_items.to_sql('order_items', con=engine, if_exists='append', index=False)
        
        print("🚀 ETL процесс завершён. Все данные успешно загружены в PostgreSQL.")
    except Exception as e:
        print(f"❌ Ошибка при загрузке в БД: {e}")
        print("💡 Проверьте, совпадает ли структура ваших CSV с типами данных в init_db.py")

if __name__ == "__main__":
    run_etl()
