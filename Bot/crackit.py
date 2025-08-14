import os
import platform
import subprocess
import tempfile
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("8268045018:AAEM2PzE2etmwBX5oBcv0jOzuflSTuFwO3I")  

# Detect Python command
if platform.system() == "Windows":
    PYTHON_CMD = ["py", "-3.12"]
else:
    PYTHON_CMD = ["python3"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hey! I’m CrackIt — send me Python code and I’ll run it for you.")

async def handle_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_code = update.message.text
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
            tmp.write(user_code.encode('utf-8'))
            tmp.flush()
            result = subprocess.run(
                PYTHON_CMD + [tmp.name],
                capture_output=True,
                text=True,
                timeout=5
            )
        output = result.stdout if result.stdout else result.stderr
        await update.message.reply_text(f"🖥 Output:\n{output}")
    except subprocess.TimeoutExpired:
        await update.message.reply_text("⏳ Your code took too long to run.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_code))
    app.run_polling()

if __name__ == "__main__":
    main()
