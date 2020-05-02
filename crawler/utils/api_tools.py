from googleapiclient.discovery import build

yt_service = build('youtube', 'v3')

"""
Set the environment variable GOOGLE_APPLICATION_CREDENTIALS to the path of the 
json file containing the API auth information
"""


def search_videos(keyword):
    """
    Get video IDs for the specified keyword
    :param keyword: String containing search term
    :return:
    """
    request = yt_service.search().list(
        part='id',
        maxResults=50,
        q=keyword
    )
    response = request.execute()
    return response


def list_categories(region_code):
    """
    Get video categories for a specific region
    :param region_code: A string containing an ISO 3166-1 alpha-2 country code
    :return: Dictionary containing the API response listing video categories for the region
    """
    request = yt_service.videoCategories().list(
        part='snippet',
        regionCode=region_code
    )
    response = request.execute()
    return response


def list_popular_videos(region_code):
    """
    List most popular videos by region
    :param region_code: A string containing an ISO 3166-1 alpha-2 country code
    :return: Dictionary with API response
    """
    request = yt_service.videos().list(
        part='contentDetails,id,liveStreamingDetails,localizations,player,' +
             'recordingDetails,snippet,statistics,status,topicDetails',
        chart='mostPopular',
        regionCode=region_code
    )
    response = request.execute()
    return response


def get_video_metadata(video_id):
    """
    Return all available metadata regarding a specific video
    :param video_id: Unique ID for selected video
    :return: Dictionary with API response
    """
    request = yt_service.videos().list(
        part='contentDetails,id,liveStreamingDetails,localizations,player,' +
             'recordingDetails,snippet,statistics,status,topicDetails',
        id=video_id
    )
    response = request.execute()
    return response


if __name__ == '__main__':
    print(search_videos('lofi'))
