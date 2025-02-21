import os
import groq


def get_client(api_key):
    client = groq.Groq(api_key=api_key)
    return client

def call_groq(client, system_prompt, user_prompt):
    # Set the user prompt
    # Initialize the chat history
    chat_history = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]
    response = client.chat.completions.create(model="llama3-70b-8192",
                                                messages=chat_history,
                                                temperature=0.8)
    return response

def fetch_file(file_path):
    with open(file_path) as f:
        return f.read()


def get_contents():
    contents = []
    for root, dirs, files in os.walk('/data/psy/blog'):
        md_files = filter(lambda file: ".md" in file, files)
        for md_file in md_files:
            md_file_path = os.path.join(root, md_file)
            content = fetch_file(md_file_path)
            contents.append(
                (md_file_path, content)
            )
    return contents

def contains_two_or_more_keywords(content, keywords, limit):
    count = 0
    hit_words = []
    for keyword in keywords:
        if keyword in content:
            count += 1
            hit_words.append(keyword)
            if count >= limit:
                return True, hit_words
    return False, hit_words



import re
def get_data():
    data = []
    for md_file_path, content in get_contents():
        md_chapters = re.split(r'#### |### |## |# ', content)
        for md_chapter in md_chapters:
            if len(md_chapter) > 50:
                data.append({
                    "md_file_path" : md_file_path,
                    #"hit_words" : hit_words,
                    "md_chapter" : md_chapter
                })
    return data





#tags = text.split("、")
#print(tags)

#candidates = []
#import re
#for md_file_path, content in get_contents():
#    md_chapters = re.split(r'#### |### |## |# ', content)
#    for md_chapter in md_chapters:
#        flag, hit_words = contains_two_or_more_keywords(md_chapter, tags, 2)
#        if flag:
#            candidates.append({
#                "md_file_path" : md_file_path,
#                "hit_words" : hit_words,
#                "md_chapter" : md_chapter
#            })
