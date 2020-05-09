import os
from selenium.webdriver import Chrome, ChromeOptions
from crawler.utils.html_parsing import *
from crawler.utils.io import *
from selenium.webdriver.support import ui, expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import requests
from time import sleep


def is_visible(driver, xpath, timeout=20):
    """
    Returns true if the element identified by the provided xpath is present within 20 seconds
    :param driver: Selenium driver object
    :param xpath: String containing XML path referencing a DOM object
    :param timeout: Time in seconds to wait for object to appear
    :return:
    """
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        return False


def collect_video_metadata():
    """
    Iterate through each video ID in the provided JSON file.
    Collects various metadata and adds as a property of each video in JSON.
    :return:
    """
    webdriver_path = './chromedriver.exe'
    options = ChromeOptions()

    # Ublock origin must be installed on an existing chrome installation on the machine
    ublock_path = os.environ['UBLOCK_ORIGIN_PATH']

    options.add_argument(f'load-extension=/{ublock_path}')
    driver = Chrome(webdriver_path, options=options)

    status_to_string = ['ended', 'played', 'paused', 'buffered', 'queued', 'unstarted']
    with open('./data/videos_sampling.json') as json_file:
        data = json.load(json_file)
        for video in data:
            print('============================================')
            url = id_to_url(video)
            # Get HTML Content
            res = requests.get(url)
            title = get_title(res.text)
            if title:  # Use the presence of the title element to detect if it has been removed

                # Get HTML Content
                view_count = get_view_count(res.text)
                print(view_count)
                player_type = get_player_type(res.text)
                print(player_type)
                date_published = get_date_published(res.text)
                print(date_published)
                upload_date = get_upload_date(res.text)
                print(upload_date)
                genre = get_genre(res.text)
                print(genre)
                category = get_category(res.text)
                print(category)

                # Get Javascript Content
                driver.implicitly_wait(5)
                driver.get(url)

                length = driver.find_elements_by_xpath('//span[@class="ytp-time-duration"]')[0].text
                print(length)
                sleep(10)
                try:
                    text_elements = driver.find_elements_by_xpath('//*[@id="text"]')
                except AttributeError:
                    text_elements = None
                print(text_elements)
                try:
                    likes = text_elements[2].get_attribute('aria-label').strip(',')
                except (AttributeError, IndexError):
                    likes = None
                print(likes)
                try:
                    dislikes = text_elements[3].get_attribute('aria-label').strip(',')
                except (AttributeError, IndexError):
                    dislikes = None
                print(dislikes)
                try:
                    channel_id = driver.find_elements_by_xpath('//*[@id="text"]/a')[0].get_attribute('href')[-24:]
                except (AttributeError, IndexError):
                    channel_id = None
                print(channel_id)

                # Add collected metadata to dictionary
                if title:
                    data[video]['title'] = title[:-10]
                if view_count:
                    data[video]['views'] = view_count
                if player_type:
                    data[video]['player_type'] = player_type
                if date_published:
                    data[video]['date_published'] = date_published
                if upload_date:
                    data[video]['date_uploaded'] = upload_date
                if likes:
                    data[video]['likes'] = ''.join(char for char in likes if char.isdigit())
                if dislikes:
                    data[video]['dislikes'] = ''.join(char for char in dislikes if char.isdigit())
                if channel_id:
                    data[video]['channel_id'] = channel_id
                if category:
                    data[video]['category'] = category

        dict_to_json('./data/videos_metadata.json', data)


if __name__ == '__main__':
    collect_video_metadata()
