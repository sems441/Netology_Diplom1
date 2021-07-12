import requests
import pprint
import PySimpleGUI as sg
import time

id_vk = int(input("Введите id пользователя: "))
picture = {}
uri_vk = "https://api.vk.com/method/photos.get?owner_id="
version = "&v=5.131"
access_token = "&album_id=wall&extended=1&access_token=d33e674fd33e674fd33e674f2cd346ec9edd33ed33e674fb3d7f3cc177e8fa046ae1411"
url = uri_vk + str(id_vk) + access_token + version
print(url)
x = requests.get(url = url)
# print(x)
# print(x.json())
# pprint.pprint(x.json())

for object_ in x.json()['response']['items']:
    max_size = 0
    url_picture = []
    picture[object_['id']] = []
    picture[object_['id']].append(object_['likes']['count'])
    picture[object_['id']].append(object_['date'])
    for size in object_['sizes']:
        if size['height'] > max_size:
            max_size = size['height']
            url_picture = size['url']
        # print(size)
    # print(max_size)
    picture[object_['id']].append(url_picture)
print(picture)
print()

#

# 663114110

token = input("Введите свой токен от яндекс.Диска: ")
ya_headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {token}'}
ya_upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload?"

for i, ids in enumerate(picture):
    sg.one_line_progress_meter('Загрузка в Яндекс Диск', i + 1, len(picture), '-key-')
    time.sleep(1)
    correct_url = "&url="
    ya_params = f"path=%2Fnetology%2F{ids}.jpg"
    for x in picture[ids][2]:
        if x == "/":
            correct_url += "%2F"
        elif x == "=":
            correct_url += "%3D"
        elif x == ":":
            correct_url += "%3A"
        elif x == "?":
            correct_url += "%3F"
        elif x == "&":
            correct_url += "%26"
        else:
            correct_url += x
    # print(correct_url)
    url = ya_upload_url + ya_params + correct_url
    # print(url)
    response = requests.post(url = url, headers = ya_headers)
    # print(response)
    # print(response.json())

files_url = 'https://cloud-api.yandex.net/v1/disk/resources?path=%2Fnetology&fields=_embedded'
response = requests.get(files_url, headers=ya_headers)
length = response.json()['_embedded']['total']
for index in range(length):
    polka = {}
    name = response.json()['_embedded']['items'][index]['name']
    polka["file_name"] = name
    size = response.json()['_embedded']['items'][index]['size']
    polka["size"] = size
    print(polka)
    with open ("upload.txt", "a", encoding="utf-8") as file:
        file.write(str(f"{polka}\n"))
pprint.pprint(response.json())


#AQAAAAAGZXvUAADLW76jFY9KWERtvUy7JjAglwA