import requests
from config import load_config

_cfg = load_config()

DT_URL = _cfg["dynatrace"]["tenant_url"]
DT_TOKEN = _cfg["dynatrace"]["api_token"]

def push_metric(metric: str, value: float, dimensions: dict):
    dims = ",".join(f"{k}={v}" for k, v in dimensions.items())
    payload = f"{metric},{dims} {value}"

    headers = {
        "Authorization": f"Api-Token {DT_TOKEN}",
        "Content-Type": "text/plain; charset=utf-8"
    }

    r = requests.post(
        f"{DT_URL}/api/v2/metrics/ingest",
        headers=headers,
        data=payload,
        timeout=5
    )

    if r.status_code != 202:
        print("Dynatrace error:", r.text)