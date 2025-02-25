import urllib
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

def get_prompt_template(sentence):
    return f"""
後述する記事から得られる実用的な心理学の定理を、次の形式で、**日本語で** 出力してください(複数可)

## 効果:<タイトル>
- action:<タイトル>
- content:<なぜそれが起きるのか>
- effect:<予想できる事象>
- example:<具体例>

以下は具体例です。

## 効果:一貫性の法則
- action:一貫性の法則
- content:一貫性を保つことは社会生活において他者から高い評価を受ける
- example:好きな歌手のCDだからという理由だけで買ってしまう
- effect:同じ行動を取り続ける

以下要約するターゲットです。

{sentence}

    """

def get_markdown_template(url, result):
    return f"""

hhhhhhhhhhhhhhhhhhh
    
[:contents]

参考 : {url}

{result}

    """

def get_method(file_path):
    if "WRITE" in file_path:
        return "write"
    elif "PERSOL" in file_path:
        return "persol"
    elif "READ" in file_path:
        return "read"
    return ""


def run_chatgpt(request):
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    SYSTEM_PROMPT = "あなたは便利な日本人アシスタントです。質問には簡潔に日本語で答えてください。"
    response = call_groq(get_client(GROQ_API_KEY), SYSTEM_PROMPT, request)
    text = response.choices[0].message.content
    return text



def main(sites):
    for site_url in sites:
        done_url_list = get_done_url_list()[20:]
        domain = "https://" + (urlparse(site_url).netloc)
        links = get_links(site_url)
        filterd_links = list(map(lambda link : create_link(link,site_url), filter( lambda link : create_link(link,site_url) not in done_url_list ,links)) )
        count = 0
        for url in filterd_links:
            print(url)
            if (count > 5):
                break
            if url in done_url_list:
                continue
            count += 1
            sentence = ""
            try:
                sentence = run_scrapy(url)
            except (AttributeError, UnicodeEncodeError):
                pass
            except urllib.error.HTTPError:
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

