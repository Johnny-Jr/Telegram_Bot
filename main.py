import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# Bot Token ကို ဒီမှာ ထည့်ပါ
TOKEN = '8616405370:AAFBU3d9fP130pRS2owCzPDRrJS4aLRTrpA'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Facebook ဒါမှမဟုတ် YouTube link ပေးရင် Video download ဆွဲပေးမယ်နော်။")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    status_msg = await update.message.reply_text("ခဏစောင့်ပေးပါ... Video ကို စစ်ဆေးနေပါတယ်။")

    # yt-dlp configuration
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_video.%(ext)s',
        'max_filesize': 50 * 1024 * 1024, # 50MB ထက်ကျော်ရင် မဆွဲခိုင်းဘူး (Telegram limit ကြောင့်)
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
        await status_msg.edit_text("ပို့ပေးနေပါပြီ...")
        
        # Video ပြန်ပို့ခြင်း
        with open(filename, 'rb') as video:
            await update.message.reply_video(video=video, caption=info.get('title'))
        
        # ပို့ပြီးရင် ဖိုင်ပြန်ဖျက်မယ်
        os.remove(filename)
        await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text(f"အမှားအယွင်းရှိသွားပါတယ်: {str(e)}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
