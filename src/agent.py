"""
Network monitoring agent that collects network metrics and pushes them to Dynatrace.
"""
import sys
import os
import time
import socket

import yaml
from probes import (
    icmp_latency,
    icmp_packet_loss,
    icmp_jitter,
    tcp_connect_time,
    http_response_time,
    detect_zscaler_latency,
)
from dynatrace import push_metric


HOST = socket.gethostname()


def resource_path(relative_path):
    """
    Return the absolute path to a resource for development and frozen executables.
    """
    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)


CONFIG_PATH = resource_path("config.yaml")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

DT_URL = cfg["dynatrace"]["tenant_url"]
DT_TOKEN = cfg["dynatrace"]["api_token"]
INTERVAL = cfg["agent"]["interval"]

def push_icmp_metrics():
    """
    Collect and push ICMP metrics.
    """
    for t in cfg["agent"]["targets"]["icmp"]:
        lat = icmp_latency(t)
        loss = icmp_packet_loss(t)
        jitter = icmp_jitter(t)

        if lat is not None:
            push_metric(
                DT_URL,
                DT_TOKEN,
                "network.icmp.latency",
                lat,
                {
                    "host": HOST,
                    "target": t,
                },
            )

        if loss is not None:
            push_metric(
                DT_URL,
                DT_TOKEN,
                "network.packet_loss",
                loss,
                {
                    "host": HOST,
                    "target": t,
                },
            )

        if jitter is not None:
            push_metric(
                DT_URL,
                DT_TOKEN,
                "network.jitter",
                jitter,
                {
                    "host": HOST,
                    "target": t,
                },
            )


def push_tcp_metrics():
    """
    Collect and push TCP metrics.
    """
    for t in cfg["agent"]["targets"]["tcp"]:
        tcp = tcp_connect_time(t["host"], t["port"])
        if tcp:
            push_metric(
                DT_URL,
                DT_TOKEN,
                "network.tcp.connect_time",
                tcp,
                {
                    "host": HOST,
                    "target": t["host"],
                },
            )


def push_http_metrics():
    """
    Collect and push HTTP metrics.
    """
    for url in cfg["agent"]["targets"]["http"]:
        http = http_response_time(url)
        if http:
            push_metric(
                DT_URL,
                DT_TOKEN,
                "network.http.response_time",
                http,
                {
                    "host": HOST,
                    "url": url,
                },
            )


def push_zscaler_metrics():
    """
    Collect and push Zscaler latency delta metrics.
    """
    for url in cfg["agent"]["targets"]["zscaler_test"]:
        delta = detect_zscaler_latency(url)
        if delta:
            push_metric(
                DT_URL,
                DT_TOKEN,
                "network.zscaler.latency_delta",
                delta,
                {
                    "host": HOST,
                    "url": url,
                },
            )


def main():
    """
    Run the agent loop to collect and push metrics at the configured interval.
    """
    while True:
        push_icmp_metrics()
        push_tcp_metrics()
        push_http_metrics()
        push_zscaler_metrics()
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()