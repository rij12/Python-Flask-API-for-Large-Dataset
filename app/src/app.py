from flask import Flask, request, jsonify
from pprint import pprint
import sys, json, os
import elasticsearch as es
from elasticsearch import helpers
from config import config

app = Flask(__name__)
client = es.Elasticsearch(hosts=[{'host': config['db_host'], 'port': config['db_port']}])


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
        # here we want to get the value of user (i.e. ?user=some-value)
    page = request.args.get('page')
    print(page)

    if page is None:
        page=0
    doc = {
            "from" : page, "size" : 10,
            'query': {
                'match_all' : {}
        }
    }
    res = client.search(index='people', doc_type='profile', body=doc)

    return jsonify(res)

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
        client.indices.create(index="people", body=body)
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
                "_index": 'people',
                "_type": 'profile',
                "_source": the_instance
            })
    # Bulk load to btach import the json to elasticsearch, to reduce overhead from making network requests. 
    r, _ = helpers.bulk(client, actions, index='people', doc_type='profile', refresh=True)
    print("Inserted: {} documents".format(r))

    


if __name__ == '__main__':
    # Add argument handler here!
    # Check for a load flag is so then load the data to popluate elasticSearch

    # loadData(sys.argv[1], "people")
    app.run(debug=True,host='0.0.0.0')

