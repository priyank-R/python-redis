# python-redis

A simple implementation of redis in python, referring the implementation from Arpit Bhayani's Redis Internals series.

# Helpful Commands: 
- Running the server: 

`python main.py <host> <port>`

- Connect using redis-cli using a one-off docker instance: 

`docker run --rm -it redis:alpine redis-cli -h host.docker.internal -p 7639`

- Run Redis Server locally and connect it using CLI:
`docker run --rm -it -p 6379:6379 redis:alpine`
`docker run --rm -it redis:alpine redis-cli -h host.docker.internal -p 6379`

- Benchmarking the SERVER WITH 10000 requests, 1 concurrent user, redis ping command

`docker run --rm -it redis:alpine redis-benchmark -n 10000 -t ping_mbulk -c 1 -h host.docker.internal -p 7379`