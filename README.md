# Setup
## Run:
`docker-compose up -d`

## Log in into the container
```
~$ docker exec -it ${CONTAINER-NAME} bash
```

You can see the name of the container running `docker-compose ps`
```
~$ docker-compose ps
          Name                       Command             State                 Ports              
--------------------------------------------------------------------------------------------------
email_fetcher_cabin_db_1   docker-entrypoint.sh mysqld   Up      0.0.0.0:3306->3306/tcp, 33060/tcp
```

## Once in the container. Log in into the mysql server.
```
root@c59b42e9c9ca:/# mysql -u user -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 12
Server version: 8.0.19 MySQL Community Server - GPL

Copyright (c) 2000, 2020, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| gemails            |
| information_schema |
+--------------------+
2 rows in set (0.00 sec)

```
