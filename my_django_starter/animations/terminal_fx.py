import sys
import time

COLOR_CODES = {
    "RED": "\033[91m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "CYAN": "\033[96m",
    "RESET": "\033[0m"
}

def status_tag(text, symbol="🔔", color="YELLOW"):
    color_code = COLOR_CODES.get(color.upper(), "")
    reset_code = COLOR_CODES["RESET"]
    print(f"{color_code}[{symbol}] {text}{reset_code}", flush=True)

def type_writer(text, delay=0.01, color="RESET"):
    color_code = COLOR_CODES.get(color.upper(), "")
    reset_code = COLOR_CODES["RESET"]
    for char in text:
        sys.stdout.write(f"{color_code}{char}{reset_code}")
        sys.stdout.flush()
        time.sleep(delay)
    print()
