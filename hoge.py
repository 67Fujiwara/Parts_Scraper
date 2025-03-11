import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


employee_id = "社番"
password = "ﾊﾟｽﾜｰﾄﾞ"
login_url = 'ﾛｸﾞｲﾝURL'
protected_url = 'ﾛｸﾞｲﾝ後のURL'

login_info = {
    'id':employee_id,
    'pwd':password, 
}
#requestsでﾛｸﾞｲﾝ
session = requests.Session()
response = session.get(login_url)
print(f'ﾛｸﾞｲﾝ前のhtml:{session}')
res = session.post(login_url, data=login_info)

#htmlのformにあるactionの相対パスを取得
soup = BeautifulSoup(res.text, 'html.parser')
form = soup.find('form')
action_url = form['action']

#URLを解析
parsed_url = urlparse(protected_url)
# ドメイン(ネットﾛｹｰｼｮﾝ)とパスを取得
domain = parsed_url.netloc
path = parsed_url.path  

scraping_url = domain + action_url

res1 = session.get(scraping_url)
print(f'ﾛｸﾞｲﾝ後のhtml:{res1}')