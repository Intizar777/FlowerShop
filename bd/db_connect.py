from pymysql.cursors import DictCursor
import pymysql as pms

conn = pms.connect(host="localhost", user="root", password="", database="flower_shop", cursorclass=DictCursor)


def auth(login, passw, role):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT roles.role, users.* FROM users 
            JOIN roles ON roles.id = users.role_id
            WHERE email = %s and passw = %s and role = %s
            """, (login, passw, role)
        )
        res = cur.fetchone()
        return res

def get_data():
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM users WHERE role_id = 2
            """
        )
        res = cur.fetchall()
        return res

def update_client(name, surname, email, id):
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE users 
                SET name = %s, surname = %s, email = %s
                WHERE id = %s
                """, (name, surname, email, id)
            )
            conn.commit()
            return {
                "success": True,
                'message': "Клиент успешно обновлен"
            }
    except Exception:
        return {
                "success": False,
                'message': "Клиента не получилось обновить.."
        }


def delete_client(id):
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM users 
                WHERE id = %s
                """, (id,)
            )
            conn.commit()
            return {
                "success": True,
                'message': "Клиент успешно удален"
            }
    except Exception:
        return {
                "success": False,
                'message': "Клиента не получилось удалить.."
        }

def add_client(name, surname, email):
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                    INSERT INTO users(name, surname, email, role_id)
                    VALUES (%s, %s, %s, 2)
                """, (name, surname, email)
            )
            conn.commit()
            return {
                "success": True,
                'message': "Клиент успешно добавлен"
            }
    except Exception:
        return {
                "success": False,
                'message': "Клиента не получилось добавить.."
        }