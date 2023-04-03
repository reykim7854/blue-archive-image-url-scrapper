from bs4 import BeautifulSoup as bs
from requests.adapters import HTTPAdapter, Retry
import requests
import time
import json
import re

BASE_URL = 'https://bluearchive.wiki/wiki'
DEFAULT_TIMEOUT = 5


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


def soupify(http, endpoint):
    result = http.get(BASE_URL + endpoint).text
    soup = bs(result, "html.parser")
    return soup


def get_character_names(http):
    result = soupify(http, '/Characters')
    result = result.find_all('tr')
    del result[0]

    character_names = []
    count = 0
    for row in result:
        print('getting character names...(' + str(count) +
              '/' + str(len(result)) + ' names)', end='\r')
        names = row.find_all('td')[1].find('a').string
        character_names.append(names)
        count += 1

    print('Getting character names...(' + str(count) +
          '/' + str(len(result)) + ' names)')
    time.sleep(5)
    return character_names


def get_character_image(http, name):
    try:
        result_avatar = soupify(
            http, '/File:' + name.replace(' ', '_') + '.png')
        time.sleep(5)
        result_full = soupify(
            http, '/File:' + name.replace(' ', '_') + '_full.png')
        time.sleep(5)
        image_avatar = result_avatar.find(
            'div', class_='fullImageLink').find('a')
        image_full = result_full.find('div', class_='fullImageLink').find('a')
        return {'avatar': 'https:' + image_avatar['href'], 'full_image': 'https:' + image_full['href']}
    except requests.exceptions.Timeout:
        result_avatar = soupify(
            http, '/File:' + name.replace(' ', '_') + '.png')
        time.sleep(5)
        result_full = soupify(
            http, '/File:' + name.replace(' ', '_') + '_full.png')
        time.sleep(5)
        image_avatar = result_avatar.find(
            'div', class_='fullImageLink').find('a')
        image_full = result_full.find('div', class_='fullImageLink').find('a')
        return {'avatar': 'https:' + image_avatar['href'], 'full_image': 'https:' + image_full['href']}
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        raise SystemExit(e)


def main():
    http = requests.Session()
    retries = Retry(total=3, backoff_factor=1,
                    status_forcelist=[429, 500, 502, 503, 504])
    adapter = TimeoutHTTPAdapter(max_retries=retries)
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    character_names = get_character_names(http)
    count = 1
    result = {}

    for name in character_names:
        name_alt = ""
        if re.search(r"(Bunny Girl)", name):
            name_alt = re.sub(r"(Bunny Girl)", "Bunny", name)
        elif re.search(r"(Cheerleader)", name):
            name_alt = re.sub(r"(Cheerleader)", "Cheer Squad", name)
        elif re.search(r"(Kid)", name):
            name_alt = re.sub(r"(Kid)", "Small", name)
        elif re.search(r"(Riding)", name):
            name_alt = re.sub(r"(Riding)", "Cycling", name)
        elif re.search(r"(Arisu)", name):
            name_alt = re.sub(r"(Arisu)", "Aris", name)
        

        print('Getting character (' + name + ') image...(' + str(count) +
              '/' + str(len(character_names)) + ' character)')

        result[name_alt if name_alt else name] = get_character_image(
            http, name)
        count += 1

    json_object = json.dumps(result, indent=2)
    with open("student-images.json", "w") as outfile:
        outfile.write(json_object)


if __name__ == '__main__':
    main()
