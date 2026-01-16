import os
import time
import json
import socket
import requests
from ping3 import ping

# Configurazione: segreti da file + fallback a variabili d'ambiente
DEFAULT_SECRETS_PATH = os.path.join(os.path.dirname(__file__), "secrets", "dynatrace.json")

def _load_dynatrace_secrets() -> tuple[str | None, str | None]:
    """Carica DT_TENANT_URL e DT_API_TOKEN da un file JSON esterno."""
    secrets_path = os.environ.get("DT_SECRETS_PATH", DEFAULT_SECRETS_PATH)
    try:
        if os.path.exists(secrets_path):
            with open(secrets_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("tenantUrl"), data.get("apiToken")
    except Exception as e:
        print(f"Errore nel caricamento dei segreti da '{secrets_path}': {e}")
    return None, None

# Fallback: variabili d'ambiente prevalgono sui segreti da file
_secrets_tenant_url, _secrets_api_token = _load_dynatrace_secrets()
DT_TENANT_URL = os.environ.get("DT_TENANT_URL", _secrets_tenant_url)
DT_API_TOKEN = os.environ.get("DT_API_TOKEN", _secrets_api_token)

# Opzioni
TARGETS = os.environ.get("TARGETS", "8.8.8.8,1.1.1.1").split(",")
TCP_PORT = int(os.environ.get("TCP_PORT", "443"))
INTERVAL_SECONDS = int(os.environ.get("INTERVAL_SECONDS", "60"))

HOST_ID = socket.gethostname()

def _headers():
    return {
        "Authorization": f"Api-Token {DT_API_TOKEN}",
        "Content-Type": "text/plain; charset=utf-8",
        "User-Agent": "pc_dynatrace_network_agent/1.0",
    }

def icmp_latency(target: str, timeout: float = 2.0) -> float | None:
    """Ritorna latenza ICMP in ms o None se non disponibile.
    Usa ping3 in modalità non privilegiata per compatibilità OS.
    """
    try:
        latency_ms = ping(target, timeout=timeout, unit="ms")
        if latency_ms is None:
            return None
        return float(latency_ms)
    except Exception:
        return None

def tcp_latency(target: str, port: int, timeout: float = 2.0) -> float | None:
    """Misura latenza di connessione TCP in ms o None se fallisce."""
    start = time.perf_counter()
    try:
        with socket.create_connection((target, port), timeout=timeout):
            pass
        return (time.perf_counter() - start) * 1000.0
    except Exception:
        return None

def push_metric(metric: str, value: float | None, target: str) -> None:
    if value is None:
        return

    payload = f"{metric},host={HOST_ID},target={target} {value}"

    try:
        r = requests.post(
            f"{DT_TENANT_URL}/api/v2/metrics/ingest",
            headers=_headers(),
            data=payload,
            timeout=5,
        )
        if r.status_code != 202:
            print("Errore ingest Dynatrace:", r.status_code, r.text[:200])
    except requests.RequestException as e:
        print("Richiesta Dynatrace fallita:", str(e))

def main():
    # Validazione configurazione obbligatoria
    if not DT_TENANT_URL or not DT_API_TOKEN:
        print("Mancano DT_TENANT_URL o DT_API_TOKEN. Configura i segreti nel file o via variabili d'ambiente.")
        print(f"Percorso predefinito segreti: {DEFAULT_SECRETS_PATH}")
        return

    targets = [t.strip() for t in TARGETS if t.strip()]

    while True:
        for t in targets:
            icmp = icmp_latency(t)
            tcp = tcp_latency(t, TCP_PORT)

            push_metric("custom.network.icmp.latency", icmp, t)
            push_metric("custom.network.tcp.latency", tcp, t)

        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
# -*- coding: utf-8 -*-