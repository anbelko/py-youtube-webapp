FROM python:alpine3.17
RUN pip install flask Pillow pytube
COPY . /opt/
EXPOSE 8080
WORKDIR /opt
ENTRYPOINT ["python", "app.py"]
