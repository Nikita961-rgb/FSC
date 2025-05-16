# Telegram Combo Bot (для Render.com)

## ✅ Функціонал:
- Три кнопки: 🇺🇦 українські пости, 🇷🇺 російські пости, 🔀 рандом
- Фото + пост + кнопка "✅ Використав"
- Перевірка доступу через `uss.txt`

## 📂 Файли:
- telegram_bot.py — основний код
- posts_ukr.txt / posts_rus.txt — пости
- photos/ — активні фото
- used/ — використані
- uss.txt — Telegram ID з доступом
- requirements.txt — залежності для Render
- start.sh — команда запуску

## 🚀 Як запустити на Render:
1. Перейди на https://render.com
2. Зареєструйся та створіть **New Web Service**
3. Завантаж папку або лінкуй GitHub репозиторій
4. Налаштуй:
   - **Environment**: Python
   - **Start command**: `bash start.sh`
   - **Build command**: `pip install -r requirements.txt`
   - Додай ENV перемінну: `TOKEN` = твій токен від BotFather
5. Натисни Deploy

Бот автоматично запуститься та працюватиме 24/7 💡
