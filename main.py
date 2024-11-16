import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

# Я просто скопировал это из доков
# Дает добро на чтение сообщений, реакций, списка пользователей и истории сообщений
intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
intents.members = True
intents.message_content = True

load_dotenv()
DISCORD_TOKEN = os.getenv("BOT_TOKEN")

# Установка префикса для бота
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())


# Просто в консоль для теста
# Работает
@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name="🎁сбор подарков🎁")
    )
    print("Готов к труду и обороне!")


# Тестовая команда
# .hello
@bot.command()
async def hello(ctx):
    await ctx.send('Привет! Я твой супер-секретный Санта-*Дедушка*!')


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
        await ctx.send("*Дедушка* не знает, чего ты хочешь!")
    else:
        # Обработка других ошибок
        # Понять, бы зачем...
        raise error


# Пытаюсь в обработку реакций и их добавление
# .santa_preparing
@bot.command()
async def santa_preparing(ctx):
    # Запрашиваем у пользователя ID сообщения (можно получить через ЛКМ)
    await ctx.send("*Дедушке* нужен ID сообщения для начала!")

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
        await ctx.send("*Дедушка* добавил реакцию!")
    except discord.NotFound:
        await ctx.send("*Дедушка* не нашел такое сообщение!")
    # Спасибо, гпт за эту ошибку
    except discord.Forbidden:
        await ctx.send("*Дедушке* не разрешено добавлять реакции!")
    # И за эту тоже
    except discord.HTTPException:
        await ctx.send("*Произошла* ошибка при добавлении реакции!")

    # НУЖЕ ОБРАБОТЧИК УЖЕ ДОБАВЛЕННОЙ РЕАКЦИИ
    # Я НЕ ЗНАЮ, КАК


# Вывод списка тех, кто поставил реацию
# .santa_waiting
@bot.command()
async def santa_waiting(ctx):
    await ctx.send("Дедушке нужно ID сообщения для работы.")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit(
        )

    msg = await bot.wait_for('message', check=check, timeout=30.0)
    message_id = int(msg.content)  # Исправлено опечатку с `coontent`

    try:
        message = await ctx.channel.fetch_message(message_id)
        await ctx.send("*Дедушка* нашел сообщение! И видит...")

        # Проверка реакций на сообщении
        users_with_reactions = []
        for reaction in message.reactions:
            if str(reaction.emoji) == '🎄':  # Проверяем, что реакция - елочка
                # че за ошибка - не понимаю
                async for user in reaction.users():
                    # Надо запомнить, полезная штука
                    if not user.bot:  # Исключаем ботов из списка
                        users_with_reactions.append(user.name)

        if users_with_reactions:
            await ctx.send(
                f"Пользователи, которые поставили реакцию 🎄: {', '.join(users_with_reactions)}"
            )
        else:
            await ctx.send("Никто не поставил реакцию 🎄 на этом сообщении.")

    except discord.NotFound:
        await ctx.send("*Дедушка* не нашел такое сообщение!")
    except discord.Forbidden:
        await ctx.send("У *Дедушки* нет прав на чтение сообщений или реакции!")
    except discord.HTTPException:
        await ctx.send("Произошла ошибка.")


bot.run(DISCORD_TOKEN)
