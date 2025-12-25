from src.database.mysql_connection import get_mysql_connection

def save_prediction(transaction_id, prob, pred, explanation, latency_ms):
    conn = get_mysql_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO predictions
    (transaction_id, fraud_probability, is_fraud, explanation, latency_ms)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(query, (transaction_id, prob, pred, explanation, latency_ms))
    conn.commit()

    cursor.close()
    conn.close()
