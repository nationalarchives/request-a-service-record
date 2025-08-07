import requests
from flask import current_app


def create_payment(amount, description, reference, return_url):
    headers = {
        "Authorization": f"Bearer {current_app.config["GOV_UK_PAY_API_KEY"]}",
        "Content-Type": "application/json",
    }

    payload = {
        "amount": amount,
        "description": description,
        "reference": reference,  # TODO: Investigate the dynamic reference that other/current services use (TNA-xxxxx?)
        "return_url": return_url,
    }

    response = requests.post(
        current_app.config["GOV_UK_PAY_API_URL"], json=payload, headers=headers
    )

    try:
        response.raise_for_status()
    except requests.RequestException as e:
        current_app.logger.error(f"Error creating payment: {e}")
        return None

    return response.json()


def check_payment(payment_id):
    headers = {
        "Authorization": f"Bearer {current_app.config["GOV_UK_PAY_API_KEY"]}",
        "Content-Type": "application/json",
    }
    response = requests.get(
        current_app.config["GOV_UK_PAY_API_URL"] + f"/{payment_id}", headers=headers
    )
    response = response.json()
    if response.get("state").get("status") == "success":
        has_paid = True
    else:
        has_paid = False
    return has_paid
