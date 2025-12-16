#declare what image to use
FROM python:3.13.4-slim-bullseye

WORKDIR /app

#RUN mkdir -p /static_folder
#COPY ./static_html /static_folder


COPY ./src .

#RUN echo "hello" > index.html

#docker login

#docker build -f Dockerfile -t pyapp .
#docker run -it pyapp

#docker build -f Dockerfile -t tracef/ai_agent:v1 .
#docker push tracef/ai_agent:v1

#python -m http.server 8000
#docker run -it -p 8080:8000 pyapp
#docker run -it -p 4000:8000 pyapp
CMD ["python", "-m", "http.server", "8000"]