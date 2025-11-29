Telegram Bot с интеграцией Local LLM 
Это проект Telegram-бота, который использует локально модель через LM Studio для генерации ответов.

Используемые библиотеки
pyTelegramBotAPI (telebot) — взаимодействие с Telegram.

requests — HTTP запросы к API LM Studio.

jsons — удобная сериализация/десериализация ответов.


Установка и запуск

1) Подготовка окружения
   ```pip install pyTelegramBotAPI requests jsons```
2) Настройка LM Studio
3) Настройка бота
   Откройте файл скрипта (например, main.py).
   Найдите переменную API_TOKEN и вставьте токен вашего бота:
   ```API_TOKEN = 'ВАШ_ТОКЕН_ОТ_BOTFATHER```
4) Запустите ```python main.py```


Команды:
```/start``` - Приветствие и инициализация диалога.
```/clear``` - Очистка контекста.
```/model``` - Показывает название текущей модели в LM Studio.
