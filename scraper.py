from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import dateparser
from database import data


def button_cliker(driver):
        try:
                driver.find_element_by_class_name("css-cuxnr-BaseStyles").click()
                sleep(5)
                phone = driver.find_element_by_class_name("css-v1ndtc").text 
                return phone
        except:
            return button_cliker(driver)

def Convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct

def take_data(driver,link):
    driver.execute_script(f"window.open('{link}', 'new_window')")
    wdw = driver.window_handles
    driver.switch_to.window(wdw[1])
    sleep(5)
    title = driver.find_element_by_class_name("css-r9zjja-Text").text  
    imgs_temp = driver.find_elements_by_class_name("css-1bmvjcs")
    imgs=[]
    for img in imgs_temp:
        if img.get_attribute("src") is not None:
            imgs.append(img.get_attribute("src"))
    info ="Тип  " + driver.find_elements_by_class_name("css-sfcl1s")[0].text
    info = info.replace('\n','  ')
    info = info.replace(':',' ')
    info = info.split('  ')
    info = Convert(info)
    created_at = driver.find_element_by_class_name("css-19yf5ek").text
    created_at = dateparser.parse(created_at, date_formats=['%d %B %Y'])
    created_at = created_at.strftime("%d-%m-%Y")
    price = driver.find_element_by_class_name("css-okktvh-Text").text
    description = driver.find_element_by_class_name("css-g5mtbi-Text").text
    checked_data = check_class_exist("css-cuxnr-BaseStyles")
    if checked_data:
        phone = button_cliker(driver)
    else:
        phone = None
    olx_data = {
            'url': link,
            'title': title,
            'imgs': imgs,
            'price': price,
            'date': created_at,
            'info': info,
            'description': description,
            'phone': phone,
        }
    if data.count_documents({"url": link}) == 0:
        data.insert_one(olx_data).inserted_id
    else: 
        exit()

def check_class_exist(check_data):
        try:
            driver.find_element_by_class_name(check_data)
            return True
        except:
            return False

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--lang=es")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.get('https://www.olx.uz/nedvizhimost/kvartiry/arenda-dolgosrochnaya/tashkent/')
sleep(5)
max_page = int(driver.find_element_by_xpath("//a[@data-cy='page-link-last']").text)
for page in range(1,max_page):
    driver.get(f'https://www.olx.uz/nedvizhimost/kvartiry/arenda-dolgosrochnaya/tashkent/?page={page}')
    table = driver.find_elements_by_class_name("offers")[1]
    elems = table.find_elements_by_class_name("thumb")
    links = []
    for elem in elems:
        links.append(elem.get_attribute("href"))
    for link in links:
        take_data(driver,link)
    wdw = driver.window_handles
    driver.close()
    driver.switch_to.window(wdw[0])
driver.quit()