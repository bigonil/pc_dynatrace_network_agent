import requests

def push_metric(tenant_url, token, metric, value, dimensions):
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