import requests
import random
import json

STATUS_ENDPOINT = "http://localhost:8000/status"


def mock_status(n: int):
    service_id = [5, 6, 7, 8]
    for _ in range(n):
        for id in service_id:
            payload = {
                "id": id,
                "cpu_utilization": random.randint(10, 100),
                "memory_utilization": random.randint(10, 100),
            }

            requests.post(STATUS_ENDPOINT, json.dumps(payload))


def main():
    mock_status(10)


if __name__ == "__main__":
    main()
