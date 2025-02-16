import os
import re
from pathlib import Path
from icecream import ic
import itertools
import json

def extract_effect_sections_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # ## 効果: で始まる章を抽出
    effect_sections = re.findall(r'^## 効果:(.*?)\n(.*?)(?=^## |\Z)', content, re.MULTILINE | re.DOTALL)
    effect_sections = effect_sections[0] if len(effect_sections) > 0  else []

    extracted_data = []
    for section in effect_sections:
        # - action:, - example:, - effect: を抽出
        matches = re.findall(r'(- action:.*?- example:.*?- effect:.*?)\n', section, re.DOTALL)
        extracted_data.extend(matches)
    if len(extracted_data) <= 0:
        return []
    dictionarys = {}
    for row in extracted_data[0].split("\n"):
        row = row.replace("- ", "")
        dictionarys = {
            **dictionarys,
            row.split(":")[0] : row.split(":")[1]
        }
    return dictionarys

def search_markdown_files(directory):
    results = []
    for file_path in Path(directory).rglob("*.md"):
        extracted_sections = extract_effect_sections_from_file(file_path)
        if extracted_sections:
            results.append(extracted_sections)
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

if __name__ == "__main__":
    target_directory = "/blog"  # ここを調査したいディレクトリに変更
    extracted_results = search_markdown_files(target_directory)
    nodeDataArray = Build().nodeDataArray( extracted_results )
    linkDataArray = Build().linkDataArray(nodeDataArray)
    print(json.dumps(nodeDataArray, ensure_ascii=False))
    print(json.dumps(linkDataArray, ensure_ascii=False))
    with open("/json/main.json", "w") as f:
        f.write(json.dumps(nodeDataArray, ensure_ascii=False))


