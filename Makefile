docker-build:
	docker build -t cereal .

docker-run:
	docker run --rm -p 8000:8000 --name cereal cereal
