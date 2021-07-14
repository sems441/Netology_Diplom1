import requests
# import pprint
import PySimpleGUI
import time


def vk_download():
    id_vk = int(input("Введите id пользователя: "))
    pictures = {}
    uri_vk = "https://api.vk.com/method/photos.get?owner_id="
    version = "&v=5.131"
    access_token = "&album_id=wall&extended=1&access_token" \
                   "=d33e674fd33e674fd33e674f2cd346ec9edd33ed33e674fb3d7f3cc177e8fa046ae1411"
    url = uri_vk + str(id_vk) + access_token + version
    response = requests.get(url=url)

    for object_ in response.json()['response']['items']:
        max_size = 0
        url_picture = []
        pictures[object_['id']] = []
        pictures[object_['id']].append(object_['likes']['count'])
        pictures[object_['id']].append(object_['date'])
        for size in object_['sizes']:
            if size['height'] > max_size:
                max_size = size['height']
                url_picture = size['url']
        pictures[object_['id']].append(url_picture)
    return pictures


def odnoklassniki_download():
    id_odn = input("Введите id пользователя: ")
    token = input("Введите свой токен от Одноклассников: ")
    uri = "https://api.ok.ru/fb.do?"
    album_id = "aid=463566561801"
    sys_info = f"&application_key=CFELGPJGDIHBABABA&fid={id_odn}&format=json&method=photos.getPhotos"
    sig_api = "&sig=364ee91f0e71219a4cf2cb7f4ec9bbed"
    token = f"&access_token={token}"

    pictures = {}
    url = uri + album_id + sys_info + sig_api + token
    request = requests.get(url)
    for picture in request.json()["photos"]:
        pictures[picture["id"]] = []
        pictures[picture["id"]].append(picture["pic640x480"])
    return pictures


def ya_disk_upload(data, index):
    token = input("Введите свой токен от яндекс.Диска: ")
    ya_headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {token}'}
    ya_upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload?"

    for i, ids in enumerate(data):
        PySimpleGUI.one_line_progress_meter('Загрузка в Яндекс Диск', i + 1, len(data), '-key-')
        time.sleep(1)
        correct_url = "&url="
        ya_params = f"path=%2Fnetology%2F{ids}.jpg"
        for symbol in data[ids][index]:
            if symbol == "/":
                correct_url += "%2F"
            elif symbol == "=":
                correct_url += "%3D"
            elif symbol == ":":
                correct_url += "%3A"
            elif symbol == "?":
                correct_url += "%3F"
            elif symbol == "&":
                correct_url += "%26"
            else:
                correct_url += symbol
        url = ya_upload_url + ya_params + correct_url
        requests.post(url=url, headers=ya_headers)

    files_url = 'https://cloud-api.yandex.net/v1/disk/resources?path=%2Fnetology&fields=_embedded'
    response = requests.get(files_url, headers=ya_headers)
    length = response.json()['_embedded']['total']
    for index in range(length):
        log_file = {}
        name = response.json()['_embedded']['items'][index]['name']
        log_file["file_name"] = name
        size = response.json()['_embedded']['items'][index]['size']
        log_file["size"] = size
        with open("upload.txt", "a", encoding="utf-8") as file:
            file.write(str(f"{log_file}\n"))


answer = 0
pictures = []
element_id = 0
while answer != 4:
    print("1 - скачать с VK\n2 - скачать с однокласcников\n3 - загрузить на яндекс диск\n4 - выход")
    answer = int(input())
    if answer == 1:
        pictures = vk_download()
        element_id = 2
    elif answer == 2:
        pictures = odnoklassniki_download()
        element_id = 0
    elif answer == 3:
        if pictures:
            ya_disk_upload(pictures, element_id)
        else:
            print("Не указали откуда скачивать фото\n")
    else:
        break
