import json
from pprint import pprint
import os
import time
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

class Search:
    def __init__(self):
        self.es = Elasticsearch(
             "https://localhost:9200",
             basic_auth=("elastic", "_68zFrkZyFKL26dxfvAY"),
             verify_certs=False,
            
        )
    def create_index(self):
        self.es.indices.delete(index='aftab_11', ignore_unavailable=True)
        self.es.indices.create(index='aftab_11')   
        
    def insert_documents(self, documents):
        operations = []
        for document in documents:
            operations.append({'index': {'_index': 'aftab_11'}})
            operations.append(document)
        return self.es.bulk(operations=operations)

    def retrieve_document(self, id):
        return self.es.get(index='aftab_11', id=id)
    
    def search(self, **query_args):
        return self.es.search(index='aftab_11', **query_args)

    def search_documents(self, query):  
        search_body = {
            "query": {
                "match": {
                    "content": query
                }
            }
        }
        response = self.es.search(index='aftab_11', body=search_body)
        return response['hits']['hits']

    def reindex(self):
        self.create_index()
        with open('data.json', 'rt') as f:
            documents = json.loads(f.read())
        return self.insert_documents(documents)
  



   

   
