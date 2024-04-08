import requests
img = 'https://img.mvideo.ru/Pdb/small_pic/480/30069844b.jpg'
p = requests.get(img)
out = open("img/img.jpg", "wb")
out.write(p.content)
out.close()