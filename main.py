from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from parsel import Selector
from datetime import datetime
from time import sleep
import csv
import undetected_chromedriver as uc
import random
import time
import re
from playwright.sync_api import Page, expect

# Create a new instance of the Chrome driver

def extract_details(driver, url):

    sleep(random.randint(13,34))
    max_scrolls = 4
    page_height = driver.execute_script("return document.body.scrollHeight")

    for i in range(max_scrolls):
        scroll_amount = random.uniform(page_height / max_scrolls * i, page_height / max_scrolls * (i + 1))
        driver.execute_script(f"window.scrollTo(0, {scroll_amount});")

    driver.get(url)

    sel = Selector(text = driver.page_source)

    fields = {}


    fields['url'] = url
    fields['title'] = sel.xpath('//div[@class="report-heading"]//span[@class="title"]/text()').extract_first()
    try:
        fields['id'] = sel.xpath('//div[@class="report-heading"]//small/text()').extract_first().split(" • ")[0].replace('Project: ', '')
    except:
        fields['id'] = ''
    try:
        fields['created'] = sel.xpath('//div[@class="report-heading"]//small/text()').extract_first().split(" • ")[1].replace('Created: ', '')
    except:
        fields['created'] = ''
    try:
        fields['updated'] = sel.xpath('//div[@class="report-heading"]//small/text()').extract_first().split(" • ")[2].replace('Updated: ', '')
    except:
        fields['updated'] = ''
    fields['size'] = sel.xpath('//td[@class="field" and contains(text(), "Project Type")]/following-sibling::td[@class="field-value"]/text()').extract_first()
    fields['construction_type'] = sel.xpath('//td[@class="field" and contains(text(), "Construction Type:")]/following-sibling::td[@class="field-value"]/text()').extract_first()
    fields['estimated_value'] = sel.xpath('//td[@class="field" and contains(text(), "Estimated Value")]/following-sibling::td[@class="field-value"]/text()').extract_first()
    fields['sector'] = sel.xpath('//td[@class="field" and contains(text(), "Sector")]/following-sibling::td[@class="field-value"]/text()').extract_first()
    try:
        fields['location'] = sel.xpath('//td[@class="field" and contains(text(), "Location")]/following-sibling::td[@class="field-value"]/text()').extract()[1]
    except:
        fields['location'] = ''
    fields['details'] = sel.xpath('//td[@class="field" and contains(text(), "Details")]/following-sibling::td[@class="field-value"]/text()').extract_first()
    fields['news'] = sel.xpath('//tbody[@class="news-and-notes"]/tr[2]/td[2]/text()').extract_first()
    fields['construction_type'] = sel.xpath('//td[@class="field" and contains(text(), "Construction Type:")]/following-sibling::td[@class="field-value"]/text()').extract_first()
    fields['stage'] = sel.xpath('//td[@class="field" and contains(text(), "Stage")]/following-sibling::td[@class="field-value"]/text()').extract_first()
    fields['bid_due_date'] = sel.xpath('//td[@class="field" and contains(text(), "Construction Type:")]/following-sibling::td[@class="field-value"]/text()').extract_first()
    fields['lat'] = sel.xpath('//div/@data-val-lat').extract_first()
    fields['log'] = sel.xpath('//div/@data-val-lng').extract_first()
    try:
        fields['address'] = sel.xpath('//td[@class="field" and contains(text(), "Location")]/following-sibling::td[@class="field-value"]/text()').extract()[1]
    except:
        fields['address'] = ''

    try:
        fields['city'] = sel.xpath('//td[@class="field" and contains(text(), "Location")]/following-sibling::td[@class="field-value"]/span/text()').extract()[0]
    except:
        fields['city'] = ''
    try:
        fields['state'] = sel.xpath('//td[@class="field" and contains(text(), "Location")]/following-sibling::td[@class="field-value"]/span/text()').extract()[1]
    except:
        fields['state'] = ''
    try:
        fields['zip'] = sel.xpath('//td[@class="field" and contains(text(), "Location")]/following-sibling::td[@class="field-value"]/text()').extract()[1].split('.')[0]
    except:
        fields['zip'] = ''

    fields['role'] = sel.xpath('//tbody[@class="contact-info"]//tr[2]/td/table/thead/tr/th[text()="Role"]/following-sibling::th[1]/text()').extract_first()
    fields['company'] = sel.xpath('//tbody[@class="contact-info"]//tr[2]/td/table/tbody/tr[1]/td[2]/text()[1]').extract_first()
    fields['contact'] = sel.xpath("//tbody[@class='contact-info']//tr[2]/td/table/tbody/tr[1]/td[3]/span[1]/text()").extract_first()
    fields['phone'] = sel.xpath("//tbody[@class='contact-info']//tr[2]/td/table/tbody/tr[1]/td[5]/text()").extract_first()
    print(fields)

    return fields



try:

    driver = uc.Chrome(version_main = 112)
    cdc_props = driver.execute_script('const j=[];for(const p in window){'
                                      'if(/^[a-z]{3}_[a-zA-Z0-9]{22}_.*/i.test(p)){'
                                      'j.push(p);delete window[p];}}return j;')
    if len(cdc_props) > 0:
        cdc_props_js_array = '[' + ','.join('"' + p + '"' for p in cdc_props) + ']'
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                               {'source': cdc_props_js_array + '.forEach(k=>delete window[k]);'})

    # Navigate to the login page
    driver.get("https://www.constructionwire.com/Login")

    sleep(10)
    email_field = driver.find_element(By.ID, "Email")
    password_field = driver.find_element(By.ID, "Password")

    email_field.send_keys("gdelany@eyzenberg.com")
    password_field.send_keys("EYZenco12!!")

    password_field.send_keys(Keys.RETURN)

    sleep(random.randint(13,34))


    f = open('config.txt', 'r')
    contents = f.read()
    lines = contents.split('\n')
    variables = {}
    for line in lines:
        if line != '':
            name, value = line.split('= ')
            variables[name] = value
    upper_random = int(variables['randomsleepupper'])
    lower_random = int(variables['randomsleeplower'])
    url = variables['URL']
    namesuffix = variables['namesuffix']
    print(variables)

    f.close()

    page = 1
    links = [2]
    data = []
    driver.get(url)
    sleep(random.randint(1, 15))
    sel = Selector(text=driver.page_source)
    driver.find_element(By.XPATH, "//div[@class='btn-group page-size']/button").click()
    sleep(random.randint(10, 30))
    sel = Selector(text=driver.page_source)
    driver.find_element(By.XPATH, '//a[@href="#100"]').click()

    while len(links) != 0:

        max_scrolls = 10
        page_height = driver.execute_script("return document.body.scrollHeight")

        for i in range(max_scrolls):
            scroll_amount = random.uniform(page_height / max_scrolls * i, page_height / max_scrolls * (i + 1))
            driver.execute_script(f"window.scrollTo(0, {scroll_amount});")

        sleep(random.randint(15,40))
        links = sel.xpath("//table//a[@class='title']/@href").extract()

        pagination = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "pagination"))
        )


        # find the next button and click it
        count = 0

        sleep(12)
        buttons = driver.find_elements(By.XPATH, "//span[@title='Preview Item']")
        for button in buttons:
            button.click()
            sleep_time = random.randint(lower_random, upper_random)
            time.sleep(sleep_time)
            print(f"Sleep Time {sleep_time} seconds")
            sel = Selector(text=driver.page_source)
            fields = {}

            count+=1
            print(f"Count {count}")
            print(f"Page {page}")
            fields['SavedSearchName'] = namesuffix


            # ID field needs to be defined to write it in the url. URL field is necessary as second column
            sleep(5)
            extracted_text = sel.xpath('//div[@class="report"]//small/text()').extract_first()
            print(extracted_text)
            if extracted_text is not None:
                match = re.search('Project: (\d+)', extracted_text)
                id = extracted_text.split('#')[1].split(' ')[0]
                #print(match)
                #if match:
                #     id = match.group(1)
                #else:
                #    id = None
            else:
                id = None

            fields['url'] = f'https://www.constructionwire.com/Client/Report/Details/{id.replace("#", "")}?reporttypeid=1'

            fields['title'] = sel.xpath('//div[@class="report"]//span[@class="title"]/text()').extract_first()
            if fields['title'] == "":
                print(sel.xpath('//div)'))
                break
            try:
                fields['id'] = sel.xpath('//div[@class="report"]//small/text()').extract_first().split(" • ")[
                    0].replace('Project: ', '')
            except:
                fields['id'] = ''
            try:
                fields['created'] = \
                sel.xpath('//div[@class="report"]//small/text()').extract_first().split(" • ")[1].replace(
                    'Created: ', '')
            except:
                fields['created'] = ''
            try:
                fields['updated'] = \
                sel.xpath('//div[@class="report"]//small/text()').extract_first().split(" • ")[2].replace(
                    'Updated: ', '')
            except:
                fields['updated'] = ''

            fields['size'] = sel.xpath(
                '//td[@class="field" and contains(text(), "Project Type")]/following-sibling::td[@class="field-value"]/text()').extract_first()
            fields['construction_type'] = sel.xpath(
                '//td[@class="field" and contains(text(), "Construction Type:")]/following-sibling::td[@class="field-value"]/text()').extract_first()
            fields['estimated_value'] = sel.xpath(
                '//td[@class="field" and contains(text(), "Estimated Value")]/following-sibling::td[@class="field-value"]/text()').extract_first()
            fields['sector'] = sel.xpath(
                '//td[@class="field" and contains(text(), "Sector")]/following-sibling::td[@class="field-value"]/text()').extract_first()
            try:
                fields['location'] = sel.xpath(
                    '//td[@class="field" and contains(text(), "Location")]/following-sibling::td[@class="field-value"]/text()').extract()[
                    1]
            except:
                fields['location'] = ''
            fields['details'] = sel.xpath(
                '//td[@class="field" and contains(text(), "Details")]/following-sibling::td[@class="field-value"]/text()').extract_first()
            fields['construction_type'] = sel.xpath(
                '//td[@class="field" and contains(text(), "Construction Type:")]/following-sibling::td[@class="field-value"]/text()').extract_first()
            fields['stage'] = sel.xpath(
                '//td[@class="field" and contains(text(), "Stage")]/following-sibling::td[@class="field-value"]/text()').extract_first()
            fields['constructionStart'] = sel.xpath(
                '//td[@class="field" and contains(text(), "Construction Start:")]/following-sibling::td[@class="field-value"]/text()').extract_first()
            fields['constructionEnd'] = sel.xpath(
                '//td[@class="field" and contains(text(), "Construction End:")]/following-sibling::td[@class="field-value"]/text()').extract_first()
            fields['bid_due_date'] = sel.xpath(
                '//td[@class="field" and contains(text(), "Bid Due Date:")]/following-sibling::td[@class="field-value"]/text()').extract_first()
            fields['news'] = sel.xpath('//tbody[@class="news-and-notes"]/tr[2]/td[2]/text()').extract_first()
            fields['lat'] = sel.xpath('//div/@data-val-lat').extract_first()
            fields['lng'] = sel.xpath('//div/@data-val-lng').extract_first()
            try:
                fields['address'] = sel.xpath(
                    '//td[@class="field" and contains(text(), "Location")]/following-sibling::td[@class="field-value"]/text()').extract()[
                    1]
            except:
                fields['address'] = ''

            try:
                fields['city'] = sel.xpath(
                    '//td[@class="field" and contains(text(), "Location")]/following-sibling::td[@class="field-value"]/span/text()').extract()[
                    0]
            except:
                fields['city'] = ''
            try:
                fields['state'] = sel.xpath(
                    '//td[@class="field" and contains(text(), "Location")]/following-sibling::td[@class="field-value"]/span/text()').extract()[
                    1]
            except:
                fields['state'] = ''
            try:
                fields['zip'] = sel.xpath(
                    '//td[@class="field" and contains(text(), "Location")]/following-sibling::td[@class="field-value"]/text()').extract()[
                    1].split('.')[0]
            except:
                fields['zip'] = ''
            #fields['role'] = sel.xpath(
            #    '//tbody[@class="contact-info"]//tr[2]/td/table/thead/tr/th[text()="Role"]/following-sibling::th[1]/text()').extract_first()
            table_len =  len(sel.xpath('//tbody[@class="contact-info"]//tr[2]/td/table/tbody/tr').extract())
            print(table_len)
            for i in range(1, table_len):
                i = str(i)
                if i != '132':

                    role =  sel.xpath('//tbody[@class="contact-info"]//tr[2]/td/table/tbody/tr['+i+']/td[1]/text()[1]').extract_first()

                    print('role',role)
                    if role == None:
                        role = ""
                        continue
                    if role in fields:
                        continue
                    company = sel.xpath(
                    '//tbody[@class="contact-info"]//tr[2]/td/table/tbody/tr['+i+']/td[2]/text()[1]').extract_first()
                    if company == None:
                        company = ''
                    try:
                        contact_address=  ' '.join(sel.xpath("//tbody[@class='contact-info']//tr[2]/td/table/tbody/tr["+i+"]/td[4]//text()").extract())
                    except:
                        contact_address = ''
                    if contact_address == None:
                        contact_address = ''
                    try:
                        contact = sel.xpath(
                            "//tbody[@class='contact-info']//tr[2]/td/table/tbody/tr["+i+"]/td[3]/span/text()").extract_first()+ sel.xpath(
                            "//tbody[@class='contact-info']//tr[2]/td/table/tbody/tr["+i+"]/td[3]/a/text()").extract_first()
                    except:
                        contact = ""
                    if contact == None:
                        contact = ''
                    phone = sel.xpath(
                        "//tbody[@class='contact-info']//tr[2]/td/table/tbody/tr["+i+"]/td[5]/text()").extract_first()
                    if phone == None:
                        phone = ''
                    if ',' in role:
                        roles = role.split(',')
                        for role in roles:
                            role = role.strip()
                            fields[role] = f'{company}|{contact_address}|{contact}|{phone}'.strip()
                    else:
                        role = role.strip()
                        fields[role] = f'{company}|{contact_address}|{contact}|{phone}'.strip()

                else:
                    continue
                    try:
                        fields['role'] = fields['role'] +';'+ sel.xpath(
                        '//tbody[@class="contact-info"]//tr[2]/td/table/tbody/tr['+i+']/td[1]/text()[1]').extract_first()
                    except:
                        fields['role'] = fields['role'] + ';'
                    try:
                        fields['company'] = fields['company'] +';'+ sel.xpath(
                        '//tbody[@class="contact-info"]//tr[2]/td/table/tbody/tr['+i+']/td[2]/text()[1]').extract_first()+ sel.xpath(
                        "//tbody[@class='contact-info']//tr[2]/td/table/tbody/tr["+i+"]/td[3]/a/text()").extract_first()
                    except:
                        fields['company'] = fields['company'] + ';'

                    try:
                        fields['contact-address'] = fields['contact-address'] +';'+ ' '.join(sel.xpath(
                            "//tbody[@class='contact-info']//tr[2]/td/table/tbody/tr["+i+"]/td[4]//text()").extract())
                    except:
                        fields['contact-address'] =  fields['contact-address'] +';'
                    try:
                        fields['contact'] = fields['contact'] +';'+ sel.xpath(
                        "//tbody[@class='contact-info']//tr[2]/td/table/tbody/tr["+i+"]/td[3]/span/text()").extract_first()
                    except:
                        fields['contact'] = fields['contact'] + ';'

                    try:
                        fields['phone'] = fields['phone'] +';'+ sel.xpath(
                        "//tbody[@class='contact-info']//tr[2]/td/table/tbody/tr["+i+"]/td[5]/text()").extract_first()
                    except:
                        fields['phone'] = fields['phone'] + ';'

            now = datetime.now()
            date_string = now.strftime('%m/%d/%Y')
            fields['scrapedDate'] = date_string
            fields['updatedDate'] = ""
            print(fields)
            data.append(fields)

            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "close-modal"))
            )
            element.click()
        sleep(random.randint(lower_random, upper_random))
        print(f"Sleep Time {sleep} seconds")
        # next_link = driver.find_element(By.CSS_SELECTOR, 'ul.pagination li.active + li a')
        # Chatgpt suggestion 20230518 - Pavel
        try:
            wait = WebDriverWait(driver, 10)  # wait for up to 10 seconds
            next_link = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.pagination li.active + li:not(:last-child) a')))
        except TimeoutException:
            print("Next page link not found after waiting. The last page may have been reached.")
            next_link = None
        if next_link is not None:
            next_link.click()
        else:
            print("next_link is None")


        page+=1
    date = datetime.today().strftime('%Y%m%d_%H%M-')
    filename = date + 'cw-' + namesuffix + '.csv'
    all_keys = data[0].keys()
    all_keys = all_keys + list(set([key for dictionary in data for key in dictionary.keys() if key not in all_keys]))

    print('all keys: ', all_keys)
    with open(filename, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=all_keys)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
except Exception as e:
    all_keys = data[0].keys()
    all_keys = all_keys + list(set([key for dictionary in data for key in dictionary.keys() if key not in all_keys]))

    print('all keys: ', all_keys)
    print('Error:', e)
    date = datetime.today().strftime('%Y%m%d_%H%M-')
    filename = date + 'cw-' + namesuffix + '.csv'
    with open(filename, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=all_keys)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
driver.quit()
