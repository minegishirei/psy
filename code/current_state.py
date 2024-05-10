from datetime import datetime
import requests as req
import json
import markdown_to_json
import os


def getContent(filePath):
    with open(filePath, "r") as f:
        return f.readlines()

def isPage(content):
    for row in content:
        if "page:https://" in row:
            return True
    return False

def isAttached(content):
    return len(content[2]) == len("6801883189101413281")

def getAllMDFilepath():
    filePaths = []
    for root, dirs, files in os.walk(top='/blog'):
        for file in files:
            filePath = os.path.join(root, file)
            if ".md" in filePath:
                filePaths.append(filePath)
    return filePaths 


if __name__ == "__main__":
    import os
    for filePath in getAllMDFilepath():
        content = getContent(filePath)
        if not isPage(content):
            print(filePath)
