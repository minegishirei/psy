from markdownify import MarkdownConverter
import urllib

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



response = urllib.request.urlopen(url)
content = response.read()

print( md(content) )







