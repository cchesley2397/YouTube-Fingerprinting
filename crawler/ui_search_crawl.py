from crawler.utils.html_parsing import *
from crawler.utils.io import *
from concurrent.futures import as_completed, ThreadPoolExecutor
import requests


def add_url_to_queue(url, urls_to_crawl, urls_crawled):
    """
    Add url to crawl queue
    :param url:
    :param urls_to_crawl:
    :param urls_crawled:
    :return:
    """
    if url not in urls_crawled and url not in urls_to_crawl:
        urls_to_crawl.append(url)
    return urls_to_crawl


def search_videos(keyword):
    """
    Returns a list of video ids found on page
    :param keyword:
    :return:
    """
    search_url = 'https://youtube.com/results?search_query='
    response = requests.get(f'{search_url}{keyword}')
    return get_video_ids(response.text)


def generate_keyword_urls():
    """
    Generate a list of keyword strings from a text file.
    For each keyword, submit a search to youtube and collect all video IDs found on page.
    Generate a valid URL for each video and write to a text file.

    Run this to generate a list of starting URLs for crawl_by_ui_search
    :return:
    """
    keywords = text_file_to_list('./data/hrefs_popular_yt_keywords_us.txt')
    keyword_urls = []
    for keyword in keywords:
        results = search_videos(keyword)
        for result in results:
            url = id_to_url(result)
            if url not in keyword_urls:
                keyword_urls.append(url)
    list_to_text_file('./data/us_keyword_urls.txt', keyword_urls)


def crawl_by_ui_search():
    """
    For each link in the queue, collect all unvisited video URLs and add them to the queue.
    :return:
    """
    videos_found = {'videos': {}}

    urls_to_crawl = []
    urls_crawled = []
    keyword_urls = text_file_to_list('./data/us_keyword_urls.txt')
    for url in keyword_urls:
        add_url_to_queue(url, urls_to_crawl, urls_crawled)
    while len(urls_to_crawl) > 0:
        with ThreadPoolExecutor(max_workers=30) as executor:
            futures = {executor.submit(requests.get, url): url for url in urls_to_crawl}
            for future in as_completed(futures):
                response = future.result()

                url = futures[future]
                view_count = get_view_count(response.text)
                if view_count:
                    if view_count >= 10000:  # Threshold for ignoring videos by view count
                        video_ids = get_video_ids(response.text)
                        for video_id in video_ids:
                            add_url_to_queue(id_to_url(video_id), urls_to_crawl, urls_crawled)
                    videos_found['videos'][url[-11:]] = {'views': view_count}
                if len(videos_found['videos']) % 100 == 0:
                    dict_to_json('./data/videos.json', videos_found)
                urls_crawled.append(url)
        urls_to_crawl = list(set(urls_to_crawl) - set(urls_crawled))
        print(videos_found)
        dict_to_json('./data/videos.json', videos_found)


if __name__ == '__main__':
    crawl_by_ui_search()
