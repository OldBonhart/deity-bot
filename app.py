import telebot
from telebot import types
from flask import Flask, request
from io import BytesIO

from generators import catGan, humanGan, dogGan, predict

# Constants
TOKEN       = ''
STICKER_ID  = 'CAADAgADAQAD3BQ9Js2i8jeh-Q6nAg'
GIF_ID      = 'CgADAgAD4AMAAtmwSUmif7hi8FXP3gI'
VIDEO_ID    = 'BAADAgADkwQAAq_1KEsWyLl-jjNGIxYE'
DOCUMENT_ID = 'BQADAgADCQQAAsvhIEtAkaS848uOLxYE'
cat_emj     = '🐱'
human_emj   = '🧔🏻'
dog_emj     = '🐶'


bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


## Bot menu
markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
btn_cat = types.KeyboardButton('🐱 Cat')
btn_human = types.KeyboardButton('🧔🏻 Human')
btn_dog = types.KeyboardButton('🐶 Dog')
btn_about = types.KeyboardButton('ℹ️ About the algorithm')

markup_menu.add(btn_cat, btn_human, btn_dog, btn_about)

## Command handlers
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_first_name = message.from_user.first_name
    bot.reply_to(message, f"Welcome {user_first_name}, I'm a bot based on generative adversarial network,"
    f" i can generate cats, people, dogs. /help",
                 reply_markup=markup_menu)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, 'Just click on one of the menu buttons.',
                 reply_markup=markup_menu)



@bot.message_handler(commands=['About the algorithm'])
def send_welcome(message):
    bot.send_video(message.chat.id, VIDEO_ID, caption='What Makes a Good Image Generator AI?')
    bot.send_document(message.chat.id, DOCUMENT_ID, caption='Generative Adversarial Nets')

# Generators
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == '🐱 Cat':
        # send message
        bot.send_message(message.chat.id,
                         f'I created you a {cat_emj}cat, look at the grandeur of my creation and start to pray to me.')
        # send feedback
        feedback = predict(catGan)
        stream = BytesIO()
        feedback.save(stream, format='PNG')
        stream.flush()
        stream.seek(0)
        bot.send_photo(message.chat.id, stream)
        print("Sent Photo to user")

    elif message.text == '🧔🏻 Human':

        # send message
        bot.send_message(message.chat.id,
                         f'I created you a {human_emj}human, look at the grandeur of my creation and start to pray to me.')
        # send feedback
        feedback = predict(humanGan)
        stream = BytesIO()
        feedback.save(stream, format='PNG')
        stream.flush()
        stream.seek(0)
        bot.send_photo(message.chat.id, stream)
        print("Sent Photo to user")

    elif message.text == '🐶 Dog':

        # send message
        bot.send_message(message.chat.id,
                         f'I created you a {dog_emj}dog, look at the grandeur of my creation and start to pray to me.')
        # send feedback
        feedback = predict(dogGan)
        stream = BytesIO()
        feedback.save(stream, format='PNG')
        stream.flush()
        stream.seek(0)
        bot.send_photo(message.chat.id, stream)
        print("Sent Photo to user")

    elif message.text == 'ℹ️ About the algorithm':
            bot.send_document(message.chat.id, DOCUMENT_ID, caption='Generative Adversarial Nets')
            bot.send_video(message.chat.id, VIDEO_ID, caption='What Makes a Good Image Generator AI?')


# File handlers
@bot.message_handler(content_types=['sticker'])
def sticker_handler(message):
    bot.send_sticker(message.chat.id, STICKER_ID)



@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "Webhook", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='app url here' + TOKEN)
    return "Webhook", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

