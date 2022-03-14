import os

import psycopg2
from dotenv import load_dotenv
from psycopg2 import Error

load_dotenv()

create_database = """
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS goods;
    DROP TABLE IF EXISTS goods_type;
    CREATE TABLE goods_type
    (
       goods_type_id INT GENERATED ALWAYS AS IDENTITY,
       goods_type_name VARCHAR(255) NOT NULL,
       PRIMARY KEY(goods_type_id)
    );
    CREATE TABLE goods
    (
       goods_id INT GENERATED ALWAYS AS IDENTITY,
       goods_name VARCHAR(255) NOT NULL,
       goods_type_id INT,
       PRIMARY KEY(goods_id),
       CONSTRAINT fk_goods
          FOREIGN KEY(goods_type_id)
        REFERENCES goods_type(goods_type_id)
    );
    CREATE TABLE orders
    (
       order_id INT GENERATED ALWAYS AS IDENTITY,
       user_name VARCHAR(255) NOT NULL,
       total INT,
       goods_id INT,
       PRIMARY KEY(order_id),
       CONSTRAINT fk_order
          FOREIGN KEY(goods_id)
        REFERENCES goods(goods_id)
    );
    INSERT INTO goods_type(goods_type_name)
    VALUES('vegetables'),
          ('fruits'),
          ('cookie');
    
    INSERT INTO goods(goods_name, goods_type_id)
    VALUES('tomato',1),
          ('potatoes',1),
          ('banana',2),
          ('orange',2),
          ('oreo',3),
          ('chocopie',3);
    
    INSERT INTO orders(user_name, total, goods_id)
    VALUES('John',2,1),
          ('John',1,3),
          ('Jane',3,5),
          ('Jane',3,6),
          ('David',10,2),
          ('David',5,5),
          ('David',3,1),
          ('Ann', 1,6);
"""


def connect_to_database_and_execute_command(command: str, create: bool = False):
    host = os.getenv('HOST')
    user = os.getenv('USER')
    password = os.getenv('PASSWORD')
    database = os.getenv('DATABASE')

    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(command)
            if not create:
                print(f"Результат: {cursor.fetchall()}")
    except (Exception, Error) as error:
        print("[INFO] Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            connection.close()
            print("[INFO] Соединение с PostgreSQL закрыто")


if __name__ == '__main__':
    # Создание нужных таблиц и заполнение их данными
    connect_to_database_and_execute_command(create_database, create=True)

    # Первый вариант решения
    popular_product_category = """
        WITH table_popular_category as (
            SELECT goods_type_name, SUM(total) goods_type_count
            FROM goods_type
            JOIN goods USING (goods_type_id)
            JOIN orders USING (goods_id)
            GROUP BY goods_type_name
            ORDER BY goods_type_count DESC
        )
    
        SELECT goods_type_name, goods_type_count
        FROM table_popular_category p_category
        WHERE p_category.goods_type_count = (
            SELECT goods_type_count 
            FROM table_popular_category 
            LIMIT 1
            );
    """

    # Второй вариант решения
    popular_product_category_2 = """
        SELECT goods_type_name, SUM(total) goods_type_count
        FROM goods_type
        JOIN goods USING (goods_type_id)
        JOIN orders USING (goods_id)
        GROUP BY goods_type_name
        ORDER BY goods_type_count DESC
        LIMIT 1;
    """

    connect_to_database_and_execute_command(popular_product_category)  # Поиск самой популярной категории товаров
