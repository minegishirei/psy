from markdownify import MarkdownConverter
from googletrans import Translator
import urllib.request
from bs4 import BeautifulSoup
translator = Translator()
import traceback
import datetime
t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
from urllib.parse import urlparse
 
class ImageBlockConverter(MarkdownConverter):
    """
    Create a custom MarkdownConverter that adds two newlines after an image
    """
    def convert_img(self, el, text, convert_as_inline):
        return super().convert_img(el, text, convert_as_inline) + '\n\n'

# Create shorthand method for conversion
def md(html, **options):
    return ImageBlockConverter(**options).convert(html)


def my_translate(text):
    translated = translator.translate(text, dest="ja")
    return translated.text

def create_japanese_sentence(url):
    sentence = ""
    title = ""
    description = ""
    with urllib.request.urlopen(url) as u:
        html = u.read()
        soup = BeautifulSoup(html)
        title = my_translate(soup.find('title').text)
        try:
            description = my_translate(soup.find('meta', attrs={'name': 'description'}).get('content'))
        except:
            pass
        markdown = md(str(soup.find("body")))
        count = 0
        for row in markdown.split("\n"):
            if len(row) < 100:
                continue
            try:
                sentence += ( my_translate(row) + "\n")
            except:
                count += 1
                if count > 10:
                    return title,description,sentence+"\n"+"error: 途中で終わりました。"
                print("error_row : ",row)
                traceback.print_exc()
                import time
                time.sleep(10)
    return title,description,sentence


def get_links(url):
    a_tags = []
    with urllib.request.urlopen(url) as u:
        html = u.read()
        soup = BeautifulSoup(html)
        for a_tag in soup.find_all('a'):
            a_tags.append(a_tag.get('href'))
        return a_tags





def create_link(link_parts, domain):
    if link_parts and link_parts.startswith("/") and  (not link_parts.endswith("/")) and len(link_parts) > 15:
        return domain + link_parts
    return False


def bloganize(sentence):
    new_sentence = ""
    for p in sentence.split("/n"):
        for jp_p in p.split("。"):
            new_sentence += jp_p + "/n"
        new_sentence += "/n/n"
    return new_sentence


sites = [
    #{
    #    "url" : "https://www.psychologytools.com/professional/techniques/behavioral-experiments/",
    #    "create_link" : create_link3
    #}
    #{
    #    "url" : "https://www.scientificamerican.com/mind-and-brain/",
    #    "domain" : "https://www.scientificamerican.com",
    #    "create_link" : create_link4
    #},
    #{
    #    "url" : "https://www.apa.org/education-career/guide/science",
    #J    "domain" : "https://www.apa.org",
    #J    "create_link" : create_link4
    #},
    {
        "url" : "https://www.sciencenews.org/topic/psychology",
    },
    #{
    #""    "url" : "https://journals.sagepub.com/home/pss",
    #""    "domain" : "https://journals.sagepub.com/home/pss",
    #J    "create_link" : create_link4
    #},

    {
        "url" : "https://www.psychologistworld.com/",
    },
    {
        "url" : "https://www.psychologytoday.com",
    }
]

done_url_list = []
with open(f"scrapy_done_list", mode='r') as f:
    done_url_list = f.read().split("\n")


for row in sites:
    links = get_links(row["url"])
    # 解析対象URL 
    # URLをパースする
    parsed_url = urlparse(row["url"])
    domain = "https://" + parsed_url.netloc
    print("【log】 domain : ", domain)
    filterd_links = list(filter( lambda link : create_link(link,domain) ,links) )
    print("【log】 filterd_links : ", filterd_links)
    filterd_links = list(map(lambda link : create_link(link,domain), filterd_links) )

    count = 0
    for url in filterd_links:
        if url in done_url_list:
            pass
        else:
            count += 1
            if count > 2:
                break
            print("【log】search : ",url)
            try:
                title,description,sentence = create_japanese_sentence(url)
                now = datetime.datetime.now(JST)
                with open(f"/data/{now.strftime('%Y%m%d%H%M%S')}{title}", "w+") as f:
                    f.write(description + "\n" + bloganize(sentence) + "\n" + "from:" + url)
                with open(f"scrapy_done_list", mode='a') as f:
                    f.write(url + "\n")
                    done_url_list.append(url)
            except:
                print("error_url : ",url)
                traceback.print_exc()


