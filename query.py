#!/usr/bin/env python3

import csv

import lxml.etree
import elasticsearch

DB_INDEX = 'efe95'
DOC_TYPE = 'doc'
NAME_LABEL = 'bruno'

es = elasticsearch.Elasticsearch()
outfile_standard = csv.writer(open('results-standard.txt', 'w'), delimiter='\t')
outfile_spanish = csv.writer(open('results-spanish.txt', 'w'), delimiter='\t')
output_standard = (outfile_standard, ['title', 'text'])
output_spanish = (outfile_spanish, ['title.spanish', 'text.spanish'])

with open('queries.xml') as infile:
    root = lxml.etree.parse(infile)

for query in root.xpath('/queries/query'):
    query_id = query.findtext('num')
    title = query.findtext('title')
    narr = query.findtext('narr')
    for outfile, fields in (output_standard, output_spanish):
        search = {
            'query': {
                'bool': {
                    'must': {
                        'match': {fields[1]: title},
                    },
                    'should': [
                        {'multi_match': {'query': title, 'fields': fields}},
                        {'multi_match': {'query': narr, 'fields': fields}},
                    ],
                },
            }
        }
        results = es.search(DB_INDEX, DOC_TYPE, search, size=100)
        for rank, doc in enumerate(results['hits']['hits']):
            output = [query_id, 'Q0', doc['_id'], rank, doc['_score'], NAME_LABEL]
            outfile.writerow(output)
