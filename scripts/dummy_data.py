import requests
import random
import json

STATUS_ENDPOINT = "http://localhost:8000/status"


def mock_status(n: int):
    service_id = [40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56]
    for _ in range(n):
        for id in service_id:
            payload = [
                {
                    "id": id,
                    "cpu_utilization": 0,
                    "memory_utilization": random.randint(1, 20),
                }
            ]

            requests.post(STATUS_ENDPOINT, json.dumps(payload))


def main():
    mock_status(10)


if __name__ == "__main__":
    main()
