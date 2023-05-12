from seleniumwire import webdriver
from bs4 import BeautifulSoup


def check(word, whiteList):
    driver = webdriver.Chrome(executable_path="./chromedriver")
    driver.get(f'https://google.com/search?q={word}')

    ads = driver.find_element_by_xpath('//*[@id="tads"]').get_attribute('innerHTML')
    soup = BeautifulSoup(ads, "html.parser")
    ads_num = len(soup.find_all("div", {"class": "uEierd"}))

    sites = []
    for num in range(1, ads_num):
        url = driver.find_element_by_xpath(
            f'//*[@id="tads"]/div[{num}]/div/div/div/div[1]/a'
        ).get_attribute("href")
        if not url in whiteList:
            sites.append(url)

    driver.quit()
    return sites


