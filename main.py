from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
options.add_argument = ('--window-size=1920,1080')

DRIVER_PATH = 'chromedriver.exe'
driver = webdriver.Chrome(options = options, executable_path=DRIVER_PATH)
driver.get('https://radiokampus.fm/playlista/')
print(driver.page_source)
driver.quit()