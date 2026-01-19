import time, socket, yaml
from probes import icmp_latency, icmp_packet_loss, icmp_jitter, tcp_connect_time, http_response_time, detect_zscaler_latency
from dynatrace import push_metric

HOST = socket.gethostname()

with open("config.yaml", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

DT_URL = cfg["dynatrace"]["tenant_url"]
DT_TOKEN = cfg["dynatrace"]["api_token"]
INTERVAL = cfg["agent"]["interval"]

def main():
    while True:
        # ICMP
        for t in cfg["agent"]["targets"]["icmp"]:
            lat = icmp_latency(t)
            loss = icmp_packet_loss(t)
            jitter = icmp_jitter(t)

            if lat is not None:
                push_metric(DT_URL, DT_TOKEN,
                    "network.icmp.latency", lat,
                    {"host": HOST, "target": t})

            if loss is not None:
                push_metric(DT_URL, DT_TOKEN,
                    "network.packet_loss", loss,
                    {"host": HOST, "target": t})

            if jitter is not None:
                push_metric(DT_URL, DT_TOKEN,
                    "network.jitter", jitter,
                    {"host": HOST, "target": t})

        # TCP
        for t in cfg["agent"]["targets"]["tcp"]:
            tcp = tcp_connect_time(t["host"], t["port"])
            if tcp:
                push_metric(DT_URL, DT_TOKEN,
                    "network.tcp.connect_time", tcp,
                    {"host": HOST, "target": t["host"]})

        # HTTP + Zscaler
        for url in cfg["agent"]["targets"]["http"]:
            http = http_response_time(url)
            if http:
                push_metric(DT_URL, DT_TOKEN,
                    "network.http.response_time", http,
                    {"host": HOST, "url": url})

        for url in cfg["agent"]["targets"]["zscaler_test"]:
            delta = detect_zscaler_latency(url)
            if delta:
                push_metric(DT_URL, DT_TOKEN,
                    "network.zscaler.latency_delta", delta,
                    {"host": HOST, "url": url})

        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()