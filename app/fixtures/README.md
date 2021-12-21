# Fixtures

fixtures load data into the db when containers is getting created.

→ see: `.docker/docker-entrypoint.sh`

## generate db dump

```
./manage.py dumpdata auth.user > ./app/fixtures/users.json
```

## load db dump

```
./manage.py loaddata ./app/fixtures/users.json
```
