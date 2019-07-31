
import requests
# headers = {
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
#
# }
# resp = requests.get(url = "http://xnxx.com",headers = headers)
#
# print(resp.text)

jar =  requests.cookies.RequestsCookieJar()
a = "aaaa=lsjdmfv;adad=cnsksajodn"
for cookie in a.split(";"):
    key, value = cookie.split ("=")
    print(key,value)
    jar.set (key, value)

# print(jar)


