"""
2023.02.03: https://huggingface.co/bigscience/bloom/ is 704.59GB
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

URL = 'https://huggingface.co/bigscience/bloom/tree/main'


def format_size(size: str) -> float:
    """format size in bytes"""
    size = size.strip('LFS').strip()
    match size.split():
        case [*nums, 'Bytes']:
            size = float(*nums)
        case [*nums, 'kB']:
            size = 1024 * float(*nums)
        case [*nums, 'MB']:
            size = 1024 * 1024 * float(*nums)
        case [*nums, 'GB']:
            size = 1024 * 1024 * 1024 * float(*nums)
        case _:
            raise NotImplementedError(f'{size}')
    return size


def browser_options():
    options = webdriver.FirefoxOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")
    return options


s = Service(GeckoDriverManager().install())

with webdriver.Firefox(service=s, options=browser_options()) as driver:
    driver.get(URL)
    driver.implicitly_wait(5)

    try:  # loads all files
        while True:
            driver.find_element(By.XPATH, "//li/button").click()
    except NoSuchElementException:
        pass

    sizes = driver.find_elements(By.XPATH, "//div/ul/li/a[@title='Download file']")

    size_in_gb = sum([format_size(size.text) for size in sizes]) / 1024 / 1024 / 1024
    print(f'size is: {size_in_gb:.2f}GB')
