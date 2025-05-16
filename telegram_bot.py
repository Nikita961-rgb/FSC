
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
)
import os
import random
import shutil

PHOTO_DIR = 'photos'
USED_DIR = 'used'
POSTS_UKR = 'posts_ukr.txt'
POSTS_RUS = 'posts_rus.txt'
USERS_FILE = 'uss.txt'
PHOTO_TRACK = {}

def load_posts(file_path):
    if not os.path.exists(file_path):
        return ["(постів не знайдено)"]
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def load_allowed_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip().isdigit()]

def user_has_access(user_id):
    allowed = load_allowed_users()
    return str(user_id) in allowed

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not user_has_access(user_id):
        await update.message.reply_text("🚫 У вас немає доступу до цього бота.")
        return

    keyboard = [
        [KeyboardButton("Отримати 🇺🇦")],
        [KeyboardButton("Получить 🇷🇺")],
        [KeyboardButton("Рандом 🔀")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Вибери, який тип поста ти хочеш отримати:", reply_markup=reply_markup)

async def handle_get(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not user_has_access(user_id):
        await update.message.reply_text("🚫 У вас немає доступу до цього бота.")
        return

    text_command = update.message.text
    if "🇺🇦" in text_command:
        posts = load_posts(POSTS_UKR)
    elif "🇷🇺" in text_command:
        posts = load_posts(POSTS_RUS)
    else:
        posts = load_posts(POSTS_UKR) + load_posts(POSTS_RUS)

    photos = [f for f in os.listdir(PHOTO_DIR) if os.path.isfile(os.path.join(PHOTO_DIR, f))]

    if not photos:
        await update.message.reply_text("Фото закінчилися 😢 Додай нові у папку 'photos/'")
        return

    text = random.choice(posts)
    photo_file = random.choice(photos)
    photo_path = os.path.join(PHOTO_DIR, photo_file)
    PHOTO_TRACK[str(update.effective_chat.id)] = photo_file

    keyboard = [[InlineKeyboardButton("✅ Використав", callback_data="used")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    with open(photo_path, "rb") as img:
        await update.message.reply_photo(img, caption=text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if not user_has_access(user_id):
        await query.edit_message_caption(caption="🚫 У вас немає доступу до цієї дії.")
        return

    user_chat_id = str(query.message.chat.id)
    if user_chat_id in PHOTO_TRACK:
        photo_file = PHOTO_TRACK[user_chat_id]
        src = os.path.join(PHOTO_DIR, photo_file)
        dst_dir = USED_DIR
        os.makedirs(dst_dir, exist_ok=True)
        dst = os.path.join(dst_dir, photo_file)

        if os.path.exists(src):
            shutil.move(src, dst)
            await query.edit_message_caption(caption="✅ Фото переміщено в used/")
        else:
            await query.edit_message_caption(caption="⚠️ Фото вже переміщено або видалено.")
    else:
        await query.edit_message_caption(caption="⚠️ Не знайдено активного фото для переміщення.")

app = ApplicationBuilder().token(os.environ.get("TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("Отримати|Получить|Рандом"), handle_get))
app.add_handler(CallbackQueryHandler(button_handler))
app.run_polling()
