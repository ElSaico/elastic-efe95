#!/usr/bin/env python3

import os

import lxml.html
import elasticsearch
import elasticsearch.helpers as es_helpers

DB_INDEX = 'efe95'
DOC_TYPE = 'doc'

es = elasticsearch.Elasticsearch()
es.indices.delete(DB_INDEX, ignore=404)
es.indices.create(DB_INDEX, {
    'settings': {
        'analysis': {
            'filter': {
                'spanish_stop': {
                    'type': 'stop',
                    'stopwords': '_spanish_',
                },
                'spanish_stemmer': {
                    'type': 'stemmer',
                    'language': 'light_spanish',
                },
            },
            'analyzer': {
                'spanish': {
                    'tokenizer': 'standard',
                    'filter': [
                        'lowercase',
                        'spanish_stop',
                        'spanish_stemmer',
                        'shingle',
                    ]
                }
            }
        }
    },
    'mappings': {
        DOC_TYPE: {
            'properties': {
                'title': {
                    'type': 'string',
                    'analyzer': 'spanish',
                },
                'narr': {
                    'type': 'string',
                    'analyzer': 'spanish',
                },
            }
        }
    }
})


def actions(docs):
    for doc in docs:
        body = {child.tag: child.text for child in doc.iterchildren()}
        yield {
            '_op_type': 'create',
            '_index': DB_INDEX,
            '_type': DOC_TYPE,
            '_id': body['docid'],
            '_source': body,
        }

for filename in sorted(os.listdir('efe95')):
    with open('efe95/{}'.format(filename), encoding='iso-8859-1') as data:
        docs = lxml.html.fragments_fromstring(data.read())
    for success, info in es_helpers.parallel_bulk(es, actions(docs)):
        pass
