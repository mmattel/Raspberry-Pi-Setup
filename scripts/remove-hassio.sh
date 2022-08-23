#! /bin/bash

echo "stopping the HA supervisor container"
container1=$(docker container ls --format="{{.Image}} {{.ID}}" |
grep "hassio-supervisor" | cut -d' ' -f2)
#echo $container1
if [ "$container" ]; then
  docker stop $container1
  docker wait $container1
fi

echo "stop the remaining HA containers, waiting"
container2=$(docker container ls --format="{{.Image}} {{.ID}}" |
grep "hassio\|home-assistant" | cut -d' ' -f2)

container2=$(echo ${container2//$container1/} | xargs)
#echo $container2
if [ "$container2" ]; then
  docker stop $container2
  docker wait $container2
fi
#exit

echo "remove all HA containers"
container3=$(docker images --format="{{.Repository}} {{.ID}}" |
grep "hassio\|homeassistant" | cut -d' ' -f2)

if [ "$container3" ]; then
  docker rmi -f $container3
fi

echo

# print the remaining images to proof image deletion
docker images

echo
echo "check: https://hub.docker.com/r/homeassistant/armv7-hassio-supervisor/tags?page=1"
echo "to get the latest stable supervisor tag (not latest or .devxxx)"

