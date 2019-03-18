from nltk.corpus import conll2000
from nltk.chunk import ChunkParserI
from nltk.chunk.util import tree2conlltags, conlltags2tree
from nltk.tag import UnigramTagger, BigramTagger
from nltk import pos_tag
import normalizer

data = conll2000.chunked_sents()
train_data = data[:10900]

def conll_tag_chunks(chunk_sents):
    tagged_sents = [tree2conlltags(tree) for tree in chunk_sents]
    return [[(t, c) for (w, t, c) in sent] for sent in tagged_sents]

def combined_tagger(train_data, taggers, backoff=None):
    for tagger in taggers:
        backoff = tagger(train_data, backoff=backoff)
    return backoff

class NGramTagChunker(ChunkParserI):

    def __init__(self, train_sents, tagger_classes=[UnigramTagger, BigramTagger]):

        train_sent_tags = conll_tag_chunks(train_sents)
        self.chunk_tagger = combined_tagger(train_sent_tags, tagger_classes)

    def parse(self, tagged_sents):

        if not tagged_sents:
            return None

        pos_tags = [tag for (word, tag) in tagged_sents]
        chunk_pos_tags = self.chunk_tagger.tag(pos_tags)
        chunk_tags = [chunk_tag for (pos_tag, chunk_tag) in chunk_pos_tags]
        wpc_tags = [(word, pos_tag, chunk_tag) for ((word, pos_tag), chunk_tag) in zip(tagged_sents, chunk_tags)]

        return conlltags2tree(wpc_tags)

def tag_and_chunk(corpus):

    corpus = normalizer.normalize_corpus(corpus, text_lower_case=False, text_lemmatization=False, special_char_removal=False)
    ntc = NGramTagChunker(train_data)

    chunked_corpus = []

    for doc in corpus:
        nltk_pos_tagged = pos_tag(doc.split())
        chunked_corpus.append(ntc.parse(nltk_pos_tagged))

    return chunked_corpus
