from flask import Flask, request, jsonify
from pprint import pprint
import sys, json, os
import elasticsearch as es
from elasticsearch import helpers
import argparse

app = Flask(__name__)
client = es.Elasticsearch(hosts=[{'host': os.environ['db_host'], 'port': os.environ['db_port']}])


# API functions 

# Search for a person with username
@app.route('/search/<string:id>', methods=['GET'])
def searchAll(id):
    print("Input ID: {}".format(id))
    doc = {
        "query": {
            "simple_query_string" : {
                "fields" : ["username"],
                "query" : "{}".format(id)
            }
        }
    }
        
    res = client.search(index='people', doc_type='profile', body=doc)
    return jsonify(res)

# Delete a Person using their username
@app.route('/people/<string:id>', methods=['DELETE'])
def DELETE_PEOPLE(id):
    '''
    Deletes a person using their username 
    '''
    doc = {
        "query": {
            "simple_query_string" : {
                "fields" : ["username"],
                "query" : "{}".format(id)
            }
        }
    }
    res = client.delete_by_query(index="people",doc_type="profile", body=doc)
    return jsonify(res)
     

#  Get all the people
@app.route('/people', methods=['GET'])
def people():

    page = request.args.get('page')

    # if note page number is given default to page 0
    if page is None:
        page=0

    doc = {
            "from" : page, "size" : 20,
            'query': {
                'match_all' : {}
        }
    }
    res = client.search(index='people', doc_type='profile', body=doc)

    return jsonify(**res)

def loadData(data_file, index_name):
    
    mappings = {
        "profile" : {
            "properties" : {
                "job": { "type" : "string", "store" : True },
                "company": { "type" : "string"},
                "ssn": { "type" : "string", "store" : True },
                "residence": { "type" : "string"},
                "current_location": { "type" : "string" },
                "blood_group": { "type" : "string"},
                "website": {"type": "string"},
                "username": { "type" : "string", "store" : True },
                "name": { "type" : "string", "store" : True },
                "sex": { "type" : "string", "store" : True },
                "address": { "type" : "string"},
                "mail": { "type" : "string"},
                "birthdate": { "type" : "date"}
            }
        }
    }

    body = {'mappings': mappings}

    # Create Index and people profile
    try:
        client.indices.create(index=index_name, body=body)
    except es.exceptions.TransportError as e:
        if e.error != 'index_already_exists_exception':
            raise
    
    json_docs = []
    actions= []
    # Loads the json used in the first program argument
    with open(data_file) as json_data:
        json_docs = json.load(json_data)

    for the_instance in json_docs:
            actions.append({
                "_index": index_name,
                "_type": 'profile',
                "_source": the_instance
            })
    # Bulk load to btach import the json to elasticsearch, to reduce overhead from making network requests. 
    # Relies of python to close connection.
    r, _ = helpers.bulk(client, actions, index=index_name, doc_type='profile', refresh=True)
    print("Inserted: {} documents".format(r))

    


if __name__ == '__main__':

    # Instantiate the parser
    parser = argparse.ArgumentParser(description='Rest Api for Json data') 

    # Json file to be loaded
    parser.add_argument('--load', type=str,
                    help='Json file to be loaded')

    parser.add_argument('--index', type=str,
                    help='index to add into elastic search')


    args = parser.parse_args()

    if args.load is not None and args.index is not None:
        print(args.load, args.index)
        loadData(args.load, args.index)

    app.run(debug=False,host='0.0.0.0')


 

