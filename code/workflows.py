from datetime import datetime
import requests as req
import json
import markdown_to_json

HATENA_ID = "minegishirei"
BLOG_DOMAIN = "psy.hatenadiary.com"
API_KEY = "u6v0f3440e"

def hatena_create_entry(title, contents, categorys=[], draft=False):
    BASE_URL = f"https://blog.hatena.ne.jp/minegishirei/{BLOG_DOMAIN}/atom/entry"
    updated = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    category = lambda x: "\n".join([f"<category term='{e}' />" for e in x])
    categorys = category(categorys) if category else ""

    xml = f"""<?xml version="1.0" encoding="utf-8"?>
    <entry xmlns="http://www.w3.org/2005/Atom"
          xmlns:app="http://www.w3.org/2007/app">
      <title>{title}</title>
      <author><name>name</name></author>
      {categorys}
      <content type="text/x-markdown">
        {contents}
      </content>
    </entry>""".encode(
        "UTF-8"
    )
    r = req.post(BASE_URL, auth=(HATENA_ID, API_KEY), data=xml)
    return r.text


def hatena_update_entry(title, contents, entry_id, categorys=[], updated="", draft=False):
    BASE_URL = f"https://blog.hatena.ne.jp/minegishirei/{BLOG_DOMAIN}/atom/entry/{entry_id}"
    updated = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    category = lambda x: "\n".join([f"<category term='{e}' />" for e in x])
    categorys = category(categorys) if category else ""

    xml = f"""<?xml version="1.0" encoding="utf-8"?>
    <entry xmlns="http://www.w3.org/2005/Atom"
          xmlns:app="http://www.w3.org/2007/app">
      <title>{title}</title>
      <author><name>name</name></author>
      {categorys}
      <updated>{updated}</updated>
      <content type="text/x-markdown">
        {contents}
      </content>
    </entry>""".encode(
        "UTF-8"
    )
    r = req.put(BASE_URL, auth=(HATENA_ID, API_KEY), data=xml)
    return r.text


def escape_xml(html):
	escape_dict = [
        {
        	"key" : "&",
			"value" : "&amp;"
		},
		{
			"key" : '"',
			"value" : "&quot;"
		},
		{
			"key" : "'",
			"value" : "&apos;"
		},
		{
			"key" : "<",
			"value" : "&lt;"
		},
		{
			"key" : ">",
			"value" : "&gt;"
		}
	]
	for row in escape_dict:
		html = html.replace(row["key"], row["value"])
	return html


if __name__ == "__main__":
    import sys
    _, arg = sys.argv
    lang_name = arg.replace("/blog/","").replace(".md","")
    with open(arg, "r") as f:
        title, categorys, entry_id, *content = f.readlines()
    categorys = categorys.split(",")
    content = "\n".join(content)
    print(entry_id)
    print(len(entry_id))
    print(len(entry_id) > 0)
    if len(entry_id) > 0:
        r = hatena_update_entry(title , escape_xml(content), entry_id, categorys,True, False)
        print(r)
        if "400 XML Parse Failed" in r:
            print(escape_xml(content))
    else:
        r = hatena_create_entry(title , escape_xml(content), categorys, False)
        print(r)
        if "400 XML Parse Failed" in r:
            print(escape_xml(content))

