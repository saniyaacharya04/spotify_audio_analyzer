.PHONY: run test docker-build docker-run

run:
	uvicorn src.main:app --reload

test:
	rm -f usage.db
	pytest -v

docker-build:
	docker build -f docker/Dockerfile -t spotify-audio-analyzer .

docker-run:
	docker run -p 8000:8000 spotify-audio-analyzer
