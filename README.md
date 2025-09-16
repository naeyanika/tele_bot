# Audit QA Telegram Bot

Bot Telegram untuk membantu tim QA melakukan monitoring, pencarian data audit, dan administrasi audit cabang secara otomatis. Bot ini terintegrasi dengan Supabase sebagai database backend.

## 🚀 Fitur Utama

- **Login**: Autentikasi user menggunakan email dan password (akun OPTIMA).
- **Search**: Cari data audit berdasarkan keyword pada matriks temuan.
- **Audit Regular**: Cek status administrasi audit regular per cabang.
- **Audit Khusus**: Cek status administrasi audit khusus per cabang.
- **Monitoring**: Lihat status monitoring cabang (Belum, Memadai, Tidak Memadai, Reminder).
- **Logout**: Keluar dari akun bot.
- **Menu**: Tampilkan daftar perintah yang tersedia.

## 🛠️ Teknologi

- **Python 3.x**
- **python-telegram-bot** (v20+)
- **Supabase-py** (untuk koneksi database)
- **python-dotenv** (untuk environment variable)

## 📦 Instalasi

1. Clone repository:
    ```bash
    git clone https://github.com/username/audit-qa-telegram-bot.git
    cd audit-qa-telegram-bot
    ```

2. Install dependencies:
    ```bash
    pip install python-telegram-bot supabase python-dotenv
    ```

3. Buat file `.env` dan isi dengan:
    ```
    SUPABASE_URL=your_supabase_url
    SUPABASE_KEY=your_supabase_key
    TELEGRAM_TOKEN=your_telegram_bot_token
    ```

4. Jalankan bot:
    ```bash
    python main.py
    ```

## 📖 Cara Penggunaan

- Mulai dengan perintah `/login` lalu masukkan email dan password.
- Gunakan `/menu` untuk melihat daftar perintah.
- Contoh perintah:
    - `/search <keyword>`
    - `/audit_reg <branch_name>`
    - `/audit_khs <branch_name>`
    - `/monitoring <branch_name>`
    - `/logout`

## ⚠️ Catatan

- Pastikan sudah mendaftar dan memiliki akun di Supabase.
- Bot hanya bisa digunakan oleh user yang sudah login.

## 👨‍💻 Author

**[Nama Anda]**
- GitHub: [@username](https://github.com/username)
- Email: your.email@example.com

---

⭐ Jika bot ini bermanfaat, silakan beri star pada repository!
