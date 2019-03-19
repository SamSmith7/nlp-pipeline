import chunker
import dataset
import itertools
import normalizer
import pandas as pd
import re
import stanford
import sys


news_df = []

flags = list(filter(lambda x: re.match('^--', x), sys.argv))
args = list(itertools.filterfalse(lambda x: re.match('^--', x), sys.argv))

if (len(args) == 1):

    print('Fetching Dataset')

    seed_urls = [
        'https://inshorts.com/en/read/technology',
        'https://inshorts.com/en/read/sports',
        'https://inshorts.com/en/read/world'
    ]

    news_df = dataset.build(seed_urls)
    news_df['full_text'] = news_df['news_headline'].map(str) + '. ' + news_df['news_article']
    news_df['clean_text'] = normalizer.normalize_corpus(news_df['full_text'])
    norm_corpus = list(news_df['clean_text'])

    news_df.iloc[1][['full_text', 'clean_text']].to_dict()

    print('Dataset dumped to: news.csv')
    news_df.to_csv('news.csv', index=False, encoding='utf-8')

else:
    print('Reading Dataset from:', args[1])
    news_df = pd.read_csv(args[1])

if '--chunk' in flags:
    print('Running Tag and Chunker')
    news_df['chunked_text'] = chunker.tag_and_chunk(news_df['full_text'])
    print('Dataset dumped to: news_chunked.csv')
    news_df.to_csv('news_chunked.csv', index=False, encoding='utf-8')

if '--stanford' in flags:
    print('Running StanfordParser')
    news_df['stanford_text'] = stanford.parse(news_df['full_text'])
    print('Dataset dumped to: news_stanford.csv')
    news_df.to_csv('news_stanford.csv', index=False, encoding='utf-8')
