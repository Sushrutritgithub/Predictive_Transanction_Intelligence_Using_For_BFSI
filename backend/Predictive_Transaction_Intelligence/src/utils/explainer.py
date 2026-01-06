import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

genai.configure(api_key = api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

def generate_risk_explanation(data, prob):
    reasons = []

    # LOW RISK
    if prob < 0.03:
        return "Transaction appears low risk based on normal usage patterns."

    # MEDIUM RISK
    if prob < 0.1:
        if data["amount"] > 10000:
            reasons.append("Higher than usual amount")
        if (data["sender_old_balance"] - data["sender_new_balance"]) / (data["sender_old_balance"] + 1) > 0.5:
            reasons.append("Significant balance reduction")
        if data["transaction_type"] in ["TRANSFER", "CASH_OUT"]:
            reasons.append("Risk-prone transaction type")

        return "Moderate risk detected: " + " | ".join(reasons) if reasons else "Moderate risk detected."

    # HIGH RISK
    if data["amount"] > 20000:
        reasons.append("Very large transaction amount")
    if (data["sender_old_balance"] - data["sender_new_balance"]) / (data["sender_old_balance"] + 1) > 0.7:
        reasons.append("Sharp balance drop")
    if data["transaction_type"] == "CASH_OUT":
        reasons.append("High-risk cash-out activity")

    reasons.append("High fraud probability assigned by model")

    return "High risk detected: " + " | ".join(reasons)



def generate_explanation(probability, data):
    # 1. Always get the rule-based explanation first
    rule_text = generate_risk_explanation(data, probability)
    print(f"Rule-based explanation: {rule_text}")
    llm_text = None  # Default to None
    
    # 2. Try to get Gemini explanation
    try:
        prompt = f"Explain this {probability:.2%} fraud risk in 2 to 3 sentences. Rules triggered: {rule_text}. Data: {data}"
        # Setting a short timeout so your API doesn't hang
        response = model.generate_content(prompt)
        print(f"Gemini response: {response.text}")
        llm_text = response.text
    except Exception as e:
        # If 429 (Rate Limit) or any error occurs, llm_text remains None
        print(f"Gemini exhausted or error: {e}")
        
    return {
        "llm_explanation": llm_text,
        "rule_explanation": rule_text
    }