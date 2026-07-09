import os
import telebot
from moviepy.editor import VideoFileClip

# تم وضع التوكن الخاص ببوتك هنا بنجاح
BOT_TOKEN = "8205729075:AAGWZuliXPB9XZ9ZBX2jBmsHaKPGk4TgQk0"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أرسل لي أي فيديو وسأقوم بضغطه وتقليل حجمه لك. 🎬")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    input_filename = "input_video.mp4"
    output_filename = "compressed_video.mp4"
    
    try:
        bot.reply_to(message, "جاري تحميل الفيديو وبدء الضغط... انتظر قليلاً ⏳")
        
        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(input_filename, 'wb') as new_file:
            new_file.write(downloaded_file)
            
        clip = VideoFileClip(input_filename)
        clip.write_videofile(output_filename, bitrate="500k", codec="libx264")
        clip.close()
        
        with open(output_filename, 'rb') as video_to_send:
            bot.send_video(message.chat.id, video_to_send, caption="تم ضغط الفيديو بنجاح! ✅")
            
    except Exception as e:
        bot.reply_to(message, f"حدث خطأ: {str(e)}")
        
    finally:
        if os.path.exists(input_filename): os.remove(input_filename)
        if os.path.exists(output_filename): os.remove(output_filename)

bot.infinity_polling()
