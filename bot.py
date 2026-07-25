import os
import discord
from discord.ext import commands
from google import genai

# Khởi tạo Gemini client (thay thế YOUR_GEMINI_API_KEY bằng API key của bạn)
client = genai.Client(api_key="AQ.Ab8RN6LvygwNOdUhFU1fHM1Ml9yYCz9z4l-RbcKETC7fVgGZpg")

# Cấu hình Discord Bot Intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot đã đăng nhập thành công với tên: {bot.user}")

@bot.event
async def on_message(message):
    # Tránh việc bot tự trả lời tin nhắn của chính nó
    if message.author == bot.user:
        return

    # Nếu bạn muốn bot chỉ trả lời khi được nhắc đến (@Bot) hoặc trong kênh chat riêng
    if bot.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
        # Lấy nội dung tin nhắn và loại bỏ phần @mention bot
        clean_content = message.content.replace(f"<@{bot.user.id}>", "").strip()
        
        if clean_content:
            async with message.channel.typing():
                try:
                    # Gọi Gemini API để tạo câu trả lời
                    response = client.models.generate_content(
                        model="gemini-3.5-flash",
                        contents=clean_content,
                    )
                    
                    # Gửi câu trả lời lên Discord
                    await message.reply(response.text)
                except Exception as e:
                    await message.reply(f"Đã có lỗi xảy ra: {e}")

    # Xử lý các lệnh khác nếu có
    await bot.process_commands(message)

# Chạy bot (thay thế YOUR_DISCORD_BOT_TOKEN bằng Token bot của bạn ở Bước 1)
bot.run("MTUzMDAyNTE5NzUzOTgxOTYyMQ.GVgiEu._xxepcrZH51vBpNYxjIvD1gjjqFFegaSdnGFQs")
