import sqlalchemy as sa
from pathlib import Path
from sqlalchemy.engine import Engine
import pandas as pd


current_path = Path(__file__).parent
en = sa.create_engine(f"sqlite:///{current_path}/FlowsterDB.db")

def get_object_by_name(en: Engine, category: str, name: str) -> pd.DataFrame:
    with en.connect() as con:
        query = f"""
        SELECT * FROM tbl{category} WHERE {category} LIKE '%{name}%'
        """
        result = pd.read_sql(query, con)
        return result

def get_employee_by_samaccountname(en: Engine, samaccountname: str) -> pd.DataFrame:
    with en.connect() as con:
        query = sa.text(f"""
        SELECT * FROM tblEmployees WHERE SamAccountname like :name
        """)
        params = {'name': f"'%{samaccountname}%'"}
        try:
            result = pd.read_sql(query, con=con, params=params)
        except sa.exc.OperationalError as e:
            raise e
        return result


if __name__ == '__main__':
    print(get_employee_by_samaccountname(en, 'felix.weidemann'))

