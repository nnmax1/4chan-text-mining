import re
import html

def cleantext(raw_text):
    raw_text=raw_text.replace('&gt;','>')
    reply_tag_pattern = re.compile(r'>>\d+') # remove reply tag
    url_pattern = re.compile(r'https?://\S+|www\.\S+') # remove urls
    CLEANR = re.compile('<.*?>') # remove html tags
    cleantext = re.sub(CLEANR, '', raw_text)
    cleantext = reply_tag_pattern.sub('', cleantext)
    cleantext = html.unescape(cleantext)
    cleantext=cleantext.replace('>','')
    cleantext=url_pattern.sub('',cleantext)
    return cleantext
from data_api import DataAPI

# get data from database, clean text, and write to txt file line by line
def writeAllDataToTXTFile(db_name):
    dataapi=DataAPI(db_name)
    data=dataapi.retrieveData()
    with open('data.txt', 'w', encoding='utf-8') as file:
        for i in range(len(data)):
            for text in data[i]['data']:
                text=cleantext(text[0])
                file.write(text+"\n")

