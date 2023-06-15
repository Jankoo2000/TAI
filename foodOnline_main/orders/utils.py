import uuid
from datetime import datetime


def generate_order_id():
    now = datetime.now()
    unique_id = uuid.uuid4().hex[:5].upper()  # generate a unique hex string
    order_id = f"{now.strftime('%Y%m%d%H%M%S')}-{unique_id}"  # format the order ID as YYYYMMDDHHMMSS-UNIQUEID
    return order_id
