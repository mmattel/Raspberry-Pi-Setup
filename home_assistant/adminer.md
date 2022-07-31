# Installing Adminer

Adminer is a tool providing a GUI to manage a database servers like mariadb/mysql.

## Installing via Docker Compose

```
version: "3.8"
services:
  adminer:
    image: adminer:latest
    container_name: adminer
    environment:
      ADMINER_DEFAULT_SERVER: <fqdn-of-the-RPi>
    restart: always
    ports:
      - 8092:8080
```

When the container is running, you can access adminer via `http://<your-server/ip>:8092`
