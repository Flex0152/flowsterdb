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
        query = f"""
        SELECT * FROM tblEmployees WHERE SamAccountname like '%{samaccountname}%'
        """
        result = pd.read_sql(query, con)
        return result

