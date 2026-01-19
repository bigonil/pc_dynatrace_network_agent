"""Dynatrace metrics ingestion helper functions."""
import requests
import yaml
from agent import resource_path   # oppure duplica la funzione

CONFIG_PATH = resource_path("config.yaml")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

def push_metric(tenant_url, token, metric, value, dimensions):
    """Push a single metric to Dynatrace via the v2 ingest API.

    Parameters:
        tenant_url (str): The Dynatrace base URL (e.g., https://{tenant}.live.dynatrace.com).
        token (str): Dynatrace API token with metrics.ingest scope.
        metric (str): Metric key.
        value (float|int|str): Metric value to ingest.
        dimensions (dict): Dictionary of dimension key/value pairs.
    """
    dims = ",".join(f"{k}={v}" for k, v in dimensions.items())
    payload = f"{metric},{dims} {value}"

    headers = {
        "Authorization": f"Api-Token {token}",
        "Content-Type": "text/plain; charset=utf-8"
    }

    r = requests.post(
        f"{tenant_url}/api/v2/metrics/ingest",
        headers=headers,
        data=payload,
        timeout=5
    )

    if r.status_code != 202:
        print("Dynatrace error:", r.text)