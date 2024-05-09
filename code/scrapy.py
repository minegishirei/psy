from markdownify import MarkdownConverter
from googletrans import Translator
import urllib.request
from bs4 import BeautifulSoup
translator = Translator()

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

base_url = "https://www.psychologytoday.com/intl"



def create_japanese_sentence(url):
    sentence = ""
    with urllib.request.urlopen(url) as u:
        html = u.read()
        soup = BeautifulSoup(html)
        print(soup)
        markdown = md(html)
        for row in markdown.split("\n"):
            if len(row) < 100:
                continue
            translated = translator.translate(row, dest="ja");
            sentence += (translated.text + "\n")
    return sentence


sentence = create_japanese_sentence(url)

print(sentence)







