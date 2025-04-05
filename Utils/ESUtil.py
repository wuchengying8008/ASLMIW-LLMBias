import ssl
from elasticsearch import Elasticsearch
from NLPConstant import ES_HOST, ES_PORT, ES_USER, ES_PASSWORD, ES_SSL_CONTEXT


def get_elasticsearch_client():
  
    context = ssl.create_default_context()
    context.load_verify_locations(ES_SSL_CONTEXT)

   
    es_url = f"https://{ES_HOST}:{ES_PORT}"

    client = Elasticsearch(
        es_url,
        basic_auth=(ES_USER, ES_PASSWORD),
        # verify_certs=False
        ssl_context=context
    )
    return client

def search_elasticsearch(index, query):
    client = get_elasticsearch_client()
    result = client.search(index=index, body=query)
    return result

def index_document(index, document):
    client = get_elasticsearch_client()
    result = client.index(index=index, body=document)
    return result

def get_document(index, doc_id):
    client = get_elasticsearch_client()
    result = client.get(index=index, id=doc_id)
    return result