from app.lib.models import ServiceRecordRequest, db
from flask import current_app


def get_service_record_request(payment_id: str) -> ServiceRecordRequest | None:
    record = None

    try:
        record = (
            db.session.query(ServiceRecordRequest)
            .filter_by(payment_id=payment_id)
            .first()
        )
    except Exception as e:
        current_app.logger.error(f"Error fetching service record request: {e}")

    if not record:
        raise ValueError(f"Service record not found for payment_id: {payment_id}")

    return record


def delete_service_record_request(record: ServiceRecordRequest) -> None:
    try:
        db.session.delete(record)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f"Error deleting service record request: {e}")
        db.session.rollback()
