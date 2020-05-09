# YouTube-Fingerprinting
YouTube fingerprinting scripts for Capstone 2020

## Crawler

A Python based web crawler for scraping YouTube videos.
Used with Python 3.8, but should be compatible with 3.6+.

#### Usage
`ui_search_crawl.py` is the primary crawling script, and is named for its use of the YouTube UI search functionality to build a
starting list of URLs for the crawl.

1. Run `generate_keyword_urls`.  
This uses a text file of keywords from `/data` as input for the YouTube search bar.
The resulting search page will contain links to 20 related videos.
These links are collected for each keyword and written to a new
 text file under `/data` with each URL separated by a newline.

`generate_keyword_urls` does not need to be run every time the crawl is performed, only prior to the first run
to generate a list of URLs as a starting point.

2. Once the starting URL list is generated, run `crawl_by_ui_search`.
This first reads the file of URLs created by `generate_keyword_urls` into a list.
Using a ThreadPoolExecutor the script will visit each video URL and collect the view count.
If the view count is greater than the specified threshold (currently 10000), all suggested videos on the page 
will be added to the queue.  Finally, the video is added to the list of crawled URLs.

The collected videos will be saved in `/data/videos.json` with the following data structure:
```json
{
"videoID1": 
  {
    "views": 12345
  }
,
"videoID2": 
  {
    "views": 12345
  }
}
```
Note that the initial crawl will only collect views.  Some limited metadata is also available through pure HTML without 
rendering Javascript, but this is currently gathered in `collect_metadata.py`.
Javascript metadata collection is significantly slower than crawling HTML so it is recommended to perform this on a 
more limited set of videos than those found by the crawl.

3. If a smaller subset of videos is desired for metadata collection, select a random sampling from videos.json
 using `select_videos.py`. Using `/data/videos.json`, this will randomly select a configurable (currently 100) number 
 of videos and save them as `/data/videos_sampling.json`.

4. `collect_metadata.py` expects a json containing key value pairs of video IDs and a dictionary of their properties, 
as generated by `ui_search_crawl.py`.  For each video ID in the json file, `collect_metadata.py` will visit the URL for
the video and collect additional metadata currently including the following:
* view count
* date published
* date uploaded
* channel ID
* title
* player type
* category
* likes
* dislikes

`collect_metadata.py` expects a selenium webdriver executable in the same directory.
This has been tested with the chrome webdriver as `chromedriver.exe`.
To avoid ads the script currently relies on Ublock origin which is imported from the local Chrome installation.
By default the extension will be located in: 
`C:\Users\username\AppData\Local\Google\Chrome\User Data\Default\Extensions\identifier\version`
This path must be configured as the environment variable **UBLOCK_ORIGIN_PATH**.

The method for ensuring all page elements are loaded before scraping metadata stands to be improved.
The script currently waits after loading the page before attempting collection as other methods tested which relied on
the presence of specific elements were inconsistent and resulted in missed metadata.  An improved system would make the
script much faster.

#### Utils
The utils package contains a series of small helper libraries.
* `api_tools.py`: Functions for interacting with the YouTube API with a registered developer account.
    * Not used by any current scripts as the default API quota is limited
* `io.py`: Functions for writing Python data structures to files and reading files to Python data structures.
* `html_parsing.py`: Functions for scraping metadata from YouTube pages using BeautifulSoup.



