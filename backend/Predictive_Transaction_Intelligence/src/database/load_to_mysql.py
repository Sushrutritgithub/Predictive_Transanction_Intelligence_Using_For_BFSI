import pandas as pd
from mysql_connection import get_mysql_connection

def load_csv_to_mysql(csv_path):
    df = pd.read_csv(csv_path)

    conn = get_mysql_connection()
    cursor = conn.cursor()

    # Create table with correct 11 columns
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            transaction_id VARCHAR(50),
            customer_id VARCHAR(50),
            kyc_verified VARCHAR(10),
            account_age_days INT,
            transaction_amount DOUBLE,
            channel VARCHAR(50),
            timestamp DATETIME,
            is_fraud INT,
            hour INT,
            day_of_week VARCHAR(20),
            is_high_value INT
        );
    """)

    # Prepare insert query with EXACT 11 CSV columns
    insert_query = """
        INSERT INTO transactions
        (transaction_id, customer_id, kyc_verified, account_age_days,
         transaction_amount, channel, timestamp, is_fraud, hour,
         day_of_week, is_high_value)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Insert each row
    for _, row in df.iterrows():
        cursor.execute(insert_query, tuple(row))

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    load_csv_to_mysql("data/processed/Fraudulent2_processed.csv")
