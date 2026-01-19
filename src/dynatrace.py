import requests
import yaml

CONFIG_PATH = "config.yaml"

with open(CONFIG_PATH) as f:
    cfg = yaml.safe_load(f)

DT_URL = cfg["dynatrace"]["tenant_url"]
DT_TOKEN = cfg["dynatrace"]["api_token"]

HEADERS = {
    "Authorization": f"Api-Token {DT_TOKEN}",
    "Content-Type": "text/plain; charset=utf-8"
}

def push_metric(metric, value, dimensions):
    dims = ",".join(f"{k}={v}" for k, v in dimensions.items())
    payload = f"{metric},{dims} {value}"

    r = requests.post(
        f"{DT_URL}/api/v2/metrics/ingest",
        headers=HEADERS,
        data=payload,
        timeout=5
    )

    if r.status_code != 202:
        print("Dynatrace error:", r.text)