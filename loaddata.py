#!/usr/bin/env python3

import os

import lxml.html
import elasticsearch

DB_INDEX = 'efe95'

es = elasticsearch.Elasticsearch()
es.indices.delete(DB_INDEX, ignore=404)
es.indices.create(DB_INDEX)
es.indices.put_mapping('doc', {
    'properties': {
        'title': {
            'type': 'string',
            'fields': {
                'spanish': {
                    'type': 'string',
                    'analyzer': 'spanish',
                }
            }
        },
        'narr': {
            'type': 'string',
            'fields': {
                'spanish': {
                    'type': 'string',
                    'analyzer': 'spanish',
                }
            }
        },
    }
}, DB_INDEX)

for filename in sorted(os.listdir('efe95')):
    print('Loading ', filename)
    with open('efe95/{}'.format(filename), encoding='iso-8859-1') as data:
        docs = lxml.html.fragments_fromstring(data.read())
    print('Loaded ', filename)
    for doc in docs:
        body = {child.tag: child.text for child in doc.iterchildren()}
        es.create(DB_INDEX, 'doc', body, id=body['docid'], ignore=409)
    print('Finished writing documents from ', filename)
