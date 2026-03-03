from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import os
import pickle
from fake_useragent import UserAgent
import argparse

parser = argparse.ArgumentParser(description="Get answers from kompege.ru")
parser.add_argument("--prob-id", required=True, help="Variant/problem id on kompege.ru")  # обязательный аргумент [web:124]
parser.add_argument("--headless", action="store_true", help="Run Chrome in headless mode")  # флаг [web:124]
args = parser.parse_args()

prob_id = args.prob_id

options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')

if args.headless:
    options.add_argument('--headless')

user_agents_filename = 'user_agents.pkl'
ua = UserAgent()
if os.path.exists(user_agents_filename):
    with open(user_agents_filename, 'rb') as f:
        user_agents = pickle.load(f)
else:
    user_agents = []

if user_agents:
    random_user_agent = user_agents.pop()
    options.add_argument(f'user-agent={random_user_agent}')
else:
    print("Список пользовательских агентов пуст. Создание случайного агента.")
    random_user_agent = ua.random
    options.add_argument(f'user-agent={random_user_agent}')

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)
driver.implicitly_wait(120)

general_url = 'https://kompege.ru/login/'
driver.get(general_url)

driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/div[4]/div[2]/input[1]').send_keys(prob_id)
driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/div[4]/div[2]/input[2]').click()

driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/div[4]/div[2]/input[2]').click()
driver.find_element(By.CLASS_NAME, "end").find_element(By.TAG_NAME, "span").click()
alert = driver.switch_to.alert
alert.accept()
driver.get('https://kompege.ru/lk')
driver.find_element(by=By.XPATH, value='//*[@id="app"]/div/div[2]/p[4]').click()

answers = {}

tr_element = driver.find_element(By.CLASS_NAME, "table__header")
td_elements = tr_element.find_elements(By.TAG_NAME, "td")[1:]
a_elements = []

driver.implicitly_wait(10)
for td in td_elements:
    try:
        a_element = td.find_element(By.TAG_NAME, "a")
        a_elements.append(a_element)
    except Exception as e:
        print("No <a> element found in this <td>", e)

links = [a.get_attribute("href") for a in a_elements]

for i in range(27):
    if 'undefined' in links[i]:
        answers[i] = 'Not_found'
    else:
        driver.get(str(links[i]))
        element = driver.find_element(By.CLASS_NAME, "link")
        element.click()
        answer = driver.find_element(By.CLASS_NAME, "answerWrap").find_element(By.TAG_NAME, "p").text
        answers[i] = answer
        driver.back()
    time.sleep(1)

with open("answers.txt", "w", encoding="utf-8") as file:
    for key, value in answers.items():
        file.write(f"{key + 1}: {value}\n")

if random_user_agent not in user_agents:
    user_agents.append(random_user_agent)
    with open(user_agents_filename, 'wb') as f:
        pickle.dump(user_agents, f)

print('the end')

