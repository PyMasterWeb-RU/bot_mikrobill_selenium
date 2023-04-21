from telebot import TeleBot
import time
import os
import glob
from auth import login, password
from Screenshot import Screenshot
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

bot = TeleBot("Ваш токена бота")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет {0.first_name}! Я бот для поиска данных о клиенте.".format(message.from_user))
    
@bot.message_handler(commands=['search_client'])
def search_client(message):
    msg = bot.send_message(message.chat.id, "Введите логин клиента, информацию по которому хотите найти: ")
    bot.register_next_step_handler(msg, search)
    
@bot.message_handler(content_types=['text'])
def text_client(message):
    bot.send_message(message.chat.id, "Ты что-то хотел?")

def search(message):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    s = Service(executable_path='chromedriver\chromedriver.exe')
    ob = Screenshot.Screenshot()
    driver = webdriver.Chrome(service=s, options=options)
    bot.send_message(message.chat.id, "Начинаю поиск")
    phrase = message.text
    driver.maximize_window()
    driver.get('ваш домен микротика/kassa/')
    login_input = driver.find_element(By.NAME, 'chaiserlogin')
    login_input.clear()
    login_input.send_keys(login)
    pass_input = driver.find_element(By.NAME, 'chaiserpassword')
    pass_input.clear()
    pass_input.send_keys(password)
    pass_input.send_keys(Keys.ENTER)
    seach_input = driver.find_element(By.ID, 'usrname')
    seach_input.clear()
    seach_input.send_keys(phrase)
    seach_click = driver.find_element(By.ID, 'lookusers')
    client_input = driver.find_element(By.CLASS_NAME, 'even').click()
    table_input = driver.find_element(By.ID, 'userinfo')
    img_url = ob.get_element(driver, table_input, r'client')
    driver.close()
    driver.quit()
    # bot.send_photo(message.chat.id, 'client\cropped_screenshot.png.png')
    photo = open("client\cropped_screenshot.png.png", "rb")
    bot.send_photo(message.chat.id, photo)
    
bot.polling()
