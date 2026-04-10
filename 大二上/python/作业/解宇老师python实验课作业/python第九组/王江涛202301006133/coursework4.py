import requests
from urllib.robotparser import RobotFileParser 

robots_url = "https://cn.bing.com/robots.txt"
rp = RobotFileParser()
rp.set_url(robots_url)
rp.read()

url_to_check = " https://cn.bing.org"
if rp.can_fetch('*', url_to_check):
    print(f"允许爬取: {url_to_check}")
else:
    print(f"禁止爬取取: {url_to_check}")