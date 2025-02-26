import sys
from build_tree import main as main_build_tree
from collect import main as collect_data
import re

def get_prompt_template(sentence):
    return f"""
後述する記事を読解して把握できる要素を教えてください。
フォーマットは次の通りで、**日本語で** 出力してください(複数可)

## 効果:<タイトル>
- action:<タイトル>
- content:<なぜそれが起きるのか>
- effect:<予想できる事象>
- example:<具体例>

以下要約するターゲットです。

{sentence}

    """

sites = [
    {
        "link" : "https://ja.wikipedia.org/wiki/%E5%BF%83%E7%90%86%E5%AD%A6",
        "filter" : (lambda url : "?" not in url and re.match("^(.*:/){3,}.*$", url) )
    },
    {
        "link" : "https://www.psychologistworld.com/"
    },
    #{ #低品質
    #    "link" : "https://cbs.riken.jp/jp/"
    #},
    #{
    #    "link" : "https://psychologist.x0.com/index.html"
    #},
    #{ 403
        # psychology today
        #"link" : "https://www.psychologytoday.com"
    #},
    #{
        #"link" : "https://www.aan.com/",
        #"filter" : (lambda url : re.match("^(.*?/){5,}.*$", url) )
    #},
    #{
        #"link" : "https://ja.wikipedia.org/wiki/%E3%82%AB%E3%83%AA%E3%82%AE%E3%83%A5%E3%83%A9%E5%8A%B9%E6%9E%9C",#カリギュラ効果:良い
        #"filter" : (lambda url : re.match("^(.*?/){3,}.*$", url) )
    #}
    
    #OUT:403エラー: "https://openmd.com/directory/neurology"
    #"https://ja.wikipedia.org/wiki/%E3%82%AB%E3%83%AA%E3%82%AE%E3%83%A5%E3%83%A9%E5%8A%B9%E6%9E%9C",#カリギュラ効果:良い
    # "https://www.psychologistworld.com/dreams/", #夢
    # "https://www.psychologistworld.com/",
    # "https://www.simplypsychology.org/regression-defence-mechanism.html", #退行:forbidden
    # "https://newstyle.link/category58/",                                    #口癖:良いが、根拠不十分
    # "https://japan-brain-science.com/archives/3618",                      #OUT:低品質
    # "https://japan-brain-science.com/",
    # "https://psychologist.x0.com/terms/144.html#btm",                       #DONE:エリクソンのライフサイクル理論
    #"https://ja.wikipedia.org/wiki/%E5%A4%A7%E8%84%B3",                    #OUT:低変質
    #"https://www.apa.org/",
    #"https://www.sciencenews.org/topic/psychology",
    #"https://www.psychologytoday.com",
    #"https://www.verywellmind.com/theories-of-love-2795341",
    #"https://www.frontiersin.org/research-topics/48534/the-psychology-of-love/magazine",
    #"https://www.nature.com/collections/abjigjgige"
]

if __name__ == "__main__":
    args = sys.argv
    collect_data(sites, get_prompt_template, 10)
    main_build_tree()