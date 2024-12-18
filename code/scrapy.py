from markdownify import MarkdownConverter
from googletrans import Translator
import urllib.request
from bs4 import BeautifulSoup
from bs4 import element
translator = Translator()
import traceback
import datetime
t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
from urllib.parse import urlparse
from eng_html_to_jp_md.main import create_japanese_sentence

def get_done_url_list():
    done_url_list = []
    with open(f"scrapy_done_list", mode='r') as f:
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


sites = [
    #"https://www.sciencenews.org/topic/psychology",
    #"https://www.psychologistworld.com/",
    "https://www.psychologytoday.com",
    #"https://www.verywellmind.com/theories-of-love-2795341",
    #"https://www.frontiersin.org/research-topics/48534/the-psychology-of-love/magazine",
    #"https://www.nature.com/collections/abjigjgige"
]


for site_url in sites:
    done_url_list = get_done_url_list()
    domain = "https://" + (urlparse(site_url).netloc)
    links = get_links(site_url)
    filterd_links = list(map(lambda link : create_link(link,site_url), filter( lambda link : create_link(link,site_url) ,links)) )
    print(filterd_links)
    count = 0
    for url in filterd_links:
        if count < 5 and (url not in done_url_list):
            count += 1
            print("【log】search : ",url)
            try:
                title, sentence = create_japanese_sentence(url)
                with open(f"/data/{site_url}/{datetime.datetime.now(JST).strftime('%Y%m%d%H%M%S')}{title}.md", "w+") as f:
                    f.write("[:contents]")
                    f.write(f"参考 : {url}")
                    f.write(sentence)
                    f.write("\n")
                    f.write(url)
            except:
                import traceback
                traceback.format_exc()
            with open(f"scrapy_done_list", mode='a') as f:
                f.write(url + "\n")
                done_url_list.append(url)


