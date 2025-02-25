import os
import re
from pathlib import Path
from icecream import ic
import itertools
import json
import itertools
from urllib.parse import urlparse
import urllib
from chatgpt import get_client, call_groq
from scrapy import get_done_url_list, get_links, create_link, add_done
from eng_html_to_jp_md.main import create_japanese_sentence
from eng_html_to_jp_md.main import run_scrapy
import datetime
import groq
t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')

def extract_effect_sections_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # ## 効果: で始まる章を抽出
    effect_sections = re.findall(r'^## 効果:(.*?)\n(.*?)(?=^## |\Z)', content, re.MULTILINE | re.DOTALL)
    effect_sections = effect_sections if len(effect_sections) > 0  else []

    dictionarys = []
    for effect_section in effect_sections:
        extracted_data = []
        for section in effect_section:
            # - action:, - example:, - effect: を抽出
            matches = re.findall(r'(- action:.*?- example:.*?- effect:.*?)\n', section, re.DOTALL)
            extracted_data.extend(matches)
        if len(extracted_data) <= 0:
            return []
        for extra in  extracted_data:
            dictionary = {}
            for row in extra.split("\n"):
                row = row.replace("- ", "")
                dictionary = {
                    **dictionary,
                    row.split(":")[0] : row.split(":")[1]
                }
            dictionarys.append(dictionary)
    return dictionarys

def search_markdown_files(directory):
    results = []
    for file_path in Path(directory).rglob("*.md"):
        extracted_sections = extract_effect_sections_from_file(file_path)
        extracted_sections = list(map(lambda row: {
            **row,
            "file_path" : str(file_path)
        }, extracted_sections))
        if extracted_sections:
            results.extend(extracted_sections)
    return results


class Build():
    def __init__(self):
        pass

    def nodeDataArray(self, sections):
        nodeDataArray = []
        for i, section in enumerate(sections):
            nodeDataArray.append({
                "key" : i,
                "type" : "Table",
                "name" : section["action"],
                "example" : section["example"],
                "effect" : section["effect"]
            })
        return nodeDataArray
    
    def linkDataArray(self, nodeDataArray):
        linkDataArray = []
        #linkDataArray =  list(itertools.chain.from_iterable((map(lambda row:row["effect"].split(","), nodeDataArray))))
        #ic(linkDataArray)
        for row in nodeDataArray:
            for row2 in nodeDataArray:
                for keyword in row["effect"].split(","):
                    for keyword2 in row2["name"].split(","):
                        if keyword==keyword2:
                            linkDataArray.append({
                                "from" : row["key"],
                                "to":row2["key"]
                            })
        return linkDataArray


def get_method(file_path):
    if "WRITE" in file_path:
        return "write"
    elif "PERSOL" in file_path:
        return "persol"
    elif "READ" in file_path:
        return "read"
    return ""

import random
class IVRtreeBuild():
    def __init__(self):
        self.last_key = 1000000000

    def nodeDataArray(self, sections):
        nodeDataArray = []
        for i, section in enumerate(sections):
            node = {
                "key" : i,
                "type" : "Table",
                "question" : section["action"],
                "actions" : list(map(lambda row : {"text" : row, "figure" : random.choice(["Hammer", "Caution", "BpmnTaskMessage"]) }, section.get("content", "").split(",") + section["example"].split(","))),
                "example" : section["example"],
                "effect" : section["effect"],
                "method" : get_method(section["file_path"]),
                "file_path" : section["file_path"]
            }
            if section["effect"] == "終了":
                node = {
                    **node,
                    "category" : "Terminal",
                    "text" : section["action"]
                }
            nodeDataArray.append(node)
        #nodeDataArray.append({
        #    "key" : self.last_key,
        #    "category" : "Terminal",
        #    "question" : "終了",
        #    "effect" : "終端",
        #    "text" : "終端2"
        #})
        return nodeDataArray
    
    def linkDataArray(self, nodeDataArray):
        linkDataArray = []
        #linkDataArray =  list(itertools.chain.from_iterable((map(lambda row:row["effect"].split(","), nodeDataArray))))
        #ic(linkDataArray)
        for row in nodeDataArray:
            for row2 in nodeDataArray:
                for keyword in row["effect"].split(","):
                    for keyword2 in row2["question"].split(","):
                        if keyword==keyword2:
                            linkDataArray.append({
                                "from" : row["key"],
                                "to":row2["key"]
                            })
        return linkDataArray


def run_chatgpt(request):
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
    SYSTEM_PROMPT = "あなたは便利な日本人アシスタントです。質問には簡潔に日本語で答えてください。"
    response = call_groq(get_client(GROQ_API_KEY), SYSTEM_PROMPT, request)
    text = response.choices[0].message.content
    return text

def get_markdown_template(url, result):
    return f"""

hhhhhhhhhhhhhhhhhhh
    
[:contents]

参考 : {url}

{result}

    """


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



if __name__ == "__main__":
    sites = [
        #"https://ja.wikipedia.org/wiki/%E3%82%AB%E3%83%AA%E3%82%AE%E3%83%A5%E3%83%A9%E5%8A%B9%E6%9E%9C",#カリギュラ効果:良い
        # "https://www.psychologistworld.com/dreams/", #夢
        # "https://www.psychologistworld.com/",
        # "https://www.simplypsychology.org/regression-defence-mechanism.html", #退行:forbidden
        # "https://newstyle.link/category58/", #口癖:根拠がない
        # "https://japan-brain-science.com/archives/3618", #低品質
        #"https://japan-brain-science.com/",
        "https://psychologist.x0.com/terms/144.html#btm", #エリクソンのライフサイクル理論
        "https://psychcentral.com/",
        "https://ja.wikipedia.org/wiki/%E5%A4%A7%E8%84%B3", #低変質
        #"https://www.apa.org/",
        #"https://www.sciencenews.org/topic/psychology",
        #"https://www.psychologytoday.com",
        #"https://www.verywellmind.com/theories-of-love-2795341",
        #"https://www.frontiersin.org/research-topics/48534/the-psychology-of-love/magazine",
        #"https://www.nature.com/collections/abjigjgige"
    ]
    print(sites)
    for site_url in sites:
        done_url_list = get_done_url_list()[20:]
        domain = "https://" + (urlparse(site_url).netloc)
        links = get_links(site_url)
        filterd_links = list(map(lambda link : create_link(link,site_url), filter( lambda link : create_link(link,site_url) not in done_url_list ,links)) )
        count = 0
        for url in filterd_links:
            print(url)
            if (count > 100):
                break
            if url in done_url_list:
                continue
            count += 1
            sentence = ""
            try:
                sentence = run_scrapy(url)
            except AttributeError:
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
    target_directory = "/blog"  # ここを調査したいディレクトリに変更
    extracted_results = search_markdown_files(target_directory)
    nodeDataArray = IVRtreeBuild().nodeDataArray(extracted_results)
    linkDataArray = IVRtreeBuild().linkDataArray(nodeDataArray)
    data = {
        "class": "go.GraphLinksModel",
        "nodeCategoryProperty": "type",
        "linkFromPortIdProperty": "frompid",
        "linkToPortIdProperty": "topid",
        "nodeDataArray" : nodeDataArray,
        "linkDataArray" : linkDataArray
    }
    data = {
      "copiesArrays": True,
      "copiesArrayObjects": True,
      "nodeDataArray": nodeDataArray,
      "linkDataArray": linkDataArray
    }
    #ic(data)
    with open("/json/main.json", "w") as f:
        f.write(json.dumps(data, ensure_ascii=False))


