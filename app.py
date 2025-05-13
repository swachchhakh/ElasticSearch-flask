from pyexpat import model
import re
from flask import Flask, json, jsonify, render_template, request
from Search import Search
import json
from urllib.request import urlopen
from elasticsearch import Elasticsearch

app = Flask(__name__)
            
es = Search()

@app.get('/')
def index():
    return render_template('index.html')

@app.post('/')
def handle_search():
    query = request.form.get('query', '')
    from_ = request.form.get('from_', type=int, default=0)
    results = es.search(
        query={
            'multi_match': {
                'query': query,
                'fields': ['name', 'summary', 'content'],
            }
        }, size=5, from_= from_
    )
    return render_template('index.html', results=results['hits']['hits'],
                           query=query, from_=0,
                           total=results['hits']['total']['value'])



@app.get('/document/<id>')
def get_document(id):
    document = es.retrieve_document(id)
    title = document['_source']['name']
    paragraphs = document['_source']['content'].split('\n')
    return render_template('document.html', title=title, paragraphs=paragraphs)


@app.cli.command("index")
def reindex():
    response = es.reindex()
    print(f'Index with {len(response["items"])} documents created '
          f'in {response["took"]} milliseconds.')