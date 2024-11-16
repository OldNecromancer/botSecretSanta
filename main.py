import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
intents.members = True
intents.message_content = True

load_dotenv()
DISCORD_TOKEN = os.getenv("BOT_TOKEN")

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())


# Просто в консоль для теста
@bot.event
async def on_ready():
    print("Готов к труду и обороне!")


# Тестовая команда
# .hello
@bot.command()
async def hello(ctx):
    await ctx.send('Привет! Я твой супер-секретный Санта!')


# Отображаем список всех доступных команд
# .hello, .help, ...
@bot.command()
async def help_me(ctx):
    commands_list = """
    Дедушка использует "." для обращения!
    Список команд:
    • hello: *Дедушка* скажет тебе "привет".
    • help_me: Нужна помощь? *Дедушка* поможет!
    """
    await ctx.send(commands_list)


# Обработчик ошибочных ситуаций
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Дедушка не знает, чего ты хочешь!")
    else:
        # Обработка других ошибок
        # Понять, бы зачем...
        raise error


bot.run(DISCORD_TOKEN)
