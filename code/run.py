import sys
from build_tree import main as main_build_tree
from collect import main as collect_data

sites = [
    "https://www.aan.com/",
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
    #main_build_tree()
    collect_data(sites)
