# 🌐 Bulk DNS Editor for Cloudflare

A simple tool that uses the Cloudflare API to find and bulk-edit DNS records across all your zones. Great for quickly replacing IPs or updating records without digging through each domain manually. Built with Python and designed for speed and simplicity.

---

## 🧰 Features

- Search for DNS records by IP or name
- View and filter results across all zones
- Select records to update in bulk
- Replace values with a new IP or content
- Fast, local, and easy to use
- Designed for sysadmins, MSPs, and automation fans

---

## 🧪 How to Use

1. **Download** this repository to your system.
2. Make sure **Python** is installed.
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   python app.py
   ```
5. Open your browser and go to:
   ```
   http://127.0.0.1:5000
   ```

6. Paste in your **Cloudflare API key**.
7. Enter the **IP address** you want to search for.
8. Click **Search** — the app will scan all zones for matching records.
9. A table will appear where you can **bulk edit** records as needed.

---

## ⚠️ Note

This runs locally and is intended for internal use. Avoid exposing it directly to the internet unless properly secured.

---

## 📌 Coming Soon

- UI polish and advanced filtering
- Token scope validation
- CLI version
- Prebuilt Docker Container
