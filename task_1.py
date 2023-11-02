"""Використовуючи бібліотеку telethon підключитися через сесію до групи та забрати інформацію про учасників.
Записати все у формат json"""
from telethon.sync import TelegramClient
import json
import os
from const import API_ID, API_HASH, PHONE_NUMBER

with TelegramClient('session_name', API_ID, API_HASH) as client:
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(PHONE_NUMBER)
        confirmation_code: str = input('Введіть код підтвердження: ')
        client.sign_in(PHONE_NUMBER, confirmation_code)

    target_group_username: str = input('Будь ласка, введіть ім\'я користувача (username) групи: ')

    try:
        participants: list = client.get_participants(target_group_username)
        participants_info: dict = {}

        for participant in participants:
            username: str = participant.username
            name: str = participant.first_name
            last_name: str = participant.last_name
            participants_info[username] = {
                'name': name,
                'last_name': last_name
            }

        with open('participants_info.json', 'w', encoding='utf-8') as json_file:
            json.dump(participants_info, json_file, ensure_ascii=False, indent=4)

        print('Інформація про учасників збережена у participants_info.json')

    except Exception as e:  # type: Exception
        print(f'Під час виконання програми виникла помилка: {e}')
