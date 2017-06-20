#!/bin/bash
#imageName=lucky-club-image
#containerName=lucky-club-container

docker build -t lucky-club-image -f Dockerfile  .

echo Delete old container...
docker rm -f lucky-club-container

echo Run new container...
docker run -d -p 4000:8000 --name lucky-club-container lucky-club-image
