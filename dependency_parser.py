import en_core_web_md


nlp = en_core_web_md.load(parse=True, tag=True, entity=True)
dep_pattern = '{left}<---{word}[{w_type}]--->{right}\n-------'

def parse(docs):

    parsed_docs = []

    for idx, doc in enumerate(docs):
        print('Processing doc:', idx)
        parsed_doc = []
        for sent in doc.split('.'):
            sent_nlp = nlp(sent)
            parsed_sent = []
            for token in sent_nlp:
                parsed_token = dep_pattern.format(
                    word=token.orth_,
                    w_type=token.dep_,
                    left=[t.orth_ for t in token.lefts],
                    right=[t.orth_ for t in token.rights]
                )
                parsed_sent.append(parsed_token)
            parsed_doc.append(parsed_sent)
        parsed_docs.append(parsed_doc)

    return parsed_docs
