
import pandas as pd
from bs4 import BeautifulSoup as soup
import csv
import requests
from datetime import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

def gwrite_to_google_sheet(i, id, postCard_name, postcard_host, postcard_Description, category, no_of_epsiode, start_date, ArtWork, website, email,
                    rss_Feed, language, latest_publish_Epsiode_Date, itune_link, latest_publish_Epsiode_Title, recent_pupliched_on_Last_6_weeks, rating):

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive',
             'https://www.googleapis.com/auth/spreadsheets.currentonly']
    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open('sample_test1')
    if i == 0:
        global title
        title = datetime.today().strftime("%Y%m%d%H%M%S%f")        #datetime.strftime('%Y%m%d%H%M%S%f')
        new_sheet = sheet.add_worksheet(title=title, rows=5, cols=21)
        row = ['Select', 'ID', 'Post Card Name', 'Post Card Host Name', 'Post Card Description', 'CATEGOURY', 'No. Of Epsiodes', 'Start Date', 'ArtWork', 'Website',
                'Email', 'Rss Feed', 'Language', 'Latest Publish Epsiode Date', 'iTune Link', 'Latest Publish Epsiode Title', 'Recent Pupliched On Last 6 Weeks', 'Rating']
        new_sheet.append_row(row)
    else:
        new_sheet = sheet.worksheet(title)
        row = [id, postCard_name, postcard_host, postcard_Description, category, no_of_epsiode, start_date, ArtWork, website, email, rss_Feed,
                 language, latest_publish_Epsiode_Date, itune_link, latest_publish_Epsiode_Title, recent_pupliched_on_Last_6_weeks, rating]
        new_sheet.append_row(row)


'''
def write_to_csv(j, id, postCard_name, postcard_host, postcard_Description, category, no_of_epsiode, start_date, ArtWork, website, email, rss_Feed,
                 language, latest_publish_Epsiode_Date, itune_link, latest_publish_Epsiode_Title, recent_pupliched_on_Last_6_weeks, rating):
    select = True
    if j == 0:
        global file_name
        global objDF
        file_name = 'itune_scrap.csv'
        objDF = pd.DataFrame(columns=['Select', 'ID', 'Post Card Name', 'Post Card Host Name', 'Post Card Description', 'CATEGOURY', 'No. Of Epsiodes', 'Start Date', 'ArtWork', 'Website',
                    'Email', 'Rss Feed', 'Language', 'Latest Publish Epsiode Date', 'iTune Link', 'Latest Publish Epsiode Title', 'Recent Pupliched On Last 6 Weeks', 'Rating'])
        objDF.to_csv(file_name)

    objDF = objDF.append({'Select': select, 'ID': id, 'Post Card Name': postCard_name, 'Post Card Host Name': postcard_host, 'Post Card Description': postcard_Description,
                'CATEGOURY': category, 'No. Of Epsiodes': no_of_epsiode, 'Start Date': start_date, 'ArtWork': ArtWork, 'Website': website, 'Email': email, 'Rss Feed': rss_Feed,
                'Language': language, 'Latest Publish Epsiode Date': latest_publish_Epsiode_Date, 'iTune Link': itune_link, 'Latest Publish Epsiode Title': latest_publish_Epsiode_Title,
                'Recent Pupliched On Last 6 Weeks': recent_pupliched_on_Last_6_weeks, 'Rating': rating}, ignore_index=True)
    objDF.to_csv(file_name)
'''

def html_parser(j, url):
    item_list = []
    global li
    req = requests.get(url)
    _page_soup = soup(req.content, 'html.parser')
    if j == 0:
        ur = _page_soup.find('ul', {'class': 'list column first'}).find('a')['href']
        html_parser(1, ur)
    elif j == 1:
        list_1 = _page_soup.find('ul', attrs={'class': 'list column first'}).findAll('li')
        list_2 = _page_soup.find('ul', attrs={'class': 'list top-level-subgenres'}).findAll('li')
        li = [i for i in list_1 + list_2 if i not in list_1 or i not in list_2]

    elif j == 3:
        li = _page_soup.find('ul', attrs={'class' : 'list top-level-subgenres'}).findAll('li')

    elif j == 4:
        li = _page_soup.find('div', attrs={'id': 'selectedcontent'}).findAll('li')
    else:
        li = _page_soup

    item_list = li
    return item_list

def main():
    i = 0
    main_url = 'https://podcasts.apple.com/us/genre/podcasts/id26'

    cat_01_list = html_parser(0, main_url)
    for inex1, item1 in enumerate(cat_01_list):
        try:
            cat_1 = item1.find('a').text
            cat_1_url = item1.find('a')['href']

            cat_2_list = html_parser(3, cat_1_url)
            for inex2, item2 in enumerate(cat_2_list):      #for Loop
                try:
                    cat_2 = item2.find('a').text
                    cat_2_url = item2.find('a')['href']

                    cat_3_list = html_parser(4, cat_2_url)
                    for inex3, item3 in enumerate(cat_3_list):          # for Loop
                        try:
                            cat_3 = item3.find('a').text
                            cat_3_url = item3.find('a')['href']

                            cat_4_list = html_parser(5, cat_3_url)
                            id=''
                            postCard_name = cat_3
                            postcard_host = cat_4_list.find('span', attrs={'class': 'product-header__identity podcast-header__identity'}).find('a').text.strip()
                            postcard_Description = cat_4_list.findAll('p')[1].text
                            category = cat_1
                            no_of_epsiode = cat_4_list.find('div', attrs={'class': 'product-artwork__caption small-hide medium-show'}).text.strip()
                            start_date = ''
                            ArtWork = ''
                            website = ''
                            email = ''
                            rss_Feed = ''
                            language = ''
                            latest_publish_Epsiode_Date = cat_4_list.find('ol', attrs={'class': 'tracks tracks--linear-show'}).find('time').text
                            itune_link = cat_3_url
                            latest_publish_Epsiode_Title = cat_4_list.find('ol', attrs={'class': 'tracks tracks--linear-show'}).find('a').text.strip()
                            recent_pupliched_on_Last_6_weeks = ''            # (Calculate :----  from ' latest_publish_Epsiode_Date ' in rarge : Y/N )
                            rating = cat_4_list.find('span', attrs={'class': 'we-star-rating-stars we-star-rating-stars-5'}).text.strip()

                            gwrite_to_google_sheet(i, id, postCard_name, postcard_host, postcard_Description, category, no_of_epsiode, start_date, ArtWork, website, email, rss_Feed,
                                          language, latest_publish_Epsiode_Date, itune_link, latest_publish_Epsiode_Title, recent_pupliched_on_Last_6_weeks, rating)
                            i += 1
                            
                        except Exception:
                            pass
                except Exception:
                    pass
        except Exception:
            pass

if __name__ == '__main__':
    main()


