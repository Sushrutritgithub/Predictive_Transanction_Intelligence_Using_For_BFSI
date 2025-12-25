def generate_risk_explanation(data, prob):
    # CASE 1: Model says LOW RISK
    if prob < 0.1:
        return (
            "Transaction is classified as low risk based on learned patterns, "
            "despite individual factors like amount or transaction type."
        )

    # CASE 2: Model says MEDIUM RISK
    reasons = []

    if data["amount"] > 10000:
        reasons.append("Transaction amount is higher than typical user behavior")

    if data["sender_old_balance"] - data["sender_new_balance"] > 0:
        reasons.append("Noticeable reduction in sender balance")

    if data["transaction_type"] in ["TRANSFER", "CASH_OUT"]:
        reasons.append("Transaction type is commonly associated with fraud cases")

    if prob > 0.8:
        reasons.append("Model confidence for fraud is very high")

    return " | ".join(reasons) if reasons else "Moderate risk detected based on combined factors"