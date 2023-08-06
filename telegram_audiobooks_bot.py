import os
import psycopg2
from telegram.ext import Updater, MessageHandler, Filters

# Функция для обработки новых сообщений в Telegram
def handle_message(update, context):
    message = update.message
    if message.audio and message.audio.mime_type == 'audio/mpeg':
        # Извлекаем необходимую информацию из сообщения
        file_id = message.audio.file_id
        book_title = message.audio.title
        author = message.audio.performer
        cover_image = message.audio.thumb

        # Сохраняем обложку в виде bytea
        cover_image_bytes = context.bot.get_file(cover_image).download_as_bytearray()

        # Подключаемся к базе данных PostgreSQL
        connection = psycopg2.connect(
            host="your_host",
            database="your_database",
            user="your_user",
            password="your_password"
        )

        # Вставляем информацию о книге в базу данных
        cursor = connection.cursor()
        cursor.execute("INSERT INTO books (file_id, book_title, author, cover_image) VALUES (%s, %s, %s, %s)",
                       (file_id, book_title, author, cover_image_bytes))
        connection.commit()

        # Закрываем соединение с базой данных
        cursor.close()
        connection.close()

# Создаем экземпляр бота Telegram
updater = Updater(token="your_bot_token", use_context=True)
dispatcher = updater.dispatcher

# Добавляем обработчик для новых сообщений
message_handler = MessageHandler(Filters.audio, handle_message)
dispatcher.add_handler(message_handler)

# Запускаем бота
updater.start_polling()
