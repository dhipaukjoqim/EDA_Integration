#Containerization with Docker
In the root directory of the project,


For the backend,
docker build -f Dockerfile.api -t react-flask-app-api .
docker run --rm -p 5000:5000 react-flask-app-api

For frontend,
docker build -f Dockerfile.client -t react-flask-app-client .
docker run --rm -p 8082:3000 react-flask-app-client


Visit http://10.115.1.185:8082/