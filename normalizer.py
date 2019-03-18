from contractions import CONTRACTION_MAP
import normalisation_utils
import re


def normalize_corpus(corpus, html_stripping=True, contraction_expansion=True,
                     accented_char_removal=True, text_lower_case=True,
                     text_lemmatization=True, special_char_removal=True,
                     stopword_removal=True, remove_digits=True):

    normalized_corpus = []

    for doc in corpus:

        if html_stripping:
            doc = normalisation_utils.strip_html(doc)

        if accented_char_removal:
            doc = normalisation_utils.remove_accented_chars(doc)

        if contraction_expansion:
            doc = normalisation_utils.expand_contractions(doc, CONTRACTION_MAP)

        if text_lower_case:
            doc = doc.lower()

        doc = re.sub(r'[\r|\n|\r\n]+', ' ', doc)

        if text_lemmatization:
            doc = normalisation_utils.lemmatize_text(doc)

        if special_char_removal:
            special_char_pattern = re.compile(r'([{.(-)!}])')
            doc = special_char_pattern.sub(' \\1', doc)
            doc = normalisation_utils.remove_special_chars(doc, remove_digits)

        doc = re.sub(' +', ' ', doc)

        if stopword_removal:
            doc = normalisation_utils.remove_stopwords(doc, text_lower_case)

        normalized_corpus.append(doc)

    return normalized_corpus
