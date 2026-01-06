from fastapi import APIRouter
from src.database.mysql_connection import get_mysql_connection
from src.api.predict import router as predict_router
router = APIRouter()
router.include_router(predict_router)


@router.get("/fraud-data")
def get_fraud_data():
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM transactions LIMIT 100;")
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return {"data": data}

@router.get("/prediction-history")
def get_history(limit: int = 50):
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary = True)

    cursor.execute("""
        SELECT 
            transaction_id,
            fraud_probability,
            is_fraud,
            explanation,
            latency_ms,
            created_at
        FROM predictions
        ORDER BY created_at DESC
        LIMIT %s
    """, (limit,))

    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"count": len(data),"history": data}