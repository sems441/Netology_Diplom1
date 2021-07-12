import requests
import pprint


id_odn = input("Введите id пользователя: ")
token = input("Введите свой токен от Одноклассников: ")
uri = "https://api.ok.ru/fb.do?"
album_id = "aid=463566561801"
sys_info = f"&application_key=CFELGPJGDIHBABABA&fid={id_odn}&format=json&method=photos.getPhotos"
sig_api = "&sig=364ee91f0e71219a4cf2cb7f4ec9bbed"
token = f"&access_token={token}"

pictures ={}
url = uri + album_id + sys_info + sig_api + token
request = requests.get(url)
for picture in request.json()["photos"]:
    pictures[picture["id"]] = []
    pictures[picture["id"]].append(picture["pic640x480"])

# print(request)
# pprint.pprint(request.json())
print(pictures)





#tkn1wy8aCXtmFMXeXejodnJuAiF9KJmuKb60WuXQ2eQyYAVcXGo1sIZLVy3NWcUEqXUhu1
#554012903945





