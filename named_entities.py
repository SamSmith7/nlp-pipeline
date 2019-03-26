import pandas as pd
import en_core_web_md


nlp = en_core_web_md.load(parse=True, tag=True, entity=True)

def parse(docs):

    named_entities = []

    for doc in docs:

        temp_entity_name = ''
        temp_named_entity = None

        for word in nlp(doc):

            term = word.text
            tag = word.ent_type_

            if tag:
                temp_entity_name = ' '.join([temp_entity_name, term]).strip()
                temp_named_entity = (temp_entity_name, tag)
            else:
                if temp_named_entity:
                    named_entities.append(temp_named_entity)
                    temp_entity_name = ''
                    temp_named_entity = None

    entities = pd.DataFrame(named_entities, columns=['Entity Name', 'Entity Type'])

    return (entities.groupby(by=['Entity Name', 'Entity Type'])
        .size()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={0 : 'Frequency'}))
