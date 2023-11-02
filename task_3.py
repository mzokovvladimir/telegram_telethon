"""Написати скрипт, який приєднається до групи як публічної, так і приватної через сесію (бібліотека telethon),
ловити повідомлення від бота і в залежності від його типу (типу капчі) вирішувати завдання.
Скрипт має бути розширюваним і легко впроваджуваним (у стилі ОВП).
Потрібно написати клас, у якому викликатимуться методи залежно від типу завдання різних роботів. Також потрібно
створити БД, в яку будуть записуватися id ботів, щоб якщо такий бот використовується в інших групах, то через БД
можна було знати який метод використовувати, а якщо ні, то додати його.
Спробуйте реалізувати рішення капчі хоча б перших двох ботів, які представлені нижче.
https://t.me/pogromista
https://t.me/LampMining"""

import sqlite3
from telethon.sync import TelegramClient, events
from typing import Optional
from const import API_ID, API_HASH

# Підключення до бази даних
conn = sqlite3.connect('bots.db')
cur = conn.cursor()

# Створення таблиці для зберігання інформації про ботів
cur.execute('''CREATE TABLE IF NOT EXISTS bots
               (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, method TEXT)''')
conn.commit()

# Підключення до Telegram API
client: TelegramClient = TelegramClient('session_name', API_ID, API_HASH)
client.start()


class BotHandler:
    """
    Клас для обробки повідомлень від різних ботів.
    """

    def __init__(self, client: TelegramClient) -> None:
        """
        Ініціалізація об'єкту BotHandler.

        :param client: Об'єкт TelegramClient для взаємодії з Telegram API.
        """
        self.client: TelegramClient = client

    async def handle_captcha(self, event: events.NewMessage.Event) -> None:
        """
        Обробляє повідомлення з капчею.

        :param event: Подія NewMessage.Event, яка представляє вхідне повідомлення.
        """
        # Отримуємо текст повідомлення з капчею
        captcha_text = event.message.text

        # Реалізуємо обробку капчі - наприклад, виводимо текст капчі та чекаємо відповіді користувача
        await event.respond(f'Капча: {captcha_text}')
        # Тут можна додати логіку для очікування відповіді користувача та подальшу обробку введених даних

    async def handle_message(self, event: events.NewMessage.Event) -> None:
        """
        Обробляє звичайні повідомлення.

        :param event: Подія NewMessage.Event, яка представляє вхідне повідомлення.
        """
        # Отримуємо текст звичайного повідомлення
        message_text = event.message.text

        # Реалізуємо обробку звичайного повідомлення - наприклад, виводимо текст повідомлення
        await event.respond(f'Отримано повідомлення: {message_text}')
        # Тут можна додати додаткову логіку для обробки тексту повідомлення

    def register_bot(self, username: str, method: str) -> None:
        """
        Реєструє нового бота в базі даних.

        :param username: Ім'я користувача бота.
        :param method: Метод обробки повідомлень для бота ('captcha' або 'message').
        """
        cur.execute("INSERT INTO bots (username, method) VALUES (?, ?)", (username, method))
        conn.commit()

    def get_bot_method(self, username: str) -> Optional[str]:
        """
        Отримує метод обробки повідомлень для заданого бота з бази даних.

        :param username: Ім'я користувача бота.
        :return: Метод обробки повідомлень ('captcha' або 'message') або None, якщо бот не зареєстрований.
        """
        cur.execute("SELECT method FROM bots WHERE username=?", (username,))
        row = cur.fetchone()
        if row:
            return row[0]
        return None


# Створення об'єкту класу BotHandler
bot_handler: BotHandler = BotHandler(client)


@client.on(events.NewMessage(from_users=['pogromista_bot']))
async def handle_pogromista(event: events.NewMessage.Event) -> None:
    """
    Обробляє повідомлення від бота pogromista_bot.

    :param event: Подія NewMessage.Event, яка представляє вхідне повідомлення.
    """
    bot_method: Optional[str] = bot_handler.get_bot_method('pogromista_bot')
    if bot_method == 'captcha':
        await bot_handler.handle_captcha(event)
    else:
        await bot_handler.handle_message(event)


@client.on(events.NewMessage(from_users=['LampMining_bot']))
async def handle_lamp_mining(event: events.NewMessage.Event) -> None:
    """
    Обробляє повідомлення від бота LampMining_bot.

    :param event: Подія NewMessage.Event, яка представляє вхідне повідомлення.
    """
    bot_method: Optional[str] = bot_handler.get_bot_method('LampMining_bot')
    if bot_method == 'captcha':
        await bot_handler.handle_captcha(event)
    else:
        await bot_handler.handle_message(event)


# Запуск бота
client.run_until_disconnected()
