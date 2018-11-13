#!/bin/sh

if [ "$#" -ne 1 ]
then
  echo "Send the token as argument"
  exit 1
fi

docker stop discordbot
docker rm discordbot
docker build -t discordbot .
docker run -d -e TOKEN=$1 --restart always --name discordbot discordbot