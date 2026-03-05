import requests
import re
from urllib.parse import quote

def test_bing_image(name, location):
    query = f"{name} {location} hotel exterior"
    url = f"https://www.bing.com/images/search?q={quote(query)}&form=HDRSC2&first=1"
    print("URL:", url)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    resp = requests.get(url, headers=headers, timeout=5)
    print("Status:", resp.status_code)
    # Bing stores image URLs in m="{... murl: 'https...' ...}"
    matches = re.findall(r'murl&quot;:&quot;(htt[^\"]+)&quot;', resp.text)
    if not matches:
        matches = re.findall(r'murl":"(http[^"]+)"', resp.text)
    if matches:
        return matches[0]
    return "Not found"

print(test_bing_image("JW Marriott", "Pune"))
