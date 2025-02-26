import os
import re
from pathlib import Path
from icecream import ic
import json
import itertools
from chatgpt import get_client, call_groq
from scrapy import get_done_url_list, get_links, create_link, add_done
from eng_html_to_jp_md.main import create_japanese_sentence
from eng_html_to_jp_md.main import run_scrapy
import datetime
import random
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


def get_method(file_path):
    if "WRITE" in file_path:
        return "write"
    elif "PERSOL" in file_path:
        return "persol"
    elif "READ" in file_path:
        return "read"
    return ""


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




def main():
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
    with open("/json/main.json", "w") as f:
        f.write(json.dumps(data, ensure_ascii=False))
