from fastapi import APIRouter
from src.database.mysql_connection import get_mysql_connection

router = APIRouter()

@router.get("/fraud-data")
def get_fraud_data():
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM transactions LIMIT 100;")
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return {"data": data}