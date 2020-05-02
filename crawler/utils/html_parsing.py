from bs4 import BeautifulSoup
import lxml


def get_title(html_string):
    """
    Return video title as a string
    :param html_string: Web page HTML content
    :return:
    """
    soup = BeautifulSoup(html_string, 'lxml')
    try:
        return soup.title.string
    except TypeError:
        return None


def get_view_count(html_string):
    """
    Return number of video views
    :param html_string: Web page HTML content
    :return:
    """
    soup = BeautifulSoup(html_string, 'lxml')
    try:
        return int(soup.select_one('meta[itemprop="interactionCount"][content]')['content'])
    except TypeError:
        return None


def get_player_type(html_string):
    """
    Return player type
    :param html_string: Web page HTML content
    :return:
    """
    soup = BeautifulSoup(html_string, 'lxml')
    try:
        return soup.select_one('meta[itemprop="playerType"][content]')['content']
    except TypeError:
        return None


def get_date_published(html_string):
    """
    Return date video was published to YouTube in the form YEAR-MONTH-DAY
    :param html_string: Web page HTML content
    :return:
    """
    soup = BeautifulSoup(html_string, 'lxml')
    try:
        return soup.select_one('meta[itemprop="datePublished"][content]')['content']
    except TypeError:
        return None


def get_upload_date(html_string):
    """
    Return date video was uploaded to YouTube in the form YEAR-MONTH-DAY
    :param html_string: Web page HTML content
    :return:
    """
    soup = BeautifulSoup(html_string, 'lxml')
    try:
        return soup.select_one('meta[itemprop="uploadDate"][content]')['content']
    except TypeError:
        return None


def get_genre(html_string):
    """
    Return genre of video
    :param html_string: Web page HTML content
    :return:
    """
    soup = BeautifulSoup(html_string, 'lxml')
    try:
        return soup.select_one('meta[itemprop="uploadDate"][content]')['content']
    except TypeError:
        return None


def get_category(html_string):
    """
    Return category of video
    :param html_string: Web page HTML content
    :return:
    """
    soup = BeautifulSoup(html_string, 'lxml')
    try:
        temp = soup.find_all("div", id="content")
        for item in temp:
            pos = item.text.find("Category")
            if pos != -1:
                temp2 = item.text[pos:-1]
                return temp2.split("\n")[3]
            else:
                return "Unable to Find Category"
    except AttributeError:
        return None


def id_to_url(video_id):
    """
    Get the full video URL for the provided ID.
    :param html_string: Web page HTML content
    :return:
    """
    return f'https://www.youtube.com/watch?v={video_id}'


def get_video_paths(html_string):
    """
    Get a list of all video URLs on a page
    :param html_string: Web page HTML content
    :return:
    """
    video_paths = []
    soup = BeautifulSoup(html_string, 'lxml')
    href_containers = soup.find_all('a', href=True)
    for container in href_containers:
        href = container['href']
        if '/watch?v=' in href:
            video_paths.append(href)
    return video_paths


def get_video_ids(html_string):
    """
    Get a list of all video IDs on a page
    :param html_string: Web page HTML content
    :return:
    """
    video_ids = set()
    soup = BeautifulSoup(html_string, 'lxml')
    href_containers = soup.find_all('a', href=True)
    for container in href_containers:
        href = container['href']
        if '/watch?v=' in href:
            video_id = href[-11:]
            if '=' not in video_id:
                video_ids.add(href[-11:])
    return video_ids


