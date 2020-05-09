import json
import random
from crawler.utils.io import *


if __name__ == '__main__':
    # Select a random sampling of 100 video IDs from the provided JSON and write to a new file
    with open('./data/videos.json') as json_file:
        data = json.load(json_file)
        indeces = set()
        selected_videos = {}
        while len(indeces) < 100:
            indeces.add(random.randint(0, len(data['videos']) - 1))

        print(indeces)
        key_list = list(data['videos'].keys())
        for index in indeces:
            key = key_list[index]
            video_data = data['videos'][key]
            selected_videos[key] = video_data
    dict_to_json('./data/videos_sampling.json', selected_videos)
