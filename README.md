# SampleFlaskAPI
This is a demo FlaskAPI for a bioinformatics variant database

## Features
 - Mongo DB Schema 
 - Dockerized (with docker-compose)
 - AWS Lambda docker configuration

## Programming Languages, Frameworks and Platforms
 - Python3
 - MongoDb
 - Flask
 - Docker

## Cmds
```
    pip install -r src/requirements
    python3 src/app.py runserver
    docker-compose build app
```

### test api: http://localhost:5002/

## VARIANT ENDPOINTS
### GET /variants
### GET /variants/{id}
### PUT /variants/{id}
 - req body: {"chr": "chr1", "pos": 12345, "ref": "a", "alt": "g", "variant_type": "SUBSTITUTION", "quality": 80.0}
### Patch /products/{id}
 - req body: {"chr": "chr1", "pos": 12345, "ref": "a", "alt": "g", "variant_type": "SUBSTITUTION", "quality": 80.0}
### DELETE /products/{id}


## In Progress
 - Parameter validation aspect
 - Complete Unit Tests
 - Code Annotation


## To Do:
 - Swagger Documentation
 - App Security
 - API Authentication + Middleware (aspect/ interceptor) and private endpoints
 - Unit Tests
 - Rate Limits (20 req per min)
 - AWS Lambda deployed to API Gateway
 - email attachment