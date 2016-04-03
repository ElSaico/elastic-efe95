#!/usr/bin/env python3

import os

import lxml.html
import elasticsearch

DB_INDEX = 'efe95'

es = elasticsearch.Elasticsearch()
es.indices.create(index='efe95', ignore=400)

for filename in sorted(os.listdir('efe95')):
    print('Loading ', filename)
    with open('efe95/{}'.format(filename), encoding='iso-8859-1') as data:
        docs = lxml.html.fragments_fromstring(data.read())
    print('Loaded ', filename)
    for doc in docs:
        body = {child.tag: child.text for child in doc.iterchildren()}
        print('Writing document {} from {}'.format(body['docid'], filename))
        es.create(DB_INDEX, 'doc', body, id=body['docid'], ignore=409)
        print('Wrote document {} from {}'.format(body['docid'], filename))
    print('Finished writing documents from ', filename)
