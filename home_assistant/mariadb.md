# Installing MariaDB

This database will be used for Home Assistant instead the embedded SQLlite database.

## Installing via Docker Compose

We are using mariadb version 10.6.8 as this has long term support until July 2026

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
      MYSQL_USER: <a-db-user>
      MYSQL_PASSWORD: <a-db-pwd>
      MYSQL_ROOT_PASSWORD: <a-db-root-pwd>
      MYSQL_DATABASE: hass
    ports:
      - 3306:3306
    volumes:
      - /home/<your-user>/docker/mariadb/data:/var/lib/mysql
      - /home/<your-user>/docker/mariadb/conf:/etc/mysql/conf.d
      # - /home/<your-user>/docker/mariadb/logs:...
```
