from config import *
import models


@dp.message_handler(commands=['start', 'help'])
async def help_message(message: types.Message):
    """
    prints help message
    :param message: user's message
    :return:
    """
    chat_id = message.chat.id
    name = message.from_user.full_name
    await bot.send_message(chat_id, INITIAL_MESSAGE.format(name))
    await bot.send_message(chat_id, SEND_YOUR_TEXT)


async def sendError(e, chat_id):
    """
    send an error to the user and print it in the console
    :param e:
    :return:
    """
    await bot.send_message(chat_id, ERROR)
    if hasattr(e, 'message'):
        print(e.message)
        await bot.send_message(chat_id, e.message)
    else:
        print(e)
        await bot.send_message(chat_id, e)


async def translate(user, chat_id) -> str:
    """
    attempt to translate the text
    :param user:
    :param chat_id:
    :return:
    """
    src = "auto"
    dest = "en"
    if user.language_src != "*":
        src = user.language_src
    if user.language_dest != "*":
        dest = user.language_dest
    try:
        translated_text = translator.translate(user.text, dest=dest, src=src).text
        await bot.send_message(chat_id, TRANSLATED_TEXT.format(translated_text))
    except Exception as e:
        await sendError(e, chat_id)
    await bot.send_message(chat_id, SEND_YOUR_TEXT)


@dp.message_handler()
async def get_input(message: types.Message):
    """
    prepare input for the `translate` function by user input
    :param message: user's message
    :return:
    """
    try:
        user_id = message.from_user.id
        chat_id = message.chat.id
        user = models.session.query(models.User).filter(models.User.user_id == user_id).first()
        if user is None:
            models.session.add(models.User(user_id, message.text))
            models.session.flush()
            models.session.commit()
            await bot.send_message(chat_id, ASK_ABOUT_LANGUAGE_SRC)
            return
        if user.language_src is None:
            user.language_src = message.text
            models.session.flush()
            models.session.commit()
            await bot.send_message(chat_id, ASK_ABOUT_LANGUAGE_DEST)
            return
        if user.language_dest is None:
            user.language_dest = message.text
            models.session.flush()
            models.session.commit()
            await translate(user, chat_id)
            models.session.delete(user)
            models.session.flush()
            models.session.commit()
            return
    except Exception as e:
        await sendError(e, chat_id)


if __name__ == '__main__':
    executor.start_polling(dp)
