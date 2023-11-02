"""Фільтрація чоловіків та жінок. Результат - два .txt файли, на кожному рядку юзернейм. (пробігати по словнику і
записувати у певний файл юзернейм залежно від вашого гендерного фільтра) male.txt та female.txt"""
import os
from telethon.sync import TelegramClient
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

        male_usernames: list = []  # Список для збереження чоловічих імен користувачів
        female_usernames: list = []  # Список для збереження жіночих імен користувачів

        for participant in participants:
            username: str = participant.username
            gender: str = participant.gender  # Передбачається, що у об'єкта 'participant' є атрибут 'gender', який вказує на стать (чоловіча, жіноча тощо)

            if gender == 'male':
                male_usernames.append(username)
            elif gender == 'female':
                female_usernames.append(username)

        # Запишіть чоловічі та жіночі імена користувачів у відповідні файли
        with open('male.txt', 'w', encoding='utf-8') as male_file:
            male_file.write('\n'.join(male_usernames))

        with open('female.txt', 'w', encoding='utf-8') as female_file:
            female_file.write('\n'.join(female_usernames))

        print('Інформація про чоловічих користувачів збережена у male.txt')
        print('Інформація про жіночих користувачів збережена у female.txt')

    except Exception as e:
        print(f'Під час виконання програми виникла помилка: {e}')
