FROM python:3.10-alpine
WORKDIR /project/project
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY ./project ./project
EXPOSE 5003
CMD ["python", "project/app.py"]
