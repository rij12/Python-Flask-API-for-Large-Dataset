# # Create the people index.
# curl -XPUT http://localhost:9200/people?pretty=true -d '
# {
#     "settings" : {
#         "index" : {
#             "number_of_shards" : 5,
#             "number_of_replicas" : 0
#         }
#     }
# }
# '

# # Create the people mapping in the database. 
# curl -XPUT http://localhost:9200/people/_mapping/profile?pretty=true -d '
# {
#     "profile" : {
#         "properties" : {
#             "job": { "type" : "string", "store" : true },
#             "company": { "type" : "string"},
#             "ssn": { "type" : "string", "store" : true },
#             "residence": { "type" : "string"},
#             "current_location": { "type" : "geo_point" },
#             "blood_group": { "type" : "string"},
#             "website": {"type": "string"},
#             "username": { "type" : "string", "store" : true },
#             "name": { "type" : "string", "store" : true },
#             "sex": { "type" : "string", "store" : true },
#             "address": { "type" : "string"},
#             "mail": { "type" : "string"},
#             "birthdate": { "type" : "date"}
#         }
#     }
# }
# '

# Show all content 

# curl http://localhost:9200/people/profile/_search?q=*


# Import the json into the database.
# curl -XPOST  http://localhost:9200/people -d @fake_profiles.json

curl -s -XPOST http://localhost:9200/people/profile/_bulk --data-binary @fake_profiles.json