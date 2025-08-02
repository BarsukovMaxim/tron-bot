# Tron ENERGY Delegate Bot

Telegram-бот на `aiogram 3`, позволяющий пользователям:
- авторизоваться по приватному ключу TRON-кошелька,
- делегировать ресурсы (ENERGY) другим адресам через `TronGrid`,
- просматривать текущий баланс и ресурсы,
- завершать сессии безопасно.

## 🛠️ Технологии

- Python 3.12+
- aiogram 3.x
- TronPy
- Docker

## 🚀 Быстрый старт

```bash
git clone https://github.com/your-org/tron-energy-bot.git
cd tron-energy-bot
cp .env.example .env
docker build -t tron-bot .
docker run --env-file .env tron-bot
```

