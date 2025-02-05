# SampleFlaskAPI
This is a demo FlaskAPI for a simple genomic variants non-relational database

## Features
 - Mongo DB Schema 
 - Dockerized (with docker-compose)
 - AWS Lambda docker configuration
 - JWT Auth

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

## AUTH ENDPOINTS
### POST /register
    - req body: {"name": "my name", "email": "test@email.com", "password": "secretPassword"}
### POST /refresh
    - req cookie: refreshToken
### POST /user_auth (login)
    - req body: {"email": "test@email.com", "password": "secretPassword"}
### GET /user_auth/{id} (logout, Private)

### DELETE /user_auth/{id} (Private)


## VARIANT ENDPOINTS

### GET /variants
### GET /variants/{id}
### PUT /variants/{id} (Private)
    - req header: Authorization: Bearer <auth_token>
    - req body: {"chr": "chr1", "pos": 12345, "ref": "a", "alt": "g", "variant_type": "SUBSTITUTION", "quality": 80.0}
### Patch /variants/{id} (Private)
    - req header: Authorization: Bearer <auth_token>
    - req body: {"chr": "chr1", "pos": 12345, "ref": "a", "alt": "g", "variant_type": "SUBSTITUTION", "quality": 80.0}
### DELETE /variants/{id} (Private)
    - req header: Authorization: Bearer <auth_token>


## In Progress
 - Parameter validation
 - App Security (auth, rate limits, cors)
 - Unit testing
 - Functional testing
 - Error handling


## To Do:
 - Swagger Documentation
 - Code Annotation