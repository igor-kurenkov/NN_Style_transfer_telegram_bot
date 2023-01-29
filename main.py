import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton
from aiogram.types import reply_keyboard

import asyncio

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import os
from copy import deepcopy
from urllib.parse import urljoin

from style_transfer import *
from gan import transfer
from config import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)  # comment this line if deploying to pythonanywhere

# uncomment next 2 lines if deploying to pythonanywhere
# proxy_url = 'http://proxy.server:3128'# uncomment these 2 lines if deploying to pythonanywhere
# bot = Bot(token=API_TOKEN, proxy=proxy_url)

dp = Dispatcher(bot)

photo_buffer = {}


class InfoAboutUser:
    def __init__(self):
        # default settigs
        self.settings = {'num_epochs': 50,
                         'imsize': 256}
        self.photos = []

    def set_default_settings(self):
        self.settings = {'num_epochs': 50,
                         'imsize': 256}


start_kb = InlineKeyboardMarkup()
start_kb.add(InlineKeyboardButton('Перенос любого стиля (NST)',
                                  callback_data='1_st'))
start_kb.add(InlineKeyboardButton('Стилизация под Ван Гога (GAN)',
                                  callback_data='vangogh'))
start_kb.add(InlineKeyboardButton('Стилизация под Моне (GAN)',
                                  callback_data='monet'))

settings1_kb = InlineKeyboardMarkup()
settings1_kb.add(InlineKeyboardButton('Стандартное качество',
                                      callback_data='default'))
settings1_kb.add(InlineKeyboardButton('Настроить',
                                      callback_data='custom'))
settings1_kb.add(InlineKeyboardButton('Назад',
                                      callback_data='main_menu'))

settings2_st_kb = InlineKeyboardMarkup()
settings2_st_kb.add(InlineKeyboardButton('Размер картинки',
                                         callback_data='imsize'))
settings2_st_kb.add(InlineKeyboardButton('Стилизовать с этими настройками',
                                         callback_data='next'))

settings2_gan_kb = InlineKeyboardMarkup()
settings2_gan_kb.add(InlineKeyboardButton('Размер картинки',
                                          callback_data='imsize'))
settings2_gan_kb.add(InlineKeyboardButton('Стилизовать с этими настройками',
                                          callback_data='next'))


# some of these settings isn`t available because of my GPU memory
imsize_kb = InlineKeyboardMarkup()

imsize_kb.add(InlineKeyboardButton('256 пикселей', callback_data='imsize_256'))
imsize_kb.add(InlineKeyboardButton('512 пикселей', callback_data='imsize_512'))
imsize_kb.add( InlineKeyboardButton('1024 пикселя', callback_data='imsize_1024'))
imsize_kb.add(InlineKeyboardButton('Стилизовать с этими настройками', callback_data='next'))

cancel_kb = InlineKeyboardMarkup()
cancel_kb.add(InlineKeyboardButton('Отмена', callback_data='main_menu'))

# warning text for EASY MODE
EASY_MODE_TEXT = "В данный момент бот работает в упрощенном режиме. Это означает, что для некоторых операций " + \
                 "боту может не хватить памяти. В такие моменты бот может просто не прислать ответ. " + \
                 "Также в данном режиме бот осуществляет NST весьма продолжительное время. " + \
                 "Для получения полного функционала бота " + \
                 "свяжитесь с создателем бота с целью перевести бота в нормальный режим работы.\n\n"


# start
@dp.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.send_message(DEBUG_ID, "Сообщение разработчику: пользователь присоединился, начинаю работать, босс")

    await bot.send_message(message.chat.id,
                           f"Привет, {message.from_user.first_name}!\nЯ бот-стилизатор. " +
                           "Я умею переносить стиль с картинки на картинку. " +
                           "Вот что я могу:", reply_markup=start_kb)

    photo_buffer[message.chat.id] = InfoAboutUser()


# help
@dp.message_handler(commands=['help'])
async def send_help(message):
    await bot.send_message(message.chat.id,
                           "Вот что я могу:", reply_markup=start_kb)


# main menu
@dp.callback_query_handler(lambda c: c.data == 'main_menu')
async def main_menu(callback_query):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text("Вот что я могу:")
    await callback_query.message.edit_reply_markup(reply_markup=start_kb)


# style transfer 1 style
@dp.callback_query_handler(lambda c: c.data == '1_st')
async def st_1_style(callback_query):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text("Выбери настройки для переноса стиля:")
    await callback_query.message.edit_reply_markup(reply_markup=settings1_kb)

    if callback_query.from_user.id not in photo_buffer:
        photo_buffer[callback_query.from_user.id] = InfoAboutUser()

    photo_buffer[callback_query.from_user.id].st_type = 1


# vangogh
@dp.callback_query_handler(lambda c: c.data == 'vangogh')
async def vangogh(callback_query):
    await bot.answer_callback_query(callback_query.id)

    await callback_query.message.edit_text(
        "Твоя картинка будет стилизована под стиль Ван Гога. " +
        "Выбери настройки для переноса стиля:")
    await callback_query.message.edit_reply_markup(reply_markup=settings1_kb)

    if callback_query.from_user.id not in photo_buffer:
        photo_buffer[callback_query.from_user.id] = InfoAboutUser()

    photo_buffer[callback_query.from_user.id].st_type = 'vangogh'


#monet
@dp.callback_query_handler(lambda c: c.data == 'monet')
async def winter2summer(callback_query):
    await bot.answer_callback_query(callback_query.id)

    await callback_query.message.edit_text(
        "Твоя картинка будет стилизована под стиль Моне. " +
        "Выбери настройки для переноса стиля:")
    await callback_query.message.edit_reply_markup(reply_markup=settings1_kb)

    if callback_query.from_user.id not in photo_buffer:
        photo_buffer[callback_query.from_user.id] = InfoAboutUser()

    photo_buffer[callback_query.from_user.id].st_type = 'monet'



# default settings
@dp.callback_query_handler(lambda c: c.data == 'default')
async def default_set(callback_query):
    extra_text = EASY_MODE_TEXT if MODE == 'EASY' else ''

    await bot.answer_callback_query(callback_query.id)

    if photo_buffer[callback_query.from_user.id].st_type == 1:
        await callback_query.message.edit_text(extra_text +
                                               "Пришли мне картинку, стиль с которой нужно перенести. " +
                                               "Для лучшего результата пришли изображение как документ." +
                                               "Во избежание поломки бота не стоит присылать файлы больше 1 Мб")

        photo_buffer[callback_query.from_user.id].need_photos = 2

    elif photo_buffer[callback_query.from_user.id].st_type == 'vangogh':
        await callback_query.message.edit_text(extra_text +
                                               "Пришли мне фотографию, и я добавлю на нее стиль Ван Гога. " +
                                               "Для лучшего результата пришли изображение как документ." +
                                               "Во избежание поломки бота не стоит присылать файлы больше 1 Мб")

        photo_buffer[callback_query.from_user.id].need_photos = 1

    elif photo_buffer[callback_query.from_user.id].st_type == 'monet':
        await callback_query.message.edit_text(extra_text +
                                               "Пришли мне фотографию, и я добавлю на нее стиль Моне. " +
                                               "Для лучшего результата пришли изображение как документ." +
                                               "Во избежание поломки бота не стоит присылать файлы больше 1 Мб")

        photo_buffer[callback_query.from_user.id].need_photos = 1


    await callback_query.message.edit_reply_markup(reply_markup=cancel_kb)

    photo_buffer[callback_query.from_user.id].set_default_settings()


# custom settings
@dp.callback_query_handler(lambda c: c.data == 'custom')
async def custom_set(callback_query):
    await bot.answer_callback_query(callback_query.id)

    await callback_query.message.edit_text(
        "Текущие настройки:" +
        "\nРазмер изображения: " + str(photo_buffer[callback_query.from_user.id].settings['imsize']) +
        " пикселей\n\nВыбери настройки для изменения:")
    await callback_query.message.edit_reply_markup(reply_markup=settings2_gan_kb)

# image size
@dp.callback_query_handler(lambda c: c.data == 'imsize')
async def set_num_epochs(callback_query):
    await bot.answer_callback_query(callback_query.id)

    await callback_query.message.edit_text(
        "Текущие настройки:" +
        "\nРазмер изображения: " + str(photo_buffer[callback_query.from_user.id].settings['imsize']) +
        " пикселей\n\nВыбери размер изображения:")

    await callback_query.message.edit_reply_markup(reply_markup=imsize_kb)


# load images
@dp.callback_query_handler(lambda c: c.data == 'next')
async def load_images(callback_query):
    extra_text = EASY_MODE_TEXT if MODE == 'EASY' else ''

    if photo_buffer[callback_query.from_user.id].st_type == 1:
        await callback_query.message.edit_text(extra_text +
                                               "Пришли мне картинку, стиль с которой нужно перенeсти. " +
                                               "Для лучшего результата пришли изображение как документ." +
                                               "Во избежание поломки бота не стоит присылать файлы больше 1 Мб")

        photo_buffer[callback_query.from_user.id].need_photos = 2

    elif photo_buffer[callback_query.from_user.id].st_type == 'vangogh':
        await callback_query.message.edit_text(extra_text +
                                               "Пришли мне изображение, и я добавлю в него стиль Ван Гога. " +
                                               "Для лучшего результата пришли изображение как документ." +
                                               "Во избежание поломки бота не стоит присылать файлы больше 1 Мб")

        photo_buffer[callback_query.from_user.id].need_photos = 1

    elif photo_buffer[callback_query.from_user.id].st_type == 'monet':
        await callback_query.message.edit_text(extra_text +
                                               "Пришли мне изображение, и я добавлю на нее стиль Моне. " +
                                               "Для лучшего результата пришли изображение как документ." +
                                               "Во избежание поломки бота не стоит присылать файлы больше 1 Мб")

        photo_buffer[callback_query.from_user.id].need_photos = 1

    await callback_query.message.edit_reply_markup(reply_markup=cancel_kb)


# changing image size
@dp.callback_query_handler(lambda c: c.data[:7] == 'imsize_')
async def change_imsize(callback_query):
    await bot.answer_callback_query(callback_query.id)
    photo_buffer[callback_query.from_user.id].settings['imsize'] = int(callback_query.data[7:])

    await callback_query.message.edit_text(
        "Текущие настройки:" +
        "\nРазмер изображения: " + str(photo_buffer[callback_query.from_user.id].settings['imsize']) +
        " пикселей\n\nВыбери настройки для изменения:")
    await callback_query.message.edit_reply_markup(reply_markup=imsize_kb)


# getting image
@dp.message_handler(content_types=['photo', 'document'])
async def get_image(message):
    if message.content_type == 'photo':
        img = message.photo[-1]

    else:
        img = message.document
        if img.mime_type[:5] != 'image':
            await bot.send_message(message.chat.id,
                                   "Загрузи, пожалуйста, файл в формате изображения.",
                                   reply_markup=start_kb)
            return

    file_info = await bot.get_file(img.file_id)
    photo = await bot.download_file(file_info.file_path)

    if message.chat.id not in photo_buffer:
        await bot.send_message(message.chat.id,
                               "Сначала выбери тип переноса стиля.", reply_markup=start_kb)
        return

    if not hasattr(photo_buffer[message.chat.id], 'need_photos'):
        await bot.send_message(message.chat.id,
                               "Сначала выбери настройки переноса стиля.", reply_markup=settings1_kb)
        return

    photo_buffer[message.chat.id].photos.append(photo)

    # style transfer
    if photo_buffer[message.chat.id].st_type == 1:
        if photo_buffer[message.chat.id].need_photos == 2:
            photo_buffer[message.chat.id].need_photos = 1

            await bot.send_message(message.chat.id,
                                   "Отлично, теперь пришли мне картинку, на которую нужно перенести этот стиль. " +
                                   "Для лучшего результата пришли изображение как документ." +
                                   "Во избежание поломки бота не стоит присылать файлы больше 1 Мб",
                                   reply_markup=cancel_kb)

        elif photo_buffer[message.chat.id].need_photos == 1:
            await bot.send_message(message.chat.id, "Начинаю обрабатывать...")

            # for debug
            log(photo_buffer[message.chat.id])

            try:
                output = await style_transfer(Simple_style_transfer, photo_buffer[message.chat.id],
                                              *photo_buffer[message.chat.id].photos)

                await bot.send_document(message.chat.id, deepcopy(output))
                await bot.send_photo(message.chat.id, output)

            except RuntimeError as err:
                if str(err)[:19] == 'CUDA out of memory.':
                    await bot.send_message(message.chat.id,
                                           "Произошла ошибка. У меня не хватает памяти, чтобы осуществить это действие."
                                           "Попробуй картинку поменьше")

                else:
                    if GET_DEBUG_INFO:
                        await bot.send_message(DEBUG_ID, "Произошла ошибка: " + str(err))
                        await bot.send_message(message.chat.id,
                                               "Произошла ошибка. Сообщение об ошибке отправлено создателю бота.")

                    else:
                        await bot.send_message(message.chat.id,
                                               "Произошла ошибка.")

            except Exception as err:
                if GET_DEBUG_INFO:
                    await bot.send_message(message.chat.id,
                                           "Произошла ошибка. Сообщение об ошибке отправлено создателю бота.")
                    await bot.send_message(DEBUG_ID, "Произошла ошибка: " + str(err))

                else:
                    await bot.send_message(message.chat.id,
                                           "Произошла ошибка.")

            await bot.send_message(message.chat.id,
                                   "Что будем делать дальше?", reply_markup=start_kb)

            del photo_buffer[message.chat.id]


    # GAN vangogh or monet
    elif photo_buffer[message.chat.id].st_type in ['vangogh', 'monet'] and \
            photo_buffer[message.chat.id].need_photos == 1:
        await bot.send_message(message.chat.id, "Начинаю обрабатывать...")

        # for debug
        log(photo_buffer[message.chat.id])

        try:
            output = gan_transfer(photo_buffer[message.chat.id],
                                  photo_buffer[message.chat.id].photos[0])

            await bot.send_document(message.chat.id, deepcopy(output))
            await bot.send_photo(message.chat.id, output)


        except RuntimeError as err:
            if str(err)[:19] == 'CUDA out of memory.':
                await bot.send_message(message.chat.id,
                                       "Произошла ошибка. У меня не хватает памяти, чтобы осуществить это действие. ")

            else:
                if GET_DEBUG_INFO:
                    await bot.send_message(DEBUG_ID, "Произошла ошибка: " + str(err))
                    await bot.send_message(message.chat.id,
                                           "Произошла ошибка. Сообщение об ошибке отправлено создателю бота.")

                else:
                    await bot.send_message(message.chat.id,
                                           "Произошла ошибка.")

        except Exception as err:
            await bot.send_message(message.chat.id,
                                   "Произошла ошибка. Сообщение об ошибке отправлено создателю бота.")

            if GET_DEBUG_INFO:
                await bot.send_message(DEBUG_ID, "Произошла ошибка: " + str(err))

        await bot.send_message(message.chat.id,
                               "Что будем делать дальше?", reply_markup=start_kb)

        del photo_buffer[message.chat.id]


# text error
@dp.message_handler(content_types=['text'])
async def get_text(message):
    # for debug
    '''
    for i in photo_buffer:
        print(photo_buffer[i].st_type)
        print(photo_buffer[i].need_photos)
        print()
    '''

    await bot.send_message(message.chat.id,
                           "Я тебя не понимаю. Вот что я могу:", reply_markup=start_kb)


async def on_startup(dispatcher):
    logging.warning('Starting...')

    await bot.set_webhook(webhook_url)


async def on_shutdown(dispatcher):
    logging.warning('Shutting down...')
    logging.warning('Bye!')


########################################################
# STYLE TRANSFER PART


async def style_transfer(st_class, user, *imgs):
    st = st_class(*imgs,
                  imsize=user.settings['imsize'],
                  num_steps=user.settings['num_epochs'],
                  style_weight=100000, content_weight=1)

    output = await st.transfer()

    return tensor2img(output)


def gan_transfer(user, img):
    output = transfer(img,
                      style=user.st_type,
                      imsize=user.settings['imsize'])

    return tensor2img(output.add(1).div(2))


def tensor2img(t):
    output = np.rollaxis(t.cpu().detach().numpy()[0], 0, 3)
    output = Image.fromarray(np.uint8(output * 255))

    bio = BytesIO()
    bio.name = 'result.jpeg'
    output.save(bio, 'JPEG')
    bio.seek(0)

    return bio


def log(user):
    if LOGGING:
        print()
        print('type:', user.st_type)
        if user.st_type == 1 or user.st_type == 2:
            print('settings:', user.settings)
            print('Epochs:')
        else:
            print('settings: imsize:', user.settings['imsize'])


def draw_img(img):
    plt.imshow(np.rollaxis(img.cpu().detach()[0].numpy(), 0, 3))
    plt.show()


def draw_photo(*photos):
    for photo in photos:
        img = np.array(Image.open(photo))
        plt.imshow(img)
        plt.show()


if __name__ == '__main__':
    if CONNECTION_TYPE == 'POLLING':
        executor.start_polling(dp, skip_updates=True)

    elif CONNECTION_TYPE == 'WEBHOOKS':
        # webhook setting
        webhook_path = f'/webhook/{API_TOKEN}'
        webhook_url = urljoin(WEBHOOK_HOST, webhook_path)

        # webserver setting
        webapp_host = '0.0.0.0'
        webapp_port = int(os.environ.get('PORT', WEBAPP_PORT))

        executor.start_webhook(
            dispatcher=dp,
            webhook_path=webhook_path,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=webapp_host,
            port=webapp_port)

    else:
        print("Invalid 'CONNECTION_TYPE'")
