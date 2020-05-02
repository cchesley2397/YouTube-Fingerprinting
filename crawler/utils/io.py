import json


def text_file_to_list(filename):
    """
    Given the path of a text file, return a list of the content split by newlines.
    :param filename: Path of text file
    :return: List of strings containing each line of the file with the newline removed
    """
    with open(filename, 'r') as text_file:
        return text_file.read().splitlines()


def dict_to_json(filename, dictionary):
    """
    Write a dictionary to a JSON file
    :param filename:
    :param dictionary:
    :return:
    """
    with open(filename, 'w') as json_file:
        json.dump(dictionary, json_file)


def json_to_dict(filename):
    """
    Return contents of a JSON file as a dictionary
    :param filename:
    :return:
    """
    with open(filename, 'r') as json_file:
        return json.load(json_file)


def list_to_text_file(filename, string_list):
    """
    Write a list to a text file with a newline following each element
    :param filename:
    :param string_list:
    :return:
    """
    with open(filename, "w") as text_file:
        for line in string_list:
            text_file.write(f"{line}\n")
