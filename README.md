# Simple Recommendation System

This system consists of two services:

1. Generator: Generates recommendations.
2. Invoker: Retrieves recommendations and checks the cache.

Both services offer auto-generated FastAPI documentation accessible at the /docs endpoint.

### Generator
This service is a Python FastAPI application with a POST /generate endpoint. 
It requires two parameters: model_name and viewerid. 
The service generates a random number and returns a JSON response of the type: 
```json
{
  "reason": "<MODELNAME>",
  "result": "<RANDOMNUMBER>"
}
```

### Invoker
This service is a Python FastAPI application with a GET /recommend endpoint. 
It takes a single query parameter: viewer_id. 
The service first checks the cache for the given user. The service uses two levels of caching:

1. Local: with a TTL of 10 seconds and 3 keys limit
2. Redis
If no data is found in the cache, it calls the Generator service.

Example request
```sh
http://0.0.0.0:8891/recommend?viewer_id=123
```

#### Invoker environment variables

| Environment Variable | Description                                         | Value                                   |
|----------------------|-----------------------------------------------------|-----------------------------------------|
| MODEL_REGISTRY       | Path to register of available recommendation models | 'resources/model_registry.json'         |
| GENERATOR_URL        | Generator service URL                               | 'http://recommendations_generator:8890' |
| NUM_MODELS           | Number of models used for recommendation requests   | 5                                       |
| REDIS_URL            | Redis URL                                           | 'redis://redis_cache'                   |

## Installation and running

Navigate to the directory containing your docker-compose.yml file and execute

```sh
docker-compose up
```
