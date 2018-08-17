"""
Wallpaper downloader for santabanta.com
"""

from urllib import request
from urllib.error import HTTPError
from bs4 import BeautifulSoup as soup
import os


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
    return html


def count_wallpapers(arg):
    """
    Counts all the wallpaper associated with given category
    creates list of all the links in the pagination of given wallpaper category
    :param arg: search query from user
    :return: wallpaper count and list of links
    """

    try:
        main_html = send_request(arg)
        main_soup = soup(main_html, 'html.parser')
        domain = 'http://www.santabanta.com'
        l_list = []
        paginate = main_soup.find('div', {'class': 'paging-div-new'})
        dot = paginate.find('a', {'class': 'dots'})

        for a in paginate.find_all('a', href=True):
            if not a.span:
                page_links = a['href']
                full_page_links = domain + page_links
                l_list.append(full_page_links)

        if dot:
            pre_link = dot.find_previous('a')['href']
            pre_page_number = dot.find_previous('a')['href'][-1]
            next_page_number = dot.find_next('a')['href'][-2:]
            no_number_pre_page = pre_link.rstrip('0123456789')

            while int(pre_page_number) < int(next_page_number):
                pre_page_number = int(pre_page_number) + 1
                pre_link = no_number_pre_page + str(pre_page_number)
                if int(pre_page_number) == int(next_page_number):
                    continue
                missing_page = domain + pre_link
                l_list.append(missing_page)

        wall_count = len(l_list) * 18 + 19
        return l_list, wall_count

    except AttributeError:
        pass


def santabanta_downloader(arg):

    """
    download all the wallpapers in given catagory
    :param arg: wallpaper category in the form of string to be used with url
    :param arg2: Plain query string entered by the user
    :return:
    """

    link_list, _ = count_wallpapers(search)
    main_html = send_request(arg)
    main_soup = soup(main_html, 'html.parser')
    div = main_soup.find('div', {'class': 'wallpaper-big-1 position-rel'})
    try:

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
            folder_name = arg.replace('-', ' ')
            download_path = os.path.join(f'Wallpapers/{folder_name.capitalize()}/')
            os.makedirs(download_path, exist_ok=True)
            request.urlretrieve(image, download_path + img_name + '.jpg')
            print(f'Downloading... {img_name}')

    except TypeError:
        print("Downloading finished!")
        
    for link in link_list:
        next_page = request.urlopen(link).read()
        next_soup = soup(next_page, 'html.parser')

        div = next_soup.find('div', {'class': 'wallpaper-big-1 position-rel'})

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
            download_path = os.path.join(f'Wallpapers/{folder_name.capitalize()}/')
            os.makedirs(download_path, exist_ok=True)
            request.urlretrieve(image, download_path + img_name + '.jpg')
            print(f'Downloading... {img_name}')


def santabanta(arg):
    main_html = send_request(arg)
    main_soup = soup(main_html, 'html.parser')
    div = main_soup.find('div', {'class': 'wallpaper-big-1 position-rel'})

    try:

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
            folder_name = arg.replace('-', ' ')
            download_path = os.path.join(f'Wallpapers/{folder_name.capitalize()}/')
            os.makedirs(download_path, exist_ok=True)
            request.urlretrieve(image, download_path + img_name + '.jpg')
            print(f'Downloading... {img_name}')

    except TypeError:
        print('Downloading finished')


if __name__ == '__main__':

    try:

        query = input(str("Enter the category name you want to download (eg: 'Dia Mirza): "))
        search = query.replace(' ', '-').lower()

        if not count_wallpapers(search):
            print("Only one page found")
            choice = input(str("For start downloading hit enter"))
            if choice == '':
                santabanta(search)
        else:
            _, wallpaper_count = count_wallpapers(search)
            print(f"{wallpaper_count} Wallpapers found")
            choice = input(str("For start downloading hit enter"))
            if choice == '':
                santabanta_downloader(search)

    except NameError:
        print("Please enter the category name")

    except HTTPError:
        print("Page not found, please try again")

    except AttributeError:
        print("Something went wrong, please try again")
