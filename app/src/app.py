from flask import Flask
from pprint import pprint
import sys, json, os
import elasticsearch as es

host = "localhost"
port = 9200
index_name = "people"

app = Flask(__name__)
client = es.Elasticsearch(hosts=[{'host': host, 'port': port}])


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
    return json.dumps(res)

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
    return json.dumps(res)
     

#  Get all the people
@app.route('/people', methods=['GET'])
def people():
    doc = {
            'query': {
                'match_all' : {}
        }
    }
    res = client.search(index='people', doc_type='profile', body=doc)
    return json.dumps(res)

def loadData(data_file):
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

    # Loads the json used in the first program argument
    with open(data_file) as json_data:
        d = json.load(json_data)
        pprint(d)

        for data in d:
            client.index(index=index_name, doc_type='profile',
                            body=data)


if __name__ == '__main__':
    # Add argument handler here!
    # Check for a load flag is so then load the data to popluate elasticSearch

    loadData(sys.argv[1])
    app.run(debug=True,host='0.0.0.0')

