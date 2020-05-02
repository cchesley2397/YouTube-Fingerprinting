import os


def get_id_dict(directory):
    """
    Build a dictionary of sequential IDs and counts for each uniquely named file in directory
    :param directory:
    :return:
    """
    ids = {}
    cnt = 0
    for video in os.listdir(f'{directory}/Capture 1'):
        ids[video[:-5]] = {'id': cnt, 'count': 0}
        cnt += 1
    return ids


def number_rename():
    """
    This function assumes capture_dir contains a series of directories.
    Each directory will contain a capture for each video named after the video's YouTube ID.
    :return: 
    """
    capture_dir = '/Captures/'
    id_dict = get_id_dict(capture_dir)
    print(id_dict)
    for capture_folder in os.listdir(capture_dir):
        if capture_folder != 'parsed':
            for capture in os.listdir(f'{capture_dir}/{capture_folder}'):
                capture_name = capture[:-5]
                capture_path = f'{capture_dir}/{capture_folder}/{capture}'
                capture_num = id_dict[capture_name]['id']
                capture_count = id_dict[capture_name]['count']
                id_dict[capture_name]['count'] += 1

                new_capture_path = f'{capture_dir}/parsed/pcap/{capture_num}-{capture_count}.pcap'

                print(f'Old: {capture_path}')
                print(f'New: {new_capture_path}')

                os.rename(capture_path, new_capture_path)


if __name__ == '__main__':
    number_rename()
