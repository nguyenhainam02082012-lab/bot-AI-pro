import os
import discord
from discord.ext import commands
from google import genai

# Khởi tạo Gemini client bảo mật bằng biến môi trường trên Render
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Cấu hình Discord Bot Intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot đã đăng nhập thành công với tên: {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Kiểm tra nếu có tin nhắn thì gửi cho Gemini xử lý
    if message.content:
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=message.content,
            )
            await message.channel.send(response.text)
        except Exception as e:
            await message.channel.send(f"Đã xảy ra lỗi: {e}")

    await bot.process_commands(message)

# Chạy bot bằng token bảo mật trên Render
bot.run(os.environ.get("DISCORD_BOT_TOKEN"))
