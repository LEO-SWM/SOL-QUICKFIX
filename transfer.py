import io
import pandas as pd
from sqlalchemy import create_engine, MetaData, delete, Table
from starlette.responses import StreamingResponse


class Transfer:
    def __init__(
        self, allowed_file_types, db_name, flash_table_name, orders_table_name
    ):
        self.allowed_file_types = allowed_file_types
        self.flash_table_name = flash_table_name
        self.orders_table_name = orders_table_name
        self.engine = create_engine(db_name)

    def is_file_type_allowed(self, file_type):
        return file_type in self.allowed_file_types

    def import_infos(self, excel_file, table_name):
        # Read the Excel file
        df = pd.read_excel(excel_file)
        # Create a database connection
        metadata = MetaData()
        metadata.reflect(bind=self.engine)
        if table_name in metadata.tables:
            with self.engine.connect() as connection:
                to_delete = df["Seriennummer"]
                table = Table(table_name, metadata, autoload=True)
                delete_query = delete(table).where(table.c.Seriennummer.in_(to_delete))
                connection.execute(delete_query)
                connection.commit()
        # Write the data from the Excel file to a SQL database
        df.set_index("Seriennummer", inplace=True)
        df.to_sql(table_name, con=self.engine, if_exists="append", index=True)

    def import_flash_infos(self, excel_file):
        self.import_infos(excel_file, self.flash_table_name)

    def import_order_infos(self, excel_file):
        self.import_infos(excel_file, self.orders_table_name)

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
