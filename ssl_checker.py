import socket
import ssl
import logging
from datetime import datetime, timezone
import requests
import time
from cryptography import x509
from cryptography.hazmat.backends import default_backend

# ==========================
# Config
# ==========================
#add your domains here

ENDPOINTS = [                
    "test.google.com",
    "test.sslshopper.com",
    "test.rahulahmed.com",
  
]

TELEGRAM_TOKEN = "6906383164:AAEoiR-PYoHgXuDn6NbAmYaSPosE38U9mbs"
TELEGRAM_CHAT_ID = "7138416664"

LOG_FILE = "ssl_checker.log"
ALERT_DAYS = [7, 3, 1]   # days before expiry

# ==========================
# Logging setup
# ==========================
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

# ==========================
# Telegram notify
# ==========================
def send_telegram(msg: str):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        r = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": msg})
        if r.status_code == 200:
            logging.info(f"Telegram alert sent: {msg}")
        else:
            logging.error(f"Telegram error {r.status_code}: {r.text}")
    except Exception as e:
        logging.error(f"Telegram send failed: {e}")

# ==========================
# SSL Expiry Checker
# ==========================
def get_ssl_expiry(hostname: str, port: int = 443, retries: int = 2):
    """Fetch SSL certificate expiry ignoring hostname mismatch"""
    for attempt in range(retries):
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False  # ignore hostname mismatch
            ctx.verify_mode = ssl.CERT_NONE  # don’t verify CN/SAN

            with socket.create_connection((hostname, port), timeout=10) as sock:
                with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                    der_cert = ssock.getpeercert(binary_form=True)
                    cert_obj = x509.load_der_x509_certificate(der_cert, default_backend())
                    expiry = cert_obj.not_valid_after_utc
                    return expiry
        except Exception as e:
            logging.error(f"SSL check failed for {hostname}: {e}")
            time.sleep(1)
    return None

# ==========================
# Main
# ==========================
def main():
    problems = []

    for ep in ENDPOINTS:
        expiry = get_ssl_expiry(ep)
        if not expiry:
            logging.warning(f"Could not get expiry for {ep}")
            continue

        now = datetime.now(timezone.utc)
        days_left = (expiry - now).days

        if days_left < 0:
            msg = f"❌ {ep}: certificate expired on {expiry.date()}"
            logging.error(msg)
            problems.append(msg)
        elif days_left in ALERT_DAYS:
            msg = f"⚠️ {ep}: certificate expiring in {days_left} days (on {expiry.date()})"
            logging.warning(msg)
            problems.append(msg)
        else:
            logging.info(f"Checked {ep}: expires {expiry.date()} ({days_left} days left)")

    # Send Telegram summary
    if problems:
        alert_msg = "🚨 SSL Alerts 🚨\n\n" + "\n".join(problems)
        send_telegram(alert_msg)
    else:
        send_telegram("✅ SSL check completed, no upcoming expiries today.")

if __name__ == "__main__":
    main()
