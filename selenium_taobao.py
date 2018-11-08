from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote
from lxml import etree


KEYWORD = 'ipad'
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 15)
MAX_PAGE = 3


def index_page(page):
    print('正在打印第', str(page) + '页')
    try:
        url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
        browser.get(url)
        if page > 1:
            input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
            submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                            '#mainsrp-pager div.form > span.btn.J_Submit')))
            input.clear()
            input.send_keys(page)
            submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
        get_product()
    except TimeoutException:
        print('==================================================')
        index_page(page)


def get_product():
    html = browser.page_source
    html = etree.HTML(html)
    items = html.xpath("//div[@class='item J_MouserOnverReq']")
    for item in items:
        product = {
            'image': item.xpath(".//img/@src"),
            'price': item.xpath(".//strong/text()"),
            'deal': item.xpath(".//div[@class='deal-cnt']/text()"),
            'title': item.xpath(".//div[@class='row row-2 title']//a/text()"),
            'shop': item.xpath(".//div[@class='shop']//span/text()"),
            'location': item.xpath(".//div[@class='location']/text()")
        }
        print(product)


def main():
    for i in range(1, MAX_PAGE+1):
        index_page(i)


if __name__ == "__main__":
    main()

