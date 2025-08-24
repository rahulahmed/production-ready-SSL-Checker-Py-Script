# SSL Monitoring Automation
## production-ready-SSL-Checker-Py-Script

Production-ready Python script to monitor SSL certificate expiry, send Telegram alerts, and provide daily acknowledgement notifications.  
This repository contains a production-ready Python script to monitor SSL certificates, send Telegram alerts, and log results.

---

## Features
- ✅ Daily SSL expiry checks for multiple endpoints
- ✅ Alerts 7, 3, and 1 day before expiry + on expiry
- ✅ Telegram notifications for real-time monitoring
- ✅ Daily acknowledgement message
- ✅ Logging for debugging and reliability

---

## Demo Endpoints
- example.com
- google.com
- github.com

---

## Files
- `ssl_checker.py` → Main Python script

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/ssl-monitoring-automation.git
cd ssl-monitoring-automation
```

### 2. Create virtual environment and activate
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure your Telegram bot credentials
Edit `ssl_checker.py` and add your `TELEGRAM_TOKEN` and `TELEGRAM_CHAT_ID`.

---

## Usage
```bash
python ssl_checker.py
```

---

## Cron Job (for daily checks)
Schedule the script to run daily at 11 AM:
```bash
0 11 * * * /full/path/to/venv/bin/python /full/path/to/ssl_checker.py
```

---

**Author:** Md Rahul Ahmed (DevOps Engineer)  
**Date:** 24 August 2025
