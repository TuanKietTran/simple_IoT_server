FROM python:3.11.1-slim-buster
RUN apt update && apt upgrade -y
COPY . /app
WORKDIR /app
RUN python3 -m pip install -r requirements.txt
EXPOSE 4000
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]