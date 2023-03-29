import os
import logging
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, Document
from telegram.ext import filters, CallbackQueryHandler, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler
from telegram.error import BadRequest
# import dbfunctions as db
# import osfunctions as osf
# import const
# from levels import LOGIN_LEVEL, SIGNUP_LEVEL, Login, Signup

# from direction import get_info

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TEXT_0 = 'welcome! please select an option:'
TEXT_1 = 'login'
TEXT_2 = 'signup'
TEXT_3 = 'you are already authorized in this chat'
TEXT_4 = 'please send your username:'
TEXT_5 = 'send your password:'
TEXT_6 = 'you are successfully logged in!'
TEXT_7 = 'username or password is incorrect'
TEXT_8 = 'please send a username:'
TEXT_9 = 'send a email:'
TEXT_10 = 'send a password:'
TEXT_11 = 'this username is alreacy exitst, please try another one:'
TEXT_12 = 'account has been successfully created! Now you can login.'
TEXT_13 = 'logout'
TEXT_14 = 'you are successfully logged out.'
TEXT_15 = "Sorry, I didn't understand that command."
TEXT_16 = 'saved!'
TEXT_17 = 'sorry, file is too big'
TEXT_18 = 'you need to login to back up your files.'
TEXT_19 = 'you need to login to see your files.'



logging_in_chats = []
signing_up_chats = []



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    buttons = [
        [KeyboardButton(TEXT_1)],
        [KeyboardButton(TEXT_2)]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=TEXT_0, reply_markup=reply_markup)


async def main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    message_text = update.message.text

    if message_text == TEXT_1:
        # check if user is authrized already
        if db.is_authorized(chat_id=chat_id):
            await context.bot.send_message(chat_id=chat_id, text=TEXT_3)
            return
        # check if user already logging in
        for l in logging_in_chats:
            if l.chat_id == chat_id:
                logging_in_chats.remove(l)
                break
        # add user to login list
        logging_in_chats.append(Login(chat_id=chat_id))
        await context.bot.send_message(chat_id=chat_id, text=TEXT_4)

    elif message_text == TEXT_2:
        # check if user already signing up
        for s in signing_up_chats:
            if s.chat_id == chat_id:
                signing_up_chats.remove(s)
                break
        signing_up_chats.append(Signup(chat_id=chat_id))
        await context.bot.send_message(chat_id=chat_id, text=TEXT_8)

    elif message_text == TEXT_13:
        db.logout_chat(chat_id=chat_id)
        await context.bot.send_message(chat_id=chat_id, text=TEXT_14)

    else:
        # check if user is trying to login
        for a in logging_in_chats:
            if a.chat_id == chat_id:
                # if user is typing a username
                if a.level == LOGIN_LEVEL.waiting_for_username:
                    a.username = message_text
                    a.level = LOGIN_LEVEL.waiting_for_password
                    await context.bot.send_message(chat_id=chat_id, text=TEXT_5)
                # if user is typing a password
                elif a.level == LOGIN_LEVEL.waiting_for_password:
                    a.password = message_text
                    if db.authorize(username=a.username, password=a.password, chat_id=chat_id):
                        await context.bot.send_message(chat_id=chat_id, text=TEXT_6)
                    else:
                        await context.bot.send_message(chat_id=chat_id, text=TEXT_7)
                    logging_in_chats.remove(a)
                break

         # check if user is trying to sing up
        for a in signing_up_chats:
            if a.chat_id == chat_id:
                # if user is typing a username
                if a.level == SIGNUP_LEVEL.waiting_for_username:
                    if db.user_exists(message_text):
                        await context.bot.send_message(chat_id=chat_id, text=TEXT_11)
                    else:
                        a.username = message_text
                        a.level = SIGNUP_LEVEL.waiting_for_email
                        await context.bot.send_message(chat_id=chat_id, text=TEXT_9)
                # if user is typing a password
                elif a.level == SIGNUP_LEVEL.waiting_for_email:
                    a.email = message_text
                    a.level = SIGNUP_LEVEL.waiting_for_password
                    await context.bot.send_message(chat_id=chat_id, text=TEXT_10)
                elif a.level == SIGNUP_LEVEL.waiting_for_password:
                    a.password = message_text
                    db.create_user(username=a.username, email=a.email, password=a.password)
                    osf.create_directory(username=a.username)
                    await context.bot.send_message(chat_id=chat_id, text=TEXT_12)
                    signing_up_chats.remove(a)
                break


async def backup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    update_message = update.message
    # check if user is authrized
    if not db.is_authorized(chat_id=chat_id):
        await context.bot.send_message(chat_id=chat_id, text=TEXT_18)
        return

    # get document details
    if update_message.document: # if type(update_message.document) == Document: 
        file_id = update_message.document.file_id
        file_name = update_message.document.file_name
        file_size = update_message.document.file_size
    elif update_message.photo:
        file_id = update_message.photo[-1].file_id
        file_name = update_message.photo[-1].file_unique_id + '.jpg'
        file_size = update_message.photo[-1].file_size
    elif update_message.audio:
        file_id = update_message.audio.file_id
        file_name = update_message.audio.file_name
        file_size = update_message.audio.file_size
    elif update_message.voice:
        file_id = update_message.voice.file_id
        file_name = update_message.voice.file_unique_id + '.ogg'
        file_size = update_message.voice.file_size
    
    # saving to drive:
    if file_id and file_name:
        # check file size
        if file_size > const.DOWNLOAD_LIMIT:
            await context.bot.send_message(chat_id=chat_id, text=TEXT_17, reply_to_message_id=chat_id)
            return
        auth_username = db.authorized_username(chat_id)
        new_file = await context.bot.get_file(file_id=file_id)
        # new_file = await update.message.effective_attachment.get_file()
        await new_file.download_to_drive(custom_path=f'backup/{auth_username}/{file_name}')
        await context.bot.send_message(chat_id=chat_id, text=TEXT_16, reply_to_message_id=update.message.id)


async def myfiles(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    # check if user is authrized
    if not db.is_authorized(chat_id=chat_id):
        await context.bot.send_message(chat_id=chat_id, text=TEXT_19)
        return

    auth_username = db.authorized_username(chat_id)
    for file in osf.get_files_list(auth_username):
        await context.bot.send_document(chat_id=update.effective_chat.id, document=f'backup/{auth_username}/{file}')


async def agree(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data="1"),
            InlineKeyboardButton("Option 2", callback_data="2"),
        ],
        [InlineKeyboardButton("Option 3", callback_data="3")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    await query.edit_message_text(text=f"Selected option: {query.data}")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=TEXT_15)


def run():
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    myfiles_handler = CommandHandler('myfiles', myfiles)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    main_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), main)
    backup_handler = MessageHandler(~filters.TEXT, backup)
    # location_handler = MessageHandler(filters.LOCATION, location)
    # echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    application.add_handler(start_handler)
    application.add_handler(myfiles_handler)
    application.add_handler(unknown_handler)
    application.add_handler(main_handler)
    application.add_handler(backup_handler)
    # application.add_handler(location_handler)
    # application.add_handler(echo_handler)
    # application.add_handler(CallbackQueryHandler(button))
    
    application.run_polling()