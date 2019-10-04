import psycopg2
from src.Constants import Constants


class DB:
    dsn = f"host={Constants.DB_HOST} " \
          f"port={Constants.DB_PORT} " \
          f"dbname={Constants.DB} " \
          f"user={Constants.DB_USER} " \
          f"password={Constants.DB_PASS} "

    def get_response_message(self, mes_from):
        # "日付"が入力された時だけDBアクセス
        if mes_from == "日付":
            with psycopg2.connect(self.dsn) as conn:
                with conn.cursor(name="cs") as cur:
                    try:
                        sql_str = "SELECT TO_CHAR(CURRENT_DATE, 'yyyy/mm/dd');"
                        cur.execute(sql_str)
                        (mes,) = cur.fetchone()
                        return mes
                    except:
                        mes = "exception"
                        return mes

        # それ以外はオウム返し
        return mes_from
