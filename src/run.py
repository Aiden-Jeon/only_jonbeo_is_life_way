import requests

url = "https://api.upbit.com/v1/candles/minutes/10"

querystring = {"market":"KRW-XRP","to":"2020-12-02 00:00:00","count":"200"}

response = requests.request("GET", url, params=querystring)

print(response.text)