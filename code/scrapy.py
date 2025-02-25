from markdownify import MarkdownConverter
#from googletrans import Translator
import urllib.request
from bs4 import BeautifulSoup
from bs4 import element
import traceback
import datetime
t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
from urllib.parse import urlparse
from eng_html_to_jp_md.main import create_japanese_sentence
from eng_html_to_jp_md.main import run_scrapy

def get_done_url_list():
    done_url_list = []
    with open(f"/code/scrapy_done_list", mode='r') as f:
        done_url_list = f.read().split("\n")
    return done_url_list


def get_links(url):
    a_tags = []
    with urllib.request.urlopen(url) as u:
        html = u.read()
        soup = BeautifulSoup(html, features="html.parser")
        for a_tag in soup.find_all('a'):
            a_tags.append(a_tag.get('href'))
        return a_tags

def create_link(link_parts,site_url):
    domain = "https://" + (urlparse(site_url).netloc)
    return urllib.parse.urljoin(site_url, link_parts).split('#')[0]
    if link_parts and link_parts.startswith("/"):
        return domain + link_parts
    if link_parts and str(link_parts[0]).isalnum():
        return site_url + link_parts
    return False


def add_done(url):
    with open(f"/code/scrapy_done_list", mode='a') as f:
        f.write(url + "\n")
