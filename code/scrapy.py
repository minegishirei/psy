from markdownify import MarkdownConverter
from googletrans import Translator
import urllib.request
from bs4 import BeautifulSoup
translator = Translator()
import traceback
import datetime
t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')

class ImageBlockConverter(MarkdownConverter):
    """
    Create a custom MarkdownConverter that adds two newlines after an image
    """
    def convert_img(self, el, text, convert_as_inline):
        return super().convert_img(el, text, convert_as_inline) + '\n\n'

# Create shorthand method for conversion
def md(html, **options):
    return ImageBlockConverter(**options).convert(html)

url = "https://www.psychologytoday.com/intl/blog/all-is-well/202405/who-decides-what-art-is-good"
url = "https://www.psychologytoday.com/intl/blog/denying-to-the-grave/202405/consequences-of-being-mistreated-by-the-healthcare-system"
url = "https://www.psychologytoday.com/intl/blog/speaking-in-tongues/202405/financial-infidelity-the-cost-of-keeping-secrets"
url = "https://www.psychologytoday.com/intl/blog/social-instincts/202405/2-popular-psychology-myths-debunked"
#url = "https://www.psychologistworld.com/memory/false-memories-questioning-eyewitness-testimony"
#url = "https://www.psychologytoday.com/intl/blog/fixing-families/202405/why-some-of-the-stories-you-tell-yourself-may-be-wrong"

url = "https://www.psychologistworld.com/memory/influential-memory-psychology-studies-experiments"


base_url = "https://www.psychologytoday.com/intl"


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
        description = my_translate(soup.find('meta', attrs={'name': 'description'}).get('content'))
        markdown = md(str(soup.find("body")))
        for row in markdown.split("\n"):
            if len(row) < 100:
                continue
            try:
                sentence += ( my_translate(row) + "\n")
            except:
                print("error_row : ",row)
                traceback.print_exc()
    return title,description,sentence


def get_links(url):
    a_tags = []
    with urllib.request.urlopen(url) as u:
        html = u.read()
        soup = BeautifulSoup(html)
        for a_tag in soup.find_all('a'):
            a_tags.append(a_tag.get('href'))
            print(a_tag)
            print(a_tags)
        return a_tags



def create_link1(link_parts):
    if link_parts.startswith("/") and  (not link_parts.endswith("/")) and len(link_parts) > 15:
        return "https://www.psychologistworld.com" + link_parts
    return False

def create_link2(link_parts):
    if link_parts and link_parts.startswith("/") and  (not link_parts.endswith("/")) and len(link_parts) > 15:
        return "https://www.psychologytoday.com" + link_parts
    return False

def create_link3(link_parts):
    if link_parts and link_parts.startswith("/resource") and  (not link_parts.endswith("/")) and len(link_parts) > 15:
        return "https://www.psychologytools.com" + link_parts
    return False



sites = [
    {
        "url" : "https://www.psychologytools.com/professional/techniques/behavioral-experiments/",
        "create_link" : create_link3
    }
    #,{
    #    "url" : "https://www.psychologistworld.com/",
    #    "create_link" : create_link1
    #}
    #,{
    #    "url" : "https://www.psychologytoday.com",
    #    "create_link" : create_link2
    #}
]

done_url_list = []
with open(f"scrapy_done_list", mode='r') as f:
    done_url_list = f.read().split("\n")


for row in sites:
    print(row)
    links = get_links(row["url"])
    create_link = row["create_link"]
    filterd_links = []
    for link in links:
        if create_link(link):
            filterd_links.append(create_link(link))
    
    count = 0
    for url in filterd_links:
        if url in done_url_list:
            pass
        else:
            count += 1
            if count > 2:
                break
            title,description,sentence = create_japanese_sentence(url)
            now = datetime.datetime.now(JST)
            with open(f"/data/{now.strftime('%Y%m%d%H%M%S')}{title}", "w+") as f:
                f.write(description + "\n" + sentence + "\n" + "from:" + url)
            with open(f"scrapy_done_list", mode='a') as f:
                f.write(url + "\n")



