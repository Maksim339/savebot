from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from pyrogram import Client
import time
from Social.YoutubeParser import title
import auth
from auth import delete_file
import os
from auth import check_url_database, insert_file_database
import datetime
from datetime import datetime
import shutil
import re, json
from lang import languages

# bot = Bot(token='')
bot = Bot(token='')

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

s_audio = 'soundcloud.com'
s_without_button = 'instagram.com', 'pinterest.ru', 'rt.pornhub.com', 'tiktok.com', \
                   'xvideos.com', 'twitter.com', 'facebook.com', 'pin.it', 'tiktok.com', 'vm.tiktok.com'


class Step(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()


@dp.message_handler(Command("start"))
async def start_handlers(message: types.Message):
    get_lang = await storage.get_data(chat=message.chat,
                                      user=message.chat.id)
    if get_lang == {}:
        await storage.update_data(chat=message.chat,
                                  user=message.chat.id,
                                  data={'lang': 'ru'})

    lang = await storage.get_data(chat=message.chat,
                                  user=message.chat.id)
    lang = list(lang.values())[0]
    await bot.send_message(message.chat.id, languages[lang]['welcome'], reply_markup=keyboard(lang))


@dp.message_handler(content_types=['text'])
async def text_handler(message: types.Message, state: FSMContext):
    get_lang = await storage.get_data(chat=message.chat,
                                      user=message.chat.id)
    if get_lang == {}:
        await storage.update_data(chat=message.chat,
                                  user=message.chat.id,
                                  data={'lang': 'ru'})

    lang = await storage.get_data(chat=message.chat,
                                  user=message.chat.id)
    lang = list(lang.values())[0]
    url = message.text
    url = url.replace('%2Fpl_cat_trends', '')
    url = re.sub(r'[?][t][=][\d][\d]', '', url)
    if url == '🆓 Поддерживаемые сервисы' or url == '🆓 Supported services':
        await bot.send_message(message.chat.id, languages[lang]['support_services'], parse_mode='HTML')
        auth.insert_statistics(user_id=message.chat.id,
                               date_add=message.date,
                               button_id='Supported services',
                               reaction_time='',
                               url='')
    elif url == '✉ Возникла проблема' or url == '✉ Need help':
        auth.insert_statistics(user_id=message.chat.id,
                               date_add=message.date,
                               button_id='Need help',
                               reaction_time='',
                               url='')
        await bot.send_message(message.chat.id, languages[lang]['need_help'])
        await Step.Q1.set()
    elif url == '💰 Поблагодарить' or url == '💰 Donate':
        await bot.send_message(message.chat.id, languages[lang]['choise_payment'],
                               reply_markup=payment_option(lang), parse_mode='HTML')
    elif url == '⚙ Настройки' or url == '⚙ Settings':
        await bot.send_message(message.chat.id, languages[lang]['choise_lang'], reply_markup=option(),
                               parse_mode='HTML')
    else:
        await bot.send_message(message.chat.id, languages[lang]['wait'])
        d_validation = auth.Control.domain_validation(url)
        if d_validation == 'accept':
            search = ''
            for i in range(0, len(s_without_button)):
                if s_without_button[i] in url:
                    search = 'True'

            if search == 'True':
                try:
                    await bot.send_message(message.chat.id, languages[lang]['loading'])
                    await two_step(message, url=message.text, state=FSMContext)
                except Exception as e:
                    await bot.send_message(, e)
                    # await bot.pin_chat_message(962567106, message.message_id, disable_notification=False)

            elif s_audio in url:
                await bot.send_message(message.chat.id, languages[lang]['loading'])
                # await bot.send_message(message.chat.id, 'Загрузка началась, ожидайте... ⏰')
                try:
                    readyFile = auth.Control.audio(url)
                    await types.ChatActions.upload_audio()
                    await bot.send_audio(message.chat.id, readyFile)
                    try:
                        await delete_file(readyFile)
                    except Exception as e:
                        print(e)

                except:
                    await bot.send_message(message.chat.id, languages[lang]['delete_playlist'])
                    # await bot.send_message(message.chat.id,
                    #                        'Вы пытались получить доступ к приватному треку. Возможно, плейлист был '
                    #                        'удален.')
            else:
                try:
                    await bot.send_photo(message.chat.id, auth.Control.preview(url),
                                         reply_markup=inline(url))
                    await Step.Q2.set()

                except Exception as e:
                    await bot.send_message(message.chat.id, title(url), reply_markup=inline(url))
                    await Step.Q2.set()

        elif d_validation == 'no_service':
            await bot.send_message(message.chat.id, languages[lang]['no_service'], parse_mode='HTML')
            # await bot.send_message(message.chat.id, 'Бот не смог обработать ссылку. '
            #                                         'Ссылка должна выглядеть вот так:\n\n'
            #                                         'https://www.instagram.com/p/CFByC0Qpm4/\n'
            #                                         'https://www.youtube.com/watch?v=xP5-iIeKXE\n'
            #                                         'https://www.pinterest.ru/pin/53944686161543638/',
            #                        parse_mode='HTML')


@dp.message_handler(state=Step.Q3)
async def two_step(message, url, state: FSMContext):

    """
    Для теста получение консольных команд.

    """
    # os.system('source /var/www/savebot/venv/bin/activate && which youtube-dl > /var/www/savebot/test1.txt')
    # os.system('sudo youtube-dl -U')
    # os.system('youtube-dl --version > /var/www/savebot/test1.txt')
    # os.chmod('/var/www/savebot/test1.txt', mode=0o777)
    # with open('/var/www/savebot/test1.txt') as file:
    #     await bot.send_document(962567106, file)
    lang = await storage.get_data(chat=message.chat,
                                  user=message.chat.id)
    lang = list(lang.values())[0]
    file_checker = check_url_database(url)
    try:
        if file_checker is not None:
            await bot.send_video(message.chat.id, file_checker)
            await state.finish()
        else:
            # FOR TEST
            # try:
            #     file = await auth.Control.media_reference(url)
            # except Exception as e:
            #     await bot.send_message(962567106, e)
            file = await auth.Control.media_reference(url)
            regex_url = file.__str__()

            data = {
                'mp4': bot.send_video,
                'jpg': bot.send_photo,
                'aiogram.types': bot.send_media_group,
                'mp3': bot.send_audio
            }
            if 'sizer' in regex_url:
                await bot.send_message(, 'SIZER?!')
                uniq_id = message.chat.id
                api_id =
                api_hash = ''
                readyFile = str(regex_url).replace("('sizer', <_io.BufferedReader name='", '').replace("'>)", '')
                async with Client("session_client_api_telegram", api_id, api_hash) as app:
                    large_file = await app.send_video("@media_localbot", readyFile,
                                                      width=1280, height=720)

                await bot.send_video(uniq_id, large_file.video.file_id, width=1280, height=720)
                await delete_file(readyFile)
                insert_file_database(url, file_id=large_file.video.file_id)
                end_cycle = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                datetime_object = datetime.strptime(end_cycle, '%Y-%m-%d %H:%M:%S')
                reaction_time = datetime_object - message.date
                await auth.insert_statistics(user_id=message.chat.id,
                                             date_add=message.date,
                                             button_id='',
                                             reaction_time=reaction_time,
                                             url=url)
                try:
                    await state.finish()
                except Exception as e:
                    await bot.send_message(, e)
            elif 'rework_service' in regex_url:
                await bot.send_message(message.chat.id, languages[lang]['rework_service'])
                # await bot.send_message(message.chat.id, 'К сожалению сервис временно недоступен, попробуйте позже')
                await state.finish()
            elif 'tt_video' in regex_url:
                os.system('cd /var/www/savebot/ && du -sh * > /var/www/savebot/test1.txt')
                # os.system('ls -lh /var/www/savebot/ > /var/www/savebot/test1.txt')
                os.chmod('/var/www/savebot/test1.txt', mode=0o777)
                with open('/var/www/savebot/test1.txt') as file:
                    await bot.send_document(, file)
                uniq_id = message.chat.id
                api_id = 8466768
                api_hash = 'c41bcc9f59abf65129750ff42be437d1'
                client_api = auth.client_api()
                async with Client("session_client_api_telegram", api_id, api_hash) as app:
                    large_file = await app.send_message("@ttsavebot", url)
                    time.sleep(4)
                    chat_history = await app.get_history(large_file.chat.id)
                    file = '/var/www/savebot/content/' + chat_history[1].video.file_id + '.mp4'
                    await app.download_media(chat_history[1].video.file_id,
                                             file_name=file)
                    file = open(file, 'rb')
                    ready_file = await app.send_video('@media_localbot', file, width=1280, height=720)
                await bot.send_video(uniq_id, ready_file.video.file_id)
                end_cycle = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                datetime_object = datetime.strptime(end_cycle, '%Y-%m-%d %H:%M:%S')
                reaction_time = datetime_object - message.date
                await auth.insert_statistics(user_id=message.chat.id,
                                             date_add=message.date,
                                             button_id='',
                                             reaction_time=reaction_time,
                                             url=url)
                await app.stop()
                try:
                    await delete_file(file)
                except Exception as e:
                    print(e)
                try:
                    await state.finish()
                except Exception as e:
                    await bot.send_message(, e)

            elif 'aiogram.types' in str(type(file)):
                await bot.send_message(, 'AIOGRAM?!')
                try:
                    await data['aiogram.types'](message.chat.id, file)
                except Exception as e:
                    video_in_array = json.loads(str(file))
                    for i in video_in_array:
                        media = types.MediaGroup()
                        if i['type'] == 'video':
                            media.attach_video(i['media'])
                        elif i['type'] == 'photo':
                            media.attach_photo(i['media'])
                        await data['aiogram.types'](message.chat.id, media)
                await bot.send_message(message.chat.id, "Успешно загружено!")
                end_cycle = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                datetime_object = datetime.strptime(end_cycle, '%Y-%m-%d %H:%M:%S')
                reaction_time = datetime_object - message.date
                await auth.insert_statistics(user_id=message.chat.id,
                                             date_add=message.date,
                                             button_id='',
                                             reaction_time=reaction_time,
                                             url=url)

                try:
                    await auth.delete_json_file(file[-1])
                except Exception as e:
                    print(e)
                try:
                    await delete_file(file)
                except Exception as e:
                    print(e)
                try:
                    await state.finish()
                except Exception as e:
                    await bot.send_message(962567106, e)
            elif 'mp4' in regex_url:
                await types.ChatActions.upload_video()
                try:
                    # os.system('du -sh /var/www/savebot/ > /var/www/savebot/test1.txt')
                    # os.chmod('/var/www/savebot/test1.txt', mode=0o777)
                    # with open('/var/www/savebot/test1.txt') as file:
                    #     await bot.send_document(962567106, file)
                    await bot.send_message(, 'TRY MP4')
                    save_file = await data['mp4'](message.chat.id, file[0], width=1280, height=720)
                    await delete_file(file)
                    insert_file_database(url, file_id=save_file.video.file_id)
                    end_cycle = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    datetime_object = datetime.strptime(end_cycle, '%Y-%m-%d %H:%M:%S')
                    reaction_time = datetime_object - message.date
                    await auth.insert_statistics(user_id=message.chat.id,
                                                 date_add=message.date,
                                                 button_id='',
                                                 reaction_time=reaction_time,
                                                 url=url)

                except Exception as e:
                    # os.system('cd /var/www/savebot/content && ls > /var/www/savebot/test1.txt')
                    # os.system('du -sh /var/www/savebot/ > /var/www/savebot/test1.txt')
                    # os.chmod('/var/www/savebot/test1.txt', mode=0o777)
                    # with open('/var/www/savebot/test1.txt') as file:
                    #     await bot.send_document(962567106, file)
                    await bot.send_message(, 'EXCEPT MP4')
                    if auth.check_base(url, user_id=message.chat.id, date_add=message.date) is None:
                        save_file = await data['mp4'](message.chat.id, file, width=1280, height=720)
                        try:
                            await delete_file(file)
                        except Exception as e:
                            await bot.send_message(, e)
                        insert_file_database(url, file_id=save_file.video.file_id)
                        end_cycle = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        datetime_object = datetime.strptime(end_cycle, '%Y-%m-%d %H:%M:%S')
                        reaction_time = datetime_object - message.date
                        await auth.insert_statistics(user_id=message.chat.id,
                                                     date_add=message.date,
                                                     button_id='',
                                                     reaction_time=reaction_time,
                                                     url=url)
                await bot.send_message(message.chat.id, languages[lang]['loaded_successfully'])
                # await bot.send_message(message.chat.id, "Видео успешно загружено!")

                try:
                    await auth.delete_json_file(file[-1])
                except Exception as e:
                    print(e)
                try:
                    await state.finish()
                except Exception as e:
                    await bot.send_message(, e)

            elif 'jpg' in regex_url:
                await bot.send_message(, 'JPG')
                await types.ChatActions.upload_photo()
                try:
                    await data['jpg'](message.chat.id, file[0])
                    end_cycle = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    datetime_object = datetime.strptime(end_cycle, '%Y-%m-%d %H:%M:%S')
                    reaction_time = datetime_object - message.date
                    await auth.insert_statistics(user_id=message.chat.id,
                                                 date_add=message.date,
                                                 button_id='',
                                                 reaction_time=reaction_time,
                                                 url=url)
                except Exception as e:
                    await data['jpg'](message.chat.id, file)
                    end_cycle = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    datetime_object = datetime.strptime(end_cycle, '%Y-%m-%d %H:%M:%S')
                    reaction_time = datetime_object - message.date
                    await auth.insert_statistics(user_id=message.chat.id,
                                                 date_add=message.date,
                                                 button_id='',
                                                 reaction_time=reaction_time,
                                                 url=url)
                # try:
                #     await data['jpg'](message.chat.id, file)
                #     end_cycle = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                #     datetime_object = datetime.strptime(end_cycle, '%Y-%m-%d %H:%M:%S')
                #     reaction_time = datetime_object - message.date
                #     await auth.insert_statistics(user_id=message.chat.id,
                #                                  date_add=message.date,
                #                                  button_id='',
                #                                  reaction_time=reaction_time,
                #                                  url=url)
                # except Exception as e:
                #     print(e)
                try:
                    await auth.delete_json_file(file[-1])
                except Exception as e:
                    print(e)
                try:
                    await state.finish()
                except Exception as e:
                    await bot.send_message(, e)

            elif 'mp3' in regex_url:
                await bot.send_message(, 'MP3333')
                await types.ChatActions.upload_audio()
                await data['mp3'](message.chat.id, file)
                await delete_file(file)
                await bot.send_message(message.chat.id, languages[lang]['audio_uploaded'])
                # await bot.send_message(message.chat.id, "Аудио успешно загружено!")
                end_cycle = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                datetime_object = datetime.strptime(end_cycle, '%Y-%m-%d %H:%M:%S')
                reaction_time = datetime_object - message.date
                await auth.insert_statistics(user_id=message.chat.id,
                                             date_add=message.date,
                                             button_id='',
                                             reaction_time=reaction_time,
                                             url=url)
                #
                await state.finish()

            elif 'None' in regex_url:
                await bot.send_message(message.chat.id, languages[lang]['None'])
                # await bot.send_message(message.chat.id, "Бот не поддерживает данный сервис 😔")
                try:
                    await state.finish()
                except Exception as e:
                    await bot.send_message(, e)

            elif 'privat_account' in regex_url:
                await bot.send_message(message.chat.id, languages[lang]['privat_account'])
                # await bot.send_message(message.chat.id,
                #                        "Бот не умеет скачивать с закрытых аккаунтов и защищенных авторским правом 😔")
                await bot.send_message(, str(os.access('/var/www/savebot/content/stories', os.X_OK)))
                try:
                    await state.finish()
                except Exception as e:
                    await bot.send_message(, e)

            elif 'large_data' in regex_url:
                await bot.send_message(message.chat.id, languages[lang]['large_data'])
                # await bot.send_message(message.chat.id, "Файл слишком большой для загрузки 😔")
                try:
                    await state.finish()
                except Exception as e:
                    await bot.send_message(, e)
            elif 'confusing_error' in regex_url:
                await bot.send_message(message.chat.id, languages[lang]['confusing_error'],
                                       parse_mode='HTML')
                # await bot.send_message(message.chat.id,
                #                        'Некорректная ссылка или данный сервис не поддерживается.\n'
                #                        'Убедитесь, что используете сервис из списка - \n<b> "Поддерживаемые сервисы" '
                #                        '</b>.\n '
                #                        'Также бот не может скачивать файлы приватных аккаунтов и защищенных авторским '
                #                        'правом.',
                #                        parse_mode='HTML')
                try:
                    await state.finish()
                except Exception as e:
                    await bot.send_message(, e)
            elif 'invalid_url' in regex_url:
                await bot.send_message(message.chat.id, languages[lang]['invalid_url'])
                # await bot.send_message(message.chat.id, 'Бот не смог обработать ссылку. '
                #                                         'Ссылка должна выглядеть вот так:\n\n'
                #                                         'https://www.instagram.com/p/CFByC0Qpm4/\n'
                #                                         'https://www.youtube.com/watch?v=xP5-iIeKXE\n'
                #                                         'https://vk.com/video-68005746_168759693')
                try:
                    await state.finish()
                except Exception as e:
                    await bot.send_message(, e)
            elif 'profile_guide' in regex_url:
                await bot.send_message(message.chat.id, languages[lang]['profile_guide'], parse_mode='HTML')
                # await bot.send_message(message.chat.id, 'Ссылка должна выглядеть вот так:\n\n'
                #                                         'https://www.instagram.com/p/CFByC0Qpm4/ - Пост\n'
                #                                         'https://www.instagram.com/tv/CBdVzV0A7Z/ - IGTV\n'
                #                                         'https://www.instagram.com/stories/username'
                #                                         '/2412407971635324364/ - '
                #                                         'Stories', parse_mode='HTML')
                try:
                    await state.finish()
                except Exception as e:
                    await bot.send_message(, e)
            elif 'highlights' in regex_url:
                await bot.send_message(message.chat.id, languages[lang]['highlights'], parse_mode='HTML')
                # await bot.send_message(message.chat.id, 'Бот не умеет скачивать Highlights\n'
                #                                         '<i>Недоступно из-за политики Instargram</i>',
                #                        parse_mode='HTML')
                try:
                    await state.finish()
                except Exception as e:
                    await bot.send_message(, e)
            else:
                os.system('cd /var/www/savebot/content/stories/ && ls > /var/www/savebot/test1.txt')
                os.chmod('/var/www/savebot/test1.txt', mode=0o777)
                with open('/var/www/savebot/test1.txt') as file:
                    await bot.send_document(, file)
                await bot.send_message(, regex_url)
                await bot.send_message(message.chat.id, languages[lang]['copyright'], parse_mode='HTML')
                await bot.send_message(, regex_url)
                try:
                    await state.finish()
                except Exception as e:
                    await bot.send_message(, e)
        try:
            await state.finish()
        except Exception as e:
            await bot.send_message(, e)

    except Exception as e:
        print(e)
        many_requests_CAPS = re.search('429 Too Many Requests', str(e))
        many_requests = re.search('429 too many requests', str(e))
        many_requests_full = re.search("b'ERROR: Unable to download webpage: HTTP Error 429: Too Many Requests", str(e))
        if many_requests or many_requests_CAPS or many_requests_full:
            await bot.send_message('@loggingMB', e)
        await bot.send_message(, e)
        await state.finish()


@dp.message_handler(state=Step.Q1)
async def feedback(message: types.Message, state: FSMContext):
    get_lang = await storage.get_data(chat=message.chat,
                                      user=message.chat.id)
    if get_lang == {}:
        await storage.update_data(chat=message.chat,
                                  user=message.chat.id,
                                  data={'lang': 'ru'})

    lang = await storage.get_data(chat=message.chat,
                                  user=message.chat.id)
    lang = list(lang.values())[0]
    chat_id = message.chat.id
    text = str(chat_id) + ' : ' + str(message.chat.username) + ' : ' + message.text + '\n'
    await bot.send_message(, text)
    await bot.send_message(message.chat.id, languages[lang]['need_help_ty'])
    await state.finish()


def keyboard(lang):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    print(lang)
    if lang == 'ru':
        button1 = types.KeyboardButton('🆓 Поддерживаемые сервисы')
        button2 = types.KeyboardButton('✉ Возникла проблема')
        button3 = types.KeyboardButton('💰 Поблагодарить')
        button4 = types.KeyboardButton('⚙ Настройки')
    elif lang == 'eng':
        button1 = types.KeyboardButton('🆓 Supported services')
        button2 = types.KeyboardButton('✉ Need help')
        button3 = types.KeyboardButton('💰 Donate')
        button4 = types.KeyboardButton('⚙ Settings')
    markup.add(button1)
    markup.add(button2)
    markup.add(button3)
    markup.add(button4)
    return markup


def inline(url):
    print('зашел в клавиатуру')
    inlinekey1 = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(text='720p ~' + '(' + str(auth.Control.file_size(url)) + ' MB' + ')' + ' (mp4)',
                                       callback_data='v*' + url)
    but_2 = types.InlineKeyboardButton(text='audio.mp3', callback_data='a*' + url)
    inlinekey1.add(but_1)
    inlinekey1.add(but_2)
    return inlinekey1


def option():
    inlinekey1 = types.InlineKeyboardMarkup()
    url_paypal0 = types.InlineKeyboardButton('Русский', callback_data='ru')
    url_paypal1 = types.InlineKeyboardButton('English', callback_data='eng')
    inlinekey1.add(url_paypal0),
    inlinekey1.add(url_paypal1)
    return inlinekey1


def payment_option(lang):
    inlinekey1 = types.InlineKeyboardMarkup()
    if lang == 'ru':
        url_paypal0 = types.InlineKeyboardButton('Paypal', callback_data='paypal',
                                                 url='https://www.paypal.com/paypalme/mediabot')
        url_paypal1 = types.InlineKeyboardButton('Сбербанк', callback_data='sber')
    elif lang == 'eng':
        url_paypal0 = types.InlineKeyboardButton('Paypal', callback_data='paypal',
                                                 url='https://www.paypal.com/paypalme/mediabot')
        url_paypal1 = types.InlineKeyboardButton('Sberbank', callback_data='sber')
    inlinekey1.add(url_paypal0), inlinekey1.add(url_paypal1)
    return inlinekey1


# def payment_inline():
#     inlinekey1 = types.InlineKeyboardMarkup()
#     url_paypal0 = types.InlineKeyboardButton('0.1$', callback_data='0.1', url='http://127.0.0.1:5000/?price=0.1')
#     url_paypal1 = types.InlineKeyboardButton('1$', callback_data='1', url='http://127.0.0.1:5000/?price=1')
#     url_paypal3 = types.InlineKeyboardButton('3$', callback_data='3', url='http://127.0.0.1:5000/?price=3')
#     url_paypal5 = types.InlineKeyboardButton('5$', callback_data='5', url='http://127.0.0.1:5000/?price=5')
#     inlinekey1.add(url_paypal0), inlinekey1.add(url_paypal1),
#     inlinekey1.add(url_paypal3), inlinekey1.add(url_paypal5)
#     return inlinekey1


@dp.callback_query_handler(state=Step.Q2)
async def inlin(callback_query: types.CallbackQuery, state: FSMContext):
    entry_data = callback_query.data.split('*')[0]
    url = callback_query.data.split('*')[-1]
    lang = await storage.get_data(chat=callback_query.message.chat,
                                  user=callback_query.message.chat.id)
    lang = list(lang.values())[0]
    await bot.send_message(callback_query.message.chat.id, languages[lang]['loading'])
    # await bot.send_message(callback_query.message.chat.id, 'Загрузка началась, ожидайте... ⏰')
    try:
        if entry_data == 'a':
            if auth.Control.audio(url) == 'confusing_error':

                await bot.send_message(callback_query.message.chat.id, languages[lang]['confusing_error'])
                # await bot.send_message(callback_query.message.chat.id, "Неудалось скачать данный файл 😔")
                await state.finish()
            else:
                await callback_query.message.delete()
                file = auth.Control.audio(url)
                await bot.send_audio(callback_query.message.chat.id, file)
                end_cycle = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                datetime_object = datetime.strptime(end_cycle, '%Y-%m-%d %H:%M:%S')
                reaction_time = datetime_object - callback_query.message.date
                await auth.insert_statistics(user_id=callback_query.message.chat.id,
                                             date_add=callback_query.message.date,
                                             button_id='audio',
                                             reaction_time=reaction_time,
                                             url=url)
                delete_file(file)
                await state.finish()
        elif entry_data == 'v':
            await callback_query.message.delete()
            await two_step(message=callback_query.message, url=url, state=state)
            auth.update_records(button_id='video',
                                url=url,
                                user_id=callback_query.message.chat.id,
                                date_add=callback_query.message.date)

    except Exception as e:
        await bot.send_message(callback_query.message.chat.id, e)


@dp.callback_query_handler(state='*')
async def inlin(callback_query: types.CallbackQuery):
    response = callback_query.data
    lang = await storage.get_data(chat=callback_query.message.chat,
                                  user=callback_query.message.chat.id)
    lang = list(lang.values())[0]
    # if response == 'paypal':
    #     await bot.send_message(callback_query.message.chat.id, languages[lang]['select_an_amount'],
    #                            reply_markup=payment_inline(), parse_mode='HTML')
    if response == 'sber':
        await bot.send_message(callback_query.message.chat.id, languages[lang]['card_number'])
    elif response == 'ru':
        await storage.update_data(chat=callback_query.message.chat,
                                  user=callback_query.message.chat.id,
                                  data={'lang': 'ru'})
        get_lang = await storage.get_data(chat=callback_query.message.chat,
                                          user=callback_query.message.chat.id)
        lang = list(get_lang.values())[0]
        await bot.send_message(callback_query.message.chat.id, 'Язык изменен', reply_markup=keyboard(lang))

    elif response == 'eng':
        await storage.update_data(chat=callback_query.message.chat,
                                  user=callback_query.message.chat.id,
                                  data={'lang': 'eng'})

        get_lang = await storage.get_data(chat=callback_query.message.chat,
                                          user=callback_query.message.chat.id)
        lang = list(get_lang.values())[0]
        await bot.send_message(callback_query.message.chat.id, 'Language has been changed', reply_markup=keyboard(lang))


content_path = '/var/www/savebot/content'
stories_folder = content_path + 'stories'
# content_path = '/content'

try:
    original_umask = os.umask(0)
    os.makedirs(content_path, mode=0o777)
    os.makedirs(stories_folder, mode=0o777)
except Exception as e:
    print(e)

try:
    for files in os.listdir(stories_folder):
        if files.endswith('.jpg') \
                or files.endswith('.json') \
                or files.endswith('.mp4') \
                or files.endswith('.DS_Store') \
                or files.endswith('.txt') \
                or files.endswith('.part') \
                or files.endswith('.mp3') \
                or files.endswith('.mkv') \
                or files.endswith('.webm') \
                or files.endswith('.ytdl')\
                or files.endswith('.m3u8'):

            os.remove(stories_folder + '/' + files)
            print(stories_folder + '/' + files)
except Exception as e:
    print(e)

try:
    for files in os.listdir(content_path):
        if files.endswith('.jpg') \
                or files.endswith('.json') \
                or files.endswith('.mp4') \
                or files.endswith('.DS_Store') \
                or files.endswith('.txt') \
                or files.endswith('.part') \
                or files.endswith('.mp3') \
                or files.endswith('.mkv') \
                or files.endswith('.webm') \
                or files.endswith('.jpg') \
                or files.endswith('.ytdl')\
                or files.endswith('.m3u8'):
            os.remove(content_path + '/' + files)
            print(content_path + '/' + files)
except Exception as e:
    print(e)

# Прокси для insaloader:
try:
    # # prod
    path_context_file = '/var/www/savebot/instaloadercontext.py'
    path_original_file = '/var/www/savebot/env/lib/python3.8/site-packages/instaloader/instaloadercontext.py'
    # local
    # path = os.getcwd()
    # path_context_file = path + '/instaloadercontext.py'
    # path_original_file = path + '/venv/lib/python3.8/site-packages/instaloader/instaloadercontext.py'
    shutil.copy(path_context_file, path_original_file)
except Exception as e:
    print(e)

executor.start_polling(dp, skip_updates=True)
