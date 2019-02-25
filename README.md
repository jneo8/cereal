# cereal

## import data

**replace {file-path} to real file path**

```
cd cereal && python manage.py import_order {file-path}
```

```
cd cereal && python manage.py import_orderitem {file-path}
```

## use docker

```
make docker-build && make docker-run
```

**To import data in docker, you need to docker cp file into container.**
