#! /bin/bash
#set -x
#debug=1

echo
echo "stopping the HA supervisor container"
container1=$(docker container ls --format="{{.Image}} {{.ID}}" | grep "hassio-supervisor" | cut -d' ' -f2 | tr '\n' ' ' | xargs)
if [ $debug ]; then
  echo "would stop HA supervisor container: $container1"
else
  if [ "$container1" ]; then
    docker stop $container1
  fi
fi

#exit

echo
echo "stop the remaining HA containers"
# get the list of all HA containers
container2=($(docker container ls --format="{{.Image}} {{.ID}}" | grep "hassio\|home-assistant" | cut -d' ' -f2 | tr '\n' ' ' | xargs))
# the supervisor container is already stopped so exclude it from the array
container3=("${container2[@]/$container1}")

if [ $debug ]; then
  echo "list of all HA containers: ${container2[@]}"
  echo "would stop remaining HA containers: ${container3[@]}"
else
  if [ "$container3" ]; then
    docker stop ${container3[@]}
  fi
fi

echo
echo "remove all HA containers"
if [ $debug ]; then
  echo "would remove all HA containers: ${container2[@]}"
else
  if [ "$container2" ]; then
    # for what reason ever, it prints c2 properly but it does not work when removing with c2
    docker rm $container1
    docker rm ${container3[@]}
  fi
fi

#exit

echo
echo "remove all HA images"
container4=($(docker images --format="{{.Repository}} {{.ID}}" | grep "hassio\|homeassistant" | cut -d' ' -f2 | tr '\n' ' ' | xargs))
if [ $debug ]; then
  echo "would remove all HA images: ${container4[@]}"
else
  if [ "$container4" ]; then
    docker rmi ${container4[@]}
  fi
fi

# print the remaining images to proof image deletion
echo
if [ $debug ]; then
  echo "would print all remaining images"
else
  docker images | (sed -u 1q; sort)
fi

echo
echo "to get the latest stable supervisor tag (not latest or .devxxx) check:"
echo -e "\e[1;36mhttps://github.com/home-assistant/supervisor\e[0m"
echo "and adapt the image version of the HA supervisor compose file accordingly."
