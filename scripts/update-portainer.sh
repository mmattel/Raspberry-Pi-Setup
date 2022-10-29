#! /bin/bash
#set -x
#debug=1
# https://docs.portainer.io/start/upgrade/docker

echo
echo "stopping the Portainer container"
docker stop portainer

#exit

echo
echo "remove the Portainer containers"
docker rm portainer

#exit

echo
echo "pull the latest Portainer container"
docker pull portainer/portainer-ce:latest

# exit

echo
echo "start the pulled container"
docker run -d -p 8000:8000 -p 9443:9443 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest

echo
echo "done"
echo
