import csv
from bs4 import BeautifulSoup
from selenium import webdriver


# url = 'https://www.amazon.com'
# driver.get(url)


# https://www.amazon.in/s?k=laptop+dell&ref=nb_sb_noss_1
def get_url(search_term):
    """generate a url from search term"""
    template = 'https://www.amazon.in/s?k={}&ref=nb_sb_noss_1'
    search_term = search_term.replace(' ', '+')
    url = template.format(search_term)
    # url += '&page{}'
    return url


# print(results)
# a-size-medium a-color-base a-text-normal
# sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20 sg-col
# sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20 sg-col
# soup = BeautifulSoup(driver.page_source, 'html.parser')
# results = soup.find_all('div', {'class': 'sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20 sg-col'})
# item=results[0]
# atag=item.h2.a
# description=atag.text.strip()
# url='https://www.amazon.com'+atag.get('href')
# 
# 
# price_parent=item.find('span','a-price')
# price=price_parent.find('span','a-offscreen').text
# 
# rating=item.i.text
# review=item.ind('span',{'class': 'a-size-base', 'dir': 'auto'}).text
# print(description)


# extracting the data format

def extract_data_pattern(item):
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.com' + atag.get('href')

    print(description)
    print(url)

    try:
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
        price=price[1:]
        price=int("".join([char for char in price if char != ","]))

    except:
        price = 'NA'
        print(price)

    try:
        rating = item.i.text
        print(rating)
        # review = item.ind('span', {'class': 'a-size-base', 'dir': 'auto'}).text
    except:
        rating = 'NA'
        # review = ''
        print(rating)
    result = [description, price, rating, url]
    print('namaste')
    return result


# extracting main url component

# soup = BeautifulSoup(driver.page_source, 'html.parser')
# results = soup.find_all('div', {'class': 'sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20 sg-col'})
# records = []
# for item in results:
#     record=extract_data_pattern(item)
#     records.append(record)


def main(search_term):
    driver = webdriver.Chrome('/home/saksham/Downloads/chromedriver')
    records = []
    url = get_url(search_term)
    # print(url)
    # driver.get(url)
    # for page in range(1, 21):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all('div', {'class': 'sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20 sg-col'})
    count = 0
    print(len(results), 'resutsprint')
    for items in results:
        record = extract_data_pattern(items)
        if record and count % 2 == 0:
            records.append(record)
        count += 1

    print(str(len(records)) + 'records line')
    driver.close()

    # storing in .csv file
    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['Description', 'Price', 'Rating', 'Url'])
        writer.writerows(records)


#var1 = 'dell laptop'
var = input()
main(var)
