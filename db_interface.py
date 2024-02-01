import io
import pandas as pd
from sqlalchemy.orm import sessionmaker
from starlette.responses import StreamingResponse
from sqlalchemy import create_engine, MetaData, delete, select, Table
from models import Base
from models.flash import Flash
from models.order import Order


class DBInterface:
    def __init__(self, db_name):
        self.flash_table_name = Flash.__tablename__
        self.orders_table_name = Order.__tablename__
        self.engine = create_engine(db_name)
        self.Session = sessionmaker(bind=self.engine)

    def initialize_database(self):
        Base.metadata.create_all(self.engine)

    def download_df(self, df, name):
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="User Info")
        buffer.seek(0)
        return StreamingResponse(
            buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f'attachment; filename="{name}_info.xlsx"'},
        )

    def import_infos(self, excel_file, table_name):
        if table_name == self.flash_table_name:
            table = Flash
        elif table_name == self.orders_table_name:
            table = Order
        else:
            raise "Not a valid table!"
        # Read the Excel file
        df = pd.read_excel(excel_file)
        # Create a database connection
        metadata = MetaData()
        metadata.reflect(bind=self.engine)
        with self.Session() as session:
            to_delete = df["Seriennummer"]
            delete_query = delete(table).where(table.Seriennummer.in_(to_delete))
            session.execute(delete_query)
            session.commit()
        # Write the data from the Excel file to a SQL database
        df.set_index("Seriennummer", inplace=True)
        keys = df.keys()
        columns = dict()
        for key in keys:
            columns[key] = key.strip().split(" ")[0]
        df.rename(columns=columns, inplace=True)
        df.to_sql(table_name, con=self.engine, if_exists="append", index=True)

    def import_flash_infos(self, excel_file):
        self.import_infos(excel_file, self.flash_table_name)

    def import_order_infos(self, excel_file):
        self.import_infos(excel_file, self.orders_table_name)

    def df_from_query(self, query):
        with self.engine.connect() as connection:
            order_result = connection.execute(query)
            rows = order_result.fetchall()
            columns = order_result.keys()
            df_query = pd.DataFrame(rows, columns=columns)
        return df_query

    def get_user_infos(self, user: str):
        order_query = select(Order).where(Order.Anschrift1.in_([user]))
        df_order = self.df_from_query(order_query)
        serial_numbers = df_order["Seriennummer"]
        flash_query = select(Flash).where(Flash.Seriennummer.in_(serial_numbers))
        df_flash = self.df_from_query(flash_query)
        merged_df = df_order.merge(df_flash, how="left", on="Seriennummer")
        merged_df = merged_df.astype(str)

        return merged_df

    def get_panel_info(self, panel: str):
        order_query = select(Order).where(Order.Seriennummer.in_([panel]))
        df_order = self.df_from_query(order_query)
        flash_query = select(Flash).where(Flash.Seriennummer.in_([panel]))
        df_flash = self.df_from_query(flash_query)
        merged_df = df_order.merge(df_flash, how="outer", on="Seriennummer")
        merged_df = merged_df.astype(str)

        return merged_df
