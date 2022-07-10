import os
import telebot
import time
from ImagenarySoundscape import unload_photo, download_mp3
import glob

bot = telebot.TeleBot('5353195887:AAGsA3edSEEk1YlwQU16QRzMZ8iyh7IB9zI')
start_t = ''


@bot.message_handler(commands=['start'])
def table(message, flag=True, flag1=True):
    global start_t
    send_mess = ''
    me = ''
    mainButton = telebot.types.InlineKeyboardMarkup(row_width=2)
    if flag == True:
        send_mess = f"Выбери из галереи изображение или отправь стикер, также можно нажать на эту кнопку для отправки фото профиля"
        me = telebot.types.InlineKeyboardButton(text='Cliсk✨', callback_data='btn1')
    else:
        send_mess = f"  \nЧто отправишь?\n  "
        me = telebot.types.InlineKeyboardButton(text='Мое фото', callback_data='btn1')
    mainButton.add(me)
    if flag == True:
        bot.send_message(chat_id=-691837534, text=f' Bot start \nName: '
                                                  f'{message.from_user.first_name} '
                                                  f'{message.from_user.last_name}\nid: @{message.from_user.id}')
    start_t = bot.send_message(message.chat.id, send_mess, reply_markup=mainButton)


@bot.message_handler(commands=['clear'])
def clear_server(message):
    try:
        path1 = open(os.path.dirname(os.path.abspath(__file__)))
        path2 = open(os.path.dirname(os.path.abspath(__file__)))
    
        photos = os.listdir('photos')
        sounds = os.listdir('sounds')
        i = 0
        j = 0
        for photo in photos:
            os.remove(f'{path1}+{photo}')
            i += 1
        for sound in sounds:
            os.remove(f'{path2}+{sound}')
            j += 1
        msg91 = bot.send_message(message.chat.id, 'Процесс удаление файлов — 🌕')
        msg92 = bot.edit_message_text('Процесс удаление файлов — 🌖', 1943319957, msg91.id)
        msg93 = bot.edit_message_text('Процесс удаление файлов — 🌗', 1943319957, msg92.id)
        msg94 = bot.edit_message_text('Процесс удаление файлов — 🌘', 1943319957, msg93.id)
        msg95 = bot.edit_message_text('Процесс удаление файлов — 🌑', 1943319957, msg94.id)
        msg96 = bot.edit_message_text('Процесс удаление файлов — 🌒', 1943319957, msg95.id)
        msg97 = bot.edit_message_text('Процесс удаление файлов — 🌓', 1943319957, msg96.id)
        msg98 = bot.edit_message_text('Процесс удаление файлов — 🌔', 1943319957, msg97.id)
        msg99 = bot.edit_message_text(f'Все файлы удалены — ✅', 1943319957, msg98.id)
        time.sleep(25)
        bot.delete_message(1943319957,msg99.id)
    except Exception as eror:
        bot.send_message(1943319957,f'Ошибка: {eror}')
        bot.send_message(1943319957,f'Ошибка: {path1}')
        bot.send_message(1943319957,f'Ошибка: {path2}')


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    try:
        if call.data == 'btn1':
            photos = bot.get_user_profile_photos(call.from_user.id)
            msg = bot.send_photo(call.from_user.id, photos.photos[0][0].file_id)
            file_from_user(msg)
    except IndexError:
        msg = bot.send_message(call.from_user.id, 'Но у тебя нет фотографии в профиле')
        time.sleep(4)
        bot.delete_message(call.from_user.id, msg.message_id)


@bot.message_handler(content_types=['photo', 'sticker'])
def file_from_user(message):
    if message.content_type == 'photo':
        active = message
        bot.delete_message(message.chat.id, message.message_id)
        process(active, photo=True)
    if message.content_type == 'sticker':
        active = message
        bot.delete_message(message.chat.id, message.message_id)
        process(active, sticker=True)


def process(message, photo=False, sticker=False):
    global start_t
    fileID = ''
    msg1 = ''
    msg5241 = ''
    try:
        if photo == True:
            msg1 = bot.send_message(message.chat.id, 'Процесс действий:\n⛔ загружаю изображение')
            fileID = message.photo[-1].file_id
        elif sticker == True:
            if message.sticker.is_animated:
                msg1 = bot.send_message(message.chat.id, 'Процесс действий:\n⛔ загружаю анимированный стикер')
                time.sleep(2)
                msg2 = bot.edit_message_text('нет, я не смог 😔', message.chat.id, msg1.id)
                time.sleep(3)
                bot.delete_message(message.chat.id, msg2.message_id)
                return
            elif message.sticker.is_video:
                msg1 = bot.send_message(message.chat.id, 'Процесс действий:\n⛔ загружаю стикер из видео')
                time.sleep(2)
                msg2 = bot.edit_message_text('не получилось 😓', message.chat.id, msg1.id)
                time.sleep(4)
                bot.delete_message(message.chat.id, msg2.message_id)
                return
            elif message.sticker:
                msg1 = bot.send_message(message.chat.id, 'Процесс действий:\n⛔ загружаю стикер')
                fileID = message.sticker.file_id

        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(os.path.dirname(os.path.abspath(__file__)) + '/photos' + f'/{fileID}.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)
            unload_photo(fileID)
            msg2 = bot.edit_message_text('Процесс действий:\n⚠ выгружаю звук', message.chat.id, msg1.id)
            time.sleep(2)
            bot.edit_message_text('Процесс действий:\n✅ готово', message.chat.id, msg2.id)
            time.sleep(1)
            name = download_mp3()
            bot.delete_message(message.chat.id, msg2.message_id)


            msg63 = bot.send_photo(message.chat.id,
                                   photo=open(os.path.dirname(os.path.abspath(__file__)) + f'/photos/{fileID}.jpg', 'rb'))
            msg412 = bot.send_audio(message.chat.id, reply_to_message_id=msg63.id,
                                    audio=open(os.path.dirname(os.path.abspath(__file__)) + f'/sounds/{name}.mp3', 'rb'))
            bot.delete_message(message.chat.id, start_t.id)
            table(msg412, flag=False, flag1=False)
    except AttributeError:
        table(msg412, False, False)
    except Exception as eror:
        print(eror)


bot.polling(none_stop=True)
