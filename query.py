#!/usr/bin/env python3

import csv

import lxml.etree
import elasticsearch

DB_INDEX = 'efe95'
NAME_LABEL = 'bruno'

es = elasticsearch.Elasticsearch()
outfile = csv.writer(open('results.txt', 'w'), delimiter='\t')

with open('queries.xml') as infile:
    root = lxml.etree.parse(infile)

for query in root.xpath('/queries/query'):
    query_id = query.findtext('num')
    title = query.findtext('title')
    narr = query.findtext('narr')
    search = {
        'query': {
            'multi_match': {
                'query': title+narr,
                'fields': ['title', 'text'],
            },
        }
    }
    results = es.search(DB_INDEX, 'doc', search, size=100)
    for rank, doc in enumerate(results['hits']['hits']):
        output = [query_id, 'Q0', doc['_id'], rank, doc['_score'], NAME_LABEL]
        outfile.writerow(output)
