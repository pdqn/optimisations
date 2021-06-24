# Example to show asysnc await gains

## Essentially run the server once with async await and once without to compare the latency.
```
docker build -t tornado-async-example .
docker run -dp 8889:8889 tornado-async-example

GET - http://localhost:8889/ping
```

WIP - facing some issues with skaffold dev.

