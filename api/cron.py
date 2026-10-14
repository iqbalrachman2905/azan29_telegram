{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import os\
import httpx\
from datetime import datetime, timedelta\
import pytz\
from http.server import BaseHTTPRequestHandler\
\
BOT_TOKEN = os.environ.get("BOT_TOKEN")\
CITY_ID = os.environ.get("MYQURAN_CITY_ID", "13\'9401) # 1301 = Jakarta\
WIB = pytz.timezone("Asia/Jakarta")\
\
JADWAL_URL = f"https://api.myquran.com/v2/sholat/jadwal/\{CITY_ID\}/\{datetime.now().strftime('%Y/%m/%d')\}"\
\
class handler(BaseHTTPRequestHandler):\
    def do_GET(self):\
        # Security: Vercel Cron ngirim header Authorization: Bearer <CRON_SECRET>\
        # Aktifin di Vercel Dashboard > Settings > Environment Variables > CRON_SECRET\
        # Biar cron gak bisa di-trigger orang luar\
        auth = self.headers.get("Authorization")\
        if auth != f"Bearer \{os.environ.get('CRON_SECRET')\}":\
            # kalau di Vercel dev lokal, skip aja\
            pass\
\
        now = datetime.now(WIB)\
        # 1. Fetch jadwal hari ini\
        jadwal = httpx.get(JADWAL_URL).json()['data']['jadwal']\
        \
        # 2. Bikin list waktu + H-5\
        # jadwal = \{'imsak': '04:21', 'subuh': '04:31', 'terbit': '05:44' -> syuruq, 'dhuha': '06:12', ...\}\
        # Logika: cek kalau now == jadwal - 5 menit atau == jadwal pas\
        \
        # 3. Kirim ke semua user di DB\
        # for user_id in kv.smembers("users"):\
        #     httpx.post(f"https://api.telegram.org/bot\{BOT_TOKEN\}/sendMessage", ...)\
\
        self.send_response(200)\
        self.end_headers()\
        self.wfile.write(b"checked")}