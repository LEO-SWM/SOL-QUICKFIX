import pandas as pd
from sqlalchemy import create_engine, MetaData, delete, select, Table

# Define the SQLite database connection


class Querier:
    def __init__(self, db_name, flash_table_name, orders_table_name):
        self.flash_table_name = flash_table_name
        self.orders_table_name = orders_table_name
        self.engine = create_engine(db_name)

    def get_user_infos(self, user: str):
        with self.engine.connect() as connection:
            metadata = MetaData()
            metadata.reflect(bind=self.engine)
            query = "SELECT * FROM orders WHERE Anschrift1 = '{}'".format(user)
            df_query = pd.read_sql_query(query, connection)
            serial_numbers = df_query["Seriennummer"]
            flash_table = Table(
                self.flash_table_name,
                metadata,
                autoload=True,
                autoload_with=self.engine,
            )
            query = select(flash_table).where(
                flash_table.c.Seriennummer.in_(serial_numbers)
            )
            flash_result = connection.execute(query)
            rows = flash_result.fetchall()
            columns = flash_result.keys()
            flash_df = pd.DataFrame(rows, columns=columns)
            merged_df = df_query.merge(flash_df, how="left", on="Seriennummer")
            merged_df = merged_df.astype(str)
        return merged_df

    def get_panel_info(self, panel: str):
        with self.engine.connect() as connection:
            metadata = MetaData()
            metadata.reflect(bind=self.engine)
            query = "SELECT * FROM orders WHERE Seriennummer = '{}'".format(panel)
            df_orders = pd.read_sql_query(query, connection)
            query = "SELECT * FROM flash WHERE Seriennummer = '{}'".format(panel)
            df_flash = pd.read_sql_query(query, connection)
            merged_df = df_orders.merge(df_flash, how="outer", on="Seriennummer")
            merged_df = merged_df.astype(str)
        return merged_df
