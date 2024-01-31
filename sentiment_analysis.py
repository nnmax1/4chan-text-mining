import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
import nltk 
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 


# list of stopwords
# nltk.download('stopwords') 
stop_words = stopwords.words('english')
stemmer = SnowballStemmer('english')


from data_api import DataAPI

# tokenizes text
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


def getSentimentDataset(db_name):
    dataapi=DataAPI(db_name)
    data=dataapi.retrieveData()
    text_data=[]
    for i in range(len(data)):
        for text in data[i]['data']:
            tokens=preprocess(text[2])
            text_data.append({'text':text[2] ,'tokens': tokens,'counts': len(tokens)   })
    analyzer = SentimentIntensityAnalyzer()
    sent_list = []
    df =pd.DataFrame(text_data)
    for i in df["text"]:
        ps = analyzer.polarity_scores(i)
        sent_list.append(ps)
    sentiment_df = pd.DataFrame(sent_list)
    dataset = pd.concat([df.reset_index(drop=True), sentiment_df], axis=1)
    dataset["frequency"] = dataset["text"].apply(lambda x: len(str(x).split(" "))) 
    dataset["sentiment"] = np.where(dataset["compound"] >= 0, "positive", "negative")
    return dataset


# bar chat comparing pos to neg sentiment of posts in dataset
def sentimenetBarChart(db_name):
    dataset=getSentimentDataset(db_name)
    result = dataset["sentiment"].value_counts()
    result.plot(kind="bar", rot=0, color=["plum","cyan"]);
    # no. of posts w/ pos sent. and no. posts w/ neg sent.
    posts_sentiment_counts=dataset.groupby("sentiment")["text"].count()
    print(posts_sentiment_counts)
    plt.ylabel('no. of posts')
    plt.savefig('sentiment_bar.png')

# get top 200 most positive or negative posts
# pos ='neg' or pos='pos'
def mostPositiveNegativePosts(db_name,pos):
    db_name='data.db'
    dataset=getSentimentDataset(db_name)
    most =dataset.groupby(pos)['text'].max()
    elems=[]
    for m in most:
        # if torrent url not in text
        if 'xt=urn:' not in m:
            elems.append(m)
    elems = elems[::-1]
    return elems[0:500]


'''
# pie chat comparing pos to neg sent
import plotly.graph_objects as go
import plotly.express as px
dataset =getSentimentDataset('data.db')
fig = px.pie(dataset, values=dataset["frequency"], names=dataset['sentiment'], 
             color_discrete_sequence=px.colors.sequential.Darkmint,
             title="Positive or Negative ?"
)
fig.show()
'''
