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


# Пытаюсь в обработку реакций и их добавление
# .santa_preparing
@bot.command()
async def santa_preparing(ctx):
    # Запрашиваем у пользователя ID сообщения (можно получить через ЛКМ)
    await ctx.send("Дедушке нужен ID сообщения для начала!")

    # Ожидание ответа от пользователя
    # проверяем, что автор и отправитель один
    # проверяем, что канал тот же
    # проверяем, что это символы (надеюсь, что это так)
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit(
        )

    # Ждём, пока пользователь отправит ID сообщения
    msg = await bot.wait_for('message', check=check, timeout=30.0)
    message_id = int(msg.content)

    # Пытаемся найти сообщение по ID
    try:
        message = await ctx.channel.fetch_message(message_id)
        await message.add_reaction('🎄')  # Добавляем реакцию "елочка"
        await ctx.send("Дедушка добавил реакцию!")
    except discord.NotFound:
        await ctx.send("Дедушка не нашел такое сообщение!")
    except discord.Forbidden:
        await ctx.send("Дедушке не разрешено добавлять реакции!")
    except discord.HTTPException:
        await ctx.send("Произошла ошибка при добавлении реакции!")


bot.run(DISCORD_TOKEN)
