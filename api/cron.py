def do_GET(self):
    auth = self.headers.get("Authorization")
    # WAJIB validasi, kalau gak cron lo bisa di-spam orang
    if auth != f"Bearer {os.environ.get('CRON_SECRET')}":
        self.send_response(401)
        self.end_headers()
        self.wfile.write(b"unauthorized")
        return
    
    # ... lanjut logic cek jadwal MyQuran ...
