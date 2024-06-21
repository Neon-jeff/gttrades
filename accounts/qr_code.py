import requests
import base64

query_url='https://chart.googleapis.com/chart?chs=225x225&chld=L|2&cht=qr&chl=ethereum:0x1d6A91643e8eC808a631eA407549E47d1A8A95b2'

key="8e3520cf14e2c8466e5f4bcc9dea126c"
# this code creates a qr code, upload and return the url to the model field
def CreateQRCode(coin,address):

    # file=requests.get(f'https://chart.googleapis.com/chart?chs=225x225&chld=L|2&cht=qr&chl={coin}:{address}').content

    url = "https://api.cryptapi.io/" + coin + "/qrcode/"

    query = {
    "address": address,
    "value": "",
    "size": "512"
    }

    response = requests.get(url, params=query)

    file = response.json()["qr_code"]
    # post image to image host server
    data={
            "key":key,
            "image":file,
        }

    resp= requests.post("https://api.imgbb.com/1/upload",data=data)
    # Perform Error Handling here
    return resp.json()['data']['url']
