from config import Base
from flask import current_app
import requests


def create_payment(amount, description, reference, return_url):
    headers = {
        "Authorization": f"Bearer {Base.GOV_UK_PAY_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "amount": amount,
        "description": description,
        "reference": reference,  # TODO: Investigate the dynamic reference that other/current services use (TNA-xxxxx?)
        "return_url": return_url,
    }

    response = requests.post(Base.GOV_UK_PAY_API_URL, json=payload, headers=headers)

    try:
        response.raise_for_status()
    except requests.RequestException as e:
        current_app.logger.error(f"Error creating payment: {e}")
        return None

    return response.json()
