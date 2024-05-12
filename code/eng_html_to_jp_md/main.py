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

def change(bsObj, target_tags):
    for tag in target_tags:
        for child in bsObj.find_all(tag):
            try:
                child.string = my_translate(child.text)
            except:
                child.string = (child.text + "!!!!!!!")
    return bsObj

def create_japanese_sentence(url):
    with urllib.request.urlopen(url) as u:
        html = u.read()
        soup = BeautifulSoup(html,features="html.parser")
        title = my_translate(soup.find('title').text)
        body_soup = soup.find("body")
        change(body_soup, ["li", "p", "h5", "h4" ,"h3","h2", "h1", "a"])
        return title,md(str(body_soup))

