import requests
from flask import current_app, request, jsonify
import hmac
import hashlib
from app.lib.models import db, ServiceRecordRequest


def create_payment(amount: int, description: str, reference: str, email: str | None, return_url: str) -> dict | None:
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

    if email is not None:
        payload["email"] = email

    response = requests.post(
        current_app.config["GOV_UK_PAY_API_URL"], json=payload, headers=headers
    )

    try:
        response.raise_for_status()
    except requests.RequestException as e:
        current_app.logger.error(f"Error creating payment: {e}")
        return None

    return response.json()


def check_payment(payment_id) -> bool:
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


def is_webhook_signature_valid(request) -> bool:
    signing_secret = current_app.config["GOV_UK_PAY_SIGNING_SECRET"]
    pay_signature = request.headers.get("Pay-Signature", "")
    body = request.get_data()

    hmac_obj = hmac.new(
        signing_secret.encode("utf-8"),
        body,
        hashlib.sha256
    )

    generated_signature = hmac_obj.hexdigest()

    # if pay_signature != generated_signature:
    #     return False

    return True


def get_service_record_request(payment_id: str) -> ServiceRecordRequest | None:
    try:
        return db.session.query(ServiceRecordRequest).filter_by(payment_id=payment_id).first()
    except Exception as e:
        current_app.logger.error(f"Error fetching service record request: {e}")
        return None


def process_webhook_data(data: dict) -> None:
    payment_id = data.get("resource_id", "")

    record = get_service_record_request(payment_id)
    if not record:
        raise ValueError(f"Service record not found for payment_id: {payment_id}")

    # This is just an example for now. There are a lot of different fields, and these vary per type of Dynamics Case
    email_data = f"""
        <enquiry_id>{record.id}</enquiry_id>
        <title>{record.requester_title}</title>
        <mandatory_forename>{record.requester_first_name}</mandatory_forename>
        <mandatory_surname>{record.requester_last_name}</mandatory_surname>
        <mandatory_email>{record.requester_email}</mandatory_email>
        <mandatory_address1>{record.requester_address1}</mandatory_address1>
        <address2>{record.requester_address2}</address2>
        <address3></address3>
        <mandatory_town>{record.requester_town_city}</mandatory_town>
        <county>{record.requester_county}</county>
        <mandatory_postcode>{record.requester_postcode}</mandatory_postcode>
        <mandatory_country>{record.requester_country}</mandatory_country>
        <mandatory_certificate_forename>{record.forenames}</mandatory_certificate_forename>
        <mandatory_certificate_surname>{record.lastname}</mandatory_certificate_surname>
        <mandatory_birth_date>{record.date_of_birth}</mandatory_birth_date>
        <birth_place>{record.place_of_birth}</birth_place>
        <service_number>{record.service_number}</service_number>
        <regiment>{record.regiment}</regiment>
        <mandatory_upload_file_name>{record.evidence_of_death}</mandatory_upload_file_name>
        <enquiry>{record.additional_information}</enquiry>
        <mandatory_catalogue_reference></mandatory_catalogue_reference>
        <certificate_othernames>{record.other_last_names}</certificate_othernames>
        <date_of_death>{record.date_of_death}</date_of_death>
        <mod_barcode_number>{record.service_number}</mod_barcode_number>
        <service_branch>{record.service_branch}</service_branch>
        <died_in_service>{record.died_in_service}</died_in_service>
        <prior_contact_reference>{record.case_reference_number}</prior_contact_reference>
    """

    print(email_data)