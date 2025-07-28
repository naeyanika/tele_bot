from supabase import create_client, Client
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

ASK_EMAIL, ASK_PASSWORD = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Masukkan email untuk login:")
    return ASK_EMAIL

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['email'] = update.message.text
    await update.message.reply_text("Masukkan password:")
    return ASK_PASSWORD

async def get_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    email = context.user_data['email']
    password = update.message.text
    try:
        result = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if result.user:
            await update.message.reply_text(
                "Login berhasil!\n\n" +
                "klik /menu untuk melihat daftar perintah yang bisa kamu gunakan.\n" 
            )
        else:
            await update.message.reply_text("Login gagal. Cek email/password.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Login dibatalkan.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('login', start)],
        states={
            ASK_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
            ASK_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_password)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    app.add_handler(conv_handler)

    # Handler untuk /search
    app.add_handler(CommandHandler('search', search))

    # Handler untuk /logout
    app.add_handler(CommandHandler('logout', logout))

    # Handler untuk /menu
    app.add_handler(CommandHandler('menu', menu))

    # Handler untuk /audit_reg
    app.add_handler(CommandHandler('audit_reg', audit_reg))

    # Handler untuk /audit_khs
    app.add_handler(CommandHandler('audit_khs', audit_khs))

    # Handler untuk /monitoring
    app.add_handler(CommandHandler('monitoring', monitoring))
    app.run_polling()
async def monitoring(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Cek apakah user sudah login
    if 'email' not in context.user_data:
        await update.message.reply_text("Harap /login terlebih dahulu.")
        return
    if not context.args:
        # Tampilkan daftar branch_name berdasarkan status monitoring
        try:
            response = supabase.table("audit_regular").select("branch_name, monitoring").execute()
            data = response.data
            if not data:
                await update.message.reply_text("Tidak ada data monitoring ditemukan.")
                return
            belum = []
            tidak_memadai = []
            memadai = []
            reminder1 = []
            reminder2 = []
            for row in data:
                status = row.get("monitoring")
                branch = row.get("branch_name", "-")
                if status is None or status == "":
                    belum.append(branch)
                elif status == "Adequate":
                    memadai.append(branch)
                elif status == "Inadequate":
                    tidak_memadai.append(branch)
                elif status == "Reminder 1":
                    reminder1.append(branch)
                elif status == "Reminder 2":
                    reminder2.append(branch)
            msg = "Daftar Monitoring Cabang:\n"
            if belum:
                msg += "\n<b>Belum Mengirimkan:</b>\n" + "\n".join(f"- {b}" for b in belum) + "\n"
            if tidak_memadai:
                msg += "\n<b>Tidak Memadai:</b>\n" + "\n".join(f"- {b}" for b in tidak_memadai) + "\n"
            if memadai:
                msg += "\n<b>Memadai:</b>\n" + "\n".join(f"- {b}" for b in memadai) + "\n"
            if reminder1:
                msg += "\n<b>Reminder 1:</b>\n" + "\n".join(f"- {b}" for b in reminder1) + "\n"
            if reminder2:
                msg += "\n<b>Reminder 2:</b>\n" + "\n".join(f"- {b}" for b in reminder2) + "\n"
            await update.message.reply_text(msg, parse_mode="HTML")
        except Exception as e:
            await update.message.reply_text(f"Error: {e}")
        return
    branch_name = " ".join(context.args)
    try:
        response = supabase.table("audit_regular").select("branch_name, monitoring").ilike("branch_name", branch_name).limit(1).execute()
        data = response.data
        if not data:
            await update.message.reply_text(f"Data monitoring untuk cabang '{branch_name}' tidak ditemukan.")
            return
        row = data[0]
        status = row.get("monitoring")
        if status is None or status == "":
            status_str = "Belum Mengirimkan"
        elif status == "Adequate":
            status_str = "Memadai"
        elif status == "Inadequate":
            status_str = "Tidak Memadai"
        elif status == "Reminder 1":
            status_str = "Reminder 1"
        elif status == "Reminder 2":
            status_str = "Reminder 2"
        else:
            status_str = status
        await update.message.reply_text(f"Status monitoring cabang '{row.get('branch_name','-')}': {status_str}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('login', start)],
        states={
            ASK_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
            ASK_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_password)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    app.add_handler(conv_handler)

    # Handler untuk /search
    app.add_handler(CommandHandler('search', search))

    # Handler untuk /logout
    app.add_handler(CommandHandler('logout', logout))

    # Handler untuk /menu
    app.add_handler(CommandHandler('menu', menu))

    # Handler untuk /audit_reg
    app.add_handler(CommandHandler('audit_reg', audit_reg))

    # Handler untuk /audit_khs
    app.add_handler(CommandHandler('audit_khs', audit_khs))
    app.run_polling()
async def audit_khs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Cek apakah user sudah login
    if 'email' not in context.user_data:
        await update.message.reply_text("Harap /login terlebih dahulu.")
        return
    if not context.args:
        # Tampilkan daftar branch_name yang belum administrasi
        try:
            response = supabase.table("audit_fraud").select("*").execute()
            data = response.data
            if not data:
                await update.message.reply_text("Tidak ada data audit khusus ditemukan.")
                return
            exclude = {"id", "uuid", "branch_name", "region", "pic", "ogo", "created_at", "review"}
            branch_belum = []
            for row in data:
                for key, value in row.items():
                    if key in exclude:
                        continue
                    if isinstance(value, bool) and not value:
                        branch_belum.append(row.get("branch_name", "-"))
                        break
            if branch_belum:
                msg = "Cabang yang belum administrasi:\n" + "\n".join(f"- {b}" for b in branch_belum)
            else:
                msg = "Semua branch sudah administrasi."
            await update.message.reply_text(msg)
        except Exception as e:
            await update.message.reply_text(f"Error: {e}")
        return
    branch_keyword = " ".join(context.args)
    try:
        # Ambil semua data audit_fraud yang branch_name-nya mengandung keyword (case-insensitive)
        response = supabase.table("audit_fraud").select("*").ilike("branch_name", f"%{branch_keyword}%").execute()
        data = response.data
        if not data:
            await update.message.reply_text(f"Data audit untuk cabang yang mengandung '{branch_keyword}' tidak ditemukan.")
            return
        for row in data:
            branch = row.get("branch_name", "-")
            exclude = {"id", "uuid", "branch_name", "region", "pic", "ogo", "created_at", "review"}
            belum_selesai = []
            for key, value in row.items():
                if key in exclude:
                    continue
                if isinstance(value, bool) and not value:
                    belum_selesai.append(key)
            if belum_selesai:
                msg = f"[{branch}] Administrasi yang belum selesai:\n" + "\n".join(f"- {item}" for item in belum_selesai)
            else:
                msg = f"[{branch}] Administrasi lengkap!"
            await update.message.reply_text(msg)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('login', start)],
        states={
            ASK_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
            ASK_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_password)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    app.add_handler(conv_handler)

    # Handler untuk /search
    app.add_handler(CommandHandler('search', search))

    # Handler untuk /logout
    app.add_handler(CommandHandler('logout', logout))

    # Handler untuk /menu
    app.add_handler(CommandHandler('menu', menu))

    # Handler untuk /audit_reg
    app.add_handler(CommandHandler('audit_reg', audit_reg))
    app.run_polling()
async def audit_reg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Cek apakah user sudah login
    if 'email' not in context.user_data:
        await update.message.reply_text("Harap /login terlebih dahulu.")
        return
    if not context.args:
        # Tampilkan daftar branch_name yang belum administrasi (selain revised dapa)
        try:
            response = supabase.table("audit_regular").select("*").execute()
            data = response.data
            if not data:
                await update.message.reply_text("Tidak ada data audit regular ditemukan.")
                return
            exclude = {"id", "uuid", "branch_name", "region", "test", "audit_period_start", "audit_period_end", "pic", "dapa", "revised_dapa"}
            branch_belum = []
            for row in data:
                for key, value in row.items():
                    if key in exclude:
                        continue
                    if isinstance(value, bool) and not value:
                        branch_belum.append(row.get("branch_name", "-"))
                        break
            if branch_belum:
                msg = "Cabang yang belum administrasi:\n" + "\n".join(f"- {b}" for b in branch_belum)
            else:
                msg = "Semua cabang sudah administrasi."
            await update.message.reply_text(msg)
        except Exception as e:
            await update.message.reply_text(f"Error: {e}")
        return
    branch_name = " ".join(context.args)
    try:
        # Ambil data audit_regular untuk branch_name (case-insensitive)
        response = supabase.table("audit_regular").select("*").ilike("branch_name", branch_name).limit(1).execute()
        data = response.data
        if not data:
            await update.message.reply_text(f"Data audit untuk cabang '{branch_name}' tidak ditemukan.")
            return
        row = data[0]
        exclude = {"id", "uuid", "branch_name", "region", "test", "audit_period_start", "audit_period_end", "pic", "dapa", "revised_dapa"}
        belum_selesai = []
        for key, value in row.items():
            if key in exclude:
                continue
            if isinstance(value, bool) and not value:
                belum_selesai.append(key)
        if belum_selesai:
            msg = "Administrasi yang belum selesai:\n" + "\n".join(f"- {item}" for item in belum_selesai)
            await update.message.reply_text(msg)
        else:
            await update.message.reply_text("Administrasi lengkap!")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('login', start)],
        states={
            ASK_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
            ASK_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_password)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    app.add_handler(conv_handler)

    # Handler untuk /search
    app.add_handler(CommandHandler('search', search))

    # Handler untuk /logout
    app.add_handler(CommandHandler('logout', logout))

    # Handler untuk /menu
    app.add_handler(CommandHandler('menu', menu))
    app.run_polling()

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "Berikut perintah yang bisa kamu gunakan:\n"
        "1. /search <keyword> : Mencari data berdasarkan matriks yang direkap oleh QA.\n"
        "2. /logout : Keluar dari akun.\n"
        "3. /audit_reg <branch_name> : Melihat hasil administrasi auditor terkait cabang audit regular.\n"
        "4. /audit_khs <branch_name> : Melihat hasil administrasi auditor terkait cabang audit khusus.\n"
        "5. /monitoring <branch_name> : Melihat status monitoring cabang.\n"
        "6. /menu : Melihat daftar perintah.\n"
        "---lainnya menyusul ya :3"
    )
    await update.message.reply_text(msg)
async def logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Cek apakah user sudah login
    if 'email' not in context.user_data:
        await update.message.reply_text("Harap /login terlebih dahulu. Login menggunakan akun OPTIMA anda.")
        return
    # Hapus data login user dari context
    context.user_data.clear()
    await update.message.reply_text("Kamu sudah logout dari bot.")
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Cek apakah user sudah login
    if 'email' not in context.user_data:
        await update.message.reply_text("Harap /login terlebih dahulu.")
        return
    if not context.args:
        await update.message.reply_text("Gunakan: /search <keyword>")
        return
    keyword = " ".join(context.args)
    try:
        # Query ke tabel matriks, kolom kc_kr_kp sampai rekomendasi
        response = supabase.table("matriks").select(
            "kc_kr_kp, judul_temuan, kode_risk_issue, judul_risk_issue, kategori, penyebab, dampak, kelemahan, rekomendasi"
        ).or_(
            f"kc_kr_kp.ilike.%{keyword}%,judul_temuan.ilike.%{keyword}%,kode_risk_issue.ilike.%{keyword}%,judul_risk_issue.ilike.%{keyword}%,kategori.ilike.%{keyword}%,penyebab.ilike.%{keyword}%,dampak.ilike.%{keyword}%,kelemahan.ilike.%{keyword}%,rekomendasi.ilike.%{keyword}%"
        ).limit(5).execute()
        data = response.data
        if not data:
            await update.message.reply_text("Tidak ada hasil ditemukan.")
            return
        for row in data:
            msg = (
                f"KC/KR/KP: {row.get('kc_kr_kp','-')}\n"
                f"Judul Temuan: {row.get('judul_temuan','-')}\n"
                f"Kode Risk Issue: {row.get('kode_risk_issue','-')}\n"
                f"Judul Risk Issue: {row.get('judul_risk_issue','-')}\n"
                f"Kategori: {row.get('kategori','-')}\n"
                f"Penyebab: {row.get('penyebab','-')}\n"
                f"Dampak: {row.get('dampak','-')}\n"
                f"Kelemahan: {row.get('kelemahan','-')}\n"
                f"Rekomendasi: {row.get('rekomendasi','-')}\n"
                "----------------------"
            )
            await update.message.reply_text(msg)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
if __name__ == '__main__':
    main()