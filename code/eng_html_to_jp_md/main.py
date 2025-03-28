from markdownify import MarkdownConverter
#from googletrans import Translator
import urllib.request
from bs4 import BeautifulSoup
from bs4 import element
#translator = Translator()
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
    if len(text) > 0:
        translated = translator.translate(text, dest="ja")
        return translated.text
    

def change(bsObj, target_tags):
    for tag in target_tags:
        for child in bsObj.find_all(tag):
            try:
                child.string = my_translate(child.text)
            except:
                print(traceback.format_exc())
                child.string = (child.text + "[error]")
    return bsObj


def change(bsObj, target_tags):
    for tag in target_tags:
        for child in bsObj.find_all(tag):
            try:
                child.string = my_translate(child.text)
            except:
                print(traceback.format_exc())
                child.string = (child.text + "[error]")
    return bsObj


def create_japanese_sentence(url):
    with urllib.request.urlopen(url) as u:
        html = u.read()
        soup = BeautifulSoup(html,features="html.parser")
        title = ""
        try:
            title = soup.find('title').text
        except:
            title = ""
        body_soup = soup
        change(body_soup, ["li", "p", "h5", "h4" ,"h3","h2", "h1", "a"])
        return title,md(str(body_soup))


def run_scrapy(url):
    with urllib.request.urlopen(url) as u:
        html = u.read()
        soup = BeautifulSoup(html,features="html.parser")
        body_test = soup.find('body').text
        return md(body_test)