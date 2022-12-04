#! /bin/bash
#set -x
#debug=1
# https://docs.portainer.io/start/upgrade/docker
version="ee"

echo "stopping the Portainer container"
container1=$(docker container ls --format="{{.Image}} {{.ID}}" | grep "portainer/portainer-$version" | cut -d' ' -f2 | tr '\n' ' ' | xargs)
if [ $debug ]; then
  echo "would stop the Portainer container: $container1"
else
  if [ "$container1" ]; then
    docker stop $container1
  fi
fi

#exit

echo
echo "remove the Portainer container"
if [ $debug ]; then
  echo "would remove the Portainer container: $container1"
else
  if [ "$container1" ]; then
    docker rm $container1
  fi
fi

#exit

echo
echo "remove the Portainer image"
container2=($(docker images --format="{{.Repository}} {{.ID}}" | grep "portainer/portainer-$version" | cut -d' ' -f2 | tr '\n' ' ' | xargs))
if [ $debug ]; then
  echo "would remove the Portainer image: $container2"
else
  if [ "$container2" ]; then
    docker rmi $container2
  fi
fi

#exit

echo
echo "pull the latest Portainer $version container"
docker pull portainer/portainer-$version:latest

# exit

echo
echo "start the pulled Portainer container"
docker run -d -p 8000:8000 -p 9443:9443 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-$version:latest

echo
echo "done"
echo
