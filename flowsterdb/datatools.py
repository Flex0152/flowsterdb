import sqlalchemy as sa
from pathlib import Path
from sqlalchemy.engine import Engine
import pandas as pd


current_path = Path(__file__).parent
en = sa.create_engine(f"sqlite:///{current_path}/FlowsterDB.db")

def get_object_by_name(en: Engine, category: str, name: str) -> pd.DataFrame:
    """Gibt es ein Ergebnis, so wird es als DataFrame zurückgegeben. Im Fehlerfall
    wird ein RuntimeError zum Aufrufer weiter gegeben. Passt auf alle Tabellen außer 
    tblEmployees.
    category - Kategorie des gesuchten Objekts
    Name - Bezeichnung des gesuchten Objekts"""
    try:
        with en.connect() as con:
            query = sa.text(f"""
            SELECT * FROM tbl{category} WHERE {category} LIKE :name""")
            params = {'name': f"%{name}%"}
            result = pd.read_sql(query, con=con, params=params)
        return result
    except sa.exc.SQLAlchemyError as e:
        raise RuntimeError("Ein Fehler in der SQL-Abfrage ist aufgetreten.") from e
    except sa.exc.OperationalError as e:
         raise RuntimeError("Fehler bei der Datenbankverbindung.") from e

def get_employee_by_samaccountname(en: Engine, samaccountname: str) -> pd.DataFrame:
        """Bietet die Möglichkeit nach ungefähren SamAccountNames zu suchen. 
        Wird etwas gefunden, wird es als DataFrame zurückgegeben. Im Fehlerfall
        wird eine Runtime Error zum Aufrufer weiter gegeben. 
        samaccountname - AD SamAccountName des gesuchten User"""
        try:
            with en.connect() as con:
                query = sa.text("""
                SELECT * FROM tblEmployees WHERE SamAccountname like :name""")
                params = {'name': f"%{samaccountname}%"}
                result = pd.read_sql(query, con=con, params=params)
            return result
        except sa.exc.OperationalError as e:
            raise RuntimeError("Fehler bei der Datenbankverbindung.") from e
        except sa.exc.SQLAlchemyError as e:
            raise RuntimeError("Ein Fehler in der SQL-Abfrage ist aufgetreten.") from e
        

if __name__ == '__main__':
    print(get_object_by_name(en, 'Distributor', 'potter'))

