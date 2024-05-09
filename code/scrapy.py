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
url = "https://www.psychologytoday.com/intl/blog/social-instincts/202405/2-popular-psychology-myths-debunked"
url = "https://www.psychologistworld.com/memory/false-memories-questioning-eyewitness-testimony"


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
        markdown = md(soup.find("body"))
        for row in markdown.split("\n"):
            if len(row) < 100:
                continue
            sentence += ( my_translate(row) + "\n")
    return title,description,sentence


title,description,sentence = create_japanese_sentence(url)


with open(f"/data/{title}", "w+") as f:
    f.write(description + "\n" + sentence + "\n" + "from:" + url)




