import os
import telebot
import time
from ImagenarySoundscape import unload_photo, download_mp3


bot = telebot.TeleBot('5353195887:AAENlgEJasJY8id9qrBQdgwFlqKzhPs1pog')
start_t = ''


@bot.message_handler(commands=['start'])
def table(message,flag=True):
    global start_t
    send_mess = f"Выбери из галереи изображение\nи отправь мне, или нажми на эту кнопку \nчтобы отправить фото профиля"
    mainButton = telebot.types.InlineKeyboardMarkup(row_width=2)
    me = telebot.types.InlineKeyboardButton(text='Cliсk?', callback_data='btn1')
    mainButton.add(me)
    if flag == True:
        bot.send_message(chat_id=-691837534, text=f' Bot start \nName: '
                                                  f'{message.from_user.first_name} '
                                                  f'{message.from_user.last_name}\nid: @{message.from_user.id}')
    start_t = bot.send_message(message.chat.id, send_mess, reply_markup=mainButton)


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    try:
        if call.data == 'btn1':
            photos = bot.get_user_profile_photos(call.from_user.id)
            msg = bot.send_photo(call.from_user.id, photos.photos[0][0].file_id)
            file_from_user(msg)
    except IndexError:
        msg = bot.send_message(call.from_user.id, 'У тебя нет фотографии в профиле')
        time.sleep(4)
        bot.delete_message(call.from_user.id, msg.message_id)


@bot.message_handler(content_types=['photo', 'sticker'])
def file_from_user(message):
    if message.content_type == 'photo':
        process(message,photo=True)
        bot.delete_message(message.chat.id, message.message_id)
    if message.content_type == 'sticker':
        process(message, sticker=True)
        bot.delete_message(message.chat.id, message.message_id)



def process(message, photo=False, sticker=False):
    global start_t
    fileID = ''
    msg1 = ''
    if photo == True:
        msg1 = bot.send_message(message.chat.id, 'загружаю изображение ??')
        fileID = message.photo[-1].file_id
    elif sticker == True:
        if message.sticker.is_animated:
            msg1 = bot.send_message(message.chat.id, 'загружаю анимированный стикер ??')
            time.sleep(2)
            msg2 = bot.edit_message_text('нет, я не смог ??', message.chat.id, msg1.id)
            time.sleep(3)
            bot.delete_message(message.chat.id, msg2.message_id)
            return
        else:
            msg1 = bot.send_message(message.chat.id, 'загружаю стикер ??')
            fileID = message.sticker.file_id

    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    #os.path.dirname(os.path.abspath(__file__)) + '/photos' + f'/{fileID}.jpg', 'wb'         <-это для моего сервера beget.com
    #os.path.dirname(os.path.abspath(__file__)) + '\\photos' + f'\\{fileID}.jpg', 'wb'       <- это для моего компа
    with open(os.path.dirname(os.path.abspath(__file__)) + '/photos' + f'/{fileID}.jpg', 'wb') as new_file:
        new_file.write(downloaded_file)
        unload_photo(fileID)
        msg2 = bot.edit_message_text('выгружаю звук ??', message.chat.id, msg1.id)
        time.sleep(2)
        bot.edit_message_text('готово ?', message.chat.id, msg2.id)
        time.sleep(1)
        name = download_mp3()
        bot.delete_message(message.chat.id, msg2.message_id)
        
        #это пути моего локального компа
        # msg63 = bot.send_photo(message.chat.id,caption='a',
        #                        photo=open(os.path.dirname(os.path.abspath(__file__)) + '\\photos' + f'\\{fileID}.jpg','rb'))
        # msg412 = bot.send_audio(message.chat.id,reply_to_message_id=msg63.id,
        #                      audio=open(os.path.dirname(os.path.abspath(__file__)) + f'\\sounds\\{name}.mp3', 'rb'))
        # bot.delete_message(message.chat.id, start_t.id)
        # table(msg412, flag=False)
        
        #это пути моего сервера beget.com
        msg633 = bot.send_photo(message.chat.id,
                               photo=open(os.path.dirname(os.path.abspath(__file__)) + f'/photos/{fileID}.jpg', 'rb'))
        msg = bot.send_audio(message.chat.id, reply_to_message_id=msg633.id,
                             audio=open(os.path.dirname(os.path.abspath(__file__)) + f'/sounds/{name}.mp3', 'rb'))
        msg86 = bot.send_photo(-691837534,
                               photo=open(os.path.dirname(os.path.abspath(__file__)) + f'/photos/{fileID}.jpg', 'rb'))

        bot.delete_message(message.chat.id, start_t.id)
        table(msg, flag=False)


bot.polling(none_stop=True)
