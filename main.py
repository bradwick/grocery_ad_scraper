# This is a sample Python script.
import re

import requests as requests
from bs4 import BeautifulSoup


# Press ⌃R to execute it or replace it with your code.


def get_items_publix(soup):
    units = soup.select(".unitB")

    this_pages_deals = []
    for unit in units:
        title = unit.findChild("div",{"class":"title"}).text.strip()
        deal = unit.findChild("div",{"class":"deal"}).text.strip()
        this_pages_deals.append({"store":"Publix", "title":title, "deal":deal})
    return this_pages_deals


def scrape_publix():
    url = 'https://accessibleweeklyad.publix.com/PublixAccessibility/BrowseByPage?storeid=2729424'

    r = requests.get(url)
    print(r.is_redirect)
    soup = BeautifulSoup(r.content, features="html.parser")


    page_counts = soup.select('.pageXofY')
    page_count = page_counts[0]
    page_count = re.findall("Page \d of (\d+)", page_count.text)
    page_count = int(page_count[0])

    a = [x['href'] for x in soup.findAll(href=True)]
    promo_id = None
    for link in a:
        promo_id = re.findall("PromotionID=(\d+)", link)
        if promo_id:
            break


    deals = get_items_publix(soup)

    for x in range(2, page_count+1):
        url = f'https://accessibleweeklyad.publix.com/PublixAccessibility/BrowseByPage?PromotionID={promo_id}&PromotionViewMode=1&StoreID=2729424&PageNumber=3&BreadCrumb=Weekly+Ad&SneakPeek=N'
        soup = BeautifulSoup(r.content, features="html.parser")
        deals.extend(get_items_publix(soup))

    return deals


def get_items_food_city(soup):
    cards = soup.select(".card-text")

    this_pages_deals = []

    for card in cards:
        deal = card.findChild("span",{"class":"tile-item__product__price"}).attrs['data-price']
        title = card.findChild("div",{"class":"tile-item__product__title"}).get_text(" ",strip=True)

        this_pages_deals.append({"store":"FoodCity", "title":title, "deal":deal})

    return this_pages_deals

def scrape_food_city():
    url = 'https://www.foodcity.com/index.php?vica=ctl_circulars&vicb=showWeeklyCirculars&vicc=p&StoreNum=716'
    r = requests.get(url)
    soup = BeautifulSoup(r.content,features="html.parser")

    item_count = soup.select(".search-filters__results-count .text-secondary")
    item_count = int(item_count[0].text)

    deals = get_items_food_city(soup)

    page_count = 1
    while len(deals) < item_count:
        url = f'https://www.foodcity.com/index.php?vica=ctl_circulars&vicb=showWeeklyCirculars&vicc=p&StoreNum=716&page={page_count}'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, features="html.parser")
        deals.extend(get_items_food_city(soup))

        page_count += 1

    return deals


def aldi_get_items(json):
    list = json['data']['listings']['list']

    deals = []

    for item in list:
        if 'Non-Food' not in [x['name'] for x in item['departments']]:
            deals.append({"store": "ALDI", "title": item['title'], "deal": item['deal']+(' '+item['priceQualifier'] if item['priceQualifier'] else '')})

    return deals

def aldi_graphql():
    deals = []
    url = 'https://graphql-cdn-slplatform.liquidus.net'

    data = {
        "operationName": "checkSavedListings",
        "variables": {
            "limit": 1000,
            "listingID": "",
            "previewHash": None,
            "require": "posted",
            "campaignid": "955ba004cd1e8395",
            "storeid": "2717863",
            "storeref": "undefined",
            "countryid": 1,
            "languageid": 1,
            "env": "undefined"
        },
        "query": "query checkSavedListings($listingID: String, $previewHash: String, $require: String, $limit: Int, $campaignid: String, $storeid: String, $storeref: String, $countryid: Int, $languageid: Int, $env: String) {\n  listings(listingID: $listingID, previewHash: $previewHash, require: $require, limit: $limit, campaignid: $campaignid, storeid: $storeid, storeref: $storeref, countryid: $countryid, languageid: $languageid, env: $env) {\n    list {\n      ...ListingBase\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment ListingBase on Listing {\n  id\n  imageURL(imageWidth: 325, previewHash: $previewHash, require: $require)\n  originalDeal\n  deal\n  title\n  finalPrice\n  buyOnlineLinkURL\n  saleStartDateString\n  saleEndDateString\n  postStartDateString\n  postEndDateString\n  previewPostStartDateString\n  priceQualifier\n  additionalDealInformation\n  description\n  productDescription\n  customProductDescription\n  finePrint\n  onlineProductCode\n  retailerProductCode\n  languageID\n  rating {\n    id\n    averageRating\n    ratingRange\n    reviewsURL\n    totalReviews\n    writeReviewURL\n    __typename\n  }\n  store {\n    id\n    referenceNumber\n    __typename\n  }\n  tags {\n    id\n    name\n    __typename\n  }\n  departments {\n    id\n    name\n    level\n    __typename\n  }\n  napi\n  __typename\n}\n"
    }

    r = requests.post(url, json=data)
    return aldi_get_items(r.json())



if __name__ == '__main__':
    deals = []
    deals.extend(scrape_publix())
    deals.extend(scrape_food_city())
    deals.extend(aldi_graphql())

    for deal in deals:
        print(deal)

