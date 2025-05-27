from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update
import logging
import os

TOKEN = os.environ.get("BOT_TOKEN")

REMINDER_MESSAGE = """Продержишься дольше?
➡ https://1wbfqv.life/v3/2451/rocket-queen?p=2u70

5к на карту тому, кто продержится дольше, скрины кидать сюда: 
https://t.me/+C1wUvbv1V7I1NWQy (в описании мой контакт)
"""

logging.basicConfig(level=logging.INFO)

def send_daily_message(context: CallbackContext):
    job = context.job
    with open('video.mp4', 'rb') as video_file:
        context.bot.send_video(
            chat_id=job.context,
            video=video_file,
            caption=REMINDER_MESSAGE
        )

def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    with open('video.mp4', 'rb') as video_file:
        update.message.reply_video(
            video=video_file,
            caption=REMINDER_MESSAGE
        )
    if 'job' in context.chat_data:
        context.chat_data['job'].schedule_removal()
    job = context.job_queue.run_repeating(send_daily_message, interval=86400, first=86400, context=chat_id)
    context.chat_data['job'] = job

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
