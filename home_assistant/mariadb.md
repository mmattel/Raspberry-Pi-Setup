# Installing MariaDB

This database will be used for Home Assistant instead the embedded SQLlite database. The user and the database are created automatically when starting the container for the first time.

## Installing via Docker Compose

We are using mariadb version 10.6.8 as this version has long term support until July 2026, use the directory `/home/<your-user>/docker` as base for the volume.


```
version: "3.8"
services:
  mariadb:
    image: mariadb:10.6.8  # long term support until July 2026
    container_name: mariadb-hass
    restart: always
    logging:
      driver: "json-file"
      options:
        max-size: "200k"
        max-file: "10"
    environment:
      MYSQL_USER: <db-user>
      MYSQL_PASSWORD: <db-pwd>
      MYSQL_ROOT_PASSWORD: <db-root-pwd>
      MYSQL_DATABASE: hass
    ports:
      - 3306:3306
    volumes:
      - /home/<your-user>/docker/mariadb/data:/var/lib/mysql
```
For normal access to login use <db-user>:<db-pwd>. For root access use root:<db-root-pwd>.
