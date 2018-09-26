import time
import sys

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

user_arg = sys.argv[1]
pass_arg = sys.argv[2]
message_text = sys.argv[3]

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

url = 'https://www.okcupid.com/login'
driver = webdriver.Chrome(chrome_options=options)  # Optional argument, if not specified will search path.

driver.get(url);
driver.maximize_window();


username = driver.find_element_by_name('username').send_keys(user_arg)
password = driver.find_element_by_name('password').send_keys(pass_arg)

login_button = driver.find_element_by_class_name ('login2017-actions-button')
login_button.click()

list_of_url = []
time.sleep(5) # Let the user actually see something!
likedurl = 'https://www.okcupid.com/who-you-like'
WebDriverWait(driver,1).until(EC.url_contains("home"))

driver.get(likedurl)
WebDriverWait(driver,1).until(EC.url_contains("who-you-like"))

all_likeduser = driver.find_elements_by_class_name('userrow-inner')
for onlineuser in all_likeduser:
    print(" ")
    if(onlineuser.find_element_by_class_name('userrow-username').find_elements_by_xpath(".//span[@class='onlinedot userrow-username-online']")):
        print(onlineuser.find_element_by_class_name('userrow-username-name').text)
        liked_profile = onlineuser.get_attribute("href")
        list_of_url.append(liked_profile)


idx = 1
for online_url in list_of_url:
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[idx])
    driver.get(online_url)
    driver.implicitly_wait(5)
    message_button = driver.find_element_by_xpath(".//button[@class='profile-buttons-actions-action profile-buttons-actions-message']")
    driver.execute_script("arguments[0].click();", message_button)
    message_window = driver.find_element_by_class_name('compose-textarea-wrapper')
    message_id = message_window.find_element_by_xpath(".//textarea[@id]").get_attribute('id')
    message_window.find_element_by_id(message_id).clear()
    message_window.find_element_by_id(message_id).send_keys(message_text)
    send_button = message_window.find_element_by_xpath("//button[@class='flatbutton']")
    send_button.click()

    time.sleep(4)
    close_button = message_window.find_element_by_xpath("//button[@class='close']")
    close_button.click()

    idx = idx + 1