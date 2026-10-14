{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import os\
from telegram import Update\
from telegram.ext import Application\
import httpx\
from http.server import BaseHTTPRequestHandler\
import json\
\
BOT_TOKEN = os.environ.get("BOT_TOKEN")\
SECRET = os.environ.get("WEBHOOK_SECRET_TOKEN")\
\
# Validasi biar cuma Telegram yang bisa hit endpoint lo\
async def handle(update: Update):\
    chat_id = update.effective_chat.id\
    # Simpen chat_id ke Vercel KV / Postgres\
    # Untuk simpel tahap awal: pakai Vercel KV (Upstash Redis)\
    # await kv.sadd("users", chat_id)\
    await update.message.reply_text(\
        "Bot Azan aktif \uc0\u9989 \\nLokasi default: Jakarta\\nKamu bakal dapet pengingat H-5 menit & pas azan.\\n\\nWaktu: Imsak, Subuh, Syuruq, Dhuha (Syuruq+20m), Dzuhur, Ashar, Maghrib, Isya"\
    )\
\
class handler(BaseHTTPRequestHandler):\
    def do_POST(self):\
        # 1. CEK SECRET HEADER - ini security utama\
        secret_header = self.headers.get("X-Telegram-Bot-Api-Secret-Token")\
        if secret_header != SECRET:\
            self.send_response(403)\
            self.end_headers()\
            return\
\
        # 2. Proses update\
        content_len = int(self.headers.get('content-length', 0))\
        data = self.rfile.read(content_len)\
        # ... panggil Application bot ...\
\
        self.send_response(200)\
        self.end_headers()}