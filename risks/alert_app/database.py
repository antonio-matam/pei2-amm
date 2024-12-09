import psycopg2
import os


def get_db():
    return psycopg2.connect(
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            host=os.environ["DB_HOST"],
            port=os.environ["DB_PORT"],
            database=os.environ["DB_NAME"]
    )


def close_db(db: psycopg2.extensions.connection):
    db.close()


def insert_alert(**alert_description):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO alerts (risk_id, risk, city_name, level) "
                    "VALUES (%s, %s, %s, %s)",
                    (alert_description["risk_id"],
                     alert_description["risk"],
                     alert_description["city_name"],
                     alert_description["level"]))
        conn.commit()
        close_db(conn)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

