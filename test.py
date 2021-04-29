import requests
import time
import pandas as pd
from math import ceil
from bs4 import BeautifulSoup
from selenium import webdriver
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

df = pd.DataFrame(columns=['Course upload date',
                           'Course upload time', 'Course'])
d = {}

GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

def coursevania_scraper(course_count):
    global df, d
    start = time.time()
    url = 'https://coursevania.com/courses/'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.binary_location = GOOGLE_CHROME_PATH
    chrome_options.headless = True
    driver = webdriver.Chrome(execution_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    driver.get(url)
    count = 0

    while True:
        try:

            load_more = driver.find_element_by_xpath(
                '//*[@id="main"]/div[2]/div[1]/div/div[2]/div/div[2]/a')
            time.sleep(2)
            load_more.click()
            count += 1
            if count*12 + 12 > course_count:
                break

        except:
            print(f"Clicked 'load more' {count} times!")
            break

    soup = BeautifulSoup(driver.page_source, 'lxml')
    actual_courselink_count = 0

    for url in soup.find_all('div', class_='stm_lms_courses__single--title'):

        if actual_courselink_count == course_count:
            print(f'Done extracting {course_count} courses')
            break
        course_name = url.h5.text
        temp_course_link = url.a.get('href')
        soup2 = BeautifulSoup(requests.get(
            temp_course_link).text, 'lxml')
        course_link = soup2.find(
            'div', class_='stm-lms-buy-buttons').a.get('href')

        # from nested_lookup import nested_lookup
        # try:
        #     d2 = json.loads(soup.find('script', {'type': 'application/ld+json'}).string)
        #     course_date, course_time = nested_lookup('dateModified',d2)[0].split('T')

        try:
            course_date, course_time = soup2.find(
                'meta', {'property': 'article:modified_time'}).get('content').split('T')
            course_date = '-'.join(course_date.split('-')[::-1])
            course_time = course_time.split('+')[0]
            hour, mins, _ = course_time.split(':')
            if int(hour) > 12:
                hour = int(hour) - 12
                course_time = f"{hour}:{mins} PM"
            elif int(hour) == 12:
                course_time = f"{hour}:{mins} PM"
            else:
                course_time = f"{hour}:{mins} AM"
        except:
            course_date = course_time = 'NA'

        index = len(df)
        test = f'<a href="{course_link}">{course_name}</a>'
        df.loc[index] = [course_date, course_time, test]
        d[course_name] = course_link
        actual_courselink_count += 1
        if actual_courselink_count % 10 == 0:
            print(
                f"Extracted {actual_courselink_count} udemy links{actual_courselink_count//10 * '.'}")
    end = time.time()
    df.loc[index] = [
        f"Time taken for {actual_courselink_count} course info to be extracted", '-', f"{round(end - start,2)} seconds"]

    return df, d


app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/home", response_class=HTMLResponse)
def home():
    return '''
    <body style="background-color:#E0FFFF;">
    <center><h1>Coursevania course scraper API</h1></center>
    <br><br><br>
    <ul style="font-size:25">
        <li>Used to scrape latest 'n' udemy courses from coursevania.</li>
        <li>Use /table/{num_of_courses} endpoint for tabular output.</li>
        <li>Use /json/{num_of_courses} endpoint for json output.</li>
    </ul>
    </body>
    '''

# https://pandas.pydata.org/pandas-docs/version/0.23.4/generated/pandas.DataFrame.to_html.html


@app.get("/", response_class=HTMLResponse)
def read_item_table_25():
    df, d = coursevania_scraper(25)
    df.index += 1
    with open('index.html') as f:
        s = f.read()
    return s.format(df.to_html(justify="center", escape=False))


@app.get("/json")
def read_item_json_10():
    _, d = coursevania_scraper(10)
    return d


@app.get("/table/{course_num}", response_class=HTMLResponse)
def read_item_table(course_num: int):
    df, _ = coursevania_scraper(course_num)
    df.index += 1
    with open('index.html') as f:
        s = f.read()

    return s.format(df.to_html(justify="center", escape=False))


@app.get("/json/{course_num}")
def read_item_json(course_num: int):
    _, d = coursevania_scraper(course_num)
    return d
