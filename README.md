# kompege

Скрипт автоматизирует получение ответов для вашего варианта на сайте kompege.ru через Selenium и записывает их в `answers.txt`.

1) Склонировать репозиторий и перейти в папку проекта

```bash
git clone https://github.com/Dreksen/kompege.git
cd kompege
```

2) Настроить окружение и установить зависимости

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

3) Запуск

```bash
python main.py --prob-id <номер_варианта>
```

Запуск в фоновом режиме (headless):

```bash
python main.py --prob-id <номер_варианта> --headless
```

- У вас будет около 2 минут, чтобы войти в свой аккаунт (если сайт попросит авторизацию).  
- После завершения (примерно 2–3 минуты) появится файл `answers.txt` с ответами в формате `task_number: answer`; если решения нет, будет `Not_found`.
