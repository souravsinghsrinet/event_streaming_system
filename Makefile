IMAGE_NAME = event_streaming_service:v1
CONTAINER_NAME = event_streaming_service

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run --env-file=app.env -p 8000:8080 --name $(CONTAINER_NAME) $(IMAGE_NAME)

remove:
	docker rm $(CONTAINER_NAME)

rebuild:
	make build
	make remove
	make run
