# kompege
Скрипт, который автоматизирует получение ответов для вашего варианта (prob_id) на сайте kompege.ru через Selenium и впиывает их в answers.txt

1) Склонировать
git clone https://github.com/Dreksen/kompege.git
cd kompege

2) Настроить окружение + зависимости
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt

3) Запуск 
python main.py --prob-id <номер_варианта>
если хотите в фоновом режиме:
python main.py --prob-id <номер_варианта> --headless


У вас будет 2 минуты, чтобы войти в свой аккаунт. 

После завершения (2-3 минуты) появится файл answers.txt, где будут ответы в формате "task_number : answer". Если решения не будет на сайте, answer = "Not_found".
