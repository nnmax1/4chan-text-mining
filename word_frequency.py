from collections import Counter
from torchtext.data.utils import get_tokenizer
from wordcloud import WordCloud
import nltk 
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import matplotlib.pyplot as plt
import pandas as pd
import re
import pandas as pd
import seaborn as sns 

from data_api import DataAPI

# basic  text frequency analysis on the dataset

#nltk.download('stopwords')
stop_words = stopwords.words('english')
stemmer = SnowballStemmer('english')



def getFromFile(file):
    arr = []
    file1 = open(file, 'r')
    Lines = file1.readlines()
    # Strips the newline character
    for line in Lines:
        arr.append(str(line.strip()))
    file1.close()
    return arr

def preprocess(text, stem=False):
    text_cleaning_re = "@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+"

    text = re.sub(text_cleaning_re, ' ', str(text).lower()).strip()
    tokens = []
    for token in text.split():
        if token not in stop_words:
            if stem:
                tokens.append(stemmer.stem(token))
            else:
                tokens.append(token)
    return tokens

def wordFrequency(db_name):
    dataapi=DataAPI(db_name)
    data=dataapi.retrieveData()
    counter = Counter()
    
    wordfilter=set(getFromFile('wordfilter.txt'))

    tokenizer = get_tokenizer('basic_english')
    
    for i in range(len(data)):
        for text in data[i]['data']:
            counter.update(tokenizer(text[2]))
           

    top_words=sorted(counter.items())

    filtered_words=[]
    for i in range(len(top_words)): 
        w=top_words[i][0]
        if len(w) > 3:
            if w not in wordfilter:  
                freq=top_words[i][1]
                if freq > 5:
                    if '’'not in w: 
                        filtered_words.append({'word':w,'freq':freq})
    return sorted(filtered_words, key=lambda d: d['freq'],reverse=True) 

def tokenizeData(db_name):
    dataapi=DataAPI(db_name)
    data=dataapi.retrieveData()
    text_data=[]
    for i in range(len(data)):
        for text in data[i]['data']:
            #print(preprocess(text[2]))
            text_data.append({'text':text[2] ,'tokens':preprocess(text[2])})
    df = pd.DataFrame(text_data)

    wordfilter=set(getFromFile('wordfilter.txt'))
    tokens=[]
    for tokenlist in df.tokens:
        for token in tokenlist: 
            if token not in wordfilter:
                tokens.append(token)
    return tokens

def generateWordCloud(db_name): 
    tokens =tokenizeData(db_name)
    text_tokens = " ".join(i for i in tokens)
    wordcloud = WordCloud(
        background_color="#6B5B95",
        colormap="Set2",
        collocations=False).generate(text_tokens)   
    plt.figure(figsize=[11,11])
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.style.use('dark_background')
    plt.savefig('wordcloud.png')

 
def wordFrequencyBarChart(db_name):
    db_name='data.db'
    data_freq=wordFrequency(db_name)
    words=[]
    counts=[]
    for d in data_freq:
        words.append(d['word'])
        counts.append(d['freq'])
    df= pd.DataFrame({'word': words, 'count': counts } )
    sns.set_style("whitegrid")
    sns.despine(left=True, bottom=True)
    sns.set_context("poster", font_scale = .5, rc={"grid.linewidth": 0.6})
    #sns.set(rc = {'figure.figsize':(11,8)})
    sns.barplot(data=df.head(10), x="word", y="count").set(title="Most Common Words:");
    plt.savefig('word_freq_bar.png')

def wordFreqPieChart(db_name):
    db_name='data.db'
    data_freq=wordFrequency(db_name)
    words=[]
    counts=[]
    for d in data_freq:
        words.append(d['word'])
        counts.append(d['freq'])
    plt.pie(counts[0:10], labels = words[0:10], autopct='%1.2f%%')
    plt.title("Most Common Words")
    plt.savefig('word_freq_pie.png')

 
 