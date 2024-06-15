import requests
from decouple import config


BASE_URL = config("SALES_SERVICE_BASE_URL")
HEADERS = {"Authorization": config("SALES_SERVICE_API_KEY")}


def create_vehicle(request_body: dict) -> None:
    response = requests.post(
        f"{BASE_URL}/vehicles/",
        json=request_body,
        headers=HEADERS,
    )
    response.raise_for_status()


def update_vehicle(request_body: dict) -> None:
    vehicle_id = request_body["id"]
    response = requests.patch(
        f"{BASE_URL}/vehicles/{vehicle_id}/",
        json=request_body,
        headers=HEADERS,
    )
    response.raise_for_status()
