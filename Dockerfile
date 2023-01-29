FROM amd64/python:3.9.13-slim-buster
WORKDIR /usr/src/app
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
COPY requirement.txt ./
RUN pip3 install --no-cache-dir --upgrade -r requirement.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
