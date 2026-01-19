import sys
import time

def run_agent():
    while True:
        collect_metrics()
        send_to_dynatrace()
        time.sleep(30)

if __name__ == "__main__":
    if "--service" in sys.argv:
        run_agent()
    else:
        print("This executable must be run as a Windows Service.")
        sys.exit(1)