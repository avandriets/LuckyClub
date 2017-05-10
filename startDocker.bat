#!/bin/bash
imageName=lucky-club-image
containerName=lucky-club-container

docker build -t $imageName -f Dockerfile  .

echo Delete old container...
docker rm -f $containerName

echo Run new container...
docker run -d -p 4000:8000 --name $containerName $imageName
