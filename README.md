# Python Flask API for ElasticSearch 

Python Flask API for large data of people. 

## 

## Technologies
* Python 
* Flask
* ElasticSearch
* Docker & Docker-Compose

# Install

```
chmod +x run.sh
./run.sh
```
# Run

```
localhost:5000
```

## API

```
DELETE - '/people/<string:id>'
GET - '/search/<string:id>'
GET - '/people'



```

# Limitataions

* It loads the whole file into RAM, would need to stream it or batch load the data for much bigger files.

