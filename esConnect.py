import traceback
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, AuthenticationException, SSLError, TransportError

def test_es_connection():
    try:
      
        es = Elasticsearch(
            hosts=['https://127.0.0.1:9200'],
            basic_auth=('elastic', '1111111'),
            ca_certs="D:\\tools\elasticsearch\combined.crt",  
            verify_certs=True  
        )

       
        if es.ping():
            print('Connected to Elasticsearch')
        else:
            try:
               
                es.info()
            except (ConnectionError, AuthenticationException, SSLError, TransportError) as e:
                print(traceback.format_exc())
    except ConnectionError as e:
        print(f"Error message: {str(e)}")
        print(traceback.format_exc())


if __name__ == "__main__":
    test_es_connection()