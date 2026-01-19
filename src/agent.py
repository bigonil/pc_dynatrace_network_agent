"""Network monitoring agent that probes targets and pushes metrics to Dynatrace."""

import time
import socket
from probes import (
    icmp_latency,
    icmp_packet_loss,
    icmp_jitter,
    tcp_connect_time,
    http_response_time,
    detect_zscaler_latency,
)
from dynatrace import push_metric
from config import load_config

HOST = socket.gethostname()
CFG = load_config()
INTERVAL = CFG["agent"]["interval"]

def run_icmp_probes(cfg):
    """Run ICMP probes and push metrics."""
    for t in cfg["agent"]["targets"]["icmp"]:
        lat = icmp_latency(t)
        loss = icmp_packet_loss(t)
        jitter = icmp_jitter(t)

        if lat is not None:
            push_metric("network.icmp.latency", lat, {"host": HOST, "target": t})

        if loss is not None:
            push_metric("network.packet_loss", loss, {"host": HOST, "target": t})

        if jitter is not None:
            push_metric("network.jitter", jitter, {"host": HOST, "target": t})


def run_tcp_probes(cfg):
    """Run TCP connect time probes and push metrics."""
    for t in cfg["agent"]["targets"]["tcp"]:
        tcp = tcp_connect_time(t["host"], t["port"])
        if tcp is not None:
            push_metric("network.tcp.connect_time", tcp,
                        {"host": HOST, "target": t["host"]})


def run_http_probes(cfg):
    """Run HTTP response time probes and push metrics."""
    for url in cfg["agent"]["targets"]["http"]:
        http = http_response_time(url)
        if http is not None:
            push_metric("network.http.response_time", http,
                        {"host": HOST, "url": url})


def run_zscaler_probes(cfg):
    """Run Zscaler latency detection probes and push metrics."""
    for url in cfg["agent"]["targets"]["zscaler_test"]:
        delta = detect_zscaler_latency(url)
        if delta is not None:
            push_metric("network.zscaler.latency_delta", delta,
                        {"host": HOST, "url": url})


def main():
    """Run network probes in an infinite loop at the configured interval."""
    while True:
        run_icmp_probes(CFG)
        run_tcp_probes(CFG)
        run_http_probes(CFG)
        run_zscaler_probes(CFG)

        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()