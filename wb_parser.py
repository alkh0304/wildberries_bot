from time import sleep
from bs4 import BeautifulSoup

from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


WB_URL = (
    'https://www.wildberries.ru/catalog/0/search.aspx?'
    'page={page_num}&sort=popular&search='
)


def parse_page(html, id):
    soup = BeautifulSoup(html, features='lxml')
    product_list = soup.find('div', attrs={'class': 'product-card-list'})
    product = product_list.find('div', attrs={'data-popup-nm-id': id})
    if product:
        product_pos = product['data-card-index']
        return product_pos
    else:
        return None


def parse_data(message, address=None):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--headless")
    s = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(
        options=options, service=s
    )
    try:
        if address:
            driver.get('https://www.wildberries.ru')
            driver.maximize_window()
            wait = WebDriverWait(driver, 10)
            # Ожидаем появления кнопки выбора пункта выдачи на главной.
            wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "simple-menu__item.j-geocity-wrap")
                )
            )
            sleep(5)
            btn1 = driver.find_element(
                By.CLASS_NAME, "simple-menu__item.j-geocity-wrap"
            )
            btn1.click()
            # Ожидаем появления попапа карты.
            wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "ymaps-2-1-79-searchbox-input__input")
                )
            )
            sleep(5)
            address_input = driver.find_element(
                By.CLASS_NAME, 'ymaps-2-1-79-searchbox-input__input'
            )
            # Ввод адреса.
            address_input.send_keys(f'{address}')
            driver.find_element(
                By.CLASS_NAME, ("ymaps-2-1-79-searchbox-button-text")
            ).click()
            # Ожидаем появления адреса в списке справа.
            wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "address-item__name")
                )
            )
            sleep(5)
            # Выбираем верхний адрес в списке справа.
            driver.find_element(
                By.CLASS_NAME, ("address-item__name")
            ).click()
            # Ожидаем появления попапа с выбором адреса.
            wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "balloon-content-block")
                )
            )
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), 'Выбрать')]")
                )
            )
            sleep(3)
            # Выбираем адрес.
            driver.find_element(
                By.XPATH, "//*[contains(text(), 'Выбрать')]"
            ).click()
            # Ожидаем обновление адреса.
            sleep(3)
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//*[contains(text(), '{address}')]")
                )
            )
        id = message.split()[0]
        keywords = message.replace(id, '')
        url = WB_URL + keywords.replace(' ', '+')
        page_num = 1
        while page_num <= 100:
            driver.get(url.format(page_num=page_num))
            wait = WebDriverWait(driver, 10)
            # Ожидаем загрузки каталога.
            wait.until(
                EC.presence_of_element_located(
                        (By.CLASS_NAME, "product-card-list")
                )
            )
            html = driver.page_source
            if html:
                # Парсим каталог.
                parse_result = parse_page(html, id)
                if parse_result:
                    return (
                        f'Товар находится на {page_num} странице, '
                        f'в {parse_result} позиции'
                    )
                else:
                    page_num += 1
        return 'Товар не обнаружен по данному запросу'
    except Exception as ex:
        print(ex)
        return f'Адрес {address} не был найден, попробуйте другой'
    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    print(parse_data(
        '87689628 Омега 3', 'Сосновоборск, Улица Энтузиастов 7'
    ))
    # print(load_data('23501578 Омега 3'))
