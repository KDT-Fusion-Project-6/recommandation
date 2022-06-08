import pandas as pd
import pymysql
import pandas as pd

def where_clause(conditions):
    where_clause = ''
    for column in conditions.keys():
        for value in conditions[column]:
            where_clause += f'{column} = "{value}"'
            where_clause += ' OR '
    return where_clause[:-4]

def columns_selection(columns):
    select_columns = ''
    for column in columns:
        select_columns += f'{column}, '
    return select_columns[:-2]


class database:
    def __init__(self, host, user, password, db, charset='utf8'):
        self.conn = pymysql.connect(
            host=host, user=user, password=password, db=db, charset=charset)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def select_all(self, table_name):
        sql = "SELECT * FROM %s" % table_name
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def select_columns(self, table_name, columns):
        column_selection = columns_selection(columns)
        sql = f"SELECT {column_selection} FROM {table_name}"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def select_where_with_condition(self, columns, table_name, conditions):
        where_clause = where_clause(conditions)
        column_selection = columns_selection(columns)
        sql = f"SELECT {column_selection} FROM {table_name} WHERE {where_clause}"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def insert_data(self, table_name, data):
        sql = "INSERT INTO %s VALUES (%s)" % (table_name, data)
        self.cursor.execute(sql)
        self.conn.commit()
