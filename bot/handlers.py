from random import shuffle

from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

from api.hh_api import langs, get_vacancies_by_lang, get_random_vacancy, parse_vacancy
from .loger import log_error
from settings.settings import ROFL

# BUTTONS -----------------------------------------------------
button_help = 'Help'
button_langs = 'Языки'
button_best = 'Лучшая вакансия!'
button_next = 'Next'
button_stop = 'Stop'
button_yea = 'Хочу'
button_yes = 'ЕБАТЬ, как хочу!'
button_no = 'Нет, спасибо'

# KEYBOARDS ---------------------------------------------------
KB_START = [
    [
        KeyboardButton(text=button_help),
        KeyboardButton(text=button_langs),
        KeyboardButton(text=button_best)
    ],
]

# MARKUPS -----------------------------------------------------
MRK_START = ReplyKeyboardMarkup(
    keyboard=KB_START,
    resize_keyboard=True,
)


# FUNCTIONS ---------------------------------------------------
def create_inline_kb(langs):
    kb = []
    for lang in langs:
        kb.append([
            InlineKeyboardButton(text=lang, callback_data=lang)
        ])
    return InlineKeyboardMarkup(kb)


# HANDLERS ----------------------------------------------------
def start_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text="Хэллоу. Данный бот, ботец, ботишка парсит ХХ, и подкидывает вакансии прямо тебе в телегу.",
        reply_markup=MRK_START
    )


def button_help_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text="Хэлп мэсседж - выводит данное сообщение.\n\nЯзыки - вакансии по ЯП.\n\nЛучшая вакансия - Рофлан вакансии.",
        reply_markup=MRK_START
    )


def button_langs_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Выбери язык программирования (чуз ё дестени)',
        reply_markup=create_inline_kb(langs)
    )


def button_best_handler(update: Update, context: CallbackContext):
    shuffle(ROFL)
    # txt = next(get_random_vacancy())
    txt = f"Наша свора диких математиков разработала квази-точный метод подбора вакансий.\n\n" \
          f"Используя передовые научные методы, такие как: {ROFL[0]}, {ROFL[1]} и {ROFL[2]} - для вас были подобраны варианты, наиболее точно отвечающие вашим навыкам.\n\n" \
          f"Хотите их увидеть?"
    update.message.reply_text(
        text=txt,
        reply_markup=create_inline_kb([button_no, button_yea, button_yes])
    )


def other_message_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text="Не понятно.",
        reply_markup=MRK_START
    )


# MAIN HANDLER ------------------------------------------------
def callback_handler(update: Update, context: CallbackContext):
    callback_data = update.callback_query.data

    if callback_data == button_yea or callback_data == button_yes:
        context.user_data['gen'] = get_random_vacancy()
        try:
            txt = next(context.user_data['gen'])
        except Exception:
            update.callback_query.edit_message_text(
                text='Всё, нахуй, вырубай!',
                parse_mode=ParseMode.MARKDOWN
            )
            return

        update.callback_query.edit_message_text(
            text=txt,
            reply_markup=create_inline_kb([button_stop, button_next])
        )

    if callback_data in langs:
        context.user_data['gen'] = get_vacancies_by_lang(callback_data)
        try:
            txt = next(context.user_data['gen'])
        except Exception:
            update.callback_query.edit_message_text(
                text='Всё, нахуй, вырубай!',
                parse_mode=ParseMode.MARKDOWN
            )
            return

        update.callback_query.edit_message_text(
            text=txt,
            reply_markup=create_inline_kb([button_stop, button_next])
        )

    elif callback_data == button_next:
        try:
            txt = next(context.user_data['gen'])
            update.callback_query.edit_message_text(
                text=txt,
                reply_markup=create_inline_kb([button_stop, button_next])
            )
        except StopIteration:
            update.callback_query.edit_message_text(
                text='Всё, нахуй, вырубай!',
                parse_mode=ParseMode.MARKDOWN
            )
            return

    elif callback_data == button_stop or callback_data == button_no:
        context.user_data['gen'].close()
        update.callback_query.edit_message_text(
            text='Закругляемся.',
            parse_mode=ParseMode.MARKDOWN
        )


@log_error
def message_handler(update: Update, context: CallbackContext):
    text = update.message.text
    if text == '/start':
        return start_handler(update, context)
    elif text == button_help:
        return button_help_handler(update, context)
    elif text == button_best:
        return button_best_handler(update, context)
    elif text == button_langs:
        return button_langs_handler(update, context)
    else:
        return other_message_handler(update, context)
