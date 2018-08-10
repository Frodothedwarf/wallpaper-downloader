"""
Wallpaper downloader for santabanta.com
"""

from urllib import request
from urllib.error import HTTPError
from bs4 import BeautifulSoup as soup
import os
import re


def send_request(arg):
    """
    Send request to host with given searched query
    :param arg:
    :return:
    """
    url = f'http://www.santabanta.com/wallpapers/{arg}/'
    req = request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    html = request.urlopen(req).read()
    make_soup = soup(html, 'html.parser')
    return make_soup


def santabanta_downloader(arg, arg2):

    """
    download all the wallpapers in given catagory
    :param arg: wallpaper category in the form of string to be used with url
    :param arg2: Plain query string entered by the user
    :return:
    """

    div = send_request(arg).find('div', {'class': 'wallpaper-big-1 position-rel'})

    for item in div.find_all('div', {'class': 'wallpapers-box-300x180-2 wallpapers-margin-2'}):
        img_page_half_link = item.find('a')['href']
        img_page_full_link = 'http://www.santabanta.com' + img_page_half_link
        inner_html = request.urlopen(img_page_full_link).read()
        make_soup = soup(inner_html, 'html.parser')
        social_bar = make_soup.find('div', {'class': 'social-bar-2a wall-right-links a'})
        res = social_bar.find_all('a')[-1]['href']
        higher_req = request.urlopen('http://www.santabanta.com' + res).read()
        higher_soup = soup(higher_req, 'html.parser')

        full_img_url = higher_soup.find('div', {'class': 'wallpaper-big-1-img width-video-new-2 lazy'})
        image = full_img_url.find('a')['href']
        img_name = full_img_url.find('a')['download']
        download_path = os.path.join(f'Wallpapers/{arg2.capitalize()}/')
        os.makedirs(download_path, exist_ok=True)
        request.urlretrieve(image, download_path + img_name + '.jpg')
        print(f'Downloading: {img_name}')


def count_wallpapers(arg):
    """
    function to calculate all the wallpapers found of searched query
    it digs all the pages of category.
    :param arg: takes urls of all the valid pages.
    :return: total count of wallpapers found.
    """
    print("Page found")
    print("Calculating wallpapers...")
    domain = 'http://www.santabanta.com'
    paginate = send_request(arg).find('div', {'class': 'paging-div-new'})
    link_list = []
    total_wallpaper = []
    for a in paginate.find_all('a', href=True):
        if not a.span:
            page_links = a['href']
            full_page_links = domain + page_links
            link_list.append(full_page_links)

    for link in link_list:
        visit = request.urlopen(link)

        make_soup = soup(visit, 'html.parser')
        div = make_soup.find('div', {'class': 'wallpaper-big-1 position-rel'})
        all_img = div.find_all('div', {'class': 'wallpapers-box-300x180-2 wallpapers-margin-2'})
        total_wallpaper.append(all_img)

        # print(len(all_img))

    page_count = len(link_list)

    wallpaper_count = page_count * 18 + 19
    return wallpaper_count


if __name__ == '__main__':

    try:
        query = input(str("Enter the category name you want to download (eg: 'Dia Mirza): "))
        query_lower = query.lower()
        dashed_query = re.sub(' ', '-', query_lower)

        if count_wallpapers(dashed_query):
            wall_count = count_wallpapers(dashed_query)
            print(f"{wall_count} Wallpapers found")
            choice = input(str("For start downloading hit enter"))
            if choice == '':
                santabanta_downloader(dashed_query, query)

    except NameError:
        print("Please enter the category name")

    except HTTPError:
        print("Page not found, please try again")

    except AttributeError:
        print("Something went wrong, please try again")
