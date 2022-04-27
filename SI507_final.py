
from cgi import test
from bs4 import BeautifulSoup
import requests
import time
import json
"""
BASE_URL = 'https://www.lego.com'
LOCATION_PATH = '/en-us'
CATEGORY= '/categories/'
AGES = ['age-1-plus-years', 'age-4-plus-years', 'age-6-plus-years', 'age-9-plus-years', 'age-13-plus-years', 'age-18-plus-years']
CACHE_FILE_NAME = 'Lego_Scrape.json'
CACHE_DICT = {}


def load_cache():
    try:
        cache_file = open(CACHE_FILE_NAME, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache

def save_cache(cache):
    cache_file = open(CACHE_FILE_NAME, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()

def make_url_request_using_cache(url, cache):
    if (url in cache.keys()): # the url is our unique key
        #print("Using cache")
        return cache[url]
    else:
        #print("Fetching")
        time.sleep(1)
        response = requests.get(url)
        cache[url] = response.text
        save_cache(cache)
        return cache[url]

# Load the cache, save in global variable
CACHE_DICT = load_cache()

web_page = {'age-1-plus-years':[],'age-4-plus-years':[],'age-6-plus-years':[],
          'age-9-plus-years':[],'age-13-plus-years':[],'age-18-plus-years':[]}
result = {'age-1-plus-years':[],'age-4-plus-years':[],'age-6-plus-years':[],'age-9-plus-years':[],'age-13-plus-years':[],'age-18-plus-years':[]}
for AGE in AGES:
    if AGE == 'age-1-plus-years':
        for i in range(1,11):
            lego_search_url = BASE_URL + LOCATION_PATH + CATEGORY + AGE +'?page=' + str(i)
            web_page['age-1-plus-years'].append(lego_search_url)
    if AGE == 'age-4-plus-years':
        for i in range(1,16):
            lego_search_url = BASE_URL + LOCATION_PATH + CATEGORY + AGE +'?page=' + str(i)
            web_page['age-4-plus-years'].append(lego_search_url)
    if AGE == 'age-6-plus-years':
        for i in range(1,50):
            lego_search_url = BASE_URL + LOCATION_PATH + CATEGORY + AGE +'?page=' + str(i)
            web_page['age-6-plus-years'].append(lego_search_url)
    if AGE == 'age-9-plus-years':
        for i in range(1,44):
            lego_search_url = BASE_URL + LOCATION_PATH + CATEGORY + AGE +'?page=' + str(i)
            web_page['age-9-plus-years'].append(lego_search_url)
    if AGE == 'age-13-plus-years':
        for i in range(1,7):
            lego_search_url = BASE_URL + LOCATION_PATH + CATEGORY + AGE +'?page=' + str(i)
            web_page['age-13-plus-years'].append(lego_search_url)
    if AGE == 'age-18-plus-years':
        for i in range(1,9):
            lego_search_url = BASE_URL + LOCATION_PATH + CATEGORY + AGE +'?page=' + str(i)
            web_page['age-18-plus-years'].append(lego_search_url)



for ages in web_page.keys():
    for web_pages in web_page[ages]:
        url_text = make_url_request_using_cache(web_pages, CACHE_DICT)
        soup = BeautifulSoup(url_text, 'html.parser')


        lego_listing_parent = soup.find('ul', class_='ProductGridstyles__Grid-lc2zkx-0 gxucff')
        lego_listing_divs = lego_listing_parent.find_all('li')

        for lego_listing_div in lego_listing_divs:
            useful_product_leaf = lego_listing_div.find('div', class_ = 'ProductLeafSharedstyles__Wrapper-sc-1epu2xb-0 ProductLeafListingstyles__Wrapper-sc-19n1otk-0 hQdRgg')\
                .find('div', class_ = 'ProductLeafSharedstyles__DetailsRow-sc-1epu2xb-4 hqZHOj')
            lego_url = 'https://www.lego.com' + useful_product_leaf.find('a')['href']
            lego_name = useful_product_leaf.find('h2', class_='Text__BaseText-sc-178efqu-0 fUTvnf ProductLeafSharedstyles__Title-sc-1epu2xb-9 iqocOo')\
                .find('span', class_ = 'Markup__StyledMarkup-ar1l9g-0 hlipzx')
            lego_rating = useful_product_leaf.find('div', class_ = 'ProductLeafListingstyles__RatingRow-sc-19n1otk-4 fnMajt').find('span',class_ = 'VisuallyHidden-sc-1dwqwvm-0 gREPpa')
            lego_price = lego_listing_div.find('div', class_ = 'ProductLeafSharedstyles__PriceRow-sc-1epu2xb-10 fEzYBd').find('span', class_ = 'Text__BaseText-sc-178efqu-0 cVmQPV ProductPricestyles__StyledText-vmt0i4-0 eGdbAY')

            # print('URL: ',lego_url)
            # print('Name: ',lego_name.text.strip())
            try:
                if lego_rating.text[15] != '.':
                    # print('Rating: ',lego_rating.text[14]+'/'+ lego_rating.text[22])
                    lego_rating_revised = lego_rating.text[14]+'/'+ lego_rating.text[22]
                else:
                    # print('Rating: ',lego_rating.text[14:17]+'/'+ lego_rating.text[24])
                    lego_rating_revised = lego_rating.text[14:17]+'/'+ lego_rating.text[24]
            except:
                # print('Rating: Not Available')
                lego_rating_revised = 'Not Available'
            try:
                # print('Price: ',lego_price.text[5:])
                lego_price_revised = lego_price.text[5:]
            except:
                try:
                    # print('Price: ',lego_listing_div.find('div', class_ = 'ProductLeafSharedstyles__PriceRow-sc-1epu2xb-10 fEzYBd').find('span', class_ = 'Text__BaseText-sc-178efqu-0 fGdHAO').text[10:])
                    lego_price_revised = lego_listing_div.find('div', class_ = 'ProductLeafSharedstyles__PriceRow-sc-1epu2xb-10 fEzYBd').find('span', class_ = 'Text__BaseText-sc-178efqu-0 fGdHAO').text[10:]
                except:
                    # print('Price: Please call the shopping assistant for getting the price')
                    lego_price_revised = 'Please call the shopping assistant for getting the price'
            
            url_text_child = make_url_request_using_cache(lego_url, CACHE_DICT)
            soup_child = BeautifulSoup(url_text_child, 'html.parser')

            product_detail = soup_child.find('div', class_ = 'ProductDetailsPagestyles__ProductOverviewLayout-sc-1waehzg-2 eCGWiU')
            try:
                status = product_detail.find('p', class_='Text__BaseText-sc-178efqu-0 fNGpzM ProductOverviewstyles__AvailabilityStatus-sc-1a1az6h-11 ejRirH').find('span', class_ = 'Markup__StyledMarkup-ar1l9g-0 hlipzx')
                # print('Status: ',status.text.strip())
                status_revised = status.text.strip()
            except:
                # print('Status: Not Available')
                status_revised = 'Not available'

            try:
                output = []
                pieces_div = product_detail.find('div', class_='ProductAttributesstyles__Container-sc-1sfk910-0 ecavSs')\
                    .find_all('div', class_='ProductAttributesstyles__AttributeWrapper-sc-1sfk910-1 hQBJju')
                string =''
                for i in pieces_div[1]:
                    string += str(i)

                if "pieces-value" in string:
                    pieces = pieces_div[1].find('span', class_ = 'Markup__StyledMarkup-ar1l9g-0 hlipzx')
                    # print('Amounts of Pieces: ',pieces.text)
                    amount_pieces_revised = pieces.text
                else:
                    # print('Amounts of Pieces: Not Available') 
                    amount_pieces_revised = 'Not Available'

            except:
                # print('Amounts of Pieces: Not Available') 
                amount_pieces_revised = 'Not Available'
            # print('-' * 80)


            result[ages].append({'URL':lego_url, 'Name':lego_name.text, 'Rating':lego_rating_revised, 'Price':lego_price_revised, 'Status': status_revised, 'Pieces':amount_pieces_revised})


# for items in result['age-1-plus-years']:
#     print(items)

# print(result['age-1-plus-years'])

# cache_file = open('result_Lego.json', 'w')
# contents_to_write = json.dumps(result)
# cache_file.write(contents_to_write)
# cache_file.close()
"""
lego_file = open('result_Lego.json', 'r')
cache_lego_contents = lego_file.read()
lego_cache = json.loads(cache_lego_contents)
i = 0
for items in lego_cache["age-4-plus-years"]:
    i += 1
print(i)


