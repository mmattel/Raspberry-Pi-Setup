# Installing Adminer

Adminer is a tool providing a GUI to manage database servers like mariadb/mysql. Note that Adminer will connect, as far I understand it, to the default port the database provides.

Adminer is helpful when migrating from SQLite to mariadb and for backups.

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

When the adminer AND the mariadb container are running, you can access adminer via `http://<your-server/ip>:8092`.

Note, use your "normal" madiadb account definded with docker-compose and root:<db-root-pwd> for root access.
