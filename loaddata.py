#!/usr/bin/env python3

import os

import lxml.html
import elasticsearch
import elasticsearch.helpers as es_helpers

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


def actions(docs):
    for doc in docs:
        body = {child.tag: child.text for child in doc.iterchildren()}
        yield {
            '_op_type': 'create',
            '_index': DB_INDEX,
            '_type': 'doc',
            '_id': body['docid'],
            '_source': body,
        }

for filename in sorted(os.listdir('efe95')):
    print('Loading ', filename)
    with open('efe95/{}'.format(filename), encoding='iso-8859-1') as data:
        docs = lxml.html.fragments_fromstring(data.read())
    print('Loaded ', filename)
    for success, info in es_helpers.parallel_bulk(es, actions(docs)):
        pass
    print('Finished writing documents from ', filename)
