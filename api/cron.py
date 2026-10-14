from http.server import BaseHTTPRequestHandler
import os, httpx
from datetime import datetime, timedelta
import pytz

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CRON_SECRET = os.environ.get("CRON_SECRET")
CITY_ID = os.environ.get("MYQURAN_CITY_ID", "1301")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")
WIB = pytz.timezone("Asia/Jakarta")

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # --- SECURITY CHECK 2: Cron Secret ---
        auth = self.headers.get("Authorization")
        if auth != f"Bearer {CRON_SECRET}":
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b"Unauthorized cron")
            return

        now = datetime.now(WIB)
        today_str = now.strftime("%Y/%m/%d")
        
        try:
            # Fetch jadwal Kemenag via MyQuran
            url = f"https://api.myquran.com/v2/sholat/jadwal/{CITY_ID}/{today_str}"
            res = httpx.get(url, timeout=10).json()
            jadwal = res["data"]["jadwal"] # {'imsak':'04:21','subuh':'04:31','terbit':'05:44',...}

            # Mapping: terbit = syuruq, dhuha = syuruq + 20 menit
            syuruq_time = jadwal["terbit"]
            dhuha_dt = datetime.strptime(syuruq_time, "%H:%M") + timedelta(minutes=20)
            jadwal["dhuha"] = dhuha_dt.strftime("%H:%M")
            jadwal["syuruq"] = syuruq_time

            # Daftar yang mau dicek
            cek_list = ["imsak", "subuh", "syuruq", "dhuha", "dzuhur", "ashar", "maghrib", "isya"]
            
            for nama in cek_list:
                jam_str = jadwal.get(nama)
                if not jam_str: continue
                
                jadwal_dt = WIB.localize(datetime.strptime(f"{today_str} {jam_str}", "%Y/%m/%d %H:%M"))
                
                # Hitung selisih menit
                diff = (jadwal_dt - now).total_seconds() / 60

                # 0 = pas waktu, 5 = H-5 menit (kasih toleransi +-2 menit karena cron jalan tiap 5 menit)
                pesan = None
                if -1 <= diff <= 1:
                    pesan = f"🔔 WAKTU {nama.upper()} {jam_str} WIB - حي على الصلاة"
                elif 4 <= diff <= 6:
                    pesan = f"⏰ 5 menit lagi {nama.upper()} jam {jam_str} WIB, siapin wudhu yuk"

                if pesan and ADMIN_CHAT_ID:
                    httpx.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                               json={"chat_id": ADMIN_CHAT_ID, "text": pesan})

            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"Checked at {now}".encode())

        except Exception as e:
            print(e)
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
