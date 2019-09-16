from afinn import Afinn
import pandas as pd


af = Afinn()

def get_category(score):

    if score > 0.25:
        return 'positive'
    elif score < -0.25:
        return 'negative'
    else:
        return 'neutral'

def analyse(docs, categories):

    sentiment_scores = [af.score(article) for article in docs]
    sentiment_category = [get_category(score) for score in sentiment_scores]

    sentiments = pd.DataFrame([categories, sentiment_scores, sentiment_category]).T
    sentiments.columns = ['Text Category', 'Sentiment Score', 'Sentiment Category']
    sentiments['Sentiment Score'] = sentiments['Sentiment Score'].astype('float')
    sentiments.groupby(by=['Text Category']).describe()

    return sentiments
