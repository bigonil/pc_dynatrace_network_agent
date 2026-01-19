import time
import socket
import requests
from ping3 import ping

def icmp_latency(target):
    rtt = ping(target, timeout=2)
    return rtt * 1000 if rtt else None

def icmp_packet_loss(target, count=5):
    lost = 0
    for _ in range(count):
        if ping(target, timeout=2) is None:
            lost += 1
    return (lost / count) * 100

def icmp_jitter(target, count=5):
    samples = []
    for _ in range(count):
        r = ping(target, timeout=2)
        if r:
            samples.append(r * 1000)
        time.sleep(0.2)
    if len(samples) < 2:
        return None
    return max(samples) - min(samples)

def tcp_connect_time(host, port):
    start = time.time()
    try:
        s = socket.create_connection((host, port), timeout=3)
        s.close()
        return (time.time() - start) * 1000
    except:
        return None

def http_response_time(url, proxies=None):
    start = time.time()
    try:
        requests.get(url, timeout=5, proxies=proxies)
        return (time.time() - start) * 1000
    except:
        return None

def detect_zscaler_latency(url):
    # test diretto (senza proxy)
    direct = http_response_time(url, proxies={"http": None, "https": None})

    # test con proxy di sistema (Zscaler)
    proxy = http_response_time(url)

    if direct and proxy:
        return proxy - direct
    return None