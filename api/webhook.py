from http.server import BaseHTTPRequestHandler
import json, os, httpx

BOT_TOKEN = os.environ.get("BOT_TOKEN")
SECRET = os.environ.get("WEBHOOK_SECRET_TOKEN")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # --- SECURITY CHECK 1: Telegram Secret ---
        telegram_secret = self.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if telegram_secret != SECRET:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"Forbidden")
            return

        try:
            length = int(self.headers.get('content-length', 0))
            body = self.rfile.read(length)
            data = json.loads(body)
            
            chat_id = data.get("message", {}).get("chat", {}).get("id")
            text = data.get("message", {}).get("text", "")

            if chat_id and "/start" in text:
                msg = (
                    "✅ Bot Azan Aktif\n\n"
                    "Lokasi: Kab. Bandung Barat (Pasirangin)\n"
                    "Jadwal: Imsak, Subuh, Syuruq, Dhuha, Dzuhur, Ashar, Maghrib, Isya\n"
                    "Reminder: H-5 menit & pas waktu azan\n\n"
                    "Bot ini jalan via Vercel + Github Actions"
                )
                httpx.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                           json={"chat_id": chat_id, "text": msg})

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        except Exception as e:
            print(e)
            self.send_response(200)
            self.end_headers()
