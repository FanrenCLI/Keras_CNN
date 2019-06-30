import requests


for i in range(737,1000):
    name = str(i+1)+".jpg"
    res = requests.get('http://jwgl.ntu.edu.cn/cjcx/checkImage.aspx')
    with open(name, 'wb') as file:
        file.write(res.content)

