import time
import subprocess
import sys
import os

BASE_DIR = os.path.dirname(sys.executable)
AGENT_SCRIPT = os.path.join(BASE_DIR, "agent.py")

INTERVAL = 60

def main():
    while True:
        try:
            subprocess.run(
                [sys.executable, AGENT_SCRIPT],
                timeout=INTERVAL - 5,
                check=False
            )
        except Exception:
            pass
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()