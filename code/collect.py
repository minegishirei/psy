import urllib
from icecream import ic
from chatgpt import get_client, call_groq
from scrapy import get_done_url_list, get_links, create_link, add_done
from eng_html_to_jp_md.main import create_japanese_sentence
from eng_html_to_jp_md.main import run_scrapy
import datetime
import groq
t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
from urllib.parse import urlparse
import os



def get_markdown_template(url, result):
    return f"""

hhhhhhhhhhhhhhhhhhh
    
[:contents]

参考 : {url}

{result}

    """


def run_chatgpt(request):
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    SYSTEM_PROMPT = "あなたは便利な日本人アシスタントです。質問には簡潔に日本語で答えてください。"
    response = call_groq(get_client(GROQ_API_KEY), SYSTEM_PROMPT, request)
    text = response.choices[0].message.content
    return text


def curry_url_filtering(done_url_list,domain, site_own_filtering):
    def url_filtering(url):
        result =  (url not in done_url_list) and (domain in url)
        return result and site_own_filtering(url)
    return url_filtering


def default_filter(url):
    return True


def main(sites, get_prompt_template, batch_size):
    for site_info in sites:
        site_url = site_info["link"]
        site_own_filtering = site_info.get("filter", default_filter)
        done_url_list = get_done_url_list()
        domain = "https://" + (urlparse(site_url).netloc)
        ic(domain)
        url_filtering =  curry_url_filtering(done_url_list, domain, site_own_filtering)
        cleaned_links = map(lambda link :  create_link(link,site_url) , get_links(site_url) )
        filterd_links = list(filter( url_filtering , cleaned_links))
        for url in filterd_links[:batch_size]:
            ic(url)
            if url in done_url_list:
                continue
            sentence = ""
            try:
                sentence = run_scrapy(url)
            except (AttributeError, UnicodeEncodeError, urllib.error.HTTPError):
                pass
            result = ""
            try:
                result = run_chatgpt(get_prompt_template(sentence)[:6000] )
            except groq.RateLimitError:
                pass
            with open(f"/data/{datetime.datetime.now(JST).strftime('%Y%m%d%H%M%S')}.md", "w+") as f:
                f.write(get_markdown_template(url, result))
            add_done(url)
            done_url_list.append(url)

